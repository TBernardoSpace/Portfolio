import pygame

# Ancho y alto de la pantalla
WIDTH = 800
HEIGHT = 600

# Inicializar pygame
pygame.init()

# Establecer la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Establecer el título de la ventana
pygame.display.set_caption("Doodle Jump")

# Establecer el reloj del juego
clock = pygame.time.Clock()

# Variables del juego
player_x = WIDTH / 2
player_y = HEIGHT / 2
player_radius = 25
player_color = (255, 255, 255)
player_speed = 5

gravity = 0.5

platform_list = []

# Bucle del juego
running = True
while running:
    # Manejar eventos de entrada
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener el estado de las teclas
    keys = pygame.key.get_pressed()

    # Mover el personaje
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Aplicar la gravedad
    player_y += gravity

    # Dibujar el juego
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, player_color, (int(player_x), int(player_y)), player_radius)

    # Actualizar la pantalla
    pygame.display.flip()

    # Limitar la tasa de actualización del juego
    clock.tick(60)

# Cerrar pygame
pygame.quit()

