'''
Algorithmically generates a large number of random colors, which will be used
as random colors by random_color.py

Modified from code for generating stochastically random colors with decent distinguishability,
written by adews. Code taken from https://gist.github.com/adewes/5884820.

Modified to produce colors in a range of 0-255, instead of 0-1

From the author:
A small Python script to generate random color sequences, e.g. for use in
plotting. Just call the "generate_new_color(existing_colors,pastel_factor)"
function to generate a random color that is (statistically) maximally different
from all colors in "existing_colors". The "pastel_factor" parameter can be used
to specify the "pasteliness"(?) of the produced colors (please, don't you chose
0...)
'''
import random
import numpy as np

def get_random_color(pastel_factor = 0.5):
    return [255*(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

def color_distance(c1,c2):
    return np.linalg.norm(np.array(c1) - np.array(c2))
    #return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

def generate_new_color(existing_colors,pastel_factor = 0.5):
    if not existing_colors:
        return get_random_color(pastel_factor = pastel_factor)
    max_distance = None
    best_color = None

    candidates = [get_random_color(pastel_factor = pastel_factor) \
                    for i in range(100)]
    min_distances = [min([color_distance(color,c) for c in existing_colors]) \
                        for color in candidates]
    return candidates[min_distances.index(max(min_distances))]

    # for i in range(0,100):
    #     color =
    #     best_distance =
    #     if not max_distance or best_distance > max_distance:
    #         max_distance = best_distance
    #         best_color = color
    # return best_color

def main():
    colors = []
    for i in range(100):
        colors.append(generate_new_color(colors))
    with open("random_color_list.txt", "w") as colorfile:
        for color in colors:
            colorfile.write(str(color) + "\n")

if __name__ == "__main__":
    main()