from threading import Thread
from socket import socket

class Write(Thread):
    
    def __init__(self, client_socket: socket):
        
        self.