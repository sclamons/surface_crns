import sys
from surface_crns.readers.grid_state_readers import read_grid_state
from surface_crns.readers.colormap_readers import read_colormap
from surface_crns.models.grids import SquareGrid
from surface_crns.views.grid_display import SquareGridDisplay
import pygame

pygame.display.init()
pygame.font.init()

'''
Produces an image of a surface CRN state. Call with

python visualize_state.py <state_file> <colormap_file> [pixels_per_node]

or call render_state directly.
'''

def main():
    if len(sys.argv) < 3:
        sys.exit("Must give a state file and a colormap file.")

    state_file = sys.argv[1]
    colormap_file = sys.argv[2]

    if len(sys.argv) >= 4:
        pixels_per_node = int(sys.argv[3])
    else:
        pixels_per_node = 5

    render_state(state_file, colormap_file, pixels_per_node)

def render_state(state_file, colormap_file, pixels_per_node):
    state_array = read_grid_state(state_file)
    x_size, y_size = state_array.shape
    state = SquareGrid(x_size, y_size)
    state.set_global_state(state_array.T)
    colormap = read_colormap(colormap_file)

    display = SquareGridDisplay(state, colormap, pixels_per_node)

    display_surface = pygame.display.set_mode((display.display_width, 
                                               display.display_height), 0, 32)
    display.render(display_surface, x_pos = 0, y_pos = 0)
    pygame.display.flip()

    pygame.image.save(display_surface, state_file.split(".")[0] + ".png")


if __name__ == "__main__":
    main()