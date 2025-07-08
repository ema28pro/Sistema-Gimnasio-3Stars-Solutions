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

def main():
    Gym = Gimnasio("Body Force","Barrio Candelilla", "3001234545", "body@force.com", 45000)
    Gym.ver_inf()
    
    ut.sp()
    
    # Registro de 20 clientes diferentes
    print("=== Registrando clientes ===")
    
    Gym.registrar_cliente("Emanuel", "21254", "333333")
    Gym.registrar_cliente("Sofia", "10234567", "3201234567")
    Gym.registrar_cliente("Carlos", "20345678", "3112345678")
    Gym.registrar_cliente("Maria", "30456789", "3223456789")
    Gym.registrar_cliente("Andres", "40567890", "3334567890")
    Gym.registrar_cliente("Valentina", "50678901", "3145678901")
    Gym.registrar_cliente("Sebastian", "60789012", "3256789012")
    Gym.registrar_cliente("Camila", "70890123", "3167890123")
    Gym.registrar_cliente("Daniel", "80901234", "3278901234")
    Gym.registrar_cliente("Isabella", "91012345", "3189012345")
    Gym.registrar_cliente("Miguel", "12123456", "3290123456")
    Gym.registrar_cliente("Alejandra", "23234567", "3101234567")
    Gym.registrar_cliente("Felipe", "34345678", "3212345678")
    Gym.registrar_cliente("Natalia", "45456789", "3123456789")
    Gym.registrar_cliente("Joaquin", "56567890", "3234567890")
    Gym.registrar_cliente("Gabriela", "67678901", "3145678902")
    Gym.registrar_cliente("Nicolas", "78789012", "3256789013")
    Gym.registrar_cliente("Paola", "89890123", "3167890124")
    Gym.registrar_cliente("Ricardo", "90901234", "3278901235")
    Gym.registrar_cliente("Fernanda", "11012345", "3189012346")
    
    print("=== Todos los clientes registrados ===")
    
    ut.sp(2)
    Gym.visualizar_clientes()
    while True:
        Gym.buscar_cliente()
    # print(Gym.get())

main()
