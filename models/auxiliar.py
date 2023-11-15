import pygame as pg

class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pg.surface.Surface]:
        """Crea y devuelve una lista de superficies a partir de una hoja de sprites.

        Args:
            - img_path (str): Ruta de la imagen de la hoja de sprites.
            - cols (int): Número de columnas en la hoja de sprites.
            - rows (int): Número de filas en la hoja de sprites.
            - step (int): Número de columnas que salta para cada frame (valor predeterminado: 1).
            - flip (bool): Si se deben voltear horizontalmente las superficies (valor predeterminado: False).

        Returns:
            list[pg.surface.Surface]: Lista de superficies individuales de la hoja de sprites.
        """
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width() / cols)
        frame_height = int(surface_img.get_height() / rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list