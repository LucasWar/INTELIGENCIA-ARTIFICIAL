from solvers import Solver
from slidingPuzzle import slidingPuzzle
import utils

tabuleiroInicial = slidingPuzzle()     
tabuleiroInicial.iniciarTabuleiro(4)
tabuleiroInicial.randomizar()

solve = Solver()
print("TABULEIRO INCIAL")
print(tabuleiroInicial.mostrarTabIncial())

print("TABULEIRO OBJETIVO")
print(tabuleiroInicial.mostrarTabObjetivo())

caminho, memoria, nosExpandidos, fatorRamificacao,tempo = solve.buscaProfInterativo(tabuleiroInicial)
utils.mostrarResultados(caminho, memoria, nosExpandidos, fatorRamificacao,tempo)