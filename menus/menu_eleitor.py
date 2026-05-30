from mysql.connector import Error
from database.conexao import conectar
import random

from Criptografia.cifra_hill import cifrar_hill, decifrar_hill


def gerar_chave_acesso(nome):

    partes = nome.strip().upper().split()

    if len(partes[0]) < 2:
        print("Nome precisa ter pelo menos 2 letras.")
        return ""

    if len(partes) >= 2:
        inicio = partes[0][0] + partes[0][1] + partes[1][0]
    else:
        inicio = partes[0][0] + partes[0][1]

    numero = str(random.randint(1000, 9999))

    chave = inicio + numero

    return chave


def validar_cpf(cpf):

    if cpf == cpf[0] * 11:
        print("CPF inválido.")
        return False

    soma = 0
    i = 0

    while i < 9:
        soma += int(cpf[i]) * (10 - i)
        i += 1

    resto = (soma * 10) % 11

    if resto == 10:
        resto = 0

    if resto != int(cpf[9]):
        print("CPF inválido.")
        return False

    soma = 0
    i = 0

    while i < 10:
        soma += int(cpf[i]) * (11 - i)
        i += 1

    resto = (soma * 10) % 11

    if resto == 10:
        resto = 0

    if resto != int(cpf[10]):
        print("CPF inválido.")
        return False

    return True


def validar_titulo(titulo):

    titulo_limpo = ""

    for c in titulo:
        if c >= "0" and c <= "9":
            titulo_limpo = titulo_limpo + c

    if len(titulo_limpo) != 12:
        print("Título de eleitor deve ter 12 números.")
        return False

    if titulo_limpo == titulo_limpo[0] * 12:
        print("Título de eleitor inválido.")
        return False

    soma = 0
    peso = 2
    i = 0

    while i < 8:
        soma = soma + int(titulo_limpo[i]) * peso
        peso = peso + 1
        i = i + 1

    resto = soma % 11
    digito1 = resto

    if digito1 == 10:
        digito1 = 0

    soma = 0
    peso = 7
    i = 8

    while i < 11:
        soma = soma + int(titulo_limpo[i]) * peso
        peso = peso + 1
        i = i + 1

    resto = soma % 11
    digito2 = resto

    if digito2 == 10:
        digito2 = 0

    if digito1 != int(titulo_limpo[10]) or digito2 != int(titulo_limpo[11]):
        print("Título de eleitor inválido.")
        return False

    return True


def limpar_numeros(texto):

    numeros = ""

    for c in texto:
        if c >= "0" and c <= "9":
            numeros += c

    return numeros


def cadastrar_eleitor():

    nome = input("Nome: ")

    titulo = input("Título de Eleitor: ")

    if not validar_titulo(titulo):
        return

    titulo = limpar_numeros(titulo)

    cpf = input("CPF: ")

    if nome == "" or titulo == "" or cpf == "":
        print("Todos os campos são obrigatórios.")
        return

    cpf = limpar_numeros(cpf)

    if len(cpf) != 11:
        print("CPF deve ter 11 números.")
        return

    if not validar_cpf(cpf):
        return

    cpf_criptografado = cifrar_hill(cpf)

    mesario = input("Mesário (S/N): ").upper()

    if mesario == "S":
        mesario = True

    elif mesario == "N":
        mesario = False

    else:
        print("Digite apenas S ou N.")
        return

    chave_acesso = gerar_chave_acesso(nome)

    if chave_acesso == "":
        return

    chave_criptografada = cifrar_hill(chave_acesso)

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM eleitores WHERE cpf = %s OR Titulo_eleitor = %s",
            (cpf_criptografado, titulo)
        )

        if len(cursor.fetchall()) > 0:
            print("Erro: CPF ou título já cadastrado.")
            return

        sql = """
        INSERT INTO eleitores
        VALUES (NULL, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            nome,
            titulo,
            cpf_criptografado,
            mesario,
            chave_criptografada,
            False
        )

        cursor.execute(sql, valores)

        conexao.commit()

        print("Eleitor cadastrado com sucesso!")
        print("Chave de acesso:", chave_acesso)

    except Error as erro:
        print("Erro ao cadastrar eleitor:", erro)

    cursor.close()
    conexao.close()


def listar_eleitores():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute("SELECT * FROM eleitores")

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Nenhum eleitor cadastrado.")
            return

        for eleitor in dados:

            print("\nID:", eleitor[0])
            print("Nome:", eleitor[1])
            print("Título:", eleitor[2])
            print("CPF:", decifrar_hill(eleitor[3]))
            print("Mesário:", "Sim" if eleitor[4] == 1 else "Não")
            print("Chave:", decifrar_hill(eleitor[5]))
            print("Já votou:", "Sim" if eleitor[6] == 1 else "Não")
            print("----------------------")

    except Error as erro:
        print("Erro ao listar eleitores:", erro)

    cursor.close()
    conexao.close()


def buscar_eleitor():

    cpf = input("Digite o CPF do eleitor: ")

    cpf = limpar_numeros(cpf)
    cpf_criptografado = cifrar_hill(cpf)

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM eleitores WHERE cpf = %s",
            (cpf_criptografado,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")
            return

        eleitor = dados[0]

        print("\nID:", eleitor[0])
        print("Nome:", eleitor[1])
        print("Título:", eleitor[2])
        print("CPF:", decifrar_hill(eleitor[3]))
        print("Mesário:", "Sim" if eleitor[4] == 1 else "Não")
        print("Chave:", decifrar_hill(eleitor[5]))
        print("Já votou:", "Sim" if eleitor[6] == 1 else "Não")

    except Error as erro:
        print("Erro ao buscar eleitor:", erro)

    cursor.close()
    conexao.close()


def editar_eleitor():

    cpf = input("Digite o CPF do eleitor: ")

    cpf = limpar_numeros(cpf)
    cpf_criptografado = cifrar_hill(cpf)

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM eleitores WHERE cpf = %s",
            (cpf_criptografado,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")
            return

        novo_nome = input("Novo nome: ")

        novo_titulo = input("Novo título: ")

        if not validar_titulo(novo_titulo):
            return

        novo_titulo = limpar_numeros(novo_titulo)

        mesario = input("Mesário (S/N): ").upper()

        if mesario == "S":
            mesario = True

        elif mesario == "N":
            mesario = False

        else:
            print("Digite apenas S ou N.")
            return

        sql = """
        UPDATE eleitores
        SET nome = %s,
            Titulo_eleitor = %s,
            mesario = %s
        WHERE cpf = %s
        """

        valores = (
            novo_nome,
            novo_titulo,
            mesario,
            cpf_criptografado
        )

        cursor.execute(sql, valores)

        conexao.commit()

        print("Eleitor atualizado com sucesso!")

    except Error as erro:
        print("Erro ao editar eleitor:", erro)

    cursor.close()
    conexao.close()


def remover_eleitor():

    cpf = input("Digite o CPF do eleitor: ")

    cpf = limpar_numeros(cpf)
    cpf_criptografado = cifrar_hill(cpf)

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM eleitores WHERE cpf = %s",
            (cpf_criptografado,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")
            return

        cursor.execute(
            "DELETE FROM eleitores WHERE cpf = %s",
            (cpf_criptografado,)
        )

        conexao.commit()

        print("Eleitor removido com sucesso!")

    except Error as erro:
        print("Erro ao remover eleitor:", erro)

    cursor.close()
    conexao.close()


def menu_eleitor():

    opcao = ""

    while opcao != "0":

        print("\n=== MENU ELEITORES ===")
        print("1 - Cadastrar eleitor")
        print("2 - Editar eleitor")
        print("3 - Remover eleitor")
        print("4 - Buscar eleitor")
        print("5 - Listar eleitores")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_eleitor()

        elif opcao == "2":
            editar_eleitor()

        elif opcao == "3":
            remover_eleitor()

        elif opcao == "4":
            buscar_eleitor()

        elif opcao == "5":
            listar_eleitores()

        elif opcao == "0":
            print("Voltando...")

        else:
            print("Opção inválida!")