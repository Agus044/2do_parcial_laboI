import sqlite3
from constantes import DB_FILE

def crear_tabla_ranking():
    """Crea la tabla de ranking en la base de datos si no existe.
    Esta función se encarga de conectar a la base de datos especificada en la constante `DB_FILE`,
    crea la tabla 'ranking' si aún no existe y luego cierra la conexión.
    """
    try:
        # Conectar a la base de datos (creará el archivo si no existe)
        conexion = sqlite3.connect(DB_FILE)
        cursor = conexion.cursor()
        # Crear la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jugador TEXT,
                puntuacion INTEGER
            )
        ''')
        # Confirmar y cerrar la conexión
        conexion.commit()
    except sqlite3.Error as e:
        print("Error al crear la tabla de ranking:", e)
    finally:
        if conexion:
            conexion.close()

def agregar_puntuacion(jugador, puntuacion):
    """Agrega una nueva puntuación de un jugador a la tabla de ranking.
    Conecta a la base de datos especificada en la constante `DB_FILE`, inserta una nueva fila
    en la tabla 'ranking' con el nombre del jugador y su puntuación, y luego cierra la conexión
    
    Args:
        jugador (str): El nombre del jugador
        puntuacion (int): La puntuacion que se desea agregar
    """
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect(DB_FILE)
        cursor = conexion.cursor()
        # Insertar una nueva fila en la tabla de ranking
        cursor.execute("INSERT INTO ranking (jugador, puntuacion) VALUES (?, ?)", (jugador, puntuacion))
        # Confirmar y cerrar la conexión
        conexion.commit()
    except sqlite3.Error as e:
        print("Error al agregar puntuación:", e)
    finally:
        if conexion:
            conexion.close()

def obtener_ranking():
    """Obtiene las mejores puntuaciones de la tabla de ranking.
    Conecta a la base de datos especificada en la constante `DB_FILE`, ejecuta una consulta SQL
    para obtener las mejores puntuaciones ordenadas de mayor a menor, y luego cierra la conexión.

    Returns:
        list: Una lista de tuplas, donde cada tupla contiene el nombre del jugador y su puntuación.
            Las tuplas están ordenadas de mayor a menor puntuación.
    """
    try:
        # Conectar a la base de datos y obtener las mejores puntuaciones
        conexion = sqlite3.connect(DB_FILE)
        cursor = conexion.cursor()
        cursor.execute("SELECT jugador, puntuacion FROM ranking ORDER BY puntuacion DESC LIMIT 10")
        filas = cursor.fetchall()
        return filas
    except sqlite3.Error as e:
        print("Error al obtener el ranking:", e)
        return []
    finally:
        if conexion:
            conexion.close()