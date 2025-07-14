import numpy as np
import json
from datetime import date, timedelta, datetime
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
        __maximo_clientes (int): Número máximo de clientes que el gimnasio puede registrar. Defaults to 50.
        __numero_clientes (int): Contador de clientes registrados.
        __historico_clientes (int): Contador de clientes históricos.
        __clientes (np.ndarray): Array que almacena los clientes registrados.
        __historico_entrenadores (int): Contador de entrenadores históricos.
        __entrenadores (list): Lista que almacena los objetos Entrenadores de los entrenadores registrados.
        __historico_sesiones (int): Contador de sesiones especiales históricas.
        __sesiones (list): Lista que almacena los objetos SescionEspecial de las sesiones especiales registradas.
        __sesiones_especiales (list): Lista de tipos de sesiones especiales disponibles.
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

    def ver_info(self):
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
                self.ingreso_caja(PRECIO_MEMBRESIA, "Membresia")

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
    
    def crear_sesion_especial(self, entrenador=None, fecha: str=None, maximo_cupos: int = 25,id_entrenador: int = None):
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
                except Exception as e:
                    print("Fecha inválida. Debe ser en formato 'YYYY-MM-DD'.")
                    print(f"Error : {str(e)}")
                    continue
        
        if not entrenador:
            if not id_entrenador:
                entrenador = self.mostrar_entrenadores()
                if entrenador is None:
                    print("No se ha seleccionado un entrenador.")
                    return None
                else:
                    id_entrenador = entrenador.get_id_entrenador()
            else:
                entrenador = self.buscar_entrenador(id_entrenador)
                if entrenador is None:
                    print(f"No se encontró un entrenador con ID {id_entrenador}.")
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
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_regitro()}")
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
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_regitro()}")
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
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_regitro()}")
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
                print(f"ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_regitro()}")
        
        print(f"\nNumero de Clientes Registradas : {total_clientes}")
        
        id_cliente = input("\nSelecione un Cliente o Enter para continuar... ")
        if id_cliente == "":
            print("Saliendo del menú de clientes...")
            return None
        else:
            # Validar que el ID ingresado sea un número
            if not ut.is_number(id_cliente, "ID de Cliente"):
                print("ID de cliente inválido. Debe ser un número.")
                return None
            if int(id_cliente) < 1:
                print(f"ID de cliente inválido.")
                return None
            
            id_cliente = int(id_cliente)
            # Buscar el cliente por ID
            for cliente in self.__clientes:
                if cliente is not None and cliente.get_id_cliente() == id_cliente:
                    print(f"\n===== Cliente Seleccionado ====")
                    print(f"Cliente ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_regitro()}")
                    return cliente
            print(f"No se encontró un cliente con ID {id_cliente}.")
            return None
    
    def visualizar_membresias(self):
        print("\n=== Membresías Registradas ===")
        total_membresias = 0
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_membresia() is not None:
                membresia = cliente.get_membresia()
                total_membresias += 1
                dias_restantes = membresia.calcular_dias_restantes()
                print(f""" - ID: {cliente.get_id_cliente()}, Cliente {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Registrado: {cliente.get_fecha_regitro()}
                        Membresia => Estado: { 'Paga' if membresia.get_pago() else 'Pendiente' }, Fecha Inicio: {membresia.get_fecha_inicio()}, Fecha Fin: {membresia.get_fecha_fin()}, Dias Restantes: {dias_restantes if dias_restantes < 0 else "Vencida"} \n""")
        
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
                if entrenador:
                    entrenador.mostrar_info()
                else:
                    print("No se encontró un entrenador para esta sesión.")
            print(f"\nNumero de Sesiones Especiales Registradas : {total_sesiones}")
        
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
        # Pensar si es necesario el Cliente quien paga, o si es necesario el ID del cliente
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
            self.ingreso_caja(PRECIO_MEMBRESIA,"PagoMembresia")
            membresia_encontrada.set_pago(True)
            print(f"Pago realizado exitosamente. Monto: ${PRECIO_MEMBRESIA:,}")
    
    def pago_ingreso_unico(self, cliente_encontrado: Cliente):
        self.ingreso_caja(PRECIO_ENTRADA_UNICA, "PagoIngresoUnico")
        cliente_encontrado.registrar_entrada("IngresoUnico")
    
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
                print("Enter o '0' para cancelar la operación.")
                id_sesion = input("Ingrese el ID de la sesión a la que desea inscribirse : ")
                
                if id_sesion == "":
                    print("Operación cancelada.")
                    return
                
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
    
    def eliminar_cliente(self, id_cliente: int= None):
        
        if id_cliente is None:
            while True:
                id_cliente = input("Ingrese el ID del Cliente: ")
                if ut.is_number(id_cliente, "ID"):
                    id_cliente = int(id_cliente)
                    break
        
        for i in range(len(self.__clientes)):
            if self.__clientes[i].get_id_cliente() == id_cliente:
                print(f"Cliente con ID {id_cliente} y nombre {self.__clientes[i].get_nombre_c()}.")
                confirmar = input("¿Está seguro de eliminar este Cliente? (si/no): ").strip().lower()
                if confirmar == 'si':
                    self.__clientes.pop(i)
                else:
                    print("Eliminación cancelada.")
                break
            
    def eliminar_membresia(self, id_cliente: int= None):
        
        if id_cliente is None:
            while True:
                id_cliente = input("Ingrese el ID del Cliente: ")
                if ut.is_number(id_cliente, "ID"):
                    id_cliente = int(id_cliente)
                    break
        
        for i in range(len(self.__clientes)):
            if self.__clientes[i].get_id_cliente() == id_cliente:
                cliente = self.__clientes[i]
                if cliente.get_membresia() is None:
                    print(f"El cliente {cliente.get_nombre_c()} no tiene una membresía activa.")
                    return
                else:
                    print(f"Cliente con ID {id_cliente} y nombre {cliente.get_nombre_c()}.")
                    confirmar = input("¿Está seguro de eliminar la membresía de este Cliente? (si/no): ").strip().lower()
                    if confirmar == 'si':
                        cliente.set_membresia(None)
                        print(f"Membresía del cliente {cliente.get_nombre_c()} eliminada.")
                    else:
                        print("Eliminación cancelada.")
                break     
    
    
    
    
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
                print(f"Tambien se eliminarán las sesiones especiales asociadas a este entrenador.")
                print(f"===== Sesiones asociadas =====")
                total_sesiones = 0
                for sesion in self.__sesiones:
                    if sesion.get_entrenador() and sesion.get_entrenador().get_id_entrenador() == id_entrenador:
                        total_sesiones += 1
                        dias_restantes = sesion.calcular_dias_restantes()
                        estado = f"{dias_restantes} días restantes" if dias_restantes is not None else "Ya pasó"
                        print(f" - Sesión ID: {sesion.get_id_sesion()}, Fecha: {sesion.get_fecha()}, {estado}")
                print(f"Total de sesiones asociadas: {total_sesiones}")
                while True:
                    confirmacion = input("¿Estas seguro de eliminar el entrenador? (si/no): ")
                    if ut.valid_yes_no(confirmacion):
                        break
                if ut.yes_no(confirmacion):
                    print(f"Eliminando entrenador {self.__entrenadores[i].get_nombre()}...")
                    self.__entrenadores.pop(i)
                    
                    # Buscar sesiones en las que esta
                    for sesion in self.__sesiones:
                        if sesion.get_entrenador() and sesion.get_entrenador().get_id_entrenador() == id_entrenador:
                            print(f"Eliminando sesión especial con ID {sesion.get_id_sesion()} que tenía al entrenador eliminado.")
                            if not self.eliminar_sesion(sesion): # Si la sesion no se elimino, hay que eliminar la referencia del entrenador
                                sesion.set_entrenador(None)
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
            if isinstance(sesion, SesionEspecial):
                id_sesion = sesion.get_id_sesion()
            else:
                id_sesion = sesion
        
        # Buscar la sesión por ID
        for i in range(len(self.__sesiones)):
            sesion = self.__sesiones[i]
            if sesion.get_id_sesion() == id_sesion:
                dias_restantes = sesion.calcular_dias_restantes()
                estado = f"{dias_restantes} días restantes" if dias_restantes is not None else "Ya pasó"
                print(f"Sesión especial con ID: {sesion.get_id_sesion()}, Fecha: {sesion.get_fecha()}, {estado}")
                while True:
                    confirmacion = input("¿Estas seguro de eliminar la sesion? (si/no): ")
                    if ut.valid_yes_no(confirmacion):
                        break
                if ut.yes_no(confirmacion):
                    print(f"Eliminando sesión especial del {sesion.get_fecha()}...")
                    
                    # Eliminamos la referencia del entrenador de la sesión
                    sesion.set_entrenador(None)
                    # Eliminamos las referencias de clientes inscritos
                    print("Eliminando inscritos...")
                    sesion.editar_inscritos(0)
                    # Y finalmente eliminamos la sesión del array
                    print("Eliminando sesión...")
                    self.__sesiones.pop(i)
                    return True
                else:
                    print("Eliminación cancelada.")
                    return False
                break



    #! ============================== Metodos de Analisis ==============================
    
    def seguimiento_membresias(self):
        # Listas para categorizar
        membresias_en_deuda = []
        membresias_por_vencer = []  # ≤ 7 días
        membresias_vencidas = []    # < 0 días
        clientes_sin_membresia = []
        
        for i in range(self.__maximo_clientes):
            cliente = self.__clientes[i]
            if cliente is not None:
                membresia = cliente.get_membresia()
                if membresia is None:
                    clientes_sin_membresia.append(cliente)
                else:
                    dias_restantes = membresia.calcular_dias_restantes()
                    if dias_restantes < 0:
                        membresias_vencidas.append(cliente)
                    elif dias_restantes <= 7:
                        membresias_por_vencer.append(cliente)
                    elif not membresia.get_pago():
                        membresias_en_deuda.append(cliente)
        
        print("\n====== CONTROL DE MEMBRESÍAS ======")
        print("="*50)
        print("\n=== CLIENTES SIN MEMBRESÍA ===")
        print(f"Total de clientes sin membresía: {len(clientes_sin_membresia)}")
        if clientes_sin_membresia:
            print("Clientes sin membresía:")
            for cliente in clientes_sin_membresia:
                print(f"    - ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}")
        print("\n===== MEMBRESÍAS EN DEUDA ====")
        print(f"Total de membresías en deuda: {len(membresias_en_deuda)}")
        if membresias_en_deuda:
            print("Clientes con membresías en deuda:")
            for cliente in membresias_en_deuda:
                print(f"    - ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}")
        print("\n==== MEMBRESÍAS POR VENCER ===")
        print(f"Total de membresías por vencer: {len(membresias_por_vencer)}")
        if membresias_por_vencer:
            print("Clientes con membresías por vencer:")
            for cliente in membresias_por_vencer:
                dias_restantes = cliente.get_membresia().calcular_dias_restantes()
                print(f"    - ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Días restantes: {dias_restantes}")
        print("\n===== MEMBRESÍAS VENCIDAS ====")
        print(f"Total de membresías vencidas: {len(membresias_vencidas)}")
        if membresias_vencidas:
            print("Clientes con membresías vencidas:")
            for cliente in membresias_vencidas:
                dias_restantes = cliente.get_membresia().calcular_dias_restantes()
                print(f"    - ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Días vencida: {dias_restantes}")
        
        # Liberamos Memoria
        
        del membresias_en_deuda
        del membresias_por_vencer
        del membresias_vencidas
        del clientes_sin_membresia


    def analisis_financiero(self):
        """
        Descripción	El sistema debe permitir generar un análisis financiero. Este análisis incluye ingresos por membresías y ingresos por entradas únicas.
        Imprimimos los meses
        Entrada : Mes del Análisis
        Salida : 
            -   Ingreso por dia y por monto (Membresia y Ingreso Unico)
        """
        print("\n=== ANÁLISIS FINANCIERO ===")
        
        registro_caja = "registros/Caja.txt"  # Formato: fecha;hora;tipo;efectivo
        
        meses_disponibles = []
        
        with open(registro_caja, "r", encoding='utf-8') as archivo:
            for linea in archivo:
                datos = linea.strip().split(";")
                if len(datos) >= 4:
                    fecha = datos[0]  # Formato YYYY-MM-DD
                    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                    mes_año = fecha_obj.strftime("%m")  # Formato YYYY-MM
                    # Solo agregar si no está ya en la lista (evitar duplicados)
                    if mes_año not in meses_disponibles:
                        meses_disponibles+=[mes_año]
        
        if not meses_disponibles:
            print("❌ No se encontraron registros de entradas en el archivo.")
            return
        
        # Mostrar meses disponibles y permitir selección
        meses_lista = sorted(meses_disponibles, reverse=True)  # Más recientes primero
        
        print(f"\nMeses con registros disponibles:")
        print("="*40)
        print(meses_lista)
        
        # 1. Solicitar mes y año
        while True:
            mes = input("Ingrese el número del mes (1-12) o Enter para cancelar: ")
            if mes == "":
                print("Operación cancelada.")
                return
            if ut.is_number(mes, "Mes"):
                mes = int(mes)
                if mes >= 1 and mes <= 12:
                    break
        
        while True:
            año = input("Ingrese el año (ej: 2025): ")
            if ut.is_number(año, "Año"):
                año = int(año)
                if año >= 2020 and año <= 2030:
                    break
        
        print(f"\nGenerando análisis financiero para: {mes}/{año}")
        print("="*50)
        
        # 2. Contadores para el análisis
        total_ingresos = 0.0
        ingresos_membresia = 0.0
        ingresos_entrada_unica = 0.0
        cantidad_membresias = 0
        cantidad_entradas = 0
        ingresos_por_dia = {}
        
        # 3. Leer archivo de caja y procesar datos del mes
        with open(registro_caja, "r", encoding='utf-8') as archivo:
            for linea in archivo:
                datos = linea.strip().split(";")
                if len(datos) >= 4:
                    fecha = datos[0]  # YYYY-MM-DD
                    tipo = datos[2]   # Tipo de transacción
                    monto = float(datos[3].replace(",", ""))  # Monto
                    
                    # Extraer año y mes de la fecha
                    partes_fecha = fecha.split("-")
                    año_transaccion = int(partes_fecha[0])
                    mes_transaccion = int(partes_fecha[1])
                    dia_transaccion = int(partes_fecha[2])
                    
                    # Solo procesar si es del mes y año seleccionado
                    if año_transaccion == año and mes_transaccion == mes:
                        total_ingresos += monto
                        
                        # Clasificar por tipo de ingreso
                        if tipo in ["Membresia", "PagoMembresia"]:
                            ingresos_membresia += monto
                            cantidad_membresias += 1
                        elif tipo in ["PagoIngresoUnico", "IngresoUnico"]:
                            ingresos_entrada_unica += monto
                            cantidad_entradas += 1
                        
                        # Agrupar por día
                        if dia_transaccion in ingresos_por_dia:
                            ingresos_por_dia[dia_transaccion] += monto
                        else:
                            ingresos_por_dia[dia_transaccion] = monto
        
        # 4. Mostrar resultados
        print(f"\nRESUMEN FINANCIERO DEL MES:")
        print(f"    Total de ingresos: ${total_ingresos:,.0f}")
        print(f"    Ingresos por membresías: ${ingresos_membresia:,.0f} ({cantidad_membresias} ventas)")
        print(f"    Ingresos por entradas únicas: ${ingresos_entrada_unica:,.0f} ({cantidad_entradas} entradas)")
        
        print(f"\nINGRESOS POR DÍA DEL MES:")
        if ingresos_por_dia:
            dias_ordenados = sorted(ingresos_por_dia.items())
            for dia, monto in dias_ordenados:
                print(f"   Día {dia:2d}: ${monto:,.0f}")
        else:
            print("   No se encontraron ingresos para este mes.")
        
        # 5. Calcular promedios
        if ingresos_por_dia:
            promedio_diario = total_ingresos / len(ingresos_por_dia)
            print(f"\nESTADÍSTICAS:")
            print(f"   Promedio diario: ${promedio_diario:,.0f}")
            print(f"   Días con ingresos: {len(ingresos_por_dia)}")
            
            # Día con mayor ingreso
            dia_mayor = max(ingresos_por_dia.items(), key=lambda x: x[1])
            print(f"   Día con mayor ingreso: Día {dia_mayor[0]} (${dia_mayor[1]:,.0f})")
        
        print("="*50)
        
        return {
            "mes": mes,
            "año": año,
            "total_ingresos": total_ingresos,
            "ingresos_membresia": ingresos_membresia,
            "ingresos_entrada_unica": ingresos_entrada_unica,
            "cantidad_membresias": cantidad_membresias,
            "cantidad_entradas": cantidad_entradas,
            "ingresos_por_dia": ingresos_por_dia
        }

    def reporte_diario(self):
        """
        Descripción	El sistema debe permitir generar un Reporte Diario. Este reporte incluye, membresías compradas, actualizadas, renovadas en el día, junto con membresías en deuda y cerca finalización.
        Entrada : Dia del Reporte
        Salida : 
            -   Membresías Compradas del Dia
            -	Balance de Efectivo del Dia
        """
        # Solicitar fecha del reporte
        print("\n=== REPORTE DIARIO ===")
        ano = datetime.now().year
        
        while True:
            fecha_reporte= input("Ingrese la fecha del reporte (YYYY-MM-DD): ")
            try:
                fecha_obj = datetime.strptime(fecha_reporte, "%Y-%m-%d").date()
                break
            except Exception as e:
                print("Fecha inválida. Debe ser en formato 'YYYY-MM-DD'.")
                print(f"Error : {str(e)}")
                continue
        
        # Convertir fecha a string para comparaciones con archivos
        fecha_reporte_str = fecha_obj.strftime("%Y-%m-%d")
        
        print(f"\n📅 Generando reporte para: {fecha_reporte_str}")
        print("="*50)
        
        # Rutas de archivos
        registro_caja = "registros/Caja.txt" # Formato: fecha;hora;tipo;efectivo(0,000.0)
        registro_entradas = "registros/Entradas.txt" # Formato Fecha;Hora;ID;Documento;Nombre;Membresía(False:Vencida/True:Activa/None:SinMembresía);Tipo(Entrada Unica/Membresia)
        
        # Variables para el reporte
        membresias_compradas = 0
        balance_efectivo = 0.0
        
        # 1. Analizar registros de caja del día
        print("\nBALANCE DE EFECTIVO DEL DÍA:")
        with open(registro_caja, "r", encoding='utf-8') as archivo_caja:
            for linea in archivo_caja:
                datos = linea.strip().split(";")
                if len(datos) >= 4:
                    fecha_transaccion = datos[0]
                    tipo_transaccion = datos[2]
                    monto = float(datos[3].replace(",", ""))
                    
                    if fecha_transaccion == fecha_reporte_str:
                        balance_efectivo += monto
                        if tipo_transaccion in ["Membresia", "PagoMembresia"]:
                            membresias_compradas += 1
        
        print(f"   Total ingresos del día: ${balance_efectivo:,.0f}")
        print(f"   Membresías vendidas: {membresias_compradas}")  # Dividir por 2 porque hay Membresia y PagoMembresia
        
        # 2. Analizar entradas del día
        print("\nENTRADAS DEL DÍA:")
        entradas_dia = 0
        entradas_membresia = 0
        entradas_unicas = 0
        
        with open(registro_entradas, "r", encoding='utf-8') as archivo_entradas:
            for linea in archivo_entradas:
                datos = linea.strip().split(";")
                if len(datos) >= 7:
                    fecha_entrada = datos[0]
                    tipo_entrada = datos[6]
                    
                    if fecha_entrada == fecha_reporte_str:
                        entradas_dia += 1
                        if tipo_entrada == "General":
                            entradas_membresia += 1
                        elif tipo_entrada == "IngresoUnico":
                            entradas_unicas += 1
            
            print(f"   Total entradas: {entradas_dia}")
            print(f"   Entradas con membresía: {entradas_membresia}")
            print(f"   Entradas únicas: {entradas_unicas}")
        
        # Resumen final
        print("\n" + "="*50)
        print("RESUMEN DEL REPORTE DIARIO:")
        print(f"    Fecha: {fecha_reporte_str}")
        print(f"    Balance efectivo: ${balance_efectivo:,.0f}")
        print(f"    Membresías compradas: {membresias_compradas}")
        print(f"    Total entradas del día: {entradas_dia}")
        print("="*50)
        
        return {
            "fecha": fecha_reporte_str,
            "balance_efectivo": balance_efectivo,
            "membresias_compradas": membresias_compradas,
            "entradas_dia": entradas_dia
        }
    
    
    def informe_entrada(self):
        """
        Nombre	Informe de Entradas
        Descripción	El sistema debe permitir generar un informe de entradas. Este informe muestra el número de entradas de clientes en los diferentes días de la semana y cuáles son las horas más frecuentadas
        Entrada	: Mes del Informe
        Salida	: 
            - Número de Entradas al Gimnasio por Días
            - Horas más Frecuentadas en el Gimnasio
        """
        print("\n=== INFORME DE ENTRADAS ===")
        
        registro_entradas = "registros/Entradas.txt" # Formato Fecha;Hora;ID;Documento;Nombre;Membresía(False:Vencida/True:Activa/None:SinMembresía);Tipo(Entrada Unica/Membresia)
        
        # Leer archivo y extraer meses únicos
        meses_disponibles = []
        
        with open(registro_entradas, "r", encoding='utf-8') as archivo:
            for linea in archivo:
                datos = linea.strip().split(";")
                if len(datos) >= 7:
                    fecha = datos[0]  # Formato YYYY-MM-DD
                    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                    mes_año = fecha_obj.strftime("%m")  # Formato YYYY-MM
                    # Solo agregar si no está ya en la lista (evitar duplicados)
                    if mes_año not in meses_disponibles:
                        meses_disponibles+=[mes_año]
        
        if not meses_disponibles:
            print("❌ No se encontraron registros de entradas en el archivo.")
            return
        
        # Mostrar meses disponibles y permitir selección
        meses_lista = sorted(meses_disponibles, reverse=True)  # Más recientes primero
        
        print(f"\nMeses con registros disponibles:")
        print("="*40)
        print(meses_lista)
        
        # Pedimos el mes
        while True:
            mes = input(f"\nSeleccione un mes (1-{len(meses_lista)}) o Enter para cancelar: ")
            if mes == "":
                print("Operación cancelada.")
                return
            if ut.is_number(mes, "Mes"):
                mes = int(mes)
                if mes <= 12 and mes > 0:
                    break
        
        # Pedimes el Año
        while True:
            año = input("Ingrese el año (ej: 2025): ")
            if ut.is_number(año, "Año"):
                año = int(año)
                if año >= 2020 and año <= 2030:
                    break
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        print(f"\n¿Qué día de la semana fue el 1 de {mes}/{año}?")
        for i, dia in enumerate(dias_semana):
            print(f"{i+1}. {dia}")
        
        # Preguntar qué día de la semana fue el primer día del mes
        while True:
            dia_inicio = input("Seleccione el día (1-7): ")
            if ut.is_number(dia_inicio, "Día"):
                dia_inicio = int(dia_inicio)
                if dia_inicio >= 1 and dia_inicio <= 7:
                    dia_inicio = dia_inicio - 1  # Convertir a índice (0-6)
                    break
        
        # 3. Crear cadena de búsqueda para el mes
        mes_busqueda = f"{año}-{mes:02d}"  # Formato: 2025-06
        print(f"\n Generando informe para: {mes}/{año}")
        print("="*50)
        
        # Contadores simples
        total_entradas = 0
        entradas_por_dia = {}  # Lunes: 0, Martes: 0, etc.
        entradas_por_hora = {}  # 08: 0, 09: 0, etc.
        
        # Inicializar contadores
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for dia in dias_semana:
            entradas_por_dia[dia] = 0
        
        # Leer archivo y contar entradas del mes seleccionado
        with open(registro_entradas, "r", encoding='utf-8') as archivo:
            for linea in archivo:
                datos = linea.strip().split(";")
                if len(datos) >= 7:
                    fecha = datos[0]  # YYYY-MM-DD
                    hora = datos[1]   # HH:MM:SS
                    
                    # Extraer año y mes de la fecha
                    partes_fecha = fecha.split("-")
                    año_entrada = int(partes_fecha[0])
                    mes_entrada = int(partes_fecha[1])
                    dia_entrada = int(partes_fecha[2])
                    
                    # Solo procesar si es del mes y año seleccionado
                    if año_entrada == año and mes_entrada == mes:
                        total_entradas += 1
                        
                        # Calcular día de la semana usando el día de inicio
                        dia_semana_indice = (dia_entrada - 1 + dia_inicio) % 7
                        dia_semana = dias_semana[dia_semana_indice]
                        entradas_por_dia[dia_semana] += 1
                        
                        # Obtener hora (solo la parte de la hora)
                        hora_simple = hora.split(":")[0]  # Solo la hora (ej: "14" de "14:30:00")
                        if hora_simple in entradas_por_hora:
                            entradas_por_hora[hora_simple] += 1
                        else:
                            entradas_por_hora[hora_simple] = 1
        
        # Mostrar resultados
        print(f"\nTOTAL DE ENTRADAS: {total_entradas}")
        
        print(f"\nENTRADAS POR DÍA DE LA SEMANA:")
        for dia, cantidad in entradas_por_dia.items():
            print(f"   {dia}: {cantidad} entradas")
        
        print(f"\nHORAS MÁS FRECUENTADAS:")
        # Ordenar horas por cantidad de entradas
        # horas_ordenadas = sorted(entradas_por_hora.items(), key=lambda x: x[1], reverse=True)
        # for hora, cantidad in horas_ordenadas[:5]:  # Solo mostrar top 5
        for hora, cantidad in entradas_por_hora.items(): 
            print(f"   {hora}:00 - {cantidad} entradas")
        
        print("="*50)

    
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
                    "fecha_registro": cliente.get_fecha_regitro(),
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
            
        except Exception as e:
            print(f"✗ Error al guardar el archivo JSON: {str(e)}")
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
        except Exception as e:
            print(f"✗ Error al cargar el archivo: {str(e)}")
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
        except Exception as e:
            print(f"✗ Error al leer el archivo: {str(e)}")
            return False

        # Contadores para estadísticas
        lineas_error = []
        clientes_cargados = 0
        membresias_cargadas = 0
        lineas_procesadas = 0
        
        inval = [None, "None", "none", "", " ", "0", 0]
        
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
                if telefono and telefono.lower() in inval:
                    telefono = None
                
                # Crear el cliente primero
                cliente_creado = self.crear_cliente(
                    nombre=linea[0],
                    documento=linea[1],
                    telefono=telefono,
                    fecha_registro=datetime.strptime(linea[3], "%Y-%m-%d").date()
                )
                
                if cliente_creado:
                    
                    if (linea[4] in inval) or (linea[5] in inval):
                        print(f"⚠️  Línea {i+1} tiene datos de membresía inválidos o cliente sin membresia, se omitirá la membresía.")
                        continue
                    
                    if linea[6] in inval:
                        linea[6] = None  # Si la fecha fin es inválida, la dejamos como None y se calculara en la membresía
                    
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
                
            except Exception as e:
                print(f"✗ Error procesando línea {i+1}: {str(e)}")
                lineas_error.append(i+1)
                continue
        
        # Mostrar estadísticas finales
        print("="*60)
        print("📊 RESUMEN DE CARGA:")
        print(f"📥 Líneas procesadas: {lineas_procesadas}")
        print(f"✅ Clientes cargados exitosamente: {clientes_cargados}")
        print(f"✅ Membresías cargadas exitosamente: {membresias_cargadas}")
        print(f"❌ Líneas con errores: {len(lineas_error)}")
        if lineas_error:
            print(f"🔍 Líneas con errores: {lineas_error}")

        # Calcular tasa de éxito basada en clientes cargados (más realista)
        if lineas_procesadas > 0:
            tasa_exito_general = (clientes_cargados / lineas_procesadas) * 100
            print(f"📈 Tasa de éxito general: {tasa_exito_general:.1f}%")

        # Mostrar tasa de membresías solo si hay clientes cargados
        if clientes_cargados > 0:
            tasa_membresias = (membresias_cargadas / clientes_cargados) * 100
            print(f"📈 Clientes con membresía: {tasa_membresias:.1f}%")
            
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
                        archivo.write(f"{i.get_nombre()};{i.get_documento()};{i.get_telefono()};{i.get_fecha_regitro()};{membresia.get_pago()};{membresia.get_fecha_inicio()};{membresia.get_fecha_fin()}\n")
                    else:
                        archivo.write(f"{i.get_nombre()};{i.get_documento()};{i.get_telefono()};{i.get_fecha_regitro()};None;None;None\n")
        
        return nombre_archivo
        print(f"✓ Datos exportados exitosamente a: {nombre_archivo}")

    #! Metodo Incompleto, falta implementar
    def cargar_entrenadores(self, nombre_archivo=None):
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
            nombre_archivo = "entrenadores.txt"
        
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
                
                # Validar que tenga el formato esperado para entrenadores (4 columnas)
                if columns != 4:
                    print(f"⚠️  ADVERTENCIA: Este archivo tiene {columns} columnas.")
                    print("""📋 Formato esperado para entrenadores : """)
                    return False
                self.crear_entrenador()
        except FileNotFoundError:
            print(f"✗ Archivo {nombre_archivo} no encontrado.")
            return False
        except Exception as e:
            print(f"✗ Error al leer el archivo: {str(e)}")
            return False

    def exportar_entrenadores(self):
        """
        Exporta los entrenadores y sus sesiones asociadas a un archivo JSON.
        Cada entrenador incluye una lista de sesiones con sus detalles e inscritos.
        
        Returns:
            str: Ruta del archivo creado o None si hubo error
        """
        nombre_archivo = f"registros/entrenadores_{date.today().strftime('%Y%m%d')}.json"
        
        # Crear estructura de datos para exportar
        datos_exportar = {
            "gimnasio": {
                "nombre": self.__nombre,
                "fecha_exportacion": date.today().strftime("%Y-%m-%d")
            },
            "estadisticas": {
                "total_entrenadores": len(self.__entrenadores),
                "total_sesiones": len(self.__sesiones)
            },
            "entrenadores": []
        }
        
        print(f"\n📥 Exportando {len(self.__entrenadores)} entrenadores...")
        
        # Procesar cada entrenador
        for entrenador in self.__entrenadores:
            datos_entrenador = {
                "id_entrenador": entrenador.get_id_entrenador(),
                "nombre": entrenador.get_nombre(),
                "especialidad": entrenador.get_especialidad(),
                "telefono": entrenador.get_telefono(),
                "sesiones": []
            }
            
            # Buscar sesiones asociadas a este entrenador
            sesiones_entrenador = 0
            for sesion in self.__sesiones:
                # Verificar si la sesión pertenece a este entrenador
                if (sesion.get_entrenador() and sesion.get_entrenador().get_id_entrenador() == entrenador.get_id_entrenador()):
                    
                    # Obtener documentos de clientes inscritos
                    documentos_inscritos = []
                    for i in range(sesion.get_cupos()):
                        cliente_inscrito = sesion._SesionEspecial__inscritos[i]
                        if cliente_inscrito is not None:
                            documentos_inscritos.append(cliente_inscrito.get_documento())
                    
                    # Crear datos de la sesión
                    datos_sesion = {
                        "id_sesion": sesion.get_id_sesion(),
                        "fecha": sesion.get_fecha(),
                        "maximo_cupos": sesion.get_maximo_cupos(),
                        "cupos_ocupados": sesion.get_cupos(),
                        "cupos_disponibles": sesion.get_cupos_disponibles(),
                        "dias_restantes": sesion.calcular_dias_restantes(),
                        "documentos_inscritos": documentos_inscritos
                    }
                    
                    datos_entrenador["sesiones"].append(datos_sesion)
                    sesiones_entrenador += 1
            
            datos_entrenador["total_sesiones"] = sesiones_entrenador
            datos_exportar["entrenadores"].append(datos_entrenador)
            print(f"✓ Entrenador {entrenador.get_nombre()}: {sesiones_entrenador} sesiones")
        
        # Guardar archivo JSON
        try:
            with open(nombre_archivo, 'w') as archivo:
                json.dump(datos_exportar, archivo, indent=4, ensure_ascii=False)
            
            print(f"\n✓ Datos exportados exitosamente a: {nombre_archivo}")
            print(f"✓ Total de entrenadores exportados: {len(datos_exportar['entrenadores'])}")
            print(f"✓ Total de sesiones exportadas: {sum(ent['total_sesiones'] for ent in datos_exportar['entrenadores'])}")
            
            return nombre_archivo
            
        except Exception as e:
            print(f"✗ Error al guardar el archivo JSON: {str(e)}")
            return None