import pygame
from constantes import *
from player import Personaje

screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.init()
pygame.display.set_caption("Star Wars Ep. III")
clock = pygame.time.Clock()

background = pygame.image.load("./assets/background/coruscant_exterior.png")
background = pygame.transform.scale(background, (ANCHO_PANTALLA, ALTO_PANTALLA))

anakin = Personaje(0, 0, 70, 20, 16, 32)

while EJECUTANDO:
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        match event.type:
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    anakin.jump(True)
                elif event.key == pygame.K_t:
                    print("Estoy atacando")
                    anakin.do_attack(True)
            case pygame.QUIT:
                print('Estoy CERRANDO el JUEGO')
                EJECUTANDO = False
                break
    
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