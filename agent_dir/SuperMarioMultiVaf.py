from . agents import *
import random
from math import sqrt
CELL_TAG = 0
CELL_ACT = 1

def t_sum(left,right):
    return (left[0]+right[0],left[1]+right[1])

def t_dif(left,right):
    return (left[0]-right[0],left[1]-right[1])

def t_dist(left,right):
    return sqrt( (left[0]-right[0])**2 + (left[1]-right[1])**2 )

def t_manhattan_dist(left,right):
    return abs(left[0]-right[0]) + abs(left[1]-right[1])

#inizialliza a infinito
def get_inf():
    try:
        inf = float('inf')
    except:  # check for a particular exception here?
        inf = 1e30000
    return inf


class SuperMarioMultiVafClass(Agent):

    def wall_cell(self):
        # add info into context
        if not (self.pos in self.context):
            self.context[ self.pos ] = ( 'wall', [] )

    def update_cell(self):
        # add info into context
        if not (self.pos in self.context):
            self.context[ self.pos ] = ( 'cell', [ 'Suck', 'GoNorth', 'GoSouth' , 'GoWest', 'GoEast' ] )

    def update_cell_neighbors(self,n_pos):
        # add info into context
        if not (n_pos in self.context):
            self.context[ n_pos ] =  ( 'cell', [ 'GoNorth', 'GoSouth' , 'GoWest', 'GoEast' ] )
            #self.context[ n_pos ] =  ( 'cell', [ ] )
        else:
            try:
                self.context[ n_pos ][CELL_ACT].remove('Suck')
            except ValueError:
                pass

    def pop_an_action_2(self):
        try:
            while True:
                action = self.context[self.pos][CELL_ACT].pop()
                n_pos  = self.get_next_pos(action)
                if not n_pos in self.context:
                    return action
                elif 'Suck' in self.context[n_pos][CELL_ACT]:
                    return action
        except IndexError:
            pass
        return None

    

    def find_nearest_cell_with_actions(self):
        #init valore di ritorno
        pos_dist = None
        #cerco la pos con la dist minima tra le celle
        for pos, (tag,actions) in self.context.items():
            #se e' cella...
            if tag == 'cell':
                #ed ha azioni
                if len(actions) > 0:
                    #ed pos_dist non e' inizializzato (caso 1)
                    if pos_dist == None:
                        #pos_dis prende la distanza e la pos della cella
                        pos_dist = ( pos, t_manhattan_dist(self.pos,pos) )
                    else:
                        new_pos_dis = ( pos, t_manhattan_dist(self.pos,pos) )
                        pos_dist = min( ( pos_dist, new_pos_dis ) , key = lambda x : x[1] )
        #se e' None return None altrimenti ritorna solo pos di pos_dis
        if pos_dist == None:
            return None
        else:
            return pos_dist[0]

   
    def get_cell_neighbors(self,pos):
        output = []
        if pos in self.context:
            list_n_pos = [ t_sum(pos,( 1, 0)),
                           t_sum(pos,(-1, 0)),
                           t_sum(pos,( 0, 1)),
                           t_sum(pos,( 0,-1)) ]
            for n_pos in list_n_pos:
                if n_pos in self.context: 
                    if self.context[ n_pos ][ CELL_TAG ] == 'cell':
                        output.append(n_pos)
        return output

    def dijkstra_dist(self, pos):
        D = {}
        Q = {}
        P = {}
        #init this
        D[ pos ] = 0
        #init all
        for value in self.context.items():
            if value[1][ CELL_TAG ] == 'cell':
                if value[0] != pos:
                    D[value[0]] = get_inf()
                    P[value[0]] = None
                Q[value[0]] = D[value[0]]

        while len(Q):
            #get min
            u_dist = min(Q.items(),key=lambda val:val[1])
            #take pos
            u = u_dist[0]
            #pop from Q
            Q.pop(u)
            #for all
            for n in self.get_cell_neighbors(u):
                alt = D[u]+t_manhattan_dist(u,n)
                if alt < D[n]:
                    D[n] = alt
                    P[n] = u
                    Q[n] = D[n]
        return (D,P)

    def search_path(self,pos,target):
        D,P = self.dijkstra_dist(self.pos)
        S = []
        u = target
        while u in P and P[u] != None:
            S.insert(0,u);
            u = P[u]
        S.insert(0,u);
        return S

    def get_name_direction(self,direction):
        if direction == ( 1, 0):
            return 'GoEast'
        if direction == (-1, 0):
            return 'GoWest'
        if direction == ( 0, 1):
            return 'GoNorth'
        if direction == ( 0,-1):
            return 'GoSouth'
        raise Exception("Invalid dir"+str(direction))

    def next_pos_of_path(self):
        if len(self.path) >= 2:
            pos = self.path.pop(0)
            target = self.path[0]
            direction = t_dif(target,pos)
            print( pos, target, self.get_name_direction(direction), direction)
            return self.get_name_direction(direction)
        self.path = None
        return 'NoOp'

   
    def no_more_suck(self):
        for value in self.context.items():
            if value[CELL_TAG] == 'cell':
                if 'Suck' in value[CELL_ACT]:
                    return True
        return False

    def remove_action(self,action):
        if action in self.context[ self.pos ][CELL_ACT] :
            try:
                self.context[ self.pos ][CELL_ACT].remove(action)
            except ValueError:
                pass
            return True
        return False    

    def get_next_pos(self,action):
        pos = self.pos
        if action == 'GoEast':
            pos = t_sum(pos,(1,0))
        elif action == 'GoWest':
            pos = t_sum(pos,(-1,0))
        elif action == 'GoNorth':
            pos = t_sum(pos,(0,1))
        elif action == 'GoSouth':
            pos = t_sum(pos,(0,-1))
        return pos

    def update_pos(self,action):
        #update action
        if action == 'GoEast':
            self.pos = t_sum(self.pos,(1,0))
        elif action == 'GoWest':
            self.pos = t_sum(self.pos,(-1,0))
        elif action == 'GoNorth':
            self.pos = t_sum(self.pos,(0,1))
        elif action == 'GoSouth':
            self.pos = t_sum(self.pos,(0,-1))
        else:
            return action
        #un azione mi costa
        self.cost -= 6
        #return
        return action

    def __init__(self, x=2, y=2):
        Agent.__init__(self)

        ##
        # Personalize the identifier of this class.
        # Will be used instead of the class name
        # in neighbours info
        self.name = 'SuperMarioMultiVaf'
        self.curr = 'GoEast'
        self.img = 'mario'
        self.walls = []
        self.pos = (0, 0)
        self.pos_old = (0, 0)
        self.actions = ['GoEast', 'GoWest', 'GoNorth', 'GoSouth']
        self.context = {}
        self.path = None
        self.cost = 100 #come se avessi fatto 1 Suck

        def program(status, bump, neighbors):

            ## Walls
            if bump == 'Bump':
                #Annullo parzialmente il costo della precedente azione
                self.cost += 3
                #qui c'e' un muro
                self.wall_cell()
                #in realta' il robot e' rimasto dove era -> quindi la posizione relativa e' quella vecchia
                self.pos = self.pos_old

            ##
            # Update context about positions of neighbors
            for (n_agent_id, n_agent_class), n_pos in neighbors:
                if n_agent_id != self.id:
                    self.update_cell_neighbors(t_sum(self.pos,n_pos))

            #aggiungo cella
            self.update_cell()

            #azione pulisci
            if status == "Dirty":
                self.path = None
                self.cost = 100
                self.remove_action('Suck')
                return 'Suck'

            if status == 'Clean' and self.cost > 0:
                #per sicurezza tolgo succhia [celle pulite all'inizio]
                self.remove_action('Suck')
                #dammi una azione
                action = self.pop_an_action_2()
                #azione
                if action == None:
                    if self.no_more_suck():
                        return 'NoOp'
                    #find best path
                    target = self.find_nearest_cell_with_actions()
                    #cases
                    if target == None:
                        return 'NoOp'
                    else:
                        self.path = self.search_path(self.pos,target)
                    #compute actions from path
                    return self.update_pos(self.next_pos_of_path())
                #not path to fw.
                self.path = None
                #save last pos
                self.pos_old = self.pos
                #compute next pos
                self.update_pos(action)

                return action
            else:
                return 'NoOp'


        self.program = program
