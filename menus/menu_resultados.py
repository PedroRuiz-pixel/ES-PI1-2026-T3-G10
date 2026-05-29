from mysql.connector import Error
from database.conexao import conectar


def menu_resultados():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        sql = """
        SELECT candidatos.nome,
               candidatos.numero,
               candidatos.partido,
               COUNT(votos.id) AS total_votos
        FROM candidatos
        LEFT JOIN votos
        ON candidatos.id = votos.candidato_id
        GROUP BY candidatos.id
        ORDER BY total_votos DESC
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        print("\n=== RESULTADOS ===")

        for resultado in resultados:

            print("\nNome:", resultado[0])
            print("Número:", resultado[1])
            print("Partido:", resultado[2])
            print("Votos:", resultado[3])

        cursor.execute(
            "SELECT COUNT(*) FROM votos WHERE candidato_id IS NULL"
        )

        votos_nulos = cursor.fetchone()[0]

        print("\nVotos nulos:", votos_nulos)

        cursor.execute(
            "SELECT COUNT(*) FROM votos"
        )

        total_votos = cursor.fetchone()[0]

        print("Total de votos:", total_votos)

        cursor.execute(
            "SELECT COUNT(*) FROM eleitores WHERE ja_votou = 1"
        )

        comparecimento = cursor.fetchone()[0]

        print("Comparecimento:", comparecimento)

        if len(resultados) > 0:

            vencedor = resultados[0]

            print("\n=== VENCEDOR ===")
            print("Nome:", vencedor[0])
            print("Número:", vencedor[1])
            print("Partido:", vencedor[2])
            print("Votos:", vencedor[3])

        print("\n=== VOTOS POR PARTIDO ===")

        cursor.execute("""
        SELECT partido, COUNT(votos.id)
        FROM candidatos
        LEFT JOIN votos
        ON candidatos.id = votos.candidato_id
        GROUP BY partido
        """)

        partidos = cursor.fetchall()

        for partido in partidos:

            print(
                partido[0],
                "-",
                partido[1],
                "votos"
            )

        print("\n=== INTEGRIDADE DOS VOTOS ===")

        cursor.execute(
            "SELECT COUNT(*) FROM votos"
        )

        total_votos_banco = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM eleitores WHERE ja_votou = 1"
        )

        total_eleitores_votaram = cursor.fetchone()[0]

        print("Total de votos registrados:", total_votos_banco)
        print("Eleitores marcados como já votaram:", total_eleitores_votaram)

        if total_votos_banco == total_eleitores_votaram:
            print("Integridade confirmada: votos e eleitores conferem.")
        else:
            print("Alerta: divergência entre votos e eleitores.")

    except Error as erro:
        print("Erro:", erro)

    cursor.close()
    conexao.close()