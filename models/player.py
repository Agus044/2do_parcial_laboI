import pygame as pg
from auxiliar import SurfaceManager as sf
from constantes import *

class Personaje():
    def __init__(self, coord_x, coord_y, frame_rate = 100, speed_walk = 5, gravity = 10, jump = 20) -> None:
        """Inicializa un objeto Jugador.

        Args:
        - coord_x (int): Coordenada x inicial del jugador.
        - coord_y (int): Coordenada y inicial del jugador.
        - frame_rate (int): Tasa de cuadros por segundo para la animación (valor predeterminado: 100).
        - speed_walk (int): Velocidad de caminar del jugador (valor predeterminado: 5).
        - gravity (int): Gravedad aplicada al jugador durante el salto (valor predeterminado: 10).
        - jump (int): Altura del salto del jugador (valor predeterminado: 20).
        """
        
        self.__iddle_r = sf.get_surface_from_spritesheet("./assets/player/Iddle/player_idle.png", 5, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet('./assets/player/Iddle/player_idle.png', 5, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet('./assets/player/Walk/player_walk.png', 13, 1)
        self.__walk_l = sf.get_surface_from_spritesheet('./assets/player/Walk/player_walk.png', 13, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet('./assets/player/Jump/player_jump.png', 6, 1)
        self.__jump_l = sf.get_surface_from_spritesheet('./assets/player/Jump/player_jump.png', 6, 1, flip=True)
        self.__attack_physical_r = sf.get_surface_from_spritesheet("./assets/player/Attack/Melee/player_atk_melee.png", 10, 1)
        self.__attack_physical_l = sf.get_surface_from_spritesheet("./assets/player/Attack/Melee/player_atk_melee.png", 10, 1, flip=True)
        self.__shoot_r = sf.get_surface_from_spritesheet("./assets/player/Attack/Shot/player_shot.png", 28, 2)
        self.__shoot_l = sf.get_surface_from_spritesheet("./assets/player/Attack/Shot/player_shot.png", 28, 2, flip=True)
        
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__initial_frame = 0
        self.__vida = 3
        
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__frame_rate = frame_rate
        self.__gravity = gravity
        self.__jump = jump
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x = coord_x
        self.__rect.y = coord_y
        
        self.__is_jumping = False
        self.__is_fall = False
        self.__is_looking_right = True
        self.__laser_sword = False
        self.__is_shoot = False
    
    def __set_x_animations_preset(self, move_x: int, animation_list: list[pg.surface.Surface], look_r: bool):
        """Configura las propiedades relacionadas con la animación horizontal del jugador.

        Args:
            - move_x (int): Movimiento horizontal del jugador.
            - animation_list (list[pg.surface.Surface]): Lista de superficies de animación.
            - look_r (bool): Dirección en la que mira el jugador (True si mira a la derecha, False si mira a la izquierda).
        """
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        
    
    def __set_y_animations_preset(self):
        """Configura las propiedades relacionadas con la animación vertical del jugador para el salto.
        """
        self.__move_y = -self.__jump
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
    
    def jump(self, jumping=True):
        """Inicia o detiene la animación de salto del jugador.

        Args:
            jumping (bool): True para iniciar el salto, False para detenerlo.
        """
        if jumping and not self.__is_jumping and self.__is_fall == False:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()
    
    def do_attack(self, attack=True):
        """Realiza el ataque del jugador."""
        self.__laser_sword = attack
        if(attack == True and self.__is_jumping == False and self.__is_fall == False):
            if(self.__actual_animation != self.__attack_physical_r and self.__actual_animation != self.__attack_physical_l):
                self.__initial_frame = 0
                if(self.__is_looking_right == True):
                    self.__actual_animation = self.__attack_physical_r
                else:
                    self.__actual_animation = self.__attack_physical_l
    
    def shoot(self, shoot=True):
        """Realiza el disparo del jugador
        """
        self.__is_shoot = shoot
        if(shoot == True and self.__is_jumping == False and self.__is_fall == False):
            if(self.__actual_animation != self.__shoot_r and self.__actual_animation != self.__shoot_l):
                self.__initial_frame = 0
                if(self.__is_looking_right == True):
                    self.__actual_animation = self.__shoot_r
                else:
                    self.__actual_animation = self.__shoot_l
    
    def __set_borders_limits(self) -> int:
        """Limita el movimiento del jugador dentro de los bordes de la ventana.

        Returns:
            int: Cantidad de píxeles que puede moverse horizontalmente.
        """
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move


    def do_movement(self, delta_ms: int):
        """Realiza el movimiento del jugador.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__rect.y += self.__move_y
            # Parte relacionado a saltar
            if self.__rect.y < 300:
                self.__rect.y += self.__gravity

    def do_animation(self, delta_ms: int):
        """Realiza la animación del jugador.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                print("Animacion normal:", self.__initial_frame)
                self.__initial_frame += 1
            else:
                print("Reinicio de animacion normal")
                self.__initial_frame = 0
    
    def update(self, delta_ms: int):
        """Actualiza el estado del jugador.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        
    
    def draw(self, screen: pg.surface.Surface):
        """Dibuja al jugador en la pantalla.

        Args:
            screen (pg.surface.Surface): Superficie de la pantalla donde se dibuja al jugador.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)