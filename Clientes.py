from datetime import date, timedelta, datetime
import Utils as ut
from Utils import PRECIO_MEMBRESIA



# ==== CLIENTES Y MEMBRESÍA ====

class Membresia:
    """_summary_
    Clase que representa una membresía de gimnasio, contiene información sobre el estado, fechas y métodos para gestionar la membresía.
    
    Atributos:
        __pago (bool): Indica si la membresía ha sido pagada o no. Defaults to False.
        __fecha_inicio (str): Fecha de inicio de la membresía.
        __fecha_fin (str): Fecha de finalización de la membresía.
    """
    def __init__(self, fecha_inicio: str, fecha_fin: str, pago: bool = False):
        self.__pago = pago
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
    
    # Métodos de acceso y modificación
    
    def get_pago(self):
        # Retorna el Boolean de pago
        return self.__pago
    
    def get_fecha_inicio(self):
        # Retornar como string
        return self.__fecha_inicio
    
    def get_fecha_fin(self):
        # Retornar como string
        return self.__fecha_fin
    
    def set_pago(self, estado: bool):
        self.__pago = estado
    
    # Métodos

    def calcular_dias_restantes(self):
        """_summary_
            Calcula los días restantes para que la membresia expire.
        Returns:
            int: Número de días restantes.
        """
        # Convertimos la fecha fin de str a objeto date
        fecha_fin_obj = datetime.strptime(self.__fecha_fin, "%Y-%m-%d").date()
        dias_restantes = (fecha_fin_obj - date.today()).days
        return dias_restantes

    def renovar_membresia(self, fecha_inicio: str=None, fecha_fin: str=None):
        """_summary_
            Actualiza la membresia, renovandola por 30 días a partir de la fecha de inicio proporcionada o la fecha actual si no se proporciona.
        Args:
            fecha_inicio (str, optional): Fecha de inicio de la membresia. Defaults to None.
            fecha_fin (str, optional): Fecha de finalizacion de la membresia, 30 dias despues de la fecha de incio. Defaults to None.

        Returns:
            bool: Booleano indicando si la renovación fue exitosa.
        """        
        
        if not self.__pago:
            print("La membresía no ha sido pagada. No se puede renovar.")
            return False
        
        if self.calcular_dias_restantes() > 0:
            print("La membresía aún está activa y no necesita renovación.")
            return False
        
        # Obtenemos el objeto date actual si no se nos dia fecha de inicio
        if fecha_inicio is None:
            fecha_inicio = date.today()
        else:
            # Si se nos dio una fecha de inicio, la convertimos a objeto date para operar
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        
        if fecha_fin is None:
            # Calcular la fecha de fin como 30 días después de el objeto fecha inicio
            fecha_fin = fecha_inicio + timedelta(days=30)
        else:
            # Si se nos dio una fecha de fin, la convertimos a objeto date
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            
            
            # Calcular la diferencia en días
            diferencia_dias = (nueva_fecha_fin - fecha_inicio).days
            # Comprobar si la diferencia es exactamente 30 días
            if diferencia_dias != 30:
                print(f"La diferencia entre la fecha de inicio y fin es de {diferencia_dias} días, no los 30 días estándar.")
                if diferencia_dias > 30:
                    print(f"Hay {diferencia_dias - 30} días adicionales.")
                else:
                    print(f"Faltan {30 - diferencia_dias} días para completar los 30 días estándar.")
                
                # Calcular la fecha de fin correcta (30 días después de la fecha de inicio)
                fecha_fin = fecha_inicio + timedelta(days=30)
                
                print(f"Se ha actualizado la fecha de fin a: {fecha_fin}")
        
        self.__fecha_inicio = fecha_inicio.strftime("%Y-%m-%d") # Convertir a string
        self.__fecha_fin = fecha_fin.strftime("%Y-%m-%d") # Convertir a string
        print(f"Memebresia actualizada: Inicio: {self.__fecha_inicio}, Fin: {self.__fecha_fin}")
    
    def ver_info(self):
        """_summary_
            Muestra la información de la membresía.
        """        
        print(f"\n=== Información de Membresía ===")
        print(f"Fecha de inicio: {self.get_fecha_inicio()}")
        print(f"Fecha de fin: {self.get_fecha_fin()}")
        print(f"Estado de pago: {'Pagada' if self.__pago else 'Pendiente'}")
        dias_restantes = self.calcular_dias_restantes()
        if dias_restantes >= 0:
            print(f"Días restantes: {dias_restantes}")
        else:
            print("La membresía ha expirado.")
        print("="*40)

class Cliente:
    """
    Clase que representa un cliente del gimnasio, contiene información personal y métodos para gestionar membresías y sesiones especiales.
    
    Atributos:
        __id_cliente (int): Identificador único del cliente.
        __nombre (str): Nombre completo del cliente.
        __documento (str): Documento de identidad del cliente.
        __telefono (str, optional): Número de teléfono del cliente. Defaults to None.
        __fecha_registro (str): Fecha de registro del cliente en el gimnasio.
        __membresia (Membresia, optional): Objeto Membresía asociada al cliente. Defaults to None.
    """
    def __init__(self, id_cliente: int, nombre: str, documento: str, fecha_registro: str, telefono: str = None):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__documento = documento
        self.__telefono = telefono
        self.__fecha_registro = fecha_registro

        self.__membresia = None 
        
    # Métodos de acceso y modificación
    
    def get_id_cliente(self):
        return self.__id_cliente
    
    def get_nombre(self):
        return self.__nombre
    
    def get_documento(self):
        return self.__documento
    
    def get_telefono(self):
        return self.__telefono
    
    def get_fecha_registro(self):
        return self.__fecha_registro
    
    def get_membresia(self):
        return self.__membresia
    
    def set_membresia(self, membresia : Membresia):
        self.__membresia = membresia
    
    # Métodos
    
    def info_cliente(self):
        """_summary_
            Muestra informacion del cliente
        """        
        print(f"\n=== Información del Cliente ===")
        print(f"ID: {self.__id_cliente}")
        print(f"Nombre: {self.__nombre}")
        print(f"Documento: {self.__documento}")
        print(f"Teléfono: {self.__telefono if self.__telefono else 'No proporcionado'}")
        print(f"Fecha de Registro: {self.__fecha_registro}")
        
        # Verificar si el cliente tiene una membresia
        if self.__membresia:
            print("Membresia Activa:")
            self.info_membresia()
        else:
            print("No tiene membresia activa.")
        print("="*40)
    
    def tiene_membresia(self):
        """Retorna el estado de la membresía del cliente."""
        if self.__membresia:
            return "Con Membresía" , self.estado_pago_membresia(), self.estado_vigencia_membresia()
        else:
            return "Sin Membresía"
    
    def estado_pago_membresia(self):
        """Retorna el estado de pago de la membresía del cliente."""
        if self.__membresia:
            if self.__membresia.get_pago():
                return "Paga"
            else:
                return "Pendiente"
        else:
            return "Sin Membresía"
    
    def estado_vigencia_membresia(self):
        """Retorna el estado de vigencia de la membresía del cliente."""
        if self.__membresia:
            dias_restantes = self.__membresia.calcular_dias_restantes()
            if dias_restantes > 0:
                return "Activa"
            elif dias_restantes == 0:
                return "Vigente, expira hoy"
            else:
                return "Expirada"
        else:
            return "Sin Membresía"
    
    def info_membresia(self):
        """Muestra información de la membresía del cliente"""
        if self.__membresia is None:
            print(f"El cliente {self.__nombre} no tiene membresía.")
        else:
            print(f"\n=== Información de Membresía de {self.__nombre} ===")
            print(f"Fecha de inicio: {self.__membresia.get_fecha_inicio()}")
            print(f"Fecha de fin: {self.__membresia.get_fecha_fin()}")
            print(f"Estado de pago: {'Pagada' if self.__membresia.get_pago() else 'Pendiente'}")
            print("="*40)

    def registrar_entrada(self, motivo: str=None):
        """_summary_
            Registra la del cliente al gimnasio, 
            guardando la fecha, hora, ID, documento, nombre y estado de la membresía
            En el archivo correspondiente 'registros/Entradas.txt'.
        Args:
            motivo (str, optional): Motivo de la entrada. Defaults to None.
        """           
        # Fecha;Hora;ID;Documento;Nombre;Membresía(False/True/None)
        
        registro_entradas = "registros/Entradas.txt"
        
        fecha = datetime.now().strftime('%Y-%m-%d') # Genera el objeto fecha y hora actual y lo convierte a fecha string
        hora = datetime.now().strftime('%H:%M:%S') # Genera el objeto fecha y hora actual y lo convierte a hora string
        estado_membresia = self.__membresia.get_pago() if self.__membresia else "None" # Estado de la membresía (True/False/None)
        
        motivo_registro = f";{motivo}" if motivo else "" # sise coloco un motivo lo agrega al registro
        registro = f"{fecha};{hora};{self.__id_cliente};{self.__documento};{self.__nombre};{estado_membresia}{motivo_registro}\n"
        
        # Guardar el registro en el archivo
        with open(registro_entradas, "a") as entrada_file:
            entrada_file.write(registro)
        
        print(f"✓ Entrada registrada para {self.__nombre} a las {hora}")
