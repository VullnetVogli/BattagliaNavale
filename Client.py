from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from time import sleep
from Read import Read
from Board import Board
import pickle
import numpy

class Client(Thread):
    
    def __init__(self, ip = 'localhost', porta = 6969):
        
        super().__init__(name = 'Client')
        
        self.board = Board()

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        
        self.client_socket.connect((ip, porta))

    def run(self):
        
        print('Aspettando un giocatore...')
        
        if self.client_socket.recv(1024) == b'connesso':
            
            print('Un giocatore si è connesso!')
        
        else:

            messaggio = b'aspetta'

            while messaggio == b'aspetta':

                messaggio = self.client_socket.recv(1024)

        print('La partita sta per iniziare...')

        turno = self.client_socket.recv(1024) == b'1'

        # Mandiamo la board del giocatore all'avversario
        self.client_socket.send(pickle.dumps(numpy.matrix(self.board.posizioni)))

        self.board.set_board_nemico(board = (pickle.loads(self.client_socket.recv(1024), encoding = 'UTF-8')).tolist())

        print('Parti per primo!') if turno else print('Parti per secondo!')

        nuova_mossa = ''
        
        while nuova_mossa != 'fine': 
            
            if turno:

                coordinate = input('> ').upper()

                while not self.board.coordinate_valide(coordinate = coordinate):

                    coordinate = input('> ').upper()

                self.board.segna(posizione = coordinate)

                self.client_socket.send(bytes(coordinate.encode('UTF-8')))

            else:

                self.board.attacca(posizione = self.client_socket.recv(1024).decode('UTF-8'))

            self.board.output()

            turno = not turno
            
        self.client_socket.shutdown(1)

        self.client_socket.close()

        print('fine')


if __name__ == '__main__':
    
    Client().start()