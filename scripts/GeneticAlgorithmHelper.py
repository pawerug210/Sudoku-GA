import random
import math


class GenericAlgorithmHelper(object):

    def select(self, population):
        pairs = self.pair(population)
        return self.tournament(pairs)

    def pair(self, population):
        if len(population) % 2 != 0:
            raise Exception
        pop_copy = population[:]
        # getting random pairs
        random.shuffle(pop_copy)
        pairs = [pop_copy[i*2: (i+1)*2] for i in range(int(len(pop_copy) / 2))]
        random.shuffle(pop_copy)
        pairs += [pop_copy[i*2: (i+1)*2] for i in range(int(len(pop_copy) / 2))]
        return pairs

    def tournament(self, pairs):
        winners = []
        for pair in pairs:
            winners.append(pair[0] if pair[0].fitness < pair[1].fitness else pair[1])
        return winners

    def mapValue(self, value, range):
        return int(math.floor((value - 0) / (1 - 0) * (range[1] - range[0]) + range[0]))

    def mutate(self, population, pm):
        for individual in population:
            self.mutateIndividual(individual, pm)

    def mutateIndividual(self, individual, pm):
        for i in range(0, 9):
            valuesRow, isFixedRow = individual.getDigitsRow(i)
            notFixedIndexes = [i for i, val in enumerate(isFixedRow) if not val]
            if len(notFixedIndexes) > 1:
                for j in range(0, len(notFixedIndexes) - 1):
                    if pm > random.random():
                        rand = random.random()
                        index = self.mapValue(rand, (j + 1, len(notFixedIndexes)))
                        swapIndexes = [notFixedIndexes[j], notFixedIndexes[index]]
                        # swapIndexes = random.sample(notFixedIndexes, 2)
                        individual.setValue(i, swapIndexes[0], valuesRow[swapIndexes[1]])
                        individual.setValue(i, swapIndexes[1], valuesRow[swapIndexes[0]])
        individual.calculateFitness()

    def crossover(self, population):
        offsprings = []
        for i in range(0, len(population), 2):
            mom, dad = population[i: i + 2]
            offsprings += dad.doublePointCrossover(mom)
        return offsprings

    def replace(self, parents, offspring, replacementFraction):
        parents.sort(key=lambda x: x.fitness)
        # offspring.sort(key=lambda x: x.fitness)
        individualsToReplace = math.floor(len(parents) * replacementFraction)
        return parents[0: len(parents) - individualsToReplace] + offspring[0: individualsToReplace]


    def getError(self, chromosome):
        return len(self.NUMBERS) - len(set(chromosome))

    def getRowWithFixedValues(self, values, mask):
        rowWithFixedValues = map(lambda value, isFixed: value if isFixed else 0, values, mask)
        return list(rowWithFixedValues)
