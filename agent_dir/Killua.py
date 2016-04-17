from . agents import *
import random
from copy import copy
import pprint


class Cell(object):

    """Class describing a single cell of the grid/map"""

    def __init__(self, type_):
        """Initialize the cell type"""
        self.type_ = type_
        if self.type_ == "normal":
            self.actions = ['Suck', 'GoNorth', 'GoSouth', 'GoWest', 'GoEast']
        elif self.type_ == "wall":
            self.actions = None

    def is_wall(self):
        """Checks if the cell is a "wall" type"""
        return self.actions is None

    def del_action(self, action):
        """This function removes an action from self.actions (removes actions 
        from the cell itself)"""
        self.actions.remove(action)

    def choose_action(self):
        """Choose randomly the next action to do from the ones available in 
        this cell """
        if type(self.actions) == list and len(self.actions) > 0:
            return random.choice(self.actions)
        else:
            return False

    def __contains__(self, pos):
        """Overrides the in method"""
        if self.actions is not None:
            return pos in self.actions
        else:
            return False

    def __repr__(self):
        """Overrides the print method"""
        return pprint.pformat(self.actions)


class Grid(object):
    
    """This class represents the grid/map. 
    It is composed from Cell type objects"""

    def __init__(self):
        """Initialize the map (is a dictionary type) which at the starting point is empty"""
        self.grid = {}

    def add_cell(self, pos, type_="normal"):
        """If a cell has normal type (is not a wall) then it is being added 
        to the map with all the available actions"""
        if pos not in self.grid:
            self.grid[pos] = Cell(type_)

    def del_action(self, pos, action):
        """Deletes the action 'action' from the position 'pos'"""
        self.grid[pos].del_action(action)

    def choose_action(self, pos):
        """Returns the chosen action for the cell in position 'pos'"""
        return self.grid[pos].choose_action()

    def already_cleaned(self, pos):
        """Checks if the action Suck is still available in that cell.
        It is available if the cell wasn't already cleaned."""
        return "Suck" not in self.grid[pos]

    def get_actions(self, pos):
        """Returns the actions available in that cell position"""
        if pos in self.grid:
            return self.grid[pos]
        return []

    def relax(self):
        """For each cell X of the grid, removes from the nearby cells all
         the actions which allow turning back in X. Also it removes from X
         the actions that end up bumping into  wall."""
        for pos, cell in self.grid.items():
            x, y = pos
            if cell is not None:
                if (x, y+1) in self.grid:
                    if not self.grid[(x, y+1)].is_wall():
                        if "GoSouth" in self.grid[(x, y+1)]:
                            self.grid[(x, y+1)].del_action("GoSouth")
                    else:
                        if "GoNorth" in cell:
                            cell.del_action("GoNorth")
                if (x, y-1) in self.grid:
                    if not self.grid[(x, y-1)].is_wall():
                        if "GoNorth" in self.grid[(x, y-1)]:
                            self.grid[(x, y-1)].del_action("GoNorth")
                    else:
                        if "GoSouth" in cell:
                            cell.del_action("GoSouth")
                if (x+1, y) in self.grid:
                    if not self.grid[(x+1, y)].is_wall():
                        if "GoWest" in self.grid[(x+1, y)]:
                            self.grid[(x+1, y)].del_action("GoWest")
                    else:
                        if "GoEast" in cell:
                            cell.del_action("GoEast")
                if (x-1, y) in self.grid:
                    if not self.grid[(x-1, y)].is_wall():
                        if "GoEast" in self.grid[(x-1, y)]:
                            self.grid[(x-1, y)].del_action("GoEast")
                    else:
                        if "GoWest" in cell:
                            cell.del_action("GoWest")

    def __contains__(self, pos):
        """Overriding of the in method"""
        return pos in self.grid

    def __repr__(self):
        """Ovverriding of the print method"""
        return pprint.pformat(self.grid)


class KilluaClass(Agent):
    """My Agent Class"""

    def __init__(self, x=2, y=2):
        Agent.__init__(self)

        ##
        # Personalize the identifier of this class.
        # Will be used instead of the class name
        # in neighbours info

        self.name = 'Killua'
        self.img = 'Killua2'

        #dictionary for the opposite/reverse actions
        self.opposite = {
            'GoNorth': "GoSouth",
            'GoSouth': "GoNorth",
            'GoWest': "GoEast",
            'GoEast': "GoWest"
        }
        #self.steps keeps track of all the actions done (used later for the
        #backtracking)
        self.steps = []

        #my current position
        self.position = (0, 0)

        #id of the other agents located in my same position
        self.same_pos = []

        #the last performed action for the backtracking
        self.back_action = None

        #call the Grid() method to create the map
        self.grid = Grid()

        def program(status, bump, neighbors):

            #updating my position
            if len(self.steps) != 0:
                #if I am doing backtracking update my position based on the
                #back_action
                if self.back_action is not None:
                    if self.back_action == "GoNorth":
                        self.position = (
                            self.position[0], self.position[1] + 1)
                    elif self.back_action == "GoSouth":
                        self.position = (
                            self.position[0], self.position[1] - 1)
                    elif self.back_action == "GoEast":
                        self.position = (
                            self.position[0] + 1, self.position[1])
                    elif self.back_action == "GoWest":
                        self.position = (
                            self.position[0] - 1, self.position[1])
                    self.back_action = None
                else:
                    #otherwise take the last action performed from steps[]
                    last_action = self.steps[0]
                    #if is not a bump (meaning that I am moving)
                    # update my position
                    if bump != "Bump":
                        if last_action == "GoNorth":
                            self.position = (
                                self.position[0], self.position[1] + 1)
                        elif last_action == "GoSouth":
                            self.position = (
                                self.position[0], self.position[1] - 1)
                        elif last_action == "GoEast":
                            self.position = (
                                self.position[0] + 1, self.position[1])
                        elif last_action == "GoWest":
                            self.position = (
                                self.position[0] - 1, self.position[1])
                    #otherwise I bumped into a wall and I dont need to update 
                    #my position
                    #I remove the last performed action (because is useless)
                    #Adds on the map a cell having type=wall
                    
                    else:
                        if last_action == "GoNorth":
                            self.steps.pop(0)
                            self.grid.add_cell(
                                (self.position[0], self.position[1] + 1), "wall")
                        elif last_action == "GoSouth":
                            self.steps.pop(0)
                            self.grid.add_cell(
                                (self.position[0], self.position[1] - 1), "wall")
                        elif last_action == "GoEast":
                            self.steps.pop(0)
                            self.grid.add_cell(
                                (self.position[0] + 1, self.position[1]), "wall")
                        elif last_action == "GoWest":
                            self.steps.pop(0)
                            self.grid.add_cell(
                                (self.position[0] - 1, self.position[1]), "wall")

            #add a cell on the grid (if the cell is being visited for the first
            #time)
            
            if self.position not in self.grid:
                self.grid.add_cell(self.position)
                # If i arrived on this position by walking (not bumping)
                # I remove the reverse action
                # this way I cant go back
                if len(self.steps) != 0:
                    last_action = self.steps[0]
                    if last_action != "Suck":
                        self.grid.del_action(
                            self.position, self.opposite[last_action])

            #check if there are others agents on the same position as myself
            # if true, add only the agent id in same_pos
            for agent, pos in neighbors:
                if agent[0] != self.id:
                    tmp_pos = (
                        self.position[0]+pos[0], self.position[1]+pos[1])
                    if tmp_pos not in self.grid:
                        self.grid.add_cell(tmp_pos)
                        if self.position == tmp_pos:
                            self.same_pos.append(int(agent[0].split("_")[1]))

            
            #if there are other agents on the same position as myself
            if len(self.same_pos) > 0:
                tmp_my_id = int(self.id.split("_")[1])

                # I perform the Suck action only if I have the smallest id
                #faccio suck soltanto se il mio di e' il piu piccolo
                if tmp_my_id != min(self.same_pos + [tmp_my_id]):
                    self.grid.del_action(self.position, "Suck")

            #reset the agent id list
            self.same_pos = []

            #call the relax method
            self.grid.relax()


            #if I find dirty and it wasnt already cleaned then I clean
            #(decided by the agents on the same position as myself)
            if status == "Dirty" and not self.grid.already_cleaned(self.position):
                self.grid.del_action(self.position, "Suck")
                self.steps.insert(0, "Suck")
                return "Suck"
            #if the cell is given (at the starting point) as cleaned do nothing
            elif status == "Clean":
                if "Suck" in self.grid.get_actions(self.position):
                    self.grid.del_action(self.position,"Suck")


            #chose a new action to perform from those available on my cell
            new_action = self.grid.choose_action(self.position)

            #if there are no more available actions I start the backtracking
            if new_action == False:

                #I go back until I find a movement action (ignore Suck actions)
                #if I cant perform backtracking anymore it means that my search
                #is over
                if len(self.steps) > 0:
                    last_action = self.steps.pop(0)
                else:
                    return "NoOp"
                if last_action == "Suck":
                    while last_action == "Suck":
                        if len(self.steps) > 0:
                            last_action = self.steps.pop(0)
                        else:
                            return "NoOp"

                #update my back_action list and perform the reversed action
                #this way I go backwards
                self.back_action = self.opposite[last_action]
                return self.opposite[last_action]
                
            #if I an not doing backtracking I remove the action from the current
            #cell and I add the action in steps[]
            self.grid.del_action(self.position, new_action)
            self.steps.insert(0, new_action)


            #perform the chosen action
            return new_action

        self.program = program
