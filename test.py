import pygame as py
from Direction import Direction
from EdgeCircle import EdgeCircle
from Player import Player
import copy
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

    def move_right(player, edges):
        if Game.canRight(player, edges):
            player[1] = player[1] + 1
                
    def move_left(player, edges):
        if Game.canLeft(player,edges):
            player[1] = player[1] - 1
        
    def move_down(player, edges):
        if Game.canDown(player, edges):
            player[0] = player[0] + 1
                

    def move_up(player, edges):
        if Game.canUp(player, edges):
            player[0] = player[0] - 1
                    

    def canUp(pos, edges):
        if pos[0] > 0:
            if edges[(pos[0]-1, pos[1], Direction.RIGHT)].isFilled == False:
                if pos[1] > 0:
                    if edges[(pos[0]-1, pos[1]-1, Direction.RIGHT)].isFilled == False:
                        return True
                elif pos[1] == 0:
                    return True

    def canDown(pos, edges):
        if pos[0] < 8:
            if edges[(pos[0], pos[1], Direction.RIGHT)].isFilled == False:
                if pos[1] > 0:
                    if edges[(pos[0], pos[1]-1, Direction.RIGHT)].isFilled == False:
                        return True
                elif pos[1] == 0:
                    return True
        return False

    def canLeft(pos, edges):
        # position is list of two integers
        if pos[1] > 0:
            if edges[(pos[0], pos[1]-1, Direction.DOWN)].isFilled == False:
                if pos[0] > 0:
                    if edges[(pos[0]-1, pos[1]-1, Direction.DOWN)].isFilled == False:
                        return True
                elif pos[0] == 0:
                    return True
        return False

    def canRight(pos, edges):
        # position is list of two integers
        if pos[1] < 8:
            if edges[(pos[0], pos[1], Direction.DOWN)].isFilled == False:
                if pos[0] > 0:
                    if edges[(pos[0]-1, pos[1], Direction.DOWN)].isFilled == False:
                        return True
                elif pos[0] == 0:
                    return True
        return False

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

    def getMoves(pos, edges):
        moves = []
        if Game.canLeft(pos, edges):
            moves.append(Game.move_left)
        if Game.canRight(pos, edges):
            moves.append(Game.move_right)
        if Game.canUp(pos, edges):
            moves.append(Game.move_up) 
        if Game.canDown(pos, edges):
            moves.append(Game.move_down)
        return moves

    def get_Edges_moves(edges, wall_count):
        if wall_count < 10:
            temp_edges = []
            # edges to the right side
            i = 0
            while i < 8:
                j = 0
                while j < 8:
                    # j = row and  i = col
                    if edges[(i, j, Direction.RIGHT)].isFilled == False:
                        if edges[(i, j+1, Direction.RIGHT)].isFilled == False:
                            temp_edges.append(edges[(i, j, Direction.RIGHT)])
                    elif edges[(i, j, Direction.RIGHT)].isFilled == True:
                        j = j + 1
                    j = j + 1
                i = i + 1

            # edges of down side
            i = 0
            while i < 8:
                j = 0
                while j < 8:
                    # j = row and  i = col
                    if edges[(j, i, Direction.DOWN)].isFilled == False:
                        if edges[(j+1, i, Direction.DOWN)].isFilled == False:
                            temp_edges.append(edges[(j, i, Direction.DOWN)])
                    elif edges[(j, i, Direction.DOWN)].isFilled == True:
                        j = j + 1
                    j = j + 1
                i = i + 1
            return temp_edges
        else:
            return []

    def value(self, player, opponent, edges):
        if player == Player.player1:
            return Game.getShortestPath(self.p2, opponent, edges) - Game.getShortestPath(self.p1, player, edges)
        else:
            return Game.getShortestPath(self.p1, opponent, edges) - Game.getShortestPath(self.p2, player, edges)

    def getShortestPath(pos, player, edges):
        visited = []
        index = 0
        paths = []
        Game.getPathAtIndex(pos, index, visited, paths, player, edges)
        return min(paths)

    def getPathAtIndex(pos, index, visited, paths, player, edges, memo=[]):
        visited.append((pos[0], pos[1]))
        if (pos, index, visited, paths, player) in memo:
            return 
        memo.append((pos, index, visited, paths, player))
        if Game.isWin(pos, player):
            paths.append(index)
            return
        else:
            if Game.canUp(pos, edges):
                if (pos[0]-1, pos[1]) not in visited:
                    Game.getPathAtIndex([pos[0]-1, pos[1]], index + 1, visited, paths, player,edges, memo)
                    visited.remove((pos[0]-1, pos[1]))
            if Game.canDown(pos, edges):
                if (pos[0]+1, pos[1]) not in visited:
                    Game.getPathAtIndex([pos[0]+1, pos[1]], index + 1, visited, paths, player, edges, memo)
                    visited.remove((pos[0]+1, pos[1]))
            if Game.canRight(pos, edges):
                if (pos[0], pos[1]+1) not in visited:
                    Game.getPathAtIndex([pos[0], pos[1]+1], index + 1, visited, paths, player, edges, memo)
                    visited.remove((pos[0], pos[1]+1))
            if Game.canLeft(pos, edges):
                if (pos[0], pos[1]-1) not in visited:
                    Game.getPathAtIndex([pos[0], pos[1]-1], index + 1, visited, paths, player, edges, memo)
                    visited.remove((pos[0], pos[1]-1))

    def getBestMoveForP2(self,depth):
        edges = copy.deepcopy(self.edges)
        moves = Game.generarteMoves(self.p2, edges, 0)
        maxi = -float("inf")
        bestMove = None
        for move in moves:
            temp_p2 = [self.p2[0], self.p2[1]]
            temp_p1= [self.p1[0], self.p1[1]]
            Game.use_move_from_moves(move, temp_p2, edges)
            if move.isWall == True:
                # giving self.p1 because it is not maximizing player
                value = self.maximini(temp_p1, temp_p2, edges, depth, False, 1)
                Game.breakWall(move.move)
            else:
                value = self.maximini(temp_p1, temp_p2, edges, depth, False, 0)
            if value > maxi:
                maxi = value
                bestMove = move
        return move

    def maximini(self, p1_pos, p2_pos, edges, depth, maximizingPlayer, wall_count, memo={}):
        if ((p1_pos[0], p1_pos[1]), (p2_pos[0], p2_pos[1]), maximizingPlayer) in memo.keys():
            return memo[((p1_pos[0], p1_pos[1]), (p2_pos[0], p2_pos[1]), maximizingPlayer)]

        if maximizingPlayer == True:
            if depth == 0 or Game.isWin(p2_pos, Player.player2):
                return self.value(Player.player2, Player.player1, edges)
            maxValue = -float('inf')
            # Generate a list of all possible moves
            moves = Game.generarteMoves(p2_pos, edges, wall_count)
    
            # For each possible move, find the minimax value recursively
            for move in moves:
                temp = [p2_pos[0], p2_pos[1]]
                Game.use_move_from_moves(move, temp, edges)
                if move.isWall == True:
                    value = self.maximini(p1_pos, temp, edges, depth-1, False, wall_count+1, memo)
                    Game.breakWall(move.move)
                else:
                    value = self.maximini(p1_pos, temp, edges, depth-1, False, wall_count, memo)
                maxValue = max(maxValue, value)
            memo[((p1_pos[0], p1_pos[1]), (p2_pos[0], p2_pos[1]),  maximizingPlayer)] = maxValue
        else:
            if depth == 0 or Game.isWin(p1_pos, Player.player1):
                return self.value(Player.player1, Player.player2, edges)

            minValue = float('inf')

            # Generate a list of all possible moves
            moves = Game.generarteMoves(p1_pos, edges, wall_count)
    
            # For each possible move, find the minimax value recursively
            for move in moves:
                temp = [p1_pos[0], p1_pos[1]]
                Game.use_move_from_moves(move, temp, edges)
                if move.isWall == True:
                    value = self.maximini(temp, p2_pos, edges, depth-1, True, wall_count+1, memo)
                    Game.breakWall(move.move)
                else:
                    value = self.maximini(temp, p2_pos, edges, depth-1, True,wall_count, memo)
                minValue = min(minValue, value)
            memo[((p1_pos[0], p1_pos[1]), (p2_pos[0], p2_pos[1]), maximizingPlayer)] = minValue

    def generarteMoves(pos, edges, wall_count):
        all_moves = []
        temp = Game.getMoves(pos, edges)
        for move in temp:
            # using false as it is not a wall
            all_moves.append(Move(move, False))

        temp = Game.get_Edges_moves(edges, wall_count)
        for wall in temp:
            all_moves.append(Move(wall, True))

        return all_moves
    
    def use_move_from_moves(move, pos, edges):
        if move.isWall == False:
            Game.makeMove(move.move, pos, edges)
        else:
            Game.makeWall(move)

    def makeMove(fun, pos, edges):
        fun(pos, edges)

    def makeWall(edge):
        edge.isFilled = True

    def breakWall(edge):
        edge.isFilled = False

g = Game()
Game.move_up(g.p1, g.edges)
Game.move_right(g.p1, g.edges)
# print(g.value(Player.player2, Player.player1, g.edges))
print(g.getBestMoveForP2(1))
