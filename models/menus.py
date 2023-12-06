import pygame
from constantes import *
from boton import Boton

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
        
        fondo_pausa = pygame.image.load("./assets/background/bg_pausa.jpeg")
        fondo_pausa = pygame.transform.scale(fondo_pausa, (ANCHO_VENTANA, ALTO_VENTANA))
        screen.blit(fondo_pausa, (0, 0))
        
        fuente = pygame.font.Font(None, 36)
        
        texto1 = fuente.render("JUEGO PAUSADO. Presiona 'C' para continuar o 'Q' para salir.", True, WHITE)
        texto2 = fuente.render("You can now hear the Tragedy of Darth Plageis, the Wise", True, WHITE)
        
        texto_rect1 = texto1.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
        texto_rect2 = texto2.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 3))
        
        screen.blit(texto1, texto_rect1)
        screen.blit(texto2, texto_rect2)
        
        pygame.display.flip()

def menu_opciones(screen, musica_activada=False):
    """Muestra y gestiona el menú de opciones del juego.

    Muestra un fondo de menú, botones para activar/desactivar la música y volver al menú principal.
    Permite al usuario interactuar con los botones y realiza acciones correspondientes.

    Args:
        screen (pygame.Surface): La superficie de la pantalla del juego.
        musica_activada (bool): Indica si la música está activada o no.

    Returns:
        bool: True si el usuario vuelve al menú principal, False de lo contrario.
    """
    fondo_opciones = pygame.image.load("./assets/background/menu_principal.jpg")
    fondo_opciones = pygame.transform.scale(fondo_opciones, (ANCHO_VENTANA, ALTO_VENTANA))

    # Crear botones del submenú de música
    musica_on_boton = Boton(150, 200, 200, 50, "Música: Activada", MAGENTA, (200, 200, 0))
    musica_off_boton = Boton(150, 300, 200, 50, "Música: Desactivada", MAGENTA, (200, 200, 0))
    volver_boton = Boton(150, 500, 200, 50, "Volver", MAGENTA, (200, 200, 200))

    en_menu_opciones = True
    en_menu_principal = False

    while en_menu_opciones and not en_menu_principal:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                musica_on_boton.handle_event(event)
                musica_off_boton.handle_event(event)
                volver_boton.handle_event(event)

        pygame.mouse.get_rel()

        screen.blit(fondo_opciones, (0, 0))

        font = pygame.font.Font(None, 36)

        # Dibujar botones
        musica_on_boton.draw(screen, font)
        musica_off_boton.draw(screen, font)
        volver_boton.draw(screen, font)

        pygame.display.update()

        # Comprobar acciones de los botones del submenú de música
        if musica_on_boton.hovered and pygame.mouse.get_pressed()[0]:
            musica_activada = not musica_activada
            pygame.mixer.music.unpause()
        elif musica_off_boton.hovered and pygame.mouse.get_pressed()[0]:
            musica_activada = False
            pygame.mixer.music.pause()
        elif volver_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu_opciones = False
            en_menu_principal = True

    return en_menu_principal


def menu_principal(screen, iniciar_juego):
    """Muestra y gestiona el menú principal del juego.

    Muestra un fondo de menú, botones para iniciar el juego, salir y acceder al menú de opciones.
    Permite al usuario interactuar con los botones y realiza acciones correspondientes.

    Args:
        screen (pygame.Surface): La superficie de la pantalla del juego.
        iniciar_juego (callable): Función que inicia el juego.

    Returns:
        None
    """
    fondo_menu = pygame.image.load("./assets/background/menu_principal.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO_VENTANA, ALTO_VENTANA))

    iniciar_boton = Boton(150, 200, 200, 50, "Iniciar Juego", BLUE, (0, 0, 255))
    salir_boton = Boton(150, 300, 200, 50, "Salir", RED, (200, 0, 0))
    opcion_boton = Boton(150, 400, 200, 50, "Opciones", GREEN, (0, 200, 0))

    en_menu = True

    while en_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                iniciar_boton.handle_event(event)
                salir_boton.handle_event(event)
                opcion_boton.handle_event(event)

        pygame.mouse.get_rel()

        screen.blit(fondo_menu, (0, 0))

        font = pygame.font.Font(None, 36)
        iniciar_boton.draw(screen, font)
        salir_boton.draw(screen, font)
        opcion_boton.draw(screen, font)

        pygame.display.update()

        if iniciar_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu = False
            pygame.mixer.music.stop()
            iniciar_juego(1)
        elif salir_boton.hovered and pygame.mouse.get_pressed()[0]:
            pygame.quit()
            quit()
        elif opcion_boton.hovered and pygame.mouse.get_pressed()[0]:
            en_menu = menu_opciones(screen, False)
            
            if not en_menu:
                en_menu = True