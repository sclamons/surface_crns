class Node:
    '''
    Represents a spatial location. Has a chemical state represented by a 
    string, a list of neighbors, and a timestamp of the last update.
    '''
    def __init__(self, state = None, neighbors = None, timestamp = 0,\
                 position = None):
        if state == None:
            state = ""
        if neighbors == None:
            neighbors = []
        self.state = state
        if not isinstance(neighbors, list):
            self.neighbors = [neighbors]
        else:
            self.neighbors = neighbors
        self.timestamp = timestamp
        if position == None:
            position = ()
        self.position = position

    def __str__(self):
        str_rep = "<State: " + self.state + " (updated at time " + \
            str(self.timestamp) + ")"
        if len(self.neighbors) > 0:
            str_rep += "; neighbor states: "
            str_rep += self.neighbors[0].state
            for i in range(1, len(self.neighbors)):
                str_rep += ", " + self.neighbors[i].state
        else:
            str_rep += "; No neighbors"
        if self.position != ():
            str_rep += "; Position: " + str(self.position)
        str_rep += ">"
        return str_rep

    def __repr__(self):
        return str(self)
#end class Node
