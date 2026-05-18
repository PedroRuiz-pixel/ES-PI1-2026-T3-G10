from mysql.connector import Error
from conexao import conectar
import random
import conexao
from menu_auditoria import menu_auditoria
from zerézima import zeresima
from logs_auditoria import registrar_log

# ================= ELEITORES =================

def gerar_chave_acesso(nome):
    partes = nome.strip().upper().split()

    if len(partes[0]) < 2:
        print("Nome precisa ter pelo menos 2 letras.")
        return ""

    if len(partes) >= 2:
        inicio = partes[0][0] + partes[0][1] + partes[1][0]
    else:
        inicio = partes[0][0] + partes[0][1] + "X"

    numero = str(random.randint(1000, 9999))
    chave = inicio + numero
    return chave


def validar_cpf(cpf):
    if cpf == cpf[0] * 11:
        print("CPF inválido.")
        return False

    # 1º
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

    # 2º
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
        if c >= '0' and c <= '9':
            titulo_limpo = titulo_limpo + c

    titulo = titulo_limpo

    if len(titulo) != 12:
        print("Título de eleitor deve ter 12 números.")
        return False

    return True


def cadastrar_eleitor():
    nome = input("Nome: ")
    titulo = input("Título de Eleitor: ")

    
    if not validar_titulo(titulo):
        return

    titulo_limpo = ""
    for c in titulo:
        if c >= '0' and c <= '9':
            titulo_limpo = titulo_limpo + c

    titulo = titulo_limpo

    cpf = input("CPF: ")

    if nome == "" or titulo == "" or cpf == "":
        print("Todos os campos são obrigatórios.")
        return

    cpf_limpo = ""
    for c in cpf:
        if c >= '0' and c <= '9':
            cpf_limpo = cpf_limpo + c

    cpf = cpf_limpo

    if len(cpf) != 11:
        print("CPF deve ter 11 números.")
        return

    if not validar_cpf(cpf):
        return

    mesario = input("Mesário(S/N): ").upper()

    if mesario == "S":
        mesario = True
    elif mesario == "N":
        mesario = False
    else:
        print("Digite apenas S ou N para mesário.")
        return

    chave_acesso = gerar_chave_acesso(nome)

    if chave_acesso == "":
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf,))
        if len(cursor.fetchall()) > 0:
            print("Erro: CPF já cadastrado.")
            return

        sql = "INSERT INTO eleitores VALUES (NULL, %s, %s, %s, %s, %s, %s)"
        valores = (nome, titulo, cpf, mesario, chave_acesso, False)

        cursor.execute(sql, valores)
        conexao.commit()

        print("Eleitor cadastrado com sucesso!")

        registrar_log(
        "Cadastro",
        "Eleitor " + nome + " cadastrado"
        )

        print("Chave de Acesso:", chave_acesso)

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
        else:
            i = 0
            while i < len(dados):
                eleitor = dados[i]

                print("\nID:", eleitor[0])
                print("Nome:", eleitor[1])
                print("Título:", eleitor[2])
                print("CPF:", eleitor[3])
                print("Mesário:", "Sim" if eleitor[4] == 1 else "Não")
                print("Chave de Acesso:", eleitor[5])
                print("Já votou:", "Sim" if eleitor[6] == 1 else "Não")
                print("----------------------")

                i += 1

    except Error as erro:
        print("Erro ao listar eleitores:", erro)

    cursor.close()
    conexao.close()


def buscar_eleitor():
    cpf = input("Digite o CPF do eleitor: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf,))
        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")
        else:
            eleitor = dados[0]

            print("\nID:", eleitor[0])
            print("Nome:", eleitor[1])
            print("Título:", eleitor[2])
            print("CPF:", eleitor[3])
            print("Mesário:", "Sim" if eleitor[4] == 1 else "Não")
            print("Chave de Acesso:", eleitor[5])
            print("Já votou:", "Sim" if eleitor[6] == 1 else "Não")

    except Error as erro:
        print("Erro ao buscar eleitor:", erro)

    cursor.close()
    conexao.close()


def editar_eleitor():
    cpf = input("Digite o CPF do eleitor que deseja editar: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf,))
        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")
            return

        novo_nome = input("Novo nome: ")
        novo_titulo = input("Novo título: ")

        mesario = input("Mesário (S/N): ").upper()

        if mesario == "S":
            mesario = True

        elif mesario == "N":
            mesario = False

        else:
            print("Digite apenas S ou N.")
            return

        cursor.execute(
            "UPDATE eleitores SET nome=%s, titulo_eleitor=%s, mesario=%s WHERE cpf=%s",
            (novo_nome, novo_titulo, mesario, cpf)
        )

        conexao.commit()

        print("Eleitor atualizado com sucesso!")

        registrar_log(
            "Edição",
            "Eleitor " + novo_nome + " editado"
        )

    except Error as erro:
        print("Erro ao editar eleitor:", erro)

    cursor.close()
    conexao.close()


def remover_eleitor():
    cpf = input("Digite o CPF do eleitor que deseja remover: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf,))

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")
            return

        nome = dados[0][1]

        cursor.execute("DELETE FROM eleitores WHERE cpf = %s", (cpf,))
        conexao.commit()

        print("Eleitor removido com sucesso!")

        registrar_log(
            "Remoção",
            "Eleitor " + nome + " removido"
        )

    except Error as erro:
        print("Erro ao remover eleitor:", erro)

    cursor.close()
    conexao.close()


def menu_eleitor():
    opcao = ""

    while opcao != "0":
        print("\nVocê entrou no modulo de Eleitor!")
        print("1- Cadastrar eleitor")
        print("2- Editar eleitor")
        print("3- Remover eleitor")
        print("4- Buscar eleitor")
        print("5- Listar eleitores")
        print("0- Voltar")

        opcao = input("Digite uma opção: ").strip()

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


# ================= CANDIDATOS =================

candidatos = []  


def cadastrar_candidato():

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
            print("Erro: Já existe candidato com esse número!")
            return

        sql = """
        INSERT INTO candidatos
        VALUES (NULL, %s, %s, %s)
        """

        valores = (nome, numero, partido)

        cursor.execute(sql, valores)
        conexao.commit()

        print("Candidato cadastrado com sucesso!")

        registrar_log(
        "Cadastro",
        "Candidato " + nome + " cadastrado" )
                                        
    except Error as erro:
        print("Erro ao cadastrar candidato:", erro)

    cursor.close()
    conexao.close()


def listar_candidatos():
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
    numero = input("Digite o número do candidato: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM candidatos WHERE numero = %s", (numero,))

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Candidato não encontrado.")
            return
        
        candidato = dados[0]

        print("\nID:", candidato[0])
        print("Nome:", candidato[1])
        print("Número:", candidato[2])
        print("Partido:", candidato[3]) 
        print("----------------------")
        
    except Error as erro:
        print("Erro ao buscar candidato:", erro)

    cursor.close()
    conexao.close()


def editar_candidato():
 
    numero = input("Digite o número do candidato que deseja editar: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM candidatos WHERE numero = %s", (numero,))
        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Candidato não encontrado.")
            return

        novo_nome = input("Novo nome: ")
        novo_numero = input("Novo número: ")
        novo_partido = input("Novo partido: ")

        sql = """
        UPDATE candidatos
        SET nome = %s,
        numero = %s,
        partido = %s
        WHERE numero = %s
        """

        valores = (novo_nome, novo_numero, novo_partido, numero)

        cursor.execute(sql, valores)
        
        conexao.commit()

        print("Candidato atualizado com sucesso!")

        registrar_log(
            "Edição",
            "Candidato " + novo_nome + " editado" )
    
    except Error as erro:
        print("Erro ao editar candidato:", erro)

    cursor.close()
    conexao.close()


def remover_candidato():
  
    numero = input("Digite o número do candidato que deseja remover: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT * FROM candidatos WHERE numero = %s", (numero,))

        dados = cursor.fetchall()
        nome = dados[0][1]

        if len(dados) == 0:
            print("Candidato não encontrado.")
            return
        
        cursor.execute("DELETE FROM candidatos WHERE numero = %s", (numero,))
        
        conexao.commit()

        print("Candidato removido com sucesso!")

        registrar_log(
            "Remoção",
            "Candidato " + nome + " removido" )

    except Error as erro:
        print("Erro ao remover candidato:", erro)
    
    cursor.close()
    conexao.close()


def menu_candidato():
  
    opcao = ""

    while opcao != "6":
        print("\n=== MENU DE CANDIDATOS ===")
        print("1 - Cadastrar candidato")
        print("2 - Listar candidatos")
        print("3 - Buscar candidato")
        print("4 - Editar candidato")
        print("5 - Remover candidato")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ")

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
        elif opcao == "6":
            print("Saindo do menu...")
        else:
            print("Opção inválida!")




# ================= GERENCIAMENTO =================

def menu_gerenciamento():
    continuar = 1

    while continuar == 1:
        print("\n----- MENU DE GERENCIAMENTO -----")
        print("1 - Eleitores")
        print("2 - Candidatos")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_eleitor()
        elif opcao == "2":
            menu_candidato()
        elif opcao == "0":
            print("Saindo do menu de gerenciamento...")
            continuar = 0
        else:
            print("Opção inválida. Tente novamente.")



# ================= ABERTURA DE VOTAÇÃO =================

eleitores = []
votos_registrados = []


def cadastrar_mesario():
    titulo = input("Título de eleitor: ")
    cpf_inicio = input("4 primeiros dígitos do CPF: ")
    chave = input("Chave de acesso: ")

    eleitor = {
        "titulo": titulo,
        "cpf_inicio": cpf_inicio,
        "chave": chave,
        "mesario": True
    }

    eleitores.append(eleitor)
    print("Mesário cadastrado com sucesso!")


def validar_mesario(titulo, cpf_inicio, chave):

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            "SELECT * FROM eleitores WHERE titulo_eleitor = %s",
            (titulo,)
        )

        dados = cursor.fetchall()

        if len(dados) == 0:
            cursor.close()
            conexao.close()
            return False

        eleitor = dados[0]

        cpf = eleitor[3]
        mesario = eleitor[4]
        chave_banco = eleitor[5]

        if (
            cpf[0:4] == cpf_inicio and
            chave == chave_banco and
            mesario == 1
        ):
            cursor.close()
            conexao.close()
            return True

        cursor.close()
        conexao.close()
        return False

    except Error as erro:
        print("Erro ao validar mesário:", erro)

        cursor.close()
        conexao.close()

        return False


def votar():
    cpf = input("Digite o seu CPF: ")

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
        "SELECT * FROM eleitores WHERE cpf = %s", (cpf,))

        dados = cursor.fetchall()

        if len(dados) == 0:
            print("Eleitor não encontrado.")
            return
    
        eleitor = dados[0]

        if eleitor[6] == 1:
            print("Eleitor já votou.")
            return
    
        cursor.execute("SELECT * FROM candidatos")

        candidatos_banco = cursor.fetchall()

        if len(candidatos_banco) == 0:
            print("Nenhum candidato cadastrado.")
            return

        for candidato in candidatos_banco:
         print("\nID:", candidato[0])
         print("Nome:", candidato[1])
         print("Número:", candidato[2])

        numero = input("\nDigite o número do candidato que deseja votar: ")

        cursor.execute("SELECT * FROM candidatos WHERE numero = %s", (numero,))

        candidatos = cursor.fetchall()

        if len(candidatos) == 0:
            print("Candidato não encontrado.")
            return
    
        candidato_id = candidatos[0][0]

        cursor.execute(
         "INSERT INTO votos (candidato_id, data_hora, protocolo) VALUES (%s, NOW(), UUID())", (candidato_id,))
    
        cursor.execute("UPDATE eleitores SET ja_votou = 1 WHERE cpf = %s", (cpf,))

        conexao.commit()

        print("Voto registrado com sucesso!")

        registrar_log(
            "Voto",
            "Eleitor com CPF " + cpf + " realizou votação" ) 

    except Error as erro:
        print("Erro ao registrar voto:", erro)

    cursor.close()
    conexao.close()


def menu_urna():
    opcao = ""

    while opcao != "2":
        print("\n=== MENU DA URNA ===")
        print("1 - Votar")
        print("2 - Encerrar votação")

        opcao = input("Escolha: ")

        if opcao == "1":
            votar()

        elif opcao == "2":
            print("Encerrando votação...")

            registrar_log(
            "Encerramento",
            "Sistema de votação encerrado"
            )

        else:
            print("Opção inválida!")


def abrir_votacao():
    print("\n=== ABERTURA DA VOTAÇÃO ===")

    titulo = input("Título de eleitor: ")
    cpf_inicio = input("4 primeiros dígitos do CPF: ")
    chave = input("Chave de acesso: ")

    if validar_mesario(titulo, cpf_inicio, chave):
        print("Acesso liberado!")
        registrar_log(
            "Abertura",
            "Sistema de votação aberto por mesário"
                )
        zeresima()
        menu_urna()
    else:
        print("Erro: acesso negado!")


def menu_abertura_votacao():
    opcao = ""

    while opcao != "0":
        print("\n=== SISTEMA DE ABERTURA ===")
        print("1 - Cadastrar mesário")
        print("2 - Abrir votação")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_mesario()
        elif opcao == "2":
            abrir_votacao()
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")



# ================= RESULTADOS =================

def menu_resultados():

    conexao = conectar()
    cursor = conexao.cursor()

    try:

        print("\n=== RESULTADOS DA VOTAÇÃO ===")

        sql = """
        SELECT candidatos.nome,
               candidatos.numero,
               COUNT(votos.id)
        FROM candidatos
        LEFT JOIN votos
        ON candidatos.id = votos.candidato_id
        GROUP BY candidatos.id
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        if len(resultados) == 0:
            print("Nenhum resultado encontrado.")
            return

        for resultado in resultados:

            nome = resultado[0]
            numero = resultado[1]
            total = resultado[2]

            print("\nNome:", nome)
            print("Número:", numero)
            print("Total de votos:", total)

    except Error as erro:
        print("Erro ao mostrar resultados:", erro)

    cursor.close()
    conexao.close()


# ================= VOTAÇÃO =================

def menu_votacao():
    opcao = ""

    while opcao != "0":
        print("=" * 50)
        print("Módulo de votação")
        print("=" * 50)
        print("1- Abrir sistema de votação")
        print("2- Auditoria de votação")
        print("3- Resultados da votação")
        print("0- Voltar")
        print("=" * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_abertura_votacao()
        elif opcao == "2":
            menu_auditoria()
        elif opcao == "3":
            menu_resultados()
        elif opcao == "0":
            print("\nVoltando...")
        else:
            print("Opção inválida!")


# ================= MENU PRINCIPAL =================

def menu_principal():
    opcao = ""

    while opcao != "0":
        print("\n===== SISTEMA DE VOTAÇÃO =====")
        print("1 - Gerenciamento")
        print("2 - Votação")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_gerenciamento()
        elif opcao == "2":
            menu_votacao()
        elif opcao == "0":
            print("Encerrando sistema...")
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_principal()
