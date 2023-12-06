import pygame as pg

class Proyectil(pg.sprite.Sprite):
    def __init__(self, x, y, velocidad_x, velocidad_y, color):
        """Inicializa un objeto proyectil.

        Args:
            x (int): coordenada x inicial del proyectil
            y (int): coordenada y inicial del proyectil
            velocidad_x (int): Velocidad x inicial del proyectil
            velocidad_y (int): Velocidad y inicial del proyectil
            color (tuple): Color que tendra el proyectil
        """
        super().__init__()

        self.image = pg.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y

    def update(self):
        """Actualiza el estado del proyectil.
        """
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y