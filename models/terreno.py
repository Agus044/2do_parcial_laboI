import pygame as pg

class Plataforma(pg.sprite.Sprite):
    def __init__(self, coord_x: int, coord_y: int, ancho: int, alto: int, image_path: str) -> None:
        """Inicializa un objeto de plataforma.

        Args:
            coord_x (int): Coordenada x inicial de la plataforma.
            coord_y (int): Coordenada y inicial de la plataforma.
            ancho (int): Ancho de la plataforma.
            alto (int): Alto de la plataforma.
            image_path (str): Ruta de la imagen de la plataforma. 
        """
        super().__init__()
        self.rect = pg.Rect(coord_x, coord_y, ancho, alto)
        self.image = image_path
        if image_path:
            self.cargar_imagen(self.image)
    
    def cargar_imagen(self, image_path: str):
        """Carga una imagen desde la ruta especificada
        y la escala para ajustarse al tamaño de la plataforma.

        Args:
            image_path (str): Ruta de la imagen.
        """
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
    
    def draw(self, screen):
        """Dibuja la plataforma en la pantalla.
        Args:
            screen (pg.Surface): Superficie de la pantalla donde se dibuja la plataforma.
        """
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pg.draw.rect(screen, (0, 255, 0), self.rect)