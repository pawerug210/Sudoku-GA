import numpy as np
from random import shuffle


class Sudoku(object):

    NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    SEGMENT_LENGTH = 9
    SQUARE_SEGMENT_SIZE = 3
    FIXED_DIGITS_MAP = []

    def __init__(self, sudokuValuesList):
        self.DigitsArray = self.initialize(sudokuValuesList)

    def initialize(self, digitsList):
        filledDigitsList = []
        valuesList = list(self.NUMBERS)
        for i in range(0, 9):
            shuffle(valuesList)
            filledDigitsList += self.fillZeros(self.getRow(values=digitsList, rowNumber=i), valuesList)
        return filledDigitsList

    def setValue(self, row, column, value):
        index = self.getIndex(row, column)
        if (value not in self.NUMBERS) or self.FIXED_DIGITS_MAP[index]:
            raise Exception
        self.DigitsArray[index] = value

    def getValue(self, row, column):
        try:
            return self.DigitsArray[self.getIndex(row, column)]
        except IndexError:
            return 0

    def getIndex(self, row, column):
        return row * self.SEGMENT_LENGTH + column

    def getRow(self, rowNumber, values=None):
        values = self.getValues(values)
        startPosition = rowNumber * self.SEGMENT_LENGTH
        return values[startPosition: startPosition + self.SEGMENT_LENGTH]

    def getColumn(self, columnNumber, values=None):
        values = self.getValues(values)
        jumpSize = self.SEGMENT_LENGTH
        return values[columnNumber::jumpSize]

    # 0 | 1 | 2
    # ---------
    # 3 | 4 | 5
    # ---------
    # 6 | 7 | 8
    def getSquare(self, squareNumber, values=None):
        values = self.getValues(values)
        startPosition1 = squareNumber * self.SQUARE_SEGMENT_SIZE
        if squareNumber > 2:
            startPosition1 += 2 * self.SEGMENT_LENGTH
        if squareNumber > 5:
            startPosition1 += 2 * self.SEGMENT_LENGTH
        startPosition2 = startPosition1 + self.SEGMENT_LENGTH
        startPosition3 = startPosition2 + self.SEGMENT_LENGTH
        squareValues = values[startPosition1: startPosition1 + self.SQUARE_SEGMENT_SIZE] + \
                       values[startPosition2: startPosition2 + self.SQUARE_SEGMENT_SIZE] + \
                       values[startPosition3: startPosition3 + self.SQUARE_SEGMENT_SIZE]
        return squareValues

    def getValues(self, values):
        if values is None:
            return self.DigitsArray
        return values

    def listError(self, values):
        return len(self.NUMBERS) - len(set(values))

    def getRowWithFixedValues(self, values, rowNumber):
        rowWithFixedValues = map(lambda value, isFixed: value if isFixed else 0, values,
                                 self.getRow(rowNumber, self.FIXED_DIGITS_MAP))
        return list(rowWithFixedValues)

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
        print(np.asarray(self.DigitsArray).reshape((9, 9)))
