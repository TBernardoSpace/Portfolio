import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
window_width = 800
window_height = 600

# Creación de la ventana del juego
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Grappling Hook Game')

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Fuentes de texto
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

# Imágenes
player_image = pygame.Surface((20, 20))
player_image.fill(white)

# Posición inicial del jugador
player_x = window_width // 2
player_y = window_height - 50

# Velocidad del jugador
player_speed = 5

# Altura máxima a la que puede subir el jugador
max_height = 100

# Velocidad de caída de los bloques
block_speed = 5

# Lista de bloques
blocks = []

# Contador de tiempo
time_counter = 0

# Contador de puntuación
score = 0

# Ciclo principal del juego
game_running = True
while game_running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Acción del grapple hook
            pass

    # Movimiento del jugador con las teclas de flecha
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Actualización de la posición del jugador
    player_rect = player_image.get_rect()
    player_rect.x = player_x
    player_rect.y = player_y

    # Dibujado del escenario
    window.fill(black)

    # Dibujado de los edificios
    pygame.draw.rect(window, white, (0, 0, 100, window_height))
    pygame.draw.rect(window, white, (window_width - 100, 0, 100, window_height))

    # Dibujado de la ciudad y el cielo
    # TODO: Implementar el dibujado de la ciudad y el cielo

    # Dibujado del jugador
    window.blit(player_image, (player_x, player_y))

    # Dibujado de los bloques y detección de colisiones
    for block in blocks:
        # Actualización de la posición del bloque
        block_rect = block.get_rect()
        block_rect.y += block_speed

        # Detección de colisiones
        if block_rect.colliderect(player_rect):
            # Si colisiona con el jugador, se reinicia el juego
            score_text = big_font.render(f"Score: {score}", True, white)
            score_rect = score_text.get_rect()
            score_rect.center = (window_width // 2, window_height // 2 - 50)

            retry_text = font.render("Press R to retry", True, white)
            retry_rect = retry_text.get_rect()
            retry_rect.center = (window_width // 2, window_height // 2 + 50)

            window.blit(score_text, score_rect)
            window.blit(retry_text, retry_rect)

            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            waiting = False
                            player_x = window_width // 2
                            player_y = window_height - 50
                            blocks = []
                            score = 0
                        elif event.key == pygame.K_ESCAPE:
                            game_running = False
def main():
    # Initialize Pygame
    pygame.init()

    # Create window
    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Grappling Hook Game")

    # Create player and blocks
    player_x = window_width // 2
    player_y = window_height - 50
    player = Player(player_x, player_y)
    blocks = []

    # Create clock
    clock = pygame.time.Clock()

    # Game loop
    game_running = True
    while game_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    player_x = window_width // 2
                    player_y = window_height - 50
                    blocks = []
                    score = 0
                elif event.key == pygame.K_ESCAPE:
                    game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not player.grappling_hook_on:
                    player.shoot_grappling_hook(pygame.mouse.get_pos())
                else:
                    player.release_grappling_hook()

        # Update player and grappling hook positions
        player.update()
        if player.grappling_hook_on:
            player.grappling_hook.update()

        # Create new block randomly
        if len(blocks) < 5:
            new_block = Block()
            blocks.append(new_block)

        # Update block positions
        for block in blocks:
            block.update()

        # Remove blocks that have gone off screen
        blocks = [block for block in blocks if block.rect.top < window_height]

        # Check for collisions
        for block in blocks:
            if block.rect.colliderect(player.rect):
                game_running = False

        # Draw background
        background_surface = pygame.Surface(window.get_size())
        background_surface.fill((135, 206, 235))

        building_width = window_width // 2
        building_height = window_height - 100
        building_color = (100, 100, 100)
        left_building_rect = pygame.Rect(0, 0, building_width, building_height)
        right_building_rect = pygame.Rect(window_width - building_width, 0, building_width, building_height)
        pygame.draw.rect(background_surface, building_color, left_building_rect)
        pygame.draw.rect(background_surface, building_color, right_building_rect)

        # Draw falling blocks
        for block in blocks:
            block.draw(background_surface)

        # Draw player and grappling hook
        player.draw(background_surface)
        if player.grappling_hook_on:
            player.grappling_hook.draw(background_surface)
        elif event.type == pygame.MOUSEBUTTONDOWN and not is_grappling:
            is_grappling = True
            grappling_hook = GrapplingHook(player_x, player_y, pygame.mouse.get_pos(), GRAPPLING_HOOK_SPEED)
        elif event.type == pygame.MOUSEBUTTONUP and is_grappling:
            is_grappling = False
            grappling_hook.release()
         # Actualizar la posición del jugador
        if is_grappling:
            player_x, player_y = grappling_hook.update(player_x, player_y)

        # Actualizar la posición de los bloques y detectar colisiones
        for block in blocks:
            block.update()
            if block.collides_with(player_x, player_y):
                game_over = True
                break

        # Actualizar la puntuación y crear nuevos bloques
        score += 1
        if score % 50 == 0:
            blocks.append(Block())

        # Dibujar el escenario
        window.blit(background, (0, 0))
        for block in blocks:
            block.draw(window)
        player_rect = player.get_rect(center=(player_x, player_y))
        window.blit(player, player_rect)

        # Dibujar la puntuación
        score_text = font.render(f"Score: {score}", True, white)
        score_rect = score_text.get_rect(topright=(window_width - 10, 10))
        window.blit(score_text, score_rect)

    else:
        # Si el juego ha terminado, mostrar la pantalla de Game Over
        score_text = big_font.render(f"Score: {score}", True, white)
        score_rect = score_text.get_rect()
        score_rect.center = (window_width // 2, window_height // 2 - 50)

        retry_text = font.render("Press R to retry", True, white)
        retry_rect = retry_text.get_rect()
        retry_rect.center = (window_width // 2, window_height // 2 + 50)

        window.blit(score_text, score_rect)
        window.blit(retry_text, retry_rect)

        pygame.display.update()

        # Esperar a que el usuario reinicie o cierre el juego
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        player_x = window_width // 2
                        player_y = window_height - 50
                        blocks = []
                        score = 0
                    elif event.key == pygame.K_ESCAPE:
                        game_running = False
                        waiting = False

    clock.tick(FPS)

pygame.quit()







