import Sudoku
import Chromosome
import random


class SudokuGA(Sudoku.Sudoku, Chromosome.Chromosome):

    def __init__(self, sudoku):
        super(SudokuGA, self).__init__(sudoku)
        self.fitness = self.calculateFitness()

    def getError(self, chromosome):
        return len(self.NUMBERS) - len(set(chromosome))

    def calculateFitness(self):
        error = 0
        for i in range(0, 9):
            error += self.getError(self.getRow(self.sudokuDigitsArray, i)) + \
                     self.getError(self.getColumn(self.sudokuDigitsArray, i)) + \
                     self.getError(self.getSquare(self.sudokuDigitsArray, i))
        self.fitness = error
        return self.fitness

    def doublePointCrossover(self, other, bounds, pc):
        firstChildDigits = self.sudokuDigitsArray[:]
        secondChildDigits = other.sudokuDigitsArray[:]
        if pc > random.random():
            for i in range(0, self.SEGMENT_LENGTH):
                listOffspring = self.listDoublePointCrossover(self.getDigitsRow(i)[0], other.getDigitsRow(i)[0], i,
                                                              bounds)
                firstChildDigits += listOffspring[0]
                secondChildDigits += listOffspring[1]
        return SudokuGA(firstChildDigits), SudokuGA(secondChildDigits)

    def listDoublePointCrossover(self, mom, dad, rowNumber, bounds):
        if len(mom) != len(dad):
            raise Exception
        leftBound = bounds[0] if bounds[0] > 0 else 1
        rightBound = bounds[1]
        firstChild = self.getRowWithFixedValues(mom, rowNumber)
        secondChild = self.getRowWithFixedValues(mom, rowNumber)
        firstChild[leftBound: rightBound] = mom[leftBound:rightBound]
        secondChild[leftBound: rightBound] = dad[leftBound:rightBound]
        firstChild = self.fillZeros(firstChild, dad)
        secondChild = self.fillZeros(secondChild, mom)
        return firstChild, secondChild