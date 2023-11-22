import pygame
from constantes import *
from player import Personaje
from enemigo import Enemigo
from terreno import Plataforma

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()
pygame.display.set_caption("Star Wars Ep. III")
clock = pygame.time.Clock()

background = pygame.image.load("./assets/background/coruscant_exterior.png")
background = pygame.transform.scale(background, (ANCHO_VENTANA, ALTO_VENTANA))

anakin = Personaje(0, 0, 80, 20, 16, 32)
battle_droid = Enemigo(1, 100, 200, 3, 3)
super_battle_droid = Enemigo(2, 50, 100, 2, 2)
plataformas = [
    Plataforma(0, 350, 800, 20, "./assets/background/Terrain/plataforma.png"),
    Plataforma(300, 400, 150, 20, "./assets/background/Terrain/plataforma.png"),
    Plataforma(500, 300, 100, 20, "./assets/background/Terrain/plataforma.png")
]

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
                elif event.key == pygame.K_y:
                    anakin.shoot(True)
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
    battle_droid.update(delta_ms)
    super_battle_droid.update(delta_ms)
    
    for plataforma in plataformas:
        plataforma.draw(screen)
    anakin.draw(screen)
    battle_droid.draw(screen)
    super_battle_droid.draw(screen)
    pygame.display.update()

pygame.quit()