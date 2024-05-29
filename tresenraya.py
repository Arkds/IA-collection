import pygame as pg
import sys

# Configuración de constantes
ANCHO = 700
ALTO = 900
LINEA_ANCHO = 15
FILAS_TABLERO = 3
COLUMNAS_TABLERO = 3
TAMANO_CASILLA = ANCHO // COLUMNAS_TABLERO
RADIO_CIRCULO = TAMANO_CASILLA // 3
OFFSET_CRUZ = 50
ANCHO_CRUZ = 25
FPS = 30

# Colores
BLANCO = (255, 255, 255)
AMARILLO = (242, 202, 80)
NEGRO = (29, 50, 64)
ROJO = (242, 56, 56)
AZUL = (55, 140, 76)
VERDECL = (	80, 191, 97)
GRIS = (180, 180, 180)

# Inicialización de Pygame
pg.init()
pantalla = pg.display.set_mode((ANCHO, ALTO))
pg.display.set_caption("Tres en Raya")
fuente = "assets/fonts/south_park.ttf"

# Fuentes
fuente_grande = pg.font.Font(fuente, 36)
fuente_pequena = pg.font.Font(fuente, 24)

def mostrar_texto(texto, x, y, fuente):
    texto_superficie = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_superficie, (x, y))

def dibujar_seleccion_dificultad():
    pantalla.fill(NEGRO)
    mostrar_texto("Selecciona la dificultad", ANCHO / 2 - 250, 100, fuente_grande)
    pg.draw.rect(pantalla, VERDECL, (ANCHO / 2 - 95, 200, 190, 50))
    mostrar_texto("Principiante", ANCHO / 2 - 85, 215, fuente_pequena)
    pg.draw.rect(pantalla, GRIS, (ANCHO / 2 - 95, 300, 180, 50))
    mostrar_texto("Intermedio", ANCHO / 2 - 85, 315, fuente_pequena)
    pg.draw.rect(pantalla, ROJO, (ANCHO / 2 - 95, 400, 170, 50))
    mostrar_texto("Experto", ANCHO / 2 - 60, 415, fuente_pequena)

def dibujar_menu():
    pantalla.fill(NEGRO)
    mostrar_texto("TRES EN RAYA", ANCHO / 2 - 120, 50, fuente_grande)
    mostrar_texto("Selecciona tu símbolo:", ANCHO / 2 - 140, 150, fuente_pequena)
    pg.draw.rect(pantalla, ROJO, (ANCHO / 2 - 100, 200, 100, 50))
    pg.draw.rect(pantalla, AZUL, (ANCHO / 2, 200, 100, 50))
    mostrar_texto("X", ANCHO / 2 - 65, 215, fuente_grande)
    mostrar_texto("O", ANCHO / 2 + 35, 215, fuente_grande)
    
    # Zona de instrucciones
    instrucciones = [
        "Instrucciones:",
        "",
        "1. Selecciona tu símbolo.",
        "2. Haz clic en una casilla para jugar.",
        "3. Haz una línea de 3 para ganar.",
        "4. El juego alterna entre X y O."
    ]
    for i, instruccion in enumerate(instrucciones):
        linea = fuente_pequena.render(instruccion, True, AMARILLO)
        rect_linea = linea.get_rect()
        rect_linea.center = (ANCHO / 2, 300 + 30 * i)
        pantalla.blit(linea, rect_linea)

def dibujar_tablero():
    pantalla.fill(NEGRO)
    dibujar_lineas()
    dibujar_figuras()
    dibujar_botones_juego()

def dibujar_lineas():
    for i in range(1, FILAS_TABLERO):
        pg.draw.line(pantalla, BLANCO, (0, i * TAMANO_CASILLA), (ANCHO, i * TAMANO_CASILLA), LINEA_ANCHO)
        pg.draw.line(pantalla, BLANCO, (i * TAMANO_CASILLA, 0), (i * TAMANO_CASILLA, ALTO), LINEA_ANCHO)

def dibujar_figuras():
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            centro_x = col * TAMANO_CASILLA + TAMANO_CASILLA // 2
            centro_y = fila * TAMANO_CASILLA + TAMANO_CASILLA // 2
            if tablero[fila][col] == 1:
                pg.draw.circle(pantalla, ROJO, (centro_x, centro_y), RADIO_CIRCULO, LINEA_ANCHO)
            elif tablero[fila][col] == 2:
                # Líneas de la cruz
                inicio_l1 = (centro_x - RADIO_CIRCULO, centro_y - RADIO_CIRCULO)
                fin_l1 = (centro_x + RADIO_CIRCULO, centro_y + RADIO_CIRCULO)
                inicio_l2 = (centro_x - RADIO_CIRCULO, centro_y + RADIO_CIRCULO)
                fin_l2 = (centro_x + RADIO_CIRCULO, centro_y - RADIO_CIRCULO)
                pg.draw.line(pantalla, AZUL, inicio_l1, fin_l1, LINEA_ANCHO)
                pg.draw.line(pantalla, AZUL, inicio_l2, fin_l2, LINEA_ANCHO)

def dibujar_botones_juego():
    pg.draw.rect(pantalla, NEGRO, (0, ALTO/2 + 220, ANCHO, ALTO-(ALTO/2+220)))
    pg.draw.rect(pantalla, ROJO, (200, ALTO - 100, ANCHO-400, 50))
    mostrar_texto("Mov. IA", ANCHO / 2 - 50, ALTO - 85, fuente_pequena)
    pg.draw.rect(pantalla, ROJO, (200, ALTO - 160, ANCHO-400, 50))
    mostrar_texto("Reiniciar", ANCHO / 2 - 60, ALTO - 145, fuente_pequena)
    pg.draw.rect(pantalla, ROJO, (200, ALTO - 220, ANCHO-400, 50))
    mostrar_texto("Salir", ANCHO / 2 - 50, ALTO - 205, fuente_pequena)

def inicializar_tablero():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def esta_tablero_lleno(tablero):
    return all(tablero[fila][col] != 0 for fila in range(FILAS_TABLERO) for col in range(COLUMNAS_TABLERO))

def hay_ganador(tablero, jugador):
    return any(all(tablero[fila][col] == jugador for col in range(COLUMNAS_TABLERO)) for fila in range(FILAS_TABLERO)) or \
           any(all(tablero[fila][col] == jugador for fila in range(FILAS_TABLERO)) for col in range(COLUMNAS_TABLERO)) or \
           all(tablero[i][i] == jugador for i in range(FILAS_TABLERO)) or \
           all(tablero[i][FILAS_TABLERO - i - 1] == jugador for i in range(FILAS_TABLERO))

def test_terminal(tablero):
    return hay_ganador(tablero, 1) or hay_ganador(tablero, 2) or esta_tablero_lleno(tablero)

def acciones(tablero):
    return [(fila, col) for fila in range(FILAS_TABLERO) for col in range(COLUMNAS_TABLERO) if tablero[fila][col] == 0]

def resultado(tablero, accion, jugador):
    fila, col = accion
    nuevo_tablero = [fila[:] for fila in tablero]
    nuevo_tablero[fila][col] = jugador
    return nuevo_tablero

def utilidad(tablero):
    if hay_ganador(tablero, simbolo_maquina):
        return -1
    elif hay_ganador(tablero, simbolo_jugador):
        return 1
    elif esta_tablero_lleno(tablero):
        return 0
    else:
        return None

def mejor_movimiento(tablero):
    mejor_movimiento = None
    mejor_eval = float('inf')
    for accion in acciones(tablero):
        eval = minimax(resultado(tablero, accion, simbolo_maquina), True, profundidad_dificultad)
        if eval < mejor_eval:
            mejor_eval = eval
            mejor_movimiento = accion
    return mejor_movimiento

def minimax(tablero, maximizando_jugador, profundidad):
    if profundidad == 0:
        return 0
    if test_terminal(tablero):
        return utilidad(tablero)

    if maximizando_jugador:
        max_eval = float('-inf')
        for accion in acciones(tablero):
            eval = minimax(resultado(tablero, accion, simbolo_jugador), False, profundidad - 1)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for accion in acciones(tablero):
            eval = minimax(resultado(tablero, accion, simbolo_maquina), True, profundidad - 1)
            min_eval = min(min_eval, eval)
        return min_eval

def jugador(tablero):
    count_X = sum(fila.count(simbolo_jugador) for fila in tablero)
    count_O = sum(fila.count(simbolo_maquina) for fila in tablero)
    return simbolo_jugador if count_X <= count_O else simbolo_maquina

def mostrar_resultado(resultado_texto):
    pantalla.fill(NEGRO)
    if resultado_texto == "Perdiste":
        victoria_imagen = pg.image.load("assets/images/jajaja.png")
    elif resultado_texto == "Ganaste":
        victoria_imagen = pg.image.load("assets/images/ganaste.jpg")
    else:
        victoria_imagen = pg.image.load("assets/images/empate.jpg")

    victoria_imagen = pg.transform.scale(victoria_imagen, (ANCHO-80, ALTO-120) if resultado_texto != "Empate" else (ANCHO, ALTO))
    pantalla.blit(victoria_imagen, (50, 100) if resultado_texto != "Empate" else (0, 0))
    mostrar_texto(resultado_texto, 50, 50, fuente_grande)
    pg.draw.rect(pantalla, ROJO, (ANCHO/2 - 50, ALTO/2-25, 100, 50))
    mostrar_texto("Menu", ANCHO/2 - 30, ALTO/2- 12, fuente_pequena)

# Estado inicial del juego
estado_juego = "SELECCION_DIFICULTAD"
simbolo_jugador = None
simbolo_maquina = None
tablero = None
profundidad_dificultad = None

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            ejecutando = False
            pg.quit()
            sys.exit()

        if estado_juego == "SELECCION_DIFICULTAD":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if ANCHO / 2 - 75 <= mouseX <= ANCHO / 2 + 75:
                    if 200 <= mouseY <= 250:
                        profundidad_dificultad = 2
                        estado_juego = "MENU"
                    elif 300 <= mouseY <= 350:
                        profundidad_dificultad = 6
                        estado_juego = "MENU"
                    elif 400 <= mouseY <= 450:
                        profundidad_dificultad = 8
                        estado_juego = "MENU"

        elif estado_juego == "MENU":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if ANCHO/2-100 <= mouseX <= ANCHO/2 and 200 <= mouseY <= 250:
                    simbolo_jugador = 2
                    simbolo_maquina = 1
                    tablero = inicializar_tablero()
                    estado_juego = "JUGANDO"
                elif ANCHO/2 <= mouseX <= ANCHO/2+100 and 200 <= mouseY <= 250:
                    simbolo_jugador = 1
                    simbolo_maquina = 2
                    tablero = inicializar_tablero()
                    estado_juego = "JUGANDO"

        elif estado_juego == "JUGANDO":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if ALTO - 100 <= mouseY <= ALTO - 50:
                    if not test_terminal(tablero) and simbolo_jugador == jugador(tablero):
                        aux = profundidad_dificultad
                        profundidad_dificultad = 8
                        fila, columna = mejor_movimiento(tablero)
                        profundidad_dificultad = aux
                        tablero = resultado(tablero, (fila, columna), simbolo_jugador)
                        if test_terminal(tablero):
                                if utilidad(tablero) == 1:
                                    resultado_texto = "Ganaste"
                                elif utilidad(tablero) == -1:
                                    resultado_texto = "Perdiste"
                                else:
                                    resultado_texto = "Empate"
                                estado_juego = "TERMINADO"
                elif ALTO - 160 <= mouseY <= ALTO - 110:
                        tablero = inicializar_tablero()
                elif ALTO - 220 <= mouseY <= ALTO - 170:
                        estado_juego = "SELECCION_DIFICULTAD"
                else:
                    if simbolo_jugador == jugador(tablero):
                        fila = mouseY // TAMANO_CASILLA
                        columna = mouseX // TAMANO_CASILLA
                        if not test_terminal(tablero) and tablero[fila][columna] == 0:
                            tablero = resultado(tablero, (fila, columna), simbolo_jugador)
                            if test_terminal(tablero):
                                if utilidad(tablero) == 1:
                                    resultado_texto = "Ganaste"
                                elif utilidad(tablero) == -1:
                                    resultado_texto = "Perdiste"
                                else:
                                    resultado_texto = "Empate"
                                estado_juego = "TERMINADO"
                    else:
                        if not test_terminal(tablero):
                            fila, columna = mejor_movimiento(tablero)
                            tablero = resultado(tablero, (fila, columna), simbolo_maquina)
                            if test_terminal(tablero):
                                if utilidad(tablero) == 1:
                                    resultado_texto = "Ganaste"
                                elif utilidad(tablero) == -1:
                                    resultado_texto = "Perdiste"
                                else:
                                    resultado_texto = "Empate"
                                estado_juego = "TERMINADO"

        elif estado_juego == "TERMINADO":
            if evento.type == pg.MOUSEBUTTONDOWN:
                mouseX, mouseY = pg.mouse.get_pos()
                if ANCHO/2 - 50 <= mouseX <= ANCHO/2 + 50 and ALTO/2-25 <= mouseY <= ALTO/2+25:
                    estado_juego = "SELECCION_DIFICULTAD"

    if estado_juego == "SELECCION_DIFICULTAD":
        dibujar_seleccion_dificultad()
    elif estado_juego == "MENU":
        dibujar_menu()
    elif estado_juego == "JUGANDO":
        dibujar_tablero()
    elif estado_juego == "TERMINADO":
        mostrar_resultado(resultado_texto)

    pg.display.flip()
    pg.time.Clock().tick(FPS)
