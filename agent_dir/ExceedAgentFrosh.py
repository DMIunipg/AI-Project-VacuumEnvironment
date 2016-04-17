# coding=utf-8
from . agents import *
from random import randint
import math


class ExceedAgentFroshClass(Agent):

    def __init__(self, noCleans=10):
        Agent.__init__(self)
        ##INIZIALIZZO LE VARIABILI
        self.img = 'frosh'
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']
        self.curr = 'GoEast'
        self.coord = (0, 0)
        ##salvo la posizine dell'eventuale muro
        self.walls = 'none'
        ##salvo le volte che bumpo in una direzione
        bum = [0,0,0,0]
        ##salvo le volte che trovo clean in una direzione
        pul = [0,0,0,0]
        ##salvo la posizione relativa dei vicini
        self.dist = (0,0);
        ##tengo il conto delle caselle consecutive già pulite su cui passo
        self.consec = 0;


        ##DEFINISCO LA PROSSIMA MOSSA
        def nextMove():
            ex = scegli('GoEast',0)
            wx = scegli('GoWest',1)
            nx = scegli('GoNorth',2)
            sx = scegli('GoSouth',3)
            
            #prendo il massimo tra i valori calcolati per ogni direzione
            m = max(nx,sx,ex,wx)
            
            if nx == m:
                vai = 2
            elif sx == m:
                vai = 3
            elif ex == m:
                vai = 0
            elif wx == m:
                vai = 1
            
            print(self.actions[vai])

            return self.actions[vai]
    
    
        ##FUNZIONE CHE RESTITUISCE IL NUMERO NORMALIZZATO
        def norm(arr,num):
            massimo = max(arr)
            if massimo == 0:
                return 0
            else:
                return num/massimo
        
           
        ##DEFINISCO LA PROBABILITà DELLA MOSSA
        def scegli(dir,num):
            seed = random.randint(4,7)
            prob=(seed+ifdir(dir)-norm(pul,pul[num])-norm(bum,bum[num])-ifpos(dir))*ifbump(dir)
            #print("%s: %s",dir,prob)
            return prob
        
        
        ##GUARDO DA DOVE VENGO
        def ifdir(dir):
            #se continuo ad andare dritto ho un valore più alto
            if self.curr == dir:
                return 1.5
            else:
                #se cerco di tornare indietro ho un valore negativo
                if (self.curr == 'GoEast' and dir == 'GoWest') or (self.curr == 'GoWest' and dir == 'GoEast') or (self.curr == 'GoNorth' and dir == 'GoSouth') or (self.curr == 'GoSouth' and dir == 'GoNorth'):
                    return -2
                else:
                    return 0


        ##GUARDO QUANTO DISTA L'ALTRO AGENTE
        def ifpos(dir):
            temp = 0
            #print("pos: ",self.dist)
            if self.dist[0] < 0 and dir == 'GoEast':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            if self.dist[0] > 0 and dir == 'GoWest':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            if self.dist[1] < 0 and dir == 'GoSouth':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            if self.dist[1] > 0 and dir == 'GoNorth':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            return 1*temp
        

    
        ##GUARDO SE BUMPO
        def ifbump(dir):
            if self.walls == dir:
                return 0
            else:
                return 1


    
        ##DEFINISCO IL PROGRAMMA
        def program(status, bump, neighbors):
            
            ##SE TROVO TUTTO PULITO MI FERMO
            if self.consec == 50:
                return 'NoOp'
            
            ##GUARDO I VICINI
            for (agent_id, agent_class), pos in neighbors:
                if agent_class == 'ExceedAgentFroshClass' and agent_id != self.id:
                    self.dist = pos
        
            ## se sporco aspiro
            if status == 'Dirty':
                print("suck")
                self.consec = 0
                return 'Suck'
            else:
                ## se ho sbattuto guardo dove
                if bump == 'Bump':
                    print("bump")
                    if self.curr == 'GoEast':
                        self.walls = 'GoEast'
                        bum[0]+=1
                    elif self.curr == 'GoWest':
                        self.walls = 'GoWest'
                        bum[1]+=1
                    elif self.curr == 'GoNorth':
                        self.walls = 'GoNorth'
                        bum[2]+=1
                    elif self.curr == 'GoSouth':
                        self.walls = 'GoSouth'
                        bum[3]+=1
                else: ##allora era pulito
                    self.consec += 1
                    print("already clean, ",self.consec,"consecutive")
                    if self.curr == 'GoEast':
                        pul[0]+=1
                    elif self.curr == 'GoWest':
                        pul[1]+=1
                    elif self.curr == 'GoNorth':
                        pul[2]+=1
                    elif self.curr == 'GoSouth':
                        pul[3]+=1
                self.curr = nextMove()
                return self.curr
        
        
        self.program = program
