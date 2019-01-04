import abc


class Chromosome(object):

    fitness = None

    @abc.abstractclassmethod
    def getFitness(self):
        pass

    @abc.abstractclassmethod
    def updateFitness(self):
        pass

    @abc.abstractclassmethod
    def mutate(self, pm):
        pass

    @abc.abstractclassmethod
    def crossover(self, other, bounds, pc):
        pass

    def __str__(self):
        return str(self.fitness)

    def __repr__(self):
        return str(self.fitness)
