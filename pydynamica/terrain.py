
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


def create_grid_world_parallel(x:int, y:int) -> np.array:
    mineral_map = perlin.create_perlin(x, y).flatten()
    food_map = perlin.create_perlin(x, y).flatten()
    empty_map = perlin.create_perlin(x,y).flatten()

    inp = np.dstack((empty_map, mineral_map, food_map))[0]

    pool = multiprocessing.Pool()
    results = pool.map(calculate_dominant, inp)
    pool.close()

    return np.array(results).reshape((x,y))

def create_grid_world(x:int, y:int) -> np.array:
    mineral_map = perlin.create_perlin(x, y)
    food_map = perlin.create_perlin(x, y)
    empty_map = perlin.create_perlin(x,y)

    map = np.empty((x, y))

    for i in range(x):
        for j in range(y):
            dominant = [empty_map[i][j],
                    mineral_map[i][j],
                    food_map[i][j]]
            map[i][j] = np.argmax(dominant)

    return map

if __name__ == "__main__":
    normal = create_grid_world(100, 100)
    world = create_grid_world_parallel(100,100)

    plt.imshow(world)
    plt.show()
 
