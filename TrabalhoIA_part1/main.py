from solvers import Solver
from slidingPuzzle import slidingPuzzle
import time
inicio = time.time()

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

tabuleiroInicial = slidingPuzzle()     
tabuleiroInicial.iniciarTabuleiro(5)
tabuleiroInicial.randomizar()
solve = Solver()
print("TABULEIRO INCIAL")
print(tabuleiroInicial.mostrarTabIncial())

print("TABULEIRO OBJETIVO")
print(tabuleiroInicial.mostrarTabObjetivo())
#UTILIZANDO BFS, BUSCA EM PROFUDIDADE 
#caminho, memoria, nosExpandidos, fatorRamificacao = solve.bfs(tabuleiroInicial)

# UTILIZANDO A*, PARA UTILIZAR OUTRA HEURISTICA BASTA TROCAR 'distManhattan' por 'numeroDePecasCertas'
#caminho, memoria, nosExpandidos, fatorRamificacao = solve.AStar(tabuleiroInicial,distManhattan)

#UTILIZADNO DFS 
#caminho,nosExpandidos,fatorRamificacao,memoria = solve.buscaProfInterativo(tabuleiroInicial)

# UTILIZADNO A* BDIDIRECIONAL 
caminho, memoria, nosExpandidos, fatorRamificacao = solve.bidirecionalAstar(tabuleiroInicial,distManhattan)
    
fim = time.time()
caminho.solucao()
print("TEMPO DE EXECUÇÂO: ",fim - inicio)
print("NUMERO NOS EXPANDIDOS",nosExpandidos)
print("FATOR MEDIO DE RAMIFICAÇÃO", fatorRamificacao)
print("Memoria: ", memoria)