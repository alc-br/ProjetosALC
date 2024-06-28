"""
Este módulo gerencia operações de documentos no Google Docs e Google Drive.

Dependências:
- googleapiclient.discovery
- googleapiclient.http
- json

Autor: Anderson Chipak - Agência ALC
Data: 26/06/2024
"""

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import logging

logger = logging.getLogger(__name__)

def duplicate_document(drive_service, file_id, new_title, parent_folder_id):
    """
    Duplica um documento no Google Drive.

    :param drive_service: Serviço do Google Drive.
    :param file_id: ID do arquivo a ser duplicado.
    :param new_title: Novo título do documento duplicado.
    :param parent_folder_id: ID da pasta de destino.
    :return: ID do novo documento duplicado.
    """
    body = {
        'name': new_title,
        'parents': [parent_folder_id]
    }
    copied_file = drive_service.files().copy(fileId=file_id, body=body).execute()
    return copied_file['id']

def convert_document_to_pdf(drive_service, document_id):
    """
    Converte um documento do Google Docs para PDF.

    :param drive_service: Serviço do Google Drive.
    :param document_id: ID do documento a ser convertido.
    :return: Caminho do arquivo PDF.
    """
    request = drive_service.files().export_media(fileId=document_id, mimeType='application/pdf')
    file_path = f'/tmp/{document_id}.pdf'
    with open(file_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
    return file_path

def replace_text_in_document(docs_service, doc_id, replacements):
    """
    Substitui texto em um documento do Google Docs.

    :param docs_service: Serviço do Google Docs.
    :param doc_id: ID do documento a ser modificado.
    :param replacements: Dicionário com os textos a serem substituídos.
    :return: Resultado da operação de substituição.
    """
    requests = []
    for key, value in replacements.items():
        if value == '':
            remove_placeholder_with_newline(requests, docs_service, doc_id, key)
        else:
            requests.append({
                'replaceAllText': {
                    'containsText': {
                        'text': key,
                        'matchCase': True
                    },
                    'replaceText': value
                }
            })
    
    if '[TITULOETAPA7]' in replacements and replacements['[TITULOETAPA7]'] == '':
        for key in ['[TITULOETAPA7] - [QTDDIASETAPA7]', '[OBJETIVOETAPA7]', '[ETAPA75]', '[ETAPA74]', '[ETAPA73]', '[ETAPA72]', '[ETAPA71]', 'Atividades...', '[TITULOETAPA7]']:
            remove_placeholder_with_newline(requests, docs_service, doc_id, key)

    replace_multiple_newlines(requests)
    
    result = docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
    return result

def remove_placeholder_with_newline(requests, docs_service, doc_id, placeholder):
    requests.append({
        'replaceAllText': {
            'containsText': {
                'text': "\n" + placeholder,
                'matchCase': True
            },
            'replaceText': ''
        }
    })
    result = docs_service.documents().get(documentId=doc_id).execute()
    for element in result['body']['content']:
        if 'paragraph' in element:
            for run in element['paragraph']['elements']:
                if 'textRun' in run and "\n" + placeholder in run['textRun']['content']:
                    requests.append({
                        'deleteContentRange': {
                            'range': {
                                'startIndex': run['startIndex'] - 1,
                                'endIndex': run['endIndex']
                            }
                        }
                    })

def replace_multiple_newlines(requests):
    requests.append({
        'replaceAllText': {
            'containsText': {
                'text': "\n" * 11,
                'matchCase': True
            },
            'replaceText': "\n"
        }
    })

def create_folder(service, folder_name, parent_folder_id=None):
    """
    Cria uma pasta no Google Drive.

    :param service: Serviço do Google Drive.
    :param folder_name: Nome da pasta a ser criada.
    :param parent_folder_id: ID da pasta pai onde a nova pasta será criada (opcional).
    :return: ID da pasta criada.
    """
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]

    folder = service.files().create(body=folder_metadata, fields='id').execute()
    logger.info(f"Pasta '{folder_name}' criada com ID: {folder.get('id')}")
    return folder.get('id')

def move_file_to_folder(service, file_path, folder_id, new_file_name):
    """
    Move um arquivo para uma pasta no Google Drive.

    :param service: Serviço do Google Drive.
    :param file_path: Caminho local do arquivo a ser enviado.
    :param folder_id: ID da pasta de destino no Google Drive.
    :param new_file_name: Novo nome do arquivo no Google Drive.
    :return: ID do arquivo movido.
    """
    file_metadata = {
        'name': new_file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    logger.info(f"Arquivo movido para a pasta com ID: {file.get('id')}")
    return file.get('id')

def share_file_with_email(service, file_id, email):
    """
    Compartilha um arquivo no Google Drive com um endereço de email.

    :param service: Serviço do Google Drive.
    :param file_id: ID do arquivo a ser compartilhado.
    :param email: Endereço de email com o qual o arquivo será compartilhado.
    """
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email
    }
    service.permissions().create(fileId=file_id, body=user_permission, fields='id').execute()
    logger.info(f"Arquivo com ID {file_id} compartilhado com {email}")
