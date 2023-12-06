import pygame as pg
from auxiliar import SurfaceManager as sf
from constantes import *
from proyectil import Proyectil

class Personaje(pg.sprite.Sprite):

    def __init__(self, coord_x: int, coord_y: int, frame_rate = 100, speed_walk = 6, gravity = 16, jump = 32):
        """Inicializa una instancia de la clase Personaje.

        Parameters:
        - `coord_x` (int): La coordenada x inicial del personaje.
        - `coord_y` (int): La coordenada y inicial del personaje.
        - `frame_rate` (int): La velocidad de fotogramas de la animación. Default: 100
        - `speed_walk` (int): La velocidad de desplazamiento lateral. Default: 6
        - `gravity` (int): La fuerza de gravedad que afecta al personaje. Default: 16
        - `jump` (int): La potencia del salto del personaje. Default: 32
        """
        super().__init__()
        self.__iddle_r = sf.get_surface_from_spritesheet('./assets/player/Iddle/player_idle.png', 5, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet('./assets/player/Iddle/player_idle.png', 5, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet('./assets/player/Walk/player_walk.png', 13, 1)
        self.__walk_l = sf.get_surface_from_spritesheet('./assets/player/Walk/player_walk.png', 13, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet('./assets/player/Jump/player_jump.png', 6, 1)
        self.__jump_l = sf.get_surface_from_spritesheet('./assets/player/Jump/player_jump.png', 6, 1, flip=True)
        self.__attack_r = sf.get_surface_from_spritesheet('./assets/player/Attack/Melee/player_atk_melee.png', 10, 1)
        self.__attack_l = sf.get_surface_from_spritesheet('./assets/player/Attack/Melee/player_atk_melee.png', 10, 1, flip=True)
        self.__shoot_r = sf.get_surface_from_spritesheet('./assets/player/Attack/Shoot/player_shoot.png', 14, 1)
        self.__shoot_l = sf.get_surface_from_spritesheet('./assets/player/Attack/Shoot/player_shoot.png', 14, 1, flip=True)
        
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True
        self.__proyectiles = pg.sprite.Group()
        self.__is_attaking = False
        self.__is_shooting = False
        
        self.__vida = 3
        self.__tiempo_transcurrido = 0
        self.__tiempo_last_jump = 0
        self.__interval_time_jump = 100

    
    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        """_summary_

        Args:
            move_x (_type_): _description_
            animation_list (list[pg.surface.Surface]): _description_
            look_r (bool): _description_
        """
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        
    
    def __set_y_animations_preset(self):
        """Configura las propiedades relacionadas con la animación vertical del jugador para el salto.
        """
        self.__move_y = -self.__jump
        self.__move_x = self.__speed_walk if self.__is_looking_right else -self.__speed_walk
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        self.__is_jumping = True
    
    def walk(self, direction: str = 'Right'):
        """Inicia la animación de caminar en la dirección especificada.

        Args:
            direction (str): Dirección del movimiento ('Right' para derecha, 'Left' para izquierda).
        """
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=look_right)
    
    
    def stay(self):
        """Detiene la animación y establece al jugador en un estado de reposo.
        """
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0
    
    def jump(self, jumping: bool):
        """Inicia o detiene la animación de salto del jugador.

        Args:
            jumping (bool): True para iniciar el salto, False para detenerlo.
        """
        if jumping and not self.__is_jumping:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()
    
    def attack(self):
        """Inicia la animación de ataque del personaje.
        """
        if not self.__is_jumping and not self.__is_shooting:
            attack_animation = self.__attack_r if self.__is_looking_right else self.__attack_l
            self.__actual_animation = attack_animation
            self.__initial_frame = 0
    
    def shoot(self):
        """Inicia la animación de disparo del personaje.
        """
        if not self.__is_jumping and not self.__is_attaking:
            proyectil = Proyectil(self.rect.x, self.rect.y, 5, 0, (0, 0, 255))
            self.__proyectiles.add(proyectil)
            shoot_animation = self.__shoot_r if self.__is_looking_right else self.__shoot_l
            self.__actual_animation = shoot_animation
            self.__initial_frame = 0
    
    def __set_borders_limits(self):
        """Limita el movimiento del jugador dentro de los bordes de la ventana.

        Returns:
            int: Cantidad de píxeles que puede moverse horizontalmente y verticalmente.
        """
        pixels_move_x = 0
        pixels_move_y = 0
        
        if self.__move_x > 0:
            pixels_move_x = self.__move_x if self.rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move_x = self.__move_x if self.rect.x > 0 else 0
        
        
        if self.__move_y > 0:
            pixels_move_y = self.__move_y if self.rect.y < ALTO_VENTANA - self.__actual_img_animation.get_height() else 0
        elif self.__move_y < 0:
            pixels_move_y = self.__move_y if self.rect.y > 0 else 0
        
        return pixels_move_x, pixels_move_y
    
    def check_collision_with_plataformas(self, plataformas):
        """Verifica la colisión del personaje con las plataformas.

        Args:
        - `plataformas` (List[Plataforma]): Lista de plataformas en el juego.

        Returns:
        - ([Plataforma]): La plataforma con la cual el personaje colisiona desde arriba, o None si no hay colisión.
        """
        colisiones = pg.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisiones:
            if self.rect.y < plataforma.rect.y:
                return plataforma
        return None

    def do_movement(self, delta_ms: int, plataformas):
        """Realiza el movimiento del personaje y maneja las colisiones con las plataformas.

        Args:
        - `delta_ms` (int): El tiempo transcurrido desde la última actualización en milisegundos.
        - `plataformas` (List[Plataforma]): Lista de plataformas en el juego.
        """
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            pixel_move_x, pixel_move_y = self.__set_borders_limits()
            self.rect.x += pixel_move_x
            self.rect.y += pixel_move_y
            
            plataforma_colisionada = self.check_collision_with_plataformas(plataformas)

            if plataforma_colisionada:
                # Ajustar la posición del jugador en la plataforma
                self.rect.y = plataforma_colisionada.rect.y - self.rect.height
                self.__is_jumping = False
                self.__move_y = 0
            # Parte relacionado a saltar
            if self.rect.y < 500:
                self.rect.y += self.__gravity

    def do_animation(self, delta_ms: int):
        """Realiza la animación del personaje.

        Args:
        - `delta_ms` (int): El tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                if self.__is_jumping:
                    self.__is_jumping = False
                    self.__move_y = 0
    
    def update(self, delta_ms: int, plataformas):
        """Actualiza el estado del personaje.

        Args:
        - `delta_ms` (int): El tiempo transcurrido desde la última actualización en milisegundos.
        - `plataformas` (List[Plataforma]): Lista de plataformas en el juego.
        """
        self.do_movement(delta_ms, plataformas)
        self.do_animation(delta_ms)
        
        for proyectil in self.__proyectiles:
            proyectil.update()
            # Verificar colisión con plataformas
            #colisiones = pg.sprite.spritecollide(proyectil, plataformas, True)
            #if colisiones:
            #    proyectil.kill()
    
    def draw(self, screen: pg.surface.Surface):
        """Dibuja el personaje en la pantalla.

        Args:
        - screen (pg.surface.Surface): Superficie de la pantalla en la que se dibujará el personaje.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.rect)
            
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)
    
    def handle_events(self, events):
        """Maneja los eventos del juego, respondiendo a las teclas presionadas o liberadas.

        Args:
            events (list): Una lista de eventos pygame a ser manejados.
        """
        for event in events:
            if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.jump(True)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.jump(False)
    
    def handle_key_input(self, keys, delta_ms):
        """Maneja la entrada del teclado para el personaje.

        Args:
            keys (dict): Un diccionario que representa el estado de las teclas presionadas.
            delta_ms (int): El tiempo transcurrido desde la última actualización en milisegundos.
        """
        if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.walk('Right')
        elif keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.walk('Left')
        else:
            self.stay()
        
        if keys[pg.K_SPACE]:
            if((self.__tiempo_transcurrido - self.__tiempo_last_jump) > self.__interval_time_jump):
                self.jump(True)
                self.__tiempo_last_jump = self.__tiempo_transcurrido
        elif keys[pg.K_a] and not keys[pg.K_t] and not keys[pg.K_SPACE]:
            self.shoot()
        elif keys[pg.K_t] and not keys[pg.K_a] and not keys[pg.K_SPACE]:
            self.attack()