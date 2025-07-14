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
    def __init__(self, fecha_inicio, fecha_fin, pago: bool = False):
        self.__pago = pago
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        
    # Métodos de acceso y modificación
    
    def get_pago(self):
        return self.__pago
    
    def get_fecha_inicio(self):
        # Retornar como string
        return self.__fecha_inicio.strftime("%Y-%m-%d")
    
    def get_fecha_fin(self):
        # Retornar como string
        return self.__fecha_fin.strftime("%Y-%m-%d")
    
    def set_pago(self, estado: bool):
        self.__pago = estado
    
    # Métodos

    def calcular_dias_restantes(self):
        if isinstance(self.__fecha_fin, str):
            fecha_fin_obj = datetime.strptime(self.__fecha_fin, "%Y-%m-%d").date()
            self.__fecha_fin = fecha_fin_obj  # Actualizar el atributo para que sea un objeto date
        else:
            fecha_fin_obj = self.__fecha_fin
        return (fecha_fin_obj - date.today()).days

    def renovar_membresia(self,fecha_inicio=None, fecha_fin=None):
        """Renueva la membresía por 30 días a partir de la fecha de inicio proporcionada o la fecha actual si no se proporciona."""
        if not self.__pago:
            print("La membresía no ha sido pagada. No se puede renovar.")
            return
        
        if self.calcular_dias_restantes() > 0:
            print("La membresía aún está activa y no necesita renovación.")
            return
        
        if fecha_inicio is None:
            fecha_inicio = date.today()
        
        # Validar que la fecha de inicio sea un objeto date
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        
        if fecha_fin is None:
            nueva_fecha_fin = fecha_inicio + timedelta(days=30)
        else:
            if not isinstance(fecha_fin, date):
                if isinstance(fecha_fin, str):
                    nueva_fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
                else:
                    print("Fecha de fin inválida para calcular diferencia.")
                    return False
            
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
                fecha_fin_correcta = fecha_inicio + timedelta(days=30)
                
                nueva_fecha_fin = fecha_fin_correcta
                print(f"Se ha actualizado la fecha de fin a: {nueva_fecha_fin}")
        
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = nueva_fecha_finGimnasio.renovar_membresia() got an unexpected keyword argument 'cliente'
        print(f"Memebresia actualizada: Inicio: {self.__fecha_inicio}, Fin: {self.__fecha_fin}")
    
    def ver_info(self):
        """Muestra información de la membresía"""
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
    def __init__(self, id_cliente: int, nombre: str, documento: str, fecha_registro, telefono: str = None):
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
        if isinstance(self.__fecha_registro, str):
            return self.__fecha_registro
        else:
            return self.__fecha_registro.strftime("%Y-%m-%d")
    
    def get_membresia(self):
        return self.__membresia
    
    def set_membresia(self, membresia : Membresia):
        self.__membresia = membresia
    
    # Métodos
    
    def info_cliente(self):
        """Muestra información del cliente"""
        print(f"\n=== Información del Cliente ===")
        print(f"ID: {self.__id_cliente}")
        print(f"Nombre: {self.__nombre}")
        print(f"Documento: {self.__documento}")
        print(f"Teléfono: {self.__telefono if self.__telefono else 'No proporcionado'}")
        
        # Manejar tanto objetos date como strings para la fecha
        if isinstance(self.__fecha_registro, str):
            print(f"Fecha de Registro: {self.__fecha_registro}")
        else:
            print(f"Fecha de Registro: {self.__fecha_registro.strftime('%Y-%m-%d')}")
            
        if self.__membresia:
            print("Membresía Activa:")
            self.info_membresia()
        else:
            print("No tiene membresía activa.")
        print("="*40)
    
    def tiene_membresia(self):
        """Verifica si el cliente tiene una membresía activa"""
        if self.__membresia:
            return "Con Membresía" , self.estado_pago_membresia(), self.estado_vigencia_membresia()
        else:
            return "Sin Membresía"
    
    def estado_pago_membresia(self):
        """Verifica el estado de la membresía del cliente"""
        if self.__membresia:
            if self.__membresia.get_pago():
                return "Paga"
            else:
                return "Pendiente"
        else:
            return "Sin Membresía"
    
    def estado_vigencia_membresia(self):
        """Verifica si la membresía está vigente"""
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

    def registrar_entrada(self,motivo:str=None):
        """Registra la entrada del cliente al gimnasio"""
        formato = "Fecha;Hora;ID;Documento;Nombre;Membresía(False/True/None)"
        
        fecha = datetime.now().strftime('%Y-%m-%d')
        hora = datetime.now().strftime('%H:%M:%S')
        id_cliente = self.__id_cliente
        documento = self.__documento
        nombre = self.__nombre
        estado_membresia = self.__membresia.get_pago() if self.__membresia else "None"
        
        # Solución: usar variable auxiliar para evitar anidación de comillas
        motivo_campo = f";{motivo}" if motivo else ""
        registro = f"{fecha};{hora};{id_cliente};{documento};{nombre};{estado_membresia}{motivo_campo}\n"
        
        with open("registros/Entradas.txt", "a") as entrada_file:
            entrada_file.write(registro)
        
        print(f"✓ Entrada registrada para {nombre} a las {hora}")



