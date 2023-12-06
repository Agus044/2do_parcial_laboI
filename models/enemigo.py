import pygame as pg
import random
from proyectil import Proyectil
from auxiliar import SurfaceManager as sf
from constantes import *

class Enemigo(pg.sprite.Sprite):
    def __init__(self, enemie_type: int, coord_x, coord_y, speed_walk: int = 6, frame_rate: int = 70, shoot_delay: int = 2000, gravity = 16) -> None:
        super().__init__()
        if enemie_type == 1:
            self.walk_r = sf.get_surface_from_spritesheet("./assets/enemie1/Iddle/enemie1_iddle.png", 9, 1)
            self.walk_l = sf.get_surface_from_spritesheet("./assets/enemie1/Iddle/enemie1_iddle.png", 9, 1, flip=True)
            self.shoot_r = sf.get_surface_from_spritesheet("./assets/enemie1/Shoot/enemie1_shoot.png", 8, 1)
            self.shoot_l = sf.get_surface_from_spritesheet("./assets/enemie1/Shoot/enemie1_shoot.png", 8, 1, flip=True)
            self.die_r = sf.get_surface_from_spritesheet("./assets/enemie1/Dead/enemie1_dead.png", 8, 1)
            self.die_l = sf.get_surface_from_spritesheet("./assets/enemie1/Dead/enemie1_dead.png", 8, 1, flip=True)
        elif enemie_type == 2:
            self.walk_r = sf.get_surface_from_spritesheet("./assets/enemie2/Iddle/enemie2_iddle.png", 8, 1)
            self.walk_l = sf.get_surface_from_spritesheet("./assets/enemie2/Iddle/enemie2_iddle.png", 8, 1, flip=True)
            self.shoot_r = sf.get_surface_from_spritesheet("./assets/enemie2/Shoot/enemie2_shoot.png", 6, 1)
            self.shoot_l = sf.get_surface_from_spritesheet("./assets/enemie2/Shoot/enemie2_shoot.png", 6, 1, flip=True)
            self.die_r = sf.get_surface_from_spritesheet("./assets/enemie2/Dead/enemie2_dead.png", 8, 1)
            self.die_l = sf.get_surface_from_spritesheet("./assets/enemie2/Dead/enemie2_dead.png", 8, 1, flip=True)

        self.speed_walk = speed_walk
        self.initial_direction = random.choice([-1, 1])  # -1 para izquierda, 1 para derecha
        self.direction = self.initial_direction
        self.random_walk_time = 0
        self.change_direction_interval = random.randint(2000, 5000)  # Cambia la dirección cada 2-5 segundos
        self.frame_rate = frame_rate
        self.shoot_delay = shoot_delay
        self.gravity = gravity
        self.shoot_time = 0
        self.initial_frame = 0
        self.actual_animation = self.walk_r
        self.image = self.actual_animation[self.initial_frame]
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.is_looking_right = True
        self.enemie_animation_time = 0
        self.enemie_move_time = 0
        self.proyectiles = pg.sprite.Group()

    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        """_summary_

        Args:
            move_x (_type_): _description_
            animation_list (list[pg.surface.Surface]): _description_
            look_r (bool): _description_
        """
        self.rect.x += move_x
        self.actual_animation = animation_list
        self.is_looking_right = look_r
        
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
    
    def __set_borders_limits(self):
        """Limita el movimiento del jugador dentro de los bordes de la ventana.

        Returns:
            int: Cantidad de píxeles que puede moverse horizontalmente y verticalmente.
        """
        pixels_move_x = 0
        
        if self.rect.x > 0:
            pixels_move_x = self.rect.x if self.rect.x < ANCHO_VENTANA - self.image.get_width() else 0
        elif self.rect.x < 0:
            pixels_move_x = self.rect.x if self.rect.x > 0 else 0
        
        return pixels_move_x
    
    def do_movement(self, delta_ms: int, plataformas):
        self.enemie_move_time += delta_ms
        self.random_walk_time += delta_ms

        if self.random_walk_time >= self.change_direction_interval:
            self.random_walk_time = 0
            self.direction = random.choice([-1, 1])  # Cambia la dirección aleatoriamente
            self.change_direction_interval = random.randint(2000, 5000)  # Establece un nuevo intervalo de cambio de dirección
        
        if self.enemie_move_time >= self.frame_rate:
            self.enemie_move_time = 0
            pixel_move_x = self.speed_walk * self.direction
            self.rect.x += pixel_move_x
            
            plataforma_colisionada = self.check_collision_with_plataformas(plataformas)

            if plataforma_colisionada:
                # Ajustar la posición del jugador en la plataforma
                self.rect.y = plataforma_colisionada.rect.y - self.rect.height
    
    def do_animation(self, delta_ms: int):
        """Realiza la animación del personaje.

        Args:
        - `delta_ms` (int): El tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.enemie_animation_time += delta_ms
        if self.enemie_animation_time >= self.frame_rate:
            self.enemie_animation_time = 0
            if self.initial_frame < len(self.actual_animation) - 1:
                self.initial_frame += 1
            else:
                self.initial_frame = 0
    
    def update(self, delta_ms: int, plataformas):
        self.shoot_time += delta_ms

        if self.shoot_time >= self.shoot_delay:
            self.shoot_time = 0
            self.shoot()
            
        self.do_movement(delta_ms, plataformas)
        self.do_animation(delta_ms)
            
        for proyectil in self.proyectiles:
            proyectil.update()

    def shoot(self):
        proyectil = Proyectil(self.rect.x, self.rect.y, -5, 0, (255, 0, 0))
        self.proyectiles.add(proyectil)
        shoot_animation = self.shoot_r if self.is_looking_right else self.shoot_l
        self.actual_animation = shoot_animation
        self.initial_frame = 0

    def draw(self, screen: pg.surface.Surface):
        """Dibuja el personaje en la pantalla.

        Args:
        - screen (pg.surface.Surface): Superficie de la pantalla en la que se dibujará el personaje.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.rect)
            
        self.actual_img_animation = self.actual_animation[self.initial_frame]
        screen.blit(self.actual_img_animation, self.rect)