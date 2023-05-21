import pygame
import random
import pygame.font


# Constantes del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
COIN_WIDTH = 20
COIN_HEIGHT = 20
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
PLATFORM_COLOR = (0, 255, 0)
PLAYER_COLOR = (255, 0, 255)
COIN_COLOR = (255, 255, 0)
OBSTACLE_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)
FPS = 60
score = 0

# Definir la posición inicial del jugador
PLAYER_START_X = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
PLAYER_START_Y = 50

# Inicializar Pygame
pygame.init()

# Crear la ventana del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mi Juego de Plataformas")

# Crear un reloj para controlar la velocidad de actualización del juego
clock = pygame.time.Clock()
# Clase de la plataforma
class Platform:
    def __init__(self, x, y, width, height, color, move_direction=None, move_speed=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.move_direction = move_direction
        self.move_speed = move_speed

    def update(self):
        # Mover la plataforma
        if self.move_direction == "left":
            self.rect.x -= self.move_speed
        elif self.move_direction == "right":
            self.rect.x += self.move_speed

        # Hacer que la plataforma rebote al llegar al borde de la pantalla
        if self.rect.right >= SCREEN_WIDTH:
            self.move_direction = "left"
        elif self.rect.left <= 0:
            self.move_direction = "right"

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
# Clase del jugador
class Player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity = 0
        self.jump = False

    def update(self):
        # Aplicar gravedad al jugador
        self.velocity += 1
        self.rect.y += self.velocity

        # Evitar que el jugador salga de la pantalla
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0
            self.jump = False

        # Verificar si el jugador ha saltado
        if self.jump:
            self.velocity -= 20
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity > 0 and self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity = 0
                    self.jump = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
    # Clase de la moneda
class Coin:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        # Clase del obstáculo
class Obstacle:
    def __init__(self, x, y, width, height, color, move_direction=None, move_speed=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.move_direction = move_direction
        self.move_speed = move_speed

    def update(self):
        # Mover el obstáculo
        if self.move_direction == "left":
            self.rect.x -= self.move_speed
        elif self.move_direction == "right":
            self.rect.x += self.move_speed

        # Hacer que el obstáculo rebote al llegar al borde de la pantalla
        if self.rect.right >= SCREEN_WIDTH:
            self.move_direction = "left"
        elif self.rect.left <= 0:
            self.move_direction = "right"

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
# Función para generar plataformas
def generate_platforms():
    platforms = []

    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT)
        platform = Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR)
        platforms.append(platform)

    return platforms


# Función para generar monedas
def generate_coins():
    coins = []

    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH - COIN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        coin = Coin(x, y, COIN_WIDTH, COIN_HEIGHT, COIN_COLOR)
        coins.append(coin)

    return coins


# Función para generar obstáculos
def generate_obstacles():
    obstacles = []

    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        move_direction = random.choice(["left", "right"])
        move_speed = random.randint(1, 3)
        obstacle = Obstacle(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR, move_direction, move_speed)
        obstacles.append(obstacle)

    return obstacles
# Generar las plataformas, monedas y obstáculos
platforms = generate_platforms()
coins = generate_coins()
obstacles = generate_obstacles()

# Crear el jugador
player = Player(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)

# Bucle principal del juego
while True:
    # Manejar eventos de Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            SystemExit.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump = True

    # Actualizar elementos del juego
    player.update()
    for platform in platforms:
        platform.update()
    for coin in coins:
        coin.update()
    for obstacle in obstacles:
        obstacle.update()

        # Verificar si el jugador ha chocado con un obstáculo
        if player.rect.colliderect(obstacle.rect):
            game_over(score)

        # Verificar si el obstáculo ha chocado con una plataforma
        for platform in platforms:
            if obstacle.rect.colliderect(platform.rect):
                if obstacle.move_direction == "left":
                    obstacle.move_direction = "right"
                else:
                    obstacle.move_direction = "left"

    # Verificar si el jugador ha recogido una moneda
    for coin in coins:
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)
            score += 10

    # Dibujar elementos del juego
    screen.fill(BG_COLOR)
    for platform in platforms:
        platform.draw()
    for coin in coins:
        coin.draw()
    for obstacle in obstacles:
        obstacle.draw()
    player.draw()

    # Verificar si el jugador ha caído fuera de la pantalla
    if player.rect.top > SCREEN_HEIGHT:
        game_over(score)

    def game_over():
    # Mostrar mensaje de Game Over
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Actualizar la pantalla
    pygame.display.update()
    clock.tick(FPS)


# Mostrar la pantalla de Game Over
game_over_font = pygame.font.SysFont(None, 48)
game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

# Esperar un poco antes de salir
pygame.time.wait(2000)

# Salir del juego
pygame.quit()




