from surface_crns.simulators.queue_simulator import QueueSimulator
from surface_crns.readers.manifest_readers import read_manifest
from surface_crns.options.option_processor import SurfaceCRNOptionParser
import os

def main():
    '''
    Run several simulations, saving states in CSV format at a few times.
    # '''
    # # sCRNs maps manifest filenames to lists of times at which to save.
    # # Uncomment lines for sCRNs you'd like to save.
    sCRNs = dict()
    sCRNs["GH_big_spiral_manifest.txt"] = [50, 200, 350, 770, 1200]
    sCRNs["big_GoL_manifest.txt"] = [500*i for i in range(10)]
    sCRNs["bitmap_butterfly_manifest.txt"] = [0, 50, 150, 250, 300, 350, 500]
    sCRNs["anthill_manifest.txt"] = [100, 2000, 5000, 14000, 20000]

    for name, times in sCRNs.items():
        base_name = name.split(".")[0].replace("_manifest", "")
        manifest_filename = os.path.join("Manifests", name)
        manifest_options  = read_manifest(manifest_filename)
        opts = SurfaceCRNOptionParser(manifest_options)
        simulator = QueueSimulator(surface = opts.grid,
                                   transition_rules = opts.transition_rules,
                                   seed = opts.rng_seed,
                                   simulation_duration = max(times) * 1.1)
        time = 0
        t_idx = 0
        next_t = times[t_idx]
        while True:
            if time >= next_t:
                outfile = os.path.join("Outputs",f"{base_name}_T={next_t}.csv")
                write_snapshot(outfile, simulator.surface)
                t_idx += 1
                if t_idx >= len(times):
                    break
                next_t = times[t_idx]
            next_rxn = simulator.process_next_reaction()
            if next_rxn is None:
                break
            time = next_rxn.time

def write_snapshot(filename, surface):
    # Note: only guaranteed for square grids.
    grid = surface.grid
    n_rows, n_cols = grid.shape
    def concatenate_row(row_num):
        return ",".join([n.state for n in grid[row_num,:]])
    rows = [concatenate_row(row_num) for row_num in range(n_rows)]
    snapshot_text = "\n".join(rows)
    with open(filename, 'w') as outfile:
        outfile.write(snapshot_text)

if __name__ == "__main__":
    main()