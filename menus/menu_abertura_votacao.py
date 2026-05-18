eleitores = []
candidatos = [
    {"numero": "10", "partido": "AAA", "votos": 0},
    {"numero": "20", "partido": "BBB", "votos": 0}
]

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
    for candidato in candidatos:
        print(f"Número: {candidato['numero']} | Votos: {candidato['votos']}")


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


opcao = ""

while opcao != "2":
    print("\n=== SISTEMA ===")
    print("1 - Cadastrar mesário")
    print("2 - Abrir votação")

    opcao = input("Escolha: ")

    if opcao == "1":
        cadastrar_mesario()
    elif opcao == "2":
        abrir_votacao()
    else:
        print("Opção inválida!")
