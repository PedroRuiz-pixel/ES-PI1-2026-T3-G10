from mysql.connector import Error
from conexao import conectar
import random
from menu_auditoria import menu_auditoria

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

        cursor.execute(
            "UPDATE eleitores SET nome=%s, titulo=%s WHERE cpf=%s",
            (novo_nome, novo_titulo, cpf)
        )
        conexao.commit()

        print("Eleitor atualizado com sucesso!")

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
        if len(cursor.fetchall()) == 0:
            print("Eleitor não encontrado.")
            return

        cursor.execute("DELETE FROM eleitores WHERE cpf = %s", (cpf,))
        conexao.commit()

        print("Eleitor removido com sucesso!")

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

    for c in candidatos:
        if c["numero"] == numero:
            print("Erro: Já existe candidato com esse número!")
            return

    candidato = {
        "nome": nome,
        "numero": numero,
        "partido": partido
    }

    candidatos.append(candidato)
    print("Candidato cadastrado com sucesso!")


def listar_candidatos():
   
    if not candidatos:
        print("Nenhum candidato cadastrado.")
        return

    print("\nLista de candidatos:")
    for c in candidatos:
        print(f"Nome: {c['nome']} | Número: {c['numero']} | Partido: {c['partido']}")


def buscar_candidato():
  
    numero = input("Digite o número do candidato: ")

    for c in candidatos:
        if c["numero"] == numero:
            print("Candidato encontrado:")
            print(f"Nome: {c['nome']} | Número: {c['numero']} | Partido: {c['partido']}")
            return

    print("Candidato não encontrado.")


def editar_candidato():
 
    numero = input("Digite o número do candidato para editar: ")

    for c in candidatos:
        if c["numero"] == numero:
            novo_nome = input("Novo nome do candidato: ")
            novo_numero = input("Novo número do candidato: ")
            novo_partido = input("Novo partido: ")

            for candidato in candidatos:
                if candidato["numero"] == novo_numero and candidato != c:
                    print("Erro: Já existe candidato com esse número!")
                    return

            c["nome"] = novo_nome
            c["numero"] = novo_numero
            c["partido"] = novo_partido

            print("Candidato editado com sucesso!")
            return

    print("Candidato não encontrado.")


def remover_candidato():
  
    numero = input("Digite o número do candidato para remover: ")

    for c in candidatos:
        if c["numero"] == numero:
            candidatos.remove(c)
            print("Candidato removido com sucesso!")
            return

    print("Candidato não encontrado.")


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
    for eleitor in eleitores:
        if (
            eleitor["titulo"] == titulo and
            eleitor["cpf_inicio"] == cpf_inicio and
            eleitor["chave"] == chave and
            eleitor["mesario"] == True
        ):
            return True
    return False


def zeresima():
    votos_registrados.clear()

    for candidato in candidatos:
        candidato["votos"] = 0

    print("\n=== ZERÉSIMA ===")

    if not candidatos:
        print("Nenhum candidato cadastrado.")
    else:
        for candidato in candidatos:
            print(f"Número: {candidato['numero']} | Votos: 0")


def menu_urna():
    opcao = ""

    while opcao != "2":
        print("\n=== MENU DA URNA ===")
        print("1 - Votar")
        print("2 - Encerrar votação")

        opcao = input("Escolha: ")

        if opcao == "1":
            print("Função votar ainda não implementada")
        elif opcao == "2":
            print("Encerrando votação...")
        else:
            print("Opção inválida!")


def abrir_votacao():
    print("\n=== ABERTURA DA VOTAÇÃO ===")

    titulo = input("Título de eleitor: ")
    cpf_inicio = input("4 primeiros dígitos do CPF: ")
    chave = input("Chave de acesso: ")

    if validar_mesario(titulo, cpf_inicio, chave):
        print("Acesso liberado!")
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
    print("\nResultados da votação")


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
