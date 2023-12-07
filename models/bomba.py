import pygame as pg

class Bomba(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, image_path: str) -> None:
        """Inicializa un objeto de tipo Bomba.

        Args:
            coord_x (int): Coordenada x inicial de la bomba.
            coord_y (int): Coordenada y inicial de la bomba.
            image_path (str): Ruta de la imagen que se utilizará para la bomba.
        """
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
    
    def desaparecer(self):
        """Eliminara la bomba del grupo a donde pertenece.
        """
        self.kill()
    
    def draw(self, screen):
        """Dibuja la bomba en la pantalla.

        Args:
            screen (pg.Surface): Superficie de la pantalla donde se dibuja la bomba.
        """
        screen.blit(self.image, self.rect)