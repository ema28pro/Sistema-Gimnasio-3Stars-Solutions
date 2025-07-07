import numpy as np
from datetime import date

# ==== ENTRENADORES Y SESIONES ====

class Entrenador:
    """_summary_
    Clase que representa un entrenador del gimnasio, contiene información personal y métodos para asignar sesiones y consultar disponibilidad.
    
    Atributos:
        __id_entrenador (str): Identificador único del entrenador.
        __nombre (str): Nombre del entrenador.
        __telefono (int, optional): Número de teléfono del entrenador. Defaults to None.
        __especialidad (set): Especialidades del entrenador (Boxeo, Yoga, Aeróbicos).
    """
    def __init__(self, id_entrenador: str, nombre: str, especialidad: set, telefono: str = None):
        self.__id_entrenador = id_entrenador
        self.__nombre = nombre
        self.__telefono = telefono
        self.__especialidad = especialidad


class SesionEspecial:
    """
    Clase que representa una sesión especial del gimnasio, contiene información sobre el entrenador, fecha, cupos y métodos para gestionar inscripciones.
    
    Atributos:
        __id_sesion (str): Identificador único de la sesión especial.
        __id_entrenador (str): Identificador unico del entrenador que dirige la sesión.
        __fecha (str): Fecha de la sesión especial.
        __maximo_cupos (int, optional): Numero maximo de cupos. Defaults to 25.
        __cupos (int): Número actual de cupos ocupados.
        __inscritos (np.ndarray): Array que almacena los clientes inscritos en la sesión.
    """
    def __init__(self, id_sesion: str, id_entrenador: str, fecha: str, maximo_cupos: int = 25):
        self.__id_sesion = id_sesion
        self.__id_entrenador = id_entrenador
        self.__cupos = 0
        self.__fecha = fecha
        self.__maximo_cupos = maximo_cupos
        self.__inscritos = np.full(maximo_cupos, None, dtype=object)