import pygame
import sys
import os

# Configuración de Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (29, 50, 64)
GRAY = (180, 180, 180)
DARK_GRAY = (50, 50, 50)

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600

# Tamaño fijo para las imágenes
IMAGE_WIDTH, IMAGE_HEIGHT = 400, 400

# Escalas para las imágenes de los juegos en la periferia y en el centro
SCALE_CENTER = 0.7
SCALE_PERIPHERY = 0.5

# Velocidad de transición
SLIDE_SPEED = 20

# Función para cargar las imágenes y nombres de los juegos
def cargar_juegos():
    juegos = [
        {'nombre': 'Buscaminas', 'imagen': 'assets/images/buscaminas.png', 'archivo': 'buscaminas.py'},
        {'nombre': 'Tres en Raya', 'imagen': 'assets/images/3enraya.jpg', 'archivo': 'tresenraya.py'},
        {'nombre': 'Adivina el Numero', 'imagen': 'assets/images/adivinaelnumero.png', 'archivo': 'adivinador.py'}
    ]
    for juego in juegos:
        imagen = pygame.image.load(juego['imagen']).convert_alpha()
        imagen = pygame.transform.scale(imagen, (IMAGE_WIDTH, IMAGE_HEIGHT))
        juego['imagen'] = imagen
    return juegos

# Función para rotar las imágenes de los juegos
def rotar_imagenes(juegos, direccion):
    if direccion == 'derecha':
        return [juegos[-1]] + juegos[:-1]
    elif direccion == 'izquierda':
        return juegos[1:] + [juegos[0]]

# Función para mostrar la lista de juegos
def mostrar_lista_juegos(screen, juegos, desplazamiento_x, escalas):
    total_juegos = len(juegos)
    espacio_entre_juegos = 120
    centro_x = WIDTH // 2

    for i, juego in enumerate(juegos):
        escala = escalas[i]
        imagen = pygame.transform.scale(juego['imagen'], (int(IMAGE_WIDTH * escala), int(IMAGE_HEIGHT * escala)))
        x = centro_x + (i - total_juegos // 2) * (imagen.get_width() + espacio_entre_juegos) - imagen.get_width() // 2 + desplazamiento_x
        y = (HEIGHT - imagen.get_height()) // 2

        # Dibujar la sombra para efecto 3D
        shadow_rect = pygame.Rect(x + 5, y + 5, imagen.get_width(), imagen.get_height())
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=15)

        # Dibujar la imagen
        screen.blit(imagen, (x, y))

        # Dibujar el borde con efecto 3D
        border_rect = pygame.Rect(x, y, imagen.get_width(), imagen.get_height())
        pygame.draw.rect(screen, WHITE, border_rect, 3, border_radius=15)

        # Resaltar el juego seleccionado
        if i == total_juegos // 2:
            pygame.draw.rect(screen, WHITE, border_rect, 5, border_radius=15)

        # Mostrar el título del juego encima de la imagen}
        fuente = "assets/fonts/south_park.ttf"
        font = pygame.font.Font(fuente, 20)
        
        text = font.render(juego['nombre'], True, WHITE)
        text_rect = text.get_rect(center=(x + imagen.get_width() // 2, y - 30))
        screen.blit(text, text_rect)

# Función para mostrar el botón de jugar
def mostrar_boton_jugar(screen):
    fuente = "assets/fonts/south_park.ttf"
    font = pygame.font.Font(fuente, 30)
    text = font.render("Ejecutar", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    pygame.draw.rect(screen, GRAY, text_rect, border_radius=10)
    screen.blit(text, text_rect)

# Función principal
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lista de Juegos")

    juegos = cargar_juegos()
    total_juegos = len(juegos)
    desplazamiento_x = 0
    direccion = None
    escalas = [SCALE_PERIPHERY if i != total_juegos // 2 else SCALE_CENTER for i in range(total_juegos)]

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direccion = 'derecha'
                elif event.key == pygame.K_LEFT:
                    direccion = 'izquierda'
                elif event.key == pygame.K_RETURN:
                    juego_seleccionado = juegos[total_juegos // 2]
                    os.system(f"python {juego_seleccionado['archivo']}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    if WIDTH // 2 - 50 <= event.pos[0] <= WIDTH // 2 + 50 and HEIGHT - 75 <= event.pos[1] <= HEIGHT - 25:
                        juego_seleccionado = juegos[total_juegos // 2]
                        os.system(f"python {juego_seleccionado['archivo']}")

        if direccion:
            if direccion == 'izquierda':
                desplazamiento_x += SLIDE_SPEED
                for i in range(total_juegos):
                    if i == total_juegos // 2 - 1:
                        escalas[i] += (SCALE_CENTER - SCALE_PERIPHERY) / (WIDTH // SLIDE_SPEED)
                    elif i == total_juegos // 2:
                        escalas[i] -= (SCALE_CENTER - SCALE_PERIPHERY) / (WIDTH // SLIDE_SPEED)

                if desplazamiento_x >= WIDTH - 500:
                    desplazamiento_x = 0
                    juegos = rotar_imagenes(juegos, 'derecha')
                    escalas = [SCALE_PERIPHERY if i != total_juegos // 2 else SCALE_CENTER for i in range(total_juegos)]
                    direccion = None

            elif direccion == 'derecha':
                desplazamiento_x -= SLIDE_SPEED
                for i in range(total_juegos):
                    if i == total_juegos // 2 + 1:
                        escalas[i] += (SCALE_CENTER - SCALE_PERIPHERY) / (WIDTH // SLIDE_SPEED)
                    elif i == total_juegos // 2:
                        escalas[i] -= (SCALE_CENTER - SCALE_PERIPHERY) / (WIDTH // SLIDE_SPEED)

                if desplazamiento_x <= -WIDTH + 500:
                    desplazamiento_x = 0
                    juegos = rotar_imagenes(juegos, 'izquierda')
                    escalas = [SCALE_PERIPHERY if i != total_juegos // 2 else SCALE_CENTER for i in range(total_juegos)]
                    direccion = None

        mostrar_lista_juegos(screen, juegos, desplazamiento_x, escalas)
        mostrar_boton_jugar(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
