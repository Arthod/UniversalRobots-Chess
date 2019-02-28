import chess
import chess.engine
import pygame as pg
import numpy as np

class Main:
    def __init__(self):
        #Chess
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.board = chess.Board()

        whose_move = True

        #Pygame
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.font = pg.font.SysFont("monospace", 15)
        clock = pg.time.Clock()
        pg.font.init()

        b = 3

        done = False

        while not done:
            #Init
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            pressed = pg.key.get_pressed()

            #Player
            if pg.mouse.get_pressed()[0] and whose_move == True:
                self.play_move("b" + str(b-1) + "b" + str(b), False)
                print("playing b2b" + str(b))
                b += 1
                whose_move = False

            #Chess AI
            if whose_move == False:
                result = engine.play(self.board, chess.engine.Limit(time=1))
                self.play_move(result.move, True)
                whose_move = True

            pg.display.flip()
            clock.tick(60)

        
        #Else
        #engine.quit()

    def play_move(self, move, computer):
        if computer:
            self.board.push(move)
        else:
            self.board.push_san(move)
        print(self.board.unicode())
        print("---------------")

Main()