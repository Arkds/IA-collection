import pygame
import random
import sys
import math

pygame.init()

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
VERDE = (0, 255, 0)
CELESTE = (0, 255, 255)
GRIS = (200, 200, 200)
AZUL_CLARO = (173, 216, 230)

ANCHO = 800
ALTO = 600

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Adivina el número")

fuente = pygame.font.SysFont('Comic Sans MS', 30)
fuente_pequena = pygame.font.SysFont('Comic Sans MS', 20)

def mostrar_texto(texto, x, y, color=BLANCO, tamano=30):
    fuente_usar = pygame.font.SysFont('Comic Sans MS', tamano)
    texto_renderizado = fuente_usar.render(texto, True, color)
    ventana.blit(texto_renderizado, (x, y))

def dibujar_luz_roja(x, y):
    pygame.draw.circle(ventana, ROJO, (x, y), 20)

def dibujar_luz_naranja(x, y):
    pygame.draw.circle(ventana, NARANJA, (x, y), 20)

def dibujar_luz_verde(x, y):
    pygame.draw.circle(ventana, VERDE, (x, y), 20)

def dibujar_luz_celeste(x, y):
    pygame.draw.circle(ventana, CELESTE, (x, y), 20)

def es_primo(numero):
    if numero < 2:
        return False
    for i in range(2, int(math.sqrt(numero)) + 1):
        if numero % i == 0:
            return False
    return True

def juego():
    numero_secreto = random.randint(1, 100)
    intentos = 0
    numero_ingresado = ""
    mensaje = ""
    tiempo_mensaje = 240
    mostrar_numero_secreto = False
    contador_intentos = 0
    numeros_intentados = []
    ultimo_numero = None
    pistas = []
    min_num = 1
    max_num = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if numero_ingresado:
                        intento = int(numero_ingresado)
                        contador_intentos += 1
                        if intento == numero_secreto:
                            mensaje = "¡Correcto! Lo adivinaste en {} intentos.".format(intentos)
                            mostrar_numero_secreto = True
                        elif intento < numero_secreto:
                            mensaje = "{} es muy bajo".format(intento)
                            pistas.append(("bajo", intento))
                            min_num = max(min_num, intento + 1)
                        else:
                            mensaje = "{} es muy alto".format(intento)
                            pistas.append(("alto", intento))
                            max_num = min(max_num, intento - 1)
                        tiempo_mensaje = 240
                        intentos += 1
                        ultimo_numero = intento
                        numeros_intentados.append(intento)
                        numero_ingresado = ""
                elif event.key == pygame.K_r:
                    numero_secreto = random.randint(1, 100)
                    intentos = 0
                    mensaje = ""
                    tiempo_mensaje = 0
                    mostrar_numero_secreto = False
                    contador_intentos = 0
                    numeros_intentados = []
                    ultimo_numero = None
                    pistas = []
                    min_num = 1
                    max_num = 100
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    numero_ingresado += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 500 <= event.pos[0] <= 570 and 300 <= event.pos[1] <= 330:
                    ia_numero = ia_adivinar_numero(numeros_intentados, pistas, min_num, max_num)
                    contador_intentos += 1
                    ultimo_numero = ia_numero
                    if ia_numero == numero_secreto:
                        mensaje = "¡La IA adivinó el número en {} intentos!".format(contador_intentos)
                        mostrar_numero_secreto = True
                    elif ia_numero < numero_secreto:
                        mensaje = "La IA probó: {} es muy bajo".format(ia_numero)
                        pistas.append(("bajo", ia_numero))
                        min_num = max(min_num, ia_numero + 1)
                    else:
                        mensaje = "La IA probó: {} es muy alto".format(ia_numero)
                        pistas.append(("alto", ia_numero))
                        max_num = min(max_num, ia_numero - 1)
                    tiempo_mensaje = 240
                    numeros_intentados.append(ia_numero)

        ventana.fill(AZUL_CLARO)

        mostrar_texto("Adivina el número entre 1 y 100:", 50, 50, tamano=40)
        mostrar_texto("Intentos realizados: {}".format(contador_intentos), 50, 100, tamano=30)
        mostrar_texto(numero_ingresado, 50, 250, tamano=30)
        if tiempo_mensaje > 0:
            mostrar_texto(mensaje, 50, 200, tamano=30)
            tiempo_mensaje -= 1

        if ultimo_numero is not None:
            if numero_secreto % ultimo_numero == 0:
                dibujar_luz_naranja(500, 200)
            if ultimo_numero % numero_secreto == 0:
                dibujar_luz_roja(500, 100)
            if ultimo_numero % 2 == 0:
                dibujar_luz_verde(500, 150)
            if es_primo(ultimo_numero):
                dibujar_luz_celeste(500, 250)

        if mostrar_numero_secreto or contador_intentos >= 10:
            mostrar_texto("El número secreto era: {}".format(numero_secreto), 50, 300, tamano=30)

        pygame.draw.rect(ventana, GRIS, (500, 300, 70, 30))
        mostrar_texto("IA", 515, 305, NEGRO, tamano=30)

        mostrar_texto("Pistas:", 50, 350, tamano=30)
        mostrar_texto("Naranja: Múltiplo de tu número", 50, 380, tamano=20)
        mostrar_texto("Rojo: Divisor de tu número", 50, 410, tamano=20)
        mostrar_texto("Verde: Número par", 50, 440, tamano=20)
        mostrar_texto("Celeste: Número primo", 50, 470, tamano=20)

        if numeros_intentados:
            mostrar_texto("Último número probado: {}".format(numeros_intentados[-1]), 50, 150, tamano=30)

        pygame.display.update()

        if tiempo_mensaje == 0:
            mensaje = ""

def ia_adivinar_numero(numeros_intentados, pistas, min_num, max_num):
    posibles_numeros = set(range(1, 101))

    for pista in pistas:
        if pista[0] == "bajo":
            min_num = max(min_num, pista[1] + 1)
        elif pista[0] == "alto":
            max_num = min(max_num, pista[1] - 1)
    
    posibles_numeros = {n for n in posibles_numeros if min_num <= n <= max_num}
    
    posibles_numeros -= set(numeros_intentados)
    
    if posibles_numeros:
        return random.choice(list(posibles_numeros))
    else:
        return random.randint(min_num, max_num)

juego()
