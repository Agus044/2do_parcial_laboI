import json
from player import Personaje
from terreno import Plataforma
from caja import Caja

def cargar_niveles_json(ruta_archivo):
    """_summary_

    Args:
        ruta_archivo (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(ruta_archivo, "r") as archivo:
        configuracion = json.load(archivo)
    
    fondo = configuracion.get("background", "")
    config_personaje = configuracion.get("personaje", {})
    anakin = Personaje(config_personaje.get("x", 0), config_personaje.get("y", 0),
                    config_personaje.get("frame_rate", 100), config_personaje.get("speed_walk", 20))
    
    config_plataformas = configuracion.get("plataformas", [])
    plataformas = [Plataforma(p["x"], p["y"], p["ancho"], p["alto"], p["imagen"]) for p in config_plataformas]
    
    config_cajas = configuracion.get("cajas", [])
    cajas = [Caja(c["x"], c["y"], c["imagen"]) for c in config_cajas]
    
    return anakin, plataformas, cajas, fondo