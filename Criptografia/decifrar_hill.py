def decifrar_hill(texto):
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

    return numeros_para_texto(descriptografado)


