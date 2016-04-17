from . agents import *
from random import randint


class ParProSMClass(Agent):
    

    def __init__(self):
    
        Agent.__init__(self)
        
        self.img = 'R2D2'                               #viene impostata una immagine per vacuum cleaner
        self.name = 'ParProAgentSM'                         #nome agente
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']           #azioni possibili
        self.coord = (0,0)                              #coordinata iniziale
        self.curr = 'Inizio'                                #azione corrente
        self.consecutive = 0                                #contatore per contare in quante celle consecutive non pulisco
        self.last4pos = []                              #ultime 4 posizioni visitate dall'agente
        self.otheragentpos = []                             #posizione degli altri agenti
        self.posizioniEscluse = []                          #posizioni in cui possono andare gli altri agenti che noi escluderemo
        self.ultimoSpostamento = ""                         #serve per vedere se ci sono bump consecutivi
        self.numBump = 2                                #serve per recuperare la posizione giusta dopo i bump
        


#--------------------------------------------------------------------------------------------------------------------
#funzione che informa l'agente se pulire la casella in cui si sovrappongono o passare alla casella successiva


        def pulisceSeSovrapposti(neighbors):
            pulisci = True
            for (agent_id, agent_class), pos in neighbors:                  #cicla per tutti i neighbors
                if pos == (0, 0):                           #se la posizione relativa e' (0, 0) allora sono sovrapposti
                    if self.id > agent_id:                      #se il nostro agente ha un ID maggiore, rispetto a quello dell'altro agente                                                     #sovrapposto, non fara' Suck e passa alla mossa successiva(Non perde 20 punti per                                                   #succhiare dove e' gia stato pulito dal quello con ID minore)
                        pulisci = False
            return pulisci


#--------------------------------------------------------------------------------------------------
#salvo le posizioni dei vicini , ogni turno le cancello e le aggiorno


        def controllaVicini(neighbors):
            self.otheragentpos = []                         #per mantenere una memoria fissa e non illimitata
            for (agent_id, agent_class), pos in neighbors:
                if agent_id != self.id:
                    self.otheragentpos.append(pos)


    
#-----------------------------------------------------------------------------------------------------
#Partendo dalle posizioni dei vicini salvo le posizioni in cui si potrebbero spostare in modo da escluderle quando
#scegliero' il mio spostamento


        def escludiMosse():
            self.posizioniEscluse = []                      #per mantenere una memoria fissa e non illimitata
            for pos in self.otheragentpos:
                self.posizioniEscluse.append((pos[0]+1,pos[1]))         #est
                self.posizioniEscluse.append((pos[0],pos[1]+1))         #nord
                self.posizioniEscluse.append((pos[0]-1,pos[1]))         #ovest
                self.posizioniEscluse.append((pos[0],pos[1]-1))         #sud



#-------------------------------------------------------------------------------------------------------
#Questa funzione prende come parametro una coordinata e un intero rappresentante le direzioni
#nelle quali posso muovermi e calcola la coordinata nuova 



        def findCoord(coord, move):
            if move == 0:
                return (coord[0]+1,coord[1])
            elif move == 1:
                return (coord[0]-1,coord[1])
            elif move == 2:
                return (coord[0],coord[1]+1)
            elif move == 3:
                return (coord[0],coord[1]-1)


#------------------------------------------------------------------------------------------------------
#Funzione che permette di muoversi e prende come parametro un azione e i vicini


    
        def nextMove(act,neighbors):
            
            controllaVicini(neighbors)                      #controllo le coordinate degli altri agenti
            escludiMosse()                              #escludo le celle nelle quali si possono muovere i miei vicini  
            

            #se l'azione e' muoversi aggiungo in coda la mia coordinata nel vettore delle ultime quattro posizioni
            #nell'if ci entro solo se ancora non ho fatto 4 mosse, altrimenti estraggo in testa e inserisco in coda
            
            if act == "Move":
                
                if len(self.last4pos) < 4:
                    self.last4pos.append(self.coord)
                else:
                    self.last4pos.pop(0)
                    self.last4pos.append(self.coord)
            


            #Se l'azione e' bump inserisco la posizione in cui ho fatto bump tra le ultime 4 visitate come sopra, dopo di che
            #faccio un controllo per recuperare la posizione giusta all'interno del terreno, se la lunghezza del vettore last4pos e' minore
            #del numero di bump che ho fatto (tenuto da numBump), pongo la mia coordinata uguale alla prima in modo da non perderla
            #datp che e' la posizione in cui si trova realmente l'agente all'interno del terreno, altrimenti recupero la pos dell'agente
            #prendendo la posizione di indice lunghezza del vettore last4pos - numero di bump
            
            
            if act == "Bump":

                if len(self.last4pos) < 4:
                    if self.coord not in self.last4pos:
                        self.last4pos.append(self.coord)
                else:
                    if self.coord not in self.last4pos:
                        self.last4pos.pop(0)
                        self.last4pos.append(self.coord)
                if (len(self.last4pos) - self.numBump) < 0:
                    self.coord = self.last4pos[0]
                else:
                    self.coord = self.last4pos[len(self.last4pos) - self.numBump]

            
            #Qui decido quale azione compiere scegliendo un intero da 0 a 3 random che rappresenta una delle direzioni
            #controllo se la cella in cui vado a finire dopo lo spostamento scelto non e' presente tra le posizioni escluse o tra quelle
            #che ho gia' visitato, se non c'e' esco dal ciclo e ritorno l'indice, se c'e' faccio al massimo 5 cicli dopo di che esco lo
            #stesso e restituisco l'ultimo indice calcolato, questo fa si che non si fermi se ha tutte le celle vicine indisponibili 
            controlla = True
            index = 0
            count = 0
            while controlla == True:
                index = randint(0, 3)
                if findCoord(self.coord, index) not in self.last4pos:
                    if findCoord(self.coord, index) not in self.posizioniEscluse:
                        controlla = False
                
                if count == 4:
                    controlla = False
                count +=1
            return self.actions[index]      



#--------------------------------------------------------------------------------------------------------------------
#funzione che aggiorna le coordinate in base alla nuova mossa generata dalla funzione nextMove



        def changeCoords():
            if self.curr == 'GoEast':
                self.coord = (self.coord[0]+1,self.coord[1])                #se GoEast incrementa di 1 la x 
            elif self.curr == 'GoWest':
                self.coord = (self.coord[0]-1,self.coord[1])                #se GoWest decrementa di 1 la x 
            elif self.curr == 'GoNorth':
                self.coord = (self.coord[0],self.coord[1]+1)                #se GoNorth incrementa di 1 la y 
            elif self.curr == 'GoSouth':
                self.coord = (self.coord[0],self.coord[1]-1)                #se GoSouth decrementa di 1 la y 






#-----------------------------------------------------------------------------------------------------------------------
#Questo e' il programma principale


    
        def program(status, bump, neighbors):
        
            if self.ultimoSpostamento != "Bump":                        #controllo se l'ultimo spostamento non e' bump
                if bump == "Bump":                          #se questo turno ho fatto bump
                    self.ultimoSpostamento = "Bump"                 #pongo l'ultimo spostamento uguale a bump
            
            else:                                       #se era bump e ora non faccio bump allora riinizializzo ultimo spotamento
                if bump != "Bump":                          #e il numero di bump, altrimenti incremento il numero di bump
                    self.ultimoSpostamento = ""
                    self.numBump = 2
                else:
                    self.numBump +=1


            if self.curr != 'NoOp':                             #se non devo stare fermo
                if bump == 'Bump':
                                #se faccio un bump richiamo nextmove con bump
                    self.curr = nextMove("Bump",neighbors)              #e poi scelgo in quale direzione muovermi in base all'indice che torna in nextMove
                    
                    changeCoords()                          #funzione che aggiorna le coordinate
        
                    return self.curr
                            
                if status == 'Dirty':

                    if pulisceSeSovrapposti(neighbors) == False:            #se il nostro agente e' sovrapposto ma ha ID minore passa alla mossa successiva                                                 #senza succhiare quella cella che e' gia' pulita da quello con ID minore

                        self.curr = nextMove("Move",neighbors)
                        
                        changeCoords()
                    
                        return self.curr

                    else:                               #altrimenti succhia

                        self.consecutive = 0

                        return 'Suck'               


                else:
                    self.consecutive += 1

                    if self.consecutive > 50:                   #se sono passato per 50 volte consecutive su celle gia' pulite mi arresto

                        self.curr = 'NoOp'

                        return self.curr

                    else:

                        self.curr = nextMove("Move",neighbors)
                        
                        changeCoords()

                        return self.curr
            else:
                return self.curr



    
        self.program = program
