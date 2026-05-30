from pathlib import Path
from datetime import datetime

from database.conexao import conectar
from mysql.connector import Error

ARQUIVO_LOGS = Path(__file__).with_name("logs_ocorrencias.txt")


def registrar_log(mensagem):
    """
    Registra uma ocorrência do sistema no arquivo de logs.

    Args:
        mensagem (str): Mensagem que descreve a ocorrência registrada.

    Returns:
        None.
    """

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARQUIVO_LOGS, "a", encoding="utf-8") as arquivo:

        arquivo.write(
            f"[{data_hora}] {mensagem}\n"
        )


def exibir_logs():
    """
    Exibe no terminal os registros armazenados no arquivo de logs.

    Args:
        Nenhum.

    Returns:
        None.
    """

    try:

        arquivo = open(
            ARQUIVO_LOGS,
            "r",
            encoding="utf-8"
        )

        logs = arquivo.readlines()

        arquivo.close()

        if len(logs) == 0:
            print("Nenhum log encontrado.")
            return

        print("\n=== LOGS DE OCORRÊNCIAS ===")

        for log in logs:
            print(log.strip())

    except FileNotFoundError:
        print("Arquivo de logs não encontrado.")


def exibir_protocolos():
    """
    Exibe os protocolos de votação registrados no banco de dados.

    Args:
        Nenhum.

    Returns:
        None.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        print("\n=== PROTOCOLOS DE VOTAÇÃO ===")

        cursor.execute(
            "SELECT protocolo, data_hora FROM votos"
        )

        protocolos = cursor.fetchall()

        if len(protocolos) == 0:
            print("Nenhum protocolo encontrado.")
            return

        for protocolo in protocolos:

            codigo = protocolo[0]
            data = protocolo[1]

            print("\nProtocolo:", codigo)
            print("Data/Hora:", data)

    except Error as erro:
        print("Erro ao mostrar protocolos:", erro)

    cursor.close()
    conexao.close()