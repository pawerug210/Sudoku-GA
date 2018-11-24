import numpy as np


def readFile(filename):
    data = np.genfromtxt(filename, delimiter=',', filling_values=0, dtype=int)
    if data.shape != (9, 9):
        raise Exception
    return data