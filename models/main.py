import pygame
from constantes import *
from player import Personaje

pygame.init()

screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Star Wars Ep. III")
clock = pygame.time.Clock()

background = pygame.image.load("./assets/background/1.png")
background = pygame.transform.scale(background, (ANCHO_PANTALLA, ALTO_PANTALLA))

anakin = Personaje(0, 0, 70, 5, 10, 20)

while EJECUTANDO:
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            EJECUTANDO = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                anakin.jump(True)
    
    lista_teclas_presionadas = pygame.key.get_pressed()
    if lista_teclas_presionadas[pygame.K_RIGHT] and not lista_teclas_presionadas[pygame.K_LEFT]:
        anakin.walk('Right')
    if lista_teclas_presionadas[pygame.K_LEFT] and not lista_teclas_presionadas[pygame.K_RIGHT]:
        anakin.walk('Left')
    if not lista_teclas_presionadas[pygame.K_RIGHT] and not lista_teclas_presionadas[pygame.K_LEFT]:
        anakin.stay()
    
    
    screen.blit(background, background.get_rect())
    delta_ms = clock.tick(FPS)
    anakin.update(delta_ms)
    anakin.draw(screen)
    pygame.display.update()

pygame.quit()