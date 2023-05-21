import pygame
import random

pygame.init()

# Define las dimensiones de la ventana
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600

# Define las dimensiones de cada bloque
BLOCK_SIZE = 30

# Define el número de columnas y filas del tablero
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Inicializar el puntaje
score = 0

# Actualizar el puntaje
score += 10

# Definir la velocidad del juego
FPS = 480


# Define el color de fondo de la ventana
BACKGROUND_COLOR = (255, 255, 255)

# Define los colores de los bloques
BLOCK_COLORS = [
    (255, 0, 0),    # Rojo
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarillo
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cian
    (128, 0, 0),    # Marrón
]

# Define los diferentes tipos de bloques
BLOCK_TYPES = [
    # Cuadrado
    [[1, 1],
     [1, 1]],
     
    # L
    [[1, 0],
     [1, 0],
     [1, 1]],
     
    # L invertida
    [[0, 1],
     [0, 1],
     [1, 1]],
     
    # Z
    [[1, 1, 0],
     [0, 1, 1]],
     
    # Z invertida
    [[0, 1, 1],
     [1, 1, 0]],
     
    # T
    [[1, 1, 1],
     [0, 1, 0]],
     
    # Barra
    [[1],
     [1],
     [1],
     [1]]
]

# Crea la ventana del juego
window = pygame.display.set_mode((WINDOW_WIDTH + 150, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

# Función para dibujar el siguiente bloque en la ventana
def draw_next_block(block, color):
    font = pygame.font.Font(None, 30)
    text = font.render("Next Block", True, (255, 255, 255))
    window.blit(text, (WINDOW_WIDTH + 10, 10))

    # Dibuja el bloque
    x_offset = WINDOW_WIDTH + 10
    y_offset = 50
    block_height = len(block)
    block_width = len(block[0]) if block_height > 0 else 0
    for row in range(block_height):
        for col in range(block_width):
            if block[row][col] != 0:
                x = x_offset + col * BLOCK_SIZE
                y = y_offset + row * BLOCK_SIZE
                pygame.draw.rect(window, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 0)

# función para dibujar el puntaje
def DrawScore(score):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

# Crea el reloj del juego
clock = pygame.time.Clock()

# Dibujar el puntaje
font = pygame.font.Font(None, 30)
text = font.render("Score: " + str(score), True, (255, 255, 255))
window.blit(text, (WINDOW_WIDTH + 10, 200))


# Función para crear un nuevo bloque aleatorio
def new_block():
    block = random.choice(BLOCK_TYPES)
    color = random.choice(BLOCK_COLORS)
    return block, color

# Función para dibujar un bloque en el tablero
def draw_block(x, y, color):
    pygame.draw.rect(window, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(window, (0, 0, 0), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Función para dibujar el tablero
def draw_board(board):
    for y, row in enumerate(board):
        for x, block in enumerate(row):
            if block:
                draw_block(x, y, BLOCK_COLORS[block - 1])

# Función para rotar un bloque
def rotate_block(block):
    return [[block[y][x] for y in range(len(block))] for x in range(len(block[0]) - 1, -1, -1)]

# Función para comprobar si un bloque cabe en el tablero
def check_collision(board, block, x, y):
    for j, row in enumerate(block):
        for i, cell in enumerate(row):
            if cell and board[j + y][i + x]:
                return True
    return False

# Función para verificar si la posición actual del bloque es válida
def is_valid_position(board, block, x, y):
    for i in range(4):
        for j in range(4):
            if i + y < 0 or i + y >= BOARD_HEIGHT or j + x < 0 or j + x >= BOARD_WIDTH:
                if block[i][j] != 0:
                    return False
            elif board[i + y][j + x] != 0 and block[i][j] != 0:
                return False
    return True



# Función para agregar un bloque al tablero
def add_block_to_board(board, block, x, y):
    for j, row in enumerate(block):
        for i, cell in enumerate(row):
            if cell:
                board[j + y][i + x] = cell

# Función para borrar una fila completa del tablero
def delete_row(board, row):
    del board[row]
    board.insert(0, [0] * BOARD_WIDTH)

# Función para comprobar si una fila está completa
def check_row(board, row):
    for cell in board[row]:
        if not cell:
            return False
    return True

# Función para eliminar las filas completas del tablero
def remove_complete_rows(board):
    rows_removed = 0
    for i in range(len(board)):
        if check_row(board, i):
            delete_row(board, i)
            rows_removed += 1
    return rows_removed

# Función principal del juego
def main():
    # Crea el tablero
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]



    # Crea el bloque actual y el siguiente
    current_block, current_color = new_block()
    next_block, next_color = new_block()

    # Inicializa el marcador
    score = 0

    # Inicializa las variables del juego
    game_over = False
    block_x = BOARD_WIDTH // 2 - len(current_block[0]) // 2
    block_y = 0
    block_fall_time = 0
    block_fall_speed = 0.5

    # Bucle principal del juego
    while not game_over:
        # Maneja los eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Actualiza el bloque actual
        block_fall_time += clock.get_rawtime()
        if block_fall_time >= block_fall_speed * 1000:
            block_fall_time = 0
            block_y += 1
            if check_collision(board, current_block, block_x, block_y):
                block_y -= 1
                add_block_to_board(board, current_block, block_x, block_y)
                score += remove_complete_rows(board) * 100
                current_block, current_color = next_block, next_color
                next_block, next_color = new_block()
                block_x = BOARD_WIDTH // 2 - len(current_block[0]) // 2
                block_y = 0
                if check_collision(board, current_block, block_x, block_y):
                    game_over = True

        # Dibuja la ventana del juego
        window.fill(BACKGROUND_COLOR)
        draw_board(board)
        draw_block(block_x, block_y, current_color)
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH, 0, 150, WINDOW_HEIGHT), 0)
        draw_next_block(next_block, next_color)
        DrawScore(score)
        pygame.display.update()

        # Actualiza el reloj del juego
        clock.tick(FPS)

    # Cierra el juego
    pygame.quit()
    sys.exit()

# Inicializa el juego
if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH + 150, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    main()



