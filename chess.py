#!/usr/bin/env python3
class Piece:
    def __init__(self, c, r, l):
        self._colour = c
        self._role = r
        self._location = l
        
    def getColour(self):
        return self._colour
        
    def getRole(self):
        return self._role
        
    def getLocation(self):
        return self._location
    
    def getIconChar(self):
        return 9812
    
    def move(self, currentLocation, newLocation, square):
        self._location = newLocation
        square.squareUpdate(currentLocation, newLocation, self)
        
    def __str__(self):
        return chr(self.getIconChar())
        
    def checkMove(self, location, newLocation, square):
        return False
    
    def getDelta(self, currentLocation, newLocation): # return (deltaX, deltaY) = (column, row) = (alpha, num)
        currentIndex = currentLocation.getMatrixIndex()
        newIndex = newLocation.getMatrixIndex()
        deltaY = newIndex[0] - currentIndex[0]
        deltaX = newIndex[1] - currentIndex[1]
        return (deltaX, deltaY)
    
    def isEnemy(self, other): # return True if its enemy
        # print('isEnemy')
        # print(self.getColour(), other.getColour())
        if self.getColour() != other.getColour():
            return True
        else:
            return False
        
    def checkBlock(self, currentLocation, newLocation, square, delta):
        # print(delta)
        if delta[0]: # get one step
            deltaStep = [int(i / abs(delta[0])) for i in delta]
        else:
            deltaStep = [int(i / abs(delta[1])) for i in delta]
        step = currentLocation.add(deltaStep[0], deltaStep[1])
        # print('deltaStep: ', deltaStep)
        # print('current: ', currentLocation.getMatrixIndex())
        # i = 0
        # while i != 2:
        #     i = i + 1
        while not step.getMatrixIndex() == newLocation.getMatrixIndex():
            # print('step: ', step.getMatrixIndex())
            # print('new: ', newLocation.getMatrixIndex())
            if not square.checkEmpty(step): # if not empty, means there's something on the way
                return False
            step = step.add(deltaStep[0], deltaStep[1])
        return True

class King(Piece):
    def __init__(self, c, l):
        super().__init__(c, 'King', l)
        
    def getIconChar(self):
        if self.getColour() == 'w':
            return super().getIconChar() + 0
        else:
            return super().getIconChar() + 6
        
    def __str__(self):
        if self.getColour() == 'w':
            return chr(super().getIconChar() + 0)
        else:
            return chr(super().getIconChar() + 6)
        
    def checkMove(self, currentLocation, newLocation, square):
        delta = self.getDelta(currentLocation, newLocation)
        onNewLocation = square.getSpot(newLocation)
        if abs(delta[0]) == 1:
            if abs(delta[1]) == 1 or abs(delta[1]) == 0:
                if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                    return False # if there is a piece and its not enemy
                elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                    square.capture(onNewLocation)
                    return True # is enemy
                else:
                    return True # no piece
            else:
                return False
        elif abs(delta[0]) == 0 and abs(delta[1]) == 1:
            if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation): 
                return False # if there is a piece and its not enemy
            elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                square.capture(onNewLocation)
                return True # is enemy
            else:
                return True # no piece
        else:
            return False
        
class Queen(Piece):
    def __init__(self, c, l):
        super().__init__(c, 'Queen', l)
        
    def getIconChar(self):
        if self.getColour() == 'w':
            return super().getIconChar() + 1
        else:
            return super().getIconChar() + 7
        
    def __str__(self):
        if self.getColour() == 'w':
            return chr(super().getIconChar() + 1)
        else:
            return chr(super().getIconChar() + 7)
        
    def checkMove(self, currentLocation, newLocation, square):
        delta = self.getDelta(currentLocation, newLocation)
        onNewLocation = square.getSpot(newLocation)
        if abs(delta[0]) == abs(delta[1]):
            if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                return False # if there is a piece and its not enemy
            elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    square.capture(onNewLocation)
                    return True # if there's a piece and is enemy
            else:
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    return True # if there's no piece
        elif abs(delta[0]) == 0 or abs(delta[1]) == 0:
            if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                return False # if there is a piece and its not enemy
            elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    square.capture(onNewLocation)
                    return True # if there's a piece and is enemy
                else:
                    return False
            else:
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    return True # if there's no piece
                else:
                    return False
        else:
            return False
        
class Castle(Piece):
    def __init__(self, c, l):
        super().__init__(c, 'Castle', l)
        
    def getIconChar(self):
        if self.getColour() == 'w':
            return super().getIconChar() + 2
        else:
            return super().getIconChar() + 8
        
    def __str__(self):
        if self.getColour() == 'w':
            return chr(super().getIconChar() + 2)
        else:
            return chr(super().getIconChar() + 8)
        
    def checkMove(self, currentLocation, newLocation, square):
        delta = self.getDelta(currentLocation, newLocation)
        onNewLocation = square.getSpot(newLocation)
        if abs(delta[0]) == 0 or abs(delta[1]) == 0:
            if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                return False # if there is a piece and its not enemy
            elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    square.capture(onNewLocation)
                    return True # if there's a piece and is enemy
                else:
                    return False
            else:
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    return True # if there's no piece
                else:
                    return False
        else:
            return False
        
class Bishop(Piece):
    def __init__(self, c, l):
        super().__init__(c, 'Bishop', l)
        
    def getIconChar(self):
        if self.getColour() == 'w':
            return super().getIconChar() + 3
        else:
            return super().getIconChar() + 9
        
    def __str__(self):
        if self.getColour() == 'w':
            return chr(super().getIconChar() + 3)
        else:
            return chr(super().getIconChar() + 9)
        
    def checkMove(self, currentLocation, newLocation, square):
        delta = self.getDelta(currentLocation, newLocation)
        onNewLocation = square.getSpot(newLocation)
        #print('onNewLocation', onNewLocation)
        if abs(delta[0]) == abs(delta[1]):
            if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                return False # if there is a piece and its not enemy
            elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    square.capture(onNewLocation)
                    return True # if there's a piece and is enemy
                else:
                    return False # the way is blocked
            else:
                if super().checkBlock(currentLocation, newLocation, square, delta):
                    return True # if there's no piece
                else:
                    return False
        else:
            return False
        
class Knight(Piece): # can be blocked
    def __init__(self, c, l):
        super().__init__(c, 'Knight', l)
        
    def getIconChar(self):
        if self.getColour() == 'w':
            return super().getIconChar() + 4
        else:
            return super().getIconChar() + 10
        
    def __str__(self):
        if self.getColour() == 'w':
            return chr(super().getIconChar() + 4)
        else:
            return chr(super().getIconChar() + 10)
        
    def checkMove(self, currentLocation, newLocation, square):
        delta = self.getDelta(currentLocation, newLocation)
        onNewLocation = square.getSpot(newLocation)
        if abs(delta[0]) == 2 and abs(delta[1]) == 1:
            if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                return False # if there is a piece and its not enemy
            elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                square.capture(onNewLocation)
                return True # is enemy
            else:
                return True # no piece
        elif abs(delta[1]) == 2 and abs(delta[0]) == 1:
            if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                return False # if there is a piece and its not enemy
            elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                square.capture(onNewLocation)
                return True # is enemy
            else:
                return True # no piece 
        else:
            return False
    
class Pawn(Piece):
    def __init__(self, c, l, m = 0):
        super().__init__(c, 'Pawn', l)
        self._move = m
        
    def getMove(self):
        return self._move
    
    def countMove(self):
        self._move = self._move + 1
    
    def move(self, currentLocation, newLocation, square):
        super().move(currentLocation, newLocation, square)
        self.countMove()
        
    def getIconChar(self):
        if self.getColour() == 'w':
            return super().getIconChar() + 5
        else:
            return super().getIconChar() + 11
        
    def __str__(self):
        if self.getColour() == 'w':
            return chr(super().getIconChar() + 5)
        else:
            return chr(super().getIconChar() + 11)
        
    def checkMove(self, currentLocation, newLocation, square):
        delta = self.getDelta(currentLocation, newLocation)
        onNewLocation = square.getSpot(newLocation)
        if delta[0] == 0:
            if self.getColour() == 'w': # white moves forwar, index delta is negative
                if delta[1] == -1 or (delta[1] == -2 and not self.getMove()): # only first move can move two
                    if isinstance(onNewLocation, Piece): # if there's a piece on the spot, it can't move this way
                        return False
                    return True # cannot capture this way
            elif self.getColour() == 'b':
                if delta[1] == 1 or (delta[1] == 2 and not self.getMove()): # black moves forwar, index delta is positive
                    if isinstance(onNewLocation, Piece):
                        return False
                    return True # cannot capture this way
        elif abs(delta[0]) == 1:
            if self.getColour() == 'w' and delta[1] == -1:
                if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                    return False
                elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                    square.capture(onNewLocation)
                    return True # is enemy
                else:
                    return False # no piece -> cannot move this way
            elif self.getColour() == 'b' and delta[1] == 1:
                onNewLocation = square.getSpot(newLocation)
                if isinstance(onNewLocation, Piece) and not self.isEnemy(onNewLocation):
                    return False
                elif isinstance(onNewLocation, Piece) and self.isEnemy(onNewLocation):
                    square.capture(onNewLocation)
                    return True # is enemy
                else:
                    return False # no piece -> cannot move this way
        else:
            return False
        
class Square:
    def __init__(self, m = [['　' for i in range(8)] for j in range(8)], wDead = [], bDead = [], w = False, c = ['b', 'w'], t = 'w'):
        self._matrix = m
        self._whiteDead = wDead
        self._blackDead = bDead
        self._win = w
        self._winColour = c
        self._colourTurn = t
    
    def startGame(self):
        self._matrix[1][0] = Pawn('b', Location('A', 7))
        self._matrix[1][1] = Pawn('b', Location('B', 7))
        self._matrix[1][2] = Pawn('b', Location('C', 7))
        self._matrix[1][3] = Pawn('b', Location('D', 7))
        self._matrix[1][4] = Pawn('b', Location('E', 7))
        self._matrix[1][5] = Pawn('b', Location('F', 7))
        self._matrix[1][6] = Pawn('b', Location('G', 7))
        self._matrix[1][7] = Pawn('b', Location('H', 7))
        self._matrix[0][0] = Castle('b', Location('A', 8))
        self._matrix[0][7] = Castle('b', Location('H', 8))
        self._matrix[0][1] = Knight('b', Location('B', 8))
        self._matrix[0][6] = Knight('b', Location('G', 8))
        self._matrix[0][2] = Bishop('b', Location('C', 8))
        self._matrix[0][5] = Bishop('b', Location('F', 8))
        self._matrix[0][3] = Queen('b', Location('D', 8))
        self._matrix[0][4] = King('b', Location('E', 8))
        
        self._matrix[6][0] = Pawn('w', Location('A', 2))
        self._matrix[6][1] = Pawn('w', Location('B', 2))
        self._matrix[6][2] = Pawn('w', Location('C', 2))
        self._matrix[6][3] = Pawn('w', Location('D', 2))
        self._matrix[6][4] = Pawn('w', Location('E', 2))
        self._matrix[6][5] = Pawn('w', Location('F', 2))
        self._matrix[6][6] = Pawn('w', Location('G', 2))
        self._matrix[6][7] = Pawn('w', Location('H', 2))
        self._matrix[7][0] = Castle('w', Location('A', 1))
        self._matrix[7][7] = Castle('w', Location('H', 1))
        self._matrix[7][1] = Knight('w', Location('B', 1))
        self._matrix[7][6] = Knight('w', Location('G', 1))
        self._matrix[7][2] = Bishop('w', Location('C', 1))
        self._matrix[7][5] = Bishop('w', Location('F', 1))
        self._matrix[7][3] = Queen('w', Location('D', 1))
        self._matrix[7][4] = King('w', Location('E', 1))
        
    def drawBoard(self):
        print('  Ａ Ｂ Ｃ Ｄ Ｅ Ｆ Ｇ Ｈ ')
        print('  － － － － － － － － ')
        row = 9
        for i in self._matrix:
            row = row - 1
            print(row, end = '')
            print('|', end = '')
            for j in i:
                print(j, end = '|')
            print(row, '\n  － － － － － － － － ')
        print('  Ａ Ｂ Ｃ Ｄ Ｅ Ｆ Ｇ Ｈ ')
        
    def putPiece(self, Piece, locationXY):
        self._matrix[x - 1][y - 1] = Piece    
    
    def getSpot(self, location):
        (row, column) = location.getMatrixIndex()
        return self._matrix[row][column]
    
    def setSpot(self, location, newRole): # newRole can be empty or a piece
        (row, column) = location.getMatrixIndex()
        self._matrix[row][column] = newRole
    
    def checkEmpty(self, location): # return true if is empty
        if self.getSpot(location) == '　':
            return True
        else:
            return False
    
    def checkTurn(self, Piece):
        if Piece.getColour() == self.getTurn():
            return True
        else:
            return False
        
    def getTurn(self):
        return self._colourTurn
    
    def changeTrun(self):
        if self._colourTurn == 'w':
            self._colourTurn = 'b'
        else:
            self._colourTurn = 'w'
        
    def squareUpdate(self, currentLocation, newLocation, Piece):
        self.setSpot(currentLocation, '　')
        self.setSpot(newLocation, Piece)
        
    def capture(self, die): # die is the captured piece
        dieColour = die.getColour()
        if dieColour == 'w':
            self._whiteDead.append(die)
        else:
            self._blackDead.append(die)
        if isinstance(die, King):
            self.setWin()
            self.setWinColour(die.getColour())
    
    def setWin(self):
        self._win = True
        
    def getWin(self): # see if anyone has won
        return self._win
    
    def setWinColour(self, c): # remove the LOST colour from the list
        self._winColour.remove(c)
    
    def getWinColour(self):
        return self._winColour
        
class Location: # use A1 - H8
    def __init__(self, alph, num):
        self._alphabet = alph
        self._number = num
        self._x = ord(self._alphabet) - 64 - 1 # A - 64 = 1
        self._y = 8 - num
        
    def getMatrixIndex(self):
        return (self._y, self._x)
    
    def getNotation(self): # A1 - H8
        return (self._alphabet, self._number)
    
    def addX(self, n): # add x by n
        (row, column) = self.getMatrixIndex()
        newX = column + n
        return Location(chr(newX + 65), 8 - row)
    
    def addY(self, n): # add y by n
        (row, column) = self.getMatrixIndex()
        newY = row + n
        return Location(chr(column + 65), 8 - newY)
    
    def add(self, nx, ny):
        (row, column) = self.getMatrixIndex()
        newX = column + nx
        # print('newx, cl, nx:', newX, column, nx)
        newY = row + ny
        # print('newy, r, ny:', newY, row, ny)
        return Location(chr(newX + 65), 8 - newY)
    
def checkInput(squareA, squareN): # check if is between A1 - H8
    alphas = set('ABCDEFGH')
    if set(squareA) <= alphas and squareN <= 8 and squareN >= 1:
        return True
    else:
        return False
    
def instruction():
    print('Select a piece you want to move and the position you want to move it to. Enter the squares using file letter and rank number, and separate them with a space.')
    print('For example, if I want to move the Pawn at A2 to A3, I enter A2 A3.')
    
def colour(pieceColour):
    if pieceColour == 'w':
        return 'White'
    else:
        return 'Black'

def main():
    game = Square()
    game.startGame()
    game.drawBoard()
    while not game.getWin():
        inpt = input('{}, Please select a piece and a square you want to move it to (type H for help, Q if you want to quit): '.format(colour(game.getTurn())))
        inptList = inpt.split()
        if inptList[0] == 'h' or inptList[0] == 'H':
            instruction()
            continue
        elif inptList[0] == 'q' or inptList[0] == 'Q':
            break
        elif len(inptList[0]) != 2 or len(inptList[1]) != 2:
            print('Invalid input! Please select a square from A1 - H8.')
            continue
        elif len(inptList) != 2:
            print('Invalid input! Please input two squares separated by space.')
        else:
            fromSquare = inptList[0]
            toSquare = inptList[1]
            fromSquareA = fromSquare[0].upper()
            toSquareA = toSquare[0].upper()
            try:
                fromSquareN = int(fromSquare[1])
                toSquareN = int(toSquare[1])
            except:
                print('Invalid input! Please input squares from A1 - H8')
                continue
            if checkInput(fromSquareA, fromSquareN) and checkInput(toSquareA, toSquareN): # fromSquareN is int
                fromLocation = Location(fromSquareA, fromSquareN)
                toLocation = Location(toSquareA, toSquareN)
                currentPiece = game.getSpot(fromLocation)
                if isinstance(currentPiece, Piece) and currentPiece.getColour() == game.getTurn(): # make sure the selected spot has the right colour
                    if currentPiece.checkMove(fromLocation, toLocation, game): # if the move is valid
                        currentPiece.move(fromLocation, toLocation, game) # then move
                        game.changeTrun()
                        game.drawBoard()
                    else:
                        print('This move is invalid! Please try again.')
                        continue
                elif isinstance(currentPiece, Piece) and currentPiece.getColour() != game.getTurn(): # select the wrong piece (colour)
                    print('It\'s {}\'s turn. Please select a {} piece.'.format(colour(game.getTurn()), colour(game.getTurn())))
                else:
                    print('It\'s an empty square! Please try again.')
                    continue
            else:
                print('Invalid input! Please select squares from A1 - H8')
                continue
    else:
        wonPlayer = colour(game.getWinColour())
        print('{} won!'.format(wonPlayer))
            
        
        
    
if __name__ == '__main__': main()
    
 
        
    
