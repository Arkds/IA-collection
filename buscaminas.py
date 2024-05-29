import pygame
import sys
import time
import random

class Buscaminas():
    def __init__(self, altura=8, anchura=8, minas=8):
        self.altura = altura
        self.anchura = anchura
        self.minas = set()
        self.tablero = []
        for i in range(self.altura):
            fila = []
            for j in range(self.anchura):
                fila.append(False)
            self.tablero.append(fila)
        while len(self.minas) != minas:
            i = random.randrange(altura)
            j = random.randrange(anchura)
            if not self.tablero[i][j]:
                self.minas.add((i, j))
                self.tablero[i][j] = True
        self.minas_encontradas = set()

    def es_mina(self, celda):
        i, j = celda
        return self.tablero[i][j]

    def minas_cercanas(self, celda):
        count = 0
        for i in range(celda[0] - 1, celda[0] + 2):
            for j in range(celda[1] - 1, celda[1] + 2):
                if (i, j) == celda:
                    continue
                if 0 <= i < self.altura and 0 <= j < self.anchura:
                    if self.tablero[i][j]:
                        count += 1
        return count

    def ganado(self):
        return self.minas_encontradas == self.minas

class Sentencia():
    def __init__(self, celdas, contador):
        self.celdas = set(celdas)
        self.contador = contador

    def __eq__(self, other):
        return self.celdas == other.celdas and self.contador == other.contador

    def conocidas_minas(self):
        if len(self.celdas) == self.contador and self.contador != 0:
            return self.celdas
        else:
            return set()

    def conocidas_seguras(self):
        if self.contador == 0:
            return self.celdas
        else:
            return set()

    def marcar_mina(self, celda):
        if celda in self.celdas:
            self.celdas.remove(celda)
            self.contador -= 1

    def marcar_segura(self, celda):
        if celda in self.celdas:
            self.celdas.remove(celda)

class IA_Buscaminas():
    def __init__(self, altura=8, anchura=8):
        self.altura = altura
        self.anchura = anchura
        self.movimientos_realizados = set()
        self.minas = set()
        self.seguras = set()
        self.conocimiento = []

    def marcar_mina(self, celda):
        self.minas.add(celda)
        for sentencia in self.conocimiento:
            sentencia.marcar_mina(celda)

    def marcar_segura(self, celda):
        self.seguras.add(celda)
        for sentencia in self.conocimiento:
            sentencia.marcar_segura(celda)

    def agregar_conocimiento(self, celda, contador):
        self.movimientos_realizados.add(celda)
        self.marcar_segura(celda)
        nuevas_celdas = set()
        for i in range(celda[0] - 1, celda[0] + 2):
            for j in range(celda[1] - 1, celda[1] + 2):
                if (i, j) == celda:
                    continue
                if (i, j) in self.seguras:
                    continue
                if (i, j) in self.minas:
                    contador -= 1
                    continue
                if 0 <= i < self.altura and 0 <= j < self.anchura:
                    nuevas_celdas.add((i, j))
        self.conocimiento.append(Sentencia(nuevas_celdas, contador))

        while True:
            conocimiento_cambiado = False
            seguras = set()
            minas = set()
            for sentencia in self.conocimiento:
                seguras = seguras.union(sentencia.conocidas_seguras())
                minas = minas.union(sentencia.conocidas_minas())
            if seguras:
                conocimiento_cambiado = True
                for segura in seguras:
                    self.marcar_segura(segura)
            if minas:
                conocimiento_cambiado = True
                for mina in minas:
                    self.marcar_mina(mina)
            vacia = Sentencia(set(), 0)
            self.conocimiento[:] = [x for x in self.conocimiento if x != vacia]
            for sentencia_1 in self.conocimiento:
                for sentencia_2 in self.conocimiento:
                    if sentencia_1.celdas == sentencia_2.celdas:
                        continue
                    if sentencia_1.celdas == set() and sentencia_1.contador > 0:
                        raise ValueError
                    if sentencia_1.celdas.issubset(sentencia_2.celdas):
                        nuevas_celdas = sentencia_2.celdas - sentencia_1.celdas
                        nuevo_contador = sentencia_2.contador - sentencia_1.contador
                        nueva_sentencia = Sentencia(nuevas_celdas, nuevo_contador)
                        if nueva_sentencia not in self.conocimiento:
                            conocimiento_cambiado = True
                            self.conocimiento.append(nueva_sentencia)
            if not conocimiento_cambiado:
                break

    def hacer_movimiento_seguro(self):
        seguras_disponibles = self.seguras - self.movimientos_realizados
        if seguras_disponibles:
            return random.choice(list(seguras_disponibles))
        return None

    def hacer_movimiento_aleatorio(self, MINAS):
        movimientos = {}
        num_minas_restantes = MINAS - len(self.minas)
        espacios_restantes = (self.altura * self.anchura) - (len(self.movimientos_realizados) + len(self.minas))
        if espacios_restantes == 0:
            return None
        probabilidad_basica = num_minas_restantes / espacios_restantes
        for i in range(0, self.altura):
            for j in range(0, self.anchura):
                if (i, j) not in self.movimientos_realizados and (i, j) not in self.minas:
                    movimientos[(i, j)] = probabilidad_basica
        if movimientos and not self.conocimiento:
            movimiento = random.choice(list(movimientos.keys()))
            return movimiento
        elif movimientos:
            for sentencia in self.conocimiento:
                num_celdas = len(sentencia.celdas)
                contador = sentencia.contador
                probabilidad_mina = contador / num_celdas
                for celda in sentencia.celdas:
                    if movimientos[celda] < probabilidad_mina:
                        movimientos[celda] = probabilidad_mina
            lista_movimientos = [[x, movimientos[x]] for x in movimientos]
            lista_movimientos.sort(key=lambda x: x[1])
            mejor_probabilidad = lista_movimientos[0][1]
            mejores_movimientos = [x for x in lista_movimientos if x[1] == mejor_probabilidad]
            movimiento = random.choice(mejores_movimientos)[0]
            return movimiento

def seleccionar_nivel(screen, fuente_grande, fuente_mediana):
    while True:
        screen.fill(OSCURO)
        titulo = fuente_grande.render("Selecciona un nivel", True, AMARILLO)
        rect_titulo = titulo.get_rect()
        rect_titulo.center = ((width / 2), 300)
        screen.blit(titulo, rect_titulo)

        botones_nivel = []
        nombres_niveles = ["Principiante", "Intermedio", "Experto"]
        for i, nombre in enumerate(nombres_niveles):
            boton_rect = pygame.Rect((width / 4), (2 / 4) * height + i * 70, width / 2, 50)
            texto_boton = fuente_mediana.render(nombre, True, VERDECL)
            rect_texto_boton = texto_boton.get_rect()
            rect_texto_boton.center = boton_rect.center
            pygame.draw.rect(screen, OSCURO, boton_rect)
            screen.blit(texto_boton, rect_texto_boton)
            botones_nivel.append(boton_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    raton = pygame.mouse.get_pos()
                    for i, boton in enumerate(botones_nivel):
                        if boton.collidepoint(raton):
                            if i == 0:
                                return 5, 5, 3
                            elif i == 1:
                                return 8, 8, 8
                            elif i == 2:
                                return 12, 12, 16   
                            
NEGRO = (0, 0, 0)
GRIS = (180, 180, 180)
BLANCO = (255, 255, 255)
AMARILLO = (242, 202, 80)
ROJO = (242, 56, 56)
VERDEOS = (55, 140, 76)
VERDECL = (	80, 191, 97)
OSCURO = (29, 50, 64)


size = width, height = 700, 900

def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    fuente = "assets/fonts/south_park.ttf"
    fuente_pequena = pygame.font.Font(fuente, 20)
    fuente_mediana = pygame.font.Font(fuente,35)
    fuente_grande = pygame.font.Font(fuente, 55)

    HEIGHT, WIDTH, MINAS = seleccionar_nivel(screen, fuente_grande, fuente_mediana)


    ESPACIO_TABLERO = 20
    ancho_tablero = ((3/ 3) * width) - (ESPACIO_TABLERO * 2)
    alto_tablero = height - (ESPACIO_TABLERO * 2)
    tamano_celda = int(min(ancho_tablero / WIDTH, alto_tablero / HEIGHT))
    origen_tablero = (ESPACIO_TABLERO, ESPACIO_TABLERO)
    bandera = pygame.image.load("assets/images/flag.png")
    bandera = pygame.transform.scale(bandera, (tamano_celda, tamano_celda))
    mina = pygame.image.load("assets/images/mine.png")
    mina = pygame.transform.scale(mina, (tamano_celda, tamano_celda))
    juego = Buscaminas(altura=HEIGHT, anchura=WIDTH, minas=MINAS)
    ia = IA_Buscaminas(altura=HEIGHT, anchura=WIDTH)
    descubiertas = set()
    banderas = set()
    perdido = False
    instrucciones = True

    # Fuera del bucle principal
    imagen_mostrada = False
    tiempo_ultima_aparicion = 0
    TIEMPO_PARPADEO = 1000  # Duración del parpadeo en milisegundos (1 segundo)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(OSCURO)

        if instrucciones:
            titulo = fuente_grande.render("Juega Buscaminas", True, BLANCO)
            rect_titulo = titulo.get_rect()
            rect_titulo.center = ((width / 2), 300)
            screen.blit(titulo, rect_titulo)
            reglas = [
                "Haz clic en una celda para revelarla.",
                "Haz clic derecho en una celda para marcarla como mina.",
                "Marca todas las minas para ganar!"
            ]
            for i, regla in enumerate(reglas):
                linea = fuente_pequena.render(regla, True, AMARILLO)
                rect_linea = linea.get_rect()
                rect_linea.center = ((width / 2), 400 + 30 * i)
                screen.blit(linea, rect_linea)
            boton_rect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
            texto_boton = fuente_mediana.render("Jugar", True, NEGRO)
            rect_texto_boton = texto_boton.get_rect()
            rect_texto_boton.center = boton_rect.center
            pygame.draw.rect(screen, BLANCO, boton_rect)
            screen.blit(texto_boton, rect_texto_boton)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                raton = pygame.mouse.get_pos()
                if boton_rect.collidepoint(raton):
                    instrucciones = False
                    time.sleep(0.3)
            pygame.display.flip()
            continue

        celdas = []
        for i in range(HEIGHT):
            fila = []
            for j in range(WIDTH):
                rect = pygame.Rect(
                    origen_tablero[0] + j * tamano_celda,
                    origen_tablero[1] + i * tamano_celda,
                    tamano_celda, tamano_celda
                )
                pygame.draw.rect(screen, VERDEOS, rect)
                pygame.draw.rect(screen, VERDECL, rect, 2)
                if juego.es_mina((i, j)) and perdido:
                    screen.blit(mina, rect)
                elif (i, j) in banderas:
                    screen.blit(bandera, rect)
                elif (i, j) in descubiertas:
                    vecinos = fuente_mediana.render(
                        str(juego.minas_cercanas((i, j))),
                        True, NEGRO
                    )
                    rect_vecinos = vecinos.get_rect()
                    rect_vecinos.center = rect.center
                    screen.blit(vecinos, rect_vecinos)
                fila.append(rect)
            celdas.append(fila)
        
        boton_ia = pygame.Rect(
            origen_tablero[0], origen_tablero[1] + HEIGHT * tamano_celda + 20,
            (width / 3) - ESPACIO_TABLERO * 1, 50
        )
        texto_boton = fuente_mediana.render("Mov. IA", True, NEGRO)
        rect_texto_boton = texto_boton.get_rect()
        rect_texto_boton.center = boton_ia.center
        pygame.draw.rect(screen, BLANCO, boton_ia)
        screen.blit(texto_boton, rect_texto_boton)
        boton_reset = pygame.Rect(
            boton_ia.right + ESPACIO_TABLERO, origen_tablero[1] + HEIGHT * tamano_celda + 20,
            (width / 3) - ESPACIO_TABLERO * 2, 50
        )
        texto_boton = fuente_mediana.render("Reiniciar", True, NEGRO)
        rect_texto_boton = texto_boton.get_rect()
        rect_texto_boton.center = boton_reset.center
        pygame.draw.rect(screen, AMARILLO, boton_reset)
        screen.blit(texto_boton, rect_texto_boton)

        boton_salir = pygame.Rect(
            boton_reset.right + ESPACIO_TABLERO, origen_tablero[1] + HEIGHT * tamano_celda + 20,
            (width / 3) - ESPACIO_TABLERO * 1, 50
        )

        texto_boton = fuente_mediana.render("Salir", True, NEGRO)
        rect_texto_boton = texto_boton.get_rect()
        rect_texto_boton.center = boton_salir.center
        pygame.draw.rect(screen, ROJO, boton_salir)
        screen.blit(texto_boton, rect_texto_boton)


        
        texto = "PERDISTE :(" if perdido else "GANASTE :)" if juego.minas == banderas else ""
        texto = fuente_grande.render(texto, True, AMARILLO)
        
        rect_texto = texto.get_rect()
        rect_texto.center = ((4/7) * width - 50, (3 / 3) * height - 80 )
        screen.blit(texto, rect_texto)
        movimiento = None
        izquierdo, _, derecho = pygame.mouse.get_pressed()
        if derecho == 1 and not perdido:
            raton = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if celdas[i][j].collidepoint(raton) and (i, j) not in descubiertas:
                        if (i, j) in banderas:
                            banderas.remove((i, j))
                        else:
                            banderas.add((i, j))
                        time.sleep(0.2)
        elif izquierdo == 1:
            raton = pygame.mouse.get_pos()
            if boton_ia.collidepoint(raton) and not perdido:
                movimiento = ia.hacer_movimiento_seguro()
                if movimiento is None:
                    movimiento = ia.hacer_movimiento_aleatorio(MINAS)
                    if movimiento is None:
                        banderas = ia.minas.copy()
                        print("No quedan movimientos posibles.")
                    else:
                        print("No se conocen movimientos seguros, IA realiza movimiento aleatorio.")
                else:
                    print("IA realiza movimiento seguro.")
                time.sleep(0.2)
            elif boton_reset.collidepoint(raton):
                juego = Buscaminas(altura=HEIGHT, anchura=WIDTH, minas=MINAS)
                ia = IA_Buscaminas(altura=HEIGHT, anchura=WIDTH)
                descubiertas = set()
                banderas = set()
                perdido = False
                continue
            elif boton_salir.collidepoint(raton):
                main()
            elif not perdido:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (celdas[i][j].collidepoint(raton)
                                and (i, j) not in banderas
                                and (i, j) not in descubiertas):
                            movimiento = (i, j)
        if movimiento:
            if juego.es_mina(movimiento):
                perdido = True
            else:
                vecinos = juego.minas_cercanas(movimiento)
                descubiertas.add(movimiento)
                ia.agregar_conocimiento(movimiento, vecinos)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()