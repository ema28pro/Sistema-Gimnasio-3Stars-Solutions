import numpy as np
from datetime import date

import Utils as ut

from Gimnasios import Gimnasio
from Clientes import Cliente, Membresia
from Sesiones import Entrenador, SesionEspecial

def menu():
    print("\n=== Menú del Gimnasio ===")
    print("Gestionar CLientes")
    print("Gestionar Sesiones Especiales")
    
    opcion = input("Seleccione una opción: ")
    
    return opcion

# Pensar en  Clase APP y lo que implica
# class Main:
#     def __init__(self, gimnasio: Gimnasio):
#         self.gimnasio = gimnasio
    
    
    
    
    
def menu_cliente(cliente):
    while True:
        print("\n=== ¿Que desea hacer? ===")
        print(f"Cliente : {cliente.get_nombre_c()} , ID : {cliente.get_id_cliente()}")
        print(30*"=")
        print("1. Adquirir Membresía" , "(Sin Membresia)" if cliente.get_membresia() is None else "(Con Membresia)")
        print("2. Consultar Membresía")
        print("3. Pago Ingreso Único")
        print("4. Agendar Sesión Especial")
        print("5. Cancelar Sesión Especial")
        print("6. Registrar Entrada")
        print("7. Eliminar Cliente")
        print("Enter para salir")
        opcion_cliente = input("Seleccione una opción : ")
        print(30*"=")
        ut.sp(2)
        
        match opcion_cliente:
            case "1":
                Gym.crear_membresia(cliente)
            case "2":
                # Menu Acciones con Membresia
                membresia = Gym.consultar_membresia(cliente)
                print("====== ¿Que desea hacer? =====")
                print(30*"=")
                print("1. Pagar Membresía" , "(Paga)" if membresia.get_pago_m() else "(Pendiente)")
                print("2. Eliminar Membresia")
                print("Enter para salir")
                opcion_membresia = input("Seleccione una opción : ")
                
                match opcion_membresia:
                    case "1":
                        Gym.pagar_membresia(membresia)
                    case "2":
                        Gym.eliminar_membresia(membresia) # Pendiente, tmb incluir dias restantes y meter en ciclo
                    case "":
                        print("Saliendo del menú de membresía.")
                        break


def exportar_datos_rapido(gimnasio):
    """
    Función auxiliar para exportar datos rápidamente sin pasar por el menú
    """
    print("\n=== Exportación Rápida de Datos ===")
    archivo = gimnasio.exportar_datos_json()
    return archivo

def App():
    # Gym = Gimnasio("Body Force","Barrio Candelilla", "3001234545", "body@force.com", 45000)
    # Gym.ver_inf()
    
    ut.sp()
    
    # Registro de 20 clientes diferentes
    print("=== Registrando clientes ===")
    
    # Gym.crear_cliente("Emanuel", "21254", "333333")
    # Gym.crear_cliente("Sofia", "10234567", "3201234567")
    # Gym.crear_cliente("Carlos", "20345678", "3112345678")
    # Gym.crear_cliente("Maria", "30456789", "3223456789")
    # Gym.crear_cliente("Andres", "40567890", "3334567890")
    # Gym.crear_cliente("Valentina", "50678901", "3145678901")
    # Gym.crear_cliente("Sebastian", "60789012", "3256789012")
    # Gym.crear_cliente("Camila", "70890123", "3167890123")
    # Gym.crear_cliente("Daniel", "80901234", "3278901234")
    # Gym.crear_cliente("Isabella", "91012345", "3189012345")
    # Gym.crear_cliente("Miguel", "12123456", "3290123456")
    # Gym.crear_cliente("Alejandra", "23234567", "3101234567")
    # Gym.crear_cliente("Felipe", "34345678", "3212345678")
    # Gym.crear_cliente("Natalia", "45456789", "3123456789")
    # Gym.crear_cliente("Joaquin", "56567890", "3234567890")
    # Gym.crear_cliente("Gabriela", "67678901", "3145678902")
    # Gym.crear_cliente("Nicolas", "78789012", "3256789013")
    # Gym.crear_cliente("Paola", "89890123", "3167890124")
    # Gym.crear_cliente("Ricardo", "90901234", "3278901235")
    # Gym.crear_cliente("Fernanda", "11012345", "3189012346")
    
    Gym.cargar_clientes("clientes.txt")
    
    print("=== Todos los clientes registrados ===")
    
    ut.sp(2)
    Gym.visualizar_clientes()
    ut.sp(2)
    
    while True:
        print("\n"*5)
        print("========= BIENVENIDO =========")
        print(30*"=")
        print("¿Que desea hacer?")
        print("1. Ver Clientes")
        print("2. Ver Membresias")
        print("3. Registrar Cliente")
        print("4. Buscar Cliente")
        print("5. Exportar Datos a JSON")
        print("Enter para salir")
        opcion = input("Ingrese una opcion : ")
        ut.sp(2)
        match opcion:
            case "1":
                Gym.visualizar_clientes()
                input("\nPresione Enter para continuar...")
            case "2":
                Gym.visualizar_membresias()
                input("\nPresione Enter para continuar...")
            case "3":
                cliente = Gym.crear_cliente()
                input("\nPresione Enter para continuar...")
                menu_cliente(cliente)
            case "4":
                # Menu Acciones con Cliente
                cliente = Gym.buscar_cliente()
                input("\nPresione Enter para continuar...")
                while True:
                    print("\n=== ¿Que desea hacer? ===")
                    print(f"Cliente : {cliente.get_nombre_c()} , ID : {cliente.get_id_cliente()}")
                    print(30*"=")
                    print("1. Adquirir Membresía" , "(Sin Membresia)" if cliente.get_membresia() is None else "")
                    print("2. Consultar Membresía")
                    print("3. Pago Ingreso Único")
                    print("4. Agendar Sesión Especial")
                    print("5. Cancelar Sesión Especial")
                    print("6. Registrar Entrada")
                    print("7. Eliminar Cliente")
                    print("Enter para salir")
                    opcion_cliente = input("Seleccione una opción : ")
                    print(30*"=")
                    ut.sp(2)
                    
                    match opcion_cliente:
                        case "1":
                            Gym.crear_membresia(cliente)
                        case "2":
                            # Menu Acciones con Membresia
                            membresia = Gym.consultar_membresia(cliente)
                            print("====== ¿Que desea hacer? =====")
                            print(30*"=")
                            print("1. Pagar Membresía" , "(Paga)" if membresia.get_pago_m() else "(Pendiente)")
                            print("2. Eliminar Membresia")
                            print("Enter para salir")
                            opcion_membresia = input("Seleccione una opción : ")
                            
                            match opcion_membresia:
                                case "1":
                                    Gym.pagar_membresia(membresia)
                                case "2":
                                    Gym.eliminar_membresia(membresia) # Pendiente, tmb incluir dias restantes y meter en ciclo
                                case "":
                                    print("Saliendo del menú de membresía.")
                                    break
                        case "3":
                            Gym.pago_ingreso_unico(cliente)
                        case "4":
                            Gym.agendar_sesion(cliente)
                        case "5":
                            Gym.cancelar_sesion(cliente)
                        case "6":
                            cliente.registrar_entrada()
                        case "7":
                            if eliminar is None:
                                while True: # Ciclo para Ingreso correcto del pago
                                    eliminar = input("¿Desea pagar inmediatamente? (si/no)\nR// ")
                                    if ut.valid_yes_no(eliminar):
                                        print(f"Cliente {cliente.get_nombre_c()} eliminado.")
                                        Gym.eliminar_cliente(cliente)
                                        break
                            break
                        case "":
                            print("Saliendo del menú de cliente.")
                            break
            case "5":
                print("\n=== Exportar Datos a JSON ===")
                nombre_archivo = input("Nombre del archivo (opcional, presione Enter para generar automáticamente): ").strip()
                if nombre_archivo == "":
                    nombre_archivo = None
                
                archivo_creado = Gym.exportar_datos_json(nombre_archivo)
                if archivo_creado:
                    print(f"Los datos se han guardado en: {archivo_creado}")
                input("\nPresione Enter para continuar...")
            case "":
                break
    
    # Ejemplo de exportación automática al finalizar (opcional)
    exportar_datos_rapido(Gym)
    
    # print(Gym.get())

if __name__ == "__main__":
Gym = Gimnasio("Body Force","Barrio Candelilla", "3001234545", "body@force.com", 45000)
Gym.ver_inf()
App()
