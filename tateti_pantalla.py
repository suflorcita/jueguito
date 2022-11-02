import pygame
from tateti import Tateti
from os import path
from random import choice

class Display:
    def __init__(self, ancho: int, alto: int):
        self.display = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption('Elecciones 2023') # nombre

        pygame.font.init()
        self.font = pygame.font.SysFont('comicsans', 32)
        self.gatito = pygame.image.load(path.join('graphics', 'gatito.png'))
        self.beto = pygame.image.load(path.join('graphics', 'beto.png'))
        
        self.cuarta = self.display.get_width()//4
        self.espacio = self.cuarta//4

        self.gatito = pygame.transform.scale(self.gatito, (self.cuarta-self.espacio, self.cuarta-self.espacio))
        self.beto   = pygame.transform.scale(self.beto, (self.cuarta-self.espacio, self.cuarta-self.espacio))
    
    def update(self, tablero: Tateti, winner: str):
        self.display.fill((0,0,0))
        mesa_dict = tablero.get_dict()
        
        for y in range(3):
            for x in range(3):
                if mesa_dict[(x, y)] == 'x':
                    color = 'blue'
                elif mesa_dict[(x, y)] == 'o':
                    color = 'red'
                    # if not pygame.mixer.music.get_busy():
                    #     pygame.mixer.music.load()
                else:
                    color = 'black'
                
                # x*cuarta + x*espacio*(3/2) + espacio
                pos_x = x*self.cuarta + x*self.espacio*(3/2) + self.espacio
                pos_y = y*self.cuarta + y*self.espacio*(3/2) + self.espacio
                # pygame.draw.rect(self.display, color, 
                #                  (y*self.cuarta+self.espacio+self.espacio*1.5*y, x*self.cuarta+self.espacio+self.espacio*1.5*x, 
                #                   self.cuarta-self.espacio, self.cuarta-self.espacio), border_radius=30)
                    
                if color == 'blue': 
                    self.display.blit(self.gatito, (pos_y, pos_x))
                elif color == 'red': 
                    self.display.blit(self.beto, (pos_y, pos_x))
        self.draw_grid()
        if not tablero.espacios_vacios() and not winner:
            self.tie_sign()
        elif winner:
            self.win_sign(winner)
        
        pygame.display.update()
    
    def draw_grid(self):
        ancho = self.display.get_width()
        for x in range(0, ancho, ancho//3):
            pygame.draw.line(self.display, 'White', (0, x), (ancho, x), 3)
            pygame.draw.line(self.display, 'white', (x, 0), (x, ancho), 3)
    
    def tie_sign(self):
        ancho = self.display.get_width()
        text = self.font.render('Aprendan a votar BOLUDOS!!', True, 'black')
        txt_rect = text.get_rect()
        txt_rect.center = ancho//2, ancho//2
        pygame.draw.rect(self.display, (0,156,54), txt_rect, border_radius=8)
        self.display.blit(text, txt_rect)

    def win_sign(self, winner: str):
        ancho = self.display.get_width()
        if winner == 'x':
            text = self.font.render('El ganador es el Macri', True, 'black')
        elif winner == 'o':
            text = self.font.render('El ganador es el Alberto', True, 'black')
        
        txt_rect = text.get_rect()
        txt_rect.center = ancho//2, ancho//2
        pygame.draw.rect(self.display, (0,156,54), txt_rect, border_radius=8)
        self.display.blit(text, txt_rect)


class Musica:
    def __init__(self):
        pygame.mixer.init()

    def play_macri(self):
        if not pygame.mixer.music.get_busy():
            macri = pygame.mixer.music.load('music/macri.mp3')
            pygame.mixer.music.play(start=32)
    
    def play_beto(self):
        if not pygame.mixer.music.get_busy():
            beto = pygame.mixer.music.load('music/beto.mp3')
            pygame.mixer.music.play()

    
    def play_tie(self):
        if not pygame.mixer.music.get_busy():
            beto = pygame.mixer.music.load('music/tie.mp3')
            pygame.mixer.music.play()
    
    def stop(self):
        pygame.mixer.music.stop()


class Jugador:
    """Clase para manejar turnos entre dos jugadores"""
    def __init__(self):
        self._jugador = choice(('O', 'X'))
    
    def swap(self):
        """Cambia el turno actual"""
        if self._jugador == 'X':
            self._jugador = 'O'
        else:
            self._jugador = 'X'
    
    @property
    def jugador(self):
        """Turno actual"""
        return self._jugador.lower()


def get_cords(key: int) -> tuple:
    BASE = 1073741912
    CORDS = {7:(0,0), 8:(0,1), 9:(0,2),
             4:(1,0), 5:(1,1), 6:(1,2),
             1:(2,0), 2:(2,1), 3:(2,2),
             
             116:(0,0), 121:(0,1), 117:(0,2),
             103:(1,0), 104:(1,1), 106:(1,2),
             98:(2,0), 110:(2,1), 109:(2,2)
             }
    try:
        if 98 <= key <= 121:        # Si es con letras
            resultado = CORDS[key]
        else:                       # Si es con teclado numerico
            key -= BASE
            resultado = CORDS[key]
    
    except KeyError:
        resultado = None
    return resultado



if __name__ == '__main__':
    
    FPS = 30
    clock = pygame.time.Clock()
    SCREEN = Display(600, 600)
    can_play = True
    winner = False
    
    tablero = Tateti()
    jugador = Jugador()
    musica = Musica()
    
    while True:
        clock.tick(FPS)
        placed = False
        cords = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                
                if event.key == pygame.K_SPACE:
                    # Reinicia el juego
                    SCREEN.display.fill((0,0,0))
                    can_play = True
                    winner = False
                    tablero.reset()
                    musica.stop()
                
                cords  = get_cords(event.key)
                
        
        if can_play and cords:
            placed = tablero.setval(cords[0], cords[1], jugador.jugador)
        
        if placed:
            jugador.swap()
            winner = tablero.check_win()
        
        if not tablero.espacios_vacios() and not winner:
            musica.play_tie()

        if winner:
            can_play = False
            if winner == 'x':
                musica.play_macri()
            else:
                musica.play_beto()
            
        SCREEN.update(tablero, winner)