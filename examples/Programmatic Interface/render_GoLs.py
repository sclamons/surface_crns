from visualize_state import render_state
import os

def main():
    colormap_file = os.path.join("Snapshots", "Manifests", 
                                 "logic_gate_colormap.txt")
    
    for t in [500*i for i in range(10)]:
        state_file = os.path.join("Snapshots", "Outputs", f"big_GoL_T={t}.csv")
        pixels_per_node = 5

        render_state(state_file, colormap_file, pixels_per_node)

if __name__ == "__main__":
    main()