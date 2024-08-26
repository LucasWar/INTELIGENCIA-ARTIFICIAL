from typing import List,Callable
from queue import PriorityQueue, Queue
from slidingPuzzle import slidingPuzzle
import time
class Solver:
    
    @staticmethod
    def AStar(tabInicial:slidingPuzzle, heuristc: Callable[[List[List[int]], List[List[int]]], int]):
        inicio = time.time()
        print("ALGORITMO UTILIZADO A*")
        #Atribuição para o tabuleiro considerado estado final do jogo.
        tabObjetivo = tabInicial.getTabObjeitivo()

        #Inicialização das variaveis para calculo da função utilizada no A*.
        gScore = {}
        fScore = {}

        #Criação de uma lista fechada para auxiliar nas ecolha de quais nos seram expadidos
        listFechada = set()

        #Inicialização do estado incial do tabuleiro.
        estadoIncial = str(tabInicial())

        #Primeiras entradas de g_score, 0 pois não foi realizado nenhum passo, f_score é o g_score do estado em questão mais o calculo da heuristica
        gScore[estadoIncial] = 0
        fScore[estadoIncial] = gScore[estadoIncial] + heuristc(tabInicial(),tabObjetivo)

        #Criação da fila de prioridade 
        fila = PriorityQueue()

        #Criação do item que será inserido na fila
        item = (fScore[estadoIncial],
                heuristc(tabInicial(),tabObjetivo),
                tabInicial)
        
        #Item adicionado a fila de prioridade, a fila sera organizada conforme os menores f_score de cada item
        fila.put(item)

        #Variaveis auxilares para coleta de dados
        nosExpandidos = 0

        numRamificacao = 0

        tamanhoMaxFila = 0

        while not fila.empty():
            tamanhoMaxFila = max(tamanhoMaxFila, fila.qsize())
            novosTabuleiros = []
            tabuleiro = fila.get()
            atualTabuleiro = tabuleiro[2]

            if(atualTabuleiro() == tabObjetivo):
                fim = time.time()
                return atualTabuleiro,tamanhoMaxFila,nosExpandidos,(numRamificacao/nosExpandidos) if nosExpandidos > 0 else 0,fim - inicio
                
            #Apenas tabuleiros que ainda não foram expadidos podem passar e verificar as possiveis novas jogadas
            if(str(atualTabuleiro()) not in listFechada):
                #Todo novo tabuleiro expadido é adicionado a lista fechada
                listFechada.add(str(atualTabuleiro()))

                #Atribuição de todas as possiveis jogadas para o atual tabuleiro analisado
                novosTabuleiros = atualTabuleiro.possibilidades(atualTabuleiro)

                if novosTabuleiros:
                    nosExpandidos += 1
                
                for novoTabuleiro in novosTabuleiros:
                    h = heuristc(novoTabuleiro(),tabObjetivo) 

                    novo_g_score = gScore[str(atualTabuleiro())] + 1
                    novo_f_Score = novo_g_score + h

                    #Verifica se novo tabuleiro não ja foi analisado ou se seu novo g_score é menor que o ja existente 
                    if(str(novoTabuleiro()) not in gScore or novo_g_score < gScore[str(novoTabuleiro())]):
                        fScore[str(novoTabuleiro())] = novo_f_Score
                        gScore[str(novoTabuleiro())] = novo_g_score
                        item = (fScore[str(novoTabuleiro())], 
                                h,
                                novoTabuleiro)
                        fila.put(item)
                        numRamificacao += 1
                        
    @staticmethod
    def bfs(estdadoAtual:slidingPuzzle):
        inicio = time.time()
        print("ALGORITMO UTILIZADO BFS")
        tabObjetivo = estdadoAtual.getTabObjeitivo()
        #Criação da fila FIFO
        fila = Queue()
        
        #Item a ser adicionado na fila, primeira etrada altura da arvore naquele momento, segunda entrada objeto sldingPuzzle
        item = estdadoAtual

        #Adiciona item a fila
        fila.put(item)
        
        #Criação de uma lista fechada para auxiliar nas ecolha de quais nos seram expadidos
        listaFechada = set()

        #Variaveis auxilares para coleta de dados
        nosExpandidos = 0

        numRamificacao = 0

        tamanhoMaxFila = 0

        while(not fila.empty()):
            tamanhoMaxFila = max(tamanhoMaxFila,fila.qsize())

            atualTabuleiro = fila.get()

            novosTabuleiros = []

            if(atualTabuleiro() == tabObjetivo):
                fim = time.time()
                return atualTabuleiro,tamanhoMaxFila,nosExpandidos,(numRamificacao/nosExpandidos) if nosExpandidos > 0 else 0, fim - inicio
            if(str(atualTabuleiro()) not in listaFechada):

                #Adiciona todo tabuleiro expandido a lista fechada para que não seja expandido novamente 
                listaFechada.add(str(atualTabuleiro()))

                #Atribuição de todas as possiveis jogadas para o atual tabuleiro analisado
                novosTabuleiros = atualTabuleiro.possibilidades(atualTabuleiro)

                nosExpandidos += 1
                for novoTabuleiro in novosTabuleiros:
                    if(novoTabuleiro() != novoTabuleiro.getTabuleiroPai()):
                        if(str(novoTabuleiro()) not in listaFechada):
                            item = novoTabuleiro
                            fila.put(item)
                            numRamificacao += 1

    @staticmethod
    def bidirecionalAstar(tabInicial:slidingPuzzle,heuristc: Callable[[List[List[int]], List[List[int]]], int]):  
        #Função para realizar a analise dos tabuleiros de cada fila, seja o tabuleiro que vai ate o estado destinho como o caminho inverso.      
        def analisarTabuliero(objAtual, objObjetivo, gScore, fScore, fila, nosExpandidos, numRamificacao):
                novosTabuleiros = objAtual.possibilidades(objAtual)
                if novosTabuleiros:
                    nosExpandidos += 1

                for novoTabuleiro in novosTabuleiros:
                    h = heuristc(novoTabuleiro(), objObjetivo())

                    novo_g_score = gScore[str(objAtual())][0] + 1
                    novo_f_Score = novo_g_score + h

                    if str(novoTabuleiro()) not in gScore or novo_g_score < gScore[str(novoTabuleiro())][0]:
                        fScore[str(novoTabuleiro())] = novo_f_Score
                        gScore[str(novoTabuleiro())] = (novo_g_score, novoTabuleiro)
                        item = (fScore[str(novoTabuleiro())], h, novoTabuleiro)
                        fila.put(item)
                        numRamificacao += 1

                return nosExpandidos, numRamificacao 
        tabObjetivo = slidingPuzzle()
        tabObjetivo.iniciarTabuleiro(len(tabInicial()),tabInicial.getTabObjeitivo())
        inicio = time.time()
        print("ALGORITMO UTILIZADO A* BIDIRECIONAL") 
        
        gScoreOrigem = {}
        fScoreOrigem = {}

        gScoreObjetivo = {}
        fScoreObjetivo = {}

        estadoInicio = str(tabInicial())
        estadoObjetivo = str(tabObjetivo())

        gScoreOrigem[estadoInicio] = (0,tabInicial)
        fScoreOrigem[estadoInicio] = gScoreOrigem[estadoInicio][0] + heuristc(tabInicial(),tabObjetivo())

        gScoreObjetivo[estadoObjetivo] = (0,tabObjetivo)
        fScoreObjetivo[estadoObjetivo] = gScoreObjetivo[estadoObjetivo][0] + heuristc(tabObjetivo(),tabInicial())

        #Criação de duas filas de prioridade, ja que agora a busca será feita de forma bidirecional
        filaOrigem = PriorityQueue()
        item = (fScoreOrigem[estadoInicio],
                heuristc(tabInicial(),tabObjetivo()),
                tabInicial)
        filaOrigem.put(item)

        filaObjetivo = PriorityQueue()
        item = (fScoreObjetivo[estadoObjetivo],
                heuristc(tabObjetivo(),tabInicial()),
                tabObjetivo)
        filaObjetivo.put(item)

        #Variaveis auxilares para coleta de dados
        tamanhoMaxOrigem = 0
        tamanhoMaxDestino = 0
        nosExpandidos = 0
        numRamificacao = 0

        while not filaOrigem.empty() or not filaObjetivo.empty():
            tamanhoMaxDestino = max(tamanhoMaxDestino, filaObjetivo.qsize())
            tamanhoMaxOrigem = max(tamanhoMaxOrigem, filaOrigem.qsize())
           
            tabuleiroOrigem = filaOrigem.get()
            tabuleiroObjetivo = filaObjetivo.get()

            #Verifica se o tabuleiro origem ja se encontra na lista de gScoreObjetivo, se sim, siguinifica que ambos ja se encontraram e temos o caminho de ida completo ate o objetivo
            if(str(tabuleiroOrigem[2]()) in gScoreObjetivo):   
                
                caminhoObjetivo = gScoreObjetivo[str(tabuleiroOrigem[2]())][1].getTabuleiroPai()
                caminhoOrigem = tabuleiroOrigem[2]
                #Verificação para ver se o caminho foi curto o suficiente para não precisar da outra parte do caminho 
                if(caminhoObjetivo != None):
                    #função para retornar o camiho completo, tanto invertendo o caminho do objetivo ate o estado incial, como juntar os dois caminhos encontrados
                    caminhoObjetivo = caminhoObjetivo.inverterJunstarTabuleiros(caminhoOrigem)
                else:
                    caminhoObjetivo = caminhoOrigem
                
                fim = time.time()
                return caminhoObjetivo,(tamanhoMaxDestino + tamanhoMaxOrigem),nosExpandidos,(numRamificacao/nosExpandidos) if nosExpandidos > 0 else 0, fim - inicio
            
            elif(str(tabuleiroObjetivo[2]()) in gScoreOrigem):  
                caminhoObjetivo = tabuleiroObjetivo[2] 
                caminhoOrigem = gScoreOrigem[str(tabuleiroObjetivo[2]())][1].getTabuleiroPai()

                if(caminhoObjetivo != None):
                    caminhoObjetivo = caminhoObjetivo.inverterJunstarTabuleiros(caminhoOrigem)
                else:
                    caminhoObjetivo = caminhoOrigem
                fim = time.time()
                return caminhoObjetivo,(tamanhoMaxDestino + tamanhoMaxOrigem),nosExpandidos,(numRamificacao/nosExpandidos),fim - inicio

            objTabuleiroObjetivo = tabuleiroObjetivo[2]
            objTabuleiroOrigem = tabuleiroOrigem[2]

            #Chamadas da função para analse de cada tabuleiro de cada fila de prioridade(destino e origem)
            nosExpandidos, numRamificacao = analisarTabuliero(objTabuleiroOrigem, objTabuleiroObjetivo, gScoreOrigem, fScoreOrigem, filaOrigem, nosExpandidos, numRamificacao)
            nosExpandidos, numRamificacao = analisarTabuliero(objTabuleiroObjetivo, objTabuleiroOrigem, gScoreObjetivo, fScoreObjetivo, filaObjetivo, nosExpandidos, numRamificacao)
    
    @staticmethod
    def buscaProfInterativo(tabInical):
        inicio = time.time()
        print("ALGORITMO UTILIZADO DFS")
        limite = 0

        #Variaveis auxilares para coleta de dados
        nosExpandidos = 0
        ramificacoes = 0
        tamMaxFila = 0
        
        #Chamada infinita da função DFS para aprofundar ate um limite X 
        while(True):
            resultado, nosExpandidos, ramificacoes, maxPilhaAtual = Solver.dfs(tabInical, limite, nosExpandidos, ramificacoes, 0)
            tamMaxFila = max(tamMaxFila, maxPilhaAtual)
            if resultado is not False:
                fim = time.time()
                return resultado,tamMaxFila, nosExpandidos, ramificacoes / nosExpandidos if nosExpandidos > 0 else 0, fim - inicio
            else:
                limite += 1

    @staticmethod
    def dfs(estadoInicial, limite=0, nosExpandidos=0, ramificacoes=0, profundidadeAtual=0):
        resultado = False
        
        tabueiroFinal = estadoInicial.getTabObjeitivo()

        # Contabilizando a profundidade atual
        tamMaxFila = profundidadeAtual + 1  

        if estadoInicial() == tabueiroFinal:
            return estadoInicial, nosExpandidos, ramificacoes, tamMaxFila

        if limite == 0:
            return False, nosExpandidos, ramificacoes, tamMaxFila

        if limite > 0:
            novosTabuleiros = estadoInicial.possibilidades(estadoInicial)  
            nosExpandidos += 1               
            ramificacoes += len(novosTabuleiros)
            for novoTabuleiro in novosTabuleiros:
                if not Solver.ciclos(novoTabuleiro):
                    resultado, nosExpandidos, ramificacoes, maxPilhaFilho = Solver.dfs(novoTabuleiro, limite - 1, nosExpandidos, ramificacoes, profundidadeAtual + 1)
                    tamMaxFila = max(tamMaxFila, maxPilhaFilho)
                    if resultado:
                        return resultado, nosExpandidos, ramificacoes, tamMaxFila

        return False, nosExpandidos, ramificacoes, tamMaxFila

    @staticmethod
    def ciclos(node):
        state = node()
        parent = node.getTabuleiroPai()
        while parent is not None:
            if state == parent():
                return True
            parent = parent.getTabuleiroPai()
        return False