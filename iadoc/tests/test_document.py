import os
import sys
import pytest
from googleapiclient.discovery import build

# Adicionando o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.modules.auth import authenticate_google
from src.modules.document import duplicate_document, replace_text_in_document, convert_document_to_pdf

@pytest.fixture
def docs_service():
    json_path = os.path.join(os.path.dirname(__file__), '../src/service_account_info.json')
    creds = authenticate_google(json_path)
    return build('docs', 'v1', credentials=creds)

@pytest.fixture
def drive_service():
    json_path = os.path.join(os.path.dirname(__file__), '../src/service_account_info.json')
    creds = authenticate_google(json_path)
    return build('drive', 'v3', credentials=creds)

def test_duplicate_document(drive_service):
    template_file_id = 'your_template_file_id'
    new_title = 'Test Document'
    parent_folder_id = 'your_parent_folder_id'
    duplicated_file_id = duplicate_document(drive_service, template_file_id, new_title, parent_folder_id)
    assert duplicated_file_id is not None

def test_replace_text_in_document(docs_service):
    doc_id = 'your_document_id'
    replacements = {
        "[TEXTO1]": "Substituição de Teste"
    }
    result = replace_text_in_document(docs_service, doc_id, replacements)
    assert result is not None

def test_convert_document_to_pdf(drive_service):
    document_id = 'your_document_id'
    pdf_path = convert_document_to_pdf(drive_service, document_id)
    assert pdf_path is not None
    assert os.path.exists(pdf_path)

if __name__ == '__main__':
    pytest.main()
