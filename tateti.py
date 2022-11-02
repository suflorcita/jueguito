from os import system

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Tateti:
    def __init__(self):
        self._mesa = [['-','-','-'],
                     ['-','-','-'],
                     ['-','-','-']]
    
    def setval(self, x: int, y: int, val: str):
        """
        Coloca un (val) en las coordenadas dadas.
        Si el (val) se puede poner en esa posicion, entonces lo guarda ahi y devuelve True.
        De lo contrario devulve False.
        """
        if self._mesa[x][y] == '-':
            self._mesa[x][y] = val.lower()
            return True
        return False
    
    def draw(self):
        """
        Dibuja el tablero en el terminal.
        """
        print('  A B C')
        for x in range(3):
            print(x+1, end=' ')
            for val in self._mesa[x]:
                if val == 'x':
                    color = bcolors.BLUE
                elif val == 'o':
                    color = bcolors.RED
                else:
                    color = bcolors.ENDC
                print(color+val+bcolors.ENDC, end=' ')
            print()
    
    def check_win(self):
        """
        Devuelve si el ganador es (x, o) o False si nadie gana aun.
        """
        # Horizontales
        for fila in range(3):
            if self._mesa[fila][0] == 'x' == self._mesa[fila][1] == self._mesa[fila][2]:
                return 'x'
            elif self._mesa[fila][0] == 'o' == self._mesa[fila][1] == self._mesa[fila][2]:
                return 'o'
        # Verticales
        for col in range(3):
            if self._mesa[0][col] == 'x' == self._mesa[1][col] == self._mesa[2][col]:
                return 'x'
            elif self._mesa[0][col] == 'o' == self._mesa[1][col] == self._mesa[2][col]:
                return 'o'
        
        # Diagonales decreciente \
        if self._mesa[0][0] == 'x' == self._mesa[1][1] == self._mesa[2][2]:
            return 'x'
        elif self._mesa[0][0] == 'o' == self._mesa[1][1] == self._mesa[2][2]:
            return 'o'
        
        # Diagonales creciente /
        if self._mesa[2][0] == 'x' == self._mesa[1][1] == self._mesa[0][2]:
            return 'x'
        elif self._mesa[2][0] == 'o' == self._mesa[1][1] == self._mesa[0][2]:
            return 'o'
        
        return False

    def espacios_vacios(self):
        """
        Devuelve True si aun quedan esapcios libres. False si ya no quedan espacios.
        """
        cont = 0
        for x in range(3):
            for y in range(3):
                if self._mesa[x][y] == '-':
                    cont += 1
        
        if cont == 0:
            return False
        return True

    def reset(self):
        self.__init__()

    def get_dict(self):
        dictio = {}
        for x, fila in enumerate(self._mesa):
            for y, col in enumerate(fila):
                dictio[(x, y)] = col.lower()
        return dictio

def clean_input():
    """
    Pide al usuario que ingrese una coordenada del estilo (1A) o (1 A).
    Si el usuario no ingresa las coordenadas de manera correcta, entonces se le pide que 
    la ingrese de nuevo.
    """
    mapeado = {'a':0, 'b':1, 'c':2}
    decicion = input('Ingrese las coordenadas: ')
    if decicion == 'salir':
        exit()
    

    if len(decicion) == 2:
        x = decicion[0]
        y = decicion[1]
    elif len(decicion) == 3:
        x = decicion[0]
        y = decicion[2]
    else:
        print(f'{bcolors.YELLOW}No ingreso una coordenada valida{bcolors.ENDC}')
        return clean_input()
    
    try:
        x = int(x) - 1
        if x not in (0,1,2):
            raise IndexError
        y = mapeado[y.lower()]
        
    
    except ValueError:
        print(f'{bcolors.YELLOW}El primer valor ingresado no es un numero{bcolors.ENDC}')
        return clean_input()
    except IndexError:
        print(f'{bcolors.YELLOW}El primer valor ingresado no se encunetra en el rango (1,2,3){bcolors.ENDC}')
        return clean_input()
    except KeyError:
        print(f'{bcolors.YELLOW}El segundo valor ingresado no esta dentro del rango (A,B,C){bcolors.ENDC}')
        return clean_input()
    return x, y

def turno_de_jugador(jugador: str, mesa: Tateti):
    """
    Maneja el turno del (jugador) y evita que pierda el turno
    si ingresa una coordenada incorrecta
    """
    if jugador.lower() == 'x':
        color = bcolors.BLUE
    else:
        color = bcolors.RED
    print(f'Turno del jugador {color}{jugador}{bcolors.ENDC}')
    x, y = clean_input()
    if not mesa.setval(x, y, jugador):
        print(f'{bcolors.YELLOW}No puede colocar nada en esa coordenada.{bcolors.ENDC}')
        mesa.draw()
        return turno_de_jugador(jugador, mesa)

if __name__ == '__main__':
    tablero = Tateti()
    print('Bienvenido al Tateti. Los valores se ingresan con el formato numero, letra')

    tablero.draw()

    for i in range(10):
        # Turno del jugador O
        turno_de_jugador('O', tablero)
        system('clear')
        tablero.draw()
        
        ganador = tablero.check_win()
        if ganador != False:
            print(f'El ganador es {ganador}')
            break
        
        if not tablero.espacios_vacios():
            print('Ya no quedan espacios vacios. Fin de la partida')
            break
        
        # Turno del jugador X
        turno_de_jugador('X', tablero)
        system('clear')
        tablero.draw()
        
        ganador = tablero.check_win()
        if ganador != False:
            print(f'El ganador es {ganador}')
            break
        
        if not tablero.espacios_vacios():
            print('Ya no quedan espacios vacios. Fin de la partida')
            break

    print('Fin del programa')