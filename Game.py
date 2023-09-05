import pygame as py
from Direction import Direction
from EdgeCircle import EdgeCircle
from Player import Player
import copy
import time
from Move import Move

class Game:
    def __init__(self):
        self.screen = py.display.set_mode((600,600))
        self.color = "white"
        self.background = "black"
        self.bigSquareLength = 40
        self.edge_circle_length = 10
        self.twoBoxLength = 106
        self.board = [["" for j in range(9)] for i in range(9)]
        self.p1_color = "blue"
        self.p2_color = "red"
        self.p1_edge = 0
        self.p2_edge = 0
        self.p1 = [8, 4]
        self.p2 = [0, 4]
        self.edges = self.get_edges()
        
    def draw_board(self):
        self.screen.fill(self.background)
        k = 13
        for i in range(9):
            l = 13
            for j in range(9):
                self.draw_square(k, l, self.bigSquareLength)
                if i == self.p1[0] and j == self.p1[1]:
                    self.draw_circle(l+20, k+20, 10, self.p1_color)
                if i == self.p2[0] and j == self.p2[1]:
                    self.draw_circle(l+20, k+20, 10, self.p2_color)
                l += 66
            k += 66

        # drawing edges to the right side
        l = 66
        i = 0
        while i < 8:
            k = 33
            j = 0
            while j < 8:
                # j = row and  i = col
                if self.edges[(i, j, Direction.RIGHT)].isFilled == False:
                    circle = self.draw_circle(k, l, self.edge_circle_length, self.color)
                    self.edges[(i, j, Direction.RIGHT)].circle = circle
                elif self.edges[(i, j, Direction.RIGHT)].isFilled == True:
                    self.draw_filled_rect(k-20, l-13, self.twoBoxLength, 20)
                    k += 66
                    j = j + 1
                k += 66
                j = j + 1
            l += 66
            i = i + 1

        # showing edges of down side
        k = 33
        i = 0
        while i < 8:
            l = 66
            j = 0
            while j < 8:
                # j = row and  i = col
                if self.edges[(j, i, Direction.DOWN)].isFilled == False:
                    circle = self.draw_circle(k+33, l-33, self.edge_circle_length, self.color)
                    self.edges[(j, i, Direction.DOWN)].circle = circle
                elif self.edges[(j, i, Direction.DOWN)].isFilled == True:
                    self.draw_filled_rect(k+23, l-53, 20,  self.twoBoxLength)
                    l += 66
                    j = j + 1
                l += 66
                j = j + 1
            k += 66
            i = i + 1

        py.display.flip()
        py.time.delay(10)
        if Game.isWin(self.p1, Player.player1):
            print("Player 1 has won")
            exit()
        elif Game.isWin(self.p2, Player.player2):
            print("Player 2 has won")
            exit()

    def get_edges(self):
        edges = {}
        for i in range(9):
            for j in range(9):
                # i = row, j = col
                temp = EdgeCircle(i, j,Direction.RIGHT)
                edges[(i, j, Direction.RIGHT)] = temp
                temp = EdgeCircle(i,j,Direction.DOWN)
                edges[(i, j, Direction.DOWN)] = temp
        return edges

    def draw_square(self, x, y, length):
        py.draw.line(self.screen, self.color, (x, y), (x+length, y))
        py.draw.line(self.screen, self.color, (x, y), (x, y+length))
        py.draw.line(self.screen, self.color, (x+length, y), (x+length, y+length))
        py.draw.line(self.screen, self.color, (x, y+length), (x+length, y+length))

    def draw_filled_square(self, x, y, length):
        py.draw.rect(self.screen, self.color, (x, y, length, length))

    def draw_filled_rect(self, x, y, height, width):
        py.draw.rect(self.screen, self.color, (x, y, height, width))

    def draw_circle(self, x, y, radius, color):
        return py.draw.circle(self.screen, color, (x, y), radius)

    def move_right(self, player):
        player[1] = player[1] + 1

                
    def move_left(self,player):
        player[1] = player[1] - 1

        
    def move_down(self, player):
        player[0] = player[0] + 1
                

    def move_up(self, player):
        player[0] = player[0] - 1
                    

    def canUp(pos, edges):
        if pos[0] > 0 and pos[0] < 9:
            # if
            if edges[(pos[0]-1, pos[1], Direction.RIGHT)].isFilled == False:
                if pos[1] > 0:
                    if edges[(pos[0]-1, pos[1]-1, Direction.RIGHT)].isFilled == False:
                        return True
                elif pos[1] == 0:
                    return True
        return False

    def canDown(pos, edges):
        if pos[0] < 8 and pos[0] >= 0:
            if edges[(pos[0], pos[1], Direction.RIGHT)].isFilled == False:
                if pos[1] > 0:
                    if edges[(pos[0], pos[1]-1, Direction.RIGHT)].isFilled == False:
                        return True
                elif pos[1] == 0:
                    return True
        return False

    def canLeft(pos, edges):
        # position is list of two integers
        if pos[1] > 0 and pos[0] < 9 and pos[0] >= 0:
            if edges[(pos[0], pos[1]-1, Direction.DOWN)].isFilled == False:
                if pos[0] > 0:
                    if edges[(pos[0]-1, pos[1]-1, Direction.DOWN)].isFilled == False:
                        return True
                elif pos[0] == 0:
                    return True
        return False

    def canRight(pos, edges):
        # position is list of two integers
        if pos[1] < 8 and pos[0] < 9 and pos[0] >= 0:
            if edges[(pos[0], pos[1], Direction.DOWN)].isFilled == False:
                if pos[0] > 0:
                    if edges[(pos[0]-1, pos[1], Direction.DOWN)].isFilled == False:
                        return True
                elif pos[0] == 0:
                    return True
        return False

    def can_go_over_right(player, opponent,edges):
        if player[0] == opponent[0] and player[1] + 1 == opponent[1]:
            if Game.canRight([player[0], player[1] + 1], edges):
                return True
        return False

    def can_go_over_left(player, opponent, edges):
        if player[0] == opponent[0] and player[1] -1 == opponent[1]:
            if Game.canLeft([player[0], player[1] -1], edges):
                return True
        return False

    def can_go_over_up(player, opponent, edges):
        if player[0] == opponent[0] + 1 and player[1]== opponent[1]:
            if Game.canUp([player[0] + 1, player[1]], edges):
                return True
        return False
        
    def can_go_over_down(player, opponent, edges):
        if player[0] == opponent[0] - 1 and player[1] == opponent[1]:
            if Game.canDown([player[0] - 1, player[1]], edges):
                return True
        return False

    def go_over_right(self, pos):
        pos[1] += 2

    def go_over_left(self, pos):
        pos[1] -= 2

    def go_over_up(self, pos):
        pos[0] -= 2

    def go_over_down(self, pos):
        pos[0] += 2

    def isWin(pos, player):
        if player == Player.player1:
            if pos[0] == 0:
                return True
            else:
                return False
        elif player == Player.player2:
            if pos[0] == 8:
                return True
            else:
                return False

    def generateMoves(pos, opponent, edges):
        moves = []
        if Game.can_go_over_down(pos, opponent, edges):
            moves.append(Game.go_over_down)
        elif Game.canDown(pos, edges):
            moves.append(Game.move_down)
        if Game.can_go_over_left(pos, opponent, edges):
            moves.append(Game.go_over_left)
        elif Game.canLeft(pos, edges):
            moves.append(Game.move_left)
        if Game.can_go_over_right(pos, opponent, edges):
            moves.append(Game.go_over_right)
        elif Game.canRight(pos, edges):
            moves.append(Game.move_right)
        if Game.can_go_over_up(pos, opponent, edges):
            moves.append(Game.go_over_up)
        elif Game.canUp(pos, edges):
            moves.append(Game.move_up)
        return moves

    def value(self, p1_pos, p2_pos):
        diff = p2_pos[0]
        return diff * 10
        

    def getBestMoveForP2(self,depth):
        moves = Game.generateMoves(self.p2, self.p1, self.edges)
        maxi = -float("inf")
        bestMove = None
        temp_p1= [self.p1[0], self.p1[1]]
        for move in moves:
            temp_p2 = [self.p2[0], self.p2[1]]
            Game.makeMove(self, move, temp_p2)
            # giving self.p1 because it is not maximizing player
            value = self.maximini(temp_p1, temp_p2, self.edges, depth, False, {})
            if value > maxi:
                maxi = value
                bestMove = move
        return bestMove

    def maximini(self, p1_pos, p2_pos, edges, depth, maximizingPlayer, memo):
        if (p1_pos[0], p1_pos[1], p2_pos[0], p2_pos[1], maximizingPlayer) in memo.keys():
            return memo[(p1_pos[0], p1_pos[1], p2_pos[0], p2_pos[1], maximizingPlayer)]

        if maximizingPlayer == True:
            if depth == 0 or Game.isWin(p2_pos, Player.player2):
                return self.value(p1_pos, p2_pos)
            maxValue = -float('inf')
            # Generate a list of all possible moves
            moves = Game.generateMoves(p2_pos, p1_pos, edges)
    
            # For each possible move, find the minimax value recursively
            for move in moves:
                temp = [p2_pos[0], p2_pos[1]]
                Game.makeMove(self, move, temp) 
                value = self.maximini(p1_pos, temp, edges, depth-1, False, memo)
                maxValue = max(maxValue, value)

            memo[(p1_pos[0], p1_pos[1], p2_pos[0], p2_pos[1], maximizingPlayer)] = maxValue
            return maxValue
        else:
            if depth == 0 or Game.isWin(p1_pos, Player.player1):
                return self.value(p1_pos,p2_pos)

            minValue = float('inf')

            # Generate a list of all possible moves
            moves = Game.generateMoves(p1_pos, p2_pos, edges)

            # For each possible move, find the minimax value recursively
            for move in moves:
                temp = [p1_pos[0], p1_pos[1]]
                Game.makeMove(self, move, temp) 
                value = self.maximini(temp, p2_pos, edges, depth-1, True, memo)
                minValue = min(minValue, value)

            memo[(p1_pos[0], p1_pos[1], p2_pos[0], p2_pos[1], maximizingPlayer)] = minValue
            return minValue

    def makeMove(self, fun, pos):
        fun(self, pos)

# g = Game()
# g.p1 = [5,6]
# g.p2 = [4,6]
# # g.edges[(5, 6, Direction.RIGHT)].isFilled = True
# # g.draw_board()
# # time.sleep(2000)
# print(g.getBestMoveForP2(6))
