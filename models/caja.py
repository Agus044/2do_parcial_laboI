import pygame as pg

class Caja(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, image_path: str) -> None:
        """Inicializa un objeto de tipo Caja.

        Args:
            coord_x (int): Coordenada x inicial de la caja.
            coord_y (int): Coordenada y inicial de la caja.
            image_path (str): Ruta de la imagen que se utilizará para la caja.
        """
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        
    def draw(self, screen):
        """Dibuja la caja en la pantalla.

        Args:
            screen (pg.Surface): Superficie de la pantalla donde se dibuja la caja.
        """
        screen.blit(self.image, self.rect)