import random
import math
import time
class Solver:    
    def __init__(self,matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.resultados  = None
        self.tempoConclucao = 0
        self.tempoIncial = time.time()

  
    def imprimirResultados(self):
        print("CAMINHO ENCONTRADO: ",self.resultados[0])
        print("CUSTO: ",self.resultados[1])
        print("TEMPO: ",self.tempoConclucao)


    def subidaDeEncosta(self):
        self.tempoIncial = time.time()
        print("EXECUTANDO SUBIDA DE ENCOSTA")
        def calcularDistancia(caminho:list[int]):
            distancaiTotal = 0
            for i in range(1,len(caminho)):
                distancaiTotal += self.matriz[caminho[i-1]][caminho[i]]
            distancaiTotal += self.matriz[caminho[-1]][caminho[0]]    
            return distancaiTotal
        
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
        distanciaAtual = calcularDistancia(caminhoAtual)
        cont = 0
        while True:
            cont += 1
            caminhoAtualAux = caminhoAtual.copy()
            vizinhos = trocarPosicoes(caminhoAtual)
            for vizinho in vizinhos:
                distanciaVizinhoAtual = calcularDistancia(vizinho)
                if distanciaVizinhoAtual < distanciaAtual:
                    distanciaAtual = distanciaVizinhoAtual
                    caminhoAtual = vizinho.copy()

            if(caminhoAtual == caminhoAtualAux):
                break

        tempoFinal = time.time()
        self.tempoConclucao = tempoFinal - self.tempoIncial
        self.resultados = [caminhoAtual,distanciaAtual]
        print("NUMERO PASSOS ",cont)

    def algoritmoGenetico(self,
                        probMutacao:float = 0.2,
                        tamPopulacao:int = 120,
                        numMaxGeracoes:int = 2000,
                        numNovosIndividuos:int = 120 ):
        self.tempoIncial = time.time()
        print("EXECUTANDO ALGORITIMO GENETICO")
        def funcaoAdptacao(caminho:list[int]):
            distancaiTotal = 0
            for i in range(1,len(caminho)):
                distancaiTotal += self.matriz[caminho[i-1]][caminho[i]]
            distancaiTotal += self.matriz[caminho[-1]][caminho[0]]
            return distancaiTotal
        
        def gerarPopulacao(tamPopulacao:int):
            populacaoInicial = []
            individuo = []
            n = len(self.matriz)
            for _ in range(0,tamPopulacao):
                individuo = []
                individuo.extend(i for i in range(0,n))
                random.shuffle(individuo)

                dist = funcaoAdptacao(individuo)
                populacaoInicial.append([individuo,dist])

                individuo[:] = reversed(individuo[:])

                dist = funcaoAdptacao(individuo)
                populacaoInicial.append([individuo,dist])
            return populacaoInicial
        
        def selecaoAleatoria(populacao: list[list[int],int]):
            selecionados = random.sample(populacao,k=10)
            melhorEscolha = min(selecionados, key=lambda x: x[1])
            return melhorEscolha
        
        def reproduzir(individuoX: list[int],individuoY:list[int]):
            n = len(individuoX)
            novoIndividuo = [None] * n
            c1, c2 = sorted(random.sample(range(n), 2))
            novoIndividuo[c1:c2] = individuoX[c1:c2]

            if(individuoX == individuoY):    
                for i in range(0,n):
                    if(novoIndividuo[i] == None):
                        for gene in individuoY:
                            if(gene not in novoIndividuo):
                                novoIndividuo[i] = gene
                                individuoY.remove(gene)
                                break
            else:
                for i in range(n-1,-1,-1):
                    if(novoIndividuo[i] == None):
                        for gene in individuoY:
                            if(gene not in novoIndividuo):
                                novoIndividuo[i] = gene
                                individuoY.remove(gene)
                                break
            dist = funcaoAdptacao(novoIndividuo)            
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
                filho = reproduzir(individuoX[0][:],individuoY[0][:])
                if random.random() < probMutacao:
                    filho[0] = mutacao(filho[0][:])
                    filho[1] = funcaoAdptacao(filho[0])
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

    def temperaSimulada(self, 
                        tempInicial:int = 4000,
                        tempFinal:int = 1,
                        taxaResfriamento:float = 0.999):
        self.tempoIncial = time.time()
        print("EXECUTANDO TEMPERA SIMULADA")
        def gerarCaminho():
            n = len(self.matriz)
            caminhoInicial = list(range(n))
            random.shuffle(caminhoInicial)
            return caminhoInicial

        def calcularDistancia(caminho):
            distanciaTotal = 0
            for i in range(1, len(caminho)):
                distanciaTotal += self.matriz[caminho[i-1]][caminho[i]]
            distanciaTotal += self.matriz[caminho[-1]][caminho[0]]
            return distanciaTotal

        def pertubacaoResultado(caminho):
            nova_caminho = caminho[:]
            c1, c2 = sorted(random.sample(range(len(caminho)), 2))
            nova_caminho[c1:c2] = reversed(nova_caminho[c1:c2])
            return nova_caminho

       
        solucaoAtual = gerarCaminho()
        distSolucaoAtual = calcularDistancia(solucaoAtual)
        melhorSolucao = solucaoAtual[:]
        melhorDistancia = distSolucaoAtual
        
        T = tempInicial

        while T > tempFinal:
            novaSolucao = pertubacaoResultado(solucaoAtual)
            distNovaSolucao = calcularDistancia(novaSolucao)
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

    def buscaTabu(self,
                  tabuListMax:int = 100,
                  maxInteracoes:int = 1000
                  ):
        self.tempoIncial = time.time()
        print("EXECUTANDO BUSCA TABU")
        def calcularDistancia(caminho:list[int]):
            distancaiTotal = 0
            for i in range(1,len(caminho)):
                distancaiTotal += self.matriz[caminho[i-1]][caminho[i]]
            distancaiTotal += self.matriz[caminho[-1]][caminho[0]]    
            return distancaiTotal
        
        def gerarCaminho():
            n = len(self.matriz)
            caminhoInicial = []
            caminhoInicial.extend(i for i in range(0,n))
            random.shuffle(caminhoInicial)

            return caminhoInicial, calcularDistancia(caminhoInicial)
        
        def trocarPosicoes(caminho:list):
            caminhosPossiveis = []
            for i in range(0,len(caminho[0])):
                for j in range(i,len(caminho[0])):
                    caminhoAux = caminho[0].copy()
                    if(i != j):
                        aux = caminhoAux[i]
                        caminhoAux[i] = caminhoAux[j]
                        caminhoAux[j] = aux
                        caminhosPossiveis.append([caminhoAux,calcularDistancia(caminhoAux)])
            return caminhosPossiveis
        
        def melhorIndividuo(populacao:list[list[int]],listTabu: list[list[int]]):
            listaFiltrada = []
            listaFiltrada = [individuo for individuo in populacao if individuo not in listTabu]
            if(listaFiltrada == []):
                return -1
            melhor = min(listaFiltrada, key=lambda x: x[1])
            return melhor
                
        
        
        solucaoAtual = gerarCaminho()
        listaTabu = []
        
        melhorSolucao = solucaoAtual

        for _ in range(0,maxInteracoes):
            vizinhos = trocarPosicoes(solucaoAtual)
            melhorVizinho = None
            melhorVizinho = melhorIndividuo(vizinhos,listaTabu)
            if(melhorVizinho == -1):
                break
            solucaoAtual = melhorVizinho
            listaTabu.append(solucaoAtual.copy())
            if(len(listaTabu) > tabuListMax):
                listaTabu.pop(0)
            
            if(melhorSolucao[1] > solucaoAtual[1]):
                melhorSolucao = solucaoAtual     

        tempoFinal = time.time()
        self.tempoConclucao = tempoFinal - self.tempoIncial
        self.resultados = melhorSolucao