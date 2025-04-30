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
def is_valid_move(piece, start, end, board, en_passant_target):
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
        #En Passant Capture
        elif abs(dc) == 1 and dr == direction and (end_row, end_col) == en_passant_target:
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
        return True  # normal king move

        # Castling
        if dr == 0 and abs(dc) == 2:
            # Kingside or Queenside
            rook_col = 7 if dc > 0 else 0
            rook = board[start_row][rook_col]
            if not rook or rook[1] != 'r' or rook[0] != color:
                return False

            # Check if path is clear
            step = 1 if dc > 0 else -1
            for c in range(start_col + step, rook_col, step):
                if board[start_row][c] is not None:
                    return False

        # Check if king or rook has moved
            if color == 'w':
                if has_moved['w_king']:
                    return False
                if dc > 0 and has_moved['w_rook_ks']:
                    return False
                if dc < 0 and has_moved['w_rook_qs']:
                    return False
            else:
                if has_moved['b_king']:
                    return False
                if dc > 0 and has_moved['b_rook_ks']:
                    return False
                if dc < 0 and has_moved['b_rook_qs']:
                    return False

            return True  # Castling allowed

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
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Basic Chess")
    clock = pygame.time.Clock()

    images = load_images()
    board = init_board()
    selected_piece = None
    en_passant_target = None  # Will be set to (row, col) of capturable pawn
    turn = 'w' #White starts
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
                       if is_valid_move(piece, (old_row, old_col), (new_row, new_col), board, en_passant_target):
                           board[new_row][new_col] = piece
                           board[old_row][old_col] = None
                       # Castling
                       if piece[1] == 'k' and abs(new_col - old_col) == 2:
                           if new_col > old_col:  # Kingside
                               board[new_row][5] = board[new_row][7]
                               board[new_row][7] = None
                           else:  # Queenside
                               board[new_row][3] = board[new_row][0]
                               board[new_row][0] = None
                       # Update movement flags
                       if piece == 'wk':
                           has_moved['w_king'] = True
                       elif piece == 'bk':
                           has_moved['b_king'] = True
                       elif piece == 'wr' and old_col == 0:
                           has_moved['w_rook_qs'] = True
                       elif piece == 'wr' and old_col == 7:
                           has_moved['w_rook_ks'] = True
                       elif piece == 'br' and old_col == 0:
                           has_moved['b_rook_qs'] = True
                       elif piece == 'br' and old_col == 7:
                           has_moved['b_rook_ks'] = True
                       # En passant capture
                       if piece[1] == 'p' and (new_row, new_col) == en_passant_target:
                           board[old_row][new_col] = None  # Remove the captured pawn

                       # Handle en passant eligibility
                       if piece[1] == 'p' and abs(new_row - old_row) == 2:
                           en_passant_target = ((old_row + new_row) // 2, new_col)
                       else:
                           en_passant_target = None

                       turn = 'b' if turn == 'w' else 'w'
                   selected_piece = None

            elif event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    selected_piece['mouse_pos'] = pygame.mouse.get_pos()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
