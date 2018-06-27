from ..base import *
import pygame
'''
Classes for creating and updating pygame surfaces based on simulation data.
'''

class SquareGridDisplay(object):
    debug = False
    '''
    Displays a SquareGrid object as a colored grid.
    '''

    def __init__(self, grid, colormap, min_x = 0, min_y = 0, pixels_per_node=5,
                 display_text = False, display_lines = False):
        '''
         Parameters:
            grid: The SquareGrid object displayed
            colormap: Dictionary defining what colors are assigned to each state
            min_x, min_y: Minimum x and y sizes, in pixels, of the surface
                            created. If the natural size of the grid isn't big
                            enough, the grid will be centered and whitespace
                            will be added to fill the excess.
            pixels_per_node: Width and height of each node, in pixels, either as
                                a pair of integers (for arbitrary form factors)
                                or as a single integer (for square nodes)
            display_text: If True, will display each node with a text overlay of
                            that node's state. Otherwise, will only display the
                            color of the node.
            display_lines
        '''

        # Constants
        self.grid_buffer = 5

        # Argument inits
        self.grid = grid
        self.colormap = colormap
        self.min_x = min_x
        self.min_y = min_y
        self.pixels_per_node = pixels_per_node

        self.display_text = display_text

        self.recalculate_display_sizes()


    def recalculate_display_sizes(self):
        # Calculate some internal variables
        self.display_width  = max((2 * self.grid_buffer +
                          self.grid.x_size * self.node_width), self.min_x)
        self.display_height = max((2 * self.grid_buffer +
                          self.grid.y_size * self.node_height), self.min_y)

    def pixels_per_node():
        doc = "The number of pixels used to display a single node in the grid."
        def fget(self):
            return (self.node_width, self.node_height)
        def fset(self, value):
            if isinstance(value, int):
                self.node_width = value
                self.node_height = value
            elif (isinstance(value, list) or isinstance(value, tuple)) and \
                 len(value) == 2:
                self.node_width = value[0]
                self.node_height = value[1]
            else:
                raise Exception("Invalid argument for pixels_per_node: " +
                                str(value))
            self.recalculate_display_sizes()
        def fdel(self):
            del self.node_width
            del self.node_height
        return locals()
    pixels_per_node = property(**pixels_per_node())

    def render(self, parent_surface, x_pos = 0, y_pos = 0):
        debug = False
        '''
        Set up the display and make the first render. This must be called before
        any other updates.
            parent_surface: The surface onto which this grid will be displayed.
            x_p os, y_pos: X and Y coordinates of the upper-left corner of this
                            grid relative to parent_surface.
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos
        # Create display surface
        if debug:
            print("Displaying grid display at position (" + str(x_pos) + "," +
                  str(y_pos) + ") with width " + str(self.display_width) +
                  " and height " + str(self.display_height) + ".")
        self.parent_surface = parent_surface
        self.display_surface = parent_surface.subsurface(
                        (x_pos, y_pos, self.display_width, self.display_height))
        # Initial render
        for x in range(self.grid.x_size):
            for y in range(self.grid.y_size):
                self.update_node_at_position(x, y)

    def update_node_at_position(self, x, y):
        self.update_node(self.grid.getnode(x,y))

    def update_node(self, node):
        '''
        Redraw a specified node.
        '''
        new_rect   = self.make_node_rectangle(node)
        node_color = self.colormap[node.state]
        pygame.draw.rect(self.display_surface, node_color, new_rect)
        if self.display_text:
            node_text_surface = self.make_node_text(node)
            text_rect = node_text_surface.get_rect()
            text_rect.center = new_rect.center
            self.display_surface.blit(node_text_surface,
                                      text_rect)

    def make_node_rectangle(self, node):
        debug = False

        x = node.position[0]
        y = node.position[1]
        if self.grid.x_size * self.node_width < self.min_x:
            x_buffer = (self.min_x - self.grid.x_size*self.node_width)/2
            x_pos    = x_buffer + x * self.node_width
        else:
            x_pos    = self.grid_buffer + x * self.node_width
        if self.grid.y_size * self.node_height < self.min_y:
            y_buffer = (self.min_y - self.grid.y_size*self.node_height)/2
            y_pos    = y_buffer + y * self.node_height
        else:
            y_pos    = self.grid_buffer + y * self.node_height
        if debug:
            print("Creating new rectangle with position (" + str(x_pos) + "," +
                  str(y_pos) + "), height " + str(self.node_height) +
                  ", and width " + str(self.node_width) + ".")
        return pygame.Rect(x_pos, y_pos, self.node_width, self.node_height)

    def make_node_text(self, node):
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        node_color = self.colormap[node.state]
        if sum(node_color) < 150:
            text_color = WHITE
        else:
            text_color = BLACK
        font = pygame.font.SysFont('monospace', 10)
        text_surface = font.render(node.state, True, text_color)
        return text_surface

#end class SquareGridDisplay





class ParallelEmulatedSquareGridDisplay(object):
    debug = False
    '''
    Displays an underlying grid and the grid it emulates (i.e., the underlying
    process of a game of life automaton and the automoton it emulates)
    side-by-side.

    Assumes that each emulated cell is determined by the value of a fixed
    position in the underlying grid; that the first character of the
    representative cell's state gives the emulated cell's state; and that the
    emulated cell's state is constant until the representative cell gains a
    new state beginning with anything other than "B".
    '''

    def __init__(self, grid, colormap, emulation_colormap, horizontal_buffer,
                 vertical_buffer, cell_height, cell_width,
                 representative_cell_x, representative_cell_y, min_x = 0,
                 min_y = 0, pixels_per_node=5, display_text = False,
                 display_lines = False):
        '''
         Parameters:
            grid: The SquareGrid object displayed
            colormap: Dictionary defining what colors are assigned to each state
            emulation_colormap: Same as colormap, but for the emulated grid.
            horizontal_buffer, vertical_buffer:
                        The number of underlying grid nodes on the left/right
                        and top/bottom of the underlying grid that aren't
                        included in the emulation (boundary conditions)
            cell_width, cell_height: The number of underlying grid nodes
                                        in an emulated node in each direction.
            representative_cell_x, representative_cell_y:
                        The location, within each emulated cell, of the
                        underlying grid cell containing information about the
                        emulated cell.
            min_x, min_y: Minimum x and y sizes, in pixels, of the surface
                            created. If the natural size of the grid isn't big
                            enough, the grid will be centered and whitespace
                            will be added to fill the excess.
            pixels_per_node: Width and height of each node, in pixels, either as
                                a pair of integers (for arbitrary form factors)
                                or as a single integer (for square nodes)
            display_text: If True, will display each node with a text overlay of
                            that node's state. Otherwise, will only display the
                            color of the node.
        '''
        pygame.init()

        # Constants
        self.grid_buffer = 5


        # Argument inits
        self.grid = grid
        self.horizontal_buffer = horizontal_buffer
        self.vertical_buffer = vertical_buffer
        self.emulated_cell_height = cell_height
        self.emulated_cell_width = cell_width
        self.representative_cell_x = representative_cell_x
        self.representative_cell_y = representative_cell_y
        self.emulation_colormap = emulation_colormap
        self.colormap = colormap
        self.min_x = min_x
        self.min_y = min_y
        self.pixels_per_node = pixels_per_node

        self.display_text = display_text

        self.recalculate_display_sizes()


    def recalculate_display_sizes(self):
        # Calculate some internal variables
        self.display_width  = max((self.grid_buffer +
                                  2 * self.grid.x_size * self.node_width ),
                                 self.min_x)
        self.display_height = max((2 * self.grid_buffer +
                          self.grid.y_size * self.node_height), self.min_y)

    def pixels_per_node():
        doc = "The number of pixels used to display a single node in the grid."
        def fget(self):
            return (self.node_width, self.node_height)
        def fset(self, value):
            if isinstance(value, int):
                self.node_width = value
                self.node_height = value
            elif (isinstance(value, list) or isinstance(value, tuple)) and \
                 len(value) == 2:
                self.node_width = value[0]
                self.node_height = value[1]
            else:
                raise Exception("Invalid argument for pixels_per_node: " +
                                str(value))
            self.recalculate_display_sizes()
        def fdel(self):
            del self.node_width
            del self.node_height
        return locals()
    pixels_per_node = property(**pixels_per_node())

    def render(self, parent_surface, x_pos = 0, y_pos = 0):
        debug = False
        '''
        Set up the display and make the first render. This must be called before
        any other updates.
            parent_surface: The surface onto which this grid will be displayed.
            x_p os, y_pos: X and Y coordinates of the upper-left corner of this
                            grid relative to parent_surface.
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos
        # Create display surface
        if debug:
            print("Displaying grid display at position (" + str(x_pos) + "," +
                  str(y_pos) + ") with width " + str(self.display_width) +
                  " and height " + str(self.display_height) + ".")
        self.parent_surface = parent_surface
        self.display_surface = parent_surface.subsurface(
                        (x_pos, y_pos, self.display_width, self.display_height))
        # Initial render
        for x in range(self.grid.x_size):
            for y in range(self.grid.y_size):
                self.update_node_at_position(x, y)

    def update_node_at_position(self, x, y):
        self.update_node(self.grid.getnode(x,y))

    def update_node(self, node):
        '''
        Redraw a specified node, and its emulated node if that emulated node
        changed state
        '''
        new_rect   = self.make_node_rectangle(node)
        node_color = self.colormap[node.state]
        pygame.draw.rect(self.display_surface, node_color, new_rect)
        if self.display_text:
            node_text_surface = self.make_node_text(node)
            text_rect = node_text_surface.get_rect()
            text_rect.center = new_rect.center
            self.display_surface.blit(node_text_surface,
                                      text_rect)

        # Update the emulated node if necessary
        x = (node.position[0]-self.horizontal_buffer) % self.emulated_cell_width
        y = (node.position[1]-self.vertical_buffer) % self.emulated_cell_height
        if x == self.representative_cell_x and y == self.representative_cell_y:
            represented_x = (node.position[0]-self.horizontal_buffer)          \
                            / self.emulated_cell_width
            represented_y = (node.position[1]-self.vertical_buffer)            \
                            / self.emulated_cell_height
            new_rect = self.make_emulated_node_rectangle(represented_x,
                                                          represented_y,
                                                          node.state[0])
            if node.state[0] in self.emulation_colormap:
                node_color = self.emulation_colormap[node.state[0]]
            else:
                node_color = self.emulation_colormap['B']
            pygame.draw.rect(self.display_surface, node_color, new_rect)

    def make_node_rectangle(self, node):
        debug = False

        x = node.position[0]
        y = node.position[1]
        if self.display_width < self.min_x:
            x_buffer = (self.min_x - self.grid.x_size*self.node_width*2 + \
                                                    self.horizontal_buffer)/2
            x_pos    = x_buffer + x * self.node_width
        else:
            x_pos    = self.grid_buffer + x * self.node_width
        if self.display_height < self.min_y:
            y_buffer = (self.min_y-self.grid.y_size*self.node_height)/2
            y_pos    = y_buffer + y * self.node_height
        else:
            y_pos    = self.grid_buffer + y * self.node_height
        if debug:
            print("Creating new rectangle with position (" + str(x_pos) + "," +
                  str(y_pos) + "), height " + str(self.node_height) +
                  ", and width " + str(self.node_width) + ".")
        return pygame.Rect(x_pos, y_pos, self.node_width, self.node_height)

    def make_emulated_node_rectangle(self, x, y, state):
        if self.display_width < self.min_x:
            x_buffer = (self.min_x - self.grid.x_size*self.node_width*2 + \
                                                    self.horizontal_buffer)/2
        else:
            x_buffer = self.grid_buffer
        x_pos = x_buffer + self.grid.x_size*self.node_width + \
                self.node_width*self.horizontal_buffer + \
                x*self.node_width*self.emulated_cell_width
        if self.display_height < self.min_y:
            y_buffer = (self.min_y-self.grid.y_size*self.node_height)/2
        else:
            y_buffer = self.grid_buffer
        y_pos = y_buffer + (self.node_height * self.vertical_buffer) + \
                (y * self.node_height * self.emulated_cell_height)
        return pygame.Rect(x_pos, y_pos,
                           self.node_width*self.emulated_cell_width,
                           self.node_height*self.emulated_cell_height)

    def make_node_text(self, node):
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        node_color = self.colormap[node.state]
        if sum(node_color) < 150:
            text_color = WHITE
        else:
            text_color = BLACK
        font = pygame.font.SysFont('monospace', 10)
        text_surface = font.render(node.state, True, text_color)
        return text_surface

#end class ParallelEmulatedSquareGridDisplay