from tps import Solver
import os

def lerArquivo(nome):
    arquivo = open(os.getcwd()+"\\trabalhoIA_part2\\entradas\\"+nome, "r")
    texto = arquivo.read()
    linhas = texto.strip().split('\n')
    
  
    matriz = []
    for linha in linhas:
        elementos = list(map(float, linha.split()))
        matriz.append(elementos)
    
    return matriz


matriz = lerArquivo('FRI26.txt')
solver = Solver(matriz)

solver.subidaDeEncosta()
solver.imprimirResultados()

solver.algoritmoGenetico()
solver.imprimirResultados()

solver.temperaSimulada()
solver.imprimirResultados()

solver.buscaTabu()
solver.imprimirResultados()