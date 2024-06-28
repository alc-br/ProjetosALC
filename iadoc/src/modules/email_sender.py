"""
Este módulo gerencia o envio de e-mails com anexos.

Dependências:
- smtplib
- email.mime.multipart
- email.mime.base
- email.mime.text
- email.encoders

Autor: Seu Nome
Data: Data
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

def send_email_with_attachment(to_address, subject, body, attachment_path):
    """
    Envia um e-mail com um anexo.

    :param to_address: Endereço de e-mail do destinatário.
    :param subject: Assunto do e-mail.
    :param body: Corpo do e-mail.
    :param attachment_path: Caminho do arquivo a ser anexado.
    """
    from_address = 'anderson@alc.dev.br'
    password = 'Vi696206@'

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={attachment_path.split('/')[-1]}")
        msg.attach(part)

    server = smtplib.SMTP('mail.alc.dev.br ', 587)
    server.starttls()
    server.login(from_address, password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
