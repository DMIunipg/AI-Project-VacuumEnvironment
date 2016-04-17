from . agents import *
from random import randint




class ProfessionalVacuumClass(Agent):

    def __init__(self, noCleans=10):
        Agent.__init__(self)

       
        #self.img = 'agent_v5'
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']

        self.coord = (0, 0) #coordinate robottino
       
        self.contarandom = 0
        self.visited = [(100,100)] #lista posizioni visitate
       
        self.walls = []  #lista dei muri incontrati
       
        self.curr = 'GoNorth' 
        self.maxNoCleans = noCleans
        self.currNoCleans = 0
        self.consecNoCleans = 0
        self.modrandom = 0
        self.direzione = 2 #nord
        self.back = 0
        self.contatore = 0
        
        def controllaDintorni(coordinate,random):
            
            self.modrandom = 1
            #nord
            if (coordinate[0], coordinate[1] + 1) not in self.visited and (coordinate[0], coordinate[1] + 1)not in self.walls:
                direzione = 2
                self.modrandom = 0
                return direzione
            #est
            elif (coordinate[0] + 1, coordinate[1]) not in self.visited and (coordinate[0] + 1, coordinate[1])not in self.walls:
                direzione = 0
                self.modrandom = 0
                return direzione
            #sud
            elif (coordinate[0], coordinate[1] - 1) not in self.visited and (coordinate[0], coordinate[1] - 1)not in self.walls:
                direzione = 3
                self.modrandom = 0
                return direzione
            #ovest
            elif (coordinate[0] - 1, coordinate[1]) not in self.visited and (coordinate[0] - 1, coordinate[1])not in self.walls:
                direzione = 1
                self.modrandom = 0
                return direzione
            else:

               
                random = randint(0,3)
                self.modrandom = 1
                return random
                
                





        def prossimeCoord(coord, move):
            if move == 0: #verso est
                #(1,0)
                return (coord[0] + 1, coord[1])
            elif move == 1: #verso ovest
                #(-1,0)
                return (coord[0] - 1, coord[1])
            elif move == 2: #verso nord
                #(0,1)
                return (coord[0], coord[1] + 1)
            elif move == 3: #verso sud
                #(0,-1)
                return (coord[0], coord[1] - 1)



        #prossima mossa
        def nextMove(direzione):
          
            return self.actions[direzione]
       
 

        def program(status, bump, neighbors):
           
            if self.curr != 'NoOp':
                
                if self.modrandom == 1:
                    casuale = randint(0,3)
                    self.contarandom += 1
                    self.curr = nextMove(casuale)


                    if status == 'Dirty':
                        return 'Suck'
                    if self.maxNoCleans > 0 and self.currNoCleans > self.maxNoCleans or self.contarandom == 40:
                         self.curr = 'NoOp'
                    return self.curr
                    

                #se ho trovato un muro

                if bump == 'Bump':
                    if self.accesso == 1:
                        self.contatore += 1
                        
                        if self.contatore == 15:
                            self.curr = 'NoOp'
                            return self.curr
                    self.accesso = 1
                    #salvo dove trovo i muri
                    if self.curr == 'GoEast':
                        self.walls.append((self.coord[0] + 1, self.coord[1]))
                        self.coord = (self.coord[0] - 1, self.coord[1] - 1)
                        self.direzione = 3
                        if prossimeCoord(self.coord, self.direzione) in self.visited or prossimeCoord(self.coord, self.direzione) in self.walls:
                            self.coord = (self.coord[0] + 1, self.coord[1] + 1)
                            self.direzione = 1
                            self.back = 1
                         
                        else:
                            self.direzione = 3
                            





                    elif self.curr == 'GoWest': #giusto
                        self.walls.append((self.coord[0] - 1, self.coord[1]))
                        self.coord = (self.coord[0] + 1, self.coord[1] + 1)
                        self.direzione = 2
                        if prossimeCoord(self.coord, self.direzione) in self.visited or prossimeCoord(self.coord, self.direzione) in self.walls:
                            self.coord = (self.coord[0] - 1, self.coord[1] - 1)
                            self.direzione = 0
                            self.back = 1
                            
                        else:
                            self.direzione = 2
                            



                


                    elif self.curr == 'GoNorth':
                        self.walls.append((self.coord[0], self.coord[1] + 1))
                        self.coord = (self.coord[0] + 1, self.coord[1] - 1)
                        self.direzione = 0  
                        if prossimeCoord(self.coord, self.direzione) in self.visited or prossimeCoord(self.coord, self.direzione) in self.walls:
                            self.coord = (self.coord[0] - 1, self.coord[1] + 1)
                            self.direzione = 3
                            self.back = 1
                            
                        else:
                            self.direzione = 0
                                        





                    elif self.curr == 'GoSouth':
                        self.walls.append((self.coord[0], self.coord[1] - 1))
                        self.coord = (self.coord[0] - 1, self.coord[1] + 1)
                        self.direzione = 1
                        if prossimeCoord(self.coord, self.direzione) in self.visited or prossimeCoord(self.coord, self.direzione) in self.walls:
                            self.coord = (self.coord[0] + 1, self.coord[1] - 1)
                            self.direzione = 2
                            self.back = 1
                            
                        else:
                            self.direzione = 1
                            
                 
                    self.curr = nextMove(self.direzione)

                    return self.curr
                else:
                    self.accesso = 0

                #se trovo sporco
                if status == 'Dirty':
                    self.currNoCleans -= 2
                    self.consecNoCleans = 0
                    self.back = 0

                    #esamino la posizione successiva
                    if prossimeCoord(self.coord, self.direzione) in self.visited:
                        if self.direzione == 1:
                                self.direzione = 2
                                self.curr = 'GoNorth'
                        elif self.direzione == 2:
                                self.direzione = 0
                                self.curr = 'GoEast'
                                
                        elif self.direzione == 0:
                                self.direzione = 3
                                self.curr = 'GoSouth'
                        elif self.direzione == 3:
                                self.direzione = 1
                                self.curr = 'GoWest'
                                
                    
                    return 'Suck'
              
                else:   
                    self.consecNoCleans += 1
                    self.currNoCleans += 1
                    
                    #condizione di terminazione
                    if self.maxNoCleans > 0 and self.currNoCleans > self.maxNoCleans or self.contarandom == 40:
                        self.curr = 'NoOp'
                        return self.curr
                    
                    else:  
                        
                        if self.back == 0:

                        

                            self.visited.append(self.coord)
                            
                            
                        
                        if self.curr == 'GoEast' and  prossimeCoord(self.coord, self.direzione) in self.visited: #giusto
                       
                            if self.back == 1:
                                
                                
                                nuovadirezione = controllaDintorni(self.coord,self.modrandom)
                                self.coord = (self.coord[0] + 2, self.coord[1] + 1)
                                
                                self.direzione = nuovadirezione
                                self.back = 0
                            else:     
                                self.coord = (self.coord[0] + 1, self.coord[1])


                        elif self.curr == 'GoWest' and  prossimeCoord(self.coord, self.direzione) in self.visited: 
                       
                            if self.back == 1:
                                
                                nuovadirezione = controllaDintorni(self.coord,self.modrandom)
                                self.coord = (self.coord[0] - 2, self.coord[1] - 1) #verificare
                                self.direzione = nuovadirezione
                                self.back = 0
                            else:     
                                self.coord = (self.coord[0] - 1, self.coord[1])



                        elif self.curr == 'GoSouth' and  prossimeCoord(self.coord, self.direzione) in self.visited:
                       
                            if self.back == 1:
                                
                                nuovadirezione = controllaDintorni(self.coord,self.modrandom)
                                self.coord = (self.coord[0] + 2, self.coord[1] - 1) #verificare
                                self.direzione = nuovadirezione
                                self.back = 0
                            else:     
                                self.coord = (self.coord[0] + 1, self.coord[1])



                        elif self.curr == 'GoNorth' and  prossimeCoord(self.coord, self.direzione) in self.visited:
                       
                            if self.back == 1:
                                
                                nuovadirezione = controllaDintorni(self.coord,self.modrandom)
                                self.coord = (self.coord[0] - 2, self.coord[1] + 1) #verificare
                                self.direzione = nuovadirezione
                                self.back = 0
                            else:     
                                self.coord = (self.coord[0] - 1, self.coord[1])




                        elif self.curr == 'GoEast': 
                             self.coord = (self.coord[0] + 1, self.coord[1])
                        elif self.curr == 'GoWest':  
                            self.coord = (self.coord[0] - 1, self.coord[1])
                     
                        elif self.curr == 'GoNorth': 
                            self.coord = (self.coord[0], self.coord[1] + 1)
                           
                        elif self.curr == 'GoSouth':  
                            self.coord = (self.coord[0], self.coord[1] - 1)

                        
                       
                        self.curr = nextMove(self.direzione)
                    
                    return self.curr  
            else:
                return self.curr
        self.program = program