from common import readFile
import SudokuGA
import GeneticAlgorithmHelper as helper
import sys

rf = 0.9

helper = helper.GenericAlgorithmHelper()
populationSize = 12
data = readFile('test_1').flatten().tolist()
SudokuGA.SudokuGA.sudokuFixedDigitsArray = [x > 0 for x in data]
population = [SudokuGA.SudokuGA(data) for i in range(0, populationSize)]
solved = False
generation = 0
resetCounter = 0
best = sys.maxsize
while not solved:
    generation += 1
    offspring = helper.select(population)
    offspring = helper.crossover(offspring)
    helper.mutate(offspring, 0.1)
    population = helper.replace(population, offspring, rf)
    print(generation, population)
    currentBest = population[0].fitness
    if currentBest < best:
        best = currentBest
        resetCounter = 0
    else:
        resetCounter += 1
    if best == 0:
        solved = True
    rf = 0.9
    if resetCounter >= 1500:
        best = sys.maxsize
        resetCounter = 0
        rf = 1.0

population[0].draw()