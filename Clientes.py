import numpy as np
from datetime import date
import Utils as u

# ==== CLIENTES Y MEMBRESÍA ====

class Cliente:
    """
    Clase que representa un cliente del gimnasio, contiene información personal y métodos para gestionar membresías y sesiones especiales.
    
    Atributos:
        __id_cliente (str): Identificador único del cliente.
        __nombre (str): Nombre completo del cliente.
        __documento_identidad (int): Documento de identidad del cliente.
        __telefono (str, optional): Número de teléfono del cliente. Defaults to None.
        __fecha_registro (str): Fecha de registro del cliente en el gimnasio.
        __id_membresia (str, optional): Ideantificador unico de la membresía asociada al cliente. Defaults to None.
        __sesion_especial (SesionEspecial, optional): Sesión especial solicitada por el cliente. Defaults to None.
        
    Notas:
        - Pensar si es necesario el atributo __sesion_especial, ya que podría ser redundante si se gestiona desde la clase SesionEspecial.
        - Pensar si Guardaremos el nombre completo o solo el nombre.
    """
    def __init__(self, id_cliente: str, nombre: str, documento: str, fecha_registro: str, telefono: str = None):   
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__documento = documento
        self.__telefono = telefono
        self.__fecha_registro = fecha_registro

        self.__id_membresia = None
        self.__sesiones_especiales = [] # Pendiente. Pensar si es necesario este atributo, ya que podría ser redundante si se gestiona desde la clase SesionEspecial.
        
    # Métodos de acceso y modificación
    
    def get_id_cliente(self):
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
    
    def get_sesiones_especiales(self):
        return self.__sesiones_especiales
    
    def set_id_membresia(self, id_membresia):
        self.__id_membresia = id_membresia
    
    # Métodos para gestionar sesiones especiales
    def agregar_sesion(self, id_sesion):
        """
        Agrega una sesión especial a la lista del cliente.
        
        Args:
            id_sesion (int): ID de la sesión especial
        """
        if id_sesion not in self.__sesiones_especiales:
            self.__sesiones_especiales.append(id_sesion)
            print(f"Sesión {id_sesion} agregada al cliente {self.__nombre}")
        else:
            print(f"El cliente {self.__nombre} ya está inscrito en la sesión {id_sesion}.")
    
    def remover_sesion(self, id_sesion):
        """
        Remueve una sesión especial de la lista del cliente.
        
        Args:
            id_sesion (int): ID de la sesión especial
        """
        if id_sesion in self.__sesiones_especiales:
            self.__sesiones_especiales.remove(id_sesion)
            print(f"Sesión {id_sesion} removida del cliente {self.__nombre}")
    
    def mostrar_sesiones_inscritas(self):
        """Muestra todas las sesiones en las que está inscrito el cliente"""
        if not self.__sesiones_especiales:
            print(f"El cliente {self.__nombre} no tiene sesiones especiales inscritas.")
        else:
            print(f"\n=== Sesiones de {self.__nombre} ===")
            for id_sesion in self.__sesiones_especiales:
                print(f"  - Sesión ID: {id_sesion}")
            print("="*30)
    
    # Métodos

    def pago_ingreso_unico(self):
        pass

    def solicitar_sesion(self):
        pass

class Membresia:
    """_summary_
    Clase que representa una membresía de gimnasio, contiene información sobre el estado, fechas y métodos para gestionar la membresía.
    
    Atributos:
        __id_membresia (str): Identificador único de la membresía.
        __pago (bool): Indica si la membresía ha sido pagada o no. Defaults to False.
        __fecha_inicio (str): Fecha de inicio de la membresía.
        __fecha_fin (str): Fecha de finalización de la membresía.
    """
    def __init__(self, id_membresia: str, fecha_inicio: str, fecha_fin: str, pago: bool = False):
        self.__id_membresia = id_membresia
        self.__pago = pago
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        
    # Métodos de acceso y modificación
    
    def get_id_membresia(self):
        return self.__id_membresia
    
    def get_pago_m(self):
        return self.__pago
    
    def get_fecha_inicio_m(self):
        return self.__fecha_inicio
    
    def get_fecha_fin_m(self):
        return self.__fecha_fin
    
    def set_pago(self, estado: bool):
        self.__pago = estado
    
    # Métodos

    def calcular_dias_restantes(self):
        return (self.fecha_fin - date.today()).days
