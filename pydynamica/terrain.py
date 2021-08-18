
import matplotlib.pyplot as plt
import multiprocessing

import numpy as np
import pydynamica.perlin as perlin

from enum import Enum
class Resources(Enum):
    empty = 0
    mineral = 1
    food = 2

def calculate_dominant(dominant_arr) -> int:
    return np.argmax(dominant_arr)

def calculate_abundance(dominant_arr) -> float:
    return (dominant_arr[np.argmax(dominant_arr)] +0.5) * 100

def create_grid_world_parallel(x:int, y:int) -> np.array:
    mineral_map = perlin.create_perlin(x, y).flatten()
    food_map = perlin.create_perlin(x, y).flatten()
    empty_map = perlin.create_perlin(x,y).flatten()

    inp = np.dstack((empty_map, mineral_map, food_map))[0]

    pool = multiprocessing.Pool()
    key_map = pool.map(calculate_dominant, inp)
    abundance_map = pool.map(calculate_abundance, inp)
    pool.close()

    return np.array(key_map).reshape((x,y)), np.array(abundance_map).reshape((x, y))

def create_grid_world(x:int, y:int) -> np.array:
    mineral_map = perlin.create_perlin(x, y)
    food_map = perlin.create_perlin(x, y)
    empty_map = perlin.create_perlin(x,y)

    key_map = np.empty((x, y))
    abundance_map = np.empty((x, y))

    for i in range(x):
        for j in range(y):
            dominant = [empty_map[i][j],
                    mineral_map[i][j],
                    food_map[i][j]]
            key_map[i][j] = np.argmax(dominant)
            abundance_map[i][j] = (dominant[key_map[i][j]] + 0.5) * 100

    return key_map, abundance_map

if __name__ == "__main__":
    normal_key, abundance_map = create_grid_world(100, 100)
    normal_key_p, abundance_map_p = create_grid_world_parallel(100,100)

    plt.imshow(world)
    plt.show()
 
