import pygame
from constantes import *
from menus import *
from nivel import cargar_nivel

class Game:
    def __init__(self) -> None:
        """Inicializa un objeto Game
        """
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Star Wars Ep. III")
        self.clock = pygame.time.Clock()
        self.PAUSA = False
        self.cronometro = 60 * 1000
        self.iniciar_nivel = False
        self.nivel_actual = 1
        self.game_over = False
        self.puntuacion = 0
        
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/sounds/main_theme.mp3")
        pygame.mixer.music.play(-1)
        
        self.font = pygame.font.Font(None, 36)
        
        self.anakin = None
        self.plataformas = None
        self.cajas = None
        self.enemigos = None
    
    def handle_events(self):
        """Maneja los eventos del juego, respondiendo a las teclas presionadas o liberadas.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Estoy cerrando el juego")
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.PAUSA = not self.PAUSA
                else:
                    self.anakin.handle_events([event])
    
    def iniciar_juego(self, nivel):
        """Inicializara el nivel del juego seleccionado

        Args:
            nivel (int): nivel especifico del juego
        """
        self.iniciar_nivel = True
        
        match nivel:
            case 1:
                self.anakin, self.plataformas, self.cajas, self.fondo, self.enemigos = cargar_nivel("nivel1.json")
                self.bg = pygame.image.load(self.fondo)
                self.bg = pygame.transform.scale(self.bg, (ANCHO_VENTANA, ALTO_VENTANA))
                self.cronometro = 60 * 1000
            case 2:
                self.anakin, self.plataformas, self.cajas, self.fondo, self.enemigos = cargar_nivel("nivel2.json")
                self.bg = pygame.image.load(self.fondo)
                self.bg = pygame.transform.scale(self.bg, (ANCHO_VENTANA, ALTO_VENTANA))
                self.cronometro = 60 * 1000
            case 3:
                self.anakin, self.plataformas, self.cajas, self.fondo, self.enemigos = cargar_nivel("nivel3.json")
                self.bg = pygame.image.load(self.fondo)
                self.bg = pygame.transform.scale(self.bg, (ANCHO_VENTANA, ALTO_VENTANA))
                self.cronometro = 60 * 1000
    
    def mostrar_mensaje(self, mensaje):
        text = self.font.render(mensaje, True, WHITE)
        self.screen.blit(text, (ANCHO_VENTANA // 2 - text.get_width() // 2, ALTO_VENTANA // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000) 
    
    
    def handle_key_input(self):
        """Maneja la entrada del teclado para el juego.

        Captura el estado de las teclas presionadas y llama al método `handle_key_input`
        del objeto `anakin` para procesar la entrada del personaje.
        """
        keys = pygame.key.get_pressed()
        self.anakin.handle_key_input(keys, self.clock.get_rawtime())

    def update(self):
        """Actualiza el estado del juego.

        Calcula el tiempo transcurrido desde la última actualización, 
        llama al método `update` del objeto `anakin` para actualizar su estado,
        y actualiza las plataformas.
        """
        delta_ms = self.clock.tick(FPS)
        
        if self.iniciar_nivel:
            self.cronometro -= delta_ms
            
            if self.cronometro <= 0:
                print("Tiempo agotado!")
                self.game_over = True
                self.iniciar_nivel = False
        else:
            self.cronometro = 60 * 1000
        
        # Detectar colisiones con cajas
        colisiones = pygame.sprite.spritecollide(self.anakin, self.cajas, dokill=True)

        for caja in colisiones:
            self.puntuacion += caja.puntos
            print(f"Puntos: {self.puntuacion}")
        
        # Detectar colisiones con enemigos
        colisiones_enemigos = pygame.sprite.spritecollide(self.anakin, self.enemigos, dokill=True)
        for enemigo in colisiones_enemigos:
            # Lógica de colisión con enemigo (por ejemplo, disminuir la vida del personaje)
            print("Colisión con enemigo!")
        
        self.anakin.update(delta_ms, self.plataformas.sprites())
        self.enemigos.update(delta_ms, self.plataformas.sprites())

    def draw(self):
        """Dibuja los elementos del juego en la pantalla.

        Rellena la pantalla con un color de fondo, dibuja el fondo y luego
        dibuja las plataformas, cajas, enemigos y el personaje (`anakin`).
        """
        self.screen.fill(BLACK)
        self.screen.blit(self.bg, self.bg.get_rect())

        self.plataformas.draw(self.screen)
        self.cajas.draw(self.screen)
        self.enemigos.draw(self.screen)

        self.anakin.draw(self.screen)
        
        if self.game_over:
            self.mostrar_mensaje("Game Over")
            menu_principal(self.screen, self.iniciar_juego)

        # Dibujar el cronómetro en la pantalla
        minutos = int(self.cronometro / 60000)
        segundos = int((self.cronometro % 60000) / 1000)
        tiempo_texto = f"{minutos:02}:{segundos:02}"
        texto = self.font.render(tiempo_texto, True, WHITE)
        self.screen.blit(texto, (10, 10))

        pygame.display.update()

    def run(self):
        """Inicia la ejecución del juego.

        Muestra el menú principal y luego ejecuta un bucle principal del juego.
        Dentro del bucle, maneja eventos, procesa la entrada del teclado, actualiza
        el estado del juego y dibuja los elementos en la pantalla
        """
        menu_principal(self.screen, self.iniciar_juego)

        while EJECUTANDO:
            self.handle_events()

            if self.PAUSA:
                pausar_juego(self.screen, [self.PAUSA])
                self.PAUSA = False

            self.handle_key_input()
            self.update()
            self.draw()

        pygame.quit()