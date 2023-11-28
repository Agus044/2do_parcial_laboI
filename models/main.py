import pygame
from constantes import *
#from player import Personaje
#from enemigo import Enemigo
#from terreno import Plataforma
from menu_pausa import pausar_juego
from nivel import cargar_niveles_json

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.init()
pygame.display.set_caption("Star Wars Ep. III")
clock = pygame.time.Clock()

#background1 = pygame.image.load("./assets/background/hallway.png")
#background1 = pygame.transform.scale(background1, (ANCHO_VENTANA, ALTO_VENTANA))

anakin, plataformas, cajas, fondo = cargar_niveles_json("nivel1.json")

bg = pygame.image.load(fondo)
bg = pygame.transform.scale(bg, (ANCHO_VENTANA, ALTO_VENTANA))
#battle_droid = Enemigo(1, 100, 200, 3, 3)
#super_battle_droid = Enemigo(2, 50, 100, 2, 2)

while EJECUTANDO:
    #delta_ms = clock.tick(FPS)
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        match event.type:
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    anakin.jump(True)
                elif event.key == pygame.K_p:
                    PAUSA = not PAUSA
            case pygame.QUIT:
                print('Estoy CERRANDO el JUEGO')
                EJECUTANDO = False
                break
    if PAUSA:
        pausar_juego(screen, [PAUSA])
        PAUSA = False
    
    lista_teclas_presionadas = pygame.key.get_pressed()
    if lista_teclas_presionadas[pygame.K_RIGHT] and not lista_teclas_presionadas[pygame.K_LEFT]:
        anakin.walk('Right')
    if lista_teclas_presionadas[pygame.K_LEFT] and not lista_teclas_presionadas[pygame.K_RIGHT]:
        anakin.walk('Left')
    if not lista_teclas_presionadas[pygame.K_RIGHT] and not lista_teclas_presionadas[pygame.K_LEFT]:
        anakin.stay()
    if lista_teclas_presionadas[pygame.K_SPACE]:
        anakin.jump(True)
    
    
    screen.blit(bg, bg.get_rect())
    delta_ms = clock.tick(FPS)
    anakin.update(delta_ms, plataformas)
    #battle_droid.update(delta_ms)
    #super_battle_droid.update(delta_ms)
    
    for plataforma in plataformas:
        plataforma.draw(screen)
    
    for caja in cajas:
        caja.draw(screen)
        
    anakin.draw(screen)
    #battle_droid.draw(screen)
    #super_battle_droid.draw(screen)
    pygame.display.update()

pygame.quit()