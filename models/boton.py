import pygame

class Boton:
    def __init__(self, x, y, width, height, text, color, hover_color):
        """Inicializa un objeto Boton con las propiedades especificadas.

        Args:
            x (int): La coordenada x de la esquina superior izquierda del botón.
            y (int): La coordenada y de la esquina superior izquierda del botón.
            width (int): El ancho del botón.
            height (int): La altura del botón.
            text (str): El texto que se mostrará en el botón.
            color (tuple): El color del botón en formato RGB.
            hover_color (tuple): El color del botón al pasar el mouse sobre él en formato RGB.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen, font):
        """Dibuja el botón en la pantalla.

        Args:
            screen (pygame.Surface): La superficie de la pantalla en la que se dibujará el botón.
            font (pygame.font.Font): La fuente utilizada para el texto en el botón.
        """
        pygame.draw.rect(screen, self.hover_color if self.hovered else self.color, self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Maneja eventos del mouse para determinar si el mouse está sobre el botón.

        Args:
            event (pygame.event.Event): El evento pygame a ser manejado.
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)