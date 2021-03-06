import Sudoku
import Chromosome
import random
import math


class SudokuGA(Sudoku.Sudoku, Chromosome.Chromosome):

    ADAPTIVE_MUTATION_VALUE = 0.0

    def __init__(self, sudoku):
        Sudoku.Sudoku.__init__(self, sudoku)
        Chromosome.Chromosome.__init__(self)
        self.AdaptiveMutationMap = [0.0] * len(self.DigitsArray)
        self.updateFitness()

    # chromosome interface

    def updateFitness(self):
        error = 0
        for i in range(0, 9):
            column = self.getColumn(i)
            square = self.getSquare(i)
            columnError = self.getError(column)
            squareError = self.getError(square)
            error += columnError + squareError
        self.fitness = error

    def mutate(self, pm):
        self.updateAdaptiveMutation()
        for i in range(0, 9):
            self.mutateRow(i, pm)

    def crossover(self, other, pc):
        bounds = self.getTwoRandomBounds(self.SEGMENT_LENGTH)
        return self.doublePointCrossover(other, bounds, pc)

    # Chromosome interface end

    def mutateRow(self, rowNumber, pm):
        valuesRow = self.getRow(rowNumber)
        adaptiveMutationRow = self.getRow(rowNumber, self.AdaptiveMutationMap)
        notFixedIndexes = [i for i, val in enumerate(self.getRow(rowNumber, self.FIXED_DIGITS_MAP)) if not val]
        if len(notFixedIndexes) > 1:
            for j in range(0, len(notFixedIndexes)):
                if pm + adaptiveMutationRow[notFixedIndexes[j]] > random.random():
                    index = self.mapValue(random.random(), (0, len(notFixedIndexes) - 1))
                    # different index value than j
                    differentIndexValueThanJ = (notFixedIndexes[:j] + notFixedIndexes[j + 1:])[index]
                    swapIndexes = [notFixedIndexes[j], differentIndexValueThanJ]
                    # swapIndexes = random.sample(notFixedIndexes, 2)
                    valuesRow[swapIndexes[1]], valuesRow[swapIndexes[0]] = valuesRow[swapIndexes[0]], valuesRow[
                        swapIndexes[1]]
                    self.setValue(rowNumber, swapIndexes[0], valuesRow[swapIndexes[0]])
                    self.setValue(rowNumber, swapIndexes[1], valuesRow[swapIndexes[1]])

    # mapping random value from 0 to 1 into given range
    def mapValue(self, value, range):
        return int(math.floor((value - 0) / (1 - 0) * (range[1] - range[0]) + range[0]))

    def getError(self, chromosome):
        return len(self.NUMBERS) - len(set(chromosome))

    def updateAdaptiveMutation(self):
        self.AdaptiveMutationMap = [0.0] * len(self.DigitsArray)
        for i in range(0, 9):
            column = self.getColumn(i)
            square = self.getSquare(i)
            if self.getError(column) != 0:
                duplicationIndexesInfo = self.getDuplicationIndexesInfo(column, self.getColumn(i, self.FIXED_DIGITS_MAP))
                for item in duplicationIndexesInfo:
                    globalIndex = item[0] * self.SEGMENT_LENGTH + i
                    self.AdaptiveMutationMap[globalIndex] += 1.0 if item[1] else self.ADAPTIVE_MUTATION_VALUE
            if self.getError(square) != 0:
                duplicationIndexesInfo = self.getDuplicationIndexesInfo(square, self.getSquare(i, self.FIXED_DIGITS_MAP))
                for item in duplicationIndexesInfo:
                    globalIndex = self.getAbsoluteIndex(i, item[0])
                    self.AdaptiveMutationMap[globalIndex] += 1.0 if item[1] else self.ADAPTIVE_MUTATION_VALUE

    def doublePointCrossover(self, other, bounds, pc):
        firstChildDigits = self.DigitsArray[:]
        secondChildDigits = other.DigitsArray[:]
        if pc > random.random():
            for i in range(0, self.SEGMENT_LENGTH):
                listOffspring = self.rowDoublePointCrossover(self.getRow(i), other.getRow(i), i,
                                                              bounds)
                firstChildDigits += listOffspring[0]
                secondChildDigits += listOffspring[1]
        return SudokuGA(firstChildDigits), SudokuGA(secondChildDigits)

    def getAbsoluteIndex(self, squareNumber, relativeIndex):
        startPosition1 = squareNumber * self.SQUARE_SEGMENT_SIZE
        if squareNumber > 2:
            startPosition1 += 2 * self.SEGMENT_LENGTH
        if squareNumber > 5:
            startPosition1 += 2 * self.SEGMENT_LENGTH
        startPosition2 = startPosition1 + self.SEGMENT_LENGTH
        startPosition3 = startPosition2 + self.SEGMENT_LENGTH
        index = relativeIndex % self.SQUARE_SEGMENT_SIZE
        if relativeIndex > 5:
            return startPosition3 + index
        if relativeIndex > 2:
            return startPosition2 + index
        return startPosition1 + index

    def rowDoublePointCrossover(self, momRow, dadRow, rowNumber, bounds):
        if len(momRow) != len(dadRow):
            raise ValueError('Chromosomes are not the same size')
        leftBound = bounds[0] if bounds[0] > 0 else 1
        rightBound = bounds[1]
        firstChild = self.getRowWithFixedValues(momRow, rowNumber)
        secondChild = self.getRowWithFixedValues(momRow, rowNumber)
        firstChild[leftBound: rightBound] = momRow[leftBound:rightBound]
        secondChild[leftBound: rightBound] = dadRow[leftBound:rightBound]
        firstChild = self.fillZeros(firstChild, dadRow)
        secondChild = self.fillZeros(secondChild, momRow)
        return firstChild, secondChild

    def getDuplicationIndexesInfo(self, valuesList, fixedValuesMask):
        fixedValues = [val for idx, val in enumerate(valuesList) if fixedValuesMask[idx]]
        duplicates = [val for val in valuesList if valuesList.count(val) > 1]
        return [(idx, val in fixedValues) for idx, val in enumerate(valuesList) if val in duplicates]

    def getTwoRandomBounds(self, size):
        firstBound = random.randint(1, size - 1)
        secondBound = (firstBound + int(size / 3)) % (size - 1)
        return sorted([firstBound, secondBound])
