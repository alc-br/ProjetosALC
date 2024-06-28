import os
import sys
import pytest

# Adicionando o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
print("sys.path:", sys.path)  # Linha de depuração para verificar o caminho

try:
    from modules.auth import authenticate_google, get_google_services
    print("Import successful")
except ImportError as e:
    print(f"ImportError: {e}")

def test_authenticate_google():
    json_path = os.path.join(os.path.dirname(__file__), '../src/service_account_info.json')
    creds = authenticate_google(json_path)
    assert creds is not None
    assert creds.token is None  # The token should not be generated until a request is made

def test_get_google_services():
    json_path = os.path.join(os.path.dirname(__file__), '../src/service_account_info.json')
    creds = authenticate_google(json_path)
    drive_service, docs_service = get_google_services(creds)
    assert drive_service is not None
    assert docs_service is not None

if __name__ == '__main__':
    pytest.main()
