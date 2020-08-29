import numpy as np
import Tetris.AI_tetris as aiPlay
from GeneticAlgorithm.CrossoverTypes import CrossOverTypes as ctypes
import GeneticAlgorithm.SelectionFunc as cfunc
import GeneticAlgorithm.Utils as gutils


class GeneticAlgorithm(object):
    def __init__(self, population, NN, generation, parents, ctype, stype):
        self.population=population
        self.NN=NN
        self.number_generation=generation
        self.number_parents=parents
        self.number_steps=30
        self.number_games=1
        self.ctype=ctype
        self.stype=stype


    def __calculate_fitness(self):
        scores=[]
        for i in range(len(self.population)):
            score=aiPlay.ai_playing(self.number_games, self.number_steps,self.population[i,:], self.NN)
            scores.append(score)
            print(f'The score of {i}th chromosome is {score}')
        return scores



    def __cross_over(self, best_chromosomes, number_chromosome):
        num_weights = self.population.shape[1]
        new_chromosomes=[]
        for i in range(number_chromosome//2):
            #points = self.__generate_points()
            points=gutils.generate_points(self.population,self.ctype)
            parent1, parent2=cfunc.roulette_selection(best_chromosomes,self.fitness_scores,self.inds,self.number_parents)
            parent1=list(parent1)
            parent2=list(parent2)
            if self.ctype==ctypes.One_Point:
                child_1=parent1[:points[0]]+parent2[points[0]:]
                child_2=parent2[:points[0]]+parent1[points[0]:]

                child_1 = self.__mutation(child_1)
                child_2 = self.__mutation(child_2)

                new_chromosomes.append(child_1)
                new_chromosomes.append(child_2)

            elif self.ctype==ctypes.Two_Point:
                child_1 = parent1[:points[0]] + parent2[points[0]:points[1]]+parent1[points[1]:]
                child_2 = parent2[:points[0]] + parent1[points[0]:points[1]]+parent2[points[1]:]

                child_1=self.__mutation(child_1)
                child_2 = self.__mutation(child_2)

                new_chromosomes.append(child_1)
                new_chromosomes.append(child_2)

        return np.asarray(new_chromosomes)


    def __mutation(self, chromosome):
        max_gen=15
        min_gen=5
        gen_number=np.random.randint(min_gen, max_gen,1)

        starting_point=np.random.randint(0,self.population.shape[1]-gen_number,1)

        limit=0.005
        random_number=np.random.rand(1)
        if random_number<limit:
            rand_gen_val = np.random.choice(np.arange(-1, 1, step=0.001), size=(1), replace=False)[0]
            for i in range(rand_gen_val):
                chromosome[starting_point+i]=chromosome[starting_point+i]+rand_gen_val

        return chromosome



    def start_process(self):

        for i in range(self.number_generation):
            print('#'*20+f'{i}th Generation'+'#'*20)
            self.fitness_scores=self.__calculate_fitness()

            print(f'Best score is {max(self.fitness_scores)}')

            #best_chromosomes=self.__select_best_chromosomes(self.fitness_scores)

            best_chromosomes, self.inds = gutils.select_best_chromosomes(self.fitness_scores,self.number_parents, self.population)

            new_chromosomes=self.__cross_over(best_chromosomes,self.population.shape[0]-self.number_parents)

            self.population[:self.number_parents,:]=best_chromosomes
            self.population[self.number_parents:, :]=new_chromosomes









