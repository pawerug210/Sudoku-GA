import abc


class Chromosome(object):

    def __init__(self):
        self.fitness = None

    @abc.abstractclassmethod
    def getFitness(self):
        return self.fitness

    @abc.abstractclassmethod
    def updateFitness(self):
        pass

    @abc.abstractclassmethod
    def mutate(self, pm):
        pass

    @abc.abstractclassmethod
    def crossover(self, other, pc):
        pass

    def __str__(self):
        return str(self.fitness)

    def __repr__(self):
        return str(self.fitness)
