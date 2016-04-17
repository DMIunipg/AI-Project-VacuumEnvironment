# coding=utf-8
from __future__ import division
from . agents import *
from random import randint


class hudrobotproClass(Agent):    
    def __init__(self, noCleans=10):
        Agent.__init__(self)
        self.name = 'HudrobotPro' 
        #self.img = 'maid' ## Immagine in base all'ID dell'agente 
        self.actions = ['GoNorth', 'GoEast', 'GoSouth', 'GoWest'] # array direzionale
        self.perc_attuale = [50, 15, 20, 15] ## "%" non numerica dei movimenti possibili
        self.pos_prec = 999  # inizializzazione posizione "precedente"; 999 indica nessuna posizione
        self.grade = 'M' # indica se l'agente è master (M) o slave (S)
        self.designedPos = 1 # indica la direzione preferenziale nel calcolo "dell'euristica", inizializzato ad "Est"
        self.passed = 200 # contatore per lo stato "goal" (fittizio) indica il nuero di movimenti massimi esclusi i bump
        self.bumpList = [] # lista dei Muri
        self.visitedList = [] # lista delle posizioni visitate
        self.position = [0,0] # tupla per la posizione "attuale"o
        self.pre_action = "NoOp"
        self.baseValue = 28 # valore asegnato ad una casella pulita già visitata
        self.betterValue = 250 # valore asegnato ad una casella sconosciuta (??)
        self.designedPosValue = 30 # valore asegnato ad una casella nella direzione prefissata (in base gli altri agenti)
        self.goSuckValue = 200 # valore assegnato ad una casella "successiva" a quella del suck
        self.sameDirectionValue = 155 # valore assegnato ad una diezione contigua e sconosciuta (??)
        self.denyValue = 28 # valore da sottrarre se la casella dalla quale provengo è "la prossima prevista"
        self.cleanded = 0 # contatore celle pulite visitate.

        def bumped(): # funzione che risponde al "bump"
            aggiornaMuri()
            self.pre_action = "Bump"
            # print("arrivato Bump* ******** ************ ")
            return muovi()

        def spostato(): # funzione che risponde all'vento movimento su locazione pulita
            self.pre_action = "Move"
            self.cleanded += 1
            return muovi() 

        def aggiornaAsseMovimento(NumAxes): # aggiorna i valori di movimento sulla posizione  relativa dell'array di azioni
            if NumAxes == self.designedPos:
                self.perc_attuale[NumAxes] += self.designedPosValue
            if NumAxes == self.pos_prec and self.pre_action == "Suck":
                self.perc_attuale[NumAxes] += self.goSuckValue
            if NumAxes == self.pos_prec:
                self.perc_attuale[NumAxes] += self.sameDirectionValue
            if NumAxes == ((self.pos_prec+2)%4):
                self.perc_attuale[NumAxes] -= self.denyValue

        def generaEuristica():
            relativeX = self.position[0]
            relativeY = self.position[1] 

            if ([relativeX, relativeY+1] in self.bumpList): #Se a nord è muro, allora assegno 0
                self.perc_attuale[0] = 0
            else: #altrimenti, verifico se è visitato
                if ([relativeX, relativeY+1] in self.visitedList): #se non è visitato assegno 25, altrimenti 10
                    self.perc_attuale[0] = self.baseValue
                else:
                    self.perc_attuale[0] = self.betterValue
                aggiornaAsseMovimento(0)

            if ([relativeX+1, relativeY] in self.bumpList): #Se a est è muro, allora assegno 0
                self.perc_attuale[1] = 0
            else: #altrimenti, verifico se è visitato
                if ([relativeX+1, relativeY] in self.visitedList): #se non è visitato assegno 25, altrimenti 10
                    self.perc_attuale[1] = self.baseValue
                else:
                    self.perc_attuale[1] = self.betterValue
                aggiornaAsseMovimento(1)

            if ([relativeX, relativeY-1] in self.bumpList): #Se a sud è muro, allora assegno 0
                self.perc_attuale[2] = 0
            else: #altrimenti, verifico se è visitato
                if ([relativeX, relativeY-1] in self.visitedList): #se non è visitato assegno 25, altrimenti 10
                    self.perc_attuale[2] = self.baseValue
                else:
                    self.perc_attuale[2] = self.betterValue
                aggiornaAsseMovimento(2)
        
            if ([relativeX-1, relativeY] in self.bumpList): #Se a ovest è muro, allora assegno 0
                self.perc_attuale[3] = 0
            else: #altrimenti, verifico se è visitato
                if ([relativeX+1, relativeY] in self.visitedList): #se non è visitato assegno 25, altrimenti 10
                    self.perc_attuale[3] = self.baseValue
                else:
                    self.perc_attuale[3] = self.betterValue
                aggiornaAsseMovimento(3)

        def muovi(): # funzione che calcola il prossimo movimento
            # genera la posizione
            if self.pos_prec != 999:
                generaEuristica();

            id1 = self.perc_attuale[0]
            id2 = id1 + self.perc_attuale[1]
            id3 = id2 + self.perc_attuale[2]
            id4 = id3 + self.perc_attuale[3] + 1
            # print(self.perc_attuale)

            #standardizzoal 100%
            self.perc_attuale[0] = int(float((self.perc_attuale[0] * 100)/id4))
            self.perc_attuale[1] = int(float((self.perc_attuale[1] * 100)/id4))
            self.perc_attuale[2] = int(float((self.perc_attuale[2] * 100)/id4))
            self.perc_attuale[3] = int(float((self.perc_attuale[3] * 100)/id4))

            id1 = self.perc_attuale[0]
            id2 = id1 + self.perc_attuale[1]
            id3 = id2 + self.perc_attuale[2]
            id4 = id3 + self.perc_attuale[3]

            index = int(random.randint(1, 101)) #  "rolled" index
            print("random=", index)
            print(self.perc_attuale)
            #print(self.pos_prec)
            # identifica quale delle 4 in %, aggiornando il movimento "precedente" per l'istante k+1
            if (index >= 0 and index <id1 and self.perc_attuale[0] != 0): ## è loc 0
                self.pos_prec = 0
                return self.actions[0] # controlla che non sia un muro la prossima mossa                    
            if (index >= id1 and index <id2 and self.perc_attuale[1] != 0): # è loc 1
                self.pos_prec = 1
                return self.actions[1] # controlla che non sia un muro la prossima mossa
            if (index >= id2 and index <id3 and self.perc_attuale[2] != 0): # è loc 2
                self.pos_prec = 2 
                return self.actions[2] # controlla che non sia un muro la prossima mossa
            if (index >= id3 and index <= 101 and self.perc_attuale[3] != 0): # è loc 3    
                self.pos_prec = 3
                return self.actions[3] # controlla che non sia un muro la prossima mossa

        def amici(neighbors): #verifico quale agente è più vicino e applico modifiche
            # Go near first neighbor (Funzione di Mirco Tracolli)
            a_near = min([((agent_id, agent_class), pos)
                        for (agent_id, agent_class), pos in neighbors
                        if agent_id != self.id],
                        key=lambda obj: obj[1]  # select position as filter
                      )
            (agent_id, agent_class), pos = a_near # Ho l'agente più vicino

            if agent_id != self.id: #controllo che tipo o che agente è
                if agent_class == self.name: # amico
                    if (min(pos) == 0): # allora è a 0,0, sto sopra un vicino amico/nemico
                        if agent_id < self.id: # sono slave
                            self.grade = 'S'
                            #self.img = 'maid' # aggiorno immagine
                            return true
                        else:
                            self.grade = 'M' # sono master, controllo se è la prima mossa
                            if self.pos_prec == 999: # anticipiamo l'avversario
                                return muovi() 
                            else:
                                return spostato()
                else: # questo è un nemico                            
                    # if agent_class != self.name:                    
                    if (abs(pos[0]) >= abs(pos[1])): # allora la X è maggiore; mi muovo sulla X
                        if pos[0] < 0:
                            self.designedPos = 1 # la posizione designata è "est"
                        else:
                            self.designedPos =  3 # la posizione designata è "ovest"
                    else: # mi muovo sulla Y
                        if pos[1] < 0:
                            self.designedPos =  0 # la posizione designata è "nord"
                        else:
                            self.designedPos =  2 # la posizione designata è "sud"
                return true

        def aggiornaPosizione():
            if self.pos_prec != 999:
                if self.pos_prec == 0: # era andato a nord
                    self.position[1] +=  1
                elif self.pos_prec == 1: # era andato a est
                    self.position[0] += 1
                elif self.pos_prec == 2: # era andato a sud
                    self.position[1] -=  1
                elif self.pos_prec == 3: # era andato a ovest
                    self.position[0] -=  1

                relativeX = self.position[0]
                relativeY = self.position[1]
                if  not ([relativeX, relativeY] in self.visitedList):
                    self.visitedList.append([relativeX, relativeY])
            else:
                relativeX = 0 #se è la prima posizione, setta la (0,0) 
                relativeY = 0
                self.visitedList.append([relativeX, relativeY])

            # print("posizioni", self.visitedList)  

        def aggiornaMuri(): 
            relativeX = self.position[0]
            relativeY = self.position[1] 
            # print(self.position)
                    
            if self.pos_prec == 0: # era andato a nord
                relativeY = self.position[1] + 1
            elif self.pos_prec == 1: # era andato a est
                relativeX = self.position[0] + 1
            elif self.pos_prec == 2: # era andato a sud
                relativeY = self.position[1] - 1
            elif self.pos_prec == 3: # era andato a ovest
                relativeX = self.position[0] - 1

            if (relativeY == 0) and (relativeX == 0):
                return

            if  not ([relativeX, relativeY] in self.bumpList):
                self.bumpList.append([relativeX, relativeY])
 
            #print("muri", self.bumpList)

        def sporco():                   
            self.pre_action = "Suck"     
            return 'Suck' # è sporco, pulisce
     
        def program(status, bump, neighbors): 
            # print("*******************")
            if (self.passed == 0) or (self.cleanded >= 35): # raggiungo lo stato terminale
                return"NoOp"

            if not neighbors: #  ho vicini ?
                amici(neighbors) # verifico e applico le K
            
           
            if bump == 'Bump':  # avviene il bump?
                return bumped() 
            
            if status == 'Dirty':  # è sporco ?
                self.cleanded = 0
                return sporco()
            else: 
                # se è pulito (!= 'Dirty')
                aggiornaPosizione(); 
                self.passed -=1 # se pulito, avvicina lo stato finale
                return spostato()

        self.program = program

