from common import readFile
import SudokuGA
import GeneticAlgorithmHelper as helper


populationSize = 50
pm = 0.1
pc = 0.2
rf = 0.7  # replacement fraction


helper = helper.GenericAlgorithmHelper()
data = readFile('test_4').flatten().tolist()
SudokuGA.SudokuGA.sudokuFixedDigitsArray = [x > 0 for x in data]
population = [SudokuGA.SudokuGA(data) for i in range(0, populationSize)]
solved = False
generation = 0
while not solved:
    generation += 1
    offspring = helper.select(population)
    offspring = helper.crossover(offspring, pc)
    helper.mutate(offspring, pm)
    population = helper.replace(population, offspring, rf)
    print(population)
    if population[0].fitness < 2:
        population[0].draw()