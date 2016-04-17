from . agents import *
import random
from copy import copy


class AllukaClass(Agent):

    def __init__(self, x=2, y=2):
        Agent.__init__(self)

        ##
        # Personalize the identifier of this class.
        # Will be used instead of the class name
        # in neighbours info
        self.name = 'Alluka'
        self.img = 'Alluka'
        # variable that keeps track of the cleanliness of the zone around the
        # agent
        self.cleaning = None

        # the actions an agent can perform
        self.actions = ['GoNorth', 'GoSouth', 'GoWest', 'GoEast']

        # dictionary with the reversed actions
        self.opposite = {
            'GoNorth': "GoSouth",
            'GoSouth': "GoNorth",
            'GoWest': "GoEast",
            'GoEast': "GoWest"
        }
        # keeping track of the last actions performed by my agent
        self.last_actions = []

        # keeping track of the last actions performed by the others agents
        self.last_agent_actions = {}

        #variables that help me "guessing" how clean is a zone around my agent
        self.num_clean = 0
        self.num_dirty = 0

        # evaluate the ratio between dirty and clean.
        def ratio():
            if self.num_clean > 0:
                return float(self.num_dirty / self.num_clean)
            return float(self.num_dirty / 1.0)

        # update the last action for each agent different my agent ,
        # if the list do not exists add an empty list,
        # then if list lenght is 2 delete the oldest action and add the new one
        # if is empty or less then 2 add the action of that agent
        def add_neighbors_actions(neighbors):
            for agent, pos in neighbors:
                if agent[0] != self.id:
                    if agent not in self.last_agent_actions:
                        self.last_agent_actions[agent] = []

                    if len(self.last_agent_actions[agent]) == 2:
                        self.last_agent_actions[agent].pop()

                    self.last_agent_actions[agent].insert(0, pos)
        # adding the last action performed by my agent
        def add_last_action(action):
            if len(self.last_actions) == 2:
                self.last_actions.pop()

            self.last_actions.insert(0, action)

        # calculate the next action    

        def next_action(bump=False):
            action_list = copy(self.actions)
            #if I go into a bump I increase the possibility of going
            # into the opposing direction
            # and I delete the action which took me into the wall
            if bump:
                action_list.append(self.opposite[self.last_actions[0]])
                action_list.remove(self.last_actions[0])

            for action in self.actions:
                if action not in self.last_actions:
                    action_list.append(self.opposite[action])
            #i try to maintain a distance from the agent which are into a 
            #cleaned zone
            if ratio() < 0.33:
                for list_pos in self.last_agent_actions.values():
                    for x, y in list_pos:
                        if x > 0:
                            action_list.append("GoWest")
                        elif x < 0:
                            action_list.append("GoEast")
                        if y < 0:
                            action_list.append("GoNorth")
                        elif y > 0:
                            action_list.append("GoSouth")

            #choose the next action to perform
            new_action = random.choice(action_list)
            #update the list of last actions with my next move
            add_last_action(new_action)

            return new_action

        def program(status, bump, neighbors):

            #update the last actions of my neighbors
          
            add_neighbors_actions(neighbors)
            #cleaning receives a value based on the distance
            #from my agent's farther neighbor
            if self.cleaning is None:
                if len(neighbors) > 1:
                    self.cleaning = (0, 0)
                    for agent, pos in neighbors:
                        self.cleaning = max(
                            self.cleaning, (abs(pos[0]), abs(pos[1])))
                    self.cleaning = self.cleaning[0] * self.cleaning[1]
                else:
                    self.cleaning = 0

            if status == "Dirty":
                self.num_dirty += 1
                self.cleaning += 5
                add_last_action("Suck")
                return "Suck"
            elif bump == "Bump":
                return next_action(bump=True)
            elif status == "Clean":
                if len(self.last_actions) > 0 and self.last_actions[0] != "Suck":
                    self.num_clean += 1
                self.cleaning -= 1

            if self.cleaning < 0:
                return "NoOp"

            return next_action()

        self.program = program
