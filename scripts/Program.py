from common import readFile
import SudokuGA
import GeneticAlgorithmHelper as helper


helper = helper.GenericAlgorithmHelper()
populationSize = 24
data = readFile('test_1').flatten().tolist()
SudokuGA.SudokuGA.sudokuFixedDigitsArray = [x > 0 for x in data]
population = [SudokuGA.SudokuGA(data) for i in range(0, populationSize)]
solved = False
generation = 0
while not solved:
    generation += 1
    offspring = helper.select(population)
    offspring = helper.crossover(offspring)
    helper.mutate(offspring, 0.01)
    population = helper.replace(population, offspring, 0.95)
    print(population)
    # if True:
    #     print(population[0])
    #     print(population[1])
    #     print(population[2])
    #     print(population[3])
    #     break
