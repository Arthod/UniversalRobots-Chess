import socket 
import time

class Robot_programmer():

    def __init__(self):
        #Socket til at sende kommandoer til robotten
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)
        self.connected = False
        
        self.top_z = 150.8/1000.0
        self.bottom_take_z = 72/1000.0
        self.bottom_release_z = 72/1000.0
        self.drop_place_y = -80/1000.0

    def connect(self, ip='10.130.58.11'):
        self.TCP_IP = ip
        TCP_PORT = 30002
        BUFFER_SIZE = 1024

        try:
            #print("Opening IP Address" + TCP_IP)
            self.s.connect((self.TCP_IP, TCP_PORT))
            self.connected = True
        except socket.error:
            print("Socket error")
            self.s.close()

    def move_home(self):
        if self.connected:
            #Prædefineret home-position:
            #(Når vi skal sende en streng til robotten,
            # skal den konverteres til et bytearrayself.
            # derfor står der b' foran strengen.)
            self.s.send(b'  movej([0,-1.5708, 1.5708, -1.5708, -1.5708, 0])\n')

    def move_xyz(self, x, y, z):
        if self.connected:
            self.s.send(b'def move_xyz():\n')
            self.send_socket_move_xyz(x, y, z)

            self.s.send(b'end\n')
            
    def move_positions(self, pos, z):
        if self.connected:
            self.s.send(b'def myProg():\n')
            
            self.s.send(b'  var_1=get_actual_tcp_pose()\n')
            st = '  var_1[2] = {}\n'.format(z/1000.0)
            self.s.send(bytearray(st,'utf8'))
            
            for i in range(len(pos)):
                x = pos[i][0]-487.0
                y = pos[i][1]-107.0
                
                #81.8
                
                #x = -487.0
                #y = -107.0
            
                self.s.send(b'  var_1=get_actual_tcp_pose()\n')
                st = '  var_1[0] = {}\n'.format(x/1000.0)
                self.s.send(bytearray(st,'utf8'))
                st = '  var_1[1] = {}\n'.format(y/1000.0)
                self.s.send(bytearray(st,'utf8'))
                st = '  var_1[2] = {}\n'.format(z/1000.0)
                self.s.send(bytearray(st,'utf8'))
                self.s.send(b'  movel(var_1, r = 0.002)\n')
                self.s.send(bytearray(st,'utf8'))
            self.s.send(b'  movej([0,-1.5708, 1.5708, -1.5708, -1.5708, 0])\n')
            self.s.send(b'end\n')
            
    def open_gripper(self):
        TCP_PORT = 29999
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
        	#print("Opening IP Address" + self.TCP_IP)
        	s.connect((self.TCP_IP, TCP_PORT))
        except socket.error:
        	print("Socket error")
        	s.close()
        
        s.send(b"load /programs/opengrip.urp\n")
        time.sleep(1)
        s.send(b"play\n")
        time.sleep(1.5)

        s.close()

    def close_gripper(self):
        TCP_PORT = 29999
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
        	s.connect((self.TCP_IP, TCP_PORT))
        except socket.error:
        	print("Socket error")
        	s.close()

        s.send(b"load /programs/closegrip.urp\n")
        time.sleep(1)
        s.send(b"play\n")
        time.sleep(1.5)

        s.close()

    def move_piece(self, from_x, from_y, to_x, to_y):
        self.s.send(b'def move_to_pickup():\n')
        
        #Go to from_position
        self.send_socket_move_xyz(from_x, from_y, self.top_z) #Go over
        self.send_socket_move_xyz(from_x, from_y, self.bottom_take_z) #Go down

        self.s.send(b'end\n')
        time.sleep(6)
        self.close_gripper() #Close gripper, take piece
        
        self.s.send(b'def move_to_release():\n')
        self.send_socket_move_xyz(from_x, from_y, self.top_z) #Go up

        #Go to to_position
        self.send_socket_move_xyz(to_x, to_y, self.top_z) #Go over
        self.send_socket_move_xyz(to_x, to_y, self.bottom_release_z) #Go down
        self.s.send(b'end\n')
        time.sleep(6)
        self.open_gripper() #Open gripper

        self.s.send(b'def move_up_to_end():\n')
        self.send_socket_move_xyz(to_x, to_y, self.top_z) #Go up
        self.s.send(b'end\n')
        time.sleep(1)

    def capture_piece(self, from_x, from_y, to_x, to_y):
        self.s.send(b'def move_to_pickup():\n')

        #Go to, to position
        self.send_socket_move_xyz(to_x, to_y, self.top_z) #Go over
        self.send_socket_move_xyz(to_x, to_y, self.bottom_take_z) #Go down
        self.s.send(b'end\n')
        time.sleep(6)
        self.close_gripper() #Close gripper

        #Put on somewhere
        self.s.send(b'def move_to_release_piece():\n')
        self.send_socket_move_xyz(to_x, to_y, self.top_z) #Go over
        #Somewhere
        self.send_socket_move_xyz(to_x, self.drop_place_y, self.top_z)
        self.s.send(b'end\n')
        time.sleep(6)
        self.open_gripper()

        self.move_piece(from_x, from_y, to_x, to_y)


    def send_socket_move_xyz(self, x, y, z):
        self.s.send(b'  var_1=get_actual_tcp_pose()\n')
		
        st = '  var_1[0] = {}\n'.format(x)
        self.s.send(bytearray(st,'utf8'))
        st = '  var_1[1] = {}\n'.format(y)
        self.s.send(bytearray(st,'utf8'))
        st = '  var_1[2] = {}\n'.format(z)
        self.s.send(bytearray(st,'utf8'))
        self.s.send(b'  movel(var_1)\n')
        self.s.send(bytearray(st,'utf8'))