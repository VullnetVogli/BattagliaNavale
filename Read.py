from threading import Thread
from socket import socket

class Read(Thread):
    
    def __init__(self, client_socket: socket):
        
        super().__init__()
        
        self.client_socket = client_socket
        
        self.messaggio = b''
        
    def get_messaggio(self):
        
        return self.messaggio
        
    def run(self):
        
        self.messaggio = self.client_socket.recv(1024)
        
        print(self.messaggio)
        
        while self.messaggio != b'':
            
            self.messaggio = self.client_socket.recv(1024)
            
            print('ricevuto', self.messaggio)