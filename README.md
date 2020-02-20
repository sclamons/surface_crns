# Simulation of Chemical Reaction Networks (CRNs) on a surface

This package is for simulating surface CRNs, as defined in Qian &
Winfree 2014 ("Parallel and Scalable Computation and Spatial Dynamics
with DNA-Based Chemical Reaction Networks on a Surface").

This package provides:

  - A core simulator for simulating surface CRNs on arbitrary graphs.
  - Models and views for square-grid and hex-grid surface CRNs.
  - A manifest-reading system to simplify setting up new surface CRNs.
  - A pygame-powered GUI for visualizing square-grid and hex-grid
    surface CRNs.

# Prerequisites

This package is for Python 2 only. It does not support Python 3.

The GUI simulator requires pygame. Installing surface\_crns with pip, as
described below, should also install pygame.

# Installation

Install with the following (probably requires superuser privilege): `pip
install git+git://github.com/sclamons/surface_crns.git@master`

To update, run (also with superuser privilege): `pip install --upgrade
--no-deps git+git://github.com/sclamons/surface_crns.git@master`

If you are using OSX and you get an error while installing surface\_crns
or pygame, you may need to install several SDL libraries used by pygame.
Install them with brew (<https://brew.sh/>) with the command:

`brew install sdl sdl_image sdl_mixer sdl_ttf portmidi`

# What's a surface CRN?

In brief, a surface CRN is a chemical reaction network where individual
molecules are tethered to positions on a surface; or, alternatively, a
surface CRN is an asynchronous cellular automata with transition rules
that resemble those of unimolecular and bimolecular chemical reactions.

A surface CRN consists of a number of sites with states on an arbitrary
lattice (often a grid, but possibly any graph), along with transition
rules of the form `A -> B` or `A + B -> C + D`, with a real-valued
reaction rate for each transition rule. States change stochastically
according to the transition rules for the surface CRN, with expected
time specified by the reaction rate for each reaction.

For example, a site with state `A` can undergo `A -> B` to
instantaneously switch to state `B`.

Bimolecular reactions (of the form `A + B -> C + D`) can occur only if
*both* of the species before the arrow are present and next to each
other on the lattice (note that there is no "directionality" inherent to
the surface, so an `A` next to a `B` is equivalent to a `B` next to an
`A`). When a bimolecular reaction occurs, the first reactant
instantaneously becomes the first product, and the second reactant
simultaneously and becomes the second product, so the states `A B` would
become `C D` (or, equivalently, `B A` would become `D C`).

What can you do with a surface CRN? Some examples are shown in Qian and
Winfree 2014; See what you can make\!

# How do I use the simulator?

The fastest way to start