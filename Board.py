from os import system
import numpy
from time import sleep
class Board():

    BOARD_DIM = 10

    pezzi = {
        #'Portaerei': numpy.matrix(['▄', '▄', '▄', '▄', '▄']),
        #'Corazzata': numpy.matrix(['▄', '▄', '▄', '▄']),
        #'Crociere': numpy.matrix(['▄', '▄', '▄']),
        'Sottomarino': numpy.matrix(['▄', '▄']),
        'Nave da assalto': numpy.matrix(['▄'])
    }

    # O: non preso, X: preso

    def __init__(self):

        self.board = self.crea()

        self.board_nemico = self.crea()

        self.posizioni = []

        self.inizializza_board()
        
        self.navi_nemico = None

    def set_board_nemico(self, board: numpy.matrix):
        
        self.navi_nemico = board

    def get_board(self):

        return self.board

    def inizializza_board(self):
            
        for nome_nave in self.pezzi.keys():

            dim_pezzo = self.pezzi[nome_nave].shape[1]

            pezzo = self.pezzi[nome_nave].transpose() if input('{} con lunghezza "{}" in verticale o in orizzontale? v/o: '.format(nome_nave, dim_pezzo)) == 'v' else self.pezzi[nome_nave]

            x, y = self.inserisci_coordinate()

            while self.collisione(x, y, dim_pezzo):

                print('Collisione!')

                x, y = self.inserisci_coordinate()

            else:
                
                # Se la nave è verticale
                if pezzo.shape[0] == 1:
                    
                    self.posizioni.append((x, y, 0, dim_pezzo, 0))
                    
                    for i in range(0, dim_pezzo):
                    
                        self.board[x][y + i] = pezzo[0, i]

                else:

                    self.posizioni.append((x, y, dim_pezzo, 0, 0)) 

                    for i in range(0, dim_pezzo):

                        self.board[x + i][y] = pezzo[i, 0]
            
            self.output()

    def inserisci_coordinate(self):

        x = y = -1

        coordinate = input('Inserisci le coordinate: ').upper()

        if self.coordinate_valide(coordinate = coordinate):

            return ord(coordinate[0]) - 64, int(coordinate[1::])

        else:

            print('Inserisci bene!', coordinate)

            return self.inserisci_coordinate()

    def output(self):

        system('cls')

        for i in range(len(self.board)):

            for j in self.board[i]:

                print(j, end = ' ')

            print('\t\t\t', end = ' ')

            for j in self.board_nemico[i]:

                print(j, end = ' ')

            print()

    def crea(self):

        a = []
        b = [' ']

        for j in range(1, self.BOARD_DIM + 1):

            b.append(str(j))

        a.append(b)

        for i in range(self.BOARD_DIM):

            b = [chr(i + ord('A'))]

            for j in range(1, self.BOARD_DIM + 1):

                b.append('~')

            a.append(b)

        return numpy.array(a)

    def collisione(self, x: int, y: int, dim_pezzo: int):
        
        return '▄' in self.board[x : x + dim_pezzo, y]

    def coordinate_valide(self, coordinate: str):
        
        # Controlliamo che la lunghezzia sia almeno di due, che la prima sia una lettera, che il resto siano dei numeri e che non vadano fuori dalla matrice
        return len(coordinate) > 1 and coordinate[0].isascii() and coordinate[1::].isdecimal() and ord(coordinate[0]) - 64 > 0 and ord(coordinate[0]) - 64 <= self.BOARD_DIM and int(coordinate[1::]) > 0 and int(coordinate[1::]) <= self.BOARD_DIM

    def segna_mie_coordinate(self, posizione: str):
        
        x = ord(posizione[0]) - 64

        y = int(posizione[1::])
        
        # Controlla se il colpo è all'interno di posizioni
        for nave_nemico in self.navi_nemico:
            
            if nave_nemico[0] <= x <= nave_nemico[0] + nave_nemico[2]:

                if nave_nemico[1] <= y <= nave_nemico[1] + nave_nemico[3]:

                    self.board[x][y] = 'X'

                    break
        
                else:

                    self.board[x][y] = 'O'

                    break
            else:

                self.board[x][y] = 'O'

        self.output()

    def segna_coordiante_aversario(self, posizione: str):
        
        x = ord(posizione[0]) - 64

        y = int(posizione[1::])
        
        # Scorro le navi dell'avversario
        for nave_nemico in self.navi_nemico:
            
            # Controlliamo se il colpo è all'interno delle coordinate x
            if nave_nemico[0] <= x <= nave_nemico[0] + nave_nemico[2]:

                # Controlliamo se il colpo è all'interno delle coordinate y
                if nave_nemico[1] <= y <= nave_nemico[1] + nave_nemico[3]:

                    # Segniamo che il colpo è andato a segno
                    self.board_nemico[x][y] = 'X'

                    # Constrolliamo se con quel colpo il giocatore abbia vinto
                    self.controlla_vittoria(nave_nemico = nave_nemico)

                    break
                
                # Altrimenti è andato a vuoto
                else:

                    # Segniamo che è andato a vuott
                    self.board_nemico[x][y] = 'O'

                    break

            # Altrimenti è andato a vuoto
            else:

                # Segniamo che è andato a vuott
                self.board_nemico[x][y] = 'O'

                break

        self.output()

    def controlla_vittoria(self, nave_nemico):

        # Se il pezzo è verticale
        if nave_nemico[2] == 0:

            # E la nave è stata colpita in tutta la sua lunghezza la consideriamo affondata
            if nave_nemico[4] == nave_nemico[3] - 1:

                self.navi_nemico.remove(nave_nemico)
                
                return True

            # Altrimenti un'altra parte della nave è stata colpita
            else:

                nave_nemico[4] += 1

        # Stessa cosa se il pezzo è in orizzontale
        else:

            if nave_nemico[4] == nave_nemico[2] - 1:

                self.navi_nemico.remove(nave_nemico)

                return True

            else:

                nave_nemico[4] += 1

        return False

if __name__ == '__main__':

    b = Board()
    
    