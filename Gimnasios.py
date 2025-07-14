import numpy as np
from datetime import date, timedelta, datetime
import json # Importante para la gestión de datos en formato JSON
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
            Imprime el nombre, telefono de contacto del gimnasio y direccion
        """        
        print(f"Gimnasio {self.__nombre}, Tel: {self.__telefono},\nCorreo: {self.__correo_electronico}, nos encontramos ubicados en {self.__direccion}")

    #? ============================== Metodos De Creacion ==============================

    # R1
    def crear_cliente(self, nombre: str=None, documento: str=None, telefono: str=None, fecha_registro: str=None):
        """_summary_
            Funcion encargada de crear el cliente y agregarlo al array de clientes.
            Si no se proporcionan datos en los argumentos, se solicita al usuario que los ingrese.
        Args:
            nombre (str, optional): Nombre del Cliente. Defaults to None.
            documento (str, optional): Documento de indentidad del Cliente. Defaults to None.
            telefono (str, optional): Numero de Telefono del Cliente. Defaults to None.
            fecha_registro (str, optional): Fecha de Registro del Cliente. Defaults to None.
        Returns:
            (bool, Cliente): False para notificar que no se creo el cliente o el Objeto Cliente creado.
        """        
        
        if self.__numero_clientes >= self.__maximo_clientes:
            print("No se pueden registrar más clientes, el gimnasio ha alcanzado su capacidad máxima.")
            return False
        
        # Si no hubo datos, se solicita al usuario
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
            if telefono and ( not ut.is_number(telefono, "Telefono")): # Si se ingreso algo en el telefono se valida
                return False
            if not (ut.is_string(nombre, "Nombre") and ut.is_number(documento, "Documento")):
                return False
        
        id_cliente = self.__historico_clientes + 1 # Se genera un ID para el cliente basado en el contador de clientes históricos
        
        if not fecha_registro:
            fecha_registro = date.today().strftime("%Y-%m-%d") # Si no se proporciona fecha, se genera un Objeto fecha actual y se convierte a string
        
        # Verificar si el cliente ya está registrado
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_documento() == documento:
                print(f"\n!!! El cliente con documento {documento} ya está registrado.")
                return False
        
        nuevo_cliente = Cliente(id_cliente, nombre.lower(), documento, fecha_registro, telefono)
        # Guardamos la referencia del cliente en el array de clientes buscando el primer espacio vacío
        for i in range(self.__maximo_clientes):
            if self.__clientes[i] is None:
                self.__clientes[i] = nuevo_cliente
                break # Salimos del ciclo una vez que encontramos un espacio vacío
        
        self.__numero_clientes += 1 # Incrementamos el contador de clientes
        self.__historico_clientes += 1 # Incrementamos el contador de clientes históricos
        print(f"ID {id_cliente}  {nombre} registrado exitosamente. {fecha_registro}")
        return nuevo_cliente # Objeto Cliente creado

    # R3
    def crear_membresia(self, cliente, fecha_inicio: str=None, fecha_fin: str=None, pago: bool=None):
        """_summary_
            Funcion encargada de crear la Mebresia del Cliente y asignarala a su respectivo Cliente.
        Args:
            cliente (Cliente): Objeto Cliente al que se le asignara la Membresia.
            fecha_inicio (str, optional): Fecha de inicio de la Membresia. Defaults to None.
            fecha_fin (str, optional): Fecha de finalizacion de la Membresia. Defaults to None.
            pago (bool, optional): _description_. Defaults to None.
        Returns:
            (bool, Membresia): Retorna el Objeto Membresia creado o False si no se pudo crear.
        """        
        
        # Validaciones
        
        if cliente.get_membresia():
            print("El cliente ya tiene membresia.")
            cliente.info_membresia()
            return False
        
        if not fecha_inicio:
            fecha_inicio = date.today() # Si no se proporciona fecha de inicio, se crea el Objeto fecha actual
        else:
            # Convertimos la fecha_inicio de str a objeto date
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        
        if not fecha_fin: # Si no se proporciona fecha de fin, se suman 30 dias al Objeto fecha de inicio
            fecha_fin = fecha_inicio + timedelta(days=30)
        else:
            # Convertimos la fecha_fin de str a objeto date
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        
        # Validar la diferencia entre fecha_inicio y fecha_fin cuando ambas son proporcionadas
        if fecha_inicio is not None and fecha_fin is not None:
            
            # Calcular la diferencia en días
            diferencia_dias = (fecha_fin - fecha_inicio).days
            # Comprobar si la diferencia es exactamente 30 días
            if diferencia_dias != 30:
                print(f"La diferencia entre la fecha de inicio y fin es de {diferencia_dias} días, no los 30 días estándar.")
                if diferencia_dias > 30:
                    print(f"Hay {diferencia_dias - 30} días adicionales.")
                else:
                    print(f"Faltan {30 - diferencia_dias} días para completar los 30 días estándar.")
                
                # Calcular la fecha de fin correcta (30 días después de la fecha de inicio)
                fecha_fin= fecha_inicio + timedelta(days=30)
                print(f"Se ha actualizado la fecha de fin a: {fecha_fin}")
        
        if pago is None:
            while True: # Ciclo para Ingreso correcto del pago
                pagar = input("¿Desea pagar inmediatamente? (si/no)\nR// ")
                if ut.valid_yes_no(pagar):
                    break
            
            pago = ut.yes_no(pagar) # Convertimos el pago a booleano
            
            if pago:
                # Se registra el pago en Caja con su motivo
                self.ingreso_caja(PRECIO_MEMBRESIA, "Membresia")

        # Crear la membresía y nos aseguramos de guardar las fechas str y no como Objetos date
        nueva_membresia = Membresia(fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d"), pago)
        cliente.set_membresia(nueva_membresia)
        print(f"Membresía creada para {cliente.get_nombre()} con ID {cliente.get_id_cliente()}")
        print(f"Vigencia: {fecha_inicio} hasta {fecha_fin}")
        print(f"Estado: {'Pagada' if pago else 'Pendiente de pago'}")
        
        return nueva_membresia # Objeto Membresia creado
    
    def crear_entrenador(self, nombre: str=None, especialidad: str=None, telefono: str=None):
        """_summary_
            Funcion encargada de crear un nuevo Entrenador y  agregarlo a la lista de entrenadores.
        Args:
            nombre (str, optional): Nombre del Entrenador. Defaults to None.
            especialidad (str, optional): Especialidad del Entrenador de la lista 'sesiones_especiales'. Defaults to None.
            telefono (str, optional): _description_. Defaults to None.

        Returns:
            (bool, Entrenador): Retorna el Objeto Entrenador creado o False si no se pudo crear.
        """
        
        if not nombre or not especialidad:
            # Si no se proporcionan datos, se solicita al usuario que los ingrese
            
            while True:
                nombre = input("Ingrese el Nombre del Entrenador : ")
                if ut.is_string(nombre, "Nombre"):
                    break
            
            while True:
                especialidad = input(f"Ingrese la indice de la especialidad del Entrenador {self.__sesiones_especiales} : ")
                if ut.is_number(especialidad, "Indice Especialidad"):
                    especialidad = int(especialidad)
                    if especialidad <= len(self.__sesiones_especiales) and especialidad >= 0:
                        break
                    else:
                        print(f"Especialidad no válida. Debe ser un indice de las siguientes: {self.__sesiones_especiales}")
            
            while True:
                telefono = input("Ingrese el numero de telefono del Entrenador (Enter para Omitir) : ")
                if telefono:
                    if ut.is_number(telefono, "Telefono"):
                        break
                else:
                    break
        else:
            # Si se proporcionan datos, se validan
            if telefono and ( not ut.is_number(telefono, "Telefono")):
                return False
            if not (ut.is_string(nombre, "Nombre") and ut.is_string(especialidad, "Especialidad")):
                return False
        
        id_entrenador = self.__historico_entrenadores + 1 # Se genera un ID para el Entrenador basado en el contador de entrenadores históricos
        # Se crea el Objeto Entrenador y se asigna la especialidad de la lista de sesiones especiales
        nuevo_entrenador = Entrenador(id_entrenador, nombre.lower(), self.__sesiones_especiales[especialidad], telefono)
        self.__entrenadores.append(nuevo_entrenador) # Agregamos el nuevo entrenador a la lista de entrenadores
        self.__historico_entrenadores += 1 # Incrementamos el contador de entrenadores históricos
        print(f"Entrenador {nombre} especializado en {self.__sesiones_especiales[especialidad]} registrado con ID: {id_entrenador}")
        return nuevo_entrenador # Objeto Entrenador creado
    
    def crear_sesion_especial(self, entrenador: Entrenador=None, fecha: str=None, maximo_cupos: int =None, id_entrenador: int=None):
        """_summary_
            Funcion encargada de crear una nueva Sesion Especial y agregarla a la lista de sesiones.
            Si no se proporcionan datos en los argumentos, se solicita al usuario que los ingrese.
        Args:
            entrenador (Entrenador, optional): Objeto Entrenador asociado a la SesionEspecial. Defaults to None.
            fecha (str, optional): Fecha del Evento SesionEspecial. Defaults to None.
            maximo_cupos (int, optional): Maximo de Clientes que se puede inscribir a la SesionEspecial. Defaults to None.
            id_entrenador (int, optional): ID del Entrenador. Defaults to None.
        Returns:
            (bool, SesionEspesial): Objeto SesionEspecial creado o False si no se pudo crear.
        """        
        
        if not fecha:
            while True:
                fecha = input("Ingrese la fecha de la sesión especial (YYYY-MM-DD): ")
                # Se usa el try para ahorrarnos hacer validaciones de fecha y evitar errores de formato
                try:
                    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                    break
                except Exception as e:
                    print("Fecha inválida. Debe ser en formato 'YYYY-MM-DD'.")
                    print(f"Error : {str(e)}")
                    continue
        
        if not entrenador:
            if not id_entrenador:
                print("Debe proporcionar un entrenador o un ID de entrenador.")
                return False
            else:
                # si no hay entrenador, buscamos por ID
                entrenador = self.buscar_entrenador(id_entrenador)
        
        # Pedimos el máximo de cupos si no se proporciona
        if not maximo_cupos:
            while True:
                maximo_cupos = input("Ingrese el número máximo de cupos (Enter para usar el valor por defecto 25): ")
                if maximo_cupos == "":
                    maximo_cupos = 25
                    break
                elif ut.is_number(maximo_cupos, "Maximo Cupos"):
                    maximo_cupos = int(maximo_cupos)
                    break
        
        id_sesion = self.__historico_sesiones + 1 # Generamos un ID para la sesión basado en el contador de sesiones históricas
        # Creamos la sesión especial y nos aseguramos de que la fecha sea un string y no un Objeto date
        nueva_sesion = SesionEspecial(id_sesion, entrenador, fecha.strftime("%Y-%m-%d"), maximo_cupos)
        self.__sesiones.append(nueva_sesion) # Agregamos la nueva sesión a la lista de sesiones
        self.__historico_sesiones += 1 # Incrementamos el contador de sesiones históricas
        print(f"Sesión especial creada con ID: {id_sesion} para la fecha {fecha}")
        print(f"Entrenador asignado: {entrenador.get_nombre()} ({entrenador.get_especialidad()})")
        return nueva_sesion # Objeto SesionEspecial creado
    
    #? ============================== Metodos De Busqueda y Visualizacion ==============================
    
    def buscar_cliente(self):
        """_summary_
            Funcion encargada de buscar un Cliente en el array de clientes.
        Returns:
            _type_: _description_
        Notes:
            - Se penso permitir colocar el modo de busqueda en el argumento para evitar el menu y ahorrar reescribir busqueda de Clientes por ID
        """
        
        # Buqueda por ID, Nombre o Documento
        # Menu de Busqueda
        print("\n======= Buscar Cliente =======")
        print(30*"=")
        print("Seleccione el tipo de búsqueda :")
        print("1. Buscar por ID")
        print("2. Buscar por Nombre") # Listar si hay mas de 1 cliente con el mismo nombre
        print("3. Buscar por Documento")
        print("Enter para salir")
        opcion_busqueda = input("Seleccione una opción : ")
        print(30*"=")
        if opcion_busqueda not in ["1", "2", "3", ""]: # Si ingresa una opcion fuera de rango termina la ejecución
            print("Saliendo del menú de búsqueda...")
            return None
        
        cliente_encontrado = None # Variable para almacenar el cliente encontrado o None si no se encuentra
        
        
        # Swich case para manejar las opciones de búsqueda
        match opcion_busqueda:
            case "1":
                # Busqueda por ID
                while True: #Ciclo para el correcto ingreso del ID
                    id_cliente = input("Ingrese el ID del cliente: ")
                    if ut.is_number(id_cliente, "ID"):
                        break # Salir del ciclo si el ID es válido
                for cliente in self.__clientes: # Recorrer el array de clientes
                    if cliente is not None and cliente.get_id_cliente() == int(id_cliente): # Buscar coincidencia
                        cliente_encontrado = cliente # Guardar el cliente encontrado
                        # Imprimir los detalles del cliente encontrado
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro()}")
                if not cliente_encontrado: # Si no se encontró el cliente, informar al usuario
                    print(f"No se encontró un cliente con ID {id_cliente}.")
                    return None
            case "2":
                # Busqueda por Nombre - Este metodo toma la primer coincidencia del nombre
                while True:
                    nombre_cliente = input("Ingrese el nombre del cliente: ")
                    if ut.is_string(nombre_cliente, "Nombre"):
                        break
                for cliente in self.__clientes:
                    if cliente is not None and cliente.get_nombre() == nombre_cliente.lower():
                        cliente_encontrado = cliente
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro()}")
                if not cliente_encontrado:
                    print(f"No se encontró un cliente con nombre {nombre_cliente}.")
                    return None
            case "3":
                # Busqueda por Documento
                while True:
                    documento = input("Ingrese el documento del cliente: ")
                    if ut.is_number(documento, "Documento"):
                        break
                for cliente in self.__clientes:
                    if cliente is not None and cliente.get_documento() == documento:
                        cliente_encontrado = cliente
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro()}")
                if not cliente_encontrado:
                    print(f"No se encontró un cliente con documento {documento}.")
                    return None
            case "":
                print("Saliendo del menú de búsqueda...")
                
        if cliente_encontrado is None:
            # Si  no se Encontro Cliente Finaliza ejecusion
            print("No se encontró ningún cliente.")
            return None
        else:
            return cliente_encontrado # Objeto Cliente encontrado


    def consultar_membresia(self, cliente):
        """ Muestra la informacion de la membresía de un cliente y Retorna el Objeto Memebreisa"""
        
        if cliente.get_membresia() is None:
            print(f"El cliente {cliente.get_nombre()} no tiene una membresía activa.")
            return
        else:
            membresia = cliente.get_membresia()
        
        # Mostrar información de la membresía
        print(f"\n=== Información de Membresía ===")
        print(f"Cliente: {cliente.get_nombre()}")
        print(f"Estado de pago: {'Pagada' if membresia.get_pago() else 'Pendiente'}") 
        print(f"Fecha de inicio: {membresia.get_fecha_inicio()}")
        print(f"Fecha de fin: {membresia.get_fecha_fin()}")
        # print(f"Días restantes: {}")
        print("="*30)
        
        return membresia # Objeto Membresia encontrado
    
    def buscar_entrenador(self, id_entrenador: int=None):
        """_sumary_
            Busca un entrenador por su ID.
        Args:
            id_entrenador (int): ID del Entrenador a buscar
        Returns:
            Entrenador: Objeto Entrenador si se encuentra, None si no se encuentra
        """
        
        if id_entrenador is None: # Si no se proporciona un ID, se solicita al usuario que lo ingrese
            while True:
                id_entrenador = input("Ingrese el ID del entrenador: ")
                if ut.is_number(id_entrenador, "ID"):
                    id_entrenador = int(id_entrenador)
                    break
        
        # Se recorre la lista de entrenadores para buscar el ID
        for entrenador in self.__entrenadores:
            if entrenador.get_id_entrenador() == id_entrenador:
                print(f"Entrenador : ID: {entrenador.get_id_entrenador()}, Nombre: {entrenador.get_nombre()}, Especialidad: {entrenador.get_especialidad()}")
                # Si se encuentra el Entrenador, se retorna para finalizar la ejecucion
                return entrenador # Objeto Entrenador encontrado
        # Si no se encuentra el entrenador, se informa al usuario
        print(f"No se encontró un entrenador con ID {id_entrenador}.")
        return None
    
    def visualizar_clientes(self):
        """Muestra todos los clientes registrados en el gimnasio."""
        print("\n=== Clientes Registrados ===")
        total_clientes = 0
        for cliente in self.__clientes:
            if cliente is not None:
                total_clientes += 1
                print(f"ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Registro: {cliente.get_fecha_registro()} {cliente.tiene_membresia()}")
        
        print(f"\nNumero de Clientes Registradas : {total_clientes}")
        
        # Permite seleccionar un cliente por ID para retornarlo
        id_cliente = input("\nSelecione un Cliente o Enter para continuar... ")
        if id_cliente == "":
            print("Saliendo del menú de clientes...")
            return None
        else:
            # Validar que el ID ingresado sea un número
            if not ut.is_number(id_cliente, "ID de Cliente"):
                print("ID de cliente inválido. Debe ser un número.")
                return None
            id_cliente = int(id_cliente)
            if id_cliente < 1:
                print(f"ID de cliente inválido.")
                return None
            
            # Buscar el cliente por ID
            for cliente in self.__clientes:
                if cliente is not None and cliente.get_id_cliente() == id_cliente:
                    # Si se encuentra el cliente, se imprime su información
                    print(f"\n===== Cliente Seleccionado ====")
                    print(f"Cliente ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Fecha de Registro: {cliente.get_fecha_registro()}")
                    print(f"Telefono: {cliente.get_telefono() if cliente.get_telefono() else 'No registrado'}")
                    print(f"Membresía: {cliente.tiene_membresia()}")
                    return cliente # Y se retorna el Objeto Cliente encontrado para finalizar la ejecucion
            print(f"No se encontró un cliente con ID {id_cliente}.")
            return None
    
    def visualizar_membresias(self):
        """Muestra todas las membresias registradas en el gimnasio."""
        print("\n=== Membresías Registradas ===")
        total_membresias = 0
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_membresia() is not None:
                membresia = cliente.get_membresia()
                total_membresias += 1
                dias_restantes = membresia.calcular_dias_restantes()
                print(f""" - ID: {cliente.get_id_cliente()}, Cliente {cliente.get_nombre()}, Documento: {cliente.get_documento()}, Registrado: {cliente.get_fecha_registro()}
                        Membresia => Estado: { 'Paga' if membresia.get_pago() else 'Pendiente' }, Fecha Inicio: {membresia.get_fecha_inicio()}, Fecha Fin: {membresia.get_fecha_fin()}, Dias Restantes: {dias_restantes if dias_restantes > 0 else "Vencida"} \n""")
        
        print(f"\nNumero de Membresias Registradas : {total_membresias}")
    
    
    def mostrar_entrenadores(self):
        """Muestra todos los entrenadores registrados en el gimnasio."""
        if not self.__entrenadores or len(self.__entrenadores) == 0:
            print("No hay entrenadores registrados.")
            return None
        
        print("\n=== Entrenadores Registrados ===")
        total_entrenadores = 0
        for entrenador in self.__entrenadores:
            entrenador.mostrar_info()
            total_entrenadores += 1
            
        print(f"\nNumero de Entrenadores Registrados : {total_entrenadores}")
        
        # Permite seleccionar un entrenador por ID para retornarlo
        id_entrenador = input("\nSeleccione un Entrenador o Enter para continuar... ")
        
        if id_entrenador == "":
            print("Saliendo del menú de entrenadores...")
            return
        else:
            # Validar que el ID ingresado sea un número
            if not ut.is_number(id_entrenador, "ID de Entrenador"):
                print("ID de entrenador inválido. Debe ser un número.")
                return None
            id_entrenador = int(id_entrenador)
            if id_entrenador < 1:
                print(f"ID de entrenador inválido.")
                return None
            
            # Buscar el entrenador por ID
            entrenador = self.buscar_entrenador(id_entrenador)
            if not entrenador:
                print(f"No se encontró un entrenador con ID {id_entrenador}.")
            else:
                return entrenador # Retorna el Objeto Entrenador encontrado
    
    
    def mostrar_sesiones(self):
        """Muestra todas las sesiones especiales disponibles"""
        total_sesiones = 0
        if not self.__sesiones or len(self.__sesiones) == 0:
            print("No hay sesiones especiales programadas.")
            return None
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
        
        # Permite seleccionar una sesión por ID para retornarla
        id_sesion = input("\nSeleccione una Sesion o Enter para continuar... ")
        
        if id_sesion == "":
            print("Saliendo del menú de sesiones...")
            return None
        else:
            # Validar que la sesión ingresada sea un número
            if not ut.is_number(id_sesion, "ID de Sesión"):
                print("ID de sesión inválido. Debe ser un número.")
                return
            id_sesion = int(id_sesion)
            if id_sesion < 1:
                print(f"ID de sesión inválido. Debe estar entre 1 y {total_sesiones}.")
                return
            
            # Buscar la sesión por ID
            for sesion in self.__sesiones:
                if sesion.get_id_sesion() == id_sesion:
                    print(f"\n===== Sesion Seleccionada ====")
                    print(f"Sesión ID: {sesion.get_id_sesion()}, Fecha: {sesion.get_fecha()}, Cupos disponibles: {sesion.get_cupos_disponibles()}")
                    entrenador = sesion.mostrar_info()
                    entrenador.mostrar_info()
                    return sesion
            print(f"No se encontró una sesión con ID {id_sesion}.")
            return None
    
    def sesiones_agendadas(self, cliente):
        """_sumary_
            Muestra las sesiones especiales a las que un cliente está inscrito.
        Args:
            cliente: Objeto Cliente para el cual se desean ver las sesiones agendadas.
        """
        print(f"\n=== Sesiones Agendadas para {cliente.get_nombre()} ===")
        for sesion in self.__sesiones:
            for cliente in sesion.get_clientes_inscritos():
                if cliente.get_id_cliente() == cliente.get_id_cliente():
                    sesion.mostrar_info()
    
    #? ============================== Metodos de Modificacion ==============================

    def ingreso_caja(self, efectivo: float, motivo: str=None): #pendieten pedir el tipo para el registro en persitencia
        """_summary_
            Modifica el efectivo del gimnasio y registra el ingreso en un archivo de texto.
        Args:
            efectivo (float): Efectivo a ingresar en la caja del gimnasio.
            motivo (str, optional): Motivo del ingreso. Defaults to None.
        Notes:
            - Se penso en guardar informacion del cliente que paga pero no c implemento
        """        

        # Registrar el ingreso en formato: fecha;hora;tipo;efectivo
        fecha = datetime.now().strftime('%Y-%m-%d') # Objeto fecha y hora actual a str
        hora = datetime.now().strftime('%H:%M:%S')  # Objeto fecha y hora actual a str
        tipo = motivo if motivo else "Ingreso" # Si no se proporciona motivo, se usa "Ingreso" como predeterminado
        registro = f"{fecha};{hora};{tipo};{float(efectivo):,}\n"
        
        print(f"Efectivo actual: ${self.__efectivo:,} + ${float(efectivo):,}")
        self.__efectivo += float(efectivo)
        print(f"Efectivo actualizado a: ${self.__efectivo:,}")
        
        # Guardar el registro en un archivo de texto
        with open("registros/Caja.txt", "a") as caja_file:
            caja_file.write(registro)
    
    def pagar_membresia(self, membresia: Membresia):
        """_summary_
            Metodo encargado de pagar la Membresia del Cliente si esta en deuda.
        Args:
            membresia (Membresia): Objeto Membresia del Cliente a pagar.
        """        
        if membresia.get_pago():
            print("La membresía ya ha sido pagada.")
            return
        else:
            print(f"El cliente tiene una membresía que aún no ha sido pagada.")
            self.ingreso_caja(PRECIO_MEMBRESIA,"PagoMembresia") # Se registra el ingreso en caja con su motivo
            membresia.set_pago(True) # Actualizamos el estado de pago de la membresía
            print(f"Pago realizado exitosamente. Monto: ${PRECIO_MEMBRESIA:,}")
    
    def renovar_membresia(self, cliente=None ,membresia: Membresia = None):
        """_summary_
            Metodo encargado de renovar la Membresia del Cliente.
        Args:
            cliente (Cliente, optional): Objeto Cliente que desea renovar su Membresia. Defaults to None.
            membresia (Membresia, optional): Membresia a renovar asiciada al Cliente. Defaults to None.
        """        
        
        if membresia is None:
            if cliente is None:
                print("Debe proporcionar un cliente para renovar la membresía.")
                return
            else:
                membresia = cliente.get_membresia()
                if membresia is None:
                    print("El cliente no tiene una membresía activa para renovar.")
                    return
        
        if not membresia.get_pago():
            print("La membresía no ha sido pagada.")
            return
        if membresia.calcular_dias_restantes() > 0:
            print("La membresía aún está activa y no necesita renovación.")
            return
        
        # Actualizar la membresía
        print(f"Membresía renovada.")
        self.ingreso_caja(PRECIO_MEMBRESIA, "RenovacionMembresia") # Se registra el ingreso en caja con su motivo
        membresia_.renovar_membresia() # Actualiza la fecha de fin de la membresía
    
    def pago_ingreso_unico(self, cliente):
        """"Metodo encargado de registrar el ingreso unico de un cliente sin tener que adquirir memebreisa, pagando el ingreso unico del Cliente."""
        self.ingreso_caja(PRECIO_ENTRADA_UNICA, "PagoIngresoUnico") # Se registra el ingreso en caja con su motivo
        cliente.registrar_entrada("IngresoUnico") # Registra la entrada del cliente en el historial de entradas
    
    def agendar_sesion(self, cliente, id_sesion: int=None):
        """_summary_
            Permite a un cliente inscribirse en una sesión especial.
        Args:
            cliente: Objeto Cliente que se quiere inscribir
            id_sesion (int, optional): ID de la sesión especial a la que se quiere inscribir. Si es None, se muestran todas las sesiones disponibles.
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
            # Si no se proporciona un ID de sesión, mostrar todas las sesiones disponibles
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
            # Lista de los IDs de las sesiones disponibles
            
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
    
    def eliminar_cliente(self, id_cliente: int=None,cliente=None):
        """_summary_
            Funcion encargada de eliminar un Cliente del array de clientes y todas sus referencias.
            Si no se proporciona un ID o un objeto Cliente, se solicita al usuario que ingrese el ID del cliente a eliminar.
        Args:
            id_cliente (int, optional): ID del Cliente a eliminar. Defaults to None.
            cliente (Cliente, optional): Objeto Cliente a eliminar. Defaults to None.

        Returns:
            bool: Booleano que indica si la eliminación fue exitosa o no.
        """        
        
        if self.__numero_clientes == 0:
            print("No hay clientes registrados para eliminar.")
            return False
        
        # Validaciones
        
        if id_cliente is None:
            if cliente is None:
                # Si no se proporciona un ID ni un objeto Cliente, se solicita al usuario que ingrese el ID
                print("Debe proporcionar un ID de cliente o un objeto Cliente para eliminar.")
                while True:
                    id_cliente = input("Ingrese el ID del Cliente: ")
                    if ut.is_number(id_cliente, "ID"):
                        id_cliente = int(id_cliente)
                        break
            else:
                # Si se proporciona un objeto Cliente, obtenemos su ID
                id_cliente = cliente.get_id_cliente()
        
        # Buscar el cliente por ID
        cliente_encontrado = None
        indice_cliente = -1
        
        for i in range(len(self.__clientes)):
            cliente = self.__clientes[i]
            if cliente is not None and cliente.get_id_cliente() == id_cliente:
                cliente_encontrado = cliente
                indice_cliente = i
                break
        
        if cliente_encontrado:
            # Mostrar Cliente
            print(f"Cliente con ID {id_cliente} y nombre {cliente_encontrado.get_nombre()}.")
            
            # Confirmación de eliminación
            while True:
                confirmar = input("¿Está seguro de eliminar este Cliente? (si/no): ").strip().lower()
                if ut.valid_yes_no(confirmar):
                    break
            
            if ut.yes_no(confirmar):
                self.__clientes[i].set_membresia(None)  # Eliminar membresía si existe, luego implementar eliminar_membresia
                
                # Buscar si el cliente tiene sesiones especiales
                for sesion in self.__sesiones:
                    print(f"Verificando sesion {sesion.get_id_sesion()} ...")
                    sesion.editar_inscritos(cliente.get_id_cliente())
                
                # Eliminar cliente del array
                self.__clientes[i] = None 
                self.__numero_clientes -= 1 
                print(f"Cliente con ID {id_cliente} eliminado exitosamente.")
                return True
            else:
                # Si el usuario cancela la eliminación, informamos y finalizamos la ejecución
                print("Eliminación cancelada.")
                return False
        else:
            # Si no se encuentra el cliente, informamos y finalizamos la ejecución
            print(f"No se encontró un cliente con ID {id_cliente}.")
            return False

    def eliminar_membresia(self, cliente=None):
        """_summary_
            Metodo encargado de eliminar la Membresia de un Cliente.
        Args:
            cliente (Cliente, optional): Objeto Cliente del cual se desea eliminar su Membresia. Defaults to None.
        Returns:
            bool: Booleano que indica si la eliminación fue exitosa o no.
        """        
        if cliente is None:
            return False
        
        if cliente.get_membresia() is None:
            print(f"El cliente {cliente.get_nombre()} no tiene una membresía activa.")
            return False
        
        print("\n=== Eliminar Membresía ===")
        print(f"Cliente: {cliente.get_nombre()}")
        print(f"ID Cliente: {cliente.get_id_cliente()}")
        print(f"Membresía: {cliente.tiene_membresia()}")
        while True:
            # Confirmación de eliminación
            confirmar = input("¿Está seguro de eliminar la membresía? (si/no): ").strip().lower()
            if ut.valid_yes_no(confirmar):
                break
        if ut.yes_no(confirmar):
            cliente.set_membresia(None) # Eliminar la membresía del cliente
            print(f"Membresía del cliente {cliente.get_nombre()} eliminada exitosamente.")
            return True
        else:
            print("Eliminación de membresía cancelada.")
            return False
    
    def eliminar_entrenador(self, id_entrenador: int=None):
        """_summary_
            Metodo encargado de eliminar un Entrenador del array de entrenadores y todas sus referencias.
        Args:
            id_entrenador (int, optional): ID del Entrenador que se desea Eliminar. Defaults to None.
        Returns:
            bool: Booleano que indica si la eliminación fue exitosa o no.
        """
        
        if not self.__entrenadores:
            print("No hay entrenadores registrados para eliminar.")
            return False
        
        if id_entrenador is None:
            # Si no se proporciona un ID, se solicita al usuario que lo ingrese
            while True:
                id_entrenador = input("Ingrese el ID del entrenador: ")
                if ut.is_number(id_entrenador, "ID"):
                    id_entrenador = int(id_entrenador)
                    break
        
        for i in range(len(self.__entrenadores)):
            # Buscamos el Entrenador por su ID y mostramos su información
            if self.__entrenadores[i].get_id_entrenador() == id_entrenador:
                print(f"Entrenador con ID {id_entrenador} y nombre {self.__entrenadores[i].get_nombre()}.")
                print(f"Tambien se eliminarán las sesiones especiales asociadas a este entrenador.")
                print(f"===== Sesiones asociadas =====")
                total_sesiones = 0
                # Mostramos las sesiones asociadas al entrenador
                for sesion in self.__sesiones:
                    if sesion.get_entrenador() and sesion.get_entrenador().get_id_entrenador() == id_entrenador:
                        total_sesiones += 1
                        dias_restantes = sesion.calcular_dias_restantes()
                        estado = f"{dias_restantes} días restantes" if dias_restantes is not None else "Ya pasó"
                        print(f" - Sesión ID: {sesion.get_id_sesion()}, Fecha: {sesion.get_fecha()}, {estado}")
                print(f"Total de sesiones asociadas: {total_sesiones}")
                
                # Y pedimos una confirmación de eliminación
                while True:
                    confirmacion = input("¿Estas seguro de eliminar el entrenador? (si/no): ")
                    if ut.valid_yes_no(confirmacion):
                        break
                if ut.yes_no(confirmacion):
                    print(f"Eliminando entrenador {self.__entrenadores[i].get_nombre()}...")
                    self.__entrenadores.pop(i) # Eliminamos el entrenador de la lsi
                    
                    # Buscar sesiones en las que esta
                    for sesion in self.__sesiones:
                        if sesion.get_entrenador() and sesion.get_entrenador().get_id_entrenador() == id_entrenador:
                            print(f"Eliminando sesión especial con ID {sesion.get_id_sesion()} que tenía al entrenador eliminado.")
                            if not self.eliminar_sesion(sesion): # Si la sesion no se elimino, hay que eliminar la referencia del entrenador
                                sesion.set_entrenador(None)
                    
                    return True # Si se elimino el entrenador y las sesiones asociadas
                else:
                    print("Eliminación cancelada.")
                    return False
                break
        
    def eliminar_sesion(self, sesion: SesionEspecial=None, id_sesion: int=None):
        """_summary_
            Metodo encargado de eliminar una Sesion Especial del array de sesiones y todas sus referencias.
        Args:
            sesion (SesionEspecial, optional): Objeto SesionEspecial que se desea eliminar. Defaults to None.
        Returns:
            bool: Booleano que indica si la eliminación fue exitosa o no.
        """        
        if not self.__sesiones or len(self.__sesiones) == 0:
            print("No hay sesiones especiales programadas para eliminar.")
            return False
        
        if sesion is None:
            if id_sesion is None:
                while True:
                    id_sesion = input("Ingrese el ID de la sesión a eliminar: ")
                    if ut.is_number(id_sesion, "ID"):
                        id_sesion = int(id_sesion)
                        break
            else:
                id_sesion = int(id_sesion)
        else:
            if id_sesion is None:
                id_sesion = sesion.get_id_sesion()
            else:
                id_sesion = int(id_sesion)
        
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
                        meses_disponibles.append(mes_año)
        
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
                        if tipo in ["Membresia", "PagoMembresia", "RenovacionMembresia"]:
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
            mes = input(f"\nSeleccione un mes {meses_lista} o Enter para cancelar: ")
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
        
        print(f"\nFRECUENCIA HORAS:")
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
                    "fecha_registro": cliente.get_fecha_registro(),
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
                print(f"Procesando línea {i+1}/{rows}: {linea}")
                
                # Validación para teléfono: si es "0", "None", "none" o vacío, se convierte a None
                telefono = linea[2]
                if telefono and telefono.lower() in inval:
                    telefono = None
                
                # Validar fecha de registro (obligatoria para crear cliente)
                try:
                    fecha_registro = datetime.strptime(linea[3], "%Y-%m-%d").date()
                except Exception as e:
                    print(f"✗ Error en la fecha de registro en línea {i+1}: {str(e)}")
                    lineas_error.append(i+1)
                    continue
                
                # Crear el cliente primero
                cliente_creado = self.crear_cliente(
                    nombre=linea[0],
                    documento=linea[1],
                    telefono=telefono,
                    fecha_registro=linea[3]
                )
                
                if cliente_creado:
                    clientes_cargados += 1
                    
                    # Verificar si el cliente tiene datos de membresía válidos
                    if (linea[4] in inval) or (linea[5] in inval):
                        print(f"⚠️  Línea {i+1}: Cliente sin membresía o datos de membresía inválidos.")
                        continue
                    
                    # Validar fecha de inicio de membresía (obligatoria)
                    try:
                        fecha_inicio = datetime.strptime(linea[5], "%Y-%m-%d").date()
                    except Exception as e:
                        print(f"✗ Error en la fecha de inicio de membresía en línea {i+1}: {str(e)}")
                        print("⚠️  Se omitirá la membresía para este cliente.")
                        lineas_error.append(i+1)
                        continue
                    
                    # Validar fecha de fin de membresía (opcional - se puede calcular automáticamente)
                    fecha_fin_valida = linea[6]
                    if linea[6] in inval:
                        print(f"⚠️  Línea {i+1}: Fecha fin inválida, se calculará automáticamente (+30 días).")
                        fecha_fin_valida = None
                    else:
                        try:
                            datetime.strptime(linea[6], "%Y-%m-%d").date()
                        except Exception as e:
                            print(f"⚠️  Error en la fecha fin en línea {i+1}: {str(e)}")
                            print("⚠️  Se calculará automáticamente (+30 días).")
                            fecha_fin_valida = None
                    
                    # Procesar el pago
                    pago_bool = linea[4].strip().lower() == 'true'
                    
                    # Intentar crear la membresía
                    membresia_creada = self.crear_membresia(
                        cliente=cliente_creado,
                        fecha_inicio=linea[5],
                        fecha_fin=fecha_fin_valida,
                        pago=pago_bool
                    )
                    
                    if membresia_creada:
                        membresias_cargadas += 1
                        print(f"✓ Cliente y membresía cargados exitosamente.")
                    else:
                        print(f"⚠️  Cliente creado pero falló la creación de la membresía.")
                        
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
                        archivo.write(f"{i.get_nombre()};{i.get_documento()};{i.get_telefono()};{i.get_fecha_registro()};{membresia.get_pago()};{membresia.get_fecha_inicio()};{membresia.get_fecha_fin()}\n")
                    else:
                        archivo.write(f"{i.get_nombre()};{i.get_documento()};{i.get_telefono()};{i.get_fecha_registro()};None;None;None\n")
        
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