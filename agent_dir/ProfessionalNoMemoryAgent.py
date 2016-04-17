from . agents import *
from random import randint


class ProfessionalNoMemoryAgentClass(Agent):

    def __init__(self):
        Agent.__init__(self)
        #self.img = 'agent_v5'
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']
        self.coord = (0, 0)
        self.visited = [(0, 0)]
        self.walls = []
        self.curr = 'GoEast'
       
        self.currNoCleans = 0
       
        self.increrandom = 0 #incremento questa variabile ogni volta che vado in loop


        def nextMove():
            self.increrandom += 1
        
            index = randint(0,3)
            return self.actions[index]
            
        def program(status, bump, neighbors):
            if self.curr != 'NoOp':
                if bump == 'Bump':
                    self.curr = nextMove()
                    return self.curr
                if status == 'Dirty':
                    self.currNoCleans -= 1
                   
                   
                    return 'Suck'
                else:

                    self.currNoCleans += 0.2
                    print(self.currNoCleans)
                    if self.increrandom == 200 or self.currNoCleans > 10:
                        self.curr = 'NoOp'
                        return self.curr
                     
                    else:
                        if self.curr == 'GoEast':
                            self.coord = (self.coord[0] + 1, self.coord[1])
                        elif self.curr == 'GoWest':
                            self.coord = (self.coord[0] - 1, self.coord[1])
                        elif self.curr == 'GoNorth':
                            self.coord = (self.coord[0], self.coord[1] + 1)
                        elif self.curr == 'GoSouth':
                            self.coord = (self.coord[0], self.coord[1] - 1)
                       
                        self.curr = nextMove()
                    return self.curr
            else:
                return self.curr
        self.program = program
