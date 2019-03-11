import chess
import chess.engine
import pygame as pg
import numpy as np
import sys

class Main:
    def __init__(self):
        #Chess
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.board = chess.Board()

        self.whose_move = True #hvis tur det er. Hvis den er initialiseret som False, er hvid AI. Ellers er sort AI.

        #Pygame
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.unicode = pg.font.Font("segoe-ui-symbol.ttf", 40)
        self.font = pg.font.SysFont("monospace", 15)
        clock = pg.time.Clock()
        pg.font.init()

        done = False
        print (self.board.unicode_array()[1])

        self.from_move = ""
        self.from_move_coordinates = (0, 0)
        self.to_move = ""
        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        rows = ["8", "7", "6", "5", "4", "3", "2", "1"]

        while not done:
            #Init
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    engine.quit()
            pressed = pg.key.get_pressed()


            #AI to move
            if not self.whose_move:
                result = engine.play(self.board, chess.engine.Limit(time=0.01))
                self.play_move(result.move, True)
                self.whose_move = True

            #Player to move
            if self.whose_move:
                x = int(pg.mouse.get_pos()[0] / 70)
                y = int(pg.mouse.get_pos()[1] / 70)
                if x < 8 and y < 8:
                    move = columns[x] + rows[y]
                    if pg.mouse.get_pressed()[0]:
                        self.from_move = move
                        self.from_move_coordinates = (x, y)
                    if pg.mouse.get_pressed()[2] and len(self.from_move) == 2:
                        self.to_move = move
                        try:
                            self.play_move(self.from_move + self.to_move, False)
                        except:
                            pass
                        else:
                            self.whose_move = False
                        self.from_move = ""
                        self.from_move_coordinates = ""
                        self.to_move = ""

            pg.display.flip()
            clock.tick(60)
            self.draw(pg)

    def play_move(self, move, computer):
        if computer:
            self.board.push(move)
        else:
            self.board.push(chess.Move.from_uci(move))
        print(str(self.return_color(self.whose_move)) + " playing " + str(move))
        print(self.board.unicode())
        print("---------------")

    def return_color(self, side):
        if side:
            return "black"
        if not side:
            return "white"

    def draw(self, pygame):
        def rect(x, y, w, h, color_rgb):
            pygame.draw.rect(self.screen, color_rgb, pygame.Rect(x, y, w, h))
        def text(x, y, font, txt, color_rgb=(0, 0, 0)):
            text = font.render(txt, False, color_rgb)
            self.screen.blit(text, (x, y))
        rect(0, 0, 800, 600, (255, 255, 255))

        #Draw board
        tile = True
        for ix in range(8):
            tile = self.boolean_flip(tile)
            for iy in range(8):
                if (ix, iy) == self.from_move_coordinates:
                    rect(ix * 70, iy * 70, 70, 70, (160, 0, 0))
                else:
                    if tile:
                        rect(ix * 70, iy * 70, 70, 70, (160, 160, 160))
                    else:
                        rect(ix * 70, iy * 70, 70, 70, (255, 255, 255))
                tile = self.boolean_flip(tile)
                text(ix * 70+15, iy * 70+15, self.unicode, self.board.unicode_array()[(ix+iy*8) * 2])

    def boolean_flip(self, boolean):
        if boolean:
            return False
        if not boolean:
            return True

Main()