from . agents import *
import random


class ManfroClass(Agent):
	
	def __init__(self, x=2, y=2):
		Agent.__init__(self)
		self.img = 'Manfro'								#Immagine persomale
		self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']			#Dichiaro le azioni
		self.lastaction = 'Suck'							#Dichiaro l'ultima azione

		def program(status, bump, neighbors):
			if bump =='Bump':							#Mi serve per non ripetere l'ultima azione fatta
				if self.lastaction == 'GoNorth':				#Se l'ultima azione fatta e' stata GoNorth e ha trovato Bump, non ripetere GoNorth
					return random.choice(['GoEast', 'GoWest', 'GoSouth'])
				elif self.lastaction == 'GoSouth':				#Se l'ultima azione fatta e' stata GoSouth e ha trovato Bump, non ripetere GoSouth
					return random.choice(['GoEast', 'GoWest', 'GoNorth'])
				elif self.lastaction == 'GoEast':				#Se l'ultima azione fatta e' stata GoEast e ha trovato Bump, non ripetere GoEast
					return random.choice(['GoSouth', 'GoWest', 'GoNorth'])
				elif self.lastaction == 'GoWest':				#Se l'ultima azione fatta e' stata GoNorth e ha trovato Bump, non ripetere GoNorth
					return random.choice(['GoEast', 'GoSouth', 'GoNorth'])
			if status == "Dirty":						#Se lo stato e' Dirty allora Suck
				self.lastaction = "Suck"
				return "Suck"
			else:
				self.lastaction = random.choice(self.actions)
				return self.lastaction

		self.program = program
			
	

