from datetime import date, timedelta, datetime
import Utils as ut
from Utils import PRECIO_MEMBRESIA


# ==== CLIENTES Y MEMBRESÍA ====

class Membresia:
    """_summary_
    Clase que representa una membresía de gimnasio, contiene información sobre el estado, fechas y métodos para gestionar la membresía.
    
    Atributos:
        __pago (bool): Indica si la membresía ha sido pagada o no. Defaults to False.
        __fecha_inicio (str): Fecha de inicio de la membresía.
        __fecha_fin (str): Fecha de finalización de la membresía.
    """
    def __init__(self, fecha_inicio, fecha_fin, pago: bool = False):
        self.__pago = pago
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        
    # Métodos de acceso y modificación
    
    def get_pago_m(self):
        return self.__pago
    
    def get_fecha_inicio_m(self):
        # Retornar como string
        return self.__fecha_inicio.strftime("%Y-%m-%d")
    
    def get_fecha_fin_m(self):
        # Retornar como string
        return self.__fecha_fin.strftime("%Y-%m-%d")
    
    def set_pago_m(self, estado: bool):
        self.__pago = estado
    
    # Métodos

    def calcular_dias_restantes(self):
        # Si fecha_fin es string, convertirla a date
        # if isinstance(self.__fecha_fin, str):
        #     fecha_fin_obj = datetime.strptime(self.__fecha_fin, "%Y-%m-%d").date()
        #     self.__fecha_fin = fecha_fin_obj  # Actualizar el atributo para que sea un objeto date
        # else:
        #     fecha_fin_obj = self.__fecha_fin
        
        return (self.__fecha_fin - date.today()).days

class Cliente:
    """
    Clase que representa un cliente del gimnasio, contiene información personal y métodos para gestionar membresías y sesiones especiales.
    
    Atributos:
        __id_cliente (int): Identificador único del cliente.
        __nombre (str): Nombre completo del cliente.
        __documento (str): Documento de identidad del cliente.
        __telefono (str, optional): Número de teléfono del cliente. Defaults to None.
        __fecha_registro (str): Fecha de registro del cliente en el gimnasio.
        __membresia (Membresia, optional): Membresía asociada al cliente. Defaults to None.
        __sesiones_especiales (list, optional): Lista de sesiones especiales solicitadas por el cliente. Defaults to [].
        
    Notas:
        - Pensar si es necesario el atributo __sesiones_especiales, ya que podría ser redundante si se gestiona desde la clase SesionEspecial.
        - Pensar si guardaremos el nombre completo o solo el nombre.
    """
    def __init__(self, id_cliente: int, nombre: str, documento: str, fecha_registro: str, telefono: str = None, membresia: Membresia = None):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__documento = documento
        self.__telefono = telefono
        self.__fecha_registro = fecha_registro

        self.__membresia = membresia
        # Se elimina la lista de sesiones especiales, ya que de eliminar una sesión especial, se tendrá que eliminar de la lista de cada cliente.
        
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
        # Retornar como string para compatibilidad con JSON
        return self.__fecha_registro.strftime("%Y-%m-%d")
    
    def get_membresia(self):
        return self.__membresia
    
    # Getters para acceder a la membresía
    
    def get_membresia_pago(self):
        if self.__membresia:
            return self.__membresia.get_pago_m()
        return False
    
    def get_membresia_fecha_inicio(self):
        if self.__membresia:
            return self.__membresia.get_fecha_inicio_m()
        return None
    
    def get_membresia_fecha_fin(self):
        if self.__membresia:
            return self.__membresia.get_fecha_fin_m()
        return None
    
    def get_membresia_dias_restantes(self):
        if self.__membresia:
            return self.__membresia.calcular_dias_restantes()
        return None
    
    def set_membresia(self, membresia : Membresia):
        self.__membresia = membresia
    
    # Metodos sin uso
    
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
    
    def info_membresia(self):
        """Muestra información de la membresía del cliente"""
        if self.__membresia is None:
            print(f"El cliente {self.__nombre} no tiene membresía.")
        else:
            print(f"\n=== Información de Membresía de {self.__nombre} ===")
            print(f"Fecha de inicio: {self.__membresia.get_fecha_inicio_m()}")
            print(f"Fecha de fin: {self.__membresia.get_fecha_fin_m()}")
            print(f"Estado de pago: {'Pagada' if self.__membresia.get_pago_m() else 'Pendiente'}")
            print("="*40)

    def pago_ingreso_unico(self):
        pass

    def solicitar_sesion(self):
        pass

