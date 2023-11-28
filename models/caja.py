import pygame as pg

class Caja(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, image_path) -> None:
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)