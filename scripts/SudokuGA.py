import Sudoku
import Chromosome
import random


class SudokuGA(Sudoku.Sudoku, Chromosome.Chromosome):

    Counter = 0

    def __init__(self, sudoku):
        super(SudokuGA, self).__init__(sudoku)
        # todo counter is not working
        self.Id = self.Counter
        self.Counter += 1
        self.fitness, self.problemMakersMap = self.update()

    def getError(self, chromosome):
        return len(self.NUMBERS) - len(set(chromosome))

    def update(self):
        error = 0
        problemIndexes = [0] * len(self.sudokuDigitsArray)
        for i in range(0, 9):
            # todo remove row from validation
            row = self.getRow(self.sudokuDigitsArray, i)
            column = self.getColumn(self.sudokuDigitsArray, i)
            square = self.getSquare(self.sudokuDigitsArray, i)
            rowError = self.getError(row)
            columnError = self.getError(column)
            squareError = self.getError(square)
            if rowError != 0:
                raise Exception
            error += columnError + squareError
            if columnError != 0:
                duplicationIndexes = self.getDuplicationIndexes(column)
                for idx in duplicationIndexes:
                    problemIndexes[idx * self.SEGMENT_LENGTH + i] += 1
            if squareError != 0:
                duplicationIndexes = self.getDuplicationIndexes(square)
                for idx in duplicationIndexes:
                    problemIndexes[self.getAbsoluteIndex(i, idx)] += 1
        if any(x > 2 for x in problemIndexes):
            raise Exception
        self.fitness = error
        self.problemMakersMap = problemIndexes
        return self.fitness, problemIndexes

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

    def getDuplicationIndexes(self, valuesList):
        duplicates = [val for val in valuesList if valuesList.count(val) > 1]
        return [idx for idx, val in enumerate(valuesList) if val in duplicates]

    def getProblemIndexes(self, row):
        startPosition = row * self.SEGMENT_LENGTH
        return self.problemMakersMap[startPosition: startPosition + self.SEGMENT_LENGTH]