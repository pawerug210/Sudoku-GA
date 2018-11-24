from common import readFile
import SudokuGA
import GeneticAlgorithmHelper as helper


helper = helper.GenericAlgorithmHelper()
populationSize = 50
data = readFile('test_1').flatten().tolist()
SudokuGA.SudokuGA.sudokuFixedDigitsArray = [x > 0 for x in data]
population = [SudokuGA.SudokuGA(data) for i in range(0, populationSize)]
solved = False
generation = 0
while not solved:
    generation += 1
    offspring = helper.select(population)
    offspring = helper.crossover(offspring)
    helper.mutate(offspring, 1)
    population = helper.replace(population, offspring, 0.8)
    print(population)
