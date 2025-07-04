import random
def pregunta_aleatoria(lista_de_preguntas:list)->dict:
    """""
    funcion que se encarga de seleccionar aleatoriamente una pregunta
    ------------------
    recibe:
    lista_de_preguntas(lista): es una copia de la lista de preguntas original
    ---------------
    retorna:
    preguntra(dict): retorna un diccionario que contiene la pregunta y la respuesta correcta

    """""
    pregunta = random.choice(lista_de_preguntas)
    return pregunta

def verificar_respuesta_correcta(respuesta_ingresada: str, respuesta_de_la_pregunta:dict)->bool:
    """""
    funcion que se encarga de verificar si la respuesta ingresada por el usuario es correcta (True) o incorrecta (False)
    -------------
    recibe:
    respuesta_ingresada(str): respuesta ingresada por el usuario
    respuesta_de_la_preguntra(dict):diccionario que contiene la pregunta y la respuesta 
    -------------
    retorna:
    es_correcta(bool): variable de tipo booleano que retorna True si la respuesta es correcta o False si es incorrecta
    """""
    if respuesta_ingresada == respuesta_de_la_pregunta["respuesta_correcta"]:
        es_correcta = True
        print('¡¡Respuesta correcta!!')
    else:
        es_correcta = False
        print('¡¡Respuesta incorrecta!!')
        print('La respuesta correcta era:',respuesta_de_la_pregunta["respuesta_correcta"])
    
    return es_correcta

