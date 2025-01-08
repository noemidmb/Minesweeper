# Noemi Barbagli
# Term Project Main

# screens:
# login
# home
# leader board
# personal stats
# game
# tutorial
# settings


from cmu_graphics import *
import random
import math
from urllib.request import urlopen
from PIL import Image
import copy
from hintFeature_TP import *

## Notes
## change font


## red flag image citing - https://www.redbubble.com/i/art-print/Red-Flag-Meme-Funny-Popular-Culture-Fan-Trending-Flags-Trend-by-gkao/93343303.DJUF3
## inspiration for tutorial - https://minesweepergame.com/strategy/how-to-play-minesweeper.php#:~:text=Minesweeper%20is%20a%20game%20where,mine%20you%20lose%20the%20game!
## hint image - https://nohat.cc/f/striking-hint-hint-information-icon-hint-icon-png/m2H7G6b1K9d3H7i8-202208020413.html



def loadPilImage(url):
    return Image.open(url)

def onAppStart(app):
    newLogin(app)
    newGame(app)

def newLogin(app):
    ## LOGIN FEATURE
    app.username = ''
    app.password = ''
    app.typingUsername = True
    app.typingPassword = False
    app.userWins = 0
    app.userLosses = 0
    try:
        app.accounts = open("accounts_TP.txt", 'r')
    except:
        app.accounts = open("accounts_TP.txt", 'x')
    app.loginMessage = ''
    
def newGame(app):
    app.rows = 10
    app.cols = 10
    
    app.cellBorderWidth = 2
    app.width= 600
    app.height= 700

    app.percentCellsMines = 0.15
    
    app.boardColor = 'default'
    app.colorBoardEven = rgb(81, 250, 81)
    app.colorBoardOdd = rgb(0, 235, 0)

    createStandardBoard(app)
    
    # bool representing if the user has made their first click on the board yet
    app.gameStarted = False
    # the coordinates of the user's first mouse click on the board
    app.firstX = None
    app.firstY = None

    # represents if mines are being placed
    app.placingMines = False

    # game over if they dig a mine
    app.gameOver = False
    
    app.stepsPerSecond = 5
    app.mineRevealColors = dict()
    app.mineRevealColorOptions = [(255,153,153), (255,204,153), (255,255,153),
                            (153,255,255), (153,204,255), (204,153,255),
                            (75,203,255),(255,153,204), (153, 153, 255)]

    # solved if they correctly dug all of the places, did not necessarily have to
    # place all the flags
    app.solved = False

    app.highlightedX = None
    app.highlightedY = None
    
    app.buttonClick = rgb(160,240,255)

    app.showHint = False
    app.hint = None
    app.hintCoordinates = (None, None)
    app.seenHints = set()
    app.numHints = 3-len(app.seenHints)
   

    app.timer = 0
    app.count = 0

    
    loadImages(app)

def loadImages(app):
# loading tutorial images
    try:
        url = 'slide1IMG.png'
        pilImage = Image.open(url).resize((120, 60), Image.Resampling.LANCZOS)
        app.slide1IMG = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.slide1IMG = None

    try:
        url = 'slide1PinkIMG.png'
        pilImage = Image.open(url).resize((420, 105), Image.Resampling.LANCZOS)
        app.slide1PinkIMG = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.slide1PinkIMG = None

    try:
        url = 'slide3IMG.png'
        pilImage = Image.open(url).resize((420, 98), Image.Resampling.LANCZOS)
        app.slide3IMG = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.slide3IMG = None
    
    try:
        url = 'slide4IMG.png'
        pilImage = Image.open(url).resize((420, 98), Image.Resampling.LANCZOS)
        app.slide4IMG = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.slide4IMG = None
    
    try:
        url = 'slide5IMG.png'
        pilImage = Image.open(url).resize((420, 98), Image.Resampling.LANCZOS)
        app.slide5IMG = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.slide5IMG = None

    try:
        url = 'hintIMG.png'
        pilImage = Image.open(url).resize((65, 40), Image.Resampling.LANCZOS)
        app.hintIMG = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.hintIMG = None

    try:
        url = 'timerIMG.png'
        pilImage = Image.open(url).resize((65, 40), Image.Resampling.LANCZOS)
        app.timerIMG = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.timerIMG = None

def createStandardBoard(app):
    app.displayedBoard = [([None] * app.cols) for row in range(app.rows)]

    # the board that keeps track of the locations of the mines
    # 2D list representation of board - each cell is either a positive number
    # representing the number of mines that square touches, or a -1 AKA a mine
    app.answerBoard = [([None] * app.cols) for row in range(app.rows)]
    # will change depending on the level
    app.numMines = int(app.cols * app.rows * app.percentCellsMines)
    app.numMinesLeft = app.numMines
    app.numCorrectMines = 0
    app.minesToBeRevealed = app.numMinesLeft

    # determining cell length 

    app.cellLength = cellLength(app)

    app.boardWidth = int(app.cols*app.cellLength)
    app.boardHeight = int(app.rows*app.cellLength)

    app.boardLeft = 300 - app.boardWidth/2
    app.boardTop = 300 - app.boardHeight/2

    # loading the flag icon
    try:
        url = 'flagImage_3.png'
        pilImage = Image.open(url).resize((app.cellLength, app.cellLength), Image.Resampling.LANCZOS)
        app.flagImage = CMUImage(pilImage)
    except Exception as e:
        print(f"Error loading menu image: {e}")
        app.flagImage = None

def cellLength(app):
    if app.rows < app.cols:
        cellLength = 500/app.cols
    elif app.cols < app.rows:
        cellLength = 500/app.rows
    else:
        cellLength = 500/app.cols
    cellLength = int(cellLength)
    return cellLength  
## implement password
def login_redrawAll(app):
    drawHomeBoard(app)
    drawRect(100, 150, 400, 160, fill = 'white', border = 'black', borderWidth = 5)

    drawLabel('WELCOME TO', 300, 200, size = 47.5, bold = True, font = 'monospace')
    drawLabel('MINESWEEPER!', 300, 260, size = 47.5, bold = True, font = 'monospace')

    if app.typingUsername == True:
        drawRect(225, 350, 150, 75, fill=rgb(160,240,255), border='black', borderWidth=4)
    else:
        drawRect(225, 350, 150, 75, fill='white', border='black', borderWidth=4)

    if app.username == '':
        drawLabel('type your name!', 300, 390, size=12, bold = True, font = 'monospace')
    else:
        drawLabel(app.username, 300, 390, size=15, bold = True, font = 'monospace')
    
    if app.loginMessage == 'incorrect password':
        drawRect(225, 425, 150, 75, fill='red', border='black', borderWidth=4)
    elif app.typingPassword == True:
        drawRect(225, 425, 150, 75, fill=rgb(160,240,255), border='black', borderWidth=4)
    else:
        drawRect(225, 425, 150, 75, fill='white', border='black', borderWidth=4)
    
    if app.password == '':
        drawLabel('click to type', 300, 458, size=12, bold = True, font = 'monospace')
        drawLabel('a password', 300, 472, size=12, bold = True, font = 'monospace')
    else:
        drawLabel(app.password, 300, 465, size=15, bold = True, font = 'monospace')



    drawRect(225, 560, 150, 75, fill='pink', border='black', borderWidth=4)
    drawLabel('LOGIN', 300, 600, size=20, bold = True, font = 'monospace')

def login_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(225, 560, 150, 75, mouseX, mouseY):
        if userExists(app) == True and checkPassword(app) == False:
            app.loginMessage = 'incorrect password'
        else:
            app.loginMessage = ''
            if len(app.username) == 0 or len(app.password) == 0:
                return
            else:
                if userExists(app) == False:
                    accountsEditor = open("accounts_TP.txt", "a")
                    accountsEditor.write(f'{app.username}={app.password}, 0 wins, 0 losses')
                    accountsEditor.write('\n')
                    accountsEditor.close()
                setActiveScreen('home')
    elif clickedOnButton(225, 350, 150, 75, mouseX, mouseY):
        app.loginMessage = ''
        app.typingUsername = True
        app.typingPassword = False
    elif clickedOnButton(225, 425, 150, 75, mouseX, mouseY):
        app.loginMessage = ''
        app.typingUsername = False
        app.typingPassword = True

# checks if user inputted the correct password
def checkPassword(app):
    accountsReader = open("accounts_TP.txt", "r")
    lines = accountsReader.readlines()
    password = ''
    for line in lines:
        if f'{app.username}=' in line:
            for element in line.split(","):
                if element.find('=') != -1:
                    password = getPassword(app, element)
    accountsReader.close()
    if password == app.password:
        return True
    return False

# returns user's password
def getPassword(app, element):
    for word in element.split('='):
        if word != app.username:
            return word
    return None

# checks if a user has played before
def userExists(app):
    accountsReader = open("accounts_TP.txt", "r")
    lines = accountsReader.readlines()
    for line in lines:
        if f'{app.username}=' in line:
            return True
    accountsReader.close()
    return False

# edits the accounts text file to update user's scores
def changeUserInformation(app, wOrL):

    accountsReader = open("accounts_TP.txt", "r")
    lines = accountsReader.readlines()

    beforeUser = ''
    afterUser = ''
    foundUser = False
    newLine = ''
    
    for line in lines:
        if foundUser == True:
            afterUser += line
        if f'{app.username}=' in line:
            foundUser = True
            for element in line.split(','):
                # finding user's current wins and losses stats
                if element.find(' wins') != -1:
                    userWins = getNum(element)
                elif element.find(' losses') != -1:
                    userLosses = getNum(element)
                else:
                    continue
            if wOrL == ' wins':
                newLine = f'{app.username}={app.password}, {userWins + 1} wins, {userLosses} losses \n'
            else:
                newLine = f'{app.username}={app.password}, {userWins} wins, {userLosses + 1} losses \n'
            
        if foundUser == False:
            beforeUser += line

    accountsReader.close()

    accountsEditor = open("accounts_TP.txt", "w")
    newText = beforeUser + newLine + afterUser
    accountsEditor.write(newText)
    accountsEditor.close()

# returns the number in a given string
def getNum(element):
    for val in element.split(' '):
        if val.isdigit():
            return int(val)
    return None

def login_onKeyPress(app, key):
    if key == 'enter' and app.typingUsername == True:
        app.typingUsername = False
        app.typingPassword = True
    if app.typingUsername == True:
        if len(app.username) <= 13:
            if (key.isalpha() or key.isdigit()) and len(key) == 1:
                app.username += key
        if len(app.username) > 0:
            if key == 'backspace':
                app.username = app.username[:-1]
    elif app.typingPassword == True:
        if len(app.password) <= 13:
            if (key.isalpha() or key.isdigit()) and len(key) == 1:
                app.password += key
        if len(app.password) > 0:
            if key == 'backspace':
                app.password = app.password[:-1]
    

## HOME SCREEN
def home_redrawAll(app):
    drawHomeBoard(app)


    drawRect(100, 150, 400, 160, fill = 'white', border = 'black', borderWidth = 5)

    drawLabel('WELCOME TO', 300, 200, size = 47.5, bold = True, font = 'monospace')
    drawLabel('MINESWEEPER!', 300, 260, size = 47.5, bold = True, font = 'monospace')

    # tutorial button
    
    drawRect(25, 460, 150, 75, fill='white', border='black', borderWidth=4)

    drawLabel('TUTORIAL', 95, 500, size=20, bold = True, font = 'monospace')

    # start game store
    # rgb(175, 255, 175)

    drawRect(225, 460, 150, 75, fill='pink', border='black', borderWidth=4)

    drawLabel('START GAME', 300, 500, size=20, bold = True, font = 'monospace')

    # customize store
    
    drawRect(425, 460, 150, 75, fill='white', border='black', borderWidth=4)

    drawLabel('SETTINGS', 495, 500, size=20, bold = True, font = 'monospace')

    # logout button

    drawRect(25, 600, 150, 75, fill='pink', border='black', borderWidth=4)

    drawLabel('LOGOUT FROM', 95, 630, size=15, bold = True, font = 'monospace')
    drawLabel(f'@{app.username}', 95, 650, size = 15, bold = True, font = 'monospace')

    # Leader board

    drawRect(225, 600, 150, 75, fill='white', border='black', borderWidth=4)

    drawLabel('LEADER', 295, 630, size=15, bold = True, font = 'monospace')
    drawLabel('BOARD', 295, 650, size = 15, bold = True, font = 'monospace')

    # personal stats button
    drawRect(425, 600, 150, 75, fill='pink', border='black', borderWidth=4)

    drawLabel(f'@{app.username}', 495, 630, size=15, bold = True, font = 'monospace')
    drawLabel('STATS', 495, 650, size = 15, bold = True, font = 'monospace')

# drawing the background for the homescreen
def drawHomeBoard(app):
    color = None
    for row in range(14):
        for col in range(12):
            if row % 2 == col % 2:
                color = rgb(81, 250, 81)
            else:
                color = rgb(0, 235, 0)
            
            drawHomeCell(app, row, col, color, None)

def drawHomeCell(app, row, col, color, val):
    cellLeft, cellTop = getCellLeftTopHome(app, row, col)
    cellWidth, cellHeight = 50, 50
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
    
def getCellLeftTopHome(app, row, col):
    cellWidth, cellHeight = 50, 50

    cellLeft = 0 + col * cellWidth
    cellTop = 0 + row * cellHeight
    return (cellLeft, cellTop)
    

def home_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(25, 460, 150, 75, mouseX, mouseY):
        # tutorial
        setActiveScreen('tutorial')
    elif clickedOnButton(225, 460, 150, 75, mouseX, mouseY):

        # starting game
        setActiveScreen('game')
    elif clickedOnButton(425, 460, 150, 75, mouseX, mouseY):
        # Store    
        newGame(app)
        setActiveScreen('store')
    elif clickedOnButton(25, 600, 150, 75, mouseX, mouseY):
        app.accounts.close()
        newLogin(app)
        newGame(app)
        setActiveScreen('login')
    elif clickedOnButton(225, 600, 150, 75, mouseX, mouseY):
        setActiveScreen('leaderBoard')
    elif clickedOnButton(425, 600, 150, 75, mouseX, mouseY):
       # app.accounts.close()
        setActiveScreen('stats')

## STATS SCREEN

def stats_redrawAll(app):
    drawHomeBoard(app)
    # drawRect(0, 0, app.width, app.height, fill='pink')

    drawRect(100, 200, 400, 80, fill = 'white', border = 'black', borderWidth = 5)
    drawLabel(f'@{app.username}', 300, 245, size = 43, font = 'monospace')

    wins, losses = getStats(app)
    drawRect(100, 350, 400, 80, fill = 'white', border = 'black', borderWidth = 5)
    drawLabel(f'WINS: {wins}', 300, 395, size = 47.5, font = 'monospace')

    drawRect(100, 450, 400, 80, fill = 'white', border = 'black', borderWidth = 5)
    drawLabel(f'LOSSES: {losses}', 300, 495, size = 47.5, font = 'monospace')

    # back to home button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')


def stats_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')

# returns the user's wins and losses
def getStats(app):
    accountsReader = open("accounts_TP.txt", "r")
    lines = accountsReader.readlines()
    for line in lines:
        if f'{app.username}=' in line:
            for element in line.split(','):
                # finding user's current wins and losses stats
                if element.find(' wins') != -1:
                    userWins = getNum(element)
                elif element.find(' losses') != -1:
                    userLosses = getNum(element)
                else:
                    continue
                
    accountsReader.close()
    return userWins, userLosses
    
## LEADER BOARD SCREEN
def leaderBoard_redrawAll(app):
    drawHomeBoard(app)
    # drawRect(0, 0, app.width, app.height, fill='pink')

    # back to home button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')

    drawRect(100, 50, 400, 100, fill='white', border='black', borderWidth=5)
    drawLabel('LEADERBOARD', 300, 100, size=50, bold = True, font = 'monospace')

    topFive, sortedFive = getTopFiveWinners(app)
    index = 100
    sortedFive = sortedFive[::-1]
    for i in range(len(sortedFive)):
        currentUser = None
        # find the user at ith spot on leader board
        for user in topFive:
            if topFive[user] == sortedFive[i]:
                currentUser = user
                wins = sortedFive[i]
        index += 75
        drawRect(100, index, 400, 50, fill = 'white', border = 'black', borderWidth = 3)
        drawLabel(f'{currentUser}: {wins} wins', 300, index+25, size = 23, font = 'monospace')
        topFive.pop(currentUser)

def leaderBoard_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')

# returns the topFive players and their number of wins
def getTopFiveWinners(app):
    topFive = dict()
    accountsReader = open("accounts_TP.txt", "r")
    lines = accountsReader.readlines()
    sortedFive = []
    for user in lines:
        # print(topFive)
        for element in user.split(','):
            # found the element in the line that notes number of wins
            if element.find('wins') != -1:
                numWins = getNum(element)
            elif element.find('=') != -1:
                # getting the user's username
                userName = ''
                for word in element.split('='):
                    if userName == '':
                        userName = word
                continue
            else:
                continue
            if len(topFive) < 5:
                topFive[userName] = numWins
                topFive, sortedFive = newTopFive(topFive, None, userName)
            else:
                # print(userName)
                topFive, sortedFive = newTopFive(topFive, numWins, userName)
    accountsReader.close()
    return topFive, sortedFive

# if a new player is added, this function inserts them into the correct spot in the topFive
def newTopFive(topFive, numWins, userName):
    
    newTopFive = topFive
    sortedFive = []
    for user in newTopFive:
        sortedFive.append(newTopFive[user])
    
    if numWins == None:
        sortedFive.sort()
        return newTopFive, sortedFive

    sortedFive.append(numWins)
    sortedFive.sort()
    
    
    removedVal = sortedFive.pop(0)
    newTopFive[userName] = numWins
    #checking which user was removed
    userToRemove = None
    for user in newTopFive:
        if newTopFive[user] == removedVal:
            userToRemove = user
    
    newTopFive.pop(userToRemove)
    return newTopFive, sortedFive


## TUTORIAL SCREEN

## the tutorial has multiple "slides"
# opening slide - intro
# slide 1 - talk about shop - you can first go customize your board, color, and difficulty to create cool boards like this:
# slide 2 - 
    # Minesweeper is a game where mines are hidden in a grid of squares. 
    # Your goal is to identify the location of all the hidden mines and dig all of the safe squares
# slide 3
    # Start by digging into any spot on the board (click on one of the cells!)
    # Safe squares have numbers telling you how many mines touch the square. 
    # You can use the number clues to solve the game by opening all of the safe squares. 
# slide 4
    # you can place flags on squares you think are hiding a mine by pressing the mine toggle at the bottom of the screen
# slide 5
    # If you click on a mine you lose the game and all the mines are revealed.




def tutorial_redrawAll(app):
    tutorialBackground(app)

    tutorialForwardButton(app)

    drawLabel('TUTORIAL', 300, 200, size = 40, bold = True, font = 'monospace')
    drawLabel("Do you need help learning how to play?", 300, 250, size = 18, bold = True, font = 'monospace')
    drawLabel("If not, press the back button and play!", 300, 300, size = 16, bold = True, font = 'monospace')
    drawLabel("Otherwise get started", 300, 350, size = 16, bold = True, font = 'monospace')
    drawLabel("with the pink forward button :)", 300, 370, size = 16, bold = True, font = 'monospace')

def tutorialBackground(app):
    drawHomeBoard(app)
    drawRect(75, 75, 450, 450, fill = 'white', border = 'black', borderWidth = 5)

    # back to home button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')

def tutorialBackButton(app):
    # backward in tutorial button
    drawCircle(110, 490, 20, fill='pink', border='black', borderWidth=2)
    drawLabel('<', 110, 490, size=18, bold = True, font = 'monospace')
def tutorialForwardButton(app):
    # forward in tutorial button
    drawCircle(490, 490, 20, fill='pink', border='black', borderWidth=2)
    drawLabel('>', 490, 490, size=18, bold = True, font = 'monospace')

def tutorial_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')
    elif clickedOnButton(470, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide1')

# slide 1 tells users about the customization settings
def slide1_redrawAll(app):
    tutorialBackground(app)
    tutorialBackButton(app)
    tutorialForwardButton(app)
    drawLabel('BEFORE YOU START PLAYING...', 300, 150, size = 20, bold = True, font = 'monospace')
    drawLabel('make sure to customize your board!', 300, 175, size = 18, bold = True, font = 'monospace')
    drawLabel('Do this by pressing', 225, 265, size = 15, bold = True, font = 'monospace')
    drawLabel('the settings button', 225, 285, size = 15, bold = True, font = 'monospace')
    drawImage(app.slide1IMG, 425, 275, align = 'center', opacity = 100)

    drawLabel('Then you can customize your board like this one',
              300, 340, size = 15, bold = True, font = 'monospace')
    drawImage(app.slide1PinkIMG, 300, 415, align = 'center', opacity = 100)

def slide1_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')
    elif clickedOnButton(90, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('tutorial')
    elif clickedOnButton(470, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide2')

# slide 2 describes the basic goals of minesweeper
def slide2_redrawAll(app):
    tutorialBackground(app)
    tutorialBackButton(app)
    tutorialForwardButton(app)
    drawLabel('BASIC RULES', 300, 150, size = 20, bold = True, font = 'monospace')
    drawLabel('Minesweeper is a game where mines', 300, 200, size = 14, bold = True, font = 'monospace')
    drawLabel('are hidden in a grid of squares', 300, 220, size = 14, bold = True, font = 'monospace')
    drawLabel('Your goal is to identify the location', 300, 250, size = 14, bold = True, font = 'monospace')
    drawLabel('of all the safe squares and dig them up!', 300, 275, size = 14, bold = True, font = 'monospace')
    drawImage(app.slide1PinkIMG, 300, 415, align = 'center', opacity = 100)

def slide2_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')
    elif clickedOnButton(90, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide1')
    elif clickedOnButton(470, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide3')

# slide 3 describes the functions and rules in minesweeper
def slide3_redrawAll(app):
    tutorialBackground(app)
    tutorialBackButton(app)
    tutorialForwardButton(app)
    drawLabel('BASIC RULES', 300, 150, size = 20, bold = True, font = 'monospace')
    drawLabel('Start by digging into any spot on the board', 300, 200, size = 14, bold = True, font = 'monospace')
    drawLabel('(click on one of the cells!)', 300, 220, size = 14, bold = True, font = 'monospace')
    drawLabel('Safe squares have numbers telling you', 300, 250, size = 14, bold = True, font = 'monospace')
    drawLabel(' how many mines touch the square.', 300, 275, size = 14, bold = True, font = 'monospace')
    drawLabel('You can use the number clues to solve the game', 300, 300, size = 14, bold = True, font = 'monospace')
    drawLabel('by digging all of the safe squares.', 300, 315, size = 14, bold = True, font = 'monospace')
    drawImage(app.slide3IMG, 300, 415, align = 'center', opacity = 100)

def slide3_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')
    elif clickedOnButton(90, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide2')
    elif clickedOnButton(470, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide4')

# slide 4 describes how to place flags
def slide4_redrawAll(app):
    tutorialBackground(app)
    tutorialBackButton(app)
    tutorialForwardButton(app)
    drawLabel('BASIC RULES', 300, 150, size = 20, bold = True, font = 'monospace')
    drawLabel('You can place flags on squares you think are', 300, 250, size = 14, bold = True, font = 'monospace')
    drawLabel('hiding a mine by pressing the mine toggle', 300, 265, size = 14, bold = True, font = 'monospace')
    drawLabel('at the bottom of the screen', 300, 280, size = 14, bold = True, font = 'monospace')
    drawLabel("or by pressing 'm' on your keyboard", 300, 295, size = 14, bold = True, font = 'monospace')
    drawLabel("to switch modes.", 300, 310, size = 14, bold = True, font = 'monospace')
    drawImage(app.slide4IMG, 300, 415, align = 'center', opacity = 100)

def slide4_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')
    elif clickedOnButton(90, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide3')
    elif clickedOnButton(470, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide5')

# slide 5 describes what happens when the user loses
def slide5_redrawAll(app):
    tutorialBackground(app)
    tutorialBackButton(app)
    
    # home in button
    drawCircle(490, 490, 20, fill='green', border='black', borderWidth=2)
    drawLabel('home', 490, 490, size=12, bold = True, font = 'monospace')

    drawLabel('BASIC RULES', 300, 150, size = 20, bold = True, font = 'monospace')
    drawLabel('If you try and dig a square that is', 300, 250, size = 14, bold = True, font = 'monospace')
    drawLabel('hiding a mine, you lose the game and', 300, 275, size = 14, bold = True, font = 'monospace')
    drawLabel('all the mines are revealed in different colors :)', 300, 290, size = 14, bold = True, font = 'monospace')
    drawImage(app.slide5IMG, 300, 415, align = 'center', opacity = 100)

def slide5_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')
    elif clickedOnButton(90, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('slide4')
    elif clickedOnButton(470, 470, 40, 40, mouseX, mouseY):
        setActiveScreen('home')

## STORE SCREEN

## changeBoard screen where user can change board size
## changeBoard color screen
## change num flag screen

def store_redrawAll(app):
    drawHomeBoard(app)

    drawRect(150, 110, 300, 80, fill = rgb(160,240,255), border = 'black', borderWidth = 5)

    drawLabel('SETTINGS', 300, 150, size = 47.5, bold = True, font = 'monospace')

    # change board size button
    
    drawRect(225, 260, 150, 75, fill=rgb(160,240,255), border='black', borderWidth=2)
    drawLabel('Change Board', 300, 293, size=17, bold = True, font = 'monospace')
    drawLabel('Size', 300, 313, size=17, bold = True, font = 'monospace')


    # change board color button

    drawRect(225, 360, 150, 75, fill=rgb(160,240,255), border='black', borderWidth=2)
    drawLabel('Change Board', 300, 393, size=17, bold = True, font = 'monospace')
    drawLabel('Colors', 300, 413, size=17, bold = True, font = 'monospace')

    # change flag button
    
    drawRect(225, 460, 150, 75, fill=rgb(160,240,255), border='black', borderWidth=2)
    drawLabel('Change', 300, 491, size=17, bold = True, font = 'monospace')
    drawLabel('Difficulty', 300, 511, size=17, bold = True, font = 'monospace')

    # back to home button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')


def store_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(225, 260, 150, 75, mouseX, mouseY):
        # tutorial
        setActiveScreen('changeSize')
    elif clickedOnButton(225, 360, 150, 75, mouseX, mouseY):

        # starting game
        setActiveScreen('changeColor')
    elif clickedOnButton(225, 460, 150, 75, mouseX, mouseY):
        # Store    
        setActiveScreen('changeFlag')
    elif clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('home')


## change board size screen

def changeSize_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='pink')
    drawTempBoard(app)

    # row increase/decrease buttons
    drawRect(50, 575, 50, 50, fill='white', border='black', borderWidth=2)
    drawLabel('-', 75, 605, size=40, font = 'monospace')

    drawRect(112.5, 575, 100, 50, fill='white', border='black', borderWidth=2)
    drawLabel('rows', 162.5, 602, size=20, bold = True, font = 'monospace')


    drawRect(225, 575, 50, 50, fill='white', border='black', borderWidth=2)
    drawLabel('+', 250, 602, size=20, bold = True, font = 'monospace')


    # column increase/decrease buttons
    drawRect(325, 575, 50, 50, fill='white', border='black', borderWidth=2)
    drawLabel('-', 350, 605, size=40, font = 'monospace')

    drawRect(387.5, 575, 100, 50, fill='white', border='black', borderWidth=2)
    drawLabel('cols', 437.5, 602, size=20, bold = True, font = 'monospace')


    drawRect(500, 575, 50, 50, fill='white', border='black', borderWidth=2)
    drawLabel('+', 525, 602, size=20, bold = True, font = 'monospace')

    # back to store button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')

def changeSize_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(225, 575, 100, 50, mouseX, mouseY):
        if app.rows >= 4 and app.rows < 20:
            app.rows += 1
            createStandardBoard(app)
    elif clickedOnButton(50, 575, 50, 50, mouseX, mouseY):
        if app.rows > 4 and app.rows <= 20:
            app.rows -= 1
            createStandardBoard(app)
    elif clickedOnButton(500, 575, 50, 50, mouseX, mouseY):
        if app.cols >= 4 and app.cols < 20:
            app.cols += 1
            createStandardBoard(app)
    elif clickedOnButton(325, 575, 50, 50, mouseX, mouseY):
        if app.cols > 4 and app.cols <= 20:
            app.cols -= 1
            createStandardBoard(app)
    elif clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('store')

## change color screen

def changeColor_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='white')
    drawTempBoard(app)

    # color option buttons
    drawRect(75, 575, 50, 50, fill='pink', border='black', borderWidth=2)

    drawRect(175, 575, 50, 50, fill='orange', border='black', borderWidth=2)

    drawRect(275, 575, 50, 50, fill='papayaWhip', border='black', borderWidth=2)

    drawRect(375, 575, 50, 50, fill='blue', border='black', borderWidth=2)

    drawRect(475, 575, 50, 50, fill='purple', border='black', borderWidth=2)

    drawRect(250, 647.5, 100, 50, fill='white', border='black', borderWidth=2)
    drawLabel('reset', 300, 647.5+25, size=20, bold = True, font = 'monospace')

    # back to store button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')

def changeColor_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(75, 575, 50, 50, mouseX, mouseY):
        # pink!
        app.colorBoardEven = rgb(255, 155, 222)
        app.colorBoardOdd = rgb(242, 98, 179) # rgb(255, 102, 204)
        app.boardColor = 'pink'
        createStandardBoard(app)
    elif clickedOnButton(175, 575, 50, 50, mouseX, mouseY):
        # orange!
        app.colorBoardEven = rgb(255, 164, 102) 
        app.colorBoardOdd = rgb(255, 102, 0)
        app.boardColor = 'orange'
        createStandardBoard(app)
    elif clickedOnButton(275, 575, 50, 50, mouseX, mouseY):
        # yellow!
        app.colorBoardEven = 'papayaWhip' 
        app.colorBoardOdd = rgb(255, 220, 158)
        app.boardColor = 'yellow'
        createStandardBoard(app)
    elif clickedOnButton(375, 575, 50, 50, mouseX, mouseY):
        # blue!
        app.colorBoardEven = rgb(131, 168, 255) 
        app.colorBoardOdd = rgb(41, 106, 255)
        app.boardColor = 'blue'
        createStandardBoard(app)
    elif clickedOnButton(475, 575, 50, 50, mouseX, mouseY):
        # purple!
        app.colorBoardEven = rgb(216, 124, 255) 
        app.colorBoardOdd = rgb(179, 0, 255)
        app.boardColor = 'purple'
        createStandardBoard(app)
    elif clickedOnButton(250, 647.5, 100, 50, mouseX, mouseY):
        # reset back to green!
        app.colorBoardEven = rgb(81, 250, 81)
        app.colorBoardOdd = rgb(0, 235, 0)
        app.boardColor = 'default'
        createStandardBoard(app)
    elif clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('store')

## change number of flags

def changeFlag_redrawAll(app):
    drawHomeBoard(app)

    drawRect(75, 75, 450, 102, fill = 'white', border = 'black', borderWidth = 5)
    drawLabel('Choose your level', 300, 100, size = 40, bold = True, font = 'monospace')
    drawLabel('of difficulty', 300, 150, size = 40, bold = True, font = 'monospace')
    
    if app.percentCellsMines == 0.12:
        drawRect(200, 200, 200, 75, fill = app.buttonClick, border = 'black', borderWidth = 2)
    else:
        drawRect(200, 200, 200, 75, fill = 'white', border = 'black', borderWidth = 2)
    drawLabel('Easy', 300, 237.5, size = 40, font = 'monospace')

    if app.percentCellsMines == 0.15:
        drawRect(200, 300, 200, 75, fill = app.buttonClick, border = 'black', borderWidth = 2)
    else:
        drawRect(200, 300, 200, 75, fill = 'white', border = 'black', borderWidth = 2)
    drawLabel('Medium', 300, 337.5, size = 40, font = 'monospace')
    
    if app.percentCellsMines == 0.20:
        drawRect(200, 400, 200, 75, fill = app.buttonClick, border = 'black', borderWidth = 2)
    else:
        drawRect(200, 400, 200, 75, fill = 'white', border = 'black', borderWidth = 2)
    drawLabel('Hard', 300, 437.5, size = 40, font = 'monospace')

    drawRect(225, 515, 150, 70, fill = 'white', border = 'black', borderWidth = 3)
    drawImage(app.flagImage, 250, 550, width = 40, height = 40, align = 'center', opacity = 100)
    drawLabel(f'X {app.numMines}', 315, 550, size = 35, font = 'monospace')

    # back to store button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')

def changeFlag_onMousePress(app, mouseX, mouseY):
    if clickedOnButton(200, 200, 200, 75, mouseX, mouseY):
        
        app.percentCellsMines = 0.12
        createStandardBoard(app)
    elif clickedOnButton(200, 300, 200, 75, mouseX, mouseY):
        app.percentCellsMines = 0.15
        createStandardBoard(app)
    elif clickedOnButton(200, 400, 200, 75, mouseX, mouseY):
        app.percentCellsMines = 0.20
        createStandardBoard(app)
    elif clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY):
        setActiveScreen('store')

# drawing the board
def drawTempBoard(app):
    color = None
    for row in range(app.rows):
        for col in range(app.cols):
            if row % 2 == col % 2:
                color = app.colorBoardEven
            else:
                color = app.colorBoardOdd
            
            drawTempCell(app, row, col, color, None)

# def drawCell(app, row, col, color):
def drawTempCell(app, row, col, color, val):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
    

## GAME SCREEN

def game_redrawAll(app):
    backGroundColor = 'pink' #rgb(230,240,200)
    #rgb(160,240,255)
    drawRect(0, 0, app.width, app.height, fill=backGroundColor)

    # back to store button
    drawRect(10, 647.5, 50, 45, fill='white', border='black', borderWidth=2)
    drawLabel('back', 35, 670, size=18, bold = True, font = 'monospace')


    drawBoard(app)
    
    if app.rows > len(app.displayedBoard) or app.cols > len(app.displayedBoard[0]):
        return
    # drawing the flags
    for row in range(app.rows):
        for col in range(app.cols):
            if app.displayedBoard[row][col] == 'X':
                if app.flagImage:
                    cellLeft, cellTop = getCellLeftTop(app, row, col)
                    cellWidth, cellHeight = getCellSize(app)
                    x = cellLeft+ cellWidth/2
                    y = cellTop + cellHeight/2
                    drawImage(app.flagImage, x, y, align = 'center', opacity = 100)

    buttonColor = rgb(160,240,255)
    
    if app.gameOver == True:
        # get this to appear after all mines have been revealed
        if app.minesToBeRevealed == app.numCorrectMines:
            drawGameOver(app)
            drawLabel('GAME OVER', 300, 175, size=40, bold = True, font = 'monospace')
    if app.solved == True:
        drawSolved(app)
        drawLabel('SOLVED', 300, 175, size=40, bold = True, font = 'monospace')
    if app.showHint == True:
        drawRect(125, 625, 350, 50, fill = buttonColor, border = 'black', borderWidth = 2)
        drawLabel(app.hint, 300, 650, size=15, bold = True, font = 'monospace')  

    
    # number of mines left that need to be placed
    drawRect(100, 5, 100, 40, fill=buttonColor, border='black', borderWidth=2)
    drawImage(app.flagImage, 100, 5, width = 40, height = 40)
    drawLabel(f'x {app.numMinesLeft}', 160, 30, size=25, font = 'monospace')
    
    drawRect(407, 5, 100, 40, fill=buttonColor, border='black', borderWidth=2)
    drawImage(app.hintIMG, 400, 5)
    drawLabel(f' x {app.numHints}', 470, 30, size=30, font = 'monospace')

    # timer
    drawRect(250, 5, 100, 40, fill=buttonColor, border='black', borderWidth=2)
    drawImage(app.timerIMG, 255, 8, width = 35, height = 35)
    drawLabel(f' {app.timer}', 310, 26, size = 30, font = 'monospace')

    # drawing the buttons
    # drawing the new game button
    drawRect(100, 560, 100, 50, fill=buttonColor, border='black', borderWidth=2)

    drawLabel('New Game', 150, 585, size=14, bold = True, font = 'monospace')

    # drawing the hint button
    drawRect(250, 560, 100, 50, fill=buttonColor, border='black', borderWidth=2)

    drawImage(app.hintIMG, 267, 565)

    # drawing the change mode button
    drawRect(400, 560, 75, 50, fill=buttonColor, border='black', borderWidth=2)
    if app.placingMines == False:
        drawRect(405, 567.5, 35, 35, fill='pink', border='black')
    else:
        drawImage(app.flagImage, 475, 565, width = 40, height = 40)
        drawRect(435, 567.5, 35, 35, fill='green', border='black')


## GENERATING + DRAWING BOARD
# this function randomly generates the answerBoard
def generateBoard(app):
    # randomly generate app.numMines amount of numbers between 0 and app.row x app.col
    # AKA randomly generate app.numMines amount of cell numbers
    # loop through answerBoard and assign the -1 to the cells that are mines
    # then another function goes through and assigns the rest of the cells a 
    # number based on the number of mines they each touch

    # keep generating until user's first click is on an empty square
    generateMines(app)
    generateLandSquares(app)
    
# generates the mines for the board    
def generateMines(app):
    mineCells = set()

    # generating random cells for Mine
    while len(mineCells) < (app.numMines):
        randomRow = random.randint(0, app.rows-1)
        randomCol = random.randint(0, app.cols-1)
        possibleIndex = (randomRow, randomCol)
        # if the index is already in mineCells, it won't be added again bc sets
        mineCells.add(possibleIndex)

    
    # loop through app.answerBoard and replace each of the mineCells with a mine
    for row in range(app.rows):
        for col in range(app.cols):
            if (row, col) in mineCells:
                app.answerBoard[row][col] = '-1'
    
# generates the values for the land squares on our board
def generateLandSquares(app):
    # loop through answer board, if the square is land call another function
    # that returns the number it must be (num mines touching it)
    # if it is not touching a mine 0

    for row in range(app.rows):
        for col in range(app.cols):
            if app.answerBoard[row][col] != '-1':
                val = numAdjacentMines(app, row, col)
                app.answerBoard[row][col] = val

# returns the number of mines a given cell is touching
def numAdjacentMines(app, row, col):
    numMines = 0
    for drow in range(-1, 2):
        for dcol in range(-1, 2):

            newRow = row + drow
            newCol = col + dcol
            if ((newRow > -1 and newRow < app.rows) and
                (newCol > -1 and newCol < app.cols) and
                (app.answerBoard[newRow][newCol] == '-1')):
                    numMines += 1
                
    return str(numMines)

# returns the highlighting color based on the theme the user chose
def getHighlightedColor(app):
    if app.boardColor == 'pink':
        return rgb(255, 223, 248)
    elif app.boardColor == 'orange':
        return rgb(255, 217, 159)
    elif app.boardColor == 'yellow':
        return rgb(255, 255, 205)
    elif app.boardColor == 'blue':
        return rgb(193, 212, 255)
    elif app.boardColor == 'purple':
        return rgb(244, 219, 255)
    elif app.boardColor == 'default':
        return rgb(153, 255, 153)

# drawing the board
def drawBoard(app):
    color = None
    circleColor = None
    if app.rows > len(app.displayedBoard) or app.cols > len(app.displayedBoard[0]):
        return
    for row in range(app.rows):
        for col in range(app.cols):
            # highlighting where mouse is feature
            if ((app.gameOver == False) and 
                (app.placingMines == False) and
                (row == app.highlightedX and col == app.highlightedY)):
                if app.showHint == False or app.hintCoordinates != (row, col):
                    color = getHighlightedColor(app)
                else:
                    color = 'yellow'
            # highlighting which cell the hint is talking about
            elif (row, col) == app.hintCoordinates:
                color = rgb(255,255,0)
            # revealing the mines when game over
            elif app.displayedBoard[row][col] == 'REVEAL':
                if (row,col) in app.mineRevealColors:
                    (r,g,b) = app.mineRevealColors[(row,col)]
                    color = rgb(r,g,b)
                    circleColor = rgb((r-50)%255,(g-50)%255,(b-50)%255)
                else:
                    randomColor = random.randint(0, 8)
                    (r,g,b) = app.mineRevealColorOptions[randomColor]
                    app.mineRevealColors[(row,col)] = (r,g,b)
                    color = rgb(r,g,b)
                    circleColor = rgb((r-50)%255,(g-50)%255,(b-50)%255)
            # making the land checkered board
            elif ((app.displayedBoard[row][col] == None) or
                  (app.displayedBoard[row][col] == 'X') or
                  (app.displayedBoard[row][col] == 'WRONG')):
                # making checkered board
                if row % 2 == col % 2:
                    color =  app.colorBoardEven
                else:
                    color =  app.colorBoardOdd
            # making the dug up land checkered board (brown)
            else:
                if row % 2 == col % 2:
                    color = rgb(232, 190, 175)
                else:
                    color = rgb(206, 157, 139)
            
            drawCell(app, row, col, color, app.displayedBoard[row][col])
            
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            x = cellLeft+ cellWidth/2
            y = cellTop + cellHeight/2

            # drawing the flags
            if ((app.gameOver == False) and 
                (app.placingMines == True) and
                (row == app.highlightedX and col == app.highlightedY)):
                if app.flagImage:
                    drawImage(app.flagImage, x, y, align = 'center', opacity = 75)

            if app.displayedBoard[row][col] == 'REVEAL':
                drawCircle(x, y, app.cellLength/5, fill = circleColor)
                

def game_onMouseMove(app, mouseX, mouseY):
    if getCell(app, mouseX, mouseY) != None:
        (row, col) = getCell(app, mouseX, mouseY)
        if (app.displayedBoard[row][col] == None):
            app.highlightedX = row
            app.highlightedY = col
        else:
            app.highlightedX = None
            app.highlightedY = None

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=app.cellBorderWidth)

# def drawCell(app, row, col, color):
def drawCell(app, row, col, color, val):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
    
    
    if ((app.displayedBoard[row][col] != None and
         app.displayedBoard[row][col].isdigit()) and
        (int(app.displayedBoard[row][col]) > 0)):
        drawCellBorder(app, row, col, cellLeft, cellTop, cellLeft + cellWidth, cellTop + cellHeight)

    if val == 'WRONG':
        drawLabel('X', cellLeft+ cellWidth/2, cellTop + cellHeight/2, size = 12)
    elif val != None and val != '0' and val != 'X' and val != 'REVEAL':
        drawLabel(str(val), cellLeft+ cellWidth/2, cellTop + cellHeight/2, size = 12)

def drawCellBorder(app, row, col, cellLeft, cellTop, cellRight, cellBottom):
    color = rgb(186, 137, 119)
    # checking where to draw the border
    # checking if there is land to the left  
    if ((col - 1 >= 0) and
        ((app.displayedBoard[row][col-1] == None) or
         (app.displayedBoard[row][col-1] == 'X') or
         (app.displayedBoard[row][col-1] == 'WRONG'))):
        drawLine(cellLeft, cellTop, cellLeft, cellBottom, fill=color, lineWidth=1.5)
    
    # checking if there is land to the right
    if ((col + 1 < app.cols) and
        ((app.displayedBoard[row][col+1] == None) or
         (app.displayedBoard[row][col+1] == 'X') or
         (app.displayedBoard[row][col+1] == 'WRONG'))):
        drawLine(cellRight, cellTop, cellRight, cellBottom, fill=color, lineWidth=3)

    # checking if there is land above
    if ((row - 1 >= 0) and
        ((app.displayedBoard[row-1][col] == None) or
         (app.displayedBoard[row-1][col] == 'X') or
         (app.displayedBoard[row-1][col] == 'WRONG'))):
        drawLine(cellLeft, cellTop, cellRight, cellTop, fill=color, lineWidth=1.5)

    # checking if there is land below
    if ((row + 1 < app.rows) and
        ((app.displayedBoard[row+1][col] == None) or
         (app.displayedBoard[row+1][col] == 'X') or
         (app.displayedBoard[row+1][col] == 'WRONG'))):
        drawLine(cellLeft, cellBottom, cellRight, cellBottom, fill=color, lineWidth=3)

## BOARD FUNCTIONS

def game_onMousePress(app, mouseX, mouseY):

    if app.gameOver == False and app.solved == False and app.showHint == True: # display hint
        
        if app.hint != 'you are out of hints!' and app.hintCoordinates != None:
            (rowH,colH) = app.hintCoordinates
            cellLeft, cellTop = getCellLeftTop(app, rowH, colH)
            # if you click on the board, but not on the hint cell, the hint stays
            if ((not clickedOnButton(cellLeft, cellTop, app.cellLength, app.cellLength, mouseX, mouseY)) and 
                (clickedOnButton(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, mouseX, mouseY))):
                playGame(app, mouseX, mouseY)
                return
            # if you click on the hint cell
            elif clickedOnButton(cellLeft, cellTop, app.cellLength, app.cellLength, mouseX, mouseY):
                app.hintCoordinates = (None, None)
                app.showHint = False
                playGame(app, mouseX, mouseY)
                return
        else:
            app.showHint = False
        
    if clickedOnButton(100, 560, 100, 50, mouseX, mouseY): # new game bottom left
        app.rows = 10
        app.cols = 10
        app.displayedBoard = [([None] * app.cols) for row in range(app.rows)]
        app.answerBoard = [([None] * app.cols) for row in range(app.rows)]
        newGame(app)
    elif clickedOnButton(10, 647.5, 50, 45, mouseX, mouseY): # back button
        setActiveScreen('home')
    elif ((app.gameOver == True) and 
        (app.minesToBeRevealed == app.numCorrectMines) and
        (clickedOnButton(175, 375, 100, 50, mouseX, mouseY))): # new game button in game over
        # resetting the board before the user clicks so that 
        # we avoid an index out of range error
        app.rows = 10
        app.cols = 10
        app.displayedBoard = [([None] * app.cols) for row in range(app.rows)]
        app.answerBoard = [([None] * app.cols) for row in range(app.rows)]
        newGame(app)
    elif ((((app.gameOver == True) and 
        (app.minesToBeRevealed == app.numCorrectMines)) or app.solved) and
        (clickedOnButton(325, 375, 100, 50, mouseX, mouseY))): # customize button in game over
        app.rows = 10
        app.cols = 10
        app.displayedBoard = [([None] * app.cols) for row in range(app.rows)]
        app.answerBoard = [([None] * app.cols) for row in range(app.rows)]
        newGame(app)
        setActiveScreen('store')
    elif app.numHints >= 0 and clickedOnButton(250, 560, 100, 50, mouseX, mouseY): # hint button
        dealWithHint(app)
    elif clickedOnButton(400, 560, 100, 50, mouseX, mouseY): # changing mode button
        app.placingMines = not (app.placingMines)
    elif app.solved and clickedOnButton(175, 375, 100, 50, mouseX, mouseY): # new game button in solved
        app.rows = 10
        app.cols = 10
        app.displayedBoard = [([None] * app.cols) for row in range(app.rows)]
        app.answerBoard = [([None] * app.cols) for row in range(app.rows)]
        newGame(app)
    elif app.solved and clickedOnButton(325, 375, 100, 50, mouseX, mouseY): # home button in solved
        app.rows = 10
        app.cols = 10
        app.displayedBoard = [([None] * app.cols) for row in range(app.rows)]
        app.answerBoard = [([None] * app.cols) for row in range(app.rows)]
        newGame(app)
        setActiveScreen('store')
    elif getCell(app, mouseX, mouseY) != None and app.gameOver == False: # clicking on the board
        playGame(app, mouseX, mouseY)

def playGame(app, mouseX, mouseY):
    app.highlightedX = None
    app.highlightedY = None
    if app.gameStarted == False and app.solved == False:
        app.firstX = mouseX
        app.firstY = mouseY
        generateBoard(app)
        (row, col) = getCell(app, mouseX, mouseY)
        # keep generating board until user's first click is on an empty square
        while app.answerBoard[row][col] != '0':
            app.answerBoard = [([None] * app.cols) for row in range(app.rows)]
            generateBoard(app)
        # generate the random block that is revealed from the first click
        clickOnEmpty(app, row, col)
        app.gameStarted = True

    else:
        # identifying cell the user clicked in
        (row, col) = getCell(app, mouseX, mouseY)

        # if user digs up a mine, the game is over and they lose
        if ((app.answerBoard[row][col] == '-1') and 
            (app.placingMines == False) and
            (app.displayedBoard[row][col] != 'X')):
            app.gameOver = True
            changeUserInformation(app, ' losses')
        
        elif app.displayedBoard[row][col] == None:
            if app.placingMines == False:
                # if the user digs on an empty cell, board automatically digs up
                # surrounding squares
                if app.answerBoard[row][col] == '0':
                    clickOnEmpty(app, row, col)
                else:
                     app.displayedBoard[row][col] = app.answerBoard[row][col]
            else:
                # user is placing a flag
                (row, col) = getCell(app, mouseX, mouseY)
                app.displayedBoard[row][col] = 'X'
                app.numMinesLeft -= 1
                # checking if it is a correct placement
                if app.answerBoard[row][col] == '-1':
                    app.numCorrectMines += 1

        # if user clicks on flag in mine setting, removes flag
        elif ((app.displayedBoard[row][col] == 'X') and 
            (app.placingMines == True)):
            app.displayedBoard[row][col] = None
            app.numMinesLeft += 1
            if app.answerBoard[row][col] == '-1':
                app.numCorrectMines -= 1
        
        # check if the board has been fully solved and if it is correct
        if isSolved(app):
            app.solved = True
            changeUserInformation(app, ' wins')

def game_onKeyPress(app, key):
    if key == 'm':
        app.placingMines = not (app.placingMines)

## SOLVED OR LOST
def drawSolved(app):
    drawRect(125, 125, 350, 350, fill=rgb(160,240,255))
    # hints used
    drawImage(app.hintIMG, 150, 200)
    drawLabel(f' used: {3-app.numHints}', 240, 225, size=20, bold = True, font = 'monospace')
    # flags placed
    drawLabel(f'correct    placed: {app.numCorrectMines}', 260, 275, size=20, bold = True, font = 'monospace')
    drawImage(app.flagImage, 225, 250, width = 40, height = 40)
    # time spent
    drawImage(app.timerIMG, 170, 305, width = 35, height = 35)
    secondS = '' # sometimes we have an s at the end, sometimes we don't
    if app.timer == 1:
        secondS = 'second'
    else:
        secondS = 'seconds'
    drawLabel(f' {app.timer} {secondS}', 300, 323, size = 30, bold = True, font = 'monospace')
    # restart button
    drawRect(175, 375, 100, 50, fill='pink', border='black', borderWidth=2)

    drawLabel('New Game', 225, 390, size=14, bold = True, font = 'monospace')
    drawLabel('Default Board', 225, 405, size=12, bold = True, font = 'monospace')
    # menu button
    drawRect(325, 375, 100, 50, fill='pink', border='black', borderWidth=2)

    drawLabel('New Game', 375, 390, size=14, bold = True, font = 'monospace')
    drawLabel('Customize Board', 375, 405, size=10, bold = True, font = 'monospace')

    

# draws the box that comes up when the user loses
def drawGameOver(app):
    drawRect(125, 125, 350, 350, fill=rgb(160,240,255))
    # hints used
    drawImage(app.hintIMG, 150, 200)
    drawLabel(f' used: {3-app.numHints}', 240, 225, size=20, bold = True, font = 'monospace')
    # flags placed
    drawLabel(f'correct    placed: {app.numCorrectMines}', 260, 275, size=20, bold = True, font = 'monospace')
    drawImage(app.flagImage, 225, 250, width = 40, height = 40)
    # time spent
    drawImage(app.timerIMG, 170, 305, width = 35, height = 35)
    secondS = '' # sometimes we have an s at the end, sometimes we don't
    if app.timer == 1:
        secondS = 'second'
    else:
        secondS = 'seconds'
    drawLabel(f' {app.timer} {secondS}', 300, 323, size = 30, bold = True, font = 'monospace')
    # restart button
    drawRect(175, 375, 100, 50, fill='pink', border='black', borderWidth=2)

    drawLabel('New Game', 225, 390, size=14, bold = True, font = 'monospace')
    drawLabel('Default Board', 225, 405, size=12, bold = True, font = 'monospace')
    # menu button
    drawRect(325, 375, 100, 50, fill='pink', border='black', borderWidth=2)

    drawLabel('New Game', 375, 390, size=14, bold = True, font = 'monospace')
    drawLabel('Customize Board', 375, 405, size=10, bold = True, font = 'monospace')
    

# only used at the end to reveal mines that the user did not find
def takeStep(app):
    # finding the first mine that needs to be revealed
    foundFirst = False
    for row in range(app.rows):
        for col in range(app.cols):
            if foundFirst == False:
                if (app.answerBoard[row][col] == '-1' and
                    app.displayedBoard[row][col] == None):
                    app.displayedBoard[row][col] = 'REVEAL'
                    app.minesToBeRevealed -= 1
                    # app.soundExplosion.play()
                    
                    foundFirst = True
                if ((app.answerBoard[row][col] != '-1') and
                    (app.displayedBoard[row][col] == 'X')):
                    app.displayedBoard[row][col] = 'WRONG'

def game_onStep(app):
    if app.gameOver == True and app.minesToBeRevealed > 0:
        takeStep(app)
    elif app.minesToBeRevealed == app.numCorrectMines or app.solved:
        return
    elif app.gameStarted:
        
        app.count += 1
        if app.count % 5 == 0:
            app.timer += 1

# checks that all the nonmines in answer have been dug on displayed board
# not all mines need to have been placed for the user to have a correct board
def isSolved(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if ((app.answerBoard[row][col] != '-1') and
                ((app.displayedBoard[row][col] == 'X') or 
                (app.displayedBoard[row][col] == None))):
                return False
    return True

## GAME FEATURES

# randomly generates a block of land around the user's mouse click
def clickOnEmpty(app, row, col):
    if (app.answerBoard[row][col] != '0'):
        if app.answerBoard[row][col] != '-1':
            app.displayedBoard[row][col] = app.answerBoard[row][col]
    else:
    # we know our current cell is a 0 - not a bomb
        for drow in range(-1, 2):
            for dcol in range(-1, 2):
                newRow = row + drow
                newCol = col + dcol
                if (app.rows > newRow >= 0 and app.cols > newCol >= 0):
                    # if our new cell is already displayed, we skip it
                    if app.displayedBoard[newRow][newCol] != app.answerBoard[row][col]:
                        # if cell isn't a bomb, display
                        if (app.answerBoard[newRow][newCol] != '-1'):
                            app.displayedBoard[row][col] = app.answerBoard[row][col]
                        clickOnEmpty(app, newRow, newCol)
                             
# gets the cell that user clicks in
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None


def clickedOnButton(buttonX, buttonY, buttonWidth, buttonHeight, x, y):
    
    if (buttonX <= x <= buttonX + buttonWidth) and (buttonY <= y <= buttonY + buttonHeight):
        return True
    else:
        return False
    

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = app.cellLength, app.cellLength

    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)



def main():
    runAppWithScreens('login')

main()

