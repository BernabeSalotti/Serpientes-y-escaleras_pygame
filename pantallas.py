import pygame
import sys
import copy
import time
from funciones_preguntas import *
from preguntas import *
from tablero import *
from funciones_movimientos import *
from funciones_generales import *


pygame.init()
pygame.mixer.init()
ANCHO, ALTO = 900, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Serpientes y Escaleras")
#---------------COLORES----------------------------
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
GRIS = (200, 200, 200)
FONDO = (240, 178, 122)
CELESTITO = (23, 85, 105 )
AMARILLITO = (159, 163, 24)
NARANJITA = (210, 99, 0)
VIOLETA = (142, 0, 228 )
#---------------IMAGENES------------------------------
imagen_sepiente_principal = pygame.image.load("juego_pygame/imagenes/serpiente_principal.png")
imagen_serpiente_2 = pygame.image.load("juego_pygame/imagenes/serpiente_2.png")
imagen_serpiente_2 = pygame.transform.scale(imagen_serpiente_2,(200, 200))
imagen_escalera_1 = pygame.image.load("juego_pygame/imagenes/escalera_1.png")
imagen_escalera_2 = pygame.image.load("juego_pygame/imagenes/escalera_2.png")
imagen_trofeo_1 = pygame.image.load("juego_pygame/imagenes/trofeos_1.png")
imagen_trofeo_1 = pygame.transform.scale(imagen_trofeo_1,(250,250))
imagen_trofeo_2 = pygame.image.load("juego_pygame/imagenes/trofeos_2.png")
imagen_trofeo_2 = pygame.transform.scale(imagen_trofeo_2,(250,250))
imagen_serpiente_3 = pygame.image.load("juego_pygame/imagenes/serpiente_3.png")
imagen_escalera_3 = pygame.image.load("juego_pygame/imagenes/escalera_3.png")
#-----------FUENTES----------------------------
fuente = pygame.font.SysFont(None, 40)
fuente_2 = pygame.font.SysFont(None,20)
fuente_3 = pygame.font.SysFont(None,30)
fuente_titulo = pygame.font.SysFont('comic sans ms', 70)

#------------SONIDOS--------------------------
sonido_resp_correcta = pygame.mixer.Sound("juego_pygame/sonidos/resp_correcta.mp3")
sonido_resp_incorrecta = pygame.mixer.Sound("juego_pygame/sonidos/resp_incorrecta.mp3")
pygame.mixer.music.load("juego_pygame/sonidos/musica_menu.mp3")
sonido_victora_final = pygame.mixer.Sound("juego_pygame/sonidos/victoria_final.mp3")
sonido_derrota_final = pygame.mixer.Sound("juego_pygame/sonidos/derrota_final.mp3")

def mostrar_puntajes():
    """
    esta funcion se escarga de crear una pantalla en la cual se muestran los mejores 10 puntajes ordenados de forma descendente
    """
    clock = pygame.time.Clock()
    pantalla.fill(FONDO)

    pantalla.blit(imagen_trofeo_1, (650,60))
    pantalla.blit(imagen_trofeo_2, (0,580))

    puntajes = []
    try:
        with open("juego_pygame/score.csv", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) == 2:
                    nombre = partes[0]
                    try:
                        puntos = int(partes[1])
                        puntajes.append((nombre, puntos))
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass

    puntajes.sort(key=lambda x: x[1], reverse=True)

    titulo = fuente.render("TOP 10 PUNTAJES", True, NEGRO)
    pantalla.blit(titulo, (300, 50))

    y = 150
    for i, (nombre, puntos) in enumerate(puntajes[:10], start=1):
        texto = fuente.render(f"{i}. {nombre} - {puntos} puntos", True, NEGRO)
        pantalla.blit(texto, (250, y))
        y += 40

    texto_salir = fuente.render("Presioná una tecla o clic para volver al menú", True, ROJO)
    pantalla.blit(texto_salir, (150, 700))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False
        clock.tick(30)

def mostrar_pregunta(pregunta: dict, opciones_rects:list, mouse_pos):
    """
    esta funcion se encarga de mostrar en pantalla la pregunta y sus opciones
    ---
    Recibe:
    pregunta(dict): diccionario que contiene la pregunta y sus opciones
    opciones_rects(list): coordenadas de los botones de opciones
    mouse_pos: posicion de mouse
    """
    pygame.draw.rect(pantalla, NEGRO, (30, 430, 780, 50))
    pregunta_txt = fuente_3.render(pregunta["pregunta"], True, BLANCO)
    pantalla.blit(pregunta_txt, (50, 440))

    opciones = ['a', 'b', 'c']
    for i, opcion in enumerate(opciones):
        rect = opciones_rects[i]
        if rect.collidepoint(mouse_pos):
            color = CELESTITO 
        else:
            color = NEGRO
        pygame.draw.rect(pantalla, color, rect)
        texto = fuente_3.render(f"Opción {opcion.upper()}: {pregunta[f'respuesta_{opcion}']}", True, BLANCO)
        pantalla.blit(texto, (rect.x + 10, rect.y + 10))   

def menu_principal():
    """
    pantalla con un menu principal de 3 botones jugar, salir,mostrar puntajes
    """
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    boton_jugar = pygame.Rect(250, 300, 400, 60)
    boton_puntajes = pygame.Rect(250, 400, 400, 60)
    boton_salir = pygame.Rect(250, 500, 400, 60)
    posicion_titulo_serpientes = (80, 50)
    posicion_titulo_escaleras = (300, 120)
    while True:
        pantalla.fill(FONDO)
        mouse_pos = pygame.mouse.get_pos()

        pantalla.blit(imagen_sepiente_principal,(500, 330))
        pantalla.blit(imagen_serpiente_2,(10, 600))
        pantalla.blit(imagen_escalera_1, (650,60))
        pantalla.blit(imagen_escalera_2, (10,200))

        texto_titulo_arriba = fuente_titulo.render('SERPIENTES',True,(NARANJITA))
        texto_titulo_abajo = fuente_titulo.render('y ESCALERAS',True ,(CELESTITO))
        pantalla.blit(texto_titulo_arriba, posicion_titulo_serpientes)
        pantalla.blit(texto_titulo_abajo,posicion_titulo_escaleras)

        # Dibujar botones
        for rect, texto, color in [
            (boton_jugar, "JUGAR", VERDE),
            (boton_puntajes, "MOSTRAR PUNTAJES", AZUL),
            (boton_salir, "SALIR", ROJO)
        ]:
            if rect.collidepoint(mouse_pos):
                color_boton = color 
            else:
                color_boton = NEGRO
            pygame.draw.rect(pantalla, color_boton, rect)
            texto_render = fuente.render(texto, True, BLANCO)
            pantalla.blit(texto_render, (rect.x + 50, rect.y + 15))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(mouse_pos):
                    pedir_nombre()
                elif boton_puntajes.collidepoint(mouse_pos):
                    mostrar_puntajes()
                elif boton_salir.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        clock.tick(30)

def pedir_nombre():
    """
    esta funcion es una pantalla en la cual se solicita nombre al usuario con dos botones comenzar(llama a la funcion jugar) o cancelar(vuelve al menu principal)
    """
    clock = pygame.time.Clock()
    nombre_jugador = ""
    escribiendo = True

    boton_comenzar = pygame.Rect(250, 500, 180, 50)
    boton_cancelar = pygame.Rect(470, 500, 180, 50)
    input_rect = pygame.Rect(250, 350, 400, 50)

    while escribiendo:
        pantalla.fill(FONDO)
        texto_titulo = fuente.render("Ingresá tu nombre:", True, NEGRO)
        pantalla.blit(texto_titulo, (300, 250))
        pantalla.blit(imagen_serpiente_3,(10,550))
        pantalla.blit(imagen_escalera_3,(700,100))

        # Rectángulo del campo de texto
        pygame.draw.rect(pantalla, BLANCO, input_rect)
        pygame.draw.rect(pantalla, NEGRO, input_rect, 2)

        # Mostrar el texto del nombre
        texto_nombre = fuente.render(nombre_jugador, True, NEGRO)
        pantalla.blit(texto_nombre, (input_rect.x + 150, input_rect.y + 10))

        mouse_pos = pygame.mouse.get_pos()

        # Dibujar botones
        for rect, texto, color in [
            (boton_comenzar, "COMENZAR", VERDE),
            (boton_cancelar, "CANCELAR", ROJO)
        ]:
            if rect.collidepoint(mouse_pos):
                color_boton = color 
            else: 
                color_boton = NEGRO
            pygame.draw.rect(pantalla, color_boton, rect)
            texto_render = fuente.render(texto, True, BLANCO)
            pantalla.blit(texto_render, (rect.x + 10, rect.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre_jugador != "":
                    juego(nombre_jugador)
                
                elif evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                else:
                    if len(nombre_jugador) < 20:
                        nombre_jugador += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_comenzar.collidepoint(mouse_pos) and nombre_jugador != "":
                    juego(nombre_jugador)
                    
                elif boton_cancelar.collidepoint(mouse_pos):
                    return  # Volver al menú principal

        clock.tick(30)

def juego(nombre_jugador):
    """
    esta funcion es la pantalla del juego
    en esta funcion se muestra por pantalla el tablero con las posiciones
    las preguntas
    el cronometreo
    """
    clock = pygame.time.Clock()
    boton_terminar = pygame.Rect(700, 30, 150, 40)
    boton_volver = pygame.Rect(250, 740, 300, 40) 
    opciones_rects = [
        pygame.Rect(100, 530, 700, 50),
        pygame.Rect(100, 590, 700, 50),
        pygame.Rect(100, 650, 700, 50)
    ]
    posicion_actual = 15
    posicion_previa = posicion_actual
    posicion_momentanea = posicion_actual
    copia_preguntas = copy.deepcopy(preguntas)
    esperando_respuesta = True
    pregunta_actual = None
    pygame.mixer.music.stop()
    
    bandera_sonido = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        pantalla.fill(FONDO)
        
        #cronometro
        if esperando_respuesta and pregunta_actual:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - tiempo_inicio) // 1000  # en segundos
            tiempo_restante = max(0, 30 - tiempo_transcurrido)
            
            # Mostrar el cronómetro en pantalla
            if tiempo_restante < 10:
                color_crono = ROJO
            elif tiempo_restante < 20:
                color_crono = AMARILLO
            else:
                color_crono = BLANCO
            pygame.draw.rect(pantalla,NEGRO,(120,30,240,40))
            texto_cronometro = fuente_3.render(f"Tiempo restante: {tiempo_restante}s", True, color_crono)
            pantalla.blit(texto_cronometro, (130, 40))

            # Si el tiempo se agotó, avanzar como si fuera incorrecta
            if tiempo_restante == 0:
                seleccion = None
                correcta = False  # Se toma como respuesta incorrecta
                sonido_resp_incorrecta.play()
                posicion_previa = posicion_actual
                posicion_momentanea = movimientos_casilleros(tablero, posicion_actual, correcta)
                posicion_actual = movimientos_valores(valores_casillas, posicion_momentanea, posicion_previa)

                while valores_casillas[posicion_actual] != 0:
                    posicion_actual = movimientos_valores(valores_casillas, posicion_actual, posicion_previa)

                if posicion_actual == 30:
                    print("¡Ganaste!")
                    guardar_score(nombre_jugador, posicion_actual)
                elif posicion_actual == 0:
                    print("¡Perdiste!")
                    guardar_score(nombre_jugador, posicion_actual)
                elif len(copia_preguntas) == 0:
                    print('no quedan más preguntas abajo')
                    guardar_score(nombre_jugador, posicion_actual)

                pregunta_actual = None
                esperando_respuesta = True

        if posicion_actual == 30:
            if bandera_sonido == False:
                sonido_victora_final.play()
                bandera_sonido = True
            pygame.draw.rect(pantalla,NEGRO,(80, 490, 740, 50))
            text_sin_preg = fuente.render('WOW, usted completo el juego!!',True, BLANCO)
            pantalla.blit(text_sin_preg,(250, 500))
            if boton_volver.collidepoint(mouse_pos):
                color_boton = ROJO 
            else:
                color_boton = NEGRO
            pygame.draw.rect(pantalla, color_boton,boton_volver)
            texto_boton = fuente.render("VOLVER AL MENU", True, BLANCO)
            pantalla.blit(texto_boton, (boton_volver.x + 20, boton_volver.y + 10))

        elif posicion_actual == 0:
            if bandera_sonido == False:
                sonido_derrota_final.play()
                bandera_sonido = True
            pygame.draw.rect(pantalla,NEGRO,(80, 490, 740, 50))
            text_sin_preg = fuente.render('LASTIMA,perdiste el juego!!',True, BLANCO)
            pantalla.blit(text_sin_preg,(250, 500))
            if boton_volver.collidepoint(mouse_pos):
                color_boton = ROJO 
            else:
                color_boton = NEGRO
            pygame.draw.rect(pantalla, color_boton,boton_volver)
            texto_boton = fuente.render("VOLVER AL MENU", True, BLANCO)
            pantalla.blit(texto_boton, (boton_volver.x + 20, boton_volver.y + 10))
        
        #preguntas- seleccion aleatoria-muestra
        elif esperando_respuesta:
            if pregunta_actual is None and copia_preguntas:
                pregunta_actual = pregunta_aleatoria(copia_preguntas)
                tiempo_inicio = pygame.time.get_ticks()
                copia_preguntas.remove(pregunta_actual)
                
        
            if pregunta_actual:
                mostrar_pregunta(pregunta_actual, opciones_rects, mouse_pos)
            else:
                pygame.draw.rect(pantalla,NEGRO,(80, 490, 740, 50))
                text_sin_preg = fuente.render('No quedan mas preguntas arriba!!',True, BLANCO)
                pantalla.blit(text_sin_preg,(250, 500))
                if boton_volver.collidepoint(mouse_pos):
                    color_boton = ROJO 
                else:
                    color_boton = NEGRO
                pygame.draw.rect(pantalla, color_boton,boton_volver)
                texto_boton = fuente.render("VOLVER AL MENU", True, BLANCO)
                pantalla.blit(texto_boton, (boton_volver.x + 20, boton_volver.y + 10))
    
        # --- Dibujar tablero de 31 posiciones ---
        for pos in range(31):
            x = 50 + (pos % 10) * 80
            y = 100 + (pos // 10) * 80
            if pos == posicion_actual:
                color = VERDE
            elif pos == posicion_previa:
                color = ROJO
            elif pos == posicion_momentanea:
                color = AZUL
            elif valores_casillas[pos] != 0:
                color =  NARANJITA
            else:
                color = GRIS          
            pygame.draw.rect(pantalla, color, (x, y, 60, 60))
            if pos == posicion_actual:
                centro_x = x + 30
                centro_y = y + 30
                pygame.draw.circle(pantalla,VIOLETA,(centro_x, centro_y),15)          
            texto_pos = fuente.render(str(pos), True, NEGRO)
            pantalla.blit(texto_pos, (x + 15, y + 15))
       
               

        # cuadrados--de--instrucciones
        pygame.draw.rect(pantalla,NARANJITA,(135,340, 30, 30))
        texto_narnja = fuente_2.render('Casilleros especiales',True, NEGRO)
        pantalla.blit(texto_narnja,(170,350))

        pygame.draw.rect(pantalla,VERDE,(320,340, 30, 30))
        texto_verde = fuente_2.render('Posicion actual',True, NEGRO)
        pantalla.blit(texto_verde,(355,350))

        pygame.draw.rect(pantalla,ROJO,(480,340, 30, 30))
        texto_rojo = fuente_2.render('Posicion anterior',True, NEGRO)
        pantalla.blit(texto_rojo,(515,350))

        pygame.draw.rect(pantalla,AZUL,(135,380, 30, 30))
        texto_azul = fuente_2.render('Posicion en la que el jugador cae pero tien un valor especial que lo desplaza',True, NEGRO)
        pantalla.blit(texto_azul,(170,390))

        # --- Botón Terminar Juego ---
        if boton_terminar.collidepoint(mouse_pos):
            color_boton = ROJO 
        else:
            color_boton = NEGRO
        pygame.draw.rect(pantalla, color_boton, boton_terminar)
        texto_boton = fuente_2.render("TERMINAR JUEGO", True, BLANCO)
        pantalla.blit(texto_boton, (boton_terminar.x + 15, boton_terminar.y + 15))

        pygame.display.flip()

        #comienza a recibir acciones
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and esperando_respuesta and pregunta_actual:
                for idx, rect in enumerate(opciones_rects):
                    if rect.collidepoint(mouse_pos):
                        seleccion = ['a', 'b', 'c'][idx]
                        correcta = verificar_respuesta_correcta(seleccion, pregunta_actual)
                        if correcta:
                            sonido_resp_correcta.play()
                        else:
                            sonido_resp_incorrecta.play()
                        posicion_previa = posicion_actual
                        posicion_momentanea = movimientos_casilleros(tablero, posicion_actual, correcta)
                        posicion_actual = movimientos_valores(valores_casillas, posicion_momentanea, posicion_previa)
                        while valores_casillas[posicion_actual] != 0:
                            posicion_actual = movimientos_valores(valores_casillas, posicion_actual, posicion_previa)

                        if posicion_actual == 30:
                            print("¡Ganaste!")
                            guardar_score(nombre_jugador, posicion_actual)
                        elif posicion_actual == 0:
                            print("¡Perdiste!")
                            guardar_score(nombre_jugador, posicion_actual)                         
                        elif len(copia_preguntas) == 0:
                            print('no quedan mas preguntas abajo')
                            guardar_score(nombre_jugador, posicion_actual)
                        
                        pregunta_actual = None
                        esperando_respuesta = True
            
            if evento.type == pygame.MOUSEBUTTONDOWN  :
                if boton_terminar.collidepoint(mouse_pos):            
                    guardar_score(nombre_jugador, posicion_actual)
                    menu_principal()            
                if boton_volver.collidepoint(mouse_pos):
                    menu_principal()
                
        clock.tick(30)
