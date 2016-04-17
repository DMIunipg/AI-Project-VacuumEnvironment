from . agents import *

class ParProCMClass(Agent):

    def __init__(self):
        Agent.__init__(self)

        ##
        # Personalize the identifier of this class.
        # Will be used instead of the class name
        # in neighbours info
        self.img = 'dart_vender'                                    #viene impostata una immagine per vacuum cleaner
        self.name = 'ParProAgentCM'                                 #viene impostato il nome
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']               #lista delle possibili mosse
        self.coord = (0, 0)                                     #coordinata iniziale dell'agente
        self.curr = 'Inizio'                                    #viene impostata la mossa iniziale
        self.visited = []                                   #viene creata una lista delle celle visitare (vengono salvate le coppie)
        self.path = ["Inizio"]                                  #viene creata una lista per salvare il percorso fatto (lista delle azioni nel path)
        self.act = ""                                       #variabile necessaria per il salvataggio dell'azione corrente (Move,Back)
        self.team = ""                                      #variabile necessaria per registrare l'ID del compagno
        self.ultimoSpostamento = ""                                 #variabile utile per determinare eventuali bump consecutivi
        self.posizioneGiusta = 2                                #permette di recuperare la giusta coordinata nella quale ci si trova dopo dei bump



#--------------------------------------------------------------------------------------------------------------------
#funzione che informa l'agente se pulire la casella in cui si sovrappongono o passare alla casella successiva


        def pulisceSeSovrapposti(neighbors):
            pulisci = True
            for (agent_id, agent_class), pos in neighbors:                  #cicla per tutti i neighbors
                if pos == (0, 0):                           #se la posizione relativa e' (0, 0) allora sono sovrapposti
                    if self.id > agent_id:                      #se il nostro agente ha un ID maggiore, rispetto a quello dell'altro agente                                                     #sovrapposto, non fara' Suck e passa alla mossa successiva(Non perde 20 punti per                                                   #succhiare dove e' gia stato pulito dal quello con ID minore)
                        pulisci = False
            return pulisci



#--------------------------------------------------------------------------------------------------------------------
#funzione che permette di recuperare eventuali agenti appartenenti allo stesso Team (agent_class)


        def trovaTeam(neighbors):
            for (agent_id, agent_class), pos in neighbors:
                if (agent_id != self.id) and (agent_class == "ParProAgentCM"):      #se l'agente e' del nostro team e non siamo noi stessi
                    self.team = agent_id                        #viene salvato l'ID dell'agente nel team




#--------------------------------------------------------------------------------------------------------------------
#funzione che permette di salvare le coordinate della mappa nelle quali e' passato l'agente del nostro team, questo ci permette di evitare il passaggio su celle gia' visitate


        def inserisciPosizioneVicini(neighbors):
            for (agent_id, agent_class), pos in neighbors:
                if agent_id == self.team:                       #se l'agente e' nel mio team
                    posizioneAssoluta = (pos[0]+self.coord[0],pos[1]+self.coord[1]) #salvo la posizione assoluta sommando la propria posizione con quella relativa                                                  #all'agente nel team
                    self.visited.insert(0,posizioneAssoluta)    
    


#--------------------------------------------------------------------------------------------------------------------   
#funzione che estrae l'ultimo spostamento eseguito nel percorso (DFS), con il quale si seleziona la direzione opposta per tornare indietro dalla visita in profondita
        

        def indiceTornaIndietro():
            direzione = self.path.pop()                         #estrazione dell'ultima mossa del path
                
            #viene ritornata la mossa opposta
            if direzione == "Inizio":
                return 4
            if direzione == "GoEast":
                return 1
            if direzione == "GoWest":
                return 0
            if direzione == "GoNorth":
                return 3
            if direzione == "GoSouth":
                return 2



#--------------------------------------------------------------------------------------------------------------------
#funzione che ritorna le coordinate aggiornate in base alla mossa selezionata


        def findCoord(coord, move):
            if move == 0:
                return (coord[0]+1,coord[1])
            elif move == 1:
                return (coord[0]-1,coord[1])
            elif move == 2:
                return (coord[0],coord[1]+1)
            elif move == 3:
                return (coord[0],coord[1]-1)    



#--------------------------------------------------------------------------------------------------------------------
#funzione che seleziona la mossa o l'azione successiva



        def nextMove(act,neighbors):

            trovaTeam(neighbors)                                #recupera eventuali agenti nel proprio team e li salva in self.team
            
            self.visited.append(self.coord)                         #vengono salvate le coordinate nelle quali si passa

            if act == "Move":                               #se l'azione e' quella di muoversi
                self.path.append(self.curr)                         #viene salvata la mossa per la costruzione del percorso di visita
        
            if act == "Bump":                               #se l'azione e' Bump viene riaggiornata la posizione corretta nella quale si trova                                                  #l'agente
                #riassegna la coordinata corretta, considerando il numero di bump avvenuti 
                self.coord = self.visited[len(self.visited) - self.posizioneGiusta]

            
            inserisciPosizioneVicini(neighbors)                         #salva le posizioni dell'agente nel nostro team 
        

            #ogni agente esegue il proprio codice per modificare l'ordine delle mosse in modo diverso dall'altro
            if self.id < self.team:                             #se questo agente ha l'ID minore di quello del proprio team eseque questo
                index = 0                               #mossa iniziale GoEast
                controlla = True
                self.act = "Move"
                while (controlla == True):
                    if findCoord(self.coord, index) not in self.visited:        #se la coordinata e' disponibile
                        controlla = False                   #esco e ritorno la mossa selezionata
                    else:                               #altrimenti
                        index += 1                      #ciclo sulle altre 3 mosse rimaste in avanti
                        if index == 4:                      #se sono in un vicolo cieco, nessuna mossa possibile 
                            index = indiceTornaIndietro()           #recupero la mossa per tornare indietro
                            self.act = "Back"               #imposto come azione Back per differenzoare da Move
                            controlla = False
            


            if self.id > self.team: #se questo agente ha l'ID maggiore di quello del proprio team eseque questo
                index = 3                               #mossa iniziale GoSouth
                controlla = True
                self.act = "Move"
                while (controlla == True):
                    if findCoord(self.coord, index) not in self.visited:
                        controlla = False
                    else:
                        index -= 1                      #ciclo sulle altre 3 mosse rimaste procedendo nell'ordine inverso
                        if index == -1:                     #se sono in un vicolo cieco, nessuna mossa possibile
                            index = indiceTornaIndietro()
                            self.act = "Back"
                            controlla = False


            if index == 4: #se index ritorna 4 significa che e' stato estratta dal path la mossa 'Inizio' che comunica la fine della visita, percio' viene riportato il NoOp
                return "NoOp"
            else:
                return self.actions[index]                      #ritorna la mossa successiva




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



#--------------------------------------------------------------------------------------------------------------------
#funzione generale



        def program(status, bump, neighbors):

            if self.ultimoSpostamento != "Bump":                        #se non e' stato ancora rilevato un Bump
                if bump == "Bump":                          #e siamo andati addosso ad un muro
                    self.ultimoSpostamento = "Bump"                 #aggiorno la variabile
            else:                                       #se la mossa precedente aveva sbattuto su un muro
                if bump != "Bump":                          #ma quella attuale no
                    self.ultimoSpostamento = ""                     #resetto la variabile ultimoSpostamento
                    self.posizioneGiusta = 2                    #e la posizione corretta in cui si trova l'agente
                else:                                   #se anche la nuova mossa e' un muro 
                    self.posizioneGiusta +=1                    #aggiusto la posizione corretta
            


            if self.curr != 'NoOp':                             #se l'azione e' diversa da NoOp

                if bump == 'Bump':                          #se l'agente ha sbattuto sul muro

                    self.curr = nextMove("Bump",neighbors)              #seleziona la mossa successiva

                    changeCoords()                          #in base alla mossa cambia le coordinate

                    return self.curr

                if status == 'Dirty':                           #se la cella e' sporca
            
                    if pulisceSeSovrapposti(neighbors) == False:            #se il nostro agente e' sovrapposto ma ha ID minore passa alla mossa successiva                                                 #senza succhiare quella cella che e' gia' pulita da quello con ID minore

                        self.curr = nextMove(self.act,neighbors)
                        
                        changeCoords()
                    
                        return self.curr

                    else:                               #altrimenti succhia
                        return 'Suck'

                else:                                   #se la cella e' pulita
                    
                    self.curr = nextMove(self.act,neighbors)

                    changeCoords()
                    
                    return self.curr

            else:
                return self.curr

        self.program = program
