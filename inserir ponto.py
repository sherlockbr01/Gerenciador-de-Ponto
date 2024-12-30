import sqlite3
from datetime import datetime


def conectar_banco():
    return sqlite3.connect('ponto.db')


def inserir_ponto(data, matricula, hora_entrada, hora_saida=None, hora_entrada_2=None, hora_saida_2=None):
    conn = conectar_banco()
    c = conn.cursor()

    # Remover pontos existentes para a data e matrícula fornecidas
    c.execute("DELETE FROM pontos WHERE data = ? AND matricula_usuario = ?", (data, matricula))

    # Inserir novos pontos
    c.execute(
        "INSERT INTO pontos (data, hora_entrada, hora_saida, hora_entrada_2, hora_saida_2, matricula_usuario) VALUES (?, ?, ?, ?, ?, ?)",
        (data, hora_entrada, hora_saida, hora_entrada_2, hora_saida_2, matricula))

    conn.commit()
    conn.close()
    print('Ponto corrigido e inserido com sucesso!')


def editar_ponto(data, matricula):
    conn = conectar_banco()
    c = conn.cursor()

    # Buscar ponto existente
    c.execute("SELECT * FROM pontos WHERE data = ? AND matricula_usuario = ?", (data, matricula))
    ponto = c.fetchone()

    if not ponto:
        print("Nenhum ponto encontrado para a data e matrícula fornecidas.")
        return

    print("Ponto encontrado:")
    print(f"Data: {data}")
    print(f"Entrada: {ponto[2]}")
    print(f"Saída: {ponto[3]}")
    print(f"Entrada 2: {ponto[4]}")
    print(f"Saída 2: {ponto[5]}")

    while True:
        escolha = input(
            "Qual horário você quer mudar? Entrada digite 1, Saída digite 2, Entrada 2 digite 3, Saída 2 digite 4: ")

        if escolha not in ["1", "2", "3", "4"]:
            print("Escolha inválida. Tente novamente.")
            continue

        novo_horario = input("Digite o novo horário no formato 00:00:00: ")

        if escolha == "1":
            c.execute("UPDATE pontos SET hora_entrada = ? WHERE id = ?", (novo_horario, ponto[0]))
        elif escolha == "2":
            c.execute("UPDATE pontos SET hora_saida = ? WHERE id = ?", (novo_horario, ponto[0]))
        elif escolha == "3":
            c.execute("UPDATE pontos SET hora_entrada_2 = ? WHERE id = ?", (novo_horario, ponto[0]))
        elif escolha == "4":
            c.execute("UPDATE pontos SET hora_saida_2 = ? WHERE id = ?", (novo_horario, ponto[0]))

        conn.commit()

        confirmar = input("Certeza que confirma? Sim para confirmar, Não para voltar: ").lower()
        if confirmar == "sim":
            print("Pontos corrigidos com sucesso!")
            break
        elif confirmar == "não":
            print("Voltando para a seleção de horário...")
        else:
            print("Entrada inválida. Voltando para a seleção de horário...")

    conn.close()


def main():
    print("O que você quer fazer hoje?")
    print("1. Inserir pontos diários completos")
    print("2. Editar pontos do usuário")

    escolha = input("Escolha uma opção (1 ou 2): ")

    if escolha == "1":
        data = input("Digite a data no formato DD/MM/AAAA: ")
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        matricula = input("Digite a matrícula do usuário: ")
        hora_entrada = input("Digite a hora de entrada no formato 00:00:00: ")
        hora_saida = input("Digite a hora de saída no formato 00:00:00 (opcional): ") or None
        hora_entrada_2 = input("Digite a hora de entrada 2 no formato 00:00:00 (opcional): ") or None
        hora_saida_2 = input("Digite a hora de saída 2 no formato 00:00:00 (opcional): ") or None

        inserir_ponto(data_formatada, matricula, hora_entrada, hora_saida, hora_entrada_2, hora_saida_2)

    elif escolha == "2":
        data = input("Qual data você quer corrigir? (no formato DD/MM/AAAA): ")
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        matricula = input("Digite a matrícula do usuário: ")

        editar_ponto(data_formatada, matricula)

    else:
        print("Escolha inválida. Tente novamente.")


if __name__ == "__main__":
    main()
