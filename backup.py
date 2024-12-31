import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, render_template, send_file, flash, redirect, url_for
from datetime import datetime
import tempfile
import zipfile

app = Flask(__name__)
app.secret_key = '@ssjjti'  # Para flash messages e sessões

# Caminho do banco de dados SQLite
db_path = '/app/ponto.db'  # No Heroku, o banco de dados estará em /app/ponto.db


# Função para enviar o backup por e-mail
def send_backup_email(zip_path):
    sender_email = "ssjjatai@gmail.com"
    receiver_email = "ssjjatai@gmail.com"  # Enviar para o mesmo e-mail
    password = "yneielcxjwrmqigu"  # Senha de aplicativo gerada

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Backup do Banco de Dados - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    part = MIMEBase('application', 'octet-stream')
    with open(zip_path, 'rb') as file:
        part.set_payload(file.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(zip_path)}")

    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Backup enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar o e-mail: {e}")


@app.route('/baixar_e_enviar_backup')
def baixar_e_enviar_backup():
    # Verifica se o banco de dados existe antes de tentar fazer o backup
    if not os.path.exists(db_path):
        flash("Erro: Banco de dados não encontrado.", "error")
        return redirect(url_for('dashboard_usuario_administrador'))  # Redireciona para a dashboard do administrador

    # Criar um diretório temporário para armazenar o backup
    with tempfile.TemporaryDirectory() as tmpdirname:
        backup_filename = f'ponto_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        zip_filename = f'ponto_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        backup_path = os.path.join(tmpdirname, backup_filename)
        zip_path = os.path.join(tmpdirname, zip_filename)

        # Fazendo o backup do banco de dados para o diretório temporário
        shutil.copy(db_path, backup_path)

        # Compactando o arquivo .db em um arquivo .zip
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(backup_path, os.path.basename(backup_path))
        print(f"Arquivo {zip_path} criado com sucesso!")

        # Enviar o backup por e-mail
        send_backup_email(zip_path)

        # Enviar o backup para o usuário fazer o download
        return send_file(zip_path, as_attachment=True, download_name=zip_filename,
                         mimetype='application/zip')


@app.route('/dashboard_usuario_administrador')
def dashboard_usuario_administrador():
    # Renderiza a página do dashboard
    return render_template('dashboard_usuario_admin.html')


if __name__ == '__main__':
    app.run(debug=True)
