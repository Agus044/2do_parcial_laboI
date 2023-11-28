import pygame as pg
import random
from auxiliar import SurfaceManager as sf
from constantes import *

class Enemigo():
    def __init__(self, enemie_type: int, coord_x, coord_y, speed_walk: int, speed: int, frame_rate = 100) -> None:
        
        if enemie_type == 1:
            self.__walk_r = sf.get_surface_from_spritesheet("./assets/enemie1/Iddle/enemie1_iddle.png", 9, 1)
            self.__walk_l = sf.get_surface_from_spritesheet("./assets/enemie1/Iddle/enemie1_iddle.png", 9, 1, flip=True)
            self.__stay_r = sf.get_surface_from_spritesheet("./assets/enemie1/Walk/enemie1_walk.png", 6, 1)
            self.__stay_l = sf.get_surface_from_spritesheet("./assets/enemie1/Walk/enemie1_walk.png", 6, 1, flip=True)
            self.__attack_r = sf.get_surface_from_spritesheet("./assets/enemie1/Shoot/enemie1_shoot.png", 8, 1)
            self.__attack_l = sf.get_surface_from_spritesheet("./assets/enemie1/Shoot/enemie1_shoot.png", 8, 1, flip=True)
            self.__die_r = sf.get_surface_from_spritesheet("./assets/enemie1/Dead/enemie1_dead.png", 8, 1)
            self.__die_l = sf.get_surface_from_spritesheet("./assets/enemie1/Dead/enemie1_dead.png", 8, 1, flip=True)
        elif enemie_type == 2:
            self.__walk_r = sf.get_surface_from_spritesheet("./assets/enemie2/Iddle/enemie2_iddle.png", 8, 1)
            self.__walk_l = sf.get_surface_from_spritesheet("./assets/enemie2/Iddle/enemie2_iddle.png", 8, 1, flip=True)
            self.__stay_r = sf.get_surface_from_spritesheet("./assets/enemie2/Walk/enemie2_walk.png", 5, 1)
            self.__stay_l = sf.get_surface_from_spritesheet("./assets/enemie2/Walk/enemie2_walk.png", 5, 1, flip=True)
            self.__attack_r = sf.get_surface_from_spritesheet("./assets/enemie2/Shoot/enemie2_shoot.png", 6, 1)
            self.__attack_l = sf.get_surface_from_spritesheet("./assets/enemie2/Shoot/enemie2_shoot.png", 6, 1, flip=True)
            self.__die_r = sf.get_surface_from_spritesheet("./assets/enemie2/Dead/enemie2_dead.png", 8, 1)
            self.__die_l = sf.get_surface_from_spritesheet("./assets/enemie2/Dead/enemie2_dead.png", 8, 1, flip=True)
        
        self.__enemie_animation_time = 0
        self.__enemie_move_time = 0
        self.__initial_frame = 0
        self.__move_x = coord_x
        self.__speed_walk = speed_walk
        self.__frame_rate = frame_rate
        self.__speed = speed
        self.__actual_animation = self.__stay_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
    
    def __update_direction(self):
        """Actualiza la dirección del enemigo si llega a los bordes de la pantalla.
        """
        if self.__rect.x <= 0 or self.__rect.x >= ANCHO_VENTANA - self.__actual_img_animation.get_width():
            self.__actual_animation = self.__walk_l
        
    def __set_borders_limits(self) -> int:
        """Limita el movimiento del enemigo dentro de los bordes de la ventana.

        Returns:
            int: Cantidad de píxeles que puede moverse horizontalmente.
        """
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__speed if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = -self.__speed if self.__rect.x > 0 else 0
        return pixels_move

    def do_movement(self, delta_ms: int):
        """Realiza el movimiento del enemigo.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.__enemie_move_time += delta_ms
        if self.__enemie_move_time >= self.__frame_rate:
            self.__enemie_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__update_direction()

    def do_animation(self, delta_ms: int):
        """Realiza la animación del enemigo.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
        """
        if self.__move_x != 0:  # Solo cambia la animación si el enemigo se está moviendo
            self.__enemie_animation_time += delta_ms
            if self.__enemie_animation_time >= self.__frame_rate:
                self.__enemie_animation_time = 0
                if self.__initial_frame < len(self.__actual_animation) - 1:
                    self.__initial_frame += 1
                else:
                    self.__initial_frame = 0

    def update(self, delta_ms: int):
        """Actualiza el estado del enemigo.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)

    def draw(self, screen: pg.surface.Surface):
        """Dibuja al enemigo en la pantalla.

        Args:
            screen (pg.surface.Surface): Superficie de la pantalla donde se dibuja al enemigo.
        """
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)