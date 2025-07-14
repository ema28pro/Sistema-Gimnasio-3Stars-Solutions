import numpy as np
from datetime import date, timedelta, datetime

import Utils as ut

from Gimnasios import Gimnasio
from Clientes import Cliente, Membresia
from Sesiones import Entrenador, SesionEspecial

def menu():
    ut.sp(1)
    print("="*30)
    print("========= BIENVENIDO =========")
    print("="*30)
    while True:
        print("\n"*3)
        print("====== Menú del Gimnasio =====")
        print(30*"=")
        print("¿Que desea hacer?")
        print("1. Ver Clientes")
        print("2. Ver Membresias")
        print("3. Registrar Cliente")
        print("4. Buscar Cliente")
        print("5. Gestionar Eventos")
        print("6. Menu Datos")
        print("Enter para salir")
        opcion_menu = input("Ingrese una opcion : ")
        ut.sp(2)
        # Validar números fuera de rango en todos los match (ahora hasta opción 6)
        if opcion_menu not in ["1", "2", "3", "4", "5", "6", ""]:
            print("Opción fuera de rango. Por favor, ingrese una opción válida.")
            continue
        match opcion_menu:
            case "1":
                cliente = Gym.visualizar_clientes()
                if cliente:  # Solo proceder si se eligio un cliente
                    menu_cliente(cliente)
                else:
                    input("\nPresione Enter para continuar...")
            case "2":
                Gym.visualizar_membresias()
                input("\nPresione Enter para continuar...")
            case "3":
                cliente = Gym.crear_cliente()
                # input("\nPresione Enter para continuar...")
                if cliente:  # Solo proceder si se creó el cliente exitosamente
                    menu_cliente(cliente)
                else:
                    input("\nPresione Enter para continuar...")
            case "4":
                # Menu Acciones con Cliente
                cliente = Gym.buscar_cliente()
                # input("\nPresione Enter para continuar...")
                if cliente:  # Solo proceder si se encontró un cliente
                    menu_cliente(cliente)
                else:
                    input("\nPresione Enter para continuar...")
            case "5":
                menu_eventos()
            case "6":
                menu_datos()
            case "":
                while True:
                    confirmacion = input("¿Esta seguro de salir? (si/no): ")
                    if ut.valid_yes_no(confirmacion):
                        confirmacion = ut.yes_no(confirmacion)
                        break
                    else:
                        print("Por favor, ingrese 'si' o 'no'.")
                        continue
                if confirmacion:
                    print("Saliendo del menú principal...")
                    break
                else:
                    print("Regresando al menú principal...")

def menu_cliente(cliente):
    # Menu Acciones con Cliente
    while True:
        print("\n=== ¿Que desea hacer? ===")
        print(f"Cliente : {cliente.get_nombre()} , ID : {cliente.get_id_cliente()}")
        print(30*"=")
        print("1. Ver información del Cliente")
        print("2. Adquirir Membresía" , "(Sin Membresia)" if cliente.get_membresia() is None else "(Con Membresia)")
        print("3. Consultar Membresía" , "(Sin Membresia)" if cliente.get_membresia() is None else "")
        print("4. Agendar Sesión Especial")
        print("5. Pago Ingreso Único")
        print("6. Registrar Entrada")
        print("7. Eliminar Cliente")
        print("Enter para salir")
        opcion_cliente = input("Seleccione una opción : ")
        print(30*"=")
        ut.sp(2)
        if opcion_cliente not in ["1", "2", "3", "4", "5", "6", "7", ""]:
            print("Opción fuera de rango. Por favor, ingrese una opción válida.")
            continue
        
        match opcion_cliente:
            case "1":
                cliente.info_cliente()
                input("\nPresione Enter para continuar...")
            case "2":
                Gym.crear_membresia(cliente)
                input("\nPresione Enter para continuar...")
            case "3":
                membresia = Gym.consultar_membresia(cliente)
                # Menu Acciones con Membresia
                if membresia:
                    menu_membresia(membresia)
                else:
                    print("El cliente no tiene una membresía activa.")
                    input("\nPresione Enter para continuar...")
            case "4":
                Gym.agendar_sesion(cliente)
                input("\nPresione Enter para continuar...")
            case "5":
                Gym.pago_ingreso_unico(cliente)
                input("\nPresione Enter para continuar...")
            case "6":
                cliente.registrar_entrada("General") # Pensar de que clase hacerlo
                input("\nPresione Enter para continuar...")
            case "7":
                eliminar = None
                while eliminar is None:
                    eliminar = input("¿Esta seguro de eliminar el Cliente? (si/no)\nR// ")
                    if ut.valid_yes_no(eliminar):
                        if ut.yes_no(eliminar):
                            print(f"Cliente {cliente.get_nombre()} eliminando.")
                            Gym.eliminar_cliente(cliente)
                        else:
                            print(f"Cliente {cliente.get_nombre()} no eliminado.")
                        break
                    else:
                        eliminar = None
                input("\nPresione Enter para continuar...")
                print("Saliendo del menú de cliente...")
                break
            case "":
                print("Saliendo del menú de cliente...")
                break

def menu_membresia(membresia):
    # Menu Acciones con Membresia
    while True:
        print("====== ¿Que desea hacer? =====")
        print(30*"=")
        print("1. Ver Información de Membresía")
        print("2. Pagar Membresía" , "(Paga)" if membresia.get_pago() else "(Pendiente)")
        print("3. Eliminar Membresia")
        print("Enter para salir")
        opcion_membresia = input("Seleccione una opción : ")
        
        if opcion_membresia not in ["1", "2", "3", ""]:
            print("Opción fuera de rango. Por favor, ingrese una opción válida.")
            continue
    
        match opcion_membresia:
            case "1":
                membresia.ver_info()
                input("\nPresione Enter para continuar...")
            case "2":
                Gym.pagar_membresia(membresia)
                input("\nPresione Enter para continuar...")
            case "3":
                Gym.eliminar_membresia(membresia) # Pendiente, tmb incluir dias restantes y meter en ciclo
                input("\nPresione Enter para continuar...")
            case "":
                print("Saliendo del menú de membresía...")
                break

def menu_eventos():
    while True:
        print("\n=== Menú de Eventos ===")
        print("1. Crear Entrenador")
        print("2. Buscar Entrenador")
        print("3. Ver Entrenadores")
        print("4. Ver Sesiones Especiales")
        print("Enter para salir")
        opcion_evento = input("Seleccione una opción: ")
        if opcion_evento not in ["1", "2", "3", "4", ""]:
            print("Opción fuera de rango. Por favor, ingrese una opción válida.")
            continue
        
        match opcion_evento:
            case "1":
                entrenador = Gym.crear_entrenador()
                if entrenador:
                    menu_entrenador(entrenador)
                else:
                    input("\nPresione Enter para continuar...")
            case "2":
                entrenador = Gym.buscar_entrenador()
                if entrenador:
                    menu_entrenador(entrenador)
                else:
                    input("\nPresione Enter para continuar...")
            case "3":
                entrenador = Gym.mostrar_entrenadores()
                if entrenador:
                    menu_entrenador(entrenador)
                else:
                    input("\nPresione Enter para continuar...")
            case "4":
                sesion = Gym.mostrar_sesiones()
                if sesion:
                    menu_sesion(sesion)
                else:
                    input("\nPresione Enter para continuar...")
            case "":
                print("Saliendo del menú de eventos...")
                break

def menu_entrenador(entrenador):
    print("====== ¿Que desea hacer? =====")
    print(30*"=")
    print("1. Crear Sesion")
    print("2. Eliminar Entrenador")
    print("Enter para salir")
    opcion_entrenador = input("Seleccione una opción : ")
    if opcion_entrenador not in ["1", "2", ""]:
        print("Opción fuera de rango. Por favor, ingrese una opción válida.")
        return
    match opcion_entrenador:
        case "1":
            Gym.crear_sesion_especial(entrenador)
            input("\nPresione Enter para continuar...")
        case "2":
            Gym.eliminar_entrenador(entrenador.get_id_entrenador())
            input("\nPresione Enter para continuar...")
        case "":
            print("Saliendo del menú de entrenador...")

def menu_sesion(sesion):
    print("\n=== ¿Que desea hacer? ===")
    print(30*"=")
    print("1. Editar Inscritos")
    print("2. Cambiar Entrenador")
    print("3. Eliminar Sesión Especial")
    print("Enter para salir")
    opcion_sesion = input("Seleccione una opción : ")
    if opcion_sesion not in ["1", "2", "3", ""]:
        print("Opción fuera de rango. Por favor, ingrese una opción válida.")
        return
    match opcion_sesion:
        case "1":
            sesion.editar_inscritos()
            input("\nPresione Enter para continuar...")
        case "2":
            print(f"=> Sesion con entrenador:")
            sesion.ver_entrenador()
            while True:
                confirmacion = input("¿Estas seguro de cambiar el entrenador? (si/no): ")
                if ut.valid_yes_no(confirmacion):
                    break
            confirmacion = ut.yes_no(confirmacion)
            if confirmacion:
                entrenador = Gym.mostrar_entrenadores()
                if entrenador:
                    sesion.set_entrenador(entrenador)
                    print(f"Entrenador cambiado a: {sesion.get_entrenador().get_nombre()}")
                else:
                    print("No se encontró un entrenador para cambiar.")
            else:
                print("Cambio de entrenador cancelado.")
            input("\nPresione Enter para continuar...")
        case "3":
            Gym.eliminar_sesion(sesion)
            input("\nPresione Enter para continuar...")
        case "":
            print("Saliendo del menú de sesión especial...")

def menu_datos():
    while True:
        print("\n=== Menú de Datos ===")
        print("1. Reporte Diario")
        print("2. Seguimiento de Membresías")
        print("3. Informe Entradas")
        print("4. Análisis Financiero")
        print("5. Exportar Clientes")
        print("6. Cargar Clientes")
        print("7. Exportar Entrenadores")
        print("10. Exportar Gimansio.JSON")
        print("Enter para salir")
        opcion_datos = input("Seleccione una opción : ")
        
        if opcion_datos not in ["1", "2", "3", "4", "5", "6", "7", "10", ""]:
            print("Opción fuera de rango. Por favor, ingrese una opción válida.")
            continue
        
        match opcion_datos:
            case "1":
                Gym.reporte_diario()
                input("\nPresione Enter para continuar...")
            case "2":
                Gym.seguimiento_membresias()
                input("\nPresione Enter para continuar...")
            case "3":
                Gym.informe_entrada()
                input("\nPresione Enter para continuar...")
            case "4":
                Gym.analisis_financiero()
            case "5":
                Gym.exportar_clientes()
            case "6":
                Gym.cargar_clientes()
            case "7":
                Gym.exportar_entrenadores()
            case "10":
                archivo_creado = Gym.exportar_datos_json()
                if archivo_creado:
                    print(f"Los datos se han guardado en: {archivo_creado}")
                input("\nPresione Enter para continuar...")
            case "":
                print("Saliendo del menú de datos...")
                break

def exportar_datos_rapido():
    # Eliminar
    """
    Función auxiliar para exportar datos rápidamente sin pasar por el menú
    """
    print("\n=== Exportación Rápida de Datos ===")
    archivo = Gym.exportar_datos_json()
    return archivo

def App():
    # Gym = Gimnasio("Body Force","Barrio Candelilla", "3001234545", "body@force.com", 45000)
    # Gym.ver_info()
    
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
    
    menu()
    
    # Gym.exportar_clientes()
    
    # Exportación automática al finalizar (opcional)
    # exportar_datos_rapido(Gym)
    
    # print(Gym.get())


if __name__ == "__main__":
    Gym = Gimnasio("Body Force","Barrio Candelilla", "3001234545", "body@force.com", 45000)
    Gym.ver_info()
    App()
    # menu_eventos()
