import abc


class Chromosome(object):

    fitness = None

    @abc.abstractclassmethod
    def fitness(self):
        pass

    @abc.abstractclassmethod
    def updateFitness(self):
        pass

    def __str__(self):
        return str(self.fitness)

    def __repr__(self):
        return str(self.fitness)
