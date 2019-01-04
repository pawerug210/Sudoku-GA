import numpy as np
import json
from collections import namedtuple


def readFile(filename):
    data = np.genfromtxt(filename, delimiter=',', filling_values=0, dtype=int)
    if data.shape != (9, 9):
        raise ValueError('Input Sudoku is wrong size')
    return data


def printPopulationDetails(generation, population):
    print(str.format('Generation {0}, best fitness {1}, worst fitness {2}', generation, population[0].fitness,
                     max([x.fitness for x in population])))

def getParams(filename):
    with open(filename) as f:
        data = json.load(f)
    return namedtuple("params", data.keys())(*data.values())