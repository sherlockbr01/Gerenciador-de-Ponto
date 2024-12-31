import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')

def send_test_email():
    sender_email = "ssjjatai@gmail.com"
    receiver_email = "ssjjatai@gmail.com"
    password = "yneielcxjwrmqigu"  # Senha de aplicativo gerada

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Teste de Envio de Email"
    msg.attach(MIMEText("Este é um email de teste sem anexo.", 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        logging.debug("Email de teste enviado com sucesso!")
        print("Email de teste enviado com sucesso!")
    except smtplib.SMTPException as e:
        logging.error(f"Erro no envio do email de teste: {e}")
        raise

# Chame a função de teste diretamente
if __name__ == "__main__":
    send_test_email()
