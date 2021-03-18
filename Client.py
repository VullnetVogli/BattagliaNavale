from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from time import sleep
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
        
        print('\n\n')

        # Aspettiamo l'altro giocatore che si connetta
        self.aspetta_giocatore()

        print('La partita sta per iniziare...')

        # Il turno sarà deciso dal server
        turno = self.client_socket.recv(1024) == b'1'

        # Mandiamo la board del giocatore all'avversario
        self.client_socket.send(pickle.dumps(numpy.matrix(self.board.posizioni)))

        # Quella che riceviamo sarà quella dell'avversario
        self.board.set_board_nemico(board = (pickle.loads(self.client_socket.recv(1024), encoding = 'UTF-8')).tolist())

        print('Parti per primo!') if turno else print('Parti per secondo!')
        
        sleep(3)

        self.board.output()

        fine_gioco = False
        
        while not fine_gioco: 

            # Se tocca a noi, inseriamo le coordinate            
            if turno:

                coordinate = input('> ').upper()

                while not self.board.coordinate_valide(coordinate = coordinate):

                    coordinate = input('> ').upper()

                # Lo appuntiamo nella nostra board
                self.board.segna_coordiante_aversario(posizione = coordinate)

                # Se abbiamo fatto fuori tutte le navi del nemico, abbiamo vinto.
                if len(self.board.navi_nemico) == 0:

                    print('Hai vinto. :)')

                    # Usiamo 1 per notificare la vittoria
                    coordinate = '1' + coordinate

                    fine_gioco = True

                self.client_socket.send(bytes(coordinate.encode('UTF-8')))

            else:
                
                # Quando riceviamo le coordinate, controlliamo che l'avversario non abbia vinto e terminiamo il gioco
                coordinate = self.client_socket.recv(1024).decode('UTF-8')
                
                if coordinate[0] == '1':

                    self.board.segna_mie_coordinate(posizione = coordinate[1::])

                    self.board.output()

                    print('Hai perso. :(')

                    fine_gioco = True

                # Se invece non ha vinto ci segniamo le coordinate sulla board
                else:

                    self.board.segna_mie_coordinate(posizione = coordinate)

                    self.board.output()

            turno = not turno
        
        self.client_socket.close()

    def aspetta_giocatore(self):

        while self.client_socket.recv(1024) == b'aspetta':

            print('Aspettando un giocatore...')

        else:

            print('Un giocatore si è connesso!')

if __name__ == '__main__':
    
    Client().start()