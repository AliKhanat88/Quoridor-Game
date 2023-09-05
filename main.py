from Game import Game
import pygame as py
from Direction import Direction
from Player import Player

DEPTH = 50
def main():
    py.init()
    game = Game()
    game.draw_board()
    while True:
        events = py.event.get()
        mouse_pos = py.mouse.get_pos()
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_LEFT:
                    if Game.can_go_over_left(game.p1, game.p2, game.edges):
                        game.go_over_left(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()
                    elif Game.canLeft(game.p1,game.edges):
                        game.move_left(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()

                elif event.key == py.K_RIGHT:
                    if Game.can_go_over_right(game.p1, game.p2, game.edges):
                        game.go_over_right(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()
                    elif Game.canRight(game.p1,game.edges):
                        game.move_right(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()

                elif event.key == py.K_UP:
                    if Game.can_go_over_up(game.p1, game.p2, game.edges):
                        game.go_over_up(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()
                    elif Game.canUp(game.p1,game.edges):
                        game.move_up(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()
                elif event.key == py.K_DOWN:
                    if Game.can_go_over_down(game.p1, game.p2 ,game.edges):
                        game.go_over_down(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()
                    elif Game.canDown(game.p1,game.edges):
                        game.move_down(game.p1)
                        game.draw_board()
                        move = game.getBestMoveForP2(DEPTH)
                        game.makeMove(move, game.p2)
                        game.draw_board()
                    
            elif event.type == py.MOUSEBUTTONDOWN:
                for edge in game.edges.values():
                    if edge.row != 8 and edge.col != 8:
                        if edge.isFilled == False and edge.circle.collidepoint(mouse_pos):
                            if edge.direction == Direction.RIGHT:
                                if game.edges[(edge.row, edge.col+1, edge.direction)].isFilled == False:
                                    if game.p1_edge < 10:
                                        edge.isFilled = True
                                        game.draw_board()
                                        move = game.getBestMoveForP2(DEPTH)
                                        game.makeMove(move, game.p2)
                                        game.p1_edge += 1
                                        game.draw_board()
                            elif edge.direction == Direction.DOWN:
                                if game.edges[(edge.row+1, edge.col, edge.direction)].isFilled == False:
                                    if game.p1_edge < 10:
                                        edge.isFilled = True
                                        game.draw_board()
                                        move = game.getBestMoveForP2(DEPTH)
                                        game.makeMove(move, game.p2)
                                        game.p1_edge += 1
                                        game.draw_board()
            elif event.type == py.QUIT:
                exit()

main()

