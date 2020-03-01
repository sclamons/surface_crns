from surface_crns.models.grids import *
from surface_crns.base.node import *
from surface_crns.simulators.queue_simulator import *
from surface_crns.simulators.queue_simulator_eager import *
from surface_crns.readers.manifest_readers import read_manifest
from surface_crns.options.option_processor import SurfaceCRNOptionParser
import time
import os

seed = 635253461

def simulate_without_display(manifest, Simulator):
    '''
    Run to completion with a given Simulator class.
    '''
    manifest_options = read_manifest(manifest)
    opts = SurfaceCRNOptionParser(manifest_options)
    simulator = Simulator(surface = opts.grid,
                           transition_rules = opts.transition_rules,
                           seed = seed,
                           simulation_duration = opts.max_duration)
    while not simulator.done():
        next_rxn = simulator.process_next_reaction()
        
    return simulator.time

def main():
	simulation_list = ["rule_110.txt", 
			os.path.join("synchronous_GH","GH_synch_manifest_full.txt"), 
			os.path.join("Robots", "anthills.txt")]
	for manifest_file in simulation_list:
		print(f"Simulation {manifest_file}:")
		for simulator, s in [(QueueSimulator, "QueueSimulator"), 
							 (EagerQueueSimulator, "EagerQueueSimulator")]:
			start_time = time.time()
			simulate_without_display(manifest_file, simulator)
			print(f"\t{s}: {time.time() - start_time} sec")


if __name__ == "__main__":
	main()