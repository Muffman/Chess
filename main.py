import pygame
from board import Board

pygame.init()


mate_font = pygame.font.SysFont('comicsans', 80)
to_move_font = pygame.font.SysFont('comicsans', 30)


ROWS, COLS = 8, 8
sq_size = 64

WIDTH, HEIGHT = COLS*sq_size, ROWS*sq_size

win = pygame.display.set_mode((WIDTH + 200, HEIGHT))
pygame.display.set_caption("Chess")


def change_turn(turn):
    if turn == 'w':
        return 'b'
    elif turn == 'b':
        return 'w'


def click_to_coords(mx, my):
    c = mx // sq_size
    r = my // sq_size

    return r, c


def find_king(color, board):
    name = color + 'K'
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece == '':
                continue
            if piece.name == name:
                return (r, c)


def check_for_check(board, turn):
    valid_locations = []
    king_pos = find_king(turn, board)
    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece != '' and piece.color != turn:
                valid_locations.extend(piece.valid_locations(board))
    if king_pos in valid_locations:
        return True
    else:
        return False


def check_for_checkmate(board, turn, move_log):
    mate = Board(ROWS, COLS)
    mate.place_pieces()
    for from_, to_ in move_log:
        r1, c1 = from_
        r2, c2 = to_
        moves = mate.board[r1][c1].valid_locations(mate.board)
        mate.board[r1][c1].move(mate.board, moves, r2, c2)

    for r, row in enumerate(board):
        for c, piece in enumerate(row):
            if piece != '' and piece.color == turn:
                for r2, c2 in piece.valid_locations(board):
                    mate.board[r][c].move(
                        mate.board, piece.valid_locations(board), r2, c2)
                    if not check_for_check(mate.board, turn):
                        return False

                    else:
                        mate.board = go_to_move(move_log, len(move_log))
    return True


def go_to_move(move_log, move_index):

    bord = Board(ROWS, COLS)
    bord.place_pieces()

    for move in range(move_index):
        from_, to_ = move_log[move]
        r1, c1 = from_
        r2, c2 = to_
        moves = bord.board[r1][c1].valid_locations(bord.board)
        bord.board[r1][c1].move(bord.board, moves, r2, c2)

    return bord.board


def draw_window(board, valid_locations, selected, mate):
    win.fill((0, 0, 0))
    board.draw(win)
    board.draw_pieces(win)

    if selected != None:
        r, c = selected
        pygame.draw.rect(
            win, 'red', (c*sq_size, r*sq_size, sq_size, sq_size), 2)

    for r, c in valid_locations:
        pygame.draw.rect(win, 'black', (c*64, r*64, 64, 64), 2)

    if mate:
        color = 'White' if next_turn == 'w' else 'Black'
        mate_label = mate_font.render(str(color)+" Won", 1, (255, 0, 0))
        win.blit(mate_label, (WIDTH//2-mate_label.get_width() //
                 2, HEIGHT//2-mate_label.get_height()//2))

    to_move_label = to_move_font.render("To Move:", 1, (255, 255, 255))
    win.blit(to_move_label, (WIDTH + 100 - to_move_label.get_width() //
             2 - 20, HEIGHT//2-to_move_label.get_height()//2 - 35))

    color = 'White' if turn == 'w' else 'Black'
    move_label = to_move_font.render(color, 1, (255, 255, 255))
    win.blit(move_label, (WIDTH + 100 - to_move_label.get_width() //
             2, HEIGHT//2-to_move_label.get_height()//2))

    pygame.display.update()


board = Board(ROWS, COLS)
board.place_pieces()
last_board_state = board.board.copy()
board_copy = board.board[:]

click_pair = []
move_log = []
move_index = 0

turn = 'w'
next_turn = 'b'

valid_locations = []
selected = None
castled = False
mate = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if x < WIDTH:
                row, col = click_to_coords(x, y)
                if len(click_pair) < 2:
                    if len(click_pair) == 0:
                        if board.board[row][col] != '':
                            if board.board[row][col].color == turn:
                                click_pair.append((row, col))
                                valid_locations = board.board[row][col].valid_locations(
                                    board.board)
                                selected = (row, col)

                    elif len(click_pair) == 1:
                        click_pair.append((row, col))

        if not mate:
            if len(click_pair) == 2:
                from_row, from_col = click_pair[0]
                to_row, to_col = click_pair[1]

                valid_locations = board.board[from_row][from_col].valid_locations(
                    board.board)

                if board.board[from_row][from_col] != '':
                    if board.board[from_row][from_col].name == turn + 'K':
                        castled = board.board[from_row][from_col].castle(
                            board.board, to_row, to_col)
                        if not castled:
                            moved = board.board[from_row][from_col].move(
                                board.board, valid_locations, to_row, to_col)
                    else:
                        moved = board.board[from_row][from_col].move(
                            board.board, valid_locations, to_row, to_col)

                    if moved or castled:
                        if not check_for_check(board.board, turn):
                            turn, next_turn = change_turn(turn), turn
                            move_log.append(click_pair)
                            move_index += 1
                            last_board_state = board.board.copy()
                        elif check_for_check(board.board, turn):
                            board.board = go_to_move(move_log, move_index)
                            moved = False
                valid_locations = []
                selected = None
                click_pair = []

    mate = check_for_checkmate(board.board, turn, move_log)
    if mate:
        valid_locations = []
        selected = None
        click_pair = []

    draw_window(board, valid_locations, selected, mate)
    pygame.display.update()

pygame.quit()
