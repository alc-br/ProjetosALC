"""
Este módulo realiza a autenticação com o Google utilizando uma conta de serviço.

Dependências:
- google.oauth2.service_account
- googleapiclient.discovery
- json

Autor: Anderson Chipak - Agência ALC
Data: 26/06/2024
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']

def authenticate_google(service_account_info_json: str):
    """
    Autentica com o Google utilizando as credenciais da conta de serviço.

    :param service_account_info_json: JSON com as informações da conta de serviço.
    :return: Credenciais autenticadas.
    """
    try:
        service_account_info = json.loads(service_account_info_json)
        private_key = service_account_info.get('private_key')
        
        if not private_key:
            logger.error("Chave privada não encontrada no JSON de credenciais.")
            raise ValueError("Chave privada não encontrada no JSON de credenciais.")
        
        if not private_key.startswith('-----BEGIN PRIVATE KEY-----') or not private_key.endswith('-----END PRIVATE KEY-----\n'):
            logger.error("Formato da chave privada no JSON está incorreto.")
            raise ValueError("Formato da chave privada no JSON está incorreto.")
        
        credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        logger.info("Autenticação com o Google bem-sucedida.")
        return credentials
    except Exception as e:
        logger.error(f"Erro ao autenticar com o Google: {e}")
        raise

def authenticate_google_from_file(json_path: str):
    """
    Autentica com o Google utilizando as credenciais da conta de serviço a partir de um arquivo JSON.

    :param json_path: Caminho para o arquivo JSON com as informações da conta de serviço.
    :return: Credenciais autenticadas.
    """
    try:
        with open(json_path, 'r') as f:
            service_account_info = json.load(f)
        
        private_key = service_account_info.get('private_key')
        
        if not private_key:
            logger.error("Chave privada não encontrada no JSON de credenciais.")
            raise ValueError("Chave privada não encontrada no JSON de credenciais.")
        
        if not private_key.startswith('-----BEGIN PRIVATE KEY-----') or not private_key.endswith('-----END PRIVATE KEY-----\n'):
            logger.error("Formato da chave privada no JSON está incorreto.")
            raise ValueError("Formato da chave privada no JSON está incorreto.")
        
        credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        logger.info("Autenticação com o Google a partir de arquivo JSON bem-sucedida.")
        return credentials
    except Exception as e:
        logger.error(f"Erro ao autenticar com o Google a partir de arquivo JSON: {e}")
        raise

def get_google_services(creds):
    """
    Cria os serviços do Google Drive e Google Docs.

    :param creds: Credenciais autenticadas.
    :return: Serviços do Google Drive e Google Docs.
    """
    try:
        drive_service = build('drive', 'v3', credentials=creds)
        docs_service = build('docs', 'v1', credentials=creds)
        logger.info("Serviços do Google Drive e Docs criados com sucesso.")
        return drive_service, docs_service
    except Exception as e:
        logger.error(f"Erro ao criar serviços do Google: {e}")
        raise
