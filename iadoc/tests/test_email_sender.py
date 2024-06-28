import os
import sys
import pytest

# Adicionando o diretório src ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.modules.email_sender import send_email_with_attachment

def test_send_email_with_attachment():
    to_address = 'destinatario@example.com'
    subject = 'Documento PDF'
    body = 'Encontre em anexo o documento PDF.'
    attachment_path = '/path/to/your/test.pdf'  # Certifique-se de que este arquivo exista para o teste

    try:
        send_email_with_attachment(to_address, subject, body, attachment_path)
        email_sent = True
    except Exception as e:
        print(e)
        email_sent = False

    assert email_sent is True

if __name__ == '__main__':
    pytest.main()
