# tiene anotaciones de noob 
import pygame
from sys import exit

pygame.init()

WIDTH, HEIGHT =  800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creo una ventana 
pygame.display.set_caption('Jejej') # nombre
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#test_surface = pygame.Surface((100, 200))
#test_surface.fill('Red')

sky_surface = pygame.image.load('graphics/fly.png')
ground_surface = pygame.image.load('graphics/ground.png')
text_surface = test_font.render('Sos un bolude', False, 'Black')



def main(): # loop del juego 

    run = True
    while run: 
        for event in pygame.event.get(): # itero en los event   
            if event.type == pygame.QUIT:  # si presiono para cerrar termina el juego 
                pygame.quit()
                exit()     

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(text_surface, (WIDTH/2 - 120, HEIGHT/2))

        pygame.display.update() # update the display surface 
        clock.tick(60)  # maximum framrate: 60 fps

if __name__ ==  "__main__": 
    main()      