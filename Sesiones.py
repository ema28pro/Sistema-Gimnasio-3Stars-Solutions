import numpy as np
from datetime import date

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
    
    def get_nombre_e(self):
        return self.__nombre
    
    def get_telefono_e(self):
        return self.__telefono
    
    def get_especialidad_e(self):
        return self.__especialidad
    
    # Métodos para mostrar información
    def mostrar_info_e(self):
        telefono = f"Tel: {self.__telefono}" if self.__telefono else "Sin teléfono"
        print(f"Entrenador {self.__nombre} (ID: {self.__id_entrenador}) - {self.__especialidad} - {telefono}")


class SesionEspecial:
    """
    Clase que representa una sesión especial del gimnasio, contiene información sobre el entrenador, fecha, cupos y métodos para gestionar inscripciones.
    
    Atributos:
        __id_sesion (int): Identificador único de la sesión especial.
        __id_entrenador (int): Identificador unico del entrenador que dirige la sesión.
        __fecha (str): Fecha de la sesión especial.
        __maximo_cupos (int, optional): Numero maximo de cupos. Defaults to 25.
        __cupos (int): Número actual de cupos ocupados.
        __inscritos (np.ndarray): Array que almacena los clientes inscritos en la sesión.
    """
    def __init__(self, id_sesion: int, id_entrenador: int, fecha: str, maximo_cupos: int = 25):
        self.__id_sesion = id_sesion
        self.__id_entrenador = id_entrenador
        self.__cupos = 0
        self.__fecha = fecha
        self.__maximo_cupos = maximo_cupos
        self.__inscritos = np.full(maximo_cupos, None, dtype=object)
    
    # Métodos getter
    def get_id_sesion(self):
        return self.__id_sesion
    
    def get_id_entrenador(self):
        return self.__id_entrenador
    
    def get_fecha_se(self):
        return self.__fecha
    
    def get_cupos_se(self):
        return self.__cupos
    
    def get_maximo_cupos_se(self):
        return self.__maximo_cupos
    
    def get_inscritos_se(self):
        return self.__inscritos
    
    def get_cupos_disponibles(self):
        return self.__maximo_cupos - self.__cupos
    
    # Métodos para gestionar inscripciones
    def inscribir_cliente(self, cliente):
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
        
        # Verificar si ya está inscrito
        for i in range(self.__cupos):
            if self.__inscritos[i] is not None and self.__inscritos[i].get_id_cliente() == cliente.get_id_cliente():
                print(f"El cliente {cliente.get_nombre_c()} ya está inscrito en esta sesión.")
                return False
        
        # Inscribir cliente
        self.__inscritos[self.__cupos] = cliente
        self.__cupos += 1
        print(f"Cliente {cliente.get_nombre_c()} inscrito exitosamente. Cupos: {self.__cupos}/{self.__maximo_cupos}")
        return True
    
    def cancelar_inscripcion(self, cliente):
        """
        Cancela la inscripción de un cliente de la sesión.
        
        Args:
            cliente: Objeto Cliente a desinscribir
            
        Returns:
            bool: True si se canceló exitosamente, False si no estaba inscrito
        """
        for i in range(self.__cupos):
            if self.__inscritos[i] is not None and self.__inscritos[i].get_id_cliente() == cliente.get_id_cliente():
                # Mover todos los elementos una posición hacia atrás
                for j in range(i, self.__cupos - 1):
                    self.__inscritos[j] = self.__inscritos[j + 1]
                
                # Limpiar la última posición
                self.__inscritos[self.__cupos - 1] = None
                self.__cupos -= 1
                print(f"Inscripción de {cliente.get_nombre_c()} cancelada. Cupos: {self.__cupos}/{self.__maximo_cupos}")
                return True
        
        print(f"El cliente {cliente.get_nombre_c()} no está inscrito en esta sesión.")
        return False
    
    def mostrar_info(self):
        """Muestra información completa de la sesión"""
        print(f"\n=== Sesión Especial ID: {self.__id_sesion} ===")
        print(f"Entrenador ID: {self.__id_entrenador}")
        print(f"Fecha: {self.__fecha}")
        print(f"Cupos: {self.__cupos}/{self.__maximo_cupos}")
        print(f"Cupos disponibles: {self.get_cupos_disponibles()}")
        
        if self.__cupos > 0:
            print("Clientes inscritos:")
            for i in range(self.__cupos):
                if self.__inscritos[i] is not None:
                    print(f"  - {self.__inscritos[i].get_nombre_c()} (ID: {self.__inscritos[i].get_id_cliente()})")
        else:
            print("No hay clientes inscritos.")
        print("="*40)
        return self.__id_entrenador