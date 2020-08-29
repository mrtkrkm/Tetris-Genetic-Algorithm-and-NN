from GA.CrossoverTypes import CrossOverTypes as ctypes
import numpy as np

def select_best_chromosomes(scores, number_parents, population):
    temp_score = -9999
    best_chromosomes = []
    inds = []
    for i in range(number_parents):
        max_index = scores.index(max(scores))
        max_parents = population[max_index]
        scores[max_index] = temp_score
        best_chromosomes.append(max_parents)
        inds.append(max_index)
    return best_chromosomes, inds


def generate_points(population, ctype):
    num_weights = population.shape[1]
    start = 6
    end = num_weights - 5
    if ctype == ctypes.One_Point:
        return list(np.random.choice(range(start, end, 1), 1))
    elif ctype == ctypes.Two_Point:
        return list(np.random.choice(range(start, end, 2), 1, replace=False))