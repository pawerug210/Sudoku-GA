import numpy as np
from random import shuffle


class Sudoku(object):

    NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    SEGMENT_LENGTH = 9
    SQUARE_SEGMENT_SIZE = 3
    sudokuFixedDigitsArray = []

    def __init__(self, sudokuValuesList):
        self.sudokuDigitsArray = self.initialize(sudokuValuesList)

    def initialize(self, digitsList):
        filledDigitsList = []
        # use NUMBERS
        valuesList = list(self.NUMBERS)
        for i in range(0, 9):
            shuffle(valuesList)
            filledDigitsList += self.fillZeros(self.getRow(values=digitsList, rowNumber=i), valuesList)
        # print(filledDigitsList)
        return filledDigitsList

    def isValid(self):
        # todo
        error = 0
        for i in range(0, 9):
            error += self.listError(self.getRow(self.sudokuDigitsArray, i)) + \
                     self.listError(self.getColumn(i)) + \
                     self.listError(self.getSquare(i))

        return error == 0


    def getRow(self, values, rowNumber):
        startPosition = rowNumber * self.SEGMENT_LENGTH
        return values[startPosition: startPosition + self.SEGMENT_LENGTH]

    def getDigitsRow(self, rowNumber):
        startPosition = rowNumber * self.SEGMENT_LENGTH
        return self.sudokuDigitsArray[startPosition: startPosition + self.SEGMENT_LENGTH], \
               self.sudokuFixedDigitsArray[startPosition: startPosition + self.SEGMENT_LENGTH]

    def getColumn(self, values, columnNumber):
        jumpSize = self.SEGMENT_LENGTH
        return values[columnNumber::jumpSize]

    def setValue(self, row, column, value):
        index = self.getIndex(row, column)
        if (value not in self.NUMBERS) or self.sudokuFixedDigitsArray[index]:
            raise Exception
        self.sudokuDigitsArray[index] = value

    def getValue(self, row, column):
        try:
            return self.sudokuDigitsArray[self.getIndex(row, column)]
        except IndexError:
            return 0

    def getIndex(self, row, column):
        return row * self.SEGMENT_LENGTH + column

    # 0 | 1 | 2
    # ---------
    # 3 | 4 | 5
    # ---------
    # 6 | 7 | 8
    def getSquare(self, values, squareNumber):
        startPosition1 = squareNumber * self.SQUARE_SEGMENT_SIZE
        if squareNumber > 2:
            startPosition1 += 2 * self.SEGMENT_LENGTH
        if squareNumber > 5:
            startPosition1 += 2 * self.SEGMENT_LENGTH
        startPosition2 = startPosition1 + self.SEGMENT_LENGTH
        startPosition3 = startPosition2 + self.SEGMENT_LENGTH
        retVal = values[startPosition1: startPosition1 + self.SQUARE_SEGMENT_SIZE] + \
                 values[startPosition2: startPosition2 + self.SQUARE_SEGMENT_SIZE] + \
                 values[startPosition3: startPosition3 + self.SQUARE_SEGMENT_SIZE]
        # print(sorted(retVal))
        return retVal

    def listError(self, values):
        return len(self.NUMBERS) - len(set(values))

    def getRowWithFixedValues(self, values, rowNumber):
        rowWithFixedValues = map(lambda value, isFixed: value if isFixed else 0, values, self.getRow(self.sudokuFixedDigitsArray, rowNumber))
        return list(rowWithFixedValues)

    def zeros(self, n):
        return [0] * n

    def fillZeros(self, child, parent):
        for value in parent:
            try:
                emptyPlaceIndex = child.index(0)
                if value not in child:
                    child[emptyPlaceIndex] = value
            except ValueError:
                break
        return child

    def draw(self):
        print(np.asarray(self.sudokuDigitsArray).reshape((9, 9)))




