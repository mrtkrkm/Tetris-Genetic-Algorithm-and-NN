This is a Tetris AI Implemantation by using Genetic Algorithm and Neural Network.

For genetic algorithm the following methods selected

 `Selection`
1. Best `number_of_parents` selected based on their fitness result
2. Best `number_of_parents` chromosomes selected for next generation. AKA `elitist selection`
3. In order to chose 2 parents `Roulette Wheel Selection` used on Best chromosomes

`Cross-Over`
- One point Crossover method was used.

`Mutation`
1. `Max_gen` and `min_gen` number selected 
2. Random gen number was selected between `min_gen` and `Max_gen`
3. Mutation rate was selected as `0.005`
4. Selected genes was changed by adding random number

For neural network `Multi Output Feed Forward Network` was selected.
The architecture of NN is:

	-Input Layer
	-Hidden1 Layer
	-Hidden2 Layer
-Output1 Layer     -Output2Layer
 
In order to play Tetris by yourself make following changes in the `run.py` 

```
#gameMain.main_func()
```
to
```
gameMain.main_func()
```