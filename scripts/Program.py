from common import readFile
import SudokuGA
import GeneticAlgorithmHelper as helper


restartEvery = 500
populationSize = 100
tournamentSize = 4
pm = 0.1
pc = 0.1
rf = 0.9  # replacement fraction


helper = helper.GenericAlgorithmHelper()
data = readFile('test_1').flatten().tolist()
SudokuGA.SudokuGA.sudokuFixedDigitsArray = [x > 0 for x in data]
solved = False
generation = 0
while not solved:
    print('New random population')
    population = [SudokuGA.SudokuGA(data) for i in range(0, populationSize)]
    while not solved:
        generation += 1
        offspring = helper.select(population, tournamentSize)
        offspring = helper.crossover(offspring, pc)
        helper.mutate(offspring, pm)
        population = helper.replace(population, offspring, rf)
        currentBest = population[0].fitness
        if currentBest == 0:
            solved = True
        if helper.shouldRestart(currentBest, generation, restartEvery):
            break
        print(generation, currentBest)

population[0].draw()
