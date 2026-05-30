try:
    from mysql.connector import Error
except ModuleNotFoundError:
    Error = Exception


def conectar():
    """
    Realiza a conexão com o banco de dados MySQL.

    Returns:
        mysql.connector.connection:
        Objeto de conexão com o banco de dados.

    Raises:
        ModuleNotFoundError:
        Caso a biblioteca mysql-connector-python
        não esteja instalada.
    """

    try:
        import mysql.connector
    except ModuleNotFoundError:
        print("Biblioteca mysql-connector-python não instalada.")
        print("Instale com: pip install mysql-connector-python")
        raise

    conexao = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Dudu4189*",
        database="projeto_integrador",
        port=3306
    )

    return conexao