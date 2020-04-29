Welcome to the Examples
=======================

This package includes a few sets of examples:
* **Programmatic Interface**: Examples that show how to use the surface_crn package within python. This lets you do things like run headless simulations (no graphics) and swap out features like the simulator algorithm or underlying grid geometry. 
* **Paper**: Examples from the paper. If you're looking to reproduce a figure from the paper, look here.
* **Other**: A few other fun examples that didn't make it into the paper.


<a name="prog_interface_ex"></a>Programmatic Interface Examples
===============================


<a name="snapshots"></a>

<a name="rugby_ex"></a>

Paper Examples
==============
This section mostly contains self-contained examples, sorted by paper section. Any file ending with "_manifest.txt" can be run directly with the simulator. For example, from the "examples" directory, `SurfaceCRNQueueSimulator -m "Paper/3 - Dynamic Spatial Patterns/3.1_GH_asynchronous_manifest.txt"` will run the simple, asynchronous Greenberg-Hastings example from section 3.1 (though see the main page README about running with pythonw on some OSX systems).

## Chapter 3: Dynamic Spatial Patterns

#### Manifests:
* `3.1_GH_asynchronous_manifest.txt`: Asynchronous Greenberg-Hastings (GH) spiral, as in the third column of Fig. 1d. 
* `3.2_GH_spinning_arrow_manifest.txt`: Synchronous suface CRN emulation of one of several GH patterns, as in the fourth column of Fig 1.c-e. Comment in exactly one of the three INCLUDE statements in the initial state section of the manifest to get either a single pulse, a spiral wave, or a random-start pattern. Transition rules, colormap, and initial states are in separate files with suggestive names. The random initialization function was produced with `generate_random_GH_init.py` and `init_state_to_spinning_arrow_init_state.py`.
* `3.3_Game_of_Life_broadcast_swap_sum_manifest.txt`: Broadcast-swap-sum synchronous emulation of a Game of Life glider, as in Fig. 2f. Edit the "E0" and "E1" states to try different Game of Life configurations.
* `3.3_GH_broadcast_swap_sum_manifest.txt`: Broadcast-swap-sum synchronous emulation of a GH spiral, as in Fig. 2g.

#### Other Files:

`Fig1b_GH_well_mixed` reproduces Fig. 1b (requires `matplotlib` and `numpy` packages).

You can make spinning-arrow emulators for any synchronous cellular automaton with NSEW neighbors, but we do not recommend trying to write rules or initial states for these by hand. We provide two scripts that may help you if you do want to make your own spinning-arrow emulators:
* `init_state_to_spinning_arrow_init_state.py`: This program takes the name of any manifest specifying an initial state that is *not* in spinning-arrow form. It will produce a file containing a corresponding initial state for a spinning-arrow emulation of the initial state in the manifest. For example, `init_state_to_spinning_arrow_init_state.py` was used to produce `3.2_GH_spinning_arrow_random_init.txt` from a manifest containing the output of `generate_random_GH_init.py` in its initial state block.
* `synch_GH_automata_rule_generator`: This script is hard-coded to genrate transition rule and colormap files for a spinning-arrow implementation of the GH automaton. It cannot, as written, generate spinning-arrow implementations of other rule sets, but it may serve as a useful guide if you wish to create your own.

## Chapter 4: Continuously Active Logic Circuits

#### Manifests

All logic gate examples share transition rules and colormaps from `logic_circuit_transition_rules.txt` and `logic_gate_colormap.txt`, respectively. 

* `Fig4a-2-bit_adder_manifest.txt`: A 2-bit adder, as shown in Fig. 4a (but rotated on its side). Set the inputs by changing initial states at positions E1, G1, I1, and L1 (as viewed in Excel). The inputs are `2*E1 + G1` and `2*I1 + L1`, and the output is `4*F28 + 2*M25 + O16`. 
* `Fig4b-binary_counter_manifest.txt`: A 4-bit binary counter, as shown in Fig. 4b (but rotated on its side).
* `Fig4c-Game_of_Life_one_cell_manifest.txt`: A single (alive) cell from a logic-circuit-based Game of Life implementation. To change the initial emulated state, edit initial positions G15:G22, Y16, and V24 (as viewed in Excel). For an example with multiple cells, see the [**Snapshots**](#snapshots) example from [**Programmatic Interface Examples**](#prog_interface_ex). 

#### Other Files

`Box5-logic_circuit_transition_rules_compressed.txt` demonstrates a 46-rule compressed transition rule set that eschews "redundant" gates (i.e., AND, NOT, OR, and XOR are replaced by NOR), as alluded to in Box 5. This will NOT work directly with any of the initial states used here, as it uses a different set of gates.

## Chapter 5: Manufacturing

#### Manifests

* `Fig5a-rule_110_manifest.txt`: Stephen Wolfram's Rule 110, computed forward in time from top to bottom, as shown in Fig. 5a.
* `Fig5b-blossom_manifest.txt`: Grows a 32-molecule, irregularly-shaped blossom, as in Fig. 5b. This will produce a different shape with each run, but every shape will have exactly 32 blossom sites.
* `Fig5c-random_line_manifest.txt`: Simple random-walking line, as in Fig. 5c. 
* `Fig5d-straight_line_manifest.txt`: Builds an infinite-length, width-2 straight line, as in Fig. 5d.
* `Fig5e-bitmap_image_manifest.txt`: Builds a bitmap-specified picture of a butterfly, as shown in Fig. 5e. This manifest is generated by `make_rastered_image_crn.py` -- edit and run that file to make other bitmap patterns. 

#### Other Files

You can generate surface CRNs to make your own bitmap patterns by modifying and running `make_rastered_image_crn.py`. Change the `image` array at the top of the file to use the same colors as the butterfly; edit lines 108-113 to define your own colors. The script will generate a manifest that can be run with the simulator.


## Chapter 6: Robots and Swarms

#### Manifests

* `Fig6a-anthill_manifest.txt`: Simulates a simple mound-building algorithm, as shown in Fig. 6a. 
* `Fig6b-scouting_ant_manifest.txt`: Simulates a simple food-finding ant with minimal trap-avoidance rules, as shown in Fig. 6b.
* `Fig6c-cargo_sorter_manifest.txt`: Simulates a spatial sorting algorithm that gathers two different materials into piles, as shown in Fig. 6c. 

## Chapter 7: Rugby

#### Manifests

* `Fig7-rugby_manifest.txt`: Simulates a game of molecular rugby using two particularly simple strategies, as shown in Fig. 7. Edit lines 55-104 to change the teams' strategies ("[rugby gods edit here]"). See the [**Rugby_Competition**](#rugby_ex) example from [**Programmatic Interface Examples**](#prog_interface_ex) for code to run a round-robin tournament between different strategies. 


Other Examples
==============

* `ertl.txt`: Manifest file for an Ertl chemical oscillator (https://doi.org/10.1021/cr00035a012). Carbon monoxide and molecular oxygen adsorb to a crystal platinum catalyst, and can diffuse on it. Adjacent CO and O will convert to carbon dioxide and desorb. Together, these dynamics cause patterned oscillations.
* `GH_big_spiral_manifest.txt`: A 750x750 Greenberg-Hastings oscillator surface CRN, as shown in the third column of Fig. 1d but on a much larger scale. At this size, spiral patterns are persistent for some time before devolving into chaotic patterns reminiscent of the Belousov-Zhabotinsky reaction. Be patient with this one -- it may take a couple of minutes to load. 