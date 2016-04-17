
# coding=utf-8
from . agents import *
from random import randint


class hudrobotClass(Agent):    
    def __init__(self, noCleans=10):
        Agent.__init__(self)
        self.name = 'Hudrobot' 
        #self.img = 'minion' ## Immagine in base all'ID dell'agente 
        self.actions = ['GoNorth', 'GoEast', 'GoSouth', 'GoWest'] # array direzionale
        self.perc_attuale = [55, 20, 5, 20] ## "%" non numerica dei movimenti possibili
        self.pos_prec = 999  # inizializzazione posizione "precedente"; 999 indica nessuna posizione
        self.grade = 'M' # indica se l'agente è master (M) o slave (S)
        self.designedPos = 1 # indica la direzione preferenziale nel calcolo "dell'euristica", inizializzato ad "Est"
        self.passed = 100 # contatore per lo stato "goal" (fittizio) indica il nuero di movimenti massimi esclusi i bump

        def k(pos, numb): 
            # ridistribuisce le % per la posizione per il prossimo movimento (simulando una Euristica)
            # Prende la posizione da EVITARE più la percentuale di incremento per le altre direzioni
            # Il master "si sposta" in modo diretto alla posizione preferenziale, lo slave nel primo adiacente
            numb = numb/4 
            resto = numb%4
            for i, x in enumerate(self.perc_attuale):
                if i != pos:
                    self.perc_attuale[i] += numb
                if i == self.designedPos: # determinata la posizione preferenziale 
                    if self.grade == "M":
                        self.perc_attuale[i] += numb
                    else:
                        self.perc_attuale[((i+2)%4)] += numb

            self.perc_attuale[((pos+2)%4)] += resto

        def k2(pos, numb): 
            # ridistribuisce le % per la posizione dopo un bump (simulando una Euristica)
            # Prende la posizione da EVITARE più la percentuale di incremento per le direzioni adiacenti
            # Il master "si sposta" in modo diretto alla posizione preferenziale, lo slave nel primo adiacente
            numb = numb/3
            resto = numb%3
            for i, x in enumerate(self.perc_attuale):
                if (i != pos and i != (pos+2)%4):
                    self.perc_attuale[i] += numb
                if i == self.designedPos: # determinata la posizione preferenziale 
                    if self.grade == "M":
                        self.perc_attuale[i] += numb
                    else:
                        self.perc_attuale[((i+2)%4)] += numb

            self.perc_attuale[((pos+2)%4)] += resto

        def bumped(): # funzione che risponde al "bump"
            tempVal = self.perc_attuale[self.pos_prec]
            self.perc_attuale[self.pos_prec] = 0
            k2(self.pos_prec, tempVal) # esegue la k2 sulla direzione del bump
            return muovi()

        def spostato(): # funzione che risponde all'vento movimento su locazione pulita
            noMove= (self.pos_prec + 2)%4
            enumb = self.perc_attuale[noMove]/2
            self.perc_attuale[noMove] = self.perc_attuale[noMove]/2
            k(noMove, enumb) # esegue la k2 sulla direzione dettata in precedenza
            return muovi() 
                
        def muovi(): # funzione che calcola il prossimo movimento
            # genera la posizione
            id1 = self.perc_attuale[0]
            id2 = id1 + self.perc_attuale[1]
            id3 = id2 + self.perc_attuale[2]
            id4 = id3 + self.perc_attuale[3] 
           
            index = int(random.randint(1, int(id4)+1))  #  "rolled" index
            # identifica quale delle 4 in %, aggiornando il movimento "precedente" per l'istante k+1
            if (index >= 0 and index <id1 and self.perc_attuale[0] != 0): ## è loc 0
                self.pos_prec = 0
                return self.actions[0]
            if (index >= id1 and index <id2 and self.perc_attuale[1] != 0): # è loc 1
                self.pos_prec = 1
                return self.actions[1]
            if (index >= id2 and index <id3 and self.perc_attuale[2] != 0): # è loc 2
                self.pos_prec = 2 
                return self.actions[2]
            if (index >= id3 and index <= id4 and self.perc_attuale[3] != 0): # è loc 3    
                self.pos_prec = 3
                return self.actions[3]

        def amici(neighbors): #verifico quale agente è più vicino e applico delle modifiche alle K e K2
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
                            #.img = 'maid' # aggiorno immagine
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

        def sporco():                        
            return 'Suck' # è sporco, pulisce
     
        def program(status, bump, neighbors): ##print("*******************")
            if self.passed == 0: # raggiungo lo stato terminale
                return"NoOp"

            if not neighbors: #  ho vicini ?
                amici(neighbors) # verifico e applico le K
            
           
            if bump == 'Bump':  # avviene il bump?
                return bumped()   
                      
            if status == 'Dirty':  # è sporco ?
                return sporco()
            else: 
                # se è pulito (!= 'Dirty')
                self.passed -=1
                return spostato()

        self.program = program

