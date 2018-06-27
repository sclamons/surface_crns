from event import Event
import numpy as np
from ..models.simulation_grid import SimulationGrid

class RotoRouterSimulator:
    '''
    Deterministic roto-router simulator. Runs with the following rules:
        0) Initialize to a grid of arrows pointing up.
        1) Drop a token at the start position
        2) Move the token in the direction of the arrow at its position and 
            rotate the source's arrow counterclockwise by 90 degrees.
        3) Repeat 2 until the token falls off.
        4) Repeat 1-3 as long as you want.
    '''
    def __init__(self, grid_size = 15, start_x = None, start_y = None, 
                 simulation_duration = 100):
        self.debugging = False
        self.simulation_duration = simulation_duration
        self.start_x = start_x
        self.start_y = start_y
        self.time = 0

        self.surface = SimulationGrid(grid_size, grid_size)
        for node in self.surface:
            node.state = "^"
        if start_x == None:
            self.start_x = self.surface.x_size / 2
            self.start_y = self.surface.y_size / 2
        self.drop_token()

    def reset(self):
        '''
        Start the simulation from the initial condition
        '''
        for node in self.surface:
            node.state = "^"
        self.drop_token()
        self.time = 0

    def drop_token(self):
        self.token_x = self.start_x
        self.token_y = self.start_y
        self.surface.getnode(self.token_x, self.token_y).state += '*'

    def done(self):
        return self.time >= self.simulation_duration

    def process_next_reaction(self):
        current_token_x = self.token_x
        current_token_y = self.token_y
        current_node = self.surface.getnode(current_token_x, current_token_y)
        if current_node.state == "^*":
            current_node.state = ">"
            self.token_y -= 1
        elif current_node.state == ">*":
            current_node.state = "V"
            self.token_x += 1
        elif current_node.state == "V*":
            current_node.state = "<"
            self.token_y += 1
        elif current_node.state =="<*":
            current_node.state = "^"
            self.token_x -= 1
        else:
            raise Exception("Invalid state at token location: " + 
                            current_node.state)

        if self.token_y < 0 or self.token_y >= self.surface.y_size or \
           self.token_x < 0 or self.token_x >= self.surface.x_size:
            self.drop_token()
        else:
            self.surface.getnode(self.token_x, self.token_y).state += "*"

        self.time += 1

        return Event(time = self.time-1,
                     rule = None,
                     participants = [current_node, 
                                     self.surface.getnode(self.token_x, 
                                                          self.token_y)
                                    ],
                     time_issued = self.time-2)