from menus.menu_abertura_votacao import menu_abertura_votacao
from menus.menu_auditoria import menu_auditoria
from menus.menu_resultados import menu_resultados


def menu_votacao():
    """
    Exibe o menu principal da votação.

    Permite acessar a abertura da votação,
    auditoria e resultados do sistema.

    Args:
        Nenhum.

    Returns:
        None.
    """

    opcao = ""

    while opcao != "0":

        print("\n=== VOTAÇÃO ===")
        print("1 - Abrir sistema")
        print("2 - Auditoria")
        print("3 - Resultados")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_abertura_votacao()

        elif opcao == "2":
            menu_auditoria()

        elif opcao == "3":
            menu_resultados()

        elif opcao == "0":
            print("Voltando...")

        else:
            print("Opção inválida!")