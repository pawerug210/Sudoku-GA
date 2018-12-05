import Sudoku
import Chromosome
import random


class SudokuGA(Sudoku.Sudoku, Chromosome.Chromosome):

    def __init__(self, sudoku):
        super(SudokuGA, self).__init__(sudoku)
        self.fitness, self.problemMakersMap = self.update()

    def getError(self, chromosome):
        return len(self.NUMBERS) - len(set(chromosome))

    def update(self):
        error = 0
        problemIndexes = [False] * len(self.sudokuDigitsArray)
        for i in range(0, 9):
            row = self.getRow(self.sudokuDigitsArray, i)
            column = self.getColumn(self.sudokuDigitsArray, i)
            square = self.getSquare(self.sudokuDigitsArray, i)
            rowError = self.getError(row)
            columnError = self.getError(column)
            squareError = self.getError(square)
            if rowError != 0:
                raise Exception
            error += rowError + columnError + squareError
            if columnError != 0:
                duplicationIndexes = self.getDuplicationIndexes(column)
                for idx in duplicationIndexes:
                    problemIndexes[idx * self.SEGMENT_LENGTH + i] = True
            # if squareError != 0:
            #     duplicationIndexes = self.getDuplicationIndexes(square)
            #     for idx in duplicationIndexes:
            #         problemIndexes[] = True
        self.fitness = error
        self.problemMakersMap = problemIndexes
        return self.fitness, problemIndexes

    def doublePointCrossover(self, other):
        firstChildDigits = []
        secondChildDigits = []
        for i in range(0, self.SEGMENT_LENGTH):
            listOffspring = self.listDoublePointCrossover(self.getDigitsRow(i)[0], other.getDigitsRow(i)[0], i)
            firstChildDigits += listOffspring[0]
            secondChildDigits += listOffspring[1]
        return SudokuGA(firstChildDigits), SudokuGA(secondChildDigits)

    def listDoublePointCrossover(self, mom, dad, rowNumber):
        if len(mom) != len(dad):
            raise Exception
        leftBound = random.randint(1, int(len(mom) / 2))
        rightBound = random.randint(leftBound + 1, len(mom) - 1)
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