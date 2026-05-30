from mysql.connector import Error
from database.conexao import conectar


def cadastrar_candidato():
    """
    Cadastra um novo candidato no banco de dados.

    Args:
        Nenhum.

    Returns:
        None.
    """

    nome = input("Nome do candidato: ")
    numero = input("Número do candidato: ")
    partido = input("Partido: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM candidatos WHERE numero = %s",
            (numero,)
        )

        if len(cursor.fetchall()) > 0:
            print("Já existe candidato com esse número.")
            return

        sql = """
        INSERT INTO candidatos
        VALUES (NULL, %s, %s, %s)
        """

        valores = (
            nome,
            numero,
            partido
        )

        cursor.execute(sql, valores)

        conexao.commit()

        print("Candidato cadastrado com sucesso!")

    except Error as erro:
        print("Erro ao cadastrar candidato:", erro)

    cursor.close()
    conexao.close()


def listar_candidatos():
    """
    Lista todos os candidatos cadastrados no banco de dados.

    Args:
        Nenhum.

    Returns:
        None.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("SELECT * FROM candidatos")

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Nenhum candidato cadastrado.")
            return

        for candidato in dados:

            print("\nID:", candidato[0])
            print("Nome:", candidato[1])
            print("Número:", candidato[2])
            print("Partido:", candidato[3])
            print("----------------------")

    except Error as erro:
        print("Erro ao listar candidatos:", erro)

    cursor.close()
    conexao.close()


def buscar_candidato():
    """
    Busca um candidato pelo número de votação.

    Args:
        Nenhum.

    Returns:
        None.
    """

    numero = input("Digite o número do candidato: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM candidatos WHERE numero = %s",
            (numero,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Candidato não encontrado.")
            return

        candidato = dados[0]

        print("\nID:", candidato[0])
        print("Nome:", candidato[1])
        print("Número:", candidato[2])
        print("Partido:", candidato[3])

    except Error as erro:
        print("Erro ao buscar candidato:", erro)

    cursor.close()
    conexao.close()


def editar_candidato():
    """
    Edita os dados de um candidato cadastrado.

    Args:
        Nenhum.

    Returns:
        None.
    """

    numero = input("Número do candidato: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM candidatos WHERE numero = %s",
            (numero,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Candidato não encontrado.")
            return

        novo_nome = input("Novo nome: ")
        novo_numero = input("Novo número: ")
        novo_partido = input("Novo partido: ")

        cursor.execute(
            "SELECT * FROM candidatos WHERE numero = %s AND numero != %s",
            (novo_numero, numero)
        )

        if len(cursor.fetchall()) > 0:
            print("Já existe candidato com esse número.")
            return

        sql = """
        UPDATE candidatos
        SET nome = %s,
            numero = %s,
            partido = %s
        WHERE numero = %s
        """

        valores = (
            novo_nome,
            novo_numero,
            novo_partido,
            numero
        )

        cursor.execute(sql, valores)

        conexao.commit()

        print("Candidato atualizado com sucesso!")

    except Error as erro:
        print("Erro ao editar candidato:", erro)

    cursor.close()
    conexao.close()


def remover_candidato():
    """
    Remove um candidato cadastrado no banco de dados.

    Args:
        Nenhum.

    Returns:
        None.
    """

    numero = input("Número do candidato: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM candidatos WHERE numero = %s",
            (numero,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Candidato não encontrado.")
            return

        cursor.execute(
            "DELETE FROM candidatos WHERE numero = %s",
            (numero,)
        )

        conexao.commit()

        print("Candidato removido com sucesso!")

    except Error as erro:
        print("Erro ao remover candidato:", erro)

    cursor.close()
    conexao.close()


def menu_candidato():
    """
    Exibe o menu de gerenciamento de candidatos.

    Args:
        Nenhum.

    Returns:
        None.
    """

    opcao = ""

    while opcao != "0":

        print("\n=== MENU CANDIDATOS ===")
        print("1 - Cadastrar candidato")
        print("2 - Listar candidatos")
        print("3 - Buscar candidato")
        print("4 - Editar candidato")
        print("5 - Remover candidato")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_candidato()

        elif opcao == "2":
            listar_candidatos()

        elif opcao == "3":
            buscar_candidato()

        elif opcao == "4":
            editar_candidato()

        elif opcao == "5":
            remover_candidato()

        elif opcao == "0":
            print("Voltando...")

        else:
            print("Opção inválida!")