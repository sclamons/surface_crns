'''
Simulates a surface chemical reaction network (CRN) on a 2D lattice.

Usage: python surface_CRN_simulator.py -m <manifest>

Simulates the stochastic behavior of a surface CRN on a 2D grid lattice. Only
implements unimolecular and bimolecular rules. Uses a Gillespie-Gibson-Bruck-
like algorithm for computing next reactions with a priority queue.
'''

from __future__ import print_function
import surface_crns.readers as readers
from surface_crns.options.option_processor import SurfaceCRNOptionParser
from surface_crns.models.grids import SquareGrid, HexGrid
from surface_crns.views.time_display import TimeDisplay
from surface_crns.views.grid_display import SquareGridDisplay, HexGridDisplay
from surface_crns.views.legend_display import LegendDisplay
from surface_crns.simulators.queue_simulator import QueueSimulator
from surface_crns.simulators.synchronous_simulator import SynchronousSimulator
from surface_crns.simulators.event_history import EventHistory
from surface_crns.simulators.event import Event
from surface_crns.base.transition_rule import TransitionRule

from surface_crns.pygbutton import *
import numpy as np
from queue import PriorityQueue
import random
import cProfile
import optparse
import sys
import pygame
#import pymedia.video.vcodec as vcodec
from pygame.locals import *

pygame.init()

#############
# CONSTANTS #
#############
PROFILE = False
WHITE = (255,255,255)
BLACK = (0, 0, 0)
time_font = pygame.font.SysFont('monospace', 24)
TEXT_X_BUFFER  = 10
TEXT_Y_BUFFER  = 5
TEXT_HEIGHT    = time_font.get_linesize() + 2 * TEXT_Y_BUFFER
button_width   = 60
button_height  = 30
button_buffer  = 5
MIN_GRID_WIDTH = 6 * button_width + 10 * button_buffer

#############
# VARIABLES #
#############
time = 0
simulation = None

################
# MAIN PROGRAM #
################
def main():
    available_options = optparse.OptionParser()
    available_options.add_option("-m", '--manifest', action = "store",
                                 type = 'string', dest = 'manifest_filename')
    (command_line_options, args) = available_options.parse_args(sys.argv)
    manifest_filename = command_line_options.manifest_filename
    if not manifest_filename:
        raise Exception("Manifest file required (use the flag -m <filename>, " +
                        "where <filename> is the name of your manifest file)")
    simulate_surface_crn(manifest_filename)

def simulate_surface_crn(manifest_filename, display_class = None,
                         init_state = None):
    '''
    Runs a simulation, and displays it in a GUI window.

    Normal operation is to read all options from a manifest file, given by
    manifest_filename. If you want to use a custom surface geometry (anything
    other than a square or hex grid), you'll need to supply your own initial
    state (whatever your display object will use, but must be an iterable and
    contain surface_crns.base.Node objects) and a class that can display your
    state (should subclass surface_crns.views.grid_display.SurfaceDisplay),
    which you should pass as "init_state" and "DisplayClass", respectively.
    '''

    ################################
    # READ MANIFEST AND INITIALIZE #
    ################################
    # Parse the manifest
    print("Reading information from manifest file " + manifest_filename + "...",
          end="")
    manifest_options = \
                readers.manifest_readers.read_manifest(manifest_filename)
    opts = SurfaceCRNOptionParser(manifest_options)

    print(" Done.")

    # Initialize simulation
    if init_state:
        grid = init_state
    else:
        if opts.grid is None:
            raise Exception("Initial grid state required.")
        grid = opts.grid
    if opts.simulation_type == "asynchronous":
        simulation = QueueSimulator(surface = grid,
                                    transition_rules = opts.transition_rules,
                                    seed = opts.rng_seed,
                                    simulation_duration = opts.max_duration)
    elif opts.simulation_type == "synchronous":
        simulation = SynchronousSimulator(
                                    surface = grid,
                                    update_rule = opts.update_rule,
                                    seed = opts.rng_seed,
                                    simulation_duration = opts.max_duration)
    else:
        raise Exception('Unknown simulation type "' + opts.simulation_type+'".')
    time = simulation.time
    event_history = EventHistory()

    ################
    # PYGAME SETUP #
    ################
    if opts.grid_type == 'parallel_emulated':
        from surface_crns.views.grid_display \
                import ParallelEmulatedSquareGridDisplay
        grid_display = ParallelEmulatedSquareGridDisplay(grid = grid,
                            colormap = opts.COLORMAP,
                            emulation_colormap = opts.emulation_colormap,
                            horizontal_buffer = opts.horizontal_buffer,
                            vertical_buffer = opts.vertical_buffer,
                            cell_height = opts.cell_height,
                            cell_width = opts.cell_width,
                            representative_cell_x = opts.representative_cell_x,
                            representative_cell_y = opts.representative_cell_y,
                            min_x = MIN_GRID_WIDTH,
                            min_y = 0,
                            pixels_per_node = opts.pixels_per_node,
                            display_text = opts.display_text)
    elif opts.grid_type == 'standard':
        if display_class:
            DisplayClass = display_class
        elif opts.grid_type == "standard" and opts.surface_geometry == "square":
            DisplayClass = SquareGridDisplay
        elif opts.grid_type == "standard" and opts.surface_geometry == "hex":
            DisplayClass = HexGridDisplay
        grid_display = DisplayClass(grid = grid,
                                    colormap = opts.COLORMAP,
                                    min_x = MIN_GRID_WIDTH,
                                    min_y = 0,
                                    pixels_per_node = opts.pixels_per_node,
                                    display_text = opts.display_text)
    else:
        raise Exception("Unrecognized grid type '" + opts.grid_type + "'")

    legend_display = LegendDisplay(colormap = opts.COLORMAP)

    # Width only requires legend and grid sizes to calculate
    display_width  = grid_display.display_width + legend_display.display_width

    # Width used to calculate time label and button placements
    time_display  = TimeDisplay(display_width)

    button_y      = time_display.display_height + grid_display.display_height+1
            # max(legend_display.display_height, grid_display.display_height) + 1
    #(int(display_width/2) - (button_width + button_buffer), button_y,
    play_back_button  = PygButton(rect =
         (legend_display.display_width + button_buffer, button_y,
         button_width, button_height),
                             caption = '<<')
    step_back_button  = PygButton(rect =
         (play_back_button.rect.right + button_buffer, button_y,
         button_width, button_height),
                             caption = '< (1)')
    pause_button  = PygButton(rect =
         (step_back_button.rect.right + button_buffer, button_y,
         button_width, button_height),
                              caption = 'Pause')
    step_button  = PygButton(rect =
        (pause_button.rect.right + button_buffer, button_y,
         button_width, button_height),
                             caption = '(1) >')
    play_button  = PygButton(rect =
        (step_button.rect.right + button_buffer, button_y,
         button_width, button_height),
                             caption = '>>')
    clip_button = PygButton(rect =
        (play_button.rect.right + 4*button_buffer, button_y,
         button_width * 1.1, button_height),
                            caption = 'Uncache')

    display_height = max(legend_display.display_height + \
                2*legend_display.VERTICAL_BUFFER + time_display.display_height,
                         button_y + button_height + 2*button_buffer)

    if opts.debug:
        print("Initializing display of size " + str(display_width) + ", " +
                str(display_height) + ".")
    display_surface = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Surface CRN Simulator')
    fpsClock = pygame.time.Clock()

    # Initial render
    display_surface.fill(WHITE)

    # Make the options menu.
    #opts_menu = MainOptionMenu()
    #opts_menu.update()

    time_display.render(display_surface, x_pos = 0,
                                         y_pos = 0)
    legend_display.render(display_surface, x_pos = 0,
                                          y_pos = time_display.y_pos +
                                                  time_display.display_height)
    grid_display.render(display_surface, x_pos = legend_display.display_width,
                                         y_pos = time_display.y_pos +
                                                 time_display.display_height)
    play_back_button.draw(display_surface)
    step_back_button.draw(display_surface)
    pause_button.draw(display_surface)
    step_button.draw(display_surface)
    play_button.draw(display_surface)
    clip_button.draw(display_surface)
    pygame.display.update()

    # Prepare movie capture
    if opts.saving_movie:
        frame_number = 1
        capture_time = 0
        movie_file = open(opts.movie_title, 'wb')
        movie_params = {\
            'type': 0,
            'gop_size': 12,
            'frame_rate_base': 125, #fps,
            'max_b_frames': 0,
            'height': display_surface.get_height(),
            'width': display_surface.get_width(),
            'frame_rate': 2997, # fps,
            'deinterlace': 0,
            'bitrate': 9800000,
            'id': vcodec.getCodecID('mpeg2video')}
        movie_encoder = vcodec.Encoder(movie_params)

    # State variables for simulation
    next_reaction_time = 0
    next_reaction = None
    prev_reaction = None
    running = False
    first_frame = True
    last_frame  = False

    # Iterate through events
    while True:
        # Check for interface events
        for event in pygame.event.get():
            if 'click' in play_back_button.handleEvent(event):
                running = True
                running_backward = True
                last_frame = False
            if 'click' in step_back_button.handleEvent(event):
                running = False
                last_frame = False
                if event_history.at_beginning():
                    time = 0
                    time_display.time = 0
                    time_display.render(display_surface, x_pos = 0, y_pos = 0)
                    pygame.display.update()
                else:
                    prev_reaction = event_history.previous_event()
                    event_history.increment_event(-1)
                    prev_reaction_rule = prev_reaction.rule
                    for i in range(len(prev_reaction.participants)):
                        cell = prev_reaction.participants[i]
                        state = prev_reaction_rule.inputs[i]
                        cell.state = state
                    display_next_event(prev_reaction, grid_display)
                    if event_history.at_beginning():
                        time = 0
                    else:
                        # Note that this is NOT the same as the time from the
                        # "previous event" that we're currently processing --
                        # it's actually the time of the event *before* the one
                        # we just undid.
                        time = event_history.previous_event().time
                    time_display.time = time
                    time_display.render(display_surface, x_pos = 0, y_pos = 0)
                    pygame.display.update()
            if 'click' in pause_button.handleEvent(event):
                running = False
            if 'click' in step_button.handleEvent(event):
                running = False
                first_frame = False
                # Process a single reaction
                reading_history = False
                if not event_history.at_end():
                    reading_history = True
                    next_reaction = event_history.next_event()
                    event_history.increment_event(1)
                    next_reaction_rule = next_reaction.rule
                    for i in range(len(next_reaction.participants)):
                        cell = next_reaction.participants[i]
                        state = next_reaction_rule.outputs[i]
                        cell.state = state
                if not next_reaction:
                    next_reaction = simulation.process_next_reaction()
                    if not reading_history:
                        event_history.add_event(next_reaction)
                        event_history.increment_event(1)
                next_reaction_time = next_reaction.time
                display_next_event(next_reaction, grid_display)
                time = next_reaction_time
                time_display.time = time
                time_display.render(display_surface, x_pos = 0, y_pos = 0)
                pygame.display.update()
                next_reaction = None
                if opts.debug:
                    print("State after update: " + str(grid))
            if 'click' in play_button.handleEvent(event):
                running = True
                running_backward = False
                first_frame = False
            if 'click' in clip_button.handleEvent(event):
                event_history.clip()
                simulation.time = time
                simulation.reset()
                for rxn in list(simulation.event_queue.queue):
                    print(rxn)
            if event.type == QUIT:
                if opts.saving_movie:
                    movie_file.close()
                cleanup_and_exit(simulation)
        # Don't do anything if paused.
        if not running:
            pygame.display.update()
            continue

        # Update time
        if running_backward and not first_frame:
            prev_reaction_time = time
            time -= opts.speedup_factor * 1./opts.fps
        elif not running_backward and not last_frame:
            next_reaction_time = time
            time += opts.speedup_factor * 1./opts.fps
        time_display.time = time
        time_display.render(display_surface, x_pos = 0,
                            y_pos = 0)

        # Process any simulation events that have happened since the last tick.
        if running_backward and not first_frame:
            while not event_history.at_beginning() and prev_reaction_time>time:
                prev_reaction = event_history.previous_event()
                if event_history.at_beginning():
                    first_frame = True
                event_history.increment_event(-1)
                for i in range(len(prev_reaction.participants)):
                    cell  = prev_reaction.participants[i]
                    state = prev_reaction.rule.inputs[i]
                    cell.state = state
                prev_reaction_time = prev_reaction.time if prev_reaction else 0
                display_next_event(prev_reaction, grid_display)
        elif not running_backward and not last_frame:
            while (not event_history.at_end() or not simulation.done()) \
               and next_reaction_time < time:
                if event_history.at_end():
                    next_reaction = simulation.process_next_reaction()
                    if next_reaction:
                        event_history.add_event(next_reaction)
                        event_history.increment_event(1)
                else:
                    next_reaction = event_history.next_event()
                    event_history.increment_event(1)
                    for i in range(len(next_reaction.participants)):
                        cell = next_reaction.participants[i]
                        state = next_reaction.rule.outputs[i]
                        cell.state = state

                next_reaction_time = next_reaction.time if next_reaction \
                                                    else opts.max_duration + 1
                display_next_event(next_reaction, grid_display)

        # Render updates and make the next clock tick.
        pygame.display.update()
        fpsClock.tick(opts.fps)

        # Check for simulation completion...
        if event_history.at_end() and running and not running_backward and \
           (simulation.done() or time > opts.max_duration):
            last_frame = True
            running = False
            # Set the time to final time when done.
            time = opts.max_duration
            time_display.time = time
            time_display.render(display_surface, x_pos = 0,
                                y_pos = 0)#opts_menu.display_height)
            if next_reaction:
                display_next_event(next_reaction, grid_display)
            pygame.display.update()
            if opts.debug:
                print("Simulation state at final time " + str(opts.max_duration) + \
                      ":")
                print(str(grid))
        if event_history.at_beginning() or time == 0:
            first_frame = True

#end def main()

def display_next_event(next_reaction, grid_display):
    # Update the display for a reaction. Reaction will be an Event object (see
    # surface_crns.simulators.py).
    DEBUG = False

    if DEBUG:
        print("Moving to next reaction:")

    if not next_reaction:
        if DEBUG:
            print("No reaction returned from event queue. Finished")
        return -1

    next_reaction_time = next_reaction.time

    if DEBUG:
        print("Updating display based on event " +
              str(next_reaction))

    # Display any changes made
    participants = next_reaction.participants
    inputs       = next_reaction.rule.inputs
    outputs      = next_reaction.rule.outputs
    # Update reactants (if changed)
    for i in range(len(participants)):
        if inputs[i] != outputs[i]:
            grid_display.update_node(participants[i])
        elif DEBUG:
            print("Input " + str(i+1) + " and output " + str(i+1) + " match " +
                  "for rule " + str(next_reaction.rule) + "\ncell " +
                  str(participants[0].position) + " not updated.")

    # Display current state to stdout.
    if DEBUG:
        print("Simulation state at time " + str(next_reaction_time) + \
              ":\n" + str(grid_display.grid))

    return next_reaction_time

def cleanup_and_exit(simulation):
    pygame.quit()
    print("Program terminated before simulation comlete.")
    print("Simulation state at termination (T = " + str(simulation.time) + "):")
    print(str(simulation.surface))
    sys.exit()

if __name__ == '__main__':
    if PROFILE:
        '''try:
            import statprof
            statprof.start()
            try:
                main()
            finally:
                statprof.stop()
                statprof.display()
        except ImportError:'''
        cProfile.run("main()", sort='tottime')
    else:
        main()