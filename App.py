import numpy as np
from datetime import date

from Gimnasios import Gimnasio
from Clientes import Cliente, Membresia
from Sesiones import Entrenador, SesionEspecial

def main():
    Gym = Gimnasio("Body Force","Barrio Candelilla", 3001234545, "body@force.com", 45000)
    # Gym.ver_inf()
    Gym.registrar_cliente("Emanuel", "21554", "0")
    print(Gym.get())
    Gym.visualizar_clientes()

main()
