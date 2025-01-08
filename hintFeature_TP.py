    

from cmu_graphics import *
import random
import math
from urllib.request import urlopen
from PIL import Image
import copy

## HINT FEATURE
def dealWithHint(app):
    if app.gameStarted and app.gameOver == False:
            app.showHint = True
            if app.numHints == 0:
                app.hint = 'you are out of hints!'
            else:
                (mOrL, coordinates) = nextMoveFinder(app)
                app.hintCoordinates = coordinates
                if mOrL == None:
                    app.hint = 'you need to guess!'
                elif mOrL == 'mine':
                    app.hint = 'place a flag on the yellow square'
                elif app.numHints == 0:
                    app.hint = 'you are out of hints!'
                else:
                    app.hint = 'dig the land on the yellow square'
                app.seenHints.add((coordinates))
                app.numHints = 3-len(app.seenHints)
                  
# making a thing that the user can use 3 times to ask if they need to make a 
# guess or if there is a concrete next move to make

def nextMoveFinder(app):

    # loop through cells
    # if cell is a number then check if it is already done
    # if not call backtracking function on it;

    foundMove = False
    for row in range(app.rows):
        for col in range(app.cols):
            if foundMove == False:
                if ((app.displayedBoard[row][col] != None) and 
                    (app.displayedBoard[row][col] != 'X')):
                # checking if the cell already touches the amount of mines and land
                #if cellDone(app, row, col, app.displayedBoard) == False:
                    # if checkCell returns None, there is no concrete move to make
                    # d = {'m': {(coordinates)}, 'l':{(coordinates)}}
                    d = checkCell(app, row, col)
                    if d != dict():
                        foundMove = True

    # choosing a next move out of the options
    if 'm' in d:
        possibleNextMoves = d['m']
        possibleNextMoves = list(possibleNextMoves)
        nextMove = ('mine', possibleNextMoves[0])
    elif 'l' in d:
        possibleNextMoves = d['l']
        possibleNextMoves = list(possibleNextMoves)
        nextMove = ('land', possibleNextMoves[0])
    else:
        nextMove = (None, None)
    return nextMove

# returns the number of mines a given cell is touching and the number of 
# empty pieces the mine is touching

def numMinesTouching(app, row, col, board):
    numMinesCurrentlyTouches = 0
    numEmptyCurrentlyTouches = 0

    for drow in range(-1,2):
        for dcol in range(-1,2):
            newRow = row + drow
            newCol = col + dcol
            if newRow != row or newCol != col:
                if ((newRow > -1 and newRow < app.rows) and
                    (newCol > -1 and newCol < app.cols) and
                    (board[newRow][newCol] == 'X')):
                        numMinesCurrentlyTouches += 1
                elif ((newRow > -1 and newRow < app.rows) and
                    (newCol > -1 and newCol < app.cols) and
                    (board[newRow][newCol] == None)):    
                        numEmptyCurrentlyTouches += 1
    return (numMinesCurrentlyTouches, numEmptyCurrentlyTouches)

# this function checks if a cell is complete. in other words it touches the correct
# amount of mines and has no empty space around it
def cellDone(app, row, col, board):
    if board[row][col] != None and board[row][col].isdigit():
        numMinesShouldTouch = int(board[row][col])
    
        (numMinesCurrentlyTouches, numEmptyCurrentlyTouches) = numMinesTouching(app, row, col, board)

        if (numMinesShouldTouch == numMinesCurrentlyTouches): # doesn't take into account empty
            return True
        return False
    return True

# returns the next moves 
def checkCell(app, row, col):
    retVal = dict()
    
    ## FINDING PLACES TO PUT MINES


    # 2d list of (row,col) vals [[(1,0)]] list of lists where the inner lists are
    # a list of every place where a mine would be placed
    placesToPutMines = findMineSpots(app, row, col)

    # checking to see if the formations of mines in placesToPutMines 
    # all share a common mine placement - a next move for the user

    # creates a dictionary seen that maps each mine placement to the number 
    # of times it appears in placedToPutMines
    seenMine = dict()
    for formation in placesToPutMines:
        for minePlacement in formation:
            if minePlacement not in seenMine:
                seenMine[minePlacement] = 1
            else:
                seenMine[minePlacement] += 1


    for mine in seenMine:
        # if this mine placement appears in every possible mine formation
        if seenMine[mine] == len(placesToPutMines):
            if 'm' not in retVal:
                retVal['m'] = set([mine])
            else:
                retVal['m'].add(mine)


    ## FINDING PLACES TO PUT LAND

    placesToPutLand = findLandSpots(app, row, col)

    seenLand = dict()
    for formation in placesToPutLand:
        for landPlacement in formation:
            if landPlacement not in seenLand:
                seenLand[landPlacement] = 1
            else:
                seenLand[landPlacement] += 1


    for land in seenLand:
        # if this mine placement appears in every possible mine formation
        if seenLand[land] == len(placesToPutLand):
            if 'l' not in retVal:
                retVal['l'] = set([land])
            else:
                retVal['l'].add(land)
        

    

    return retVal

# returns a 2D list representing all the different ways in which land could be placed
def findLandSpots(app, row, col):
    copyOfAnswerBoard = copy.deepcopy(app.answerBoard)
    copyOfDisplayBoard = copy.deepcopy(app.displayedBoard)
    (minesTouching, emptyTouching) = numMinesTouching(app, row, col, copyOfDisplayBoard)

    if (copyOfAnswerBoard[row][col] == None):
        return None
    
    numMinesNeeded = int(copyOfAnswerBoard[row][col]) - minesTouching
    # the number of lands that still need to be placed adjacent to the cell
    numLandNeeded = emptyTouching - numMinesNeeded

    allWays = []
    foundAll = False
    # search for different ways to place land until we can't find anymore
    while foundAll == False:
        copyOfAnswerBoard = copy.deepcopy(app.answerBoard)
        copyOfDisplayBoard = copy.deepcopy(app.displayedBoard)
        possible = solvedLandSpots(app, row, col, copyOfDisplayBoard, numLandNeeded, set(), allWays)
        if possible == None:
            foundAll = True
        elif list(possible) not in allWays:
            allWays.append(list(possible))
    return allWays

def solvedLandSpots(app, row, col, copyDisplay, numLandNeeded, current, allWays):
    # found a new possible formation for the land
    if len(current) == numLandNeeded:
        # if we have already seen this, then keep searching
        # if list(current) in allWays: # edit to check for purmutations and no duplicates like that
        if notIn(list(current), allWays) == False:
            return None
        return current
    else:
        for drow in range(-1,2):
            for dcol in range(-1,2):
                newRow = row + drow
                newCol = col + dcol
                if isLegalLandPlacement(app, newRow, newCol, copyDisplay, current):
                    copyDisplay[newRow][newCol] = app.answerBoard[newRow][newCol]
                    current.add((newRow, newCol))
                    solved = solvedLandSpots(app, row, col, copyDisplay, numLandNeeded, current, allWays)
                    if solved != None:
                        return solved
                    current.remove((newRow, newCol))
                    copyDisplay[newRow][newCol] = None
    return None

def isLegalLandPlacement(app, row, col, display, current):
    # no duplicates
    if (row, col) in current:
        return False
    # in bounds
    if ((row < 0 or row >= app.rows) or
        (col < 0 or col >= app.cols)):
        return False
    # only place land on empty cell
    if display[row][col] != None:
        return False

    for drow in range(-1,2):
        for dcol in range(-1,2):
            newRow = drow + row
            newCol = dcol + col
            if ((0 <= newRow < app.rows) and
                (0 <= newCol < app.cols)):
                if ((display[newRow][newCol] != None) and
                    (display[newRow][newCol] != 'X') and
                    (not cellDone(app, newRow, newCol, display))):
                    if display[newRow][newCol].isdigit() and landNotAvailable(app, row, col, newRow, newCol, display):
                        return False
    return True

# returns True if adding a piece of land at landRow, landCol, will make it
# impossible to place all the mines for the cell at checkRow, checkCol
def landNotAvailable(app, landRow, landCol, checkRow, checkCol, display):
    copyOfAnswerBoard = copy.deepcopy(app.answerBoard)
    (minesTouching, emptyTouching) = numMinesTouching(app, checkRow, checkCol, display)
    numMinesNeeded = int(copyOfAnswerBoard[checkRow][checkCol]) - minesTouching

    # if all the surrounding empty cells must be filled with mines, 
    # we can't place anymore land around this cell
    if emptyTouching == numMinesNeeded:
        return True
    return False

# returns a 2D list representing all the different ways in which mines could be placed
def findMineSpots(app, row, col):
    copyOfAnswerBoard = copy.deepcopy(app.answerBoard)
    copyOfDisplayBoard = copy.deepcopy(app.displayedBoard)
    (minesTouching, emptyTouching) = numMinesTouching(app, row, col, copyOfDisplayBoard)
    # number of mines that need to be placed
    if (copyOfAnswerBoard[row][col] == None):
        return None
    numMinesNeeded = int(copyOfAnswerBoard[row][col]) - minesTouching

    allWays = []
    foundAll = False

    # search for different ways to place mines until we can't find anymore
    while foundAll == False:
        copyOfAnswerBoard = copy.deepcopy(app.answerBoard)
        copyOfDisplayBoard = copy.deepcopy(app.displayedBoard)
        possible = solvedMineSpots(app, row, col, copyOfDisplayBoard, numMinesNeeded, set(), allWays)
        if possible == None:
            foundAll = True
        elif list(possible) not in allWays:
            allWays.append(list(possible))
    return allWays

# backtracking function
def solvedMineSpots(app, row, col, copyDisplay, numMinesNeeded, current, allWays):
    # found a new possible formation for the mines
    if len(current) == numMinesNeeded:
        # if we have already seen this, then keep searching
        # if list(current) in allWays: # edit to check for purmutations and no duplicates like that
        if notIn(list(current), allWays) == False:
            return None
        return current
    else:
        for drow in range(-1,2):
            for dcol in range(-1,2):
                newRow = row + drow
                newCol = col + dcol
                if isLegalMinePlacement(app, newRow, newCol, copyDisplay, current):
                    copyDisplay[newRow][newCol] = 'X'
                    current.add((newRow, newCol))
                    solved = solvedMineSpots(app, row, col, copyDisplay, numMinesNeeded, current, allWays)
                    if solved != None:
                        return solved
                    current.remove((newRow, newCol))
                    copyDisplay[newRow][newCol] = None
    return None

# checks if we can legally put a flag in the row,col
def isLegalMinePlacement(app, row, col, display, current):
    if (row, col) in current:
        return False
    if ((row < 0 or row >= app.rows) or
        (col < 0 or col >= app.cols)):
        return False
    # we can only place the flag on an empty cell
    if display[row][col] != None:
        return False
    
    # check if it works for the surrounding cells
    for drow in range(-1,2):
        for dcol in range(-1,2):
            newRow = drow + row
            newCol = dcol + col
            if ((0 <= newRow < app.rows) and
                (0 <= newCol < app.cols)):
                if display[newRow][newCol] != None and display[newRow][newCol] != 'X':
                    if display[newRow][newCol].isdigit() and cellDone(app, newRow, newCol, display):
                        return False
    return True

# checks if we have already found this pair of mine placing
def notIn(current, allWays):
    copyCurrent = copy.copy(current)
    copyAllWays = copy.deepcopy(allWays)
    for i in range(len(copyAllWays)):
        if sorted(copyCurrent) == sorted(copyAllWays[i]):
            return False
    return True
