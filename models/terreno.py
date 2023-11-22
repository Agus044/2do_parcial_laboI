import pygame as pg

class Plataforma:
    def __init__(self, coord_x, coord_y, ancho, alto, image_path) -> None:
        self.rect = pg.Rect(coord_x, coord_y, ancho, alto)
        self.imagen = None
        if image_path:
            self.cargar_imagen(image_path)
    
    def cargar_imagen(self, image_path):
        self.imagen = pg.image.load(image_path)
        self.imagen = pg.transform.scale(self.imagen, (self.rect.width, self.rect.height))
    
    def draw(self, screen):
        pg.draw.rect(screen, (0, 255, 0), self.rect)