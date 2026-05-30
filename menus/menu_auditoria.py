from auditoria.logs_auditoria import exibir_logs, exibir_protocolos


def menu_auditoria():
    """
    Exibe o menu de auditoria do sistema de votação.

    Args:
        Nenhum.

    Returns:
        None.
    """

    opcao = ""

    while opcao != "0":

        print("\nVocê Entrou no Modo Auditoria")
        print("Modo Auditoria")
        print("1- Mostrar logs de Ocorrências")
        print("2- Exibir Protocolos de Votação")
        print("0- Voltar")

        opcao = input("Escolha uma das opções: ").strip()

        if opcao == "1":
            exibir_logs()

        elif opcao == "2":
            exibir_protocolos()

        elif opcao == "0":
            print("Retornando...")

        else:
            print("Opção inválida... Tente Novamente")