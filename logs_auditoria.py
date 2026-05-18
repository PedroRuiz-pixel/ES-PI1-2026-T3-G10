from conexao import conectar
from mysql.connector import Error


def registrar_log(tipo, descricao):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = "INSERT INTO log (tipo, descricao) VALUES (%s, %s)"

        valores = (tipo, descricao)

        cursor.execute(sql, valores)

        conexao.commit()

    except Error as erro:
        print("Erro ao registrar log:", erro)

    cursor.close()
    conexao.close()


def exibir_logs():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("SELECT * FROM log")

        logs = cursor.fetchall()

        if len(logs) == 0:
            print("Nenhum log encontrado.")
            return

        print("\n=== LOGS DE OCORRÊNCIAS ===")

        for log in logs:

            print("ID:", log[0])
            print("Tipo:", log[1])
            print("Descrição:", log[2])
            print("Data/Hora:", log[3])
            print("-------------------")

    except Error as erro:
        print("Erro ao exibir logs:", erro)

    cursor.close()
    conexao.close()


def exibir_protocolos():

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