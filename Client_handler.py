from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from time import sleep

class ClientHandler(Thread):
    
    def __init__(self, server_socket: socket, client_socket_1: socket, client_socket_2: socket):
        
        super().__init__()
        
        self.server_socket = server_socket
        
        self.client_socket_1 = client_socket_1
        
        self.client_socket_2 = client_socket_2
        
    def run(self):
        
        print('runno')
        
        dati1 = 'dsa'
        
        dati2 = 'dsa'
        
        while dati1 != b'' and dati2 != b'':
            
            dati1 = self.client_socket_1.recv(1024)
            
            dati2 = self.client_socket_2.recv(1024)
            
            print(dati1, dati2)
            
            self.client_socket_1.send(dati1)
            
            self.client_socket_2.send(dati2)
            
            sleep(1)
        
        print('fin')
        
        self.client_socket_1.close()
        
        self.client_socket_2.shutdown(1)
        
        
        