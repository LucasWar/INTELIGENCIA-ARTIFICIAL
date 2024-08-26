def mostrarResultados(caminho, memoria, nosExpandidos, fatorRamificacao,tempo, imprimirPassos = False):
    caminho.solucao(imprimirPassos)
    print("TEMPO DE EXECUÇÂO: ",tempo)
    print("NUMERO NOS EXPANDIDOS",nosExpandidos)
    print("FATOR MEDIO DE RAMIFICAÇÃO", fatorRamificacao)
    print("Memoria: ", memoria)

def numeroDePecasCertas(tabAtual,tabObjetivo):
    count = 0
    for i in range(len(tabObjetivo)):
        for j in range(len(tabObjetivo[0])):
            if tabObjetivo[i][j] != tabAtual[i][j]:
                count += 1
    return count

def distManhattan(tabuleiroInicial,tabuleiroObj):  
    n = len(tabuleiroInicial)
    posicoes = {}

    for i in range(n):
        for j in range(n):
            if tabuleiroObj[i][j] not in posicoes:
                posicoes[tabuleiroObj[i][j]] = (i, j)

    soma = 0
    for i in range(n):
        for j in range(n):
            elemento = tabuleiroInicial[i][j]
            if elemento != 0:
                x2, y2 = posicoes[elemento]
                soma += abs(i - x2) + abs(j - y2)

    return soma