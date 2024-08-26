from solvers import Solver
from slidingPuzzle import slidingPuzzle
import time
import utils

tabuleiroInicial = slidingPuzzle()     
tabuleiroInicial.iniciarTabuleiro(6)
tabuleiroInicial.randomizar()

solve = Solver()
print("TABULEIRO INCIAL")
print(tabuleiroInicial.mostrarTabIncial())

print("TABULEIRO OBJETIVO")
print(tabuleiroInicial.mostrarTabObjetivo())

caminho, memoria, nosExpandidos, fatorRamificacao,tempo = solve.bidirecionalAstar(tabuleiroInicial,utils.distManhattan)
utils.mostrarResultados(caminho, memoria, nosExpandidos, fatorRamificacao,tempo)