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
            if cliente is not None and cliente.get_documento_c() == documento:
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
        print(f"Membresía creada para {cliente_encontrado.get_nombre_c()} con ID {cliente_encontrado.get_id_cliente()}")
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
        nuevo_entrenador = Entrenador(id_entrenador, nombre, especialidad, telefono)
        self.__entrenadores+=[nuevo_entrenador]
        self.__historico_entrenadores += 1
        print(f"Entrenador {nombre} especializado en {especialidad} registrado con ID: {id_entrenador}")
        return nuevo_entrenador
    
    def crear_sesion_especial(self, id_entrenador: int, fecha: str=None, maximo_cupos: int = 25):
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
        
        if not entrenador_encontrado:
            print(f"No se encontró un entrenador con ID {id_entrenador}")
            return None
        
        id_sesion = self.__historico_sesiones + 1
        nueva_sesion = SesionEspecial(id_sesion, id_entrenador, fecha, maximo_cupos)
        self.__sesiones+=[nueva_sesion]
        self.__historico_sesiones += 1
        print(f"Sesión especial creada con ID: {id_sesion} para la fecha {fecha}")
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
                
        if cliente_encontrado is None:
            print("No se encontró ningún cliente.")
            return
        else:
            return cliente_encontrado


    def consultar_membresia(self, cliente_encontrado: Cliente):
        if cliente_encontrado.get_membresia() is None:
            print(f"El cliente {cliente_encontrado.get_nombre_c()} no tiene una membresía activa.")
            return
        else:
            membresia_encontrada = cliente_encontrado.get_membresia()
        
        # Mostrar información de la membresía
        print(f"\n=== Información de Membresía ===")
        print(f"Cliente: {cliente_encontrado.get_nombre_c()}")
        print(f"Estado de pago: {'Pagada' if membresia_encontrada.get_pago_m() else 'Pendiente'}") 
        print(f"Fecha de inicio: {membresia_encontrada.get_fecha_inicio_m()}")
        print(f"Fecha de fin: {membresia_encontrada.get_fecha_fin_m()}")
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
                print(f"Entrenador : ID: {entrenador.get_id_entrenador()}, Nombre: {entrenador.get_nombre_e()}, Especialidad: {entrenador.get_especialidad_e()}")
                return entrenador
        print(f"No se encontró un entrenador con ID {id_entrenador}.")
        return None
    
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
        for cliente in self.__clientes:
            if cliente is not None and cliente.get_membresia() is not None:
                membresia = cliente.get_membresia()
                total_membresias += 1
                print(f""" - ID: {cliente.get_id_cliente()}, Cliente {cliente.get_nombre_c()}, Documento: {cliente.get_documento_c()}, Registrado: {cliente.get_fecha_registro_c()}
                        Membresia => Estado: { 'Paga' if membresia.get_pago_m() else 'Pendiente' }, Fecha Inicio: {membresia.get_fecha_inicio_m()}, Fecha Fin: {membresia.get_fecha_fin_m()}, Dias Restantes: {membresia.calcular_dias_restantes()} \n""")
        
        print(f"\nNumero de Membresias Registradas : {total_membresias}")
    
    def mostrar_sesiones(self):
        """Muestra todas las sesiones especiales disponibles"""
        if not self.__sesiones or len(self.__sesiones) == 0:
            print("No hay sesiones especiales programadas.")
            return
        else:
            print("\n=== Todas las Sesiones Especiales ===")
            for sesion in self.__sesiones:
                entrenador = sesion.mostrar_info()
                self.buscar_entrenador(entrenador)
    
    def mostrar_entrenadores(self):
        if not self.__entrenadores or len(self.__entrenadores) == 0:
            print("No hay entrenadores registrados.")
            return
        else:    
            print("\n=== Entrenadores Registrados ===")
            total_entrenadores = 0
            for entrenador in self.__entrenadores:
                entrenador.mostrar_info_e()
                total_entrenadores += 1
                
            print(f"\nNumero de Entrenadores Registrados : {total_entrenadores}")
    
    
    
    
    
    #? ============================== Metodos de Modificacion ==============================

    def ingreso_caja(self, efectivo: float): #pendieten pedir el tipo para el registro en persitencia
        """_summary_
            Modifica el efectivo del gimnasio.
        """
        print(f"Efectivo actual: ${self.__efectivo:,} + ${float(efectivo):,}")
        self.__efectivo += float(efectivo)
        print(f"Efectivo actualizado a: ${self.__efectivo:,}")
        
        # registro = f"{tipo} - Ingreso: ${float(efectivo):,}, Fecha: {date.today().strftime('%Y-%m-%d')}\n"
        
        

    
    def pagar_membresia(self, membresia_encontrada: Membresia):
        if membresia_encontrada.get_pago_m():
            print("La membresía ya ha sido pagada.")
            return
        else:
            print(f"El cliente tiene una membresía que aún no ha sido pagada.")
            self.ingreso_caja(PRECIO_MEMBRESIA)
            membresia_encontrada.set_pago_m(True)
            print(f"Pago realizado exitosamente. Monto: ${PRECIO_MEMBRESIA:,}")
    
    def pago_ingreso_unico(self, cliente_encontrado: Cliente):
        pass
    

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
                    print(f"   Entrenador: {entrenador.get_nombre_e() if entrenador else 'No encontrado'}")
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
                print(f"Entrenador con ID {id_entrenador} y nombre {self.__entrenadores[i].get_nombre_e()}.")
                confirmar = input("¿Está seguro de eliminar este entrenador? (si/no): ").strip().lower()
                if confirmar == 'si':
                    self.__entrenadores.pop(i)
                else:
                    print("Eliminación cancelada.")
                break



    #! ============================== Metodos Opcionales ==============================

    def registrar_entrada(self, cliente_encontrado: Cliente):
        pass

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
                    "nombre": cliente.get_nombre_c(),
                    "documento": cliente.get_documento_c(),
                    "telefono": cliente.get_telefono_c(),
                    "fecha_registro": cliente.get_fecha_registro_c(),
                    "membresia": None
                }
                
                # Agregar datos de membresía si existe
                membresia = cliente.get_membresia()
                if membresia is not None:
                    datos_cliente["membresia"] = {
                        "pago": membresia.get_pago_m(),
                        "fecha_inicio": membresia.get_fecha_inicio_m(),
                        "fecha_fin": membresia.get_fecha_fin_m(),
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
    
    def cargar_clientes(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                rows = len(lineas)
                columns = len(lineas[0].strip().split(";"))
                print(f"Número de líneas : {rows}")
                print(f"Número de columnas : {columns}")
        except FileNotFoundError:
            print(f"✗ Archivo {nombre_archivo} no encontrado.")
            return False
        except Exception as e:
            print(f"✗ Error al leer el archivo: {str(e)}")
            return False

        lineas_error=[]
        for i in range(1, rows):
            linea = lineas[i].strip().split(";")
            if len(linea) < 7:
                print(f"✗ Línea {i+1} malformada: {lineas[i]}")
                continue

            try:
                print("="*30)
                print(f"Procesando línea {i+1}: {linea}")
                # Crear el cliente primero
                cliente_creado = self.crear_cliente(
                    nombre=linea[0],
                    documento=linea[1],
                    telefono=linea[2],
                    fecha_registro=datetime.strptime(linea[3], "%Y-%m-%d").date()
                )
                
                if cliente_creado:
                    pago_bool = linea[4].strip().lower() == 'true'
                    self.crear_membresia(
                        cliente_encontrado=cliente_creado,
                        fecha_inicio=datetime.strptime(linea[5], "%Y-%m-%d").date(),
                        fecha_fin=datetime.strptime(linea[6], "%Y-%m-%d").date(),
                        pago=pago_bool
                    )
                else:
                    lineas_error+=[i+1]
                    print(f"✗ No se pudo crear el cliente {linea[0]} con documento {linea[1]}.")
                    continue
                
            except Exception as error:
                print(f"✗ Error procesando línea {i+1}: {str(error)}")
                continue
            
        print(f"Lineas con errores : {lineas_error}")
        return True



