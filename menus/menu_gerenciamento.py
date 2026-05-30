from menus.menu_eleitor import menu_eleitor
from menus.menu_candidato import menu_candidato


def menu_gerenciamento():
    """
    Exibe o menu de gerenciamento de eleitores e candidatos.

    Args:
        Nenhum.

    Returns:
        None.
    """

    opcao = ""

    while opcao != "0":

        print("\n=== GERENCIAMENTO ===")
        print("1 - Eleitores")
        print("2 - Candidatos")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_eleitor()

        elif opcao == "2":
            menu_candidato()

        elif opcao == "0":
            print("Voltando...")

        else:
            print("Opção inválida!")