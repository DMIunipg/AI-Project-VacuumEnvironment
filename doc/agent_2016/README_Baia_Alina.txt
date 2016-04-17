Welcome to MultiVA Environment
HunterXHunter Class Edition
-------------------------------------------------------
Multi Vacuumcleaner Agent with Constant memory

 -------------------------------------
 #do this in the __init__.py file
 from . Alluka import AllukaClass
 -------------------------------------
 ==Description==

 The first agent (AllukaClass - Alluka = an anime character 
 with double personality :a good one and a bad one. The good 
 side of Alluka can perform miracles meanwhile her bad side 
 can kill several people in one shot. When dealing wiht Alluka 
 you must be lucky) is based on a weight-random
 approach. When an action A is chosen from the list of all
 actions with the random.choice function, we add in the 
 list of actions the reverse action of A with the intent
 of reducing the chances of going backwards.
 When multiple agent are exploring the map we use the ratio
 variable to try to maintain a safe distance from the others
 agents. Doing so we hope to avoid going into already
 cleaned zones.
-------------------------------------------------------
Multi Vacuumcleaner Agent with Free memory

 -------------------------------------
 #do this in the __init__.py file
 from . Killua import KilluaClass
 -------------------------------------

 ==Description==

 The second agent (KilluaClass - Killua =  an anime character 
 trained as an assasin (hunting people) since his early age)
 is based on the DFS algorithm.

 The agent peforms a DFS exploration with backtracking. Every 
 step of the exploration, the agent verifies if the current cell
 has been added to the grid and if there are still available 
 actions. If the cell was already added to the grid it means that
 is was already visited and it will change the type into a wall
 (removing also all the actions available on that particular cell).
 This way we avoid unnecessary (future) exploration on that cell.
 Using multiple agent to explore the map we guarantee that every
 agent will have his "hunting zone" and no other agents will
 be able to go over an already explored/cleaned zone.

