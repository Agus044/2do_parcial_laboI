import pygame
from constantes import *

def pausar_juego(screen, paused):
    paused = True
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        screen.fill((0, 0, 0))
        
        fuente = pygame.font.Font(None, 36)
        
        texto = fuente.render("JUEGO PAUSADO. Presiona 'C' para continuar o 'Q' para salir.", True, (255, 255, 255))
        
        texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        
        screen.blit(texto, texto_rect)
        
        pygame.display.flip()