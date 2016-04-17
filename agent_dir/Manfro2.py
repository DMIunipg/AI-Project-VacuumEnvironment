#!/usr/bin/python
# -*- coding: utf-8 -*-
from . agents import *
import random
 
class Manfro2Class(Agent):
 
    def __init__(self, x=0, y=0):
        Agent.__init__(self)
        #self.img = 'agent_v5'  # Immagine persomale
        # Dichiaro le azioni
 
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']
        self.lastaction = ''  # Dichiaro l'ultima azione
        self.pos = (0, 0)  # Indicizzo la posizione iniziale
        self.memory = {}  # Definisco la memoria dell'agente
        self.clean = 0
        def Update():                   #update aggiorna la posizione in base all'ultima azione
            if self.lastaction == 'GoNorth':
                self.pos = (self.pos[0], self.pos[1] + 1)
                return self.pos
            elif self.lastaction == 'GoSouth':
                self.pos = (self.pos[0], self.pos[1] - 1)
                return self.pos
            elif self.lastaction == 'GoEast':
                self.pos = (self.pos[0] + 1, self.pos[1])
                return self.pos
            elif self.lastaction == 'GoWest':
                self.pos = (self.pos[0] - 1, self.pos[1])
                return self.pos
 
        def program(status, bump, neighbors):           #cerco di finire le azioni e se non ci sono faccio un movimento dato da una scelta random di possibili azioni da fare
            Update()
            if self.pos not in self.memory:
                self.memory[self.pos] = [
                    'Suck', 'GoEast', 'GoWest', 'GoNorth', 'GoSouth']
 
            if status == 'Dirty':  # Se lo stato e' Dirty allora Suck
                if "Suck" in self.memory[self.pos]:
                    self.lastaction = self.memory[self.pos].pop(0)
                    return 'Suck'
            #for agent, pos in neighbors:
                #x, y = pos
                #self.memory[(self.pos[0]+x, self.pos[1]+y)] = []
 
            if bump != 'Bump':
                if len(self.memory[self.pos]) > 0:
                    self.lastaction = self.memory[self.pos].pop(0)
                    return self.lastaction
                else:
                    self.lastaction = random.choice(self.actions).pop(self.pos)
                    return self.lastaction
            else:
                new_actions = [
                    elm for elm in self.actions if elm != self.lastaction]
                self.lastaction = random.choice(new_actions)
                return self.lastaction
            if status == "Clean":       #Contatore che manda in NoOp l'agente qualora Clean > 25
                self.clean += 1 
            if self.clean > 25:
                return "NoOp"
        
        
        self.program = program
