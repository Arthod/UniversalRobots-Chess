import chess
import chess.engine
import pygame as pg
from RTData import RTData
from robotprogrammer import Robot_programmer
import time


class Main:
    def __init__(self):
        #Chess
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.board = chess.Board()
        self.status = ["", "", ""]
        self.move_number = 0

        self.whose_move = True #hvis tur det er. Hvis den er initialiseret som False, er hvid AI. Ellers er sort AI.

        #Robotprogrammer
        self.robotprogrammer = Robot_programmer()
        self.robotprogrammer.connect("10.130.58.11", False) #ip, simulation
        
        #self.robot = RTData()
        #self.robot.connect("10.130.58.11", True)

        #Chess board real life position
        self.board_x = -200
        self.delta = 46 * 8

        #Misc
        self.from_move = ""
        self.from_move_coordinates = (0, 0)
        self.to_move = ""
        self.columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.rows = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.last_move = ""
        self.current_move = ""

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
            if True: #not self.whose_move or self.whose_move: #Any atm.
                try:
                    self.draw(pg)
                    result = engine.play(self.board, chess.engine.Limit(time=0.1)) #time=5
                except:
                    print("Engine crash")
                else:
                    self.status[0] = str(self.return_color(self.whose_move)) + " playing " + str(result.move)

                    self.draw(pg)
                    self.play_move(result.move, True)

                    self.draw(pg)
                    self.whose_move = self.flip_bool(self.whose_move)


            #Player to move
            if False: #self.whose_move:
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
                            self.status[0] = str(self.return_color(self.whose_move)) + " playing " + str(self.from_move) + str(self.to_move)
                            self.draw(pg)
                            self.whose_move = self.flip_bool(self.whose_move)
                        self.from_move = ""
                        self.from_move_coordinates = ""
                        self.to_move = ""

            pg.display.flip()
            clock.tick(60)


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
            tile = self.flip_bool(tile)
            for iy in range(8):
                if (ix, iy) == self.from_move_coordinates:
                    rect(ix * 70, iy * 70, 70, 70, (160, 0, 0))
                else:
                    if tile:
                        rect(ix * 70, iy * 70, 70, 70, (160, 160, 160))
                    else:
                        rect(ix * 70, iy * 70, 70, 70, (255, 255, 255))
                tile = self.flip_bool(tile)
                if self.board.unicode_array()[(ix+iy*8) * 2] != "·":
                    text(ix * 70+15, iy * 70+15, self.unicode, self.board.unicode_array()[(ix+iy*8) * 2])

        #Draw side GUI
        #Home
        rect(560+40, 0, 150, 50, (200, 160, 160))
        text(560+50, 15, self.font, "Home")
        
        #Open gripper
        rect(560+40, 100, 150, 50, (200, 160, 160))
        text(560+50, 115, self.font, "Open Gripper")

        #Close gripper
        rect(560+40, 200, 150, 50, (200, 160, 160))
        text(560+50, 215, self.font, "Close Gripper")

        y_right = 300
        text(560+50, y_right, self.font, "Move " + str(self.move_number) + ":")
        text(560+20, y_right+20, self.font, self.status[0])

        text(560+50, y_right+60, self.font, "Last move:")
        text(560+20, y_right+60+20, self.font, self.status[1])

        text(560+50, y_right+120, self.font, "..:")
        text(560+20, y_right+120+20, self.font, self.status[2])

    def play_move(self, move, computer):

        self.move_number += 1
        #Check if piece is captured
        where_to = self.move_to_coordinates(str(move))[1]
        where_from = self.move_to_coordinates(str(move))[0]

        print(where_from, where_to)
        board_array = self.board.unicode_array()
        board_array = self.remove_instance(" ", board_array)
        board_array = self.remove_instance("\n", board_array)
        print(str(board_array[((where_from[0]-1) + (8-where_from[1])*8)]) + " --> " + str(board_array[((where_to[0]-1) + (8-where_to[1])*8)]))
        captured_piece = board_array[((where_to[0]-1) + (8-where_to[1])*8)]
        time.sleep(0.01)

        if not(captured_piece in ['·', '\n', ' ']):
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
        coords_to = self.move_to_coordinates(str(move))[1]
        move_to_x = self.map_to_board(coords_to[0])/1000.0
        move_to_y = self.map_to_board(coords_to[1])/1000.0

        #Coords from
        coords_from = self.move_to_coordinates(str(move))[0]
        move_from_x = self.map_to_board(coords_from[0])/1000.0
        move_from_y = self.map_to_board(coords_from[1])/1000.0

        if have_captured: #If captured piece
            self.robotprogrammer.capture_piece(move_from_x, move_from_y, move_to_x, move_to_y)
        elif castled: #If castled
            self.robotprogrammer.move_piece(move_from_x, move_from_y, move_to_x, move_to_y) #Move king to square
            
            #Move rook to square
            rook_from = self.move_to_coordinates(new_rook_position)[0]
            rook_from_x = self.map_to_board(rook_from[0])/1000.0
            rook_from_y = self.map_to_board(rook_from[1])/1000.0

            rook_to = self.move_to_coordinates(new_rook_position)[1]
            rook_to_x = self.map_to_board(rook_to[0])/1000.0
            rook_to_y = self.map_to_board(rook_to[1])/1000.0
            self.robotprogrammer.move_piece(rook_from_x, rook_from_y, rook_to_x, rook_to_y)
            
        else: #Simply move piece
            self.robotprogrammer.move_piece(move_from_x, move_from_y, move_to_x, move_to_y)

    def move_to_coordinates(self, move):
        from_coordinate = (self.char_to_int(move[0]), int(move[1]))
        to_coordinate = (self.char_to_int(move[2]), int(move[3]))
        return (from_coordinate, to_coordinate)

    def char_to_int(self, char):
        for i in range(len(self.columns)):
            if self.columns[i] == char:
                return i+1

    def map_value(self, value, start1, stop1, start2, stop2):
        leftSpan = stop1 - start1
        rightSpan = stop2 - start1

        valueScaled = float(value - start1) / float(leftSpan)

        return start2 + (valueScaled * rightSpan)

    def remove_instance(self, k, arr):
        for i in arr:
            if(i == k):
                arr.remove(i)
        return arr

    def map_to_board(self, value):
        return self.map_value(value, 0, 8, 0, self.delta) + self.board_x - self.delta

    def return_color(self, side):
        if side:
            return "white"
        if not side:
            return "black"


    def flip_bool(self, boolean):
        if boolean:
            return False
        if not boolean:
            return True

Main()