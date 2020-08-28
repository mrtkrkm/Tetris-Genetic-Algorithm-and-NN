import numpy as np
import Tetris.AI_tetris as aiPlay
from GA.CrossoverTypes import CrossOverTypes as ctypes
class GeneticAlgorithm(object):

    def __init__(self, population, NN, generation, parents, ctype):
        self.population=population
        self.NN=NN
        self.number_generation=generation
        self.number_parents=parents
        self.number_steps=30
        self.number_games=1
        self.ctype=ctype


    def __calculate_fitness(self):
        scores=[]
        for i in range(len(self.population)):
            score=aiPlay.ai_playing(self.number_games, self.number_steps,self.population[i,:], self.NN)
            scores.append(score)
            print(f'The score of {i}th chromosome is {score}')
        return scores

    def __select_best_chromosomes(self, scores):
        temp_score=-9999
        best_chromosomes=[]
        for i in range(self.number_parents):
            max_index=scores.index(max(scores))
            max_parents=self.population[max_index]
            scores[max_index]=temp_score
            best_chromosomes.append(max_parents)
        return best_chromosomes

    def __select_parents(self, best_chromosomes):
        p1=np.random.randint(0,self.number_parents,1)
        parent1 = best_chromosomes[p1]

        p2=p1
        while p2==p1:
            p2=np.random.randint(0, self.number_parents,1)

        parent2=best_chromosomes[p2]

        return parent1, parent2


    def __generate_points(self):
        num_weights = self.population.shape[1]
        start=6
        end=num_weights-5
        if self.ctype == ctypes.One_Point:
            return list(np.random.choice(range(start,end,1),1))
        elif self.ctype==ctypes.Two_Point:
            return list(np.random.choice(range(start, end, 2), 1, replace=False))



    def __cross_over(self, best_chromosomes, number_chromosome):
        num_weights = self.population.shape[1]
        new_chromosomes=[]
        for i in range(number_chromosome/2):
            points = self.__generate_points()
            parent1, parent2 = self.__select_parents(best_chromosomes)

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
            rand_gen_val = np.random.choice(np.arange(-1, 1, step=0.001), size=(1), replace=False)
            for i in range(gen_number):
                chromosome[starting_point+i]=chromosome[starting_point+i]+rand_gen_val

        return chromosome



    def start_process(self):

        for i in range(self.number_generation):
            print('#'*20+f'{i}th Generation'+'#'*20)
            fitness_scores=self.__calculate_fitness()

            print(f'Best score is {max(fitness_scores)}')

            best_chromosomes=self.__select_best_chromosomes(fitness_scores)

            new_chromosomes=self.__cross_over(best_chromosomes,self.population.shape[0]-self.number_parents)

            self.population[:self.number_parents,:]=best_chromosomes
            self.population[self.number_parents:, :]=new_chromosomes









