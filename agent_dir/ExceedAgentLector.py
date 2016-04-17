# coding=utf-8
from . agents import *
from random import randint
import math


class ExceedAgentLectorClass(Agent):

    def __init__(self, noCleans=10):
        Agent.__init__(self)
        ##INIZIALIZZO LE VARIABILI
        self.img = 'lector'
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']
        self.coord = (0, 0)
        self.visited = [(0, 0)]
        ##mappo i muri
        self.walls = []
        ##salvo dove si spostano gli agenti avversari
        self.others = []
        self.curr = 'GoEast'
        ##salvo la posizione relativa dei vicini
        self.dist = (0,0)
        ##tengo il conto delle caselle consecutive già pulite su cui passo
        self.consec = 0
        ##tengo il conto di tutte le caselle pulite da me
        self.clearTiles = 0
        ##salvo le coordinate relative al mio punto di partenza
        self.coord = (0,0)
        #stima della grandezza della mappa
        self.extN = 0
        self.extS = 0
        self.extE = 0
        self.extS = 0


        ##DEFINISCO LA PROSSIMA MOSSA
        def nextMove():
            ex = scegli('GoEast',0)
            wx = scegli('GoWest',1)
            nx = scegli('GoNorth',2)
            sx = scegli('GoSouth',3)
            
            m = max(nx,sx,ex,wx)
            
            if nx == m:
                vai = 2
            ##self.coord = (self.coord[0],self.coord[1] + 1)
            elif sx == m:
                vai = 3
            ##self.coord = (self.coord[0],self.coord[1] - 1)
            elif ex == m:
                vai = 0
            ##  self.coord = (self.coord[0] + 1,self.coord[1])
            elif wx == m:
                vai = 1
            ##  self.coord = (self.coord[0] - 1,self.coord[1])
            
            print("coord: ",self.coord,", ",self.actions[vai])

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
            seed = random.randint(5,7)
            prob=(seed+ifdir(dir)-ifVisto(dir)-ifpos(dir))*ifbump(dir)
            #print("%s: %s",dir,prob)
            return prob
        
        
        ##GUARDO DA DOVE VENGO
        def ifdir(dir):
            if self.curr == dir:
                return 1.5
            else:
                if (self.curr == 'GoEast' and dir == 'GoWest') or (self.curr == 'GoWest' and dir == 'GoEast') or (self.curr == 'GoNorth' and dir == 'GoSouth') or (self.curr == 'GoSouth' and dir == 'GoNorth'):
                    return -1.5
                else:
                    return 0


        ##GUARDO QUANTO DISTA L'ALTRO AGENTE
        def ifpos(dir):
            temp = 0
            #print("pos: ",self.dist)
            if self.dist[0] < 0 and dir == 'GoEast':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            elif self.dist[0] > 0 and dir == 'GoWest':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            elif self.dist[1] < 0 and dir == 'GoSouth':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            elif self.dist[1] > 0 and dir == 'GoNorth':
                temp = 1/math.sqrt(self.dist[0]**2+self.dist[1]**2)
            return 1*temp
        

        ##GUARDO SE è GIà VISITATO
        def ifVisto(dir):
            temp_coord = self.coord
            if dir == 'GoNorth':
                temp_coord = (temp_coord[0],temp_coord[1] + 1)
            elif dir == 'GoSouth':
                temp_coord = (temp_coord[0],temp_coord[1] - 1)
            elif dir == 'GoEast':
                temp_coord = (temp_coord[0] + 1,temp_coord[1])
            elif dir == 'GoWest':
                temp_coord = (temp_coord[0] - 1,temp_coord[1])
            if temp_coord in self.visited:
                return 1
            else:
                if temp_coord in self.others:
                    return 0.5
                return 0
        
        ##GUARDO SE BUMPO
        def ifbump(dir):
            temp_coord = self.coord
            if dir == 'GoNorth':
                temp_coord = (temp_coord[0],temp_coord[1] + 1)
            elif dir == 'GoSouth':
                temp_coord = (temp_coord[0],temp_coord[1] - 1)
            elif dir == 'GoEast':
                temp_coord = (temp_coord[0] + 1,temp_coord[1])
            elif dir == 'GoWest':
                temp_coord = (temp_coord[0] - 1,temp_coord[1])

            if temp_coord in self.walls:
                return 0
            else:
                return 1

        ##GUARDO DOVE SONO I VICINI
        def whereNei(neighbors):
            
            for (agent_id, agent_class), pos in neighbors:
                if agent_class == 'ExceedAgentLectorClass' and agent_id != self.id:
                    self.dist = pos
                    if pos not in self.visited:
                        self.visited.append((self.coord[0]+pos[0],self.coord[1]+pos[1]))
                else:
                    if pos not in self.others:
                        self.others.append((self.coord[0]+pos[0],self.coord[1]+pos[1]))
    


        
        
        
        ##DEFINISCO IL PROGRAMMA
        def program(status, bump, neighbors):
            
            print("muri",self.walls)
            print("io:",self.coord)
            print("visitati:",self.visited)
            
            ##SE TROVO TUTTO PULITO MI FERMO
            if self.consec > 15:
                #stimo la grandezza della mappa
                for x in self.walls:
                    self.extN = max(self.extN,x[1])
                    self.extS = min(self.extS,x[1])
                    self.extE = max(self.extN,x[0])
                    self.extO = min(self.extS,x[0])

                height = self.extN-self.extS-1
                width = self.extE-self.extO-1
                size = height*width
                self.clearTiles = len(self.visited)
                
                print("n: ",self.extN,", s: ",self.extS,", e:",self.extE,", o:",self.extO)
                print("size: ",size,", clear tiles: ",self.clearTiles)
                print("consecutive",self.consec)
                
                if (self.clearTiles > 0.8*size) or (self.consec > size):
                    if status == 'Dirty':
                        print("suck")
                        self.consec = 0
                        whereNei(neighbors);
                        return 'Suck'
                    return 'NoOp'
        
        
            ## se sporco aspiro
            if status == 'Dirty':
                print("suck")
                self.consec = 0
                whereNei(neighbors);
                return 'Suck'
            
            else:
                ## se ho sbattuto guardo dove
                if bump == 'Bump':
                    print("bump")
                    if self.curr == 'GoEast':
                        self.walls.append((self.coord[0] + 1, self.coord[1]))
                    elif self.curr == 'GoWest':
                        self.walls.append((self.coord[0] - 1, self.coord[1]))
                    elif self.curr == 'GoNorth':
                        self.walls.append((self.coord[0], self.coord[1] + 1))
                    elif self.curr == 'GoSouth':
                        self.walls.append((self.coord[0], self.coord[1] - 1))
                else: ##allora era pulito
                    self.consec += 1
                    print("already clean, ",self.consec,"consecutive")
                    if self.curr == 'GoEast':
                        self.coord = (self.coord[0] + 1, self.coord[1])
                    elif self.curr == 'GoWest':
                        self.coord = (self.coord[0] - 1, self.coord[1])
                    elif self.curr == 'GoNorth':
                        self.coord = (self.coord[0], self.coord[1] + 1)
                    elif self.curr == 'GoSouth':
                        self.coord = (self.coord[0], self.coord[1] - 1)
                    
                    if self.coord not in self.visited:
                        self.visited.append(self.coord)

                whereNei(neighbors)
                self.curr = nextMove()
                return self.curr
        
        
        self.program = program
