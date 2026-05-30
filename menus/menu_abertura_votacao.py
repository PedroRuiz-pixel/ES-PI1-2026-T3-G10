from mysql.connector import Error
from database.conexao import conectar
import random

from auditoria.logs_auditoria import registrar_log
from votacao.zeresima import zeresima
from Criptografia.cifra_hill import cifrar_hill, decifrar_hill

def gerar_protocolo(cursor, numero_candidato):

    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    letra1 = random.choice(letras)
    letra2 = random.choice(letras)

    ano = "26"

    if numero_candidato is None:
        numero_formatado = "00"
    else:
        numero_formatado = str(numero_candidato).zfill(2)

    aleatorio = str(random.randint(0, 99999)).zfill(5)

    protocolo = (
        "V" +
        letra1 +
        letra2 +
        ano +
        numero_formatado +
        aleatorio
    )

    protocolo_criptografado = cifrar_hill(protocolo)

    cursor.execute(
        "SELECT * FROM votos WHERE protocolo = %s",
        (protocolo_criptografado,)
    )

    dados = cursor.fetchall()

    while len(dados) > 0:

        letra1 = random.choice(letras)
        letra2 = random.choice(letras)

        aleatorio = str(random.randint(0, 99999)).zfill(5)

        protocolo = (
            "V" +
            letra1 +
            letra2 +
            ano +
            numero_formatado +
            aleatorio
        )

        protocolo_criptografado = cifrar_hill(protocolo)

        cursor.execute(
            "SELECT * FROM votos WHERE protocolo = %s",
            (protocolo_criptografado,)
        )

        dados = cursor.fetchall()

    return protocolo


def validar_mesario(titulo, cpf_inicio, chave):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM eleitores WHERE Titulo_eleitor = %s",
            (titulo,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            return False

        eleitor = dados[0]

        cpf = decifrar_hill(eleitor[3])
        mesario = eleitor[4]
        chave_banco = decifrar_hill(eleitor[5])

        

        if (
            cpf[:4] == cpf_inicio and
            chave == chave_banco and
            mesario == 1
        ):
            return True

        return False

    except Error as erro:
        print("Erro ao validar mesário:", erro)
        return False

    finally:
        cursor.close()
        conexao.close()


def votar():

    titulo = input("Digite seu título de eleitor: ")
    cpf_inicio = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite sua chave de acesso: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM eleitores WHERE Titulo_eleitor = %s",
            (titulo,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")

            registrar_log(
                "ALERTA: Tentativa de acesso negado"
            )

            return

        eleitor = dados[0]

        cpf = decifrar_hill(eleitor[3])
        chave_banco = decifrar_hill(eleitor[5])

        if cpf[0:4] != cpf_inicio or chave != chave_banco:
            print("Dados inválidos.")

            registrar_log(
                "ALERTA: Tentativa de acesso negado"
            )

            return

        if eleitor[6] == 1:
            print("Eleitor já votou.")

            registrar_log(
                "ALERTA: Tentativa de voto duplo"
            )

            return

        voto_confirmado = False

        while voto_confirmado == False:

            numero = input("\nNúmero do candidato: ")

            cursor.execute(
                "SELECT * FROM candidatos WHERE numero = %s",
                (numero,)
            )

            candidato = cursor.fetchall()

            if len(candidato) == 0:

                print("Candidato não encontrado.")

                confirmar = input(
                    "Deseja confirmar voto nulo? (S/N): "
                ).upper()

                if confirmar == "S":
                    candidato_id = None
                    voto_confirmado = True

                else:
                    print("Voto cancelado. Digite novamente.")

            else:

                print("\n=== CONFIRMAÇÃO DO VOTO ===")
                print("Nome:", candidato[0][1])
                print("Número:", candidato[0][2])
                print("Partido:", candidato[0][3])

                confirmar = input(
                    "Confirmar voto? (S/N): "
                ).upper()

                if confirmar == "S":
                    candidato_id = candidato[0][0]
                    voto_confirmado = True

                else:
                    print("Voto cancelado. Digite novamente.")

        if candidato_id is None:
            numero_protocolo = None
        else:
            numero_protocolo = candidato[0][2]

        protocolo = gerar_protocolo(
            cursor,
            numero_protocolo
        )

        protocolo_criptografado = cifrar_hill(protocolo)

        sql = """
        INSERT INTO votos
        (candidato_id, data_hora, protocolo)
        VALUES (%s, NOW(), %s)
        """

        cursor.execute(sql, (candidato_id, protocolo_criptografado))

        cursor.execute(
            "UPDATE eleitores SET ja_votou = 1 WHERE Titulo_eleitor = %s",
            (titulo,)
        )

        conexao.commit()

        print("Voto registrado com sucesso!")
        print("Protocolo de votação:", protocolo)

        registrar_log(
            "SUCESSO: Voto realizado com sucesso"
        )

    except Error as erro:
        print("Erro ao registrar voto:", erro)

    cursor.close()
    conexao.close()


def menu_urna():

    opcao = ""

    while opcao != "2":

        print("\n=== MENU URNA ===")
        print("1 - Votar")
        print("2 - Encerrar votação")

        opcao = input("Escolha: ")

        if opcao == "1":
            votar()

        elif opcao == "2":

            print("\n=== ENCERRAMENTO DA VOTAÇÃO ===")

            titulo = input("Título de eleitor do mesário: ")
            cpf_inicio = input("4 primeiros dígitos do CPF: ")
            chave = input("Chave de acesso: ")

            if not validar_mesario(titulo, cpf_inicio, chave):
                print("Erro: acesso negado.")
                opcao = ""
                continue

            confirmar = input("Deseja realmente encerrar a votação? (S/N): ").upper()

            if confirmar != "S":
                print("Encerramento cancelado.")
                opcao = ""
                continue

            chave_confirmacao = input("Digite novamente a chave de acesso: ")

            if chave_confirmacao != chave:
                print("Chave incorreta. Encerramento cancelado.")
                opcao = ""
                continue

            print("Encerrando votação...")

            registrar_log(
                "ENCERRAMENTO: Votação finalizada com sucesso."
            )

        else:
            print("Opção inválida!")


def abrir_votacao():

    print("\n=== ABERTURA DA VOTAÇÃO ===")

    titulo = input("Título: ")

    cpf_inicio = input("4 primeiros dígitos do CPF: ")

    chave = input("Chave de acesso: ")

    if validar_mesario(titulo, cpf_inicio, chave):

        print("Acesso liberado!")

        registrar_log(
            "ABERTURA: Votação iniciada com sucesso. Total de votos zerado."
        )

        zeresima()

        menu_urna()

    else:
        print("Acesso negado.")

        registrar_log(
            "ALERTA: Tentativa de acesso negado"
        )


def menu_abertura_votacao():

    opcao = ""

    while opcao != "0":

        print("\n=== ABERTURA DE VOTAÇÃO ===")
        print("1 - Abrir votação")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            abrir_votacao()

        elif opcao == "0":
            print("Voltando...")

        else:
            print("Opção inválida!")
