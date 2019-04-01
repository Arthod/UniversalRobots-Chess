import chess
import chess.engine
import pygame as pg
import numpy as np
import asyncio
from RTData import RTData
from robotprogrammer import Robot_programmer
import time


class Main:
    def __init__(self):
        #Chess
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.board = chess.Board()

        self.whose_move = True #hvis tur det er. Hvis den er initialiseret som False, er hvid AI. Ellers er sort AI.

        #Robotprogrammer
        self.robotprogrammer = Robot_programmer()
        self.robotprogrammer.connect("10.130.58.11")
        
        self.robot = RTData()
        self.robot.connect("10.130.58.11", False)

        #Chess board real life position
        self.board_x = -200
        self.delta = 46 * 8

        #Misc
        self.from_move = ""
        self.from_move_coordinates = (0, 0)
        self.to_move = ""
        self.columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.rows = ["8", "7", "6", "5", "4", "3", "2", "1"]

        ready = True
        timer_buttons = 0

        #Pygame
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.unicode = pg.font.Font("segoe-ui-symbol.ttf", 40)
        self.font = pg.font.SysFont("monospace", 15)
        clock = pg.time.Clock()
        pg.font.init()

        done = False

        while not done:
            self.draw(pg)
            #Init
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            pressed = pg.key.get_pressed()

            timer_buttons += 1
            if timer_buttons > 60:
                ready = True
                timer_buttons = 0

            #Buttons
            self.mouse = pg.mouse.get_pos()
            if pg.mouse.get_pressed()[0] and ready == True:
                if self.mouse[0] > 560+40 and self.mouse[0] < 560+40+100:
                    if self.mouse[1] > 0 and self.mouse[1] < 50:
                        self.robotprogrammer.move_home()
                        print("Button home")
                    if self.mouse[1] > 100 and self.mouse[1] < 150:
                        self.robotprogrammer.open_gripper()
                        print("Button open gripper")
                    if self.mouse[1] > 200 and self.mouse[1] < 250:
                        self.robotprogrammer.close_gripper()
                        print("Button close gripper")
                    ready = False
                    timer_buttons = 0

            #AI to move
            if not self.whose_move or self.whose_move: #Any atm.
                try:
                    result = engine.play(self.board, chess.engine.Limit(time=5))
                except:
                    print("ERROR: Engine crashed")
                else:
                    self.play_move(result.move, True)
                    self.whose_move = True


            #Player to move
            if self.whose_move:# or True:
                x = int(pg.mouse.get_pos()[0] / 70)
                y = int(pg.mouse.get_pos()[1] / 70)
                if x < 8 and y < 8:
                    move = self.columns[x] + self.rows[y]
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

    def play_move(self, move, computer):
        def move_to_coordinates(the_move):
            from_coordinate = (char_to_int(the_move[0]), int(the_move[1]))
            to_coordinate = (char_to_int(the_move[2]), int(the_move[3]))
            return (from_coordinate, to_coordinate)

        def char_to_int(char):
            for i in range(len(self.columns)):
                if self.columns[i] == char:
                    return i+1

        def map_value(value, start1, stop1, start2, stop2):
            leftSpan = stop1 - start1
            rightSpan = stop2 - start1

            valueScaled = float(value - start1) / float(leftSpan)

            return start2 + (valueScaled * rightSpan)
        def remove_instance(k, arr):
            for i in arr:
                if(i == k):
                    arr.remove(i)
            return arr
        def map_to_board(value):
            return map_value(value, 0, 8, 0, self.delta) + self.board_x - self.delta

        #Check if piece is captured
        where_to = move_to_coordinates(str(move))[1]
        where_from = move_to_coordinates(str(move))[0]

        print(where_from, where_to)
        board_array = self.board.unicode_array()
        board_array = remove_instance(" ", board_array)
        board_array = remove_instance("\n", board_array)
        print(str(board_array[((where_from[0]-1) + (8-where_from[1])*8)]) + "-->" + str(board_array[((where_to[0]-1) + (8-where_to[1])*8)]))
        captured_piece = board_array[((where_to[0]-1) + (8-where_to[1])*8)]
        time.sleep(0.01)

        if not(captured_piece in ["·", '\n', ' ']):
            have_captured = True
        else:
            have_captured = False

        #Castling
        castled = True
        if str(move) == "e1g1":
            new_rook_position = "h1f1"
        elif str(move) == "e1c1":
            new_rook_position = "a1d1"

        elif str(move) == "e8g8":
            new_rook_position = "h8f8"
        elif str(move) == "e8c8":
            new_rook_position = "a8d8"
        else:
            castled = False

        if computer:
            self.board.push(move)
        else:
            self.board.push(chess.Move.from_uci(move))
        print(str(self.return_color(self.whose_move)) + " playing " + str(move))
        print(str(self.board.unicode()) + "\n ---------------")

        #Coords To
        coords_to = move_to_coordinates(str(move))[1]
        move_to_x = map_to_board(coords_to[0])
        move_to_y = map_to_board(coords_to[1])

        #Coords from
        coords_from = move_to_coordinates(str(move))[0]
        move_from_x = map_to_board(coords_from[0])
        move_from_y = map_to_board(coords_from[1])
        
        if have_captured: #If captured piece
            self.robotprogrammer.capture_piece(move_from_x/1000.0, move_from_y/1000.0, move_to_x/1000.0, move_to_y/1000.0)
        elif castled: #If castled
            self.robotprogrammer.move_piece(move_from_x/1000.0, move_from_y/1000.0, move_to_x/1000.0, move_to_y/1000.0) #Move king to square
            
            #Move rook to square
            rook_from = move_to_coordinates(new_rook_position)[0]
            rook_from_x = map_to_board(rook_from[0])
            rook_from_y = map_to_board(rook_from[1])

            rook_to = move_to_coordinates(new_rook_position)[1]
            rook_to_x = map_to_board(rook_to[0])
            rook_to_y = map_to_board(rook_to[1])
            self.robotprogrammer.move_piece(rook_from_x/1000.0, rook_from_y/1000.0, rook_to_x/1000.0, rook_to_y/1000.0)
            
        else:
            self.robotprogrammer.move_piece(move_from_x/1000.0, move_from_y/1000.0, move_to_x/1000.0, move_to_y/1000.0)

        #x = -588 .. -200		Delta = -388
        #y = -588 .. -200		Delta = -388

        #x = -588 .. -200		Delta = -388
        #y = -553 .. -166		Delta = -387
        

    def return_color(self, side):
        if side:
            return "white"
        if not side:
            return "black"

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

        #Draw side GUI
        #Home
        rect(560+40, 0, 100, 50, (200, 160, 160))
        text(560+40, 0, self.font, "Home")
        
        #Open gripper
        rect(560+40, 100, 100, 50, (200, 160, 160))
        text(560+40, 100, self.font, "Open Gripper")

        #Close gripper
        rect(560+40, 200, 100, 50, (200, 160, 160))
        text(560+40, 200, self.font, "Close Gripper")



    def boolean_flip(self, boolean):
        if boolean:
            return False
        if not boolean:
            return True

Main()