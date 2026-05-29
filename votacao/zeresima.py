from mysql.connector import Error
from database.conexao import conectar


def zeresima():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        print("\n=== ZERÉSIMA ===")

        cursor.execute("DELETE FROM votos WHERE id > 0")
        conexao.commit()

        cursor.execute("SELECT * FROM candidatos")
        candidatos = cursor.fetchall()

        if len(candidatos) == 0:
            print("Nenhum candidato encontrado.")
            return

        cursor.execute("SELECT COUNT(*) FROM votos")
        total_votos = cursor.fetchone()[0]

        for candidato in candidatos:

            nome = candidato[1]
            numero = candidato[2]
            partido = candidato[3]

            print("Nome:", nome)
            print("Número:", numero)
            print("Partido:", partido)
            print("Votos: 0")
            print("-------------------")

        print("\nTotal de votos:", total_votos)

    except Error as erro:
        print("Erro ao gerar zerésima:", erro)

    cursor.close()
    conexao.close()
