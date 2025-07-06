import numpy as np
from datetime import date, timedelta

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
    
    def set_efectivo(self, efectivo: float):
        """_summary_
            Modifica el efectivo del gimnasio.
        """
        if efectivo >= 0:
            print(f"Efectivo actual: {self.__efectivo}")
            self.__efectivo = efectivo
            print(f"Efectivo actualizado a: {self.__efectivo}")
        else:
            print("El efectivo no puede ser negativo.")

    def ver_inf(self):
        """_summary_
            Imprime el nombre y telefono de contacto del gimnasio
        """        
        print(f"Gimnasio {self.__nombre}, Tel: {self.__telefono},\nCorreo: {self.__correo_electronico}, nos encontramos ubicados en {self.__direccion}")

    def registrar_cliente(self, nombre, documento, telefono=None):
        
        #Validaciones
        
        if self.__numero_clientes >= 50:
            print("No se pueden registrar más clientes, el gimnasio ha alcanzado su capacidad máxima.")
            return False
        if not nombre or not documento:
            print("Nombre y documento son obligatorios.")
            return False
        if telefono and (telefono.isalpha() or not telefono.isdigit()):
            print("El teléfono debe ser un número válido.")
            return False
        if nombre.isdigit() or not nombre.isalpha():
            print("El nombre no debe contener números ni símbolos ni espacios.")
            return False
        if documento.isalpha() or not documento.isdigit():
            print("El documento no debe contener letras ni símbolos ni espacios.")
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
    
    def buscar_cliente(self):
        print("======Menu=======")
        print("Seleccione el tipo de búsqueda :")
        print("1. Buscar por ID")
        print("2. Buscar por Nombre")
        print("3. Buscar por Documento")
        print("Enter para salir")
        opcion = input("Seleccione una opción : ")
        cliente_encontrado = None
        match opcion:
            case "1":
                while True:
                    id_cliente = input("Ingrese el ID del cliente: ")
                    if id_cliente.isalpha() or not id_cliente.isdigit():
                        print("El ID no debe contener letras ni símbolos ni espacios.")
                    else:
                        break
                for cliente in self.__clientes:
                    if cliente is not None and cliente.get_id_cliente() == int(id_cliente):
                        cliente_encontrado = cliente
                        print(f"Cliente encontrado: ID: {cliente.get_id_cliente()}, Nombre: {cliente.get_nombre_c()}, Documento: {cliente.get_documento_c()}, Fecha de Registro: {cliente.get_fecha_registro_c()}")
                if not cliente_encontrado:
                    print(f"No se encontró un cliente con ID {id_cliente}.")
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
            case "":
                print("Saliendo del menú de búsqueda.")
        



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
    
    #? 
    
    def crear_membresia(self, nombre: str, documento: str):
        
        # Validaciones
        
        if self.__numero_membresias >= 50:
            print("No se pueden registrar más membresias, el gimnasio ha alcanzado su capacidad máxima.")
            return
        if not nombre or not documento:
            print("Nombre y documento son obligatorios.")
            return
        if nombre.isdigit() or not nombre.isalpha():
            print("El nombre no debe contener números ni símbolos ni espacios.")
            return
        if documento.isalpha() or not documento.isdigit():
            print("El documento no debe contener letras ni símbolos ni espacios.")
            return
        
        nombre = nombre.lower()
        
        cliente_encontrado = None
        for cliente in self.__clientes:
            if cliente is not None:
                if nombre == cliente.get_nombre_c() and documento == cliente.get_documento_c():
                    cliente_encontrado = cliente

        if cliente_encontrado is None:
            print("Cliente no Encontrado")
            crear = input("¿Desea crearlo? (si/no)\nR// ")
            if not "no" in crear.lower():
                telefono = input("Telefono, enter para omitir")
                print(nombre, documento, telefono if telefono else "None")
                if not self.registrar_cliente(nombre, documento, telefono):
                    print(f"No se pudo registrar el cliente {nombre}, {documento}.")
                    return
                # Buscar el cliente recién creado
                for cliente in self.__clientes:
                    if cliente is not None:
                        if nombre == cliente.get_nombre_c() and documento == cliente.get_documento_c():
                            cliente_encontrado = cliente
                            break
            else:
                print("No se puede crear una membresía a un cliente no registrado.")
                return
        
        id_membresia = self.__historico_membresias + 1
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=30)
        
        pagar = input("Desea pagar inmediatamente. (si/no)\nR// ")
        if not "no" in pagar.lower():
            print(f"Efectivo actual: {self.__efectivo}")
            self.__efectivo += 50000
            print(f"Efectivo actualizado a: {self.__efectivo}")
            nueva_membresia = Membresia(id_membresia, fecha_inicio, fecha_fin, "Pagada")
        else:
            nueva_membresia = Membresia(id_membresia, fecha_inicio, fecha_fin)
        
        # Agregar la membresía al array de membresías
        for i in range(50):
            if self.__membresias[i] is None:
                self.__membresias[i] = nueva_membresia
                break
        
        self.__numero_membresias += 1
        self.__historico_membresias +=1
        print(f"Cliente {nombre}, la membresia con ID {id_membresia} fue creada con finalizacion : {fecha_fin}")
        
        cliente_encontrado.set_id_membresia(id_membresia)
        print(f"Cliente {cliente_encontrado.get_nombre_c()} ahora tiene la membresía con ID {cliente_encontrado.get_id_membresia()}.")


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
    
    def get_id_cliente(self):
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
    
    def set_id_membresia(self, id_membresia):
        self.__id_membresia = id_membresia
    
    
    # Métodos

    def pago_ingreso_unico(self):
        pass

    def pagar_membresia(self):
        if self.__id_membresia is None:
            print("No tiene una membresía asociada.")
            return
        else:
            for membresia in self.__membresias:
                if membresia.get_id_memebresia() == self.__id_membresia:
                    if membresia.get_estado_m() == "Pagada":
                        print("La membresía ya está pagada.")
                        return
                    else:
                        # Cambiar estado de la membresía a "Pagada"
                        membresia.set_estado_m("Pagada")
                        print(f"Membresía {membresia.get_id_m()} pagada exitosamente.")
                        return

    def solicitar_sesion(self):
        pass

class Membresia:
    """_summary_
    Clase que representa una membresía de gimnasio, contiene información sobre el estado, fechas y métodos para gestionar la membresía.
    
    Atributos:
        __id_membresia (int): Identificador único de la membresía.
        __estado (str, optional): Estado de la membresía (Pagada, Debe). Defaults to "Pagada".
        __fecha_inicio (str): Fecha de inicio de la membresía.
        __fecha_fin (str): Fecha de finalización de la membresía.
    """
    def __init__(self, id_membresia: int, fecha_inicio: str, fecha_fin: str, estado: str = "Debe"):
        self.__id_membresia = id_membresia
        self.__estado = estado
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        
    # Métodos de acceso
    
    def get_id_membresia(self):
        return self.__id_membresia
    
    def get_estado_m(self):
        return self.__estado
    
    def get_fecha_inicio_m(self):
        return self.__fecha_inicio
    
    def get_fecha_fin_m(self):
        return self.__fecha_fin
    
    def set_estado_m(self, estado: str):
        """_summary_
        Modifica el estado de la membresía.
        """
        if estado.lower() in ["pagada", "debe"]:
            self.__estado = estado
        else:
            print("Estado no válido. Debe ser 'Pagada' o 'Debe'")
    
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


def menu():
    print("\n=== Menú del Gimnasio ===")
    print("Gestionar CLientes")
    print("Gestionar Sesiones Especiales")
    
    opcion = input("Seleccione una opción: ")
    
    return opcion

def main():
    Gym = Gimnasio("Body Force","Barrio Candelilla", 3001234545, "body@force.com", 45000)
    Gym.ver_inf()
    Gym.registrar_cliente("Emanuel", "21554", "333333")
    print(Gym.get())
    Gym.visualizar_clientes()
    print(Gym.get())
    # Gym.crear_membresia("Emanuel", "21554")
    Gym.buscar_cliente()

main()
