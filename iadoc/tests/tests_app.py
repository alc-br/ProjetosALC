import os
import sys
import json
import pytest
from src.app import app

# Adicionando o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_process_document(client):
    proposta_path = os.path.join(os.path.dirname(__file__), '../proposta.json')
    with open(proposta_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    response = client.post('/process', json=data)
    assert response.status_code == 200
    json_response = response.get_json()
    assert 'message' in json_response

if __name__ == '__main__':
    pytest.main()
