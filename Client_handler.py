from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from time import sleep

class ClientHandler(Thread):
    
    def __init__(self, client_socket_1: socket, client_socket_2: socket):
        
        super().__init__()
        
        self.client_socket_1 = client_socket_1
        
        self.client_socket_2 = client_socket_2
        
    def run(self):
        
        sleep(1)

        # Decidiamo i turni in maniera random
        self.turni()

        dati1 = self.client_socket_1.recv(1024)
        
        dati2 = self.client_socket_2.recv(1024)

        self.client_socket_1.send(dati2)

        self.client_socket_2.send(dati1)

        dati1 = None

        dati2 = None

        while dati1 != b'' and dati2 != b'':
            
            dati1 = self.client_socket_1.recv(1024)
            
            self.client_socket_2.send(dati1)

            dati2 = self.client_socket_2.recv(1024)

            self.client_socket_1.send(dati2)
        
        print('fin')
        
    def turni(self):

        self.client_socket_1.send(b'1')

        self.client_socket_2.send(b'0')