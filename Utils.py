# ===== CONSTANTES DEL SISTEMA =====
PRECIO_MEMBRESIA = 50000  # Precio mensual de la membresía
PRECIO_ENTRADA_UNICA = 8000  # Precio de entrada por día

# ===== FUNCIONES DE VALIDACIÓN =====

def is_number(numero: str, tipo = None):
    # Adveritencia
    
    if tipo:
        advertencia = f"El {tipo} debe ser un número válido, sin espacios."
    else:
        advertencia = "Debe ser un número válido, sin espacios."
    
    # Validacion
    
    if numero.isalpha() or not numero.isdigit():
        print(advertencia) # Imprime advertencia
        return False
    else:
        return True

def is_positve(numero: str, tipo = None):
    # Advertencia
    
    if tipo:
        advertencia = f"El {tipo} debe ser valido y un número positivo, sin espacios."
    else:
        advertencia = "Debe ser valido y un número positivo, sin espacios."
    
    # Validacion
    
    if numero.isalpha() or not numero.isdigit() or int(numero) <= 0:
        print(advertencia) # Imprime advertencia
        return False
    else:
        return True

def is_string(texto: str, tipo = None):
    # Advertencia
    
    if tipo:
        advertencia = f"El {tipo} debe ser valido y no debe contener números ni símbolos ni espacios."
    else:
        advertencia = "Debe ser valido y no debe contener números ni símbolos ni espacios."
    
    # Validacion
    
    if texto.isdigit() or not texto.isalpha():
        print(advertencia) # Imprime advertencia
        return False
    else:
        return True

# no usamos correo XD
def is_email(email: str):
    # Validacion
    
    if "@" not in email or "." not in email or " " in email:
        print("El correo electrónico no debe tener espacios y debe contener '@' y '.'")
        return False
    else:
        return True

# estas funciones se pueden arreglar si se llama una sola funcion que pregunte y retorne un booleano

def valid_yes_no(respuesta: str):
    # Validacion
    
    if respuesta.lower() not in ["si", "sí", "no", "s", "n"]:
        print("La respuesta debe ser 'si' o 'no'.")
        return False
    else:
        return True

def yes_no(respuesta: str):
    if respuesta.lower() in ["no", "n"]:
        return False
    else:
        return True

# ===== UTILIDADES =====

def sp(i: int = None):
    if i:
        print("\n"*i)
    else:
        print("\n"*10)