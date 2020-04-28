from surface_crns.models.grids import *
from surface_crns.simulators.queue_simulator import *
from surface_crns.readers.manifest_readers import read_manifest
from surface_crns.options.option_processor import SurfaceCRNOptionParser

def run_game(manifest_file):
    '''Input: manifest file name
       Output: string representing winner'''
    manifest_options = read_manifest(manifest_file)
    opts = SurfaceCRNOptionParser(manifest_options)

    lattice = SquareGrid(27, 19, wrap=False)
    lattice.set_global_state(opts.init_state)

    simulator = QueueSimulator(surface = lattice,
                                transition_rules = opts.transition_rules,
                                seed = opts.rng_seed,
                                simulation_duration = opts.max_duration)

    while not simulator.done():
        # faster to let simulation complete than to check for winner at
        # each step
        simulator.process_next_reaction()

    end_state = simulator.surface.get_global_state()
    if 'WX' in [j for i in end_state for j in i]:
        return 'X'
    elif 'WY' in [j for i in end_state for j in i]:
        return 'Y'
    return 'N'

filename = input("Manifest file name: ")
n = int(input("Number of games to run: "))
res = [run_game(filename) for i in range(n)]
print('X wins %d times' % (sum([(i=='X') for i in res])))
print('Y wins %d times' % (sum([(i=='Y') for i in res])))
print('%d ties' % (sum([(i=='N') for i in res])))
