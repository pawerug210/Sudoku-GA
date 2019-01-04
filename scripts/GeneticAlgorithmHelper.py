import random
import math


class GenericAlgorithmHelper(object):

    AdaptiveMutationFactor = 0.3
    CurrentBest = 100000  # bigger value than possible
    LastChange = 0  # iteration when last time something changed

    def select(self, population, tournamentSize):
        groups = self.group(population, tournamentSize)
        return self.tournament(groups)

    def group(self, population, groupSize):
        if len(population) % groupSize != 0:
            raise ValueError('Population size is not divisible by tournament size')
        pop_copy = population[:]
        groups = []
        for j in range(groupSize):
            random.shuffle(pop_copy)
            groups += [pop_copy[i * groupSize: (i + 1) * groupSize] for i in range(int(len(pop_copy) / groupSize))]
        return groups

    def tournament(self, groups):
        winners = []
        for group in groups:
            fitnesses = [x.fitness for x in group]
            minFitnessIndex = fitnesses.index(min(fitnesses))
            winners.append(group[minFitnessIndex])
        return winners

    def mapValue(self, value, range):
        return int(math.floor((value - 0) / (1 - 0) * (range[1] - range[0]) + range[0]))

    def mutate(self, population, pm):
        for individual in population:
            self.mutateIndividual(individual, pm)

    def mutateIndividual(self, individual, pm):
        for i in range(0, 9):
            valuesRow, isFixedRow = individual.getDigitsRow(i)
            problemIndexes = individual.getProblemIndexes(i)
            notFixedIndexes = [i for i, val in enumerate(isFixedRow) if not val]
            if len(notFixedIndexes) > 1:
                for j in range(0, len(notFixedIndexes)):
                    if pm + self.AdaptiveMutationFactor * problemIndexes[notFixedIndexes[j]] > random.random():
                        rand = random.random()
                        index = self.mapValue(rand, (0, len(notFixedIndexes) - 1))
                        # different value than j
                        valueFromIndexDifferentThanJ = (notFixedIndexes[:j] + notFixedIndexes[j + 1:])[index]
                        if notFixedIndexes[j] != valueFromIndexDifferentThanJ:
                            swapIndexes = [notFixedIndexes[j], valueFromIndexDifferentThanJ]
                            if swapIndexes[0] == swapIndexes[1]:
                                raise Exception
                            # swapIndexes = random.sample(notFixedIndexes, 2)
                            valuesRow[swapIndexes[1]], valuesRow[swapIndexes[0]] = valuesRow[swapIndexes[0]], valuesRow[swapIndexes[1]]
                            individual.setValue(i, swapIndexes[0], valuesRow[swapIndexes[0]])
                            individual.setValue(i, swapIndexes[1], valuesRow[swapIndexes[1]])
                        else:
                            raise Exception
        individual.update()

    def crossover(self, population, pc):
        offsprings = []
        for i in range(0, len(population), 2):
            mom, dad = population[i: i + 2]
            bounds = self.getTwoBounds(mom.SEGMENT_LENGTH)
            offsprings += dad.doublePointCrossover(mom, bounds, pc)
        return offsprings

    def replace(self, parents, offspring, replacementFraction):
        parents.sort(key=lambda x: x.fitness)
        individualsNumberToReplace = math.floor(len(parents) * replacementFraction)
        return parents[0: len(parents) - individualsNumberToReplace] + offspring[0: individualsNumberToReplace]


    def getError(self, chromosome):
        return len(self.NUMBERS) - len(set(chromosome))

    def getRowWithFixedValues(self, values, mask):
        rowWithFixedValues = map(lambda value, isFixed: value if isFixed else 0, values, mask)
        return list(rowWithFixedValues)

    def getTwoBounds(self, size):
        firstBound = random.randint(1, size - 1)
        secondBound = (firstBound + int(size / 3)) % (size - 1)
        bounds = sorted([firstBound, secondBound])
        return bounds

    def shouldRestart(self, currentBest, iteration, restart):
        if currentBest < self.CurrentBest:
            self.CurrentBest = currentBest
            self.LastChange = iteration
            return False
        if iteration - self.LastChange >= restart:
            self.LastChange = iteration
            self.CurrentBest = 1000000
            return True
        return False
