# Projeto de Geração Automática de Orçamento

## Descrição
Este projeto duplica um documento modelo do Google Docs, substitui placeholders por dados fornecidos em um arquivo JSON, converte o documento em PDF e envia-o por e-mail.

## Estrutura do Projeto
/orcamentoalc
/src
init.py
app.py
service_account_info.json
/modules
init.py
auth.py
document.py
email_sender.py
/static
/templates
/tests
init.py
test_auth.py
test_document.py
test_email_sender.py
test_app.py
README.md
requirements.txt


## Dependências
- flask
- google-api-python-client
- google-auth
- pytest

## Instruções de Uso
1. Configure as credenciais da conta de serviço do Google e salve o JSON em `src/service_account_info.json`.
2. Instale as dependências com o comando:
    ```sh
    pip install -r requirements.txt
    ```
3. Execute o aplicativo Flask:
    ```sh
    python src/app.py
    ```

## Instruções para Testes
1. Certifique-se de que os arquivos de teste estão configurados corretamente.
2. Execute os testes com o comando:
    ```sh
    pytest tests/
    ```

## Como Usar o Serviço
1. Envie uma requisição `POST` para o endpoint `/process` com um JSON no corpo da requisição, contendo a estrutura necessária para a proposta. Por exemplo:
    ```json
    {
        "proposta": {
            "data": "10/11/2023",
            "ano": "2023",
            "cliente": {
                "nome": "João Silva",
                "email": "joao.silva@example.com",
                "telefone": "(11) 98765-4321",
                "empresa": "Empresa X"
            },
            "escopo_do_projeto": {
                "objetivo_do_projeto": "Desenvolver uma plataforma de e-commerce robusta e escalável",
                "itens_do_escopo": [
                    {
                        "item": "Levantamento de Requisitos",
                        "descrição": "Identificação das necessidades e funcionalidades do sistema"
                    },
                    {
                        "item": "Design da Interface",
                        "descrição": "Criação de protótipos de alta fidelidade para o sistema"
                    },
                    {
                        "item": "Desenvolvimento Backend",
                        "descrição": "Codificação da lógica do servidor e banco de dados"
                    },
                    {
                        "item": "Desenvolvimento Frontend",
                        "descrição": "Criação da interface do usuário com responsividade"
                    },
                    {
                        "item": "Teste e Qualidade",
                        "descrição": "Verificação e validação das funcionalidades do sistema"
                    },
                    {
                        "item": "Entrega e Treinamento",
                        "descrição": "Implantação do sistema e treinamento dos usuários"
                    }
                ]
            },
            "etapas_do_projeto": [
                {
                    "titulo_da_etapa": "Análise Inicial",
                    "objetivo": "Objetivo: Compreender as necessidades do cliente e definir o escopo do projeto",
                    "atividades": [
                        "Reunião inicial para discussão dos detalhes e expectativas",
                        "Análise dos tipos de dados envolvidos",
                        "Identificação dos principais stakeholders"
                    ],
                    "qtd_dias": 5
                },
                {
                    "titulo_da_etapa": "Planejamento da Solução",
                    "objetivo": "Objetivo: Definir a arquitetura e as tecnologias a serem utilizadas",
                    "atividades": [
                        "Definição da arquitetura do sistema",
                        "Escolha das tecnologias principais",
                        "Planejamento das sprints de desenvolvimento"
                    ],
                    "qtd_dias": 7
                },
                {
                    "titulo_da_etapa": "Desenvolvimento",
                    "objetivo": "Objetivo: Codificar as funcionalidades conforme planejamento",
                    "atividades": [
                        "Desenvolvimento do backend",
                        "Desenvolvimento do frontend",
                        "Integração de APIs"
                    ],
                    "qtd_dias": 20
                },
                {
                    "titulo_da_etapa": "Testes e Ajustes",
                    "objetivo": "Objetivo: Garantir que todas as funcionalidades estejam operando conforme o esperado",
                    "atividades": [
                        "Criação de cenários de teste",
                        "Execução de testes manuais e automatizados",
                        "Correção de bugs"
                    ],
                    "qtd_dias": 10
                },
                {
                    "titulo_da_etapa": "Implementação e Entrega",
                    "objetivo": "Objetivo: Implantar a solução no ambiente de produção e garantir sua operação",
                    "atividades": [
                        "Configuração do ambiente de produção",
                        "Migração de dados",
                        "Treinamento dos usuários"
                    ],
                    "qtd_dias": 5
                },
                {
                    "titulo_da_etapa": "Suporte e Manutenção",
                    "objetivo": "Objetivo: Fazer o acompanhamento e resolução de possíveis problemas pós-implantação",
                    "atividades": [
                        "Monitoramento do sistema",
                        "Suporte técnico",
                        "Manutenção evolutiva e corretiva"
                    ],
                    "qtd_dias": 30
                }
            ],
            "metodologia_de_trabalho": {
                "ferramentas_e_tecnologias_utilizadas": [
                    {
                        "ferramenta": "JIRA",
                        "descricao": "Ferramenta de gerenciamento de projetos e controle de sprints"
                    },
                    {
                        "ferramenta": "GitHub",
                        "descricao": "Plataforma para hospedagem e controle de versão de código"
                    },
                    {
                        "ferramenta": "Figma",
                        "descricao": "Ferramenta para design de interface e prototipagem"
                    },
                    {
                        "ferramenta": "Node.js",
                        "descricao": "Framework para desenvolvimento do backend"
                    },
                    {
                        "ferramenta": "React",
                        "descricao": "Biblioteca para desenvolvimento de interfaces de usuário"
                    }
                ]
            },
            "custo_do_projeto": {
                "valor_original": "R$25.000",
                "valor_a_vista": "R$22.500"
            }
        }
    }
    ```

## Testando com Postman

Para testar o endpoint `/process` com o Postman:

1. **Instale e Abra o Postman**:
   - Se você ainda não possui o Postman instalado, baixe e instale a partir do site oficial [Postman](https://www.postman.com/).

2. **Importe a Coleção**:
   - Clique em `Import` no canto superior esquerdo.
   - Selecione `Upload Files` e escolha o arquivo JSON exportado.
   - Clique em `Import`.

3. **Execute a Requisição**:
   - Dentro da coleção importada, selecione a requisição `Process Document`.
   - Clique em `Send` para enviar a requisição ao servidor Flask.

### Script de Teste do Postman

O script de teste verifica se a resposta contém um código de status 200 e uma propriedade `message` no JSON de resposta:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property("message");
});


## Autor
Anderson Chipak - Agência ALC

## Data
26/06/2024