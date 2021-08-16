import timeit

import terrain

def bench_terrain():
    to_benchmark = [terrain.create_grid_world_parallel,
            terrain.create_grid_world]
    
    for func in to_benchmark:
        print(f"Benching {func.__name__}...")
        time = timeit.timeit(lambda: func(1000, 1000), number=1)
        print(f"{func.__name__} took {str(time)}s\n")

if __name__ == "__main__":
    bench_terrain()

