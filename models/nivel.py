import json
import pygame
from player import Personaje
from terreno import Plataforma
from caja import Caja
from enemigo import Enemigo

def cargar_nivel(nombre_nivel):
    """Carga un nivel especificado por su nombre.

    Args:
        nombre_nivel (str): El nombre del nivel que se desea cargar.

    Returns:
        tuple: Una tupla que contiene un objeto Personaje, un grupo de plataformas (Plataforma),
        un grupo de cajas (Caja), y la ruta de la imagen de fondo.
    """
    with open(nombre_nivel, "r") as archivo:
        configuracion = json.load(archivo)

    fondo = configuracion.get("background", "")
    
    config_personaje = configuracion.get("personaje", {})
    anakin = Personaje(config_personaje.get("x", 0), config_personaje.get("y", 0),
                    config_personaje.get("frame_rate", 100), config_personaje.get("speed_walk", 20))

    config_plataformas = configuracion.get("plataformas", [])
    plataformas = pygame.sprite.Group([Plataforma(p["x"], p["y"], p["ancho"], p["alto"], p["imagen"]) for p in config_plataformas])

    config_cajas = configuracion.get("cajas", [])
    cajas = pygame.sprite.Group([Caja(c["x"], c["y"], c["imagen"], puntos=10) for c in config_cajas])
    
    config_enemigos = configuracion.get("enemigos", [])
    enemigos = pygame.sprite.Group([Enemigo(e["enemie_type"], e["x"], e["y"]) for e in config_enemigos])
    
    return anakin, plataformas, cajas, fondo, enemigos