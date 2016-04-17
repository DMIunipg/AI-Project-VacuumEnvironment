AI-Project-VacuumEnvironment
============================

An environment to test a vacuum agent, created for the university project of Prof. Milani's Artificial Intelligence course at Department of Mathematics and Computer Science, University of Perugia, and inspired from a problem posed by Stuart Russell and Peter Norvig in the book "Artificial Intelligence: A Modern Approach".

## Dependencies

You must have [kivy](http://kivy.org/#home) installed on your system.

* [Download Kivy](https://kivy.org/#download)
* [Install Kivy on Windows](https://kivy.org/docs/installation/installation-windows.html)
* [Install kivy on Mac](https://kivy.org/docs/installation/installation-osx.html)

**Note**: that Kivy dependencies installation command for Windows installation (the one on the official guide page) can give problems: to solve, just put the two commands in a single line, deleting the separation backslash between the two, which is only for visualization purposes 

## Run the application

If you have installed all the dependencies, you can run the program with:
```bash
# To open the GUI with max 2 Agent (old program)
python aima-ui-2a.py

# To open the GUI with 4 Agent
python aima-ui-4a.py
```

## Add an Agent

You can write your own agent and add it to the environment. The procedure is simply, you have to follow these steps:

* Create a file in `agent_dir`, for example named `MyNewAgent.py`
* Add a class named like the file and ended with `Class`. In this example will be `MyNewAgentClass`
* Your class have to inherit from `Agent` class
* Insert your class in the list of imported module in `agent_dir/__init__.py`

Below we have an example `MyAgent.py` with some useful details:

```python
from . agents import *


class MyNewAgentClass(Agent):

    def __init__(self, x=2, y=2):
        Agent.__init__(self)

        ##
        # Personalize the identifier of this class.
        # Will be used instead of the class name
        # in neighbours info
        self.name = 'ExampleAgent'

        def program(status, bump, neighbors):
            """Main function of the Agent.

            Params:
                status (string): 'Dirty' or 'Clean'
                bump (string): 'Bump' or 'None'
                neighbors (list of tuples): [
                        ( (agent_id, agent_type), (r_x, r_y) ),
                        ...,
                        ...
                    ]

            Returns:
                 (string): one of these commands:
                            - 'Suck'
                            - 'GoNorth'
                            - 'GoSouth'
                            - 'GoWest'
                            - 'GoEast'
                            - 'NoOp' or 'Noop'

            """
            ##
            # id is assigned by the environment
            # in aima-ui-4a
            print(self.id)
            print(status, bump, neighbors)

            return 'NoOp'


        self.program = program

```

## Contributing

Contributions are welcome, so please feel free to fix bugs, improve things, provide documentation. 
For anything submit a personal message or fork the project to make a pull request and so on... thanks!

## Notes

This library is under development, so there may be substantial changes and improvements in the near future.

This project is based on [aima-python](https://code.google.com/p/aima-python/) for a course of artificial intelligence. In particular, these modules have been modified to meet the new specifications:

* Environment
* Agent
* utils

## Contributors

In this section will be mentioned all the people who have contributed to the creation of this program (the list will be in alphabetic order), divided by university department or private groups/people.

University of Perugia, Dept. of Maths and Computer Science: all the students for each year, contributing with their own agent and some personalized images for the agent graphics

AI 2013-2014, University of Perugia, Dept. of Maths and Computer Science: 
* Tracolli Mirco (student, first creation)
* Biondi Giulio (student)
* Parcus Robert (student)
* Franzoni Valentina (research assistant)
* Milani Alfredo (professor)

AI 2015-2016, University of Perugia, Dept. of Maths and Computer Science, AI 2013-2014: 
* Tracolli Mirco (graduating student)
* Franzoni Valentina (teacher assistant)
* Milani Alfredo (professor)


## Licenses
For text and images:
Creative Common BY-NC-SA: Share Alike, Non Commercial, give Attribution for the credits to the original authors: http://creativecommons.org/licenses/by-nc-sa/4.0/

For code:
Apache Licence 2.0
give attribution, free for any use, no responsability to the authors (AS IS) 
http://www.apache.org/licenses/
also see the LICENCE file
