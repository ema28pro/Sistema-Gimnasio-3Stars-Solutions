import numpy as np
from datetime import date, timedelta, datetime
import Utils as ut

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
    def __init__(self, id_entrenador: int, nombre: str, especialidad: set, telefono: str = None):
        self.__id_entrenador = id_entrenador
        self.__nombre = nombre
        self.__telefono = telefono
        self.__especialidad = especialidad

    # Métodos getter
    def get_id_entrenador(self):
        return self.__id_entrenador
    
    def get_nombre(self):
        return self.__nombre
    
    def get_telefono(self):
        return self.__telefono
    
    def get_especialidad(self):
        return self.__especialidad
    
    # Métodos para mostrar información
    def mostrar_info(self):
        telefono = f"Tel: {self.__telefono}" if self.__telefono else "Sin teléfono"
        print(f"Entrenador {self.__nombre} (ID: {self.__id_entrenador}) - {self.__especialidad} - {telefono}")


class SesionEspecial:
    """
    Clase que representa una sesión especial del gimnasio, contiene información sobre el entrenador, fecha, cupos y métodos para gestionar inscripciones.
    
    Atributos:
        __id_sesion (int): Identificador único de la sesión especial.
        __entrenador (Entrenador): Objeto entrenador que dirige la sesión.
        __fecha (str): Fecha de la sesión especial.
        __cupos (int): Número actual de cupos ocupados.
        __maximo_cupos (int, optional): Numero maximo de cupos. Defaults to 25.
        __inscritos (np.ndarray): Array que almacena los clientes inscritos en la sesión.
    """
    def __init__(self, id_sesion: int, entrenador, fecha: str, maximo_cupos: int = 25):
        self.__id_sesion = id_sesion
        self.__entrenador = entrenador  # Ahora guarda el objeto Entrenador completo
        self.__fecha = fecha
        self.__cupos = 0
        self.__maximo_cupos = maximo_cupos
        self.__inscritos = np.full(maximo_cupos, None, dtype=object) # Estamos guardando el objeto Cliente
    
    # Métodos getter
    def get_id_sesion(self):
        return self.__id_sesion
    
    def get_entrenador(self):
        if self.__entrenador:
            return self.__entrenador
        else:
            print("No hay entrenador asignado a esta sesión.")
    
    def get_id_entrenador(self):
        """Método de compatibilidad para obtener el ID del entrenador"""
        if self.__entrenador:
            return self.__entrenador.get_id_entrenador() 
        else:
            print("No hay entrenador asignado a esta sesión.")
        
    def get_fecha(self):
        if isinstance(self.__fecha, str):
            return self.__fecha
        else:
            return self.__fecha.strftime("%Y-%m-%d")
    
    def get_cupos(self):
        return self.__cupos
    
    def get_maximo_cupos(self):
        return self.__maximo_cupos
    
    def get_cupos_disponibles(self):
        return self.__maximo_cupos - self.__cupos
    
    def get_clientes_inscritos(self):
        """Devuelve una lista de clientes inscritos en la sesión"""
        return [cliente for cliente in self.__inscritos if cliente is not None]
    
    def set_entrenador(self, entrenador):
        if self.__entrenador is None:
            print("Sesion sin entrenador")
        self.__entrenador = entrenador  # Asigna el objeto Entrenador completo
    
    def calcular_dias_restantes(self):
        fecha_actual = date.today()
        
        # Convertir la fecha de la sesión a objeto date
        if isinstance(self.__fecha, str):
            # Asumiendo formato "YYYY-MM-DD"
            if len(self.__fecha.split('-')) == 3:
                fecha_sesion = datetime.strptime(self.__fecha, "%Y-%m-%d").date()
            else:
                print(f"Formato de fecha inválido: {self.__fecha}")
                return None
        elif isinstance(self.__fecha, date):
            fecha_sesion = self.__fecha
        else:
            print("Tipo de fecha no soportado")
            return None
        
        # Calcular la diferencia en días
        diferencia = (fecha_sesion - fecha_actual).days
        if not diferencia or diferencia is None or diferencia < 0:
            return None
        else:
            return diferencia
    
    # Métodos para gestionar inscripciones
    def inscribir_cliente(self, cliente=None):
        """
        Inscribe un cliente a la sesión especial.
        
        Args:
            cliente: Objeto Cliente a inscribir
            
        Returns:
            bool: True si se inscribió exitosamente, False si no hay cupos
        """
        
        
        if self.__cupos >= self.__maximo_cupos:
            print(f"No hay cupos disponibles. Sesión llena ({self.__maximo_cupos}/{self.__maximo_cupos})")
            return False
        
        if cliente is None:
            print("No se proporcionó un cliente para inscribir.")
            return False 
        
        # Verificar si ya está inscrito
        for i in range(self.__cupos):
            if self.__inscritos[i] is not None and self.__inscritos[i].get_id_cliente() == cliente.get_id_cliente():
                print(f"El cliente {cliente.get_nombre()} ya está inscrito en esta sesión.")
                return False
        
        # Inscribir cliente
        self.__inscritos[self.__cupos] = cliente
        self.__cupos += 1
        print(f"Cliente {cliente.get_nombre()} inscrito exitosamente. Cupos: {self.__cupos}/{self.__maximo_cupos}")
        return True
    
    def editar_inscritos(self,id_cliente=None):
        """
        Cancela la inscripción de un cliente de la sesión.
        
        Args:
            cliente: Objeto Cliente a desinscribir
            
        Returns:
            bool: True si se canceló exitosamente, False si no estaba inscrito
        """
        
        if not self.__cupos or self.__cupos <= 0:
            print("No hay clientes inscritos en esta sesión.")
            return False
        
        if self.__cupos > 0:
            print("Clientes inscritos:")
            for i in range(self.__cupos):
                if self.__inscritos[i] is not None:
                    print(f"  - {self.__inscritos[i].get_nombre()} (ID: {self.__inscritos[i].get_id_cliente()})")
        
        if id_cliente is None:
            while True:
                print("0 para cancelar todas las inscripciones")
                id_cliente = input("Ingrese el ID del cliente a cancelar inscripción: ")
                if id_cliente.isdigit():
                    id_cliente = int(id_cliente)
                    break
        
        if id_cliente == 0:
            print("Cancelando todas las inscripciones...")
            self.__inscritos = np.full(self.__maximo_cupos, None, dtype=object)
            self.__cupos = 0
            print(f"Todas las inscripciones canceladas. Cupos: {self.__cupos}/{self.__maximo_cupos}")
            return True
        else:
            
            eliminado = False
            
            for i in range(self.__cupos):
                cliente = self.__inscritos[i]
                if cliente is not None and cliente.get_id_cliente() == id_cliente:
                    # Mover todos los elementos una posición hacia atrás
                    for j in range(i, self.__cupos - 1):
                        self.__inscritos[j] = self.__inscritos[j + 1]
                    
                    # Limpiar la última posición
                    self.__inscritos[self.__cupos - 1] = None
                    self.__cupos -= 1
                    eliminado = True
            
            if eliminado:
                print(f"Inscripción del cliente ID {id_cliente} cancelada exitosamente. Cupos: {self.__cupos}/{self.__maximo_cupos}")
                return True
            else:
                print(f"No se encontró ningún cliente con el ID: {id_cliente} en esta sesión.")
                return False
    
    def mostrar_info(self):
        """Muestra información completa de la sesión"""
        print(f"\n=== Sesión Especial ID: {self.__id_sesion} ===")
        if self.__entrenador:
            print(f"Entrenador: {self.__entrenador.get_nombre()} (ID: {self.__entrenador.get_id_entrenador()}) - {self.__entrenador.get_especialidad()}")
        else:
            print("Entrenador: No asignado")
        print(f"Fecha: {self.__fecha}")
        print(f"Cupos: {self.__cupos}/{self.__maximo_cupos}")
        print(f"Cupos disponibles: {self.get_cupos_disponibles()}")
        
        if self.__cupos > 0:
            print("Clientes inscritos:")
            for i in range(self.__cupos):
                if self.__inscritos[i] is not None:
                    print(f"  - {self.__inscritos[i].get_nombre()} (ID: {self.__inscritos[i].get_id_cliente()})")
        else:
            print("No hay clientes inscritos.")
        print("="*40)
        return self.__entrenador

    def ver_entrenador(self):
        """Muestra información del entrenador de la sesión"""
        if self.__entrenador:
            self.__entrenador.mostrar_info()
        else:
            print("No hay entrenador asignado a esta sesión.")