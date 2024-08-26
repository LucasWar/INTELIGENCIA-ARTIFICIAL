from tsp import Solver
import os
import random 

solve = Solver("FRI26.txt")
solve.algoritmoGenetico()


# solver = Solver("ATT48.txt")
# distMedia = tempoMedio = maiorDist = menorDist = 0
# menorDist = float('inf')
# numPassos = 0
# for _ in range(0,10):
#     solver.subidaDeEncosta()
#     caminho, distancia, tempo = solver.retorneResultados()

#     if distancia > maiorDist:
#         maiorDist = distancia
    
#     elif distancia < menorDist:
#         menorDist = distancia

#     distMedia += distancia
#     tempoMedio += tempo
# tempoMedio = tempoMedio / 10
# distMedia = distMedia / 10
# print("Maior distancia {}, menor distancia {}".format(maiorDist,menorDist))
# print("Tempo medio {}, distancia media {}".format(tempoMedio,distMedia))
