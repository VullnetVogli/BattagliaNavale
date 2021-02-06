from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from time import sleep
from Read import Read

class Client(Thread):
    
    def __init__(self, ip = 'localhost', porta = 6969):
        
        super().__init__(name = 'Client')
        
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        
        self.client_socket.connect((ip, porta))
        
        self.read = Read(client_socket = self.client_socket)
        
    def run(self):
        
        self.read.start()
        
        sleep(1)
        
        while self.read.get_messaggio() == b'aspetta':
            
            print('aspetto')
            
            sleep(1)
        
        for i in range(10):
            
            self.client_socket.send(bytes('{}'.format(i).encode('UTF-8')))
            
            print('mando', i)
            
            sleep(1)
            
        self.client_socket.shutdown(1)
        
if __name__ == '__main__':
    
    Client().start()