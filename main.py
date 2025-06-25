import numpy as np
from datetime import date

class Gimnasio:
    """_summary_
    Clase que representa un gimnasio, contiene información básica y métodos para gestionar clientes, membresías, entrenadores y sesiones especiales.
    
    Atributos:
        __nombre (str): Nombre del Gimnasio.
        __direccion (str): Dirección del Gimnasio.
        __telefono (int): Número de teléfono del Gimnasio.
        __correo_electronico (str): Correo electrónico de contacto del Gimnasio.
        __efectivo (float, optional): Dinero en efectivo del Gimnasio. Defaults to 0.
        __numero_clientes (int): Contador de clientes registrados.
        __historia_clientes (int): Contador de clientes históricos.
        __clientes (np.ndarray): Array que almacena los clientes registrados.
        __membresias (np.ndarray): Array que almacena las membresías registradas.
        __entrenadores (np.ndarray): Array que almacena los entrenadores registrados.
        __sesiones (np.ndarray): Array que almacena las sesiones especiales programadas.
        
        Notas:
        - Necesitaremos un contador para membresias y para entrenadores?
    """    
    def __init__(self, nombre: str, direccion: str, telefono: int, correo: str, efectivo: float = 0):   
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.__correo_electronico = correo
        self.__efectivo = efectivo

        self.__numero_clientes = 0
        self.__historia_clientes = 0
        self.__clientes = np.full(50, None, dtype=object)
        self.__membresias = np.full(50, None, dtype=object)
        self.__entrenadores = np.full(5, None, dtype=object)
        self.__sesiones = np.full(10, None,dtype=object)
        
    def get(self):
        return self.__clientes, self.__membresias, self.__entrenadores, self.__sesiones

    def ver_inf(self):
        """_summary_
            Imprime el nombre y telefono de contacto del gimnasio
        """        
        print(f"Gimnasio {self.__nombre}, Tel: {self.__telefono},\nCorreo: {self.__correo_electronico}, nos encontramos ubicados en {self.__direccion}")

    def registrar_cliente(self, cliente):
        nuevo_cliente = Cliente()

    def consultar_membresia(self, id_cliente):
        pass

    def registrar_entrada(self, id_cliente):
        # lógica para registrar entrada de un cliente
        pass

    def visualizar_membresias(self):
        pass

    def analisis_financiero(self):
        # lógica de análisis
        pass

    def reporte_diario(self):
        # generar un resumen del día
        pass

    def informe_entrada(self):
        # reporte de entradas diarias
        pass

# ==== CLIENTES Y MEMBRESÍA ====

class Cliente:
    """
    Clase que representa un cliente del gimnasio, contiene información personal y métodos para gestionar membresías y sesiones especiales.
    
    Atributos:
        __id_cliente (int): Identificador único del cliente.
        __nombre (str): Nombre completo del cliente.
        __documento_identidad (int): Documento de identidad del cliente.
        __telefono (int, optional): Número de teléfono del cliente. Defaults to None.
        __fecha_registro (str): Fecha de registro del cliente en el gimnasio.
        __id_membresia (Membresia, optional): Ideantificador unico de la membresía asociada al cliente. Defaults to None.
        __sesion_especial (SesionEspecial, optional): Sesión especial solicitada por el cliente. Defaults to None.
    """
    def __init__(self, id_cliente: int, nombre: str, documento: int, fecha_registro: str, telefono: int = None):   
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__documento_identidad = documento
        self.__telefono = telefono
        self.__fecha_registro = fecha_registro

        self.__id_membresia = None
        self.__sesion_especial = None # Es necesario?

    def adquirir_membresia(self):
        pass

    def pago_ingreso_unico(self):
        pass

    def pagar_membresia(self):
        pass

    def solicitar_sesion(self):
        pass

class Membresia:
    """_summary_
    Clase que representa una membresía de gimnasio, contiene información sobre el estado, fechas y métodos para gestionar la membresía.
    
    Atributos:
        __id_membresia (int): Identificador único de la membresía.
        __estado (str, optional): Estado de la membresía (Activa, Debe). Defaults to "Activa".
        __fecha_inicio (str): Fecha de inicio de la membresía.
        __fecha_fin (str): Fecha de finalización de la membresía.
    """
    def __init__(self, id_membresia: int, fecha_inicio: str, fecha_fin: str, estado: str = "Activa"):
        self.__id_membresia = id_membresia
        self.__estado = estado
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin

    def calcular_dias_restantes(self):
        return (self.fecha_fin - date.today()).days

# ==== ENTRENADORES Y SESIONES ====

class Entrenador:
    """_summary_
    Clase que representa un entrenador del gimnasio, contiene información personal y métodos para asignar sesiones y consultar disponibilidad.
    
    Atributos:
        __id_entrenador (int): Identificador único del entrenador.
        __nombre (str): Nombre del entrenador.
        __telefono (int, optional): Número de teléfono del entrenador. Defaults to None.
        __especialidad (set): Especialidades del entrenador (Boxeo, Yoga, Aeróbicos).
    """
    def __init__(self, id_entrenador: int, nombre: str, especialidad: set, telefono: int = None):
        self.__id_entrenador = id_entrenador
        self.__nombre = nombre
        self.__telefono = telefono
        self.__especialidad = especialidad


class SesionEspecial:
    """
    Clase que representa una sesión especial del gimnasio, contiene información sobre el entrenador, fecha, cupos y métodos para gestionar inscripciones.
    
    Atributos:
        __id_entrenador (int): Identificador unico del entrenador que dirige la sesión.
        __fecha (str): Fecha de la sesión especial.
        __maximo_cupos (int, optional): Numero maximo de cupos. Defaults to 25.
        __cupos (int): Número actual de cupos ocupados.
        __inscritos (np.ndarray): Array que almacena los clientes inscritos en la sesión.
    """
    def __init__(self, id_entrenador: int, fecha: str, maximo_cupos: int = 25):
        self.__id_entrenador = id_entrenador
        self.__cupos = 0
        self.__fecha = fecha
        self.__maximo_cupos = maximo_cupos
        self.__inscritos = np.full(maximo_cupos, None, dtype=object)



Gym = Gimnasio("Body Force","Barrio Candelilla", 3001234545, "body@force.com", 45000)
Gym.ver_inf()
print(Gym.get())


