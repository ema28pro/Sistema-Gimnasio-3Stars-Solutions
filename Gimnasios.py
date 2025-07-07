import numpy as np
from datetime import date, timedelta
import Utils as ut

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
        self.__historico_entrenadores = 0
        self.__entrenadores = []
        self.__historico_sesiones = 0
        self.__sesiones = []
        
    # Métodos accesores y modificadores
    
    def get(self):
        return self.__clientes, self.__membresias, self.__entrenadores, self.__sesiones
    
    def set_efectivo(self, efectivo: float):
        """_summary_
            Modifica el efectivo del gimnasio.
        """
        if efectivo >= 0:
            print(f"Efectivo actual: {self.__efectivo}")
            self.__efectivo += efectivo
            print(f"Efectivo actualizado a: {self.__efectivo}")
        else:
            print("El efectivo no puede ser negativo.")

    def ver_inf(self):
        """_summary_
            Imprime el nombre y telefono de contacto del gimnasio
        """        
        print(f"Gimnasio {self.__nombre}, Tel: {self.__telefono},\nCorreo: {self.__correo_electronico}, nos encontramos ubicados en {self.__direccion}")

    # Metodos

    # R1
    def registrar_cliente(self, nombre, documento, telefono=None):
        
        #Validaciones
        
        if self.__numero_clientes >= 50:
            print("No se pueden registrar más clientes, el gimnasio ha alcanzado su capacidad máxima.")
            return False
        if telefono and ( not ut.is_number(telefono, "Telefono")):
            return
        if not (ut.is_string(nombre, "Nombre") and ut.is_number(documento, "Documento")):
            return False
        
        id_cliente = self.__historico_clientes + 1
        
        fecha_registro = date.today()
        
        # Verificar si el cliente ya está registrado
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_documento_c() == documento:
                print(f"El cliente con documento {documento} ya está registrado.")
                return False
        
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
        return True
    
    # R3
    def crear_membresia(self, cliente_encontrado: Cliente):
        
        # Validaciones
        
        if self.__numero_membresias >= 50:
            print("No se pueden registrar más membresias, el gimnasio ha alcanzado su capacidad máxima.")
            return
        
        id_membresia = self.__historico_membresias + 1
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=30)
        
        while True: # Ciclo para el correcto ingreso del ID
            pagar = input("Desea pagar inmediatamente. (si/no)\nR// ")
            if ut.valid_yes_no(pagar):
                break
        
        if ut.yes_no(pagar):
            self.set_efectivo(50000)
            print("Pago realizado exitosamente.")
            nueva_membresia = Membresia(id_membresia, fecha_inicio, fecha_fin, True)
        else:
            nueva_membresia = Membresia(id_membresia, fecha_inicio, fecha_fin)
        
        # Agregar la membresía al array de membresías
        for i in range(50):
            if self.__membresias[i] is None:
                self.__membresias[i] = nueva_membresia
                break
        
        self.__numero_membresias += 1
        self.__historico_membresias +=1
        print(f"Cliente {cliente_encontrado.get_nombre_c()}, la membresia con ID {id_membresia} fue creada con finalizacion : {fecha_fin}")
        
        cliente_encontrado.set_id_membresia(id_membresia)
        print(f"Cliente {cliente_encontrado.get_nombre_c()} ahora tiene la membresía con ID {cliente_encontrado.get_id_membresia()}.")
    
    def buscar_cliente(self):
        
        # Buqueda por ID, Nombre o Documento
        
        print("\n======= Buscar Cliente =======")
        print(30*"=")
        print("Seleccione el tipo de búsqueda :")
        print("1. Buscar por ID")
        print("2. Buscar por Nombre")
        print("3. Buscar por Documento")
        print("Enter para salir")
        opcion_busqueda = input("Seleccione una opción : ")
        cliente_encontrado = None # Variable para almacenar el cliente encontrado o None si no se encuentra
        
        # Swich case para manejar las opciones de búsqueda
        match opcion_busqueda:
            case "1":
                while True: #Ciclo para el correcto ingreso del ID
                    id_cliente = input("Ingrese el ID del cliente: ")
                    if id_cliente.isalpha() or not id_cliente.isdigit(): # Validacion (Pensar en una funcion para validar Numeros y Strings)
                        print("El ID no debe contener letras ni símbolos ni espacios.")
                    else:
                        break # Salir del ciclo si el ID es válido
                for cliente in self.__clientes: # Recorrer el array de clientes
                    if cliente is not None and cliente.get_id_cliente() == int(id_cliente): # Buscar coincidencia
                        cliente_encontrado = cliente # Guardar el cliente encontrado
                        # Imprimir los detalles del cliente encontrado
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre_c()}, Documento: {cliente.get_documento_c()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
                if not cliente_encontrado: # Si no se encontró el cliente, informar al usuario
                    print(f"No se encontró un cliente con ID {id_cliente}.")
                    return
            case "2":
                while True:
                    nombre_cliente = input("Ingrese el nombre del cliente: ")
                    if nombre_cliente.isdigit() or not nombre_cliente.isalpha():
                        print("El nombre no debe contener números ni símbolos ni espacios.")
                    else:
                        break
                for cliente in self.__clientes:
                    if cliente is not None and cliente.get_nombre_c() == nombre_cliente.lower():
                        cliente_encontrado = cliente
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre_c()}, Documento: {cliente.get_documento_c()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
                if not cliente_encontrado:
                    print(f"No se encontró un cliente con nombre {nombre_cliente}.")
                    return
            case "3":
                while True:
                    documento = input("Ingrese el documento del cliente: ")
                    if documento.isalpha() or not documento.isdigit():
                        print("El documento no debe contener letras ni símbolos ni espacios.")
                    else:
                        break
                for cliente in self.__clientes:
                    if cliente is not None and cliente.get_documento_c() == documento:
                        cliente_encontrado = cliente
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre_c()}, Documento: {cliente.get_documento_c()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
                if not cliente_encontrado:
                    print(f"No se encontró un cliente con documento {documento}.")
                    return
            case "":
                print("Saliendo del menú de búsqueda.")
        
        # Acciones con el cliente encontrado
        
        print("\n=== ¿Que desea hacer? ===")
        print(30*"=")
        print("1. Adquirir Membresía")
        print("2. Pagar Membresía")
        print("3. Consultar Membresía")
        print("4. Registrar Entrada")
        print("6. Pago Ingreso Único")
        print("7. Solicitar Sesión Especial")
        print("8. Cancelar Sesión Especial")
        print("Enter para salir")
        opcion_cliente = input("Seleccione una opción : ")
        
        match opcion_cliente:
            case "1":
                self.crear_membresia(cliente_encontrado)
            case "2":
                self.pagar_membresia(cliente_encontrado)
            case "3":
                self.consultar_membresia(cliente_encontrado.get_id_membresia())
            case "4":
                self.registrar_entrada(cliente_encontrado)
            case "6":
                self.pago_ingreso_unico(cliente_encontrado)
            case "7":
                cliente_encontrado.agendar_sesion()
            case "8":
                cliente_encontrado.cancelar_sesion()
            case "":
                print("Saliendo del menú de cliente.")

    def consultar_membresia(self, id_membresia):
        membresia_encontrada = None
        for membresia in self.__membresias:
            if membresia is not None and membresia.get_id_m() == id_membresia:
                membresia_encontrada = membresia
                print(f"Membresía encontrada: ID: {membresia.get_id_m()}, Estado: {membresia.get_estado_m()}, Fecha Inicio: {membresia.get_fecha_inicio_m()}, Fecha Fin: {membresia.get_fecha_fin_m()}")
                break
        if not membresia_encontrada:
            print(f"No se encontró una membresía con ID {id_membresia}.")
            return
        else:
            # Menu membresia
            print("\n=== ¿Que desea hacer? ===")
            print(30*"=")
            print("1. Eliminar Membresia")
            print("2. Pagar Membresía" if not membresia_encontrada.get_pago_m())
            print("Enter para salir")
            opcion_membresia = input("Seleccione una opción : ")
            
            match opcion_membresia:
                case "1":
                    self.elminar_membresia(membresia_encontrada)
                case "2":
                    self.pagar_membresia(membresia_encontrada)
                case "":
                    print("Saliendo del menú de membresía.")


    def registrar_entrada(self, id_cliente):
        # lógica para registrar entrada de un cliente
        pass

    def visualizar_clientes(self):      
        print("\n=== Clientes Registrados ===")
        total_clientes = 0
        for cliente in self.__clientes:
            if cliente is not None:
                total_clientes += 1
                print(f"ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre_c()}, Documento: {cliente.get_documento_c()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
        
        print(f"\nNumero de Clientes Registradas : {total_clientes}")
    
    def visualizar_membresias(self):
        print("\n=== Membresías Registradas ===")
        total_membresias = 0
        for membresia in self.__membresias:
            if membresia is not None:
                total_membresias += 1
                print(f"ID: {membresia.get_id_m()}, Estado: {membresia.get_estado_m()}, Fecha Inicio: {membresia.get_fecha_inicio_m()}, Fecha Fin: {membresia.get_fecha_fin_m()}")
        
        print(f"\nNumero de Membresias Registradas : {total_membresias}")
        
    
    def ingreso_caja(self, efectivo: float):
        """_summary_
            Modifica el efectivo del gimnasio.
        """
        if efectivo >= 0:
            print(f"Efectivo actual: {self.__efectivo} + {efectivo}")
            self.__efectivo += efectivo
            print(f"Efectivo actualizado a: {self.__efectivo}")
        else:
            print("El efectivo no puede ser negativo.")

    #! Tarea de Emanuel

    def analisis_financiero(self):
        # lógica de análisis
        pass

    def reporte_diario(self):
        # generar un resumen del día
        pass

    def informe_entrada(self):
        # reporte de entradas diarias
        pass
