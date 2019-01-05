import random
import math


class GenericAlgorithmHelper(object):

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
            winners.append(group[fitnesses.index(min(fitnesses))])
        return winners

    def mutate(self, population, pm):
        for individual in population:
            individual.mutate(pm)
            individual.updateFitness()

    def crossover(self, population, pc):
        offsprings = []
        for i in range(0, len(population), 2):
            mom, dad = population[i: i + 2]
            offsprings += dad.crossover(mom, pc)
        return offsprings

    def replace(self, parents, offspring, replacementFraction):
        parents.sort(key=lambda x: x.fitness)
        quantityToReplace = math.floor(len(parents) * replacementFraction)
        return sorted(parents[0: len(parents) - quantityToReplace] + offspring[0: quantityToReplace], key=lambda x: x.fitness)

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
