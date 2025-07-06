import numpy as np
from datetime import date

from Clientes import Cliente, Membresia
from Sesiones import Entrenador, SesionEspecial

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
        self.__membresias = np.full(50, None, dtype=object)
        self.__entrenadores = np.full(5, None, dtype=object)
        self.__sesiones = np.full(10, None,dtype=object)
        
    def get(self):
        return self.__clientes, self.__membresias, self.__entrenadores, self.__sesiones
    
    # Métodos accesores y modificadores
    
    def set_membresias(self, membresia):
        """_summary_
            Agrega una membresía al gimnasio.
        """
        for i in range(50):
            if self.__membresias[i] is None:
                self.__membresias[i] = membresia
                # Tinking
                break

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