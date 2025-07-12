import numpy as np
from datetime import date, timedelta
import Utils as ut
from Utils import PRECIO_MEMBRESIA, PRECIO_ENTRADA_UNICA

from Clientes import Cliente, Membresia
from Sesiones import Entrenador, SesionEspecial

class Gimnasio:
    """_summary_
    Clase que representa un gimnasio, contiene información básica y métodos para gestionar clientes, membresías, entrenadores y sesiones especiales.
    
    Atributos:
        __nombre (str): Nombre del Gimnasio.
        __direccion (str): Dirección del Gimnasio.
        __telefono (str): Número de teléfono del Gimnasio.
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

        self.__maximo_clientes = 50
        self.__numero_clientes = 0
        self.__historico_clientes = 0
        self.__clientes = np.full(self.__maximo_clientes, None, dtype=object)
        self.__numero_membresias = 0
        self.__historico_membresias = 0
        self.__membresias = np.full(self.__maximo_clientes, None, dtype=object)
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
        if ut.is_positve(efectivo, "Efectivo"):
            print(f"Efectivo actual: ${self.__efectivo:,} + ${float(efectivo):,}")
            self.__efectivo += float(efectivo)
            print(f"Efectivo actualizado a: ${self.__efectivo:,}")

    def ver_inf(self):
        """_summary_
            Imprime el nombre y telefono de contacto del gimnasio
        """        
        print(f"Gimnasio {self.__nombre}, Tel: {self.__telefono},\nCorreo: {self.__correo_electronico}, nos encontramos ubicados en {self.__direccion}")

    # Metodos

    # R1
    def crear_cliente(self, nombre, documento, telefono=None):
        
        #Validaciones
        
        if self.__numero_clientes >= self.__maximo_clientes:
            print("No se pueden registrar más clientes, el gimnasio ha alcanzado su capacidad máxima.")
            return False
        if telefono and ( not ut.is_number(telefono, "Telefono")):
            return False
        if not (ut.is_string(nombre, "Nombre") and ut.is_number(documento, "Documento")):
            return False
        
        id_cliente = self.__historico_clientes + 1
        
        fecha_registro = date.today()
        
        # Verificar si el cliente ya está registrado
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_documento_c() == documento:
                print(f"\n!!! El cliente con documento {documento} ya está registrado.")
                return False
        
        nuevo_cliente = Cliente(id_cliente, nombre.lower(), documento, fecha_registro, telefono if telefono else None)
        # Forma 1, buscar un espacio vacío en el array de clientes
        for i in range(self.__maximo_clientes):
            if self.__clientes[i] is None:
                self.__clientes[i] = nuevo_cliente
                break
        # # Forma 2, asignar directamente al índice del contador de clientes
        # self.__clientes[self.__numero_clientes] = nuevo_cliente

        self.__numero_clientes += 1
        self.__historico_clientes += 1
        print(f"ID {id_cliente} : Cliente {nombre} registrado exitosamente. {fecha_registro}")
        return True
    
    def registrar_cliente(self):
        print("===== Registrando Cliente =====")
        
        if self.__numero_clientes >= len(self.__clientes):
            print("No se pueden registrar más clientes, el gimnasio ha alcanzado su capacidad máxima.")
            return False
        
        
        while True:
            nombre = input("Ingrese el Nombre del CLiente : ")
            if ut.is_string(nombre, "Nombre"):
                break
        
        while True:
            documento = input("Ingrese el Documento del Cliente : ")
            if ut.is_number(documento, "Documento"):
                break
        
        
        while True:
            telefono = input("Ingrese el numero del Cliente (Enter para Omitir) : ")
            if telefono:
                if ut.is_number(telefono, "Telefono"):
                    break
            else:
                break
        
        if self.crear_cliente(nombre,documento,telefono):
            print("\nCliente registrado exitosamente")
            return True
        else:
            print("\nError al registrar el cliente")
            return False
    
    
    # R3
    def crear_membresia(self, cliente_encontrado: Cliente):
        
        # Validaciones
        
        if self.__numero_membresias >= self.__maximo_clientes:
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
            self.ingreso_caja(PRECIO_MEMBRESIA)
            print(f"Pago realizado exitosamente. Monto: ${PRECIO_MEMBRESIA:,}")
            nueva_membresia = Membresia(id_membresia, fecha_inicio, fecha_fin, True)
        else:
            nueva_membresia = Membresia(id_membresia, fecha_inicio, fecha_fin)
        
        # cliente_encontrado.membresia =  nueva_membresia
        
        # Agregar la membresía al array de membresías
        for i in range(self.__maximo_clientes):
            if self.__membresias[i] is None:
                self.__membresias[i] = nueva_membresia
                break
        
        self.__numero_membresias += 1
        self.__historico_membresias +=1
        print(f"Cliente {cliente_encontrado.get_nombre_c()}, la membresia con ID {id_membresia} fue creada con finalizacion : {fecha_fin}")
        
        cliente_encontrado.set_id_membresia(id_membresia)
        print(f"Cliente {cliente_encontrado.get_nombre_c()} ahora tiene la membresía con ID {cliente_encontrado.get_id_membresia()}.")
    
    def buscar_cliente(self, op=None):
        
        # Buqueda por ID, Nombre o Documento
        
        print("\n======= Buscar Cliente =======")
        print(30*"=")
        print("Seleccione el tipo de búsqueda :")
        print("1. Buscar por ID")
        print("2. Buscar por Nombre")
        print("3. Buscar por Documento")
        print("Enter para salir")
        opcion_busqueda = input("Seleccione una opción : ")
        print(30*"=")
        
        cliente_encontrado = None # Variable para almacenar el cliente encontrado o None si no se encuentra
        
        # Swich case para manejar las opciones de búsqueda
        match opcion_busqueda:
            case "1":
                while True: #Ciclo para el correcto ingreso del ID
                    id_cliente = input("Ingrese el ID del cliente: ")
                    if ut.is_number(id_cliente, "ID"):
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
                    if ut.is_string(nombre_cliente, "Nombre"):
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
                    if ut.is_number(documento, "Documento"):
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
        
        print("\n"*3)
        
        # Acciones con el cliente encontrado
        while True:
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
            print(30*"=")
            
            match opcion_cliente:
                case "1":
                    self.crear_membresia(cliente_encontrado)
                case "2":
                    self.pagar_membresia(cliente_encontrado)
                case "3":
                    self.consultar_membresia(cliente_encontrado)
                case "4":
                    cliente_encontrado.registrar_entrada()
                case "6":
                    cliente_encontrado.pago_ingreso_unico()
                case "7":
                    self.agendar_sesion(cliente_encontrado)
                case "8":
                    self.cancelar_sesion(cliente_encontrado)
                case "":
                    print("Saliendo del menú de cliente.")
                    break

    def consultar_membresia(self, cliente_encontrado: Cliente):
        if cliente_encontrado.get_id_membresia() is None:
            print(f"El cliente {cliente_encontrado.get_nombre_c()} no tiene una membresía activa.")
            return
        id_membresia = cliente_encontrado.get_id_membresia()
        membresia_encontrada = None
        for membresia in self.__membresias:
            if membresia is not None and membresia.get_id_membresia() == id_membresia:
                membresia_encontrada = membresia
                print(f"Membresía encontrada: ID: {membresia.get_id_membresia()}, Estado: {membresia.get_pago_m()}, Fecha Inicio: {membresia.get_fecha_inicio_m()}, Fecha Fin: {membresia.get_fecha_fin_m()}")
                break
        if not membresia_encontrada:
            print(f"No se encontró una membresía con ID {id_membresia}.")
            return
        else:
            # Mostrar información de la membresía
            print(f"\n=== Información de Membresía ===")
            print(f"Cliente: {cliente_encontrado.get_nombre_c()}")
            print(f"ID Membresía: {membresia_encontrada.get_id_membresia()}")
            print(f"Fecha de inicio: {membresia_encontrada.get_fecha_inicio_m()}")
            print(f"Fecha de fin: {membresia_encontrada.get_fecha_fin_m()}")
            print(f"Estado de pago: {'Pagada' if membresia_encontrada.get_pago_m() else 'Pendiente'}")
            print("="*30)
            
            # Menu membresia
            print("\n=== ¿Que desea hacer? ===")
            print(30*"=")
            print("1. Eliminar Membresia")
            print("2. Pagar Membresía" if not membresia_encontrada.get_pago_m() else "Membresía ya pagada")
            print("Enter para salir")
            opcion_membresia = input("Seleccione una opción : ")
            
            match opcion_membresia:
                case "1":
                    self.elminar_membresia(membresia_encontrada)
                case "2":
                    self.pagar_membresia(membresia_encontrada)
                case "":
                    print("Saliendo del menú de membresía.")

    def pagar_membresia(self, membresia_encontrada: Membresia):
        """_summary_
            Paga la membresía encontrada y actualiza su estado.
        """
        
        # No se coloca en la clase Membresia para no dar acceso a la modificación del efectivo desde la clase Membresia y porque el pago se gestiona desde el gimnasio.
        
        if membresia_encontrada.get_pago_m():
            print("La membresía ya ha sido pagada.")
            return
        else:
            print(f"El cliente tiene una membresía con ID {membresia_encontrada.get_id_membresia()} qudee aún no ha sido pagada.")   
            self.set_efectivo(PRECIO_MEMBRESIA)
            membresia_encontrada.set_pago_m(True)
            print(f"Pago realizado exitosamente. Monto: ${PRECIO_MEMBRESIA:,}")
        

    def registrar_entrada(self, cliente_encontrado: Cliente):
        pass

    def pago_ingreso_unico(self, cliente_encontrado: Cliente):
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
                print(f"ID: {membresia.get_id_membresia()}, Estado: {membresia.get_pago_m()}, Fecha Inicio: {membresia.get_fecha_inicio_m()}, Fecha Fin: {membresia.get_fecha_fin_m()}")
        
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

    # Métodos para gestionar entrenadores
    def registrar_entrenador(self, nombre: str, especialidad: set, telefono: str = None):
        """
        Registra un nuevo entrenador en el gimnasio.
        
        Args:
            nombre (str): Nombre del entrenador
            especialidad (set): Conjunto de especialidades del entrenador
            telefono (str, optional): Teléfono del entrenador
        """
        id_entrenador = self.__historico_entrenadores + 1
        nuevo_entrenador = Entrenador(id_entrenador, nombre, especialidad, telefono)
        self.__entrenadores.append(nuevo_entrenador)
        self.__historico_entrenadores += 1
        print(f"Entrenador {nombre} registrado con ID: {id_entrenador}")
        return nuevo_entrenador
    
    def crear_sesion_especial(self, id_entrenador: int, fecha: str, maximo_cupos: int = 25):
        """
        Crea una nueva sesión especial.
        
        Args:
            id_entrenador (int): ID del entrenador que dirigirá la sesión
            fecha (str): Fecha de la sesión
            maximo_cupos (int, optional): Número máximo de cupos. Defaults to 25.
        """
        # Verificar que el entrenador existe
        entrenador_encontrado = None
        for entrenador in self.__entrenadores:
            if entrenador.get_id_entrenador() == id_entrenador:
                entrenador_encontrado = entrenador
                break
        
        if not entrenador_encontrado:
            print(f"No se encontró un entrenador con ID {id_entrenador}")
            return None
        
        id_sesion = self.__historico_sesiones + 1
        nueva_sesion = SesionEspecial(id_sesion, id_entrenador, fecha, maximo_cupos)
        self.__sesiones.append(nueva_sesion)
        self.__historico_sesiones += 1
        print(f"Sesión especial creada con ID: {id_sesion} para el {fecha}")
        return nueva_sesion
    
    def agendar_sesion(self, cliente):
        """
        Permite a un cliente inscribirse en una sesión especial.
        
        Args:
            cliente: Objeto Cliente que se quiere inscribir
        """
        if not self.__sesiones:
            print("No hay sesiones especiales disponibles.")
            return
        
        print("\n=== Sesiones Especiales Disponibles ===")
        sesiones_disponibles = []
        
        for i, sesion in enumerate(self.__sesiones):
            if sesion.get_cupos_disponibles() > 0:
                sesiones_disponibles.append(sesion)
                # Buscar el entrenador
                entrenador = None
                for ent in self.__entrenadores:
                    if ent.get_id_entrenador() == sesion.get_id_entrenador():
                        entrenador = ent
                        break
                
                print(f"{len(sesiones_disponibles)}. Sesión ID: {sesion.get_id_sesion()}")
                print(f"   Fecha: {sesion.get_fecha()}")
                print(f"   Entrenador: {entrenador.get_nombre() if entrenador else 'No encontrado'}")
                print(f"   Cupos disponibles: {sesion.get_cupos_disponibles()}")
                print()
        
        if not sesiones_disponibles:
            print("No hay sesiones con cupos disponibles.")
            return
        
        try:
            print("Ingrese 0 para cancelar")
            opcion = int(input("Seleccione una sesión: "))
            
            if opcion == 0:
                print("Operación cancelada.")
                return
            
            if 1 <= opcion <= len(sesiones_disponibles):
                sesion_elegida = sesiones_disponibles[opcion - 1]
                
                # Inscribir en la sesión (esto actualiza la sesión)
                if sesion_elegida.inscribir_cliente(cliente):
                    # También agregar la sesión al cliente (esto actualiza el cliente)
                    cliente.agregar_sesion(sesion_elegida.get_id_sesion())
                    print(f"¡Inscripción exitosa en la sesión del {sesion_elegida.get_fecha()}!")
            else:
                print("Opción inválida.")
                
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    def cancelar_sesion(self, cliente):
        """
        Permite a un cliente cancelar su inscripción en una sesión especial.
        
        Args:
            cliente: Objeto Cliente que quiere cancelar
        """
        sesiones_cliente = cliente.get_sesiones_especiales()
        
        if not sesiones_cliente:
            print(f"El cliente {cliente.get_nombre_c()} no tiene sesiones inscritas.")
            return
        
        print(f"\n=== Sesiones de {cliente.get_nombre_c()} ===")
        sesiones_encontradas = []
        
        for id_sesion in sesiones_cliente:
            # Buscar la sesión en la lista del gimnasio
            for sesion in self.__sesiones:
                if sesion.get_id_sesion() == id_sesion:
                    sesiones_encontradas.append(sesion)
                    # Buscar el entrenador
                    entrenador = None
                    for ent in self.__entrenadores:
                        if ent.get_id_entrenador() == sesion.get_id_entrenador():
                            entrenador = ent
                            break
                    
                    print(f"{len(sesiones_encontradas)}. Sesión ID: {sesion.get_id_sesion()}")
                    print(f"   Fecha: {sesion.get_fecha()}")
                    print(f"   Entrenador: {entrenador.get_nombre() if entrenador else 'No encontrado'}")
                    print()
                    break
        
        try:
            print("Ingrese 0 para cancelar")
            opcion = int(input("Seleccione una sesión a cancelar: "))
            
            if opcion == 0:
                print("Operación cancelada.")
                return
            
            if 1 <= opcion <= len(sesiones_encontradas):
                sesion_elegida = sesiones_encontradas[opcion - 1]
                
                # Cancelar en la sesión (esto actualiza la sesión)
                if sesion_elegida.cancelar_inscripcion(cliente):
                    # También remover la sesión del cliente (esto actualiza el cliente)
                    cliente.remover_sesion(sesion_elegida.get_id_sesion())
                    print(f"¡Cancelación exitosa de la sesión del {sesion_elegida.get_fecha()}!")
            else:
                print("Opción inválida.")
                
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    def mostrar_sesiones_disponibles(self):
        """Muestra todas las sesiones especiales disponibles"""
        if not self.__sesiones:
            print("No hay sesiones especiales programadas.")
            return
        
        print("\n=== Todas las Sesiones Especiales ===")
        for sesion in self.__sesiones:
            sesion.mostrar_info()
    
    def mostrar_entrenadores(self):
        """Muestra todos los entrenadores registrados"""
        if not self.__entrenadores:
            print("No hay entrenadores registrados.")
            return
        
        print("\n=== Entrenadores Registrados ===")
        for entrenador in self.__entrenadores:
            entrenador.mostrar_info()


