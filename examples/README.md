Welcome to the Examples
=======================

This package includes a few sets of examples:
* "Paper": Examples from the paper. If you're looking to reproduce a figure from the paper, look here.
* "Programmatic Interface": Examples that show how to use the surface_crn package within python. This lets you do things like run headless simulations (no graphics) and swap out features like the simulator algorithm or underlying grid geometry. 
* "Other": A few other fun examples that didn't make it into the paper.

Paper
=====
This section mostly contains self-contained examples, sorted by paper section. Any file ending with "_manifest.txt" can be run directly with the simulator. For example, from the "examples" directory, `SurfaceCRNQueueSimulator -m "Paper/3 - Dynamic Spatial Patterns/3.1_GH_asynchronous_manifest.txt"` will run the simple, asynchronous Greenberg-Hastings example from section 3.1 (though see the main page README about running with pythonw on some OSX systems).

## Chapter 3: Dynamic Spatial Patterns

#### Manifests:
* `3.1_GH_asynchronous_manifest.txt`: Asynchronous Greenberg-Hastings (GH) spiral, as in the third column of Fig. 1d. 
* `3.2_GH_spinning_arrow_manifest.txt`: Synchronous suface CRN emulation of one of several GH patterns, as in the fourth column of Fig 1.c-e. Comment in exactly one of the three INCLUDE statements in the initial state section of the manifest to get either a single pulse, a spiral wave, or a random-start pattern. Transition rules, colormap, and initial states are in separate files with suggestive names. The random initialization function was produced with `generate_random_GH_init.py` and `init_state_to_spinning_arrow_init_state.py`.
* `3.3_Game_of_Life_broadcast_swap_sum_manifest.txt`: Broadcast-swap-sum synchronous emulation of a Game of Life glider, as in Fig. 2f. Edit the "E0" and "E1" states to try different Game of Life configurations.
* `3.3_GH_broadcast_swap_sum_manifest.txt`: Broadcast-swap-sum synchronous emulation of a GH spiral, as in Fig. 2g.

#### Other files:

`Fig1b_GH_well_mixed` reproduces Fig. 1b (requires `matplotlib` and `numpy` packages).

You can make spinning-arrow emulators for any synchronous cellular automaton with NSEW neighbors, but we do not recommend trying to write rules or initial states for these by hand. We provide two scripts that may help you if you do want to make your own spinning-arrow emulators:
* `init_state_to_spinning_arrow_init_state.py`: This program takes the name of any manifest specifying an initial state that is *not* in spinning-arrow form. It will produce a file containing a corresponding initial state for a spinning-arrow emulation of the initial state in the manifest. For example, `init_state_to_spinning_arrow_init_state.py` was used to produce `3.2_GH_spinning_arrow_random_init.txt` from a manifest containing the output of `generate_random_GH_init.py` in its initial state block.
* `synch_GH_automata_rule_generator`: This script is hard-coded to genrate transition rule and colormap files for a spinning-arrow implementation of the GH automaton. It cannot, as written, generate spinning-arrow implementations of other rule sets, but it may serve as a useful guide if you wish to create your own.

## Chapter 4: Continuously Active Logic Circuits