import socket 
import time

class Robot_programmer():

    def __init__(self):
        #Socket til at sende kommandoer til robotten
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)
        self.connected = False
        
        self.top_z = 245/1000.0
        self.bottom_z = 50/1000.0

    def connect(self, ip='10.130.58.11'):
        self.TCP_IP = ip
        TCP_PORT = 30002
        BUFFER_SIZE = 1024

        try:
            #print("Opening IP Address" + TCP_IP)
            self.s.connect((self.TCP_IP, TCP_PORT))
            response = self.s.recv(BUFFER_SIZE)
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
        	print("Opening IP Address" + self.TCP_IP)
        	s.connect((self.TCP_IP, TCP_PORT))
        	response = s.recv(BUFFER_SIZE)
        except socket.error:
        	print("Socket error")
        	s.close()
        
        s.send(b"load /programs/opengrip.urp\n")
        s.send(b"play\n")

        s.close()

    def close_gripper(self):
        TCP_PORT = 29999
        BUFFER_SIZE = 1024

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
        	print("Opening IP Address" + self.TCP_IP)
        	s.connect((self.TCP_IP, TCP_PORT))
        	response = s.recv(BUFFER_SIZE)
        except socket.error:
        	print("Socket error")
        	s.close()

        s.send(b"load /programs/closegrip.urp\n")
        s.send(b"play\n")

        s.close()

    def move_piece(self, from_x, from_y, to_x, to_y):
        self.s.send(b'def move_piece():\n')
        
    #Go to from_position
        self.send_socket_move_xyz(from_x, from_y, self.top_z) #Go over
        self.send_socket_move_xyz(from_x, from_y, self.bottom_z) #Go down

    #Grab piece, close gripper
        #CLOSE HERE
        self.send_socket_move_xyz(from_x, from_y, self.top_z) #Go up

    #Go to to_position
        self.send_socket_move_xyz(to_x, to_y, self.top_z)
        self.send_socket_move_xyz(to_x, to_y, self.bottom_z)

    #Put piece, open gripper
        #OPEN HERE
        self.send_socket_move_xyz(to_x, to_y, self.top_z) #Go up

        self.s.send(b'end\n')

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