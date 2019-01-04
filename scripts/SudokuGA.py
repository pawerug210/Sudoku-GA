import Sudoku
import Chromosome
import random


class SudokuGA(Sudoku.Sudoku, Chromosome.Chromosome):

    def __init__(self, sudoku):
        super(SudokuGA, self).__init__(sudoku)
        self.fitness, self.problemMakersMap = self.update()


    # chromosome interface

    def getFitness(self):
        pass

    def updateFitness(self):
        pass

    def mutate(self, pm):
        pass

    def crossover(self, other, bounds, pc):
        return self.doublePointCrossover(other, bounds, pc)

    def getError(self, chromosome):
        return len(self.NUMBERS) - len(set(chromosome))

    def update(self):
        error = 0
        problemIndexes = [0] * len(self.DigitsArray)
        for i in range(0, 9):
            # todo remove row from validation
            row = self.getRow(self.DigitsArray, i)
            column = self.getColumn(self.DigitsArray, i)
            square = self.getSquare(self.DigitsArray, i)
            rowError = self.getError(row)
            columnError = self.getError(column)
            squareError = self.getError(square)
            if rowError != 0:
                raise Exception
            error += columnError + squareError
            if columnError != 0:
                # todo rename duplicationindexes
                duplicationIndexes = self.getDuplicationIndexes(column, self.getColumn(self.FIXED_DIGITS_MAP, i))
                for item in duplicationIndexes:
                    globalIndex = item[0] * self.SEGMENT_LENGTH + i
                    problemIndexes[globalIndex] += 10 if item[1] else 1
            if squareError != 0:
                duplicationIndexes = self.getDuplicationIndexes(square, self.getSquare(self.FIXED_DIGITS_MAP, i))
                for item in duplicationIndexes:
                    globalIndex = self.getAbsoluteIndex(i, item[0])
                    problemIndexes[globalIndex] += 10 if item[1] else 1
        self.fitness = error
        self.problemMakersMap = problemIndexes
        return self.fitness, problemIndexes

    def doublePointCrossover(self, other, bounds, pc):
        firstChildDigits = self.DigitsArray[:]
        secondChildDigits = other.DigitsArray[:]
        if pc > random.random():
            for i in range(0, self.SEGMENT_LENGTH):
                listOffspring = self.rowDoublePointCrossover(self.getDigitsRow(i)[0], other.getDigitsRow(i)[0], i,
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

    # todo rename it
    def getDuplicationIndexes(self, valuesList, fixedValuesMask):
        fixedValues = [val for idx, val in enumerate(valuesList) if fixedValuesMask[idx]]
        duplicates = [val for val in valuesList if valuesList.count(val) > 1]
        return [(idx, val in fixedValues) for idx, val in enumerate(valuesList) if val in duplicates]

    def getProblemIndexes(self, row):
        startPosition = row * self.SEGMENT_LENGTH
        return self.problemMakersMap[startPosition: startPosition + self.SEGMENT_LENGTH]