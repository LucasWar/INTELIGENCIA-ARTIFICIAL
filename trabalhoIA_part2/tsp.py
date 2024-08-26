import random
import math
import time
import os
class Solver:    
    def __init__(self,arquivo = "FIVE.txt"):
        self.matriz = Solver.lerArquivo(arquivo)
        self.n = len(self.matriz)
        self.resultados  = None
        self.tempoConclucao = 0
        self.tempoIncial = time.time()


#========================================Auxilares===================================================


    def lerArquivo(nome):
        arquivo = open(os.getcwd()+"\\trabalhoIA_part2\\entradas\\"+nome, "r")
        texto = arquivo.read()
        linhas = texto.strip().split('\n')
        matriz = []
        for linha in linhas:
            elementos = list(map(float, linha.split()))
            matriz.append(elementos)

        return matriz

    def calcularDistancia(self,caminho: list[int]) -> int:
            matriz = self.matriz
            distancaiTotal = 0
            for i in range(1, len(caminho)):
                distancaiTotal += matriz[caminho[i-1]][caminho[i]]
            distancaiTotal += matriz[caminho[-1]][caminho[0]]
            return distancaiTotal

    def imprimirResultados(self):
        print("CAMINHO ENCONTRADO: ",self.resultados[0])
        print("CUSTO: ",self.resultados[1])
        print("TEMPO: ",self.tempoConclucao)

    def retorneResultados(self):
        return self.resultados[0],self.resultados[1],self.tempoConclucao


#========================================Subida de enconsta===================================================


    def subidaDeEncosta(self):
        self.tempoIncial = time.time()
        print("EXECUTANDO SUBIDA DE ENCOSTA")   
        def trocarPosicoes(caminho:list):
            caminhosPossiveis = []
            for i in range(0,len(caminho)):
                for j in range(i,len(caminho)):
                    caminhoAux = caminho.copy()
                    if(i != j):
                        aux = caminhoAux[i]
                        caminhoAux[i] = caminhoAux[j]
                        caminhoAux[j] = aux
                        caminhosPossiveis.append(caminhoAux)

            return caminhosPossiveis
        def gerarCaminho():
            caminho = []
            caminho.extend(i for i in range(0,self.n))
            random.shuffle(caminho)
            return caminho
        
        caminhoAtual = gerarCaminho()
        distanciaAtual = self.calcularDistancia(caminhoAtual)
        cont = 0
        while True:
            cont += 1
            caminhoAtualAux = caminhoAtual.copy()
            vizinhos = trocarPosicoes(caminhoAtual)
            for vizinho in vizinhos:
                distanciaVizinhoAtual = self.calcularDistancia(vizinho)
                if distanciaVizinhoAtual < distanciaAtual:
                    distanciaAtual = distanciaVizinhoAtual
                    caminhoAtual = vizinho.copy()

            if(caminhoAtual == caminhoAtualAux):
                break

        tempoFinal = time.time()
        self.tempoConclucao = tempoFinal - self.tempoIncial
        self.resultados = [caminhoAtual,distanciaAtual]
        self.imprimirResultados()
        print("NUMERO PASSOS ",cont)


#============================================Algoritmo Genetico==============================================


    def algoritmoGenetico(self,
                        probMutacao:float = 0.2,
                        tamPopulacao:int = 120,
                        numMaxGeracoes:int = 1000,
                        numNovosIndividuos:int = 120 ):
        self.tempoIncial = time.time()
        print("EXECUTANDO ALGORITIMO GENETICO")     

        def gerarPopulacao(tamPopulacao:int):
            populacaoInicial = []
            individuo = []
            n = len(self.matriz)
            for _ in range(0,tamPopulacao):
                individuo = []
                individuo.extend(i for i in range(0,n))
                random.shuffle(individuo)

                dist = self.calcularDistancia(individuo)
                populacaoInicial.append([individuo,dist])

                individuo[:] = reversed(individuo[:])

                dist = self.calcularDistancia(individuo)
                populacaoInicial.append([individuo,dist])
            return populacaoInicial
        
        def selecaoAleatoria(populacao: list[list[int],int]):
            selecionados = random.sample(populacao,k=10)
            melhorEscolha = min(selecionados, key=lambda x: x[1])
            return melhorEscolha
        
        def reproduzir(individuoX: list[int],individuoY:list[int]):
            if(individuoX == individuoY):    
                return individuoX
            else:
                individuoX = individuoX[0][:]
                individuoY = individuoY[0][:]
                n = len(individuoX)
                novoIndividuo = [None] * n
                c1, c2 = sorted(random.sample(range(n), 2))
                novoIndividuo[c1:c2] = individuoX[c1:c2]
                for i in range(n-1,-1,-1):
                    if(novoIndividuo[i] == None):
                        for gene in individuoY:
                            if(gene not in novoIndividuo):
                                novoIndividuo[i] = gene
                                individuoY.remove(gene)
                                break
            dist = self.calcularDistancia(novoIndividuo)            
            return [novoIndividuo, dist]
        
        def mutacao(caminho:list[int]):
            opcao = random.choice(['swap','reversed','shuffle'])
            n = len(caminho)
            if(opcao == 'reversed'):
                c1, c2 = sorted(random.sample(range(n), 2))
                caminho[c1:c2] = reversed(caminho[c1:c2])
            elif(opcao == 'swap'):
                c1, c2 = sorted(random.sample(range(n), 2))
                aux = caminho[c1]
                caminho[c1] = caminho[c2]
                caminho[c2] = aux
            else:
                c1, c2 = sorted(random.sample(range(n), 2))
                sublista = caminho[c1:c2]
                random.shuffle(sublista)
                caminho[c1:c2] = sublista
            return caminho

        def selecionarMelhorIndividuo(populacao:list[list[int]]):
            melhor = min(populacao, key=lambda x: x[1])
            return melhor     
        
        def selecionarElite(populacao:list[list[int]]):
            n = 10
            populacao = sorted(populacao, key=lambda x: x[1])
            elite = []
            individuosVistos = set()
            
            for individuo in populacao:
                individuo_tuple = tuple(individuo[0])  
                if individuo_tuple not in individuosVistos:
                    elite.append(individuo)
                    individuosVistos.add(individuo_tuple)
                if len(elite) >= n:
                    break
            
            return elite
        populacao = gerarPopulacao(tamPopulacao)
        melhorIndividuo = selecionarMelhorIndividuo(populacao)
        elite = selecionarElite(populacao.copy())

        for _ in range(0,numMaxGeracoes):
            novaPopulacao = []
            while(len(novaPopulacao) <= numNovosIndividuos - len(elite)):
                individuoX = selecaoAleatoria(populacao)
                individuoY = selecaoAleatoria(populacao)
                filho = reproduzir(individuoX.copy(),individuoY.copy())
                if random.random() < probMutacao:
                    filho[0] = mutacao(filho[0][:])
                    filho[1] = self.calcularDistancia(filho[0])
                novaPopulacao.append(filho)

            populacao = novaPopulacao[:]
            populacao.extend(elite)
            melhorIndividuoAux = selecionarMelhorIndividuo(populacao)
            elite = selecionarElite(populacao)

            if(melhorIndividuoAux[1] < melhorIndividuo[1]):
                melhorIndividuo = melhorIndividuoAux
    
        tempoFinal = time.time()
        self.tempoConclucao = tempoFinal - self.tempoIncial
        self.resultados = melhorIndividuo
        self.imprimirResultados()

#========================================Tempera simulada==================================================



    def temperaSimulada(self, 
                        tempInicial:int = 4000,
                        tempFinal:int = 0.05,
                        taxaResfriamento:float = 0.999):
        self.tempoIncial = time.time()
        print("EXECUTANDO TEMPERA SIMULADA")
        def gerarCaminho():
            n = len(self.matriz)
            caminhoInicial = list(range(n))
            random.shuffle(caminhoInicial)
            return caminhoInicial

        def pertubacaoResultado(caminho):
            nova_caminho = caminho[:]
            c1, c2 = sorted(random.sample(range(len(caminho)), 2))
            nova_caminho[c1:c2] = reversed(nova_caminho[c1:c2])
            return nova_caminho

       
        solucaoAtual = gerarCaminho()
        distSolucaoAtual = self.calcularDistancia(solucaoAtual)
        melhorSolucao = solucaoAtual[:]
        melhorDistancia = distSolucaoAtual
        
        T = tempInicial
        cont = 0
        while T > tempFinal:
            novaSolucao = pertubacaoResultado(solucaoAtual)
            distNovaSolucao = self.calcularDistancia(novaSolucao)
            if distNovaSolucao < distSolucaoAtual:
                solucaoAtual = novaSolucao
                distSolucaoAtual = distNovaSolucao
                if distNovaSolucao < melhorDistancia:
                    melhorSolucao = novaSolucao[:]
                    melhorDistancia = distNovaSolucao
            else:
                deltaE = distNovaSolucao - distSolucaoAtual
                probabilidade = math.exp(-deltaE / T)
                if random.random() < probabilidade:
                    solucaoAtual = novaSolucao
                    distSolucaoAtual = distNovaSolucao
            T *= taxaResfriamento

        tempoFinal = time.time()
        self.tempoConclucao = tempoFinal - self.tempoIncial
        self.resultados = [melhorSolucao,melhorDistancia]
        self.imprimirResultados()

#==========================================Busca tabu=======================================================


    def buscaTabu(self,
                  tabuListMax:int = 40,
                  maxInteracoes:int = 12000,
                  numMaxInterSemMelhora = 500,
                  numVizinhos = 300
                  ):
        self.tempoIncial = time.time()
        print("EXECUTANDO BUSCA TABU")

        def pertubacaoResultado(caminho):
            nova_caminho = caminho[:]
            c1, c2 = sorted(random.sample(range(len(caminho)), 2))
            nova_caminho[c1:c2] = reversed(nova_caminho[c1:c2])
            return nova_caminho,self.calcularDistancia(nova_caminho)

        
        def gerarCaminho():
            n = len(self.matriz)
            caminhoInicial = []
            caminhoInicial.extend(i for i in range(0,n))
            random.shuffle(caminhoInicial)
            return caminhoInicial, self.calcularDistancia(caminhoInicial)
        
        def trocarPosicoes(caminho:list):
            vizinhos = []
            for _ in range(0,numVizinhos):
                no1 = 0
                no2 = 0
                while no1 == no2:
                    no1 = random.randint(0, len(caminho[0])-1)
                    no2 = random.randint(0, len(caminho[0])-1)

                    if no1 > no2:
                        troca = no1
                        no1 = no2
                        no2 = troca

                    tmp = caminho[0][no1:no2]
                    tmp_state = caminho[0][:no1] + tmp[::-1] + caminho[0][no2:]

                    distValor = self.calcularDistancia(tmp_state)
                    if(((distValor - caminho[1])/caminho[1]) * 100 <= 0.5):
                        if [tmp_state,distValor] not in vizinhos:
                            vizinhos.append([tmp_state,distValor])

            return vizinhos

        def melhorIndividuo(populacao:list[list[int]],listTabu: list[list[int]],melhorEncontrada,melhorAtual):
            melhorGeral = min(populacao, key=lambda x: x[1])

            if(melhorGeral in listaTabu and (melhorEncontrada[1] - melhorGeral[1]) >= melhorEncontrada[1] * 0.2 or (melhorAtual[1] - melhorGeral[1]) >= melhorAtual[1] * 0.2):
                return melhorGeral
            
            listaFiltrada = []
            listaFiltrada = [individuo for individuo in populacao if individuo not in listTabu]
            if(listaFiltrada == []):
                return -1
            melhor = min(listaFiltrada, key=lambda x: x[1])
            return melhor
                
        
        
        solucaoAtual = gerarCaminho()
        listaTabu = []
        
        melhorSolucao = solucaoAtual
        cont = 0
        while(maxInteracoes > 0):
            if(random.random() < 0.2):
                solucaoAtual = pertubacaoResultado(solucaoAtual[0])
                if(solucaoAtual in listaTabu):
                    print("aqui")

            vizinhos = trocarPosicoes(solucaoAtual)
            melhorVizinho = melhorIndividuo(vizinhos,listaTabu,melhorSolucao,solucaoAtual)
            
            if(melhorVizinho == -1):
                break
            
            solucaoAtual = melhorVizinho

            if(solucaoAtual not in listaTabu):
                listaTabu.append(solucaoAtual.copy())

            if(len(listaTabu) > tabuListMax):
                listaTabu.pop(0)
            
            if(melhorSolucao[1] > solucaoAtual[1]):
                cont = 0
                melhorSolucao = solucaoAtual     
            else:
                cont += 1
                if(cont == numMaxInterSemMelhora):
                    break
            maxInteracoes -= 1
        tempoFinal = time.time()
        self.tempoConclucao = tempoFinal - self.tempoIncial
        self.resultados = melhorSolucao
        self.imprimirResultados()