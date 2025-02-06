from copy import deepcopy
import math
import time

def number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
class Node():
    def __init__(self):
        self.childs = []
        self.colu = None
        self.value = None
        self.clas= None
        self.ind=None
        self.caunter=None

class Tree():
    def __init__(self,colu,x,unique):
        self.node = Node()
        self.col = colu
        self.x= x
        self.unique=unique

    def buildtree(self,x,dis,ndis,node):                    #dataset, valores, numerovalres, node
        if node is None:
            node = self.node
            
        clas = unique(x,-1)             #ve valores unicos da ultima coluna

        if len(clas)==1:
            node.clas = clas[0]
            node.caunter= len(x)
            node.ind= -1

        elif ndis==0:
            node.clas,node.caunter = self.maiorclas(x,clas)
            node.ind=-1

        else:
            i = self.matributo(x,dis)
            node.colu = self.col[i]
            node.ind=i
            coluna = []
            for w in x:
                coluna.append(w[i])
            todosatri= self.unique[i]
            for val in todosatri:
                split = self.split(x,i,val)
                nod =  Node()
                node.childs.append(nod)
                if(len(split) ==0):
                    nod.clas,nod.caunter = self.maiorclas(x,clas)
                    nod.caunter=0
                    nod.ind=-1
                    nod.value= val
                else:
                    nod.value = val
                    dist2 = deepcopy(dis)
                    dist2[i] = False
                    self.buildtree(split,dist2,ndis-1,nod)
    
    def maiorclas(self,x,list):
        max=0
        clas=""
        coluna = []
        for w in x:
            coluna.append(w[-1])
        for i in list:
            number =self.caunt(coluna,i)
            if number > max:
                max = number
                clas = i
        return clas,max

    def matributo(self,x,dis):
        h = self.entropy(x)
        max = 0
        mi=0
        numero = len(x[:])
        colunas =[]
        for i in range(len(dis)):
            if dis[i]:
                colunas.append(i)
        for i in colunas:
            val = self.unique[i]
            entroatri = 0
            for j in val:
                split = self.split(x,i,j)
                entroatri += (float)(self.entropy(split))*(float)(len(split)/numero)
            if(h-entroatri>max):
                max = h-entroatri
                mi =i
        if max ==0:
            mi =colunas[0]
        return mi
    
    def split(self,x,col,val):
        split=[]
        for i in x:
            if i[col]== val:
                split.append(i)
        return split

    def entropy(self,x):
        y=[]
        for i in x:
            y.append(i[-1])
        labels = unique(x,-1)
        entropy = 0
        for cls in labels:
            p_cls = self.caunt(y,cls) / len(y)
            entropy += -p_cls * math.log2(p_cls)
        return entropy
    
    def caunt(self,y,clas):
        count =0
        for i in y:
            if i ==clas:
                count = count+1
        return count

    def printtree(self,node,indent,c):
        if node is None:
            node =self.node
        print((indent)*c + '<'+node.colu +'>')
        for i in node.childs:
            if( len(i.childs) ==0):
                print(indent*(c+1) +str(i.value)+ ':[' + str(i.clas) + "] (" + str(i.caunter) + ')')
            else:
                print(indent*(c+1)+ str(i.value) + ':')
                self.printtree(i,indent,c+2)
    
    def predict(self,node,exemplo):
        if node is None:
            node =self.node
        if(node.clas is not None):
            return node.clas
        for i in node.childs:
            if number(exemplo[node.ind]):
                exemplo[node.ind] = str(round(float(exemplo[node.ind])))
            if exemplo[node.ind] == i.value:
                return self.predict(i,exemplo)
        x,y = self.maiorclas(self.x,unique(self.x,-1))
        return x
        
def unique(x,col):#para ve num determinado atributo,quais os valores distintos que ha
    uni =set()
    for i in x:
        uni.add(i[col])
    return list(uni)


print("escolhe o que quer fazer: 1-arvore de pesquisa, 2-jogar connect 4")
modo = int(input())
if modo== 1:
    print("ponha o nome do ficheiro com os dados")
    s= input()
    file = open(s)
    dataset = file.read().splitlines()              #cria lista em que cada elemento é uma linha
    c=0
    colu=[]                                         #lista dos nomes das colunas
    ds =[]                                          #çista dos valores das colunas
    for i in dataset:
        if c ==0:
            colu = i.split(',')                     #adiciona os nomes das colunas a lista
            c =c+1
        else:
            ds.append(i.split(','))                 #adiciona os valores das colunas a lista
            c = c+1

    cpa=[]                                          #lista que vai conter os valores das colunas uteis
    for i in range(len(ds[0])):#ver todas as colunas que taem valores numericos
        if number(ds[0][i]):
            cpa.append(i)
    for i in range(len(ds)):#arrendodar todos os valores da colunas com valores numericos
        for w in cpa:
            ds[i][w]= str(round(float(ds[i][w])))

    dispo = [True]*(len(colu)-1)
    ndis = len(dispo)

    if colu[0] == "ID" or colu[0] =="id" or colu[0]=="Id":
        dispo[0] = False
        ndis=ndis-1

    uni =[]
    for i in range(len(colu)):
        uni.append(unique(ds,i))
    d = Tree(colu,ds,uni)
    d.buildtree(ds,dispo,ndis,None)
    print("arvore de pesquisa obtida")
    d.printtree(None,' ',0)
    print("quer testar exemplos? 1-sim, 0-nao")
    qte=int(input())
    if qte==1:
        cj =[]
        print("nome do ficheiro")
        s= input()
        fil = open(s)
        datase = fil.read().splitlines()
        for i in datase:
            cj.append(i.split(','))
        for i in cj:
            print(d.predict(None,i))










 #--------------------------------------------------------------------------------------------------------------------





else:#para fazer o dataset do connect 4
    import numpy as np
    import copy
    import math
    import time
    def createboard():
        board = np.zeros((6,7))
        return board

    def printboard(board):
        b =""
        for i in range(6):
            for d in range (7):
                if board[i][d] == 0:
                    b = b + "_"
                elif board[i][d] == 1:
                    b = b + 'X'
                else:
                    b = b + 'O'
            b = b +'\n'
        b = b +'1234567\n'
        print(b)

    def jogada(jog,col,board):#mudar depois,vai se inserir aqui o bot
        tabu = copy.deepcopy(board)
        n = possivel(col,tabu)
        tabu[n][col] = jog
        return tabu

    def possivel(col,board):
        for i in range(6):
            if board[5-i][col] == 0:
                return 5-i
        return -1

    def possimoves(board):
        possimoves = list()
        for i in range(7):
            n = possivel(i,board)
            if n != -1:
                possimoves.append(i)
        return possimoves

    def empate(board):
            for i in range(7):
                if board[0][i] == 0:
                    return False
            return True

    def vencedor(board):
        for col in range(4):
            for li in range(6):
                if board[li][col] ==  board[li][col+1] == board[li][col+2] ==  board[li][col+3] and board[li][col] !=0:
                    return True
        for col in range(7):
            for li in range(3):
                if board[li][col] ==  board[li+1][col] ==  board[li+2][col] ==  board[li+3][col] and board[li][col] !=0:
                    return True
                    
        for col in range(4):
            for li in range(3):
                if board[li][col] ==  board[li+1][col+1] ==  board[li+2][col+2] ==  board[li+3][col+3] and board[li][col] !=0:
                    return True
        for col in range(4):
            for li in range(3, 6):
                if board[li][col] ==  board[li-1][col+1] ==  board[li-2][col+2] ==  board[li-3][col+3] and board[li][col] !=0:
                    return True
    class MonteCarloTreeSearchNode():
        def __init__(self, state,player,d, parent=None, parent_action=None):
            self.state = state
            self.parent = parent
            self.parent_action = parent_action
            self.children = []
            self._number_of_visits = 0
            self.q =0
            self._untried_actions = self.untried_actions()
            self.player = player
            self.tree =d
            return
        
        def untried_actions(self):
            self._untried_actions = possimoves(self.state)
            return self._untried_actions
        
        def n(self):
            return self._number_of_visits
        
        def expand(self):
            action = self._untried_actions.pop()
            next_state = self.move(action,self.player,self.state)
            child_node = MonteCarloTreeSearchNode(
                next_state,-self.player,self.tree, parent=self, parent_action=action)
            self.children.append(child_node)
            return child_node 
        
        def is_terminal_node(self):
            return self.is_game_over(self.state)
        
        def rollout(self):#mudanca
            current_rollout_state = self.state
            pla = self.player
            nodes =0
            possible_moves = possimoves(current_rollout_state)
            for i in possible_moves:
                state=self.move(i,pla,current_rollout_state)
                li = self.converter(state)
                if self.tree.predict(None,li) == "loss":
                    return -1,0
            if self.tree.predict(None,li) == "draw":
                return 0,0
            else: return 1,0
        def converter(self,state):
            list=[]
            for i in range(6):
                for j in range(7):
                    if state[i][j] ==0:
                        list.append('b')
                    elif state[i][j] ==1:
                        list.append('x')
                    else:
                        list.append('o')
            return list
    
        def backpropagate(self, result):
            reward = 0 if result == self.player else 1
            while self !=None:
                self._number_of_visits+=1
                self.q+= reward
                self = self.parent
                if result==0:
                    reward=0
                else:
                    reward=1-reward
        
        def is_fully_expanded(self):
            return len(self._untried_actions) == 0
        
        def best_child(self, c_param=math.sqrt(2)):#mudanca
            max =0
            move=0
            for i in self.children:
                val=(i.q / i.n()) + c_param *((math.sqrt(math.log(i.parent.n()) / i.n())))
                if val>max :
                    max=val
                    move =i
            return move
        
        def rollout_policy(self, possible_moves):
            if len(possible_moves)==0:return None
            return possible_moves[np.random.randint(0,len(possible_moves))]
        
        def _tree_policy(self):#foi mudado aqui
            current_node = self
            while not current_node.is_terminal_node():
                if not current_node.is_fully_expanded():
                    return current_node.expand()
                else:
                    current_node = current_node.best_child()
            return current_node
        
        def best_action(self,time_limit):
            start_time = time.process_time()
            nodes=0
            while time.process_time() - start_time < time_limit:
                v = self._tree_policy()
                reward,n= v.rollout()
                nodes=n+nodes
                v.backpropagate(reward)
            for i in self.children:
                li = self.converter(i.state)
                if self.tree.predict(None,li)=="loss":
                    return i
            return self.children[0]

        def is_game_over(self,board):
            return vencedor(board) or empate(board)

        def game_result(self,board):
            jog =1
            for col in range(4):
                for li in range(6):
                    if board[li][col] ==  board[li][col+1] == board[li][col+2] ==  board[li][col+3] and board[li][col] !=0:
                        if board[li][col] == jog:return 1
                        else:return -1
            for col in range(7):
                for li in range(3):
                    if board[li][col] ==  board[li+1][col] ==  board[li+2][col] ==  board[li+3][col] and board[li][col] !=0:
                        if board[li][col] == jog:return 1
                        else:return -1
                        
            for col in range(4):
                for li in range(3):
                    if board[li][col] ==  board[li+1][col+1] ==  board[li+2][col+2] ==  board[li+3][col+3] and board[li][col] !=0:
                        if board[li][col] == jog:return jog
                        else:return -jog
            for col in range(4):
                for li in range(3, 6):
                    if board[li][col] ==  board[li-1][col+1] ==  board[li-2][col+2] ==  board[li-3][col+3] and board[li][col] !=0:
                        if board[li][col] == jog:return jog
                        else:return -jog
            return 0

        def move(self,action,jog,board):
            sta= jogada(jog,action,board)
            return sta
        
    def bot(jog,board,flag):
        alpha = -math.inf
        beta  =  math.inf
        root = MonteCarloTreeSearchNode(board,jog,flag)
        d =root.best_action(2)
        jo= d.parent_action
        return jo
    

    #--------------------------------------------------------------------------------------------------------------------


    file = open("co.data")
    dataset = file.read().splitlines() 
    c=0
    colu=[]
    ds =[]
    for i in dataset:
        if c ==0:
            colu = i.split(',')
            c =c+1
        else:
            ds.append(i.split(','))
            c = c+1
    dispo = [True]*(len(colu)-1)
    ndis = len(dispo)
    uni =[]
    for i in range(len(colu)):
        uni.append(unique(ds,i))
    d = Tree(colu,ds,uni)
    d.buildtree(ds,dispo,ndis,None)

    #esta parte é para o dataset de desafio do connect 4
    boar = createboard()
    jogador =1
    printboard(boar)
    while True:
        if jogador ==1:
            colu = int(input()) -1
        else:
            start_time = time.process_time()
            colu = bot(jogador,boar,d)
            print(time.process_time() - start_time)
        boar =jogada(jogador,colu,boar)
        printboard(boar)
        if vencedor(boar):
            print(str(jogador) +' venceu ')
            break
        jogador*=-1