import numpy as np
import json
from datetime import date, timedelta, datetime
import Utils as ut
from Utils import PRECIO_MEMBRESIA, PRECIO_ENTRADA_UNICA

from Clientes import Cliente, Membresia
from Sesiones import Entrenador, SesionEspecial
import os

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
        self.__historico_entrenadores = 0
        self.__entrenadores = []
        self.__historico_sesiones = 0
        self.__sesiones = []
        self.__sesiones_especiales = ["boxeo", "yoga", "aerobicos"]
        
    # Métodos accesores y modificadores
    
    def get(self):
        return self.__clientes, self.__entrenadores, self.__sesiones

    def ver_inf(self):
        """_summary_
            Imprime el nombre y telefono de contacto del gimnasio
        """        
        print(f"Gimnasio {self.__nombre}, Tel: {self.__telefono},\nCorreo: {self.__correo_electronico}, nos encontramos ubicados en {self.__direccion}")

    #? ============================== Metodos De Creacion ==============================

    # R1
    def crear_cliente(self, nombre=None, documento=None, telefono=None, fecha_registro=None):
        
        if self.__numero_clientes >= self.__maximo_clientes:
            print("No se pueden registrar más clientes, el gimnasio ha alcanzado su capacidad máxima.")
            return False
        
        if not nombre or not documento:
            while True:
                nombre = input("Ingrese el Nombre del Cliente : ")
                if ut.is_string(nombre, "Nombre"):
                    break
            
            while True:
                documento = input("Ingrese el Documento del Cliente : ")
                if ut.is_number(documento, "Documento"):
                    break
            
            while True:
                telefono = input("Ingrese el numero de telefono del Cliente (Enter para Omitir) : ")
                if telefono:
                    if ut.is_number(telefono, "Telefono"):
                        break
                else:
                    break
            
        else:
            if telefono and ( not ut.is_number(telefono, "Telefono")):
                return False
            if not (ut.is_string(nombre, "Nombre") and ut.is_number(documento, "Documento")):
                return False
        
        id_cliente = self.__historico_clientes + 1
        
        if not fecha_registro:
            fecha_registro = date.today().strftime("%Y-%m-%d")
        else:
            if isinstance(fecha_registro, str):
                fecha_registro = datetime.strptime(fecha_registro, "%Y-%m-%d").date()
            elif not isinstance(fecha_registro, date):
                print("Fecha de registro inválida. Debe ser un objeto date o una cadena en formato 'YYYY-MM-DD'.")
                return False
        
        # Verificar si el cliente ya está registrado
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_documento() == documento:
                print(f"\n!!! El cliente con documento {documento} ya está registrado.")
                return False
        
        nuevo_cliente = Cliente(id_cliente, nombre.lower(), documento, fecha_registro, telefono)
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
        return nuevo_cliente

    # R3
    def crear_membresia(self, cliente_encontrado: Cliente, fecha_inicio = None, fecha_fin = None, pago: bool = None):
        
        # Validaciones
        
        if cliente_encontrado.get_membresia():
            print("El cliente ya tiene membresia.")
            cliente_encontrado.info_membresia()
            return False
        
        if not fecha_inicio:
            fecha_inicio = date.today()
        else:
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            elif not isinstance(fecha_inicio, date):
                print("Fecha de inicio inválida. Debe ser un objeto date o una cadena en formato 'YYYY-MM-DD'.")
                return False
        
        if not fecha_fin:
            fecha_fin = fecha_inicio + timedelta(days=30)
        else:
            if isinstance(fecha_fin, str):
                fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            elif not isinstance(fecha_fin, date):
                print("Fecha de fin inválida. Debe ser un objeto date o una cadena en formato 'YYYY-MM-DD'.")
                return False
        
        if pago is None:
            while True: # Ciclo para Ingreso correcto del pago
                pagar = input("¿Desea pagar inmediatamente? (si/no)\nR// ")
                if ut.valid_yes_no(pagar):
                    break
            
            pago = ut.yes_no(pagar)
            
            if pago:
                self.ingreso_caja(PRECIO_MEMBRESIA)

        # Crear la membresía
        nueva_membresia = Membresia(fecha_inicio, fecha_fin, pago)
        cliente_encontrado.set_membresia(nueva_membresia)
        print(f"Membresía creada para {cliente_encontrado.get_nombre()} con ID {cliente_encontrado.get_id_cliente()}")
        print(f"Vigencia: {fecha_inicio} hasta {fecha_fin}")
        print(f"Estado: {'Pagada' if pago else 'Pendiente de pago'}")
        
        return nueva_membresia
    
    def crear_entrenador(self, nombre: str = None, especialidad: str = None, telefono: str = None):
        """
        Registra un nuevo entrenador en el gimnasio.
        
        Args:
            nombre (str): Nombre del entrenador
            especialidad (set): Conjunto de especialidades del entrenador
            telefono (str, optional): Teléfono del entrenador
        """
        
        if not nombre or not especialidad:
            while True:
                nombre = input("Ingrese el Nombre del Entrenador : ")
                if ut.is_string(nombre, "Nombre"):
                    break
            
            while True:
                especialidad = input(f"Ingrese la especialidad del Entrenador {self.__sesiones_especiales} : ").lower()
                if ut.is_string(nombre, "Especialidad"):
                    if especialidad in self.__sesiones_especiales:
                        break
                    else:
                        print(f"Especialidad no válida. Debe ser una de las siguientes: {self.__sesiones_especiales}")
            
            while True:
                telefono = input("Ingrese el numero de telefono del Entrenador (Enter para Omitir) : ")
                if telefono:
                    if ut.is_number(telefono, "Telefono"):
                        break
                else:
                    break
        else:
            if telefono and ( not ut.is_number(telefono, "Telefono")):
                return False
            if not (ut.is_string(nombre, "Nombre") and ut.is_string(especialidad, "Especialidad")):
                return False
            else:
                if not especialidad in self.__sesiones_especiales:
                    print(f"Especialidad no válida. Debe ser una de las siguientes: {self.__sesiones_especiales}")
                return False
        
        
        id_entrenador = self.__historico_entrenadores + 1
        nuevo_entrenador = Entrenador(id_entrenador, nombre.lower(), especialidad, telefono)
        self.__entrenadores+=[nuevo_entrenador]
        self.__historico_entrenadores += 1
        print(f"Entrenador {nombre} especializado en {especialidad} registrado con ID: {id_entrenador}")
        return nuevo_entrenador
    
    def crear_sesion_especial(self, entrenador, fecha: str=None, maximo_cupos: int = 25):
        """
        Crea una nueva sesión especial.
        
        Args:
            entrenador: Objeto entrenador que dirigirá la sesión
            fecha (str): Fecha de la sesión
            maximo_cupos (int, optional): Número máximo de cupos. Defaults to 25.
        """
        if not fecha:
            while True:
                fecha = input("Ingrese la fecha de la sesión especial (YYYY-MM-DD): ")
                try:
                    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                    break
                except Exception as error:
                    print("Fecha inválida. Debe ser en formato 'YYYY-MM-DD'.")
                    print(f"Error : {str(error)}")
                    continue
        
        if not entrenador:
            print("No se proporcionó un entrenador válido")
            return None
        
        id_sesion = self.__historico_sesiones + 1
        nueva_sesion = SesionEspecial(id_sesion, entrenador, fecha, maximo_cupos)
        self.__sesiones+=[nueva_sesion]
        self.__historico_sesiones += 1
        print(f"Sesión especial creada con ID: {id_sesion} para la fecha {fecha}")
        print(f"Entrenador asignado: {entrenador.get_nombre()} ({entrenador.get_especialidad()})")
        return nueva_sesion
    
    
    
    
    
    
    #? ============================== Metodos De Busqueda y Visualizacion ==============================
    
    def buscar_cliente(self, op=None):
        
        # Buqueda por ID, Nombre o Documento
        
        print("\n======= Buscar Cliente =======")
        print(30*"=")
        print("Seleccione el tipo de búsqueda :")
        print("1. Buscar por ID")
        print("2. Buscar por Nombre") # Listar si hay mas de 1 cliente con el mismo nombre
        print("3. Buscar por Documento")
        print("Enter para salir")
        opcion_busqueda = input("Seleccione una opción : ")
        print(30*"=")
        if opcion_busqueda not in ["1", "2", "3", ""]:
            print("Saliendo del menú de búsqueda...")
            return None
        
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
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
                if not cliente_encontrado: # Si no se encontró el cliente, informar al usuario
                    print(f"No se encontró un cliente con ID {id_cliente}.")
                    return
            case "2":
                while True:
                    nombre_cliente = input("Ingrese el nombre del cliente: ")
                    if ut.is_string(nombre_cliente, "Nombre"):
                        break
                for cliente in self.__clientes:
                    if cliente is not None and cliente.get_nombre() == nombre_cliente.lower():
                        cliente_encontrado = cliente
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
                if not cliente_encontrado:
                    print(f"No se encontró un cliente con nombre {nombre_cliente}.")
                    return
            case "3":
                while True:
                    documento = input("Ingrese el documento del cliente: ")
                    if ut.is_number(documento, "Documento"):
                        break
                for cliente in self.__clientes:
                    if cliente is not None and cliente.get_documento() == documento:
                        cliente_encontrado = cliente
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
                if not cliente_encontrado:
                    print(f"No se encontró un cliente con documento {documento}.")
                    return
            case "":
                print("Saliendo del menú de búsqueda...")
                
        if cliente_encontrado is None:
            print("No se encontró ningún cliente.")
            return
        else:
            return cliente_encontrado


    def consultar_membresia(self, cliente_encontrado: Cliente):
        if cliente_encontrado.get_membresia() is None:
            print(f"El cliente {cliente_encontrado.get_nombre()} no tiene una membresía activa.")
            return
        else:
            membresia_encontrada = cliente_encontrado.get_membresia()
        
        # Mostrar información de la membresía
        print(f"\n=== Información de Membresía ===")
        print(f"Cliente: {cliente_encontrado.get_nombre()}")
        print(f"Estado de pago: {'Pagada' if membresia_encontrada.get_pago() else 'Pendiente'}") 
        print(f"Fecha de inicio: {membresia_encontrada.get_fecha_inicio()}")
        print(f"Fecha de fin: {membresia_encontrada.get_fecha_fin()}")
        # print(f"Días restantes: {}")
        print("="*30)
        
        return membresia_encontrada
        
    
    def buscar_entrenador(self, id_entrenador: int = None):
        """
        Busca un entrenador por su ID.
        
        Args:
            id_entrenador (int): ID del entrenador a buscar
        
        Returns:
            Entrenador: Objeto Entrenador si se encuentra, None si no se encuentra
        """
        
        if id_entrenador is None:
            while True:
                id_entrenador = input("Ingrese el ID del entrenador: ")
                if ut.is_number(id_entrenador, "ID"):
                    id_entrenador = int(id_entrenador)
                    break
        
        for entrenador in self.__entrenadores:
            if entrenador.get_id_entrenador() == id_entrenador:
                print(f"Entrenador : ID: {entrenador.get_id_entrenador()}, Nombre: {entrenador.get_nombre()}, Especialidad: {entrenador.get_especialidad()}")
                return entrenador
        print(f"No se encontró un entrenador con ID {id_entrenador}.")
        return None
    
    def visualizar_clientes(self):      
        print("\n=== Clientes Registrados ===")
        total_clientes = 0
        for cliente in self.__clientes:
            if cliente is not None:
                total_clientes += 1
                print(f"ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
        
        print(f"\nNumero de Clientes Registradas : {total_clientes}")
    
    def visualizar_membresias(self):
        print("\n=== Membresías Registradas ===")
        total_membresias = 0
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_membresia() is not None:
                membresia = cliente.get_membresia()
                total_membresias += 1
                print(f""" - ID: {cliente.get_id_cliente()}, Cliente {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Registrado: {cliente.get_fecha_registro_c()}
                        Membresia => Estado: { 'Paga' if membresia.get_pago() else 'Pendiente' }, Fecha Inicio: {membresia.get_fecha_inicio()}, Fecha Fin: {membresia.get_fecha_fin()}, Dias Restantes: {membresia.calcular_dias_restantes()} \n""")
        
        print(f"\nNumero de Membresias Registradas : {total_membresias}")
    
    
    def mostrar_entrenadores(self):
        if not self.__entrenadores or len(self.__entrenadores) == 0:
            print("No hay entrenadores registrados.")
            return
        
        print("\n=== Entrenadores Registrados ===")
        total_entrenadores = 0
        for entrenador in self.__entrenadores:
            entrenador.mostrar_info()
            total_entrenadores += 1
            
        print(f"\nNumero de Entrenadores Registrados : {total_entrenadores}")
        
        id_entrenador = input("\nSeleccione un Entrenador o Enter para continuar... ")
        
        if id_entrenador == "":
            print("Saliendo del menú de entrenadores...")
            return
        else:
            # Validar que el ID ingresado sea un número
            if not ut.is_number(id_entrenador, "ID de Entrenador"):
                print("ID de entrenador inválido. Debe ser un número.")
                return
            if int(id_entrenador) < 1:
                print(f"ID de entrenador inválido.")
                return
            
            id_entrenador = int(id_entrenador)
            # Buscar el entrenador por ID
            entrenador = self.buscar_entrenador(id_entrenador)
            if not entrenador:
                print(f"No se encontró un entrenador con ID {id_entrenador}.")
            else:
                return entrenador
    
    
    def mostrar_sesiones(self):
        """Muestra todas las sesiones especiales disponibles"""
        total_sesiones = 0
        if not self.__sesiones or len(self.__sesiones) == 0:
            print("No hay sesiones especiales programadas.")
            return
        else:
            print("\n=== Todas las Sesiones Especiales ===")
            for sesion in self.__sesiones:
                total_sesiones += 1
                entrenador = sesion.mostrar_info()
                entrenador.mostrar_info()
        
        id_sesion = input("\nSeleccione una Sesion o Enter para continuar... ")
        
        if id_sesion == "":
            print("Saliendo del menú de sesiones...")
            return
        else:
            # Validar que la sesión ingresada sea un número
            if not ut.is_number(id_sesion, "ID de Sesión"):
                print("ID de sesión inválido. Debe ser un número.")
                return
            if int(id_sesion) < 1:
                print(f"ID de sesión inválido. Debe estar entre 1 y {total_sesiones}.")
                return
            
            id_sesion = int(id_sesion)
            # Buscar la sesión por ID
            for sesion in self.__sesiones:
                if sesion.get_id_sesion() == id_sesion:
                    print(f"\n===== Sesion Seleccionada ====")
                    print(f"Sesión ID: {sesion.get_id_sesion()}, Fecha: {sesion.get_fecha()}, Cupos disponibles: {sesion.get_cupos_disponibles()}")
                    entrenador = sesion.mostrar_info()
                    entrenador.mostrar_info()
                    return sesion
            print(f"No se encontró una sesión con ID {id_sesion}.")
            return
    
    
    
    #? ============================== Metodos de Modificacion ==============================

    def ingreso_caja(self, efectivo: float, motivo:str=None): #pendieten pedir el tipo para el registro en persitencia
        """_summary_
            Modifica el efectivo del gimnasio.
        """
        # Registrar el ingreso en formato: fecha;hora;tipo;efectivo
        fecha = datetime.now().strftime('%Y-%m-%d')
        hora = datetime.now().strftime('%H:%M:%S')
        tipo = motivo if motivo else "Ingreso"
        registro = f"{fecha};{hora};{tipo};{float(efectivo):,}\n"
        
        print(f"Efectivo actual: ${self.__efectivo:,} + ${float(efectivo):,}")
        self.__efectivo += float(efectivo)
        print(f"Efectivo actualizado a: ${self.__efectivo:,}")
        
        with open("registros/Caja.txt", "a") as caja_file:
            caja_file.write(registro)
        

    
    def pagar_membresia(self, membresia_encontrada: Membresia):
        if membresia_encontrada.get_pago():
            print("La membresía ya ha sido pagada.")
            return
        else:
            print(f"El cliente tiene una membresía que aún no ha sido pagada.")
            self.ingreso_caja(PRECIO_MEMBRESIA)
            membresia_encontrada.set_pago(True)
            print(f"Pago realizado exitosamente. Monto: ${PRECIO_MEMBRESIA:,}")
    
    def pago_ingreso_unico(self, cliente_encontrado: Cliente):
        pass
    
    def registrar_entrada(self, cliente_encontrado: Cliente):
        pass

    def agendar_sesion(self, cliente, id_sesion: int= None):
        """
        Permite a un cliente inscribirse en una sesión especial.
        
        Args:
            cliente: Objeto Cliente que se quiere inscribir
        """
        if not self.__sesiones or len(self.__sesiones) == 0:
            print("No hay sesiones especiales disponibles.")
            return
        
        if id_sesion is not None:
            # Buscar la sesión por ID
            for sesion in self.__sesiones:
                if sesion.get_id_sesion() == id_sesion:
                    if sesion.get_cupos_disponibles() > 0:
                        # Inscribir en la sesión (esto actualiza la sesión)
                        if sesion.inscribir_cliente(cliente):
                            print(f"¡Inscripción exitosa en la sesión del {sesion.get_fecha()}!")
                        else:
                            print("No se pudo inscribir en la sesión. Verifique los datos.")
                        return
                    else:
                        print("No hay cupos disponibles para esta sesión.")
                        return
            print(f"No se encontró una sesión con ID {id_sesion}.")
            return
        else:
            print("\n=== Sesiones Especiales Disponibles ===")
            sesiones_disponibles = []
            
            for sesion in self.__sesiones:
                if sesion.get_cupos_disponibles() > 0:
                    sesiones_disponibles+=[sesion]
                    # Obtener el entrenador directamente del objeto sesión
                    entrenador = sesion.get_entrenador()
                    
                    print(f"{len(sesiones_disponibles)}. Sesión ID: {sesion.get_id_sesion()}")
                    print(f"   Fecha: {sesion.get_fecha()}")
                    print(f"   Entrenador: {entrenador.get_nombre() if entrenador else 'No encontrado'}")
                    print(f"   Cupos disponibles: {sesion.get_cupos_disponibles()}")
                    
            print(f"\n\nSesiones Disponibles :{len(sesiones_disponibles)}")
            
            if not sesiones_disponibles:
                print("No hay sesiones con cupos disponibles.")
                return
            
            sesion_ids = [sesion.get_id_sesion() for sesion in sesiones_disponibles]
            
            while True:
                id_sesion = input("Ingrese el ID de la sesión a la que desea inscribirse (o '0' para cancelar): ")
                if ut.is_number(id_sesion, "ID"):
                    id_sesion = int(id_sesion)
                    if id_sesion == 0:
                        print("Operación cancelada.")
                        return
                        # Validar que el id_sesion esté en las sesiones disponibles
                    else:
                        if id_sesion not in sesion_ids:
                            print("El ID de sesión ingresado no está en las sesiones disponibles.")
                            continue
                        else:
                            break
                else:
                    print("Por favor ingrese un número válido.")
                    
            # Buscar la sesión seleccionada
            for sesion in sesiones_disponibles:
                if sesion.get_id_sesion() == id_sesion:
                    if sesion.inscribir_cliente(cliente):
                        print(f"¡Inscripción exitosa en la sesión del {sesion.get_fecha()}!")
                        break
                    else:
                        print("No se pudo inscribir en la sesión. Verifique los datos.")


    #! ============================== Metodos de Eliminacion ==============================
    
    def eliminar_entrenador(self, id_entrenador: int=None):
        if not self.__entrenadores:
            print("No hay entrenadores registrados para eliminar.")
            return
        
        if id_entrenador is None:
            while True:
                id_entrenador = input("Ingrese el ID del entrenador: ")
                if ut.is_number(id_entrenador, "ID"):
                    id_entrenador = int(id_entrenador)
                    break
        
        for i in range(len(self.__entrenadores)):
            if self.__entrenadores[i].get_id_entrenador() == id_entrenador:
                print(f"Entrenador con ID {id_entrenador} y nombre {self.__entrenadores[i].get_nombre()}.")
                confirmar = input("¿Está seguro de eliminar este entrenador? (si/no): ").strip().lower()
                if confirmar == 'si':
                    print(f"Eliminando entrenador {self.__entrenadores[i].get_nombre()}...")
                    self.__entrenadores.pop(i)
                    
                    # Buscar sesiones en las que esta
                    for sesion in self.__sesiones:
                        if sesion.get_entrenador() and sesion.get_entrenador().get_id_entrenador() == id_entrenador:
                            print(f"Eliminando sesión especial con ID {sesion.get_id_sesion()} que tenía al entrenador eliminado.")
                            self.eliminar_sesion(sesion)
                    
                else:
                    print("Eliminación cancelada.")
                break
        
    def eliminar_sesion(self, sesion=None):
        if not self.__sesiones or len(self.__sesiones) == 0:
            print("No hay sesiones especiales programadas para eliminar.")
            return
        if sesion is None:
            while True:
                id_sesion = input("Ingrese el ID de la sesión a eliminar: ")
                if ut.is_number(id_sesion, "ID"):
                    id_sesion = int(id_sesion)
                    break
        else:
            id_sesion = sesion.get_id_sesion()
        
        # Buscar la sesión por ID
        for i in range(len(self.__sesiones)):
            if self.__sesiones[i].get_id_sesion() == id_sesion:
                print(f"Sesión especial con ID {id_sesion} y fecha {self.__sesiones[i].get_fecha()}.")
                while True:
                    confirmacion = input("¿Estas seguro de eliminar el entrenador? (si/no): ")
                    if ut.valid_yes_no(confirmacion):
                        break
                if ut.yes_no(confirmacion)
                    print(f"Eliminando sesión especial del {self.__sesiones[i].get_fecha()}...")
                    
                    # Eliminamos la referencia del entrenador de la sesión
                    self.__sesiones[i].set_entrenador(None)
                    # Eliminamos las referencias de clientes inscritos
                    self.__sesiones[i].editar_inscritos(0)
                    # Y finalmente eliminamos la sesión del array
                    self.__sesiones.pop(i)
                    return True
                else:
                    print("Eliminación cancelada.")
                    return False
                break



    #! ============================== Metodos Opcionales ==============================


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
    
    #* ============================== Exportar e Importar Datos ==============================
    
    def exportar_datos_json(self, nombre_archivo: str = None):
        """
        Guarda todos los datos de clientes y sus membresías en un archivo JSON.
        
        Args:
            nombre_archivo (str, optional): Nombre del archivo JSON. Si no se especica se genera automáticamente con la fecha actual.
        
        Returns:
            str: Ruta del archivo creado
        """
        # Generar nombre de achivo si no se proporciona
        if nombre_archivo is None:
            fecha_actual = date.today().strftime("%Y%m%d")
            nombre_archivo = f"datos_gimnasio_{fecha_actual}.json"
        nombre_archivo = f"registros/{nombre_archivo}"
        
        # Crear estructura de datos para exportar
        datos_exportar = {
            "gimnasio": {
                "nombre": self.__nombre,
                "direccion": self.__direccion,
                "telefono": self.__telefono,
                "correo": self.__correo_electronico,
                "efectivo": self.__efectivo
            },
            "estadisticas": {
                "total_clientes": self.__numero_clientes,
                "historico_clientes": self.__historico_clientes,
                "fecha_exportacion": date.today().strftime("%Y-%m-%d")
            },
            "clientes": []
        }
        
        # Procesar cada cliente registrado
        for i in range(self.__numero_clientes):
            cliente = self.__clientes[i]
            if cliente is not None:
                # Datos básicos del cliente
                datos_cliente = {
                    "id_cliente": cliente.get_id_cliente(),
                    "nombre": cliente.get_nombre(),
                    "documento": cliente.get_documento(),
                    "telefono": cliente.get_telefono(),
                    "fecha_registro": cliente.get_fecha_registro_c(),
                    "membresia": None
                }
                
                # Agregar datos de membresía si existe
                membresia = cliente.get_membresia()
                if membresia is not None:
                    datos_cliente["membresia"] = {
                        "pago": membresia.get_pago(),
                        "fecha_inicio": membresia.get_fecha_inicio(),
                        "fecha_fin": membresia.get_fecha_fin(),
                        "dias_restantes": membresia.calcular_dias_restantes()
                    }
                
                datos_exportar["clientes"].append(datos_cliente)
        
        # Guardar archivo JSON
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos_exportar, archivo, indent=4, ensure_ascii=False)
            
            print(f"✓ Datos exportados exitosamente a: {nombre_archivo}")
            print(f"✓ Total de clientes exportados: {len(datos_exportar['clientes'])}")
            
            return nombre_archivo
            
        except Exception as error:
            print(f"✗ Error al guardar el archivo JSON: {str(error)}")
            return None
    
    def cargar_datos_json(self, nombre_archivo: str):
        """
        Carga datos de clientes desde un archivo JSON (método complementario).
        
        Args:
            nombre_archivo (str): Nombre del archivo JSON a cargar
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario
        """
        
        nombre_archivo = f"registros/{nombre_archivo}"
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            print(f"✓ Archivo {nombre_archivo} cargado exitosamente")
            print(f"✓ Datos del gimnasio: {datos['gimnasio']['nombre']}")
            print(f"✓ Total de clientes en archivo: {len(datos['clientes'])}")
            print(f"✓ Fecha de exportación: {datos['estadisticas']['fecha_exportacion']}")
            
            return datos
            
        except FileNotFoundError:
            print(f"✗ Archivo {nombre_archivo} no encontrado")
            return None
        except json.JSONDecodeError:
            print(f"✗ Error al leer el archivo JSON: formato inválido")
            return None
        except Exception as error:
            print(f"✗ Error al cargar el archivo: {str(error)}")
            return None
    
    def cargar_clientes(self, nombre_archivo=None):
        if nombre_archivo is None:
            print("Archivos disponibles en la carpeta 'registros':")
            archivos = [f for f in os.listdir("registros") if f.endswith(".txt")]
            for idx, archivo in enumerate(archivos, 1):
                print(f"{idx}. {archivo}")
            nombre_archivo = input("Ingrese el nombre del archivo a cargar (.txt separado por ';'): ")
        if nombre_archivo is None:
            nombre_archivo = input("Ingrese el nombre del archivo a cargar (.txt separado por ';'): ")
        if nombre_archivo == 0 or nombre_archivo == "0" or nombre_archivo == "":
            print("Operacion cancelada.")
            return False
        if nombre_archivo == "1" or nombre_archivo == 1:
            nombre_archivo = "clientes.txt"
        
        nombre_archivo = f"registros/{nombre_archivo}"
        
        print("\n")
        print("="*40)
        print(f"📂 Cargando datos desde el archivo: {nombre_archivo}\n")
        
        try:
            with open(nombre_archivo, "r") as archivo:
                lineas = archivo.readlines()
                rows = len(lineas)
                
                if rows == 0:
                    print("✗ El archivo está vacío.")
                    return False
                
                # Validar formato del archivo (debe tener encabezados)
                primera_linea = lineas[0].strip().split(";")
                columns = len(primera_linea)
                print(f"Número de líneas : {rows}")
                print(f"Número de columnas : {columns}")
                print(f"Encabezados detectados: {primera_linea}")
                
                # Validar que tenga el formato esperado para clientes (7 columnas)
                if columns != 7:
                    print(f"⚠️  ADVERTENCIA: Este archivo tiene {columns} columnas.")
                    print("""📋 Formato esperado para clientes : 
    Nombre;Documento;Telefono;Fecha Registro;Membresia:Pago;Membresia:Fecha Inicio;Membresia:Fecha Fin""")
                    print("📋 Formato detectado:", ";".join(primera_linea))
                
                # Verificar si hay líneas de datos (más de solo encabezados)
                if rows <= 1:
                    print("✗ El archivo solo contiene encabezados, no hay datos para cargar.")
                    return False
                    
        except FileNotFoundError:
            print(f"✗ Archivo {nombre_archivo} no encontrado.")
            return False
        except Exception as error:
            print(f"✗ Error al leer el archivo: {str(error)}")
            return False

        # Contadores para estadísticas
        lineas_error = []
        clientes_cargados = 0
        membresias_cargadas = 0
        lineas_procesadas = 0
        
        print(f"\n📥 Iniciando carga de {rows-1} líneas de datos...")
        
        for i in range(1, rows):
            lineas_procesadas += 1
            linea = lineas[i].strip().split(";")
            
            # Validar que la línea tenga suficientes columnas
            if len(linea) < 7:
                print(f"✗ Línea {i+1} malformada (solo {len(linea)} columnas): {lineas[i].strip()}")
                lineas_error.append(i+1)
                continue

            try:
                print("="*30)
                print(f"Procesando línea {i+1}/{rows-1}: {linea}")
                
                # Validación para teléfono: si es "0", "None", "none" o vacío, se convierte a None
                telefono = linea[2]
                if telefono and telefono.lower() in ["0", "none", ""]:
                    telefono = None
                
                # Crear el cliente primero
                cliente_creado = self.crear_cliente(
                    nombre=linea[0],
                    documento=linea[1],
                    telefono=telefono,
                    fecha_registro=datetime.strptime(linea[3], "%Y-%m-%d").date()
                )
                
                if cliente_creado:
                    clientes_cargados += 1
                    pago_bool = linea[4].strip().lower() == 'true'
                    membresia_creada = self.crear_membresia(
                        cliente_encontrado=cliente_creado,
                        fecha_inicio=datetime.strptime(linea[5], "%Y-%m-%d").date(),
                        fecha_fin=datetime.strptime(linea[6], "%Y-%m-%d").date(),
                        pago=pago_bool
                    )
                    if membresia_creada:
                        membresias_cargadas += 1
                        print(f"✓ Cliente y membresía cargados exitosamente.")
                    else:
                        print(f"⚠️  Cliente creado pero falló la membresía.")
                else:
                    lineas_error.append(i+1)
                    print(f"✗ No se pudo crear el cliente {linea[0]} con documento {linea[1]}.")
                    continue
                
            except Exception as error:
                print(f"✗ Error procesando línea {i+1}: {str(error)}")
                lineas_error.append(i+1)
                continue
        
        # Mostrar estadísticas finales
        print("="*60)
        print("📊 RESUMEN DE CARGA:")
        print(f"📥 Líneas procesadas: {lineas_procesadas}")
        print(f"✅ Clientes cargados exitosamente: {clientes_cargados}")
        print(f"✅ Membresias cargadas exitosamente: {membresias_cargadas}")
        print(f"❌ Líneas con errores: {len(lineas_error)}")
        if lineas_error:
            print(f"🔍 Líneas con errores: {lineas_error}")
        print(f"📈 Tasa de éxito: {(membresias_cargadas/lineas_procesadas)*100:.1f}%" if lineas_procesadas > 0 else "0%")
        print("="*60)
        
        return membresias_cargadas > 0  # Retorna True si se cargó al menos una línea
    
    def exportar_clientes(self):
        nombre_archivo = f"registros/clientes_{date.today().strftime('%Y%m%d')}.txt"
        
        with open(nombre_archivo, "w",) as archivo:
            archivo.write("Nombre;Documento;Telefono;Fecha Registro;Membresia:Pago;Membresia:Fecha Inicio;Membresia:Fecha Fin\n")
            for i in self.__clientes:
                if i is not None:
                    membresia = i.get_membresia()
                    if membresia:
                        archivo.write(f"{i.get_nombre()};{i.get_documento()};{i.get_telefono()};{i.get_fecha_registro_c()};{membresia.get_pago()};{membresia.get_fecha_inicio()};{membresia.get_fecha_fin()}\n")
                    else:
                        archivo.write(f"{i.get_nombre()};{i.get_documento()};{i.get_telefono()};{i.get_fecha_registro_c()};None;None;None\n")



