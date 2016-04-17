from . agents import *
import random


class SuperLuigiMultiVacClass(Agent):

    def __init__(self, x=2, y=2):
        Agent.__init__(self)

        self.img = 'luigi'
        self.name = 'SuperLuigiMultiVac'
        self.last = None
        self.maxpulito = 50
        self.conta = 0
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']
        
        def program(status, bump, neighbors):
    
            ## Walls?
            muro = bump == 'Bump'

            if status == "Dirty":
                self.conta = 0
                self.last = 'Suck'
                return 'Suck' 

            elif status == "Clean":
                    self.conta += 1
                    if self.conta > self.maxpulito:
                        self.last = 'NoOp'
                        return 'NoOp'
                    else:
                        if muro or True:
                            actions = list(self.actions)
                            if self.last != None and self.last in actions:
                                actions.remove(self.last)
                            self.last = random.choice(actions)
                        else:
                            self.last = random.choice(self.actions)
                        return self.last


        self.program = program
