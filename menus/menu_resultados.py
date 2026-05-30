from mysql.connector import Error
from database.conexao import conectar


def boletim_urna():

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
        ORDER BY candidatos.nome
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        print("\n=== BOLETIM DE URNA ===")

        if len(resultados) == 0:
            print("Nenhum candidato encontrado.")
            return

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

        vencedor = resultados[0]

        for resultado in resultados:

            if resultado[3] > vencedor[3]:
                vencedor = resultado

        print("\n=== VENCEDOR ===")
        print("Nome:", vencedor[0])
        print("Número:", vencedor[1])
        print("Partido:", vencedor[2])
        print("Votos:", vencedor[3])

    except Error as erro:
        print("Erro:", erro)

    cursor.close()
    conexao.close()


def estatistica_comparecimento():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT COUNT(*) FROM eleitores"
        )

        total_eleitores = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM eleitores WHERE ja_votou = 1"
        )

        comparecimento = cursor.fetchone()[0]

        print("\n=== ESTATÍSTICA DE COMPARECIMENTO ===")
        print("Eleitores aptos:", total_eleitores)
        print("Eleitores que votaram:", comparecimento)

        if total_eleitores > 0:
            percentual = (comparecimento / total_eleitores) * 100
        else:
            percentual = 0

        print("Percentual de comparecimento:", round(percentual, 2), "%")

    except Error as erro:
        print("Erro:", erro)

    cursor.close()
    conexao.close()


def votos_por_partido():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        print("\n=== VOTOS POR PARTIDO ===")

        cursor.execute("""
        SELECT candidatos.partido,
               COUNT(votos.id)
        FROM candidatos
        LEFT JOIN votos
        ON candidatos.id = votos.candidato_id
        GROUP BY candidatos.partido
        ORDER BY candidatos.partido
        """)

        partidos = cursor.fetchall()

        if len(partidos) == 0:
            print("Nenhum partido encontrado.")
            return

        for partido in partidos:

            print(
                partido[0],
                "-",
                partido[1],
                "votos"
            )

    except Error as erro:
        print("Erro:", erro)

    cursor.close()
    conexao.close()


def validacao_integridade():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        print("\n=== VALIDAÇÃO DE INTEGRIDADE ===")

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


def menu_resultados():

    opcao = ""

    while opcao != "0":

        print("\n=== RESULTADOS DA VOTAÇÃO ===")
        print("1 - Boletim de urna e vencedor")
        print("2 - Estatística de comparecimento")
        print("3 - Votos por partido")
        print("4 - Validação de integridade")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            boletim_urna()

        elif opcao == "2":
            estatistica_comparecimento()

        elif opcao == "3":
            votos_por_partido()

        elif opcao == "4":
            validacao_integridade()

        elif opcao == "0":
            print("Voltando...")

        else:
            print("Opção inválida!")