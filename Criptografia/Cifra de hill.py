ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MODULO = len(ALFABETO)  


def limpar_texto(texto):
    
    texto = texto.upper()
    resultado = ""

    for caractere in texto:
        if caractere in ALFABETO:
            resultado += caractere

    return resultado


def texto_para_numeros(texto):
    
    numeros = []

    for caractere in texto:
        numeros.append(ALFABETO.index(caractere))

    return numeros


def numeros_para_texto(numeros):
   
    texto = ""

    for numero in numeros:
        texto += ALFABETO[numero % MODULO]

    return texto


def multiplicar_matriz_vetor(matriz, vetor):
    
    resultado_1 = (matriz[0][0] * vetor[0] + matriz[0][1] * vetor[1]) % MODULO
    resultado_2 = (matriz[1][0] * vetor[0] + matriz[1][1] * vetor[1]) % MODULO

    return [resultado_1, resultado_2]


def cifrar_hill(texto):
 
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
