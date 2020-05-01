from visualize_state import render_state
import os

def main():
    colormap_file = os.path.join("Snapshots", "Manifests",
                                 # "big_GH_colormap.txt")
                                 # ^ Swap this in to render the GH example ^
                                 "logic_gate_colormap.txt")


    for t in [500*i for i in range(10)]:
        state_file = os.path.join("Snapshots", "Outputs", f"big_GoL_T={t}.csv")

    # Swap in these two lines, and one on line 7, to render GH spirals instead.
    # for t in [50, 200, 350, 770, 1200]:
    #     state_file = os.path.join("Snapshots", "Outputs", f"GH_big_spiral_T={t}.csv")
        pixels_per_node = 5

        render_state(state_file, colormap_file, pixels_per_node)

if __name__ == "__main__":
    main()

    