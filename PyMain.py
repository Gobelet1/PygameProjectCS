import pygame
import sys
# CHESS BOARD
pygame.mixer.quit()
# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (232, 235, 239)
GRAY = (125, 135, 150)

# Load images
def load_images():
    pieces = ['bp', 'br', 'bn', 'bb', 'bq', 'bk',
              'wp', 'wr', 'wn', 'wb', 'wq', 'wk']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(
            pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE)
        )
    return images

# Draw board
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Initialize pieces on board
def init_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]

    # Place pawns
    for i in range(COLS):
        board[1][i] = 'bp'
        board[6][i] = 'wp'

    # Rooks, Knights, Bishops, Queen, King
    order = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    for i in range(COLS):
        board[0][i] = 'b' + order[i]
        board[7][i] = 'w' + order[i]

    return board

# Draw pieces
def draw_pieces(win, board, images, selected_piece):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                if selected_piece and selected_piece['pos'] == (row, col):
                    continue  # Skip drawing if dragging
                win.blit(images[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))

# Get row/col from mouse position
def get_row_col_from_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Basic Chess")
    clock = pygame.time.Clock()

    images = load_images()
    board = init_board()
    selected_piece = None

    run = True
    while run:
        clock.tick(60)
        draw_board(win)
        draw_pieces(win, board, images, selected_piece)
        if selected_piece:
            win.blit(images[selected_piece['piece']], selected_piece['mouse_pos'])
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                piece = board[row][col]
                if piece:
                    selected_piece = {
                        'piece': piece,
                        'pos': (row, col),
                        'mouse_pos': pygame.mouse.get_pos()
                    }

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece:
                    new_row, new_col = get_row_col_from_mouse(pygame.mouse.get_pos())
                    old_row, old_col = selected_piece['pos']
                    board[new_row][new_col] = selected_piece['piece']
                    board[old_row][old_col] = None
                    selected_piece = None

            elif event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    selected_piece['mouse_pos'] = pygame.mouse.get_pos()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
