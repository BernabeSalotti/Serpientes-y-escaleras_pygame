def movimientos_casilleros(tablero:list, posicion : int, es_correcta: bool)->int:
    """""
    si la respuesta es correcta avanza un lugar en el tablero
    si es incorrecta retrocede un lugar 
    ----------------
    funcion que recibe:
    tablero(lista):lista que contiene todos los casilleros del tablero
    posicion(int): recibe la posicion en la que se encuentra el jugador
    es_correcta(booleano): verdadero si la respuesta es correcta
    -------------------------- 
    retorna posicion_nueva(int): es un entero que indica la nueva posicion del jugador
    """""
    if es_correcta:
        posicion_nueva = posicion + 1 
    else:
        posicion_nueva = posicion - 1 
    
    return posicion_nueva

def movimientos_valores(valores_casillas: list,posicion_momentanea: int,posicion_previa: int)->int:
    """""
    esta funcion se encarga de mover al jugador dependiendo del valor de la caasilla en la que caiga 
    ------------------
    recibe:
    valores_casillas(lista): lista que contiene los valores de cada casilla del tablero
    posicion_momentanea(int): lugar en el que se encuentra el jugador antes de sumar o restar el valor de la casilla
    posicion_previa(int): posicion del jugador antes de responder
    -------------------
    retorna:
    posicion_final(int): esta funcion retorna la posicion final del jugar luego de haber respondido correcta o incorrectamente 
    """""
    if posicion_momentanea > posicion_previa:
        posicion_final = posicion_momentanea + valores_casillas[posicion_momentanea]
    else:
        posicion_final = posicion_momentanea - valores_casillas[posicion_momentanea]

    return posicion_final