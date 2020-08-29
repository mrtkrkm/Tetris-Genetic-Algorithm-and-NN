from Tetris import main as gameMain
from Tetris import AI_tetris as aiplay
from GeneticAlgorithm.Steps import GeneticAlgorithm
import numpy as np
from NeuralNetwork.FeedForward import NN
from GeneticAlgorithm.CrossoverTypes import CrossOverTypes as ctypes
from GeneticAlgorithm.SelectionTypes import SelectionTypes as stypes

if __name__ == "__main__":

    #To play by yourself
    #gameMain.main_func()


    input_number = 4
    hidden_number = 4
    output1_number = 4
    output2_number = 10

    pop_size = 20
    Cross_over_types=ctypes.One_Point
    Selection_type=stypes.Roulette
    num_generation=10
    num_parents=4

    size_w = input_number * hidden_number + hidden_number* output1_number + hidden_number * output2_number
    size = (pop_size, size_w)
    population = np.random.choice(np.arange(-1, 1, step=0.01), size=size, replace=True)

    network=NN(input_number, hidden_number,output1_number, output2_number)

    Genetic=GeneticAlgorithm(population, network, num_generation, num_parents, Cross_over_types, Selection_type)

    Genetic.start_process()

