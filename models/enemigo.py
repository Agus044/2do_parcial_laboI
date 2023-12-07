import pygame as pg
import random
from proyectil import Proyectil
from auxiliar import SurfaceManager as sf
from constantes import *

class Enemigo(pg.sprite.Sprite):
    def __init__(self, enemie_type: int, coord_x: int, coord_y: int, speed_walk: int = 3, frame_rate: int = 70, shoot_delay: int = 3000, gravity = 16) -> None:
        """_summary_
        
        Args:
            enemie_type (int): es el tipo de enemigo: 1 si es Battle droid, 2 si es Super Battle droid
            coord_x (int): _description_
            coord_y (int): _description_
            speed_walk (int): _description_. Defaults to 3.
            frame_rate (int): _description_. Defaults to 70.
            shoot_delay (int): _description_. Defaults to 5000.
            gravity (int): La fuerza de gravedad que afecta al enemigo. Defaults to 16.
        """
        super().__init__()
        if enemie_type == 1:
            self.walk_r = sf.get_surface_from_spritesheet("./assets/enemie1/Iddle/enemie1_iddle.png", 9, 1)
            self.walk_l = sf.get_surface_from_spritesheet("./assets/enemie1/Iddle/enemie1_iddle.png", 9, 1, flip=True)
            self.shoot_r = sf.get_surface_from_spritesheet("./assets/enemie1/Shoot/enemie1_shoot.png", 8, 1)
            self.shoot_l = sf.get_surface_from_spritesheet("./assets/enemie1/Shoot/enemie1_shoot.png", 8, 1, flip=True)
        elif enemie_type == 2:
            self.walk_r = sf.get_surface_from_spritesheet("./assets/enemie2/Iddle/enemie2_iddle.png", 8, 1)
            self.walk_l = sf.get_surface_from_spritesheet("./assets/enemie2/Iddle/enemie2_iddle.png", 8, 1, flip=True)
            self.shoot_r = sf.get_surface_from_spritesheet("./assets/enemie2/Shoot/enemie2_shoot.png", 6, 1)
            self.shoot_l = sf.get_surface_from_spritesheet("./assets/enemie2/Shoot/enemie2_shoot.png", 6, 1, flip=True)
        elif enemie_type == 3:
            self.walk_r = sf.get_surface_from_spritesheet("./assets/boss/boss_walk.png", 13, 1)
            self.walk_l = sf.get_surface_from_spritesheet("./assets/boss/boss_walk.png", 13, 1, flip=True)
            self.shoot_r = sf.get_surface_from_spritesheet("./assets/boss/boss_shoot.png", 12, 1)
            self.shoot_l = sf.get_surface_from_spritesheet("./assets/boss/boss_shoot.png", 12, 1, flip=True)
        
        self.speed_walk = speed_walk
        self.initial_direction = random.choice([-1, 1])  # -1 para izquierda, 1 para derecha
        self.direction = self.initial_direction
        self.random_walk_time = 0
        self.frame_rate = frame_rate
        self.shoot_delay = shoot_delay
        self.gravity = gravity
        self.shoot_time = 0
        self.shoot_delay_timer = 0
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
        self.enemie_shoot = pg.mixer.Sound("./assets/sounds/droid_blaster.wav")
    
    
    def check_collision_with_plataformas(self, plataformas):
        """Verifica la colisión del enemigocon las plataformas.
        
        Args:
        - `plataformas` (List[Plataforma]): Lista de plataformas en el juego.
        
        Returns:
        - ([Plataforma]): La plataforma con la cual el enemigo colisiona desde arriba, o None si no hay colisión.
        """
        colisiones = pg.sprite.spritecollide(self, plataformas, False)
        for plataforma in colisiones:
            if self.rect.y < plataforma.rect.y:
                return plataforma
        return None
    
    def do_movement(self, delta_ms: int, plataformas):
        """Realiza el movimiento del enemigo y maneja las colisiones
        con las plataformas.
        
        Args:
            delta_ms (int): El tiempo transcurrido desde la última actualización en milisegundos.
            plataformas (List[Plataforma]): Lista de plataformas en el juego.
        """
        
        self.enemie_move_time += delta_ms
        if self.enemie_move_time >= self.frame_rate:
            self.enemie_move_time = 0
        
        # Cambios en la dirección cuando alcanza los bordes
        if self.rect.x <= 0 or self.rect.x >= ANCHO_VENTANA - self.image.get_width():
            self.direction *= -1
            self.is_looking_right = not self.is_looking_right
            self.actual_animation = self.walk_r if self.is_looking_right else self.walk_l
        
        # Mover en la dirección actual
        self.rect.x = self.rect.x + self.speed_walk * self.direction
        
        plataforma_colisionada = self.check_collision_with_plataformas(plataformas)
        # Ajustar la posición del jugador en la plataforma
        if plataforma_colisionada:
            self.rect.y = plataforma_colisionada.rect.y - self.rect.height
            self.gravity = 0
        else:
            self.gravity = 16
        
        # Parte relacionada a saltar
        if self.rect.y < 500:
            self.rect.y += self.gravity
    
    def do_animation(self, delta_ms: int):
        """Realiza la animacion del enemigo.

        Args:
            delta_ms (int): El tiempo transcurrido desde la última actualización en milisegundos.
        """
        self.enemie_animation_time += delta_ms
        if self.enemie_animation_time >= self.frame_rate:
            self.enemie_animation_time = 0
            if self.initial_frame < len(self.actual_animation) - 1:
                self.initial_frame += 1
            else:
                self.initial_frame = 0
        self.image = self.actual_animation[self.initial_frame]
    
    def update(self, delta_ms: int, plataformas):
        """Actualiza el estado del enemigo

        Args:
            delta_ms (int): El tiempo transcurrido desde la última actualización en milisegundos.
            plataformas (List[Plataforma]): Lista de plataformas en el juego.
        """
        
        self.do_movement(delta_ms, plataformas)
        self.do_animation(delta_ms)
        
        self.shoot_delay_timer += delta_ms
        
        if self.shoot_delay_timer >= self.shoot_delay:
            self.shoot_time = 0
            self.shoot_delay_timer = 0
            self.shoot()
            self.enemie_shoot.play()
        
        for proyectil in self.proyectiles:
            proyectil.update()
    
    def shoot(self):
        """Inicializa la animacion de disparo del enemigo.
        """
        offset = 20 if self.is_looking_right else -20
        proyectil = Proyectil(self.rect.x + offset, self.rect.y, 5, 0, BLUE, self.is_looking_right)
        self.proyectiles.add(proyectil)
        shoot_animation = self.shoot_r if self.is_looking_right else self.shoot_l
        self.actual_animation = shoot_animation
        self.initial_frame = 0
    
    def draw(self, screen: pg.surface.Surface):
        """Dibuja el enemigo en la pantalla.
        Args:
            screen (pg.surface.Surface): Superficie de la pantalla en la que se dibujará el enemigo.
        """
        if DEBUG:
            pg.draw.rect(screen, 'red', self.rect)
            
        self.image = self.actual_animation[self.initial_frame]
        screen.blit(self.image, self.rect)
        
        for proyectil in self.proyectiles:
            proyectil.draw(screen)