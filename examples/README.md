Welcome to the Examples
=======================

This package includes a few sets of examples:
* [**Programmatic Interface**](#prog_interface_ex): Examples that show how to use the surface_crn package within python. This lets you do things like run headless simulations (no graphics) and swap out features like the simulator algorithm or underlying grid geometry.
* [**Paper**](#paper_ex): Examples from the paper. If you're looking to reproduce a figure from the paper, look here.
* [**Other**](#other_ex): A few other fun examples that didn't make it into the paper.


<a name="prog_interface_ex"></a>Programmatic Interface Examples
===============================

## Miscellanious Examples

#### Running Simulations with Python

If you are having difficulty using SurfaceCRNQueueSimulator from the command line -- or you just want to invoke it programmatically -- `simple_python_interface_example.py` will show you what to do. In short:

```python
from surface_crns import SurfaceCRNQueueSimulator

manifest_filename = "some_manifest.txt"
SurfaceCRNQueueSimulator.simulate_surface_crn(manifest_filename)
```

SurfaceCRNQueueSimulator is somewhat modular, and the `simulate_surface_crn` function allows you to drop in custom display classes and state objects as the `display_class` and `init_state` arguments. The [**Water Adsorption Model**](#water_adsorption) and [**Long-Range Leaky Interactions**](#long_range) examples to see how to do this.

You can also run the simulator headlessly by bypassing SurfaceCRNQueueSimulator entirely and using the underlying simulator and model objects directly. Several examples, including [**The Water Adsorption Model**](#water_adsorption), [**Visualizing State Snapshots**](#visualize), and [**Comparing Queue Implementations**](#comparing_queues) demonstrate various ways to use surface_crn objects directly.

Under the hood, surface_crns uses a Model-View-Controller architecture.
* **Model** -- This is a grid object that stores the site lattice and the state of each node in the lattice. Usually this is a `surface_crns.models.grids.SquareGrid`, but `grids.py` in `surface_crns/models` has a few other examples, as does the [**Water Adsorption Model**](#water_adsorption) example.
* **View** -- Views are handled by several classes in various files in `surface_crns/views`. Views in surface_crns are intimately tied to pygame. The [**Visualizing State Snapshots**](#visualize) example shows how to use pygame to directly invoke `surface_crns.views.grid_display.SquareGridDisplay` (which displays states on a square grid -- the default used by SurfaceCRNQueueSimulator), and the [**Water Adsorption Model**](#water_adsorption) model shows how to build and use your own grid display class.
* **Controller** -- Control of the models and views is split across two levels. Simulation and update of the model is handled by one of two simulator objects (QueueSimulator or QueueSimulatorEager, in `surface_crns.simulators.queue_simulator.py` and `surface_crns.simulators.queue_simulator_eager.py`, respectively), while inputs, views, and GUI are coordinated by SurfaceCRNQueueSimulator (which is intended to be the main user-facing class in surface_crns). The [**Comparing Queue Implementations**](#comparing_queues) example shows how to directly invoke a simulator.

#### Large-Field Greenberg-Hastings

This is another example of how to run SurfaceCRNQueueSimulator programmatically, this time to run an asynchronous GH simulation with a variable (potentially large) size. Running

```python GH_big_spiral.py N```

will generate a new manifest (`big_GH_init.txt`) describing a GH surface CRN simulation on an NxN grid, laid out to generate a large spiral.

#### <a name="visualize"></a>Visualizing State Snapshots

The script `visualize_state.py` is used to create static images of surface CRN states stored in a CSV or TSV file (such as those produced in the [**Snapshots**](#snapshots) example). The script requires a file containing a surface CRN state (and ONLY a surface CRN state) in the same format used by a manifest file, and a file containing (ONLY) a colormap definition, again in the same format used in a manifest file. It can also optionally take a `pixels_per_node` argument to set the size of each state in the output image, in pixels. It uses the colormap to make a static render of the image, which is saved as a PNG file.

Invoke either from the command line:

```python visualize_state.py state_file colormap_file (pixels_per_node)```

Or invoke in python, from the same directory as `visualize_state.py`:

```python
import visualize_state
state_file = "example_state.txt"
colormap_file = "example_colormap.txt"
pix_per_node = 25
visualize_state.render_state(state_file, colormap_file, pix_per_node)
```

For more example usage, see `render_GoLs.py`, which produces renders of the Game of Life snapshots produced in the [**Snapshots**](#snapshots) example.

#### <a name="comparing_queues"></a>Comparing Queue Implementations

This script compares the performance profile of two different queue-based simulator objects on a couple of different examples from the "Paper" section. It shows a compact example of how to run a surface CRN simulation "headlessly" (without graphic display).

Both simulators implement the efficient queue-based algorithm described in the second half of Box 2, from the paper. The two simulators differ in how they remove "stale" reactions (reactions scheduled to occur at a site that has already been modified by another reaction) from the queue. `QueueSimulator`, the standard simulator, checks each reaction for staleness as it is popped from the queue. This is fast per-reaction, but it leaves potentially large numbers of stale reactions in the queue, which slows down every dequeueing event.

The second simulator, EagerQueueSimulator, checks every reaction in the queue for staleness after each reaction, so that stale reactions are never stored. This introduces a step linear in the size of the queue to each event, but it keeps the queue smaller, which can be faster for small queues and for systems where many reactions are possible at each site.

This one can take a while to run.

#### <a name="water_adsorption"></a>Physical Surface Chemistry (Water adsorption/splitting Model)

The script `water_adsorption.py` simulates the interaction of gaseous water and the a regular hexagonal silver crystal (Ag(111)) surface, loosely adapted from [Jin Qian, Yifan Ye, Hao Yang, Junko Yano, Ethan J. Crumlin, and William A. Goddard III
*Journal of the American Chemical Society* 2019 141 (17), 6946-6954](https://doi.org/10.1021/jacs.8b13672). This system uses non-square grid geometry -- reactions can occur at either a silver molecule or at the tri-fold intersection (3F) of three sites -- and so shows how to use custom grid geometries and custom displays.

Briefly, water can interact with a silver surface as follows:
* Water can adsorb from the air onto any open silver site. Adsorption is greatly enhanced by the presence of molecular oxygen already on the surface.
* Water can detatch from the silver surface.
* Water attached to a silver atom can reversibly react with an adjacent oxygen atom at a three-fold site to form two silver-complexed OH ions.
* Complexed water can diffuse between adjacent silver sites; complexed OH can diffuse between three-fold sites and silver molecules.

The script can run either graphically or without graphics (headless). By default, it will show a windowed simulation, much as any simulation called with SurfaceCRNQueueSimulator. When run with the "headless" flag, it will instead run with no graphics and instead show a plot of species concentrations in the system over time.

The water adsorption model uses a custom model -- a hex grid plus three-fold intersection sites at the corner of each hex -- and accompanyig custom display class. Any custom model must have an iterator that returns nodes in the model, and should implement the `populate_grid` method, which sets up the model and sets it to a default state. A custom model must also implement a `set_global_state` function that takes an array (or Numpy ndarray) and sets the state of each node in the model accordingly; this is implemented in `surface_crns.models.grids.SquareGrid`, from which `HexGridPlusIntersections` inherits.

The custom display class used in this example, `HexGridPlusIntersectionDisplay`, indirectly inherits from `surface_crns.views.grid_display.SurfaceDisplay`, which defines an interface for any display. Anyting inheriting from `SurfaceDisplay` should implement a constructor (taking a minimum of a model object representing the surface and a dictionary mapping state names to colors), a `render` function, and an `update_node` function. `render` is called at the beginning of a simulation, and usually iterates over all the nodes on the surface, drawing each with `update_node`. The `update_node` function is what you will usually need to overwrite in a custom display class -- it must, when passed a node from the model, draw that node's current state to the screen. See `water_adsorption.py` for an example.

#### <a name="long_range"></a>Long-Range Leaky Interactions

This program simulates diffusion of a gas across an empty background. It serves as an example of simulation with a custom model object.

If you watch closely, stepping through individual reactions, you will see that the gas can sometimes diffuse across a corner. This is because this program uses a nonstandard grid with weighted connections, in which nodes that neighbor by a corner are connected with low weight. This allows molecules to interact across corners, albeit with less frequency. This could be realistic if, for example, a surface CRN were constructed with molecules held to a surface by a flexible tether that was long enough to allow corner-neighbors to touch, but not to react as efficiently as full-neighbors.

This leaky-corner model is implemented with the `SquareGridWithCornerLeak` class, provided in `surface_crns.models.grids`. See surface_crns/models/grids.py for implementation details.

## <a name="snapshots"></a>Snapshots

The script `examples/Programmatic Interface/Snapshots/save_simulation_snapshots.py` headlessly simulates four example simulations, defined in a "Manifests" subfolder, and saves snapshots at defined time to an "Outputs" subfolder. These snapshots are saved as CSV files, which can be rendered into an image with [`visualize_state.py`](#visualize).

This script is a useful example of how to directly use the simulator objects underlying SurfaceCRNQueueSimulator, and shows how to interact directly with a model object. The "Manifests" subfolder also contains a helper script GoL_state_to_sCRN_init.py, which converts a Game of Life state (stored in Manifests/gol_state.txt) into an initial state for a logic-gate-implemented Game of Life surface CRN.

## <a name="rugby_ex"></a>Rugby Competition

This folder is for running molecular rugby competitions. The basic molecular rugby rules (and simulation specs) are given in `templated_rugby_manifest.txt`. Team strategies should be stored in individual text files in the "Teams" subfolder, and should always be defined for team X.

You can watch a game between two strategies using the `examples/Programmatic Interface/Rugby Competition/rugby_game.py` script. The script takes two text files specifying strategies (for example, the ones in the "Teams" folder) as inputs. It will create a manifest file for the matchup in the "temp" folder, which it will then use to run and display the game.

The script `examples/Programmatic Interface/Rugby Competition/rugby_tournament.py` runs a round-robin tournament between any molecular rugby strategies defined in files inside a "Teams" subfolder, printing the results to a uniquely-indexed text file in a "results" subfolder. For each pair of strategies, `rugbycompete.py` will flip one team to be team Y, play some number of games N (which can be specified in a command line argument or left to a default 100), and determines a winner. A team wins if it beats the other team by at least sqrt(N). If no team beats the other by at least this margin, the game is considered a tie.

Because surface CRN simulation is stochastic, this program is not guaranteed to always provide the same results. If you want consistent, reproducible outputs, change the `SEED` variable near the top of the python script.

You'll need to be patient with this simulation! It can take quite a while to run, and will give you progress information as it runs.

<a name="paper_ex"></a>Paper Examples
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

## <a name="logic_ex"></a>Chapter 4: Continuously Active Logic Circuits

#### Manifests

All logic gate examples share transition rules and colormaps from `logic_circuit_transition_rules.txt` and `logic_gate_colormap.txt`, respectively.

* `Fig4a-2-bit_adder_manifest.txt`: A 2-bit adder, as shown in Fig. 4a (but rotated on its side). Set the inputs by changing initial states at positions E1, G1, I1, and L1 (as viewed in Excel). The inputs are `2*E1 + G1` and `2*I1 + L1`, and the output is `4*F28 + 2*M25 + O16`.
* `Fig4b-binary_counter_manifest.txt`: A 4-bit binary counter, as shown in Fig. 4b (but rotated on its side).
* <a name="gol_ex"></a>`Fig4c-Game_of_Life_one_cell_manifest.txt`: A single (alive) cell from a logic-circuit-based Game of Life implementation. To change the initial emulated state, edit initial positions G15:G22, Y16, and V24 (as viewed in Excel). For an example with multiple cells, see the [**Snapshots**](#snapshots) example from [**Programmatic Interface Examples**](#prog_interface_ex).

#### Other Files

`Box5-logic_circuit_transition_rules_compressed.txt` demonstrates a 46-rule compressed transition rule set that eschews "redundant" gates (i.e., AND, NOT, OR, and XOR are replaced by NOR), as alluded to in Box 5. This will NOT work directly with any of the initial states used here, as it uses a different set of gates.

## Chapter 5: Manufacturing

#### Manifests

* `Fig5a-rule_110_manifest.txt`: Stephen Wolfram's Rule 110, computed forward in time from top to bottom, as shown in Fig. 5a.
* `Fig5b-blossom_manifest.txt`: Grows a 32-molecule, irregularly-shaped blossom, as in Fig. 5b. This will produce a different shape with each run, but every shape will have exactly 32 blossom sites.
* `Fig5c-random_line_manifest.txt`: Simple random-walking line, as in Fig. 5c.
* <a name="line_ex"></a>`Fig5d-straight_line_manifest.txt`: Builds an infinite-length, width-2 straight line, as in Fig. 5d.
* `Fig5e-bitmap_image_manifest.txt`: Builds a bitmap-specified picture of a butterfly, as shown in Fig. 5e. This manifest is generated by `make_rastered_image_crn.py` -- edit and run that file to make other bitmap patterns.

#### Other Files

You can generate surface CRNs to make your own bitmap patterns by modifying and running `make_rastered_image_crn.py`. Change the `image` array at the top of the file to use the same colors as the butterfly; edit lines 108-113 to define your own colors. The script will generate a manifest that can be run with the simulator.


## Chapter 6: Robots and Swarms

#### Manifests

* `Fig6a-anthill_manifest.txt`: Simulates a simple mound-building algorithm, as shown in Fig. 6a.
* <a name="ants_ex"></a>`Fig6b-scouting_ant_manifest.txt`: Simulates a simple food-finding ant with minimal trap-avoidance rules, as shown in Fig. 6b.
* `Fig6c-cargo_sorter_manifest.txt`: Simulates a spatial sorting algorithm that gathers two different materials into piles, as shown in Fig. 6c.

## Chapter 7: Rugby

#### Manifests

* `Fig7-rugby_manifest.txt`: Simulates a game of molecular rugby using two particularly simple strategies, as shown in Fig. 7. Edit lines 55-104 to change the teams' strategies ("[rugby gods edit here]"). See the [**Rugby_Competition**](#rugby_ex) example from [**Programmatic Interface Examples**](#prog_interface_ex) for code to run a round-robin tournament between different strategies.


<a name="other_ex"></a>Other Examples
==============

* `alternate_line_builder.txt`: A different [straight line builder](#line_ex) example designed by Philip Peterson. This version requires more rules and states than the one in the paper, and uses a much larger head, but builds a line of width 1 (instead of width 2).
* `Brusselator.txt`: Surface CRN implementation of the autocatalytic Brusselator chemical oscillator. Classically, this oscillator is described as a CRN with the following rules (see the manifest file for implementation details):
    * A -> X
    * X + X + Y -> X + X + X
    * B + X -> Y + D
    * X -> E
* `busy_beaver.txt`: 3-state, 2-symbol [Busy Beaver Turing machine](https://en.wikipedia.org/wiki/Busy_beaver).
* `ertl.txt`: Manifest file for an Ertl chemical oscillator (https://doi.org/10.1021/cr00035a012). Carbon monoxide and molecular oxygen adsorb to a crystal platinum catalyst, and can diffuse on it. Adjacent CO and O will convert to carbon dioxide and desorb. Together, these dynamics cause patterned oscillations.
* `game_of_life_5x5_circuit.txt`: A larger version of the [circuit-based Game of Life implementation](#gol_ex) from Chapter 4. This shows a 5x5 grid of synchronized Game of Life cells. The small circuits on the fringes of the grid are mock cells that eat any outgoing signals and provide a dummy "0" signal.
* `game_of_life_one_to_one.txt`: A custom one-to-one implementation of the Game of Life not shown in Chapter 4. This implementation uses a rastering strategy, in which a robot walking along the outside of the game board sends signals top-to-bottom, left-to-right, to count vertical and horizontal neighbors, respectively. See the manifest for details. This strategy is as spatially compact as the spinning-arrow strategy with far fewer transition rules, but has an update speed that scales with the total size of the game board.
* `smarter_scout_ant.txt`: A smarter version of the [food-finding scout ant](#ants_ex) from Chapter 6.. This ant puts down "guard rails" to avoid crossing over its own path, and can give up, undo its trail, and start again if it gets stuck.
* `GH_big_spiral.txt`: A 750x750 Greenberg-Hastings oscillator surface CRN, as shown in the third column of Fig. 1d but on a much larger scale. At this size, spiral patterns are persistent for some time before devolving into chaotic patterns reminiscent of the Belousov-Zhabotinsky reaction. Be patient with this one -- it may take a couple of minutes to load.
* `Majority Vote`: Spatial majority vote, in which self-catalyzing "0"s and "1"s compete to cover a surface. In the limit of infinite time with an infinite surface, the entire surface will become covered with whichever state ("0" or "1") has the most representatives at the beginning of the simulation. In practice, convergence can take quite a while, and the surface CRN produces striking patterns in the meantime. We include three different majority vote examples:
* * `majority_asynchronous.txt`: A simple implementation with no synchronicity.
* * `majority_synchronous_large.txt`: A synchronous version of the majority-vote automaton, implemented with the spinning arrow strategy from Chapter 3. This is a large field, zoomed out so you can see its patterns better.
* * `majority_synchronous_small.txt`: The same system as in `majority_synchronous_large.txt`, but zoomed in with state labels, so you can better see the operation of the spinning arrow mechanism.
* * `molecular_walker.txt`: Simple emulation of a burnt-bridge, one-way DNA robot (or other molecular walker). The walker moves along a track, converting track to spent waste as it goes.
* * `parens_matcher.txt`: A Turing machine that checks whether a string contains matched open and closed parentheses ("OP" and "CL", respectively).
* * `sierpinski_1D_synch.txt`: Surface CRN implementation of a 1-dimensional XOR blocked cellular automaton. After each step, a cell in the automaton is 1 if and only if exactly one of its neighbors was 1 in the last step.
* * `sorting_asynch.txt`: An asynchronous bubble sort on a 1D tape. Each position is labeled with the a marker "A", "B", or "C" in order to distinguish between left and right.
* * `sorting_synch.txt`: A synchronous bubble sort on a 1D tape.
* * `sqrt_circuit.txt`: A 4-bit square-root circuit, implemented with the logic rules from [Chapter 4](#logic_ex). Input starts at the left edge (read bottom-to-top, most- to least-significant). Output bits go to the bottom (most significant digit) and left (least-significant digit).