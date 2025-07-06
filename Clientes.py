import numpy as np
from datetime import date

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
        
    Notas:
        - Pensar si es necesario el atributo __sesion_especial, ya que podría ser redundante si se gestiona desde la clase SesionEspecial.
        - Pensar si Guardaremos el nombre completo o solo el nombre.
    """
    def __init__(self, id_cliente: int, nombre: str, documento: str, fecha_registro: str, telefono: str = None):   
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__documento = documento
        self.__telefono = telefono
        self.__fecha_registro = fecha_registro

        self.__id_membresia = None
        self.__sesiones_especiales = [] # Pendiente
        
    # Métodos de acceso
    
    def get_id_c(self):
        return self.__id_cliente
    
    def get_nombre_c(self):
        return self.__nombre
    
    def get_documento_c(self):
        return self.__documento
    
    def get_telefono_c(self):
        return self.__telefono
    
    def get_fecha_registro_c(self):
        return self.__fecha_registro
    
    def get_id_membresia(self):
        return self.__id_membresia
    
    # Métodos

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
        
    # Métodos de acceso
    
    def get_id_m(self):
        return self.__id_membresia
    
    def get_estado_m(self):
        return self.__estado
    
    def get_fecha_inicio_m(self):
        return self.__fecha_inicio
    
    def get_fecha_fin_m(self):
        return self.__fecha_fin
    
    # Métodos

    def calcular_dias_restantes(self):
        return (self.fecha_fin - date.today()).days