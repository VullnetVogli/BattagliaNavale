from socket import AF_INET, SOCK_STREAM, socket
from Client_handler import ClientHandler
from threading import Thread

class Server(Thread):
    
    def __init__(self, ip = 'localhost', porta = 6969):
        
        super().__init__(name = 'Server')
        
        self.server_socket = socket(AF_INET, SOCK_STREAM) 
        
        self.server_socket.bind((ip, porta))
        
        self.server_socket.listen()
        
    def run(self):
        
        try:
        
            while True:
                
                socket_client_1, indirizzo = self.server_socket.accept()
                    
                socket_client_1.send(b'aspetta')
                    
                socket_client_2, indirizzo = self.server_socket.accept()
                    
                socket_client_1.send(b'connesso')
                    
                ClientHandler(client_socket_1 = socket_client_1, client_socket_2 = socket_client_2, server_socket = self.server_socket).start()
                
        except KeyboardInterrupt:
            
            self.server_socket.close()
         
if __name__ == '__main__':
    
    Server().start()
        