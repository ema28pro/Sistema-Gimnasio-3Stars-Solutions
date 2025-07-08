# ===== CONFIGURACIÓN DEL SISTEMA =====
"""
Opcional?

Archivo de configuración para el Sistema de Gimnasio 3Stars Solutions
Contiene todas las constantes y configuraciones del sistema
"""

# ===== PRECIOS =====
class Precios:
    """Configuración de precios del gimnasio"""
    MEMBRESIA_MENSUAL = 50000
    ENTRADA_UNICA = 8000
    SESION_ESPECIAL = 15000
    
    # Descuentos
    DESCUENTO_ESTUDIANTE = 0.20  # 20% descuento
    DESCUENTO_TERCERA_EDAD = 0.15  # 15% descuento

# ===== LÍMITES DEL SISTEMA =====
class Limites:
    """Configuración de límites del sistema"""
    MAX_CLIENTES = 50
    MAX_MEMBRESIAS = 50
    MAX_ENTRENADORES = 10
    MAX_SESIONES = 20
    MAX_CUPOS_SESION = 25
    
    # Duración de membresía en días
    DURACION_MEMBRESIA = 30

# ===== CONFIGURACIÓN DE SESIONES =====
class SesionesConfig:
    """Configuración de sesiones especiales"""
    TIPOS_SESION = ["Boxeo", "Yoga", "Aeróbicos", "Funcional", "Spinning"]
    HORARIOS_DISPONIBLES = [
        "06:00", "07:00", "08:00", "09:00", "10:00",
        "16:00", "17:00", "18:00", "19:00", "20:00"
    ]

# ===== CONFIGURACIÓN GENERAL =====
class ConfigGeneral:
    """Configuración general del sistema"""
    FORMATO_FECHA = "%d/%m/%Y"
    MONEDA = "COP"
    SIMBOLO_MONEDA = "$"
    
    # Información del gimnasio por defecto
    NOMBRE_GIMNASIO = "Body Force"
    TELEFONO_GIMNASIO = "300-123-4567"
    EMAIL_GIMNASIO = "info@bodyforce.com"
    DIRECCION_GIMNASIO = "Calle 123 #45-67, Barrio Centro"

# ===== MENSAJES DEL SISTEMA =====
class Mensajes:
    """Mensajes predefinidos del sistema"""
    BIENVENIDA = "¡Bienvenido al Sistema de Gimnasio 3Stars Solutions!"
    CLIENTE_REGISTRADO = "Cliente registrado exitosamente."
    CLIENTE_NO_ENCONTRADO = "Cliente no encontrado en el sistema."
    MEMBRESIA_CREADA = "Membresía creada exitosamente."
    PAGO_EXITOSO = "Pago procesado exitosamente."
    OPERACION_CANCELADA = "Operación cancelada por el usuario."
    CAPACIDAD_MAXIMA = "Se ha alcanzado la capacidad máxima."
    
    # Errores comunes
    ERROR_DATOS_INVALIDOS = "Los datos ingresados no son válidos."
    ERROR_CLIENTE_EXISTENTE = "El cliente ya está registrado en el sistema."
    ERROR_MEMBRESIA_VENCIDA = "La membresía ha vencido."

# ===== FUNCIONES PARA GESTIONAR PRECIOS =====

def get_precio_membresia():
    """Obtiene el precio actual de la membresía"""
    return PRECIO_MEMBRESIA

def get_precio_entrada_unica():
    """Obtiene el precio actual de la entrada única"""
    return PRECIO_ENTRADA_UNICA

def actualizar_precio_membresia(nuevo_precio):
    """Actualiza el precio de la membresía (solo para administradores)"""
    global PRECIO_MEMBRESIA
    if nuevo_precio > 0:
        PRECIO_MEMBRESIA = nuevo_precio
        print(f"Precio de membresía actualizado a: ${PRECIO_MEMBRESIA:,}")
        return True
    else:
        print("El precio debe ser mayor a 0")
        return False

def actualizar_precio_entrada_unica(nuevo_precio):
    """Actualiza el precio de la entrada única (solo para administradores)"""
    global PRECIO_ENTRADA_UNICA
    if nuevo_precio > 0:
        PRECIO_ENTRADA_UNICA = nuevo_precio
        print(f"Precio de entrada única actualizado a: ${PRECIO_ENTRADA_UNICA:,}")
        return True
    else:
        print("El precio debe ser mayor a 0")
        return False

def mostrar_precios():
    """Muestra los precios actuales del sistema"""
    print("\n=== PRECIOS ACTUALES ===")
    print(f"💳 Membresía mensual: ${PRECIO_MEMBRESIA:,}")
    print(f"🎫 Entrada única: ${PRECIO_ENTRADA_UNICA:,}")
    print("========================\n")

# ===== Gestionar Precios Gimnasio =====

def gestionar_precios(self):
    """Menú para gestionar precios del gimnasio (solo administradores)"""
    print("\n=== Gestión de Precios ===")
    ut.mostrar_precios()
    
    print("1. Actualizar precio de membresía")
    print("2. Actualizar precio de entrada única")
    print("3. Ver precios actuales")
    print("Enter para salir")
    
    opcion = input("Seleccione una opción: ")
    
    match opcion:
        case "1":
            while True:
                nuevo_precio = input("Ingrese el nuevo precio de membresía: ")
                if ut.is_positve(nuevo_precio, "Precio"):
                    ut.actualizar_precio_membresia(int(nuevo_precio))
                    break
        case "2":
            while True:
                nuevo_precio = input("Ingrese el nuevo precio de entrada única: ")
                if ut.is_positve(nuevo_precio, "Precio"):
                    ut.actualizar_precio_entrada_unica(int(nuevo_precio))
                    break
        case "3":
            ut.mostrar_precios()
        case "":
            print("Saliendo de gestión de precios.")