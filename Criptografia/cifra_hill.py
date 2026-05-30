ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MODULO = len(ALFABETO)


def limpar_texto(texto):
    """
    Remove caracteres inválidos e converte o texto para letras maiúsculas.

    Args:
        texto (str): Texto original que será tratado.

    Returns:
        str: Texto contendo apenas caracteres presentes no alfabeto permitido.
    """

    texto = texto.upper()
    resultado = ""

    for caractere in texto:

        if caractere in ALFABETO:
            resultado += caractere

    return resultado


def texto_para_numeros(texto):
    """
    Converte cada caractere do texto em seu índice numérico no alfabeto.

    Args:
        texto (str): Texto que será convertido para números.

    Returns:
        list: Lista de números correspondentes aos caracteres do texto.
    """

    numeros = []

    for caractere in texto:
        numeros.append(ALFABETO.index(caractere))

    return numeros


def numeros_para_texto(numeros):
    """
    Converte uma lista de números em texto usando o alfabeto definido.

    Args:
        numeros (list): Lista de números que será convertida para texto.

    Returns:
        str: Texto gerado a partir dos números informados.
    """

    texto = ""

    for numero in numeros:
        texto += ALFABETO[numero % MODULO]

    return texto


def multiplicar_matriz_vetor(matriz, vetor):
    """
    Multiplica uma matriz 2x2 por um vetor de dois elementos.

    Args:
        matriz (list): Matriz 2x2 usada na operação.
        vetor (list): Vetor com dois valores numéricos.

    Returns:
        list: Lista com dois números resultantes da multiplicação modular.
    """

    resultado_1 = (
        matriz[0][0] * vetor[0] +
        matriz[0][1] * vetor[1]
    ) % MODULO

    resultado_2 = (
        matriz[1][0] * vetor[0] +
        matriz[1][1] * vetor[1]
    ) % MODULO

    return [resultado_1, resultado_2]


def cifrar_hill(texto):
    """
    Criptografa um texto utilizando o método da Cifra de Hill.

    Args:
        texto (str): Texto original que será criptografado.

    Returns:
        str: Texto criptografado pela Cifra de Hill.
    """

    chave = [
        [5, 7],
        [2, 3]
    ]

    texto = limpar_texto(texto)

    if len(texto) % 2 != 0:
        texto += "X"

    numeros = texto_para_numeros(texto)
    criptografado = []

    for i in range(0, len(numeros), 2):

        bloco = [numeros[i], numeros[i + 1]]
        bloco_cifrado = multiplicar_matriz_vetor(chave, bloco)

        criptografado.extend(bloco_cifrado)

    return numeros_para_texto(criptografado)


def decifrar_hill(texto):
    """
    Descriptografa um texto criptografado com a Cifra de Hill.

    Args:
        texto (str): Texto criptografado que será descriptografado.

    Returns:
        str: Texto descriptografado.
    """

    chave_inversa = [
        [3, 29],
        [34, 5]
    ]

    texto = limpar_texto(texto)

    numeros = texto_para_numeros(texto)
    descriptografado = []

    for i in range(0, len(numeros), 2):

        bloco = [numeros[i], numeros[i + 1]]
        bloco_decifrado = multiplicar_matriz_vetor(chave_inversa, bloco)

        descriptografado.extend(bloco_decifrado)

    return numeros_para_texto(descriptografado).rstrip("X")