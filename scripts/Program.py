from common import readFile
from common import printPopulationDetails
from common import getParams
import SudokuGA
import GeneticAlgorithmHelper


def solveSudoku(filename):
    helper = GeneticAlgorithmHelper.GenericAlgorithmHelper()
    params = getParams('params.json')
    data = readFile(filename).flatten().tolist()
    SudokuGA.SudokuGA.sudokuFixedDigitsArray = [x > 0 for x in data]
    solved = False
    generation = 0
    while not solved:
        print('New random population')
        population = [SudokuGA.SudokuGA(data) for i in range(0, int(params.populationSize))]
        while not solved:
            generation += 1
            offspring = helper.select(population, int(params.tournamentSize))
            offspring = helper.crossover(offspring, float(params.pc))
            helper.mutate(offspring, float(params.pm))
            population = helper.replace(population, offspring, float(params.rf))
            currentBest = population[0].fitness
            if currentBest == 0:
                solved = True
            if helper.shouldRestart(currentBest, generation, float(params.restartCriteria)):
                break
            printPopulationDetails(generation, population)
    population[0].draw()


def main():
    solveSudoku('test_3')


if __name__ == "__main__":
    main()