from random import choice
class slidingPuzzle:
    def __init__(self,tabuleiroPai: 'slidingPuzzle' = None):
        self.tabuleiroPai = tabuleiroPai
        
    def mostrarTabIncial(self):  
        max_lengths = [max(len(str(element)) for element in row) for row in self.tabuleiro]
        matrix_str = ""
        for row in self.tabuleiro:
            matrix_str += "|"
            for i, element in enumerate(row):
                matrix_str += f" {element:>{max_lengths[i]}} |"
            matrix_str += "\n"
        return matrix_str

    def mostrarTabObjetivo(self):  
        max_lengths = [max(len(str(element)) for element in row) for row in self.tabuleiroObjetivo]
        matrix_str = ""
        for row in self.tabuleiroObjetivo:
            matrix_str += "|"
            for i, element in enumerate(row):
                matrix_str += f" {element:>{max_lengths[i]}} |"
            matrix_str += "\n"
        return matrix_str
    
    def __call__(self):
        return self.tabuleiro
    
    def __lt__(self,other):
       return None
    
    def getTabuleiroPai(self):
        return self.tabuleiroPai

    def getPosVazio(self):
        return self.posVazio
    
    #Busca a posição do zero no tabuleiro 
    def buscarPosZero(self):
        for i in range(self.n):
            if(0 in self.tabuleiro[i]):
                j = self.tabuleiro[i].index(0)
                self.posVazio = (i,j)
                break
    
    def getTabObjeitivo(self):
        return self.tabuleiroObjetivo

    def iniciarTabuleiro(self, n:int,tabuleiro: list[list[int]] = '',tabuleiroObjetivo: list[list[int]] = ''):
        if(tabuleiro == ''):
            self.n = n
        else:
            n = self.n = len(tabuleiro)
            
        if(tabuleiro == ''):
            self.tabuleiro:list[list[int]] = [[j + i * n + 1 for j in range(n)] for i in range(n)]
            self.tabuleiro[self.n - 1][self.n - 1] = 0
            self.posVazio = (self.n - 1,self.n - 1)
        else:
            self.tabuleiro = [linha[:] for linha in tabuleiro]
            self.buscarPosZero() 

        if(tabuleiroObjetivo == ''):
            self.tabuleiroObjetivo:list[list[int]] = [[j + i * n + 1 for j in range(n)] for i in range(n)]
            self.tabuleiroObjetivo[self.n - 1][self.n - 1] = 0
        else:
            self.tabuleiroObjetivo = [linha[:] for linha in tabuleiroObjetivo]

    #Função utilizada para embaralhar o tabuleiro ate um limite minimo de peças peças corretas dentro do tabuleiro
    def randomizar(self):
        while(self.calcularNumPosCorretas() > (self.n*self.n)*0.30):
            #Movimento escolhidos aleatoriamente e executados 
            execute = choice([self.moverCima,self.moverBaixo,self.moverDireita,self.moverEsquerda])
            execute()

    #Função auxiliar para criar uma copia do tabuleiro e realiza uma movimentação, criando um novo tabuleiro com base em outro
    def copyPuzzle(self,novoTabuleiro:list[list[int]],move:str = ''):
        self.tabuleiro = [linha[:] for linha in novoTabuleiro]
        self.buscarPosZero()
        if(move != ''):
            if(move == 'UP'):
                self.moverCima()
            elif(move == 'DOWN'):
                self.moverBaixo()
            elif(move == 'LEFT'):
                self.moverEsquerda()
            elif(move == 'RIGTH'):
                self.moverDireita()
        

    def calcularNumPosCorretas(self) -> int:
        cont = 0
        for i in range(self.n):
            for j in range(self.n):
                if(self.tabuleiro[i][j] == self.tabuleiroObjetivo[i][j]):
                    cont += 1
        return cont

    def inverterJunstarTabuleiros(self,novaPontaTAbuleiro:list[list[int]] = ''):
        noAtual = self
        noAnterior = None

        while noAtual != None:
            proximoNo = noAtual.getTabuleiroPai()
            noAtual.tabuleiroPai = noAnterior
            noAnterior = noAtual
            noAtual = proximoNo
        if(novaPontaTAbuleiro != ''):
            self.tabuleiroPai = novaPontaTAbuleiro
        return noAnterior

    def moverCima(self):
        if(self.posVazio[0] - 1 == -1):
            return False
        
        valor = self.tabuleiro[self.posVazio[0] - 1][self.posVazio[1]]
        self.tabuleiro[self.posVazio[0] - 1][self.posVazio[1]] = 0
        self.tabuleiro[self.posVazio[0]][self.posVazio[1]] = valor
        self.posVazio = (self.posVazio[0] - 1,self.posVazio[1])

    def moverBaixo(self):
        if(self.posVazio[0] + 1 == self.n):
            return False
        
        valor = self.tabuleiro[self.posVazio[0] + 1][self.posVazio[1]]
        self.tabuleiro[self.posVazio[0] + 1][self.posVazio[1]] = 0
        self.tabuleiro[self.posVazio[0]][self.posVazio[1]] = valor
        self.posVazio = (self.posVazio[0] + 1,self.posVazio[1])

    def moverEsquerda(self):
        if(self.posVazio[1] - 1 == -1):
            return False
        
        valor = self.tabuleiro[self.posVazio[0]][self.posVazio[1] - 1]
        self.tabuleiro[self.posVazio[0]][self.posVazio[1] - 1] = 0
        self.tabuleiro[self.posVazio[0]][self.posVazio[1]] = valor
        self.posVazio = (self.posVazio[0],self.posVazio[1] - 1)

    def moverDireita(self):
        if(self.posVazio[1] + 1 == self.n):
            return False
        
        valor = self.tabuleiro[self.posVazio[0]][self.posVazio[1] + 1]
        self.tabuleiro[self.posVazio[0]][self.posVazio[1] + 1] = 0
        self.tabuleiro[self.posVazio[0]][self.posVazio[1]] = valor
        self.posVazio = (self.posVazio[0],self.posVazio[1] + 1)
    
    def veirfiqueMoveCima(self):
        if(self.posVazio[0] - 1 == -1):
            return False
        return True
    
    def verifiqueMoveBaixo(self):
        if(self.posVazio[0] + 1 == self.n):
            return False
        return True
    
    def verifiqueMoveEsqueda(self):
        if(self.posVazio[1] - 1 == -1):
            return False
        return True    
    
    def verifiqueMoveDireira(self):
        if(self.posVazio[1] + 1 == self.n):
            return False
        return True

    #Função utilizada para verificar e realizar todas as possiveis jogadas para o tabuleiro, retornar uma lista de objetos slidingPuzzle
    def possibilidades(self):
        tabuleiroPai = self
        novosTabuleiros = []
        if(self.veirfiqueMoveCima() == True):
            newTabuleiro = slidingPuzzle(tabuleiroPai)
            newTabuleiro.iniciarTabuleiro(self.n)
            newTabuleiro.copyPuzzle(self.tabuleiro,'UP')
            
            novosTabuleiros.append(newTabuleiro)

        if(self.verifiqueMoveBaixo() == True):
            newTabuleiro = slidingPuzzle(tabuleiroPai)
            newTabuleiro.iniciarTabuleiro(self.n)
            newTabuleiro.copyPuzzle(self.tabuleiro,'DOWN')
            
            novosTabuleiros.append(newTabuleiro)

        if(self.verifiqueMoveEsqueda() == True):
            newTabuleiro = slidingPuzzle(tabuleiroPai)
            newTabuleiro.iniciarTabuleiro(self.n)
            newTabuleiro.copyPuzzle(self.tabuleiro,'LEFT')
            
            novosTabuleiros.append(newTabuleiro)
            
        if(self.verifiqueMoveDireira() == True):
            newTabuleiro = slidingPuzzle(tabuleiroPai)
            newTabuleiro.iniciarTabuleiro(self.n)
            newTabuleiro.copyPuzzle(self.tabuleiro,'RIGTH')
            
            novosTabuleiros.append(newTabuleiro)

        return novosTabuleiros
    
    def solucao(self, imprimirResultado = False):
        caminho = self
        caminho = caminho.inverterJunstarTabuleiros()
        passos = 0
        while(True):
            if(imprimirResultado == True):
                print("--------PASSO N° {}--------".format(passos))
                print(caminho.mostrarTabIncial())
            if(caminho.getTabuleiroPai() != None):
                caminho = caminho.getTabuleiroPai()
                passos += 1
            else:
                break
        print("NUMERO DE PASSOS TOTAIS: ",passos)
        return passos