import sqlite3
from datetime import datetime, timedelta
import random

def conectar_banco():
    return sqlite3.connect('ponto.db')

def inserir_ponto(data, matricula, hora_entrada, hora_saida=None, hora_entrada_2=None, hora_saida_2=None):
    conn = conectar_banco()
    c = conn.cursor()

    # Verificar se já existem pontos para a data e matrícula fornecidas
    c.execute("SELECT * FROM pontos WHERE data = ? AND matricula_usuario = ?", (data, matricula))
    pontos = c.fetchall()

    if not pontos:
        c.execute("INSERT INTO pontos (data, hora_entrada, hora_saida, hora_entrada_2, hora_saida_2, matricula_usuario) VALUES (?, ?, ?, ?, ?, ?)",
                  (data, hora_entrada, hora_saida, hora_entrada_2, hora_saida_2, matricula))
    else:
        ponto = pontos[0]
        if not ponto[2]:  # Se a coluna hora_entrada está vazia
            c.execute("UPDATE pontos SET hora_entrada = ? WHERE id = ?", (hora_entrada, ponto[0]))
        if not ponto[3]:  # Se a coluna hora_saida está vazia
            c.execute("UPDATE pontos SET hora_saida = ? WHERE id = ?", (hora_saida, ponto[0]))
        if not ponto[4]:  # Se a coluna hora_entrada_2 está vazia
            c.execute("UPDATE pontos SET hora_entrada_2 = ? WHERE id = ?", (hora_entrada_2, ponto[0]))
        if not ponto[5]:  # Se a coluna hora_saida_2 está vazia
            c.execute("UPDATE pontos SET hora_saida_2 = ? WHERE id = ?", (hora_saida_2, ponto[0]))

    conn.commit()
    conn.close()
    print(f'Ponto inserido com sucesso para {data}.')

# Função para gerar pontos aleatórios para dias de semana em novembro
def gerar_pontos_novembro(matricula, carga_horaria_padrao=8):
    start_date = datetime(2024, 12, 1)
    end_date = datetime(2024, 12, 31)
    delta = timedelta(days=1)

    saldo_negativo_segundos = 5 * 3600  # 5 horas negativas em segundos

    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Apenas dias de semana
            hora_entrada = datetime.strptime('08:00:00', "%H:%M:%S")
            hora_saida = hora_entrada + timedelta(hours=random.randint(3, 5))  # Saída entre 3 a 5 horas após entrada
            hora_entrada_2 = hora_saida + timedelta(hours=1)  # Pausa de 1 hora para almoço
            hora_saida_2 = hora_entrada_2 + timedelta(hours=random.randint(2, 4))  # Saída entre 2 a 4 horas após entrada 2

            total_trabalhado_segundos = (hora_saida - hora_entrada).total_seconds() + (hora_saida_2 - hora_entrada_2).total_seconds()
            saldo_negativo_segundos -= (carga_horaria_padrao * 3600 - total_trabalhado_segundos)

            data = current_date.strftime("%Y-%m-%d")
            inserir_ponto(data, matricula, hora_entrada.strftime("%H:%M:%S"), hora_saida.strftime("%H:%M:%S"), hora_entrada_2.strftime("%H:%M:%S"), hora_saida_2.strftime("%H:%M:%S"))

        current_date += delta

    print(f'Saldo negativo restante: {saldo_negativo_segundos / 3600} horas.')

# Exemplo de uso do script
matricula = '3'
gerar_pontos_novembro(matricula)
