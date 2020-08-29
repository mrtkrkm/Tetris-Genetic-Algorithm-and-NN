import numpy as np

class Selections(object):
    def __init__(self, type):
        self.ctype=type

    def cross_over_func(self):
        pass

def random_selection(best_chromosomes, number_parents):
    p1 = np.random.randint(0, number_parents, 1)[0]
    parent1 = best_chromosomes[p1]

    p2 = p1
    while p2 == p1:
        p2 = np.random.randint(0, number_parents, 1)[0]

    parent2 = best_chromosomes[p2]

    return parent1, parent2

def roulette_selection(best_chromosomes,fitness_scores, inds, number_parents):
    scores = [fitness_scores[ind] for ind in inds]
    total_score = sum(scores)

    scores = np.asarray(scores) / total_score
    scores = np.cumsum(scores)

    # scores=list(scores)

    rand1 = np.random.uniform(size=1)[0]
    our_cond = np.argmin(scores < rand1)
    #get_ind = inds[our_cond]
    parent1 = best_chromosomes[our_cond]

    rand2=rand1
    while rand2 == rand1:
        rand2 = np.random.uniform(size=1)[0]


    our_cond = np.argmin(scores < rand2)
    #get_ind = inds[our_cond]
    parent2 = best_chromosomes[our_cond]

    return parent1, parent2