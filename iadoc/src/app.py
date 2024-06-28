from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os
import logging
from iadoc.src.modules.auth import authenticate_google, get_google_services
from iadoc.src.modules.document import duplicate_document, replace_text_in_document, convert_document_to_pdf, create_folder, move_file_to_folder, share_file_with_email
from iadoc.src.modules.email_sender import send_email_with_attachment

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

iadoc_app = Blueprint('iadoc_app', __name__)

# Carregar informações da conta de serviço do arquivo JSON
service_account_info_json_path = os.path.join(os.path.dirname(__file__), 'service_account_info.json')
if not os.path.exists(service_account_info_json_path):
    logger.error(f"Arquivo de credenciais de conta de serviço não encontrado: {service_account_info_json_path}")
    raise FileNotFoundError(f"Arquivo de credenciais de conta de serviço não encontrado: {service_account_info_json_path}")

with open(service_account_info_json_path) as f:
    service_account_info_json = f.read()

# Verificação da chave privada no JSON
try:
    service_account_info = json.loads(service_account_info_json)
    private_key = service_account_info.get('private_key')
    if not private_key.startswith('-----BEGIN PRIVATE KEY-----') or not private_key.endswith('-----END PRIVATE KEY-----\n'):
        logger.error("Formato da chave privada no JSON está incorreto.")
        raise ValueError("Formato da chave privada no JSON está incorreto.")
except json.JSONDecodeError as e:
    logger.error(f"Erro ao carregar JSON de credenciais: {e}")
    raise

@iadoc_app.route('/', methods=['POST'])
def process_document():
    try:
        # Carregar dados do JSON enviado na requisição
        data = request.get_json()
        logger.info("Dados JSON recebidos: %s", data)

        if not data or "proposta" not in data or "cliente" not in data["proposta"]:
            logger.error("Dados JSON incompletos ou mal formatados")
            return jsonify({'error': 'Dados JSON incompletos ou mal formatados'}), 400

        empresa_nome = data["proposta"]["cliente"]["empresa"]
        timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        new_document_title = f'{empresa_nome}-{timestamp}'
        logger.info("Novo título do documento: %s", new_document_title)

        # Autenticar e criar os serviços Drive e Docs
        creds = authenticate_google(service_account_info_json)
        drive_service, docs_service = get_google_services(creds)

        # Criar pasta com o nome da empresa
        company_folder_id = create_folder(drive_service, empresa_nome, '1xqD5kFf5uaDHGQsC33Fmsl47teXbRAa2')
        logger.info("Pasta criada com ID: %s", company_folder_id)

        # ID do documento de modelo e título do novo documento
        template_file_id = '1b0iKx9vZro4lS2NiBtk9-qE9EtH8YRvgSoj0khxAuM4'
        logger.info("ID do arquivo de modelo: %s", template_file_id)

        # Duplicar o documento
        duplicated_file_id = duplicate_document(drive_service, template_file_id, new_document_title, company_folder_id)
        if not duplicated_file_id:
            logger.error("Falha ao duplicar o documento")
            return jsonify({'error': 'Falha ao duplicar o documento'}), 500
        logger.info("Documento duplicado com ID: %s", duplicated_file_id)

        # Preparar os shortcodes para substituição
        shortcodes = {
            "[DATA]": data["proposta"]["data"],
            "[ANO]": data["proposta"]["ano"],
            "[EMPRESA]": data["proposta"]["cliente"]["empresa"],
            "[OBJETIVODOPROJETO]": data["proposta"]["escopo_do_projeto"]["objetivo_do_projeto"],
            "[XXXX]": data["proposta"]["custo_do_projeto"]["valor_original"],
            "[YYYY]": data["proposta"]["custo_do_projeto"]["valor_a_vista"],
            "[duracaoprojeto]": str(sum(etapa.get("qtd_dias", 0) for etapa in data["proposta"]["etapas_do_projeto"])) + " dias"
        }

        for i, item in enumerate(data["proposta"]["escopo_do_projeto"]["itens_do_escopo"], start=1):
            shortcodes[f"[TITULOITEMESCOPO{i}]"] = item.get("item", "")
            shortcodes[f"[DESCRIÇÃOITEMESCOPO{i}]"] = item.get("descrição", "")

        for i, etapa in enumerate(data["proposta"]["etapas_do_projeto"], start=1):
            shortcodes[f"[TITULOETAPA{i}]"] = etapa.get("titulo_da_etapa", "")
            shortcodes[f"[OBJETIVOETAPA{i}]"] = etapa.get("objetivo", "")
            for j, atividade in enumerate(etapa.get("atividades", []), start=1):
                shortcodes[f"[ETAPA{i}{j}]"] = atividade
            qtd_dias = etapa.get("qtd_dias", 0)
            shortcodes[f"[QTDDIASETAPA{i}]"] = f"{qtd_dias} dia" if qtd_dias == 1 else f"{qtd_dias} dias"

        for i, ferramenta in enumerate(data["proposta"]["metodologia_de_trabalho"]["ferramentas_e_tecnologias_utilizadas"], start=1):
            shortcodes[f"[FERRAMENTA{i}]"] = ferramenta.get("ferramenta", "")
            shortcodes[f"[DESCFERRAMENTA{i}]"] = ferramenta.get("descricao", "")

        all_shortcodes = [
            "[FERRAMENTA6]","[DESCFERRAMENTA6]","[TITULOETAPA7] - [QTDDIASETAPA7]","[FERRAMENTA3]", "[DESCFERRAMENTA3]", "[FERRAMENTA4]", "[DESCFERRAMENTA4]",
            "[FERRAMENTA5]", "[DESCFERRAMENTA5]",
            "[TITULOETAPA7]", "[OBJETIVOETAPA7]", "[ETAPA71]", "[ETAPA72]", "[ETAPA73]",
            "[ETAPA74]", "[ETAPA75]", "Atividades...",
            "[ETAPA11]", "[ETAPA12]", "[ETAPA13]", "[ETAPA14]", "[ETAPA15]",
            "[ETAPA21]", "[ETAPA22]", "[ETAPA23]", "[ETAPA24]", "[ETAPA25]",
            "[ETAPA31]", "[ETAPA32]", "[ETAPA33]", "[ETAPA34]", "[ETAPA35]",
            "[ETAPA41]", "[ETAPA42]", "[ETAPA43]", "[ETAPA44]", "[ETAPA45]",
            "[ETAPA51]", "[ETAPA52]", "[ETAPA53]", "[ETAPA54]", "[ETAPA55]",
            "[ETAPA61]", "[ETAPA62]", "[ETAPA63]", "[ETAPA64]", "[ETAPA65]",
            "[ETAPA71]", "[ETAPA72]", "[ETAPA73]", "[ETAPA74]", "[ETAPA75]"
        ]

        for shortcode in all_shortcodes:
            if shortcode not in shortcodes:
                shortcodes[shortcode] = ""

        replace_text_in_document(docs_service, duplicated_file_id, shortcodes)
        logger.info("Shortcodes substituídos no documento: %s", shortcodes)

        # Converter o documento para PDF e mover para a mesma pasta
        pdf_path = convert_document_to_pdf(drive_service, duplicated_file_id)
        if not pdf_path or not os.path.exists(pdf_path):
            logger.error("Arquivo PDF não encontrado para envio.")
            return jsonify({'error': 'Arquivo PDF não encontrado'}), 500
        logger.info(f"Documento convertido em PDF e salvo em: {pdf_path}")

        # Mover o PDF gerado para a mesma pasta no Google Drive
        pdf_file_id = move_file_to_folder(drive_service, pdf_path, company_folder_id, new_document_title + '.pdf')
        logger.info(f"PDF movido para o Google Drive com ID: {pdf_file_id}")

        # Compartilhar o documento com o email especificado
        share_file_with_email(drive_service, duplicated_file_id, 'ilivindigital@gmail.com')
        share_file_with_email(drive_service, pdf_file_id, 'ilivindigital@gmail.com')
        logger.info("Documento compartilhado com sucesso com ilivindigital@gmail.com")

        # Definindo detalhes do e-mail
        to_address = data["proposta"]["cliente"]["email"]
        subject = 'Documento PDF'
        body = 'Encontre em anexo o documento PDF.'

        # Enviar o e-mail com o anexo
        try:
            send_email_with_attachment(to_address, subject, body, pdf_path)
            logger.info(f"E-mail enviado com sucesso para: {to_address}")
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail: {e}")
            return jsonify({'error': 'Falha ao enviar o e-mail'}), 500

        return jsonify({'message': 'Processo concluído com sucesso'}), 200

    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        return jsonify({'error': str(e)}), 500
