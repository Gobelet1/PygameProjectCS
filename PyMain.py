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
def is_valid_move(piece, start, end, board):
    piece_type = piece[1]  # 'p', 'r', 'n', 'b', 'q', 'k'
    color = piece[0]       # 'w' or 'b'
    start_row, start_col = start
    end_row, end_col = end
    dr = end_row - start_row
    dc = end_col - start_col

    destination = board[end_row][end_col]
    if destination and destination[0] == color:
        return False  # Can't capture own piece

    if piece_type == 'p':  # Pawn
        direction = -1 if color == 'w' else 1
        start_row_home = 6 if color == 'w' else 1
        if dc == 0:
            if dr == direction and not destination:
                return True
            if dr == 2 * direction and start_row == start_row_home and not board[start_row + direction][start_col] and not destination:
                return True
        elif abs(dc) == 1 and dr == direction and destination and destination[0] != color:
            return True

    elif piece_type == 'r':  # Rook
        if dr == 0 or dc == 0:
            return path_is_clear(start, end, board)

    elif piece_type == 'n':  # Knight
        if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
            return True

    elif piece_type == 'b':  # Bishop
        if abs(dr) == abs(dc):
            return path_is_clear(start, end, board)

    elif piece_type == 'q':  # Queen
        if dr == 0 or dc == 0 or abs(dr) == abs(dc):
            return path_is_clear(start, end, board)

    elif piece_type == 'k':  # King
        if max(abs(dr), abs(dc)) == 1:
            return True

    return False  # Invalid move
def is_valid_move(piece, start, end, board):
    piece_type = piece[1]  # 'p', 'r', 'n', 'b', 'q', 'k'
    color = piece[0]       # 'w' or 'b'
    start_row, start_col = start
    end_row, end_col = end
    dr = end_row - start_row
    dc = end_col - start_col

    destination = board[end_row][end_col]
    if destination and destination[0] == color:
        return False  # Can't capture own piece

    if piece_type == 'p':  # Pawn
        direction = -1 if color == 'w' else 1
        start_row_home = 6 if color == 'w' else 1
        if dc == 0:
            if dr == direction and not destination:
                return True
            if dr == 2 * direction and start_row == start_row_home and not board[start_row + direction][start_col] and not destination:
                return True
        elif abs(dc) == 1 and dr == direction and destination and destination[0] != color:
            return True

    elif piece_type == 'r':  # Rook
        if dr == 0 or dc == 0:
            return path_is_clear(start, end, board)

    elif piece_type == 'n':  # Knight
        if (abs(dr), abs(dc)) in [(2, 1), (1, 2)]:
            return True

    elif piece_type == 'b':  # Bishop
        if abs(dr) == abs(dc):
            return path_is_clear(start, end, board)

    elif piece_type == 'q':  # Queen
        if dr == 0 or dc == 0 or abs(dr) == abs(dc):
            return path_is_clear(start, end, board)

    elif piece_type == 'k':  # King
        if max(abs(dr), abs(dc)) == 1:
            return True

    return False  # Invalid move
def path_is_clear(start, end, board):
    r1, c1 = start
    r2, c2 = end
    dr = r2 - r1
    dc = c2 - c1

    step_r = (dr // abs(dr)) if dr != 0 else 0
    step_c = (dc // abs(dc)) if dc != 0 else 0

    r, c = r1 + step_r, c1 + step_c
    while (r, c) != (r2, c2):
        if board[r][c] is not None:
            return False
        r += step_r
        c += step_c
    return True


def main():
    turn = 'w' #White starts
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
                if piece and piece[0] == turn:  # Only allow selecting current player's piece
                        selected_piece = {
                        'piece': piece,
                        'pos': (row, col),
                        'mouse_pos': pygame.mouse.get_pos()
                        }

            elif event.type == pygame.MOUSEBUTTONUP:
               if selected_piece:
                   new_row, new_col = get_row_col_from_mouse(pygame.mouse.get_pos())
                   old_row, old_col = selected_piece['pos']
                   piece = selected_piece['piece']

                   if 0 <= new_row < 8 and 0 <= new_col < 8:
                       if is_valid_move(piece, (old_row, old_col), (new_row, new_col), board):
                           board[new_row][new_col] = piece
                           board[old_row][old_col] = None
                           turn = 'b' if turn == 'w' else 'w'  # Switch turns
                   selected_piece = None

            elif event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    selected_piece['mouse_pos'] = pygame.mouse.get_pos()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
