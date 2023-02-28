import pygame
from board import Board

pygame.init()


ROWS, COLS = 8, 8
sq_size = 64

WIDTH, HEIGHT = COLS*sq_size, ROWS*sq_size

win = pygame.display.set_mode((WIDTH, HEIGHT))
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


def draw_window(board, valid_locations, selected):
    board.draw(win)
    board.draw_pieces(win)

    for r, c in valid_locations:
        pygame.draw.rect(win, 'black', (c*64, r*64, 64, 64), 2)

    if selected != None:
        r, c = selected
        pygame.draw.rect(
            win, 'red', (c*sq_size, r*sq_size, sq_size, sq_size), 2)

    pygame.display.update()


board = Board(ROWS, COLS)
board.place_pieces()


click_pair = []
move_log = []

turn = 'w'

valid_locations = []
selected = None


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            row, col = click_to_coords(*pygame.mouse.get_pos())
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

        if len(click_pair) == 2:
            from_row, from_col = click_pair[0]
            to_row, to_col = click_pair[1]

            valid_locations = board.board[from_row][from_col].valid_locations(
                board.board)

            moved = board.board[from_row][from_col].move(
                board.board, valid_locations, to_row, to_col)
            if moved:
                turn = change_turn(turn)
                move_log.append(click_pair)
            selected = None
            valid_locations = []
            click_pair = []

    draw_window(board, valid_locations, selected)
    pygame.display.update()

pygame.quit()
