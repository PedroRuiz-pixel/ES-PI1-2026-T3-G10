from menus.menu_gerenciamento import menu_gerenciamento
from menus.menu_votacao import menu_votacao


def menu_principal():

    opcao = ""

    while opcao != "0":

        print("\n===== SISTEMA DE VOTAÇÃO =====")
        print("1 - Gerenciamento")
        print("2 - Votação")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

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
