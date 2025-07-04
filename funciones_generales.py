
def verificar_los_datos (dato, respuestas_correctas: list)-> bool:
    """""
    funcion que se encarga de verificar si un dato es correcto
    -------
    recibe:
    dato: es el dato a verificar
    respuestas_correctas(list): lista de posibles respuestas validas
    ----------
    retorna:
    existe(bool): si el dato se encuentra en la lista de respuestas correctas retoena True
    """""
    existe = False
    for respuesta in respuestas_correctas:
        if respuesta == dato:
            existe = True
    
    return existe 

def guardar_score(nombre: str, posicion: int):
    """
    funcion que se encarga de guardar en un archivo dos datos
    ----
    Recibe:
    nombre(str):cadena de caracteres
    posicion(int):valor numerico 
    """
    with open("juego_pygame/score.csv", "a") as archivo:
        archivo.write(f"{nombre},{posicion}\n")
        print("Puntaje guardado correctamente.")

