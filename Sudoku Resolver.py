import pygame
import sys
from pygame.locals import *

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WINDOW_SIZE = 540
GRID_SIZE = WINDOW_SIZE // 9
LINE_WIDTH = 2
FONT_SIZE = 40
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Crear la ventana
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BUTTON_HEIGHT))
pygame.display.set_caption('Sudoku Resolutor')

# Fuente para el texto
font = pygame.font.Font(None, FONT_SIZE)

def draw_board(board, editable, selected):
    """
    Dibuja el tablero de Sudoku y los botones en la pantalla.
    """
    # Limpiar la pantalla
    screen.fill(WHITE)

    # Dibujar las líneas del tablero
    for i in range(10):
        # Ajustar el grosor de las líneas
        thickness = LINE_WIDTH if i % 3 else 4
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, WINDOW_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WINDOW_SIZE, i * GRID_SIZE), thickness)

    # Dibujar los números en el tablero
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num:
                # Establecer el color basado en si el número es editable o no
                color = BLUE if editable[i][j] else BLACK
                text = font.render(str(num), True, color)
                text_rect = text.get_rect(center=(j * GRID_SIZE + GRID_SIZE // 2, i * GRID_SIZE + GRID_SIZE // 2))
                screen.blit(text, text_rect)
            if editable[i][j]:
                pygame.draw.rect(screen, BLACK, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    # Resaltar la celda seleccionada
    if selected:
        pygame.draw.rect(screen, GREEN, (selected[1] * GRID_SIZE, selected[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)

    # Dibujar los botones
    pygame.draw.rect(screen, BLACK, (0, WINDOW_SIZE, WINDOW_SIZE, BUTTON_HEIGHT))
    pygame.draw.line(screen, WHITE, (WINDOW_SIZE // 2, WINDOW_SIZE), (WINDOW_SIZE // 2, WINDOW_SIZE + BUTTON_HEIGHT), 1)
    
    solve_button = font.render("Resolver", True, WHITE)
    solve_button_rect = solve_button.get_rect(center=(WINDOW_SIZE // 4, WINDOW_SIZE + BUTTON_HEIGHT // 2))
    screen.blit(solve_button, solve_button_rect)
    
    clear_button = font.render("Borrar", True, WHITE)
    clear_button_rect = clear_button.get_rect(center=(3 * WINDOW_SIZE // 4, WINDOW_SIZE + BUTTON_HEIGHT // 2))
    screen.blit(clear_button, clear_button_rect)

def is_valid(board, row, col, num):
    """
    Verifica si un número puede ser colocado en una celda específica.
    """
    # Verificar fila
    for x in range(9):
        if board[row][x] == num:
            return False
    # Verificar columna
    for x in range(9):
        if board[x][col] == num:
            return False
    # Verificar subcuadro 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board, editable):
    """
    Resuelve el tablero de Sudoku utilizando backtracking.
    """
    empty = find_empty_location(board)
    if not empty:
        return True  # No hay ubicaciones vacías, el Sudoku está resuelto
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            editable[row][col] = False  # Marcar como no editable
            if solve_sudoku(board, editable):
                return True
            board[row][col] = 0  # Backtracking
            editable[row][col] = True  # Volver a marcar como editable
    return False

def find_empty_location(board):
    """
    Encuentra una celda vacía en el tablero.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def main():
    """
    Función principal del programa.
    """
    # Crear tablero vacío y editable
    board = [[0] * 9 for _ in range(9)]
    editable = [[True] * 9 for _ in range(9)]
    selected = None

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                # Manejar la selección de celdas y botones
                x, y = event.pos
                if y < WINDOW_SIZE:
                    selected = (y // GRID_SIZE, x // GRID_SIZE)
                else:
                    if WINDOW_SIZE <= y <= WINDOW_SIZE + BUTTON_HEIGHT:
                        if WINDOW_SIZE // 4 - BUTTON_WIDTH // 2 <= x <= WINDOW_SIZE // 4 + BUTTON_WIDTH // 2:
                            solve_sudoku(board, editable)
                        elif 3 * WINDOW_SIZE // 4 - BUTTON_WIDTH // 2 <= x <= 3 * WINDOW_SIZE // 4 + BUTTON_WIDTH // 2:
                            board = [[0] * 9 for _ in range(9)]
                            editable = [[True] * 9 for _ in range(9)]
                            selected = None
            elif event.type == KEYDOWN:
                if selected:
                    row, col = selected
                    # Detectar entrada de números (teclas 1-9)
                    if event.key in range(K_1, K_9 + 1):
                        num = event.key - K_0
                        if editable[row][col]:
                            board[row][col] = num
                    # Detectar entrada de números (teclado numérico 1-9)
                    elif event.key in range(K_KP1, K_KP9 + 1):
                        num = event.key - K_KP1 + 1
                        if editable[row][col]:
                            board[row][col] = num
                    # Borrar celda con BACKSPACE
                    elif event.key == K_BACKSPACE:
                        if editable[row][col]:
                            board[row][col] = 0

        # Dibuja el tablero y actualiza la pantalla
        draw_board(board, editable, selected)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
