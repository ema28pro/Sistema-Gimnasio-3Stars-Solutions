import numpy as np
from datetime import date, timedelta









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
