from surface_crns import SurfaceCRNQueueSimulator
import sys

def main():
    # Get the size of the simulation from command line input, if possible.
    # Otherwise fall back to default.
    if len(sys.argv) > 1:
        GRID_SIZE = int(sys.argv[1])
    else:
        # To change grid size, either pass a number from the command line or 
        # change this value.
        GRID_SIZE = 750

    manifest_filename = "big_GH_init.txt"
    with open(manifest_filename, 'w') as outfile:
        header = '''# Run settings
pixels_per_node    = 1
speedup_factor     = 5
rng_seed           = 123123123
max_duration       = 6000
node_display       = Color

# Transition rules
!START_TRANSITION_RULES
A + Q -> A + A (1)
A -> R (0.6)
R -> Q (.03)
!END_TRANSITION_RULES

!START_COLORMAP
Q: (230,230,230)
A: (255, 0, 0)
R: (0, 100, 255)
!END_COLORMAP


!START_INIT_STATE'''
        outfile.write(header)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if col < GRID_SIZE/2:
                    outfile.write("Q ")
                else:
                    if row < GRID_SIZE/2:
                        outfile.write("A ")
                    else:
                        outfile.write("R ")
            outfile.write("\n")
        outfile.write("!END_INIT_STATE")

    # Run from the manifest just written.
    SurfaceCRNQueueSimulator.simulate_surface_crn(manifest_filename)

if __name__ == "__main__":
    main()