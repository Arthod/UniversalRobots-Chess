import chess
import chess.engine
import pygame as pg
import numpy as np

class Main:
    def __init__(self):
        #Chess
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.board = chess.Board()

        self.whose_move = True

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

            #Player to move
            if self.whose_move:
                if pg.mouse.get_pressed()[0]:
                    self.play_move("b" + str(b-1) + "b" + str(b), False)
                    b += 1
                    self.whose_move = False

            #AI to move
            if not self.whose_move:
                result = engine.play(self.board, chess.engine.Limit(time=1))
                self.play_move(result.move, True)
                self.whose_move = True

            pg.display.flip()
            clock.tick(60)
            self.draw(pg)

        
        #Else
        #engine.quit()

    def play_move(self, move, computer):
        if computer:
            self.board.push(move)
        else:
            self.board.push_san(move)
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
        def text(x, y, font, color_rgb, txt):
            text = font.render(txt, False, color_rgb)
            self.screen.blit(text, (x, y))
        rect(0, 0, 800, 600, (255, 255, 255))

        #Draw board
        tile = True
        for ix in range(8):
            tile = self.boolean_flip(tile)
            for iy in range(8):
                if tile:
                    rect(ix * 70, iy * 70, 70, 70, (255, 255, 255))
                else:
                    rect(ix * 70, iy * 70, 70, 70, (0, 0, 0))
                tile = self.boolean_flip(tile)
    
    def boolean_flip(self, boolean):
        if boolean:
            return False
        if not boolean:
            return True

Main()