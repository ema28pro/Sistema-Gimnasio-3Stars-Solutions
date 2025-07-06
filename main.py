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
        __numero_membresias (int): Contador de membresías registradas.
        __historico_membresias (int): Contador de membresías históricas.
        __entrenadores (np.ndarray): Array que almacena los entrenadores registrados.
        __sesiones (np.ndarray): Array que almacena las sesiones especiales programadas.
        
        Notas:
        - Necesitaremos un contador para membresias y para entrenadores?
        - Pensar en los registros y como lo llevaremos
    """    
    def __init__(self, nombre: str, direccion: str, telefono: str, correo: str, efectivo: float = 0):   
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.__correo_electronico = correo
        self.__efectivo = efectivo

        self.__numero_clientes = 0
        self.__historico_clientes = 0
        self.__clientes = np.full(50, None, dtype=object)
        self.__numero_membresias = 0
        self.__historico_membresias = 0
        self.__membresias = np.full(50, None, dtype=object)
        self.__entrenadores = np.full(5, None, dtype=object)
        self.__sesiones = np.full(10, None,dtype=object)
        
    def get(self):
        return self.__clientes, self.__membresias, self.__entrenadores, self.__sesiones
    
    # Métodos accesores y modificadores
    
    # def set_membresias(self, membresia):
    #     """_summary_
    #         Agrega una membresía al gimnasio.
    #     """
    #     for i in range(50):
    #         if self.__membresias[i] is None:
    #             self.__membresias[i] = membresia
    #             # Tinking
    #             break

    def ver_inf(self):
        """_summary_
            Imprime el nombre y telefono de contacto del gimnasio
        """        
        print(f"Gimnasio {self.__nombre}, Tel: {self.__telefono},\nCorreo: {self.__correo_electronico}, nos encontramos ubicados en {self.__direccion}")

    def registrar_cliente(self, nombre, documento, telefono=None):
        
        #Validaciones
        
        if self.__numero_clientes >= 50:
            print("No se pueden registrar más clientes, el gimnasio ha alcanzado su capacidad máxima.")
            return
        if not nombre or not documento:
            print("Nombre y documento son obligatorios.")
            return
        if telefono and (telefono.isalpha() or not telefono.isdigit()):
            print("El teléfono debe ser un número válido.")
            return
        if nombre.isdigit() or not nombre.isalpha():
            print("El nombre no debe contener números ni símbolos ni espacios.")
            return
        if documento.isalpha() or not documento.isdigit():
            print("El documento no debe contener letras ni símbolos ni espacios.")
            return
        
        id_cliente = self.__historico_clientes + 1
        
        fecha_registro = date.today()
        
        nuevo_cliente = Cliente(id_cliente, nombre.lower(), documento, fecha_registro, telefono if telefono else None)
        # Forma 1, buscar un espacio vacío en el array de clientes
        for i in range(50):
            if self.__clientes[i] is None:
                self.__clientes[i] = nuevo_cliente
                break
        # # Forma 2, asignar directamente al índice del contador de clientes
        # self.__clientes[self.__numero_clientes] = nuevo_cliente

        self.__numero_clientes += 1
        self.__historico_clientes += 1
        print(f"ID {id_cliente} : Cliente {nombre} registrado exitosamente. {fecha_registro}")

    def consultar_membresia(self, id_cliente):
        pass

    def registrar_entrada(self, id_cliente):
        # lógica para registrar entrada de un cliente
        pass

    def visualizar_clientes(self):      
        print("\n=== Clientes Registrados ===")
        total_clientes = 0
        for cliente in self.__clientes:
            if cliente is not None:
                total_clientes += 1
                print(f"ID: {cliente.get_id_c()}, Nombre: {cliente.get_nombre_c()}, Documento: {cliente.get_documento_c()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
        
        print(f"\nNumero de Clientes Registradas : {total_clientes}")
    
    def visualizar_membresias(self):
        print("\n=== Membresías Registradas ===")
        total_membresias = 0
        for membresia in self.__membresias:
            if membresia is not None:
                total_membresias += 1
                print(f"ID: {membresia.get_id_m()}, Estado: {membresia.get_estado_m()}, Fecha Inicio: {membresia.get_fecha_inicio_m()}, Fecha Fin: {membresia.get_fecha_fin_m()}")
        
        print(f"\nNumero de Membresias Registradas : {total_membresias}")

    def analisis_financiero(self):
        # lógica de análisis
        pass

    def reporte_diario(self):
        # generar un resumen del día
        pass

    def informe_entrada(self):
        # reporte de entradas diarias
        pass
    
    # def crear_membresia(self, ):
    #     for cliente in self.__clientes:
    #         if 

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
        self.__sesiones_especiales = [] # Pendiente. Pensar si es necesario este atributo, ya que podría ser redundante si se gestiona desde la clase SesionEspecial.
        
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
        pago = input("Pago inmediato? (Si/No) : ").lower()
        
        if pago not in ["si", "no", "sí"]:
            print("Respuesta no válida, por favor ingrese 'Si' o 'No'.")
            return
        
        if pago in ["si", "sí"]:
            print("Procesando pago inmediato...")
            # Aquí iría la lógica para crear la membresía
        else:
            print("Se registra deuda pendiente...")
            # Aquí iría la lógica para crear membresía con estado "Debe"

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

def main():
    Gym = Gimnasio("Body Force","Barrio Candelilla", 3001234545, "body@force.com", 45000)
    # # Gym.ver_inf()
    # Gym.registrar_cliente("Emanuel", "21554", "0")
    # print(Gym.get())
    # Gym.visualizar_clientes()
    print(Gym.get())

main()
