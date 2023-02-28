import pygame


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color.lower()[0]
        self.empty = ''
        self.moved = False
        self.sq_size = 64
        self.alive = True

    def move(self, board, valid_moves, to_row, to_col):
        if (to_row, to_col) in valid_moves:
            board[self.row][self.col], board[to_row][to_col] = self.empty, board[self.row][self.col]
            self.row, self.col = to_row, to_col
            self.moved = True
            return True
        else:
            return False

    def draw(self, win, img, sq_size):
        if self.alive:
            img = pygame.transform.scale(img, (sq_size, sq_size))
            x = self.col * sq_size
            y = self.row * sq_size
            win.blit(img, (x, y))


class Pawn(Piece):
    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.img = pygame.image.load(f"Images/{self.color}P.png")
        self.name = self.color+"P"

    def valid_locations(self, board):
        valid_moves = []
        mutiplier = 1 if self.color == 'w' else -1
        if board[self.row-(mutiplier*1)][self.col] == self.empty:
            valid_moves.append((self.row-(mutiplier*1), self.col))
            if not self.moved:
                if board[self.row-(mutiplier*2)][self.col] == self.empty:
                    valid_moves.append((self.row-(mutiplier*2), self.col))

        if self.col > 0:
            if board[self.row-(mutiplier*1)][self.col-1] != self.empty and board[self.row-(mutiplier*1)][self.col-1].color != self.color:
                valid_moves.append((self.row-(mutiplier*1), self.col-1))
        if self.col < len(board[0])-1:
            if board[self.row-(mutiplier*1)][self.col+1] != self.empty and board[self.row-(mutiplier*1)][self.col+1].color != self.color:
                valid_moves.append((self.row-(mutiplier*1), self.col+1))
        return valid_moves


class Knight(Piece):
    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.img = pygame.image.load(f"Images/{self.color}N.png")
        self.name = self.color+'N'

    def valid_locations(self, board):
        all_moves = [(self.row-2, self.col-1),
                     (self.row-2, self.col+1),
                     (self.row-1, self.col+2),
                     (self.row+1, self.col+2),
                     (self.row+2, self.col+1),
                     (self.row+2, self.col-1),
                     (self.row+1, self.col-2),
                     (self.row-1, self.col-2)]
        valid_moves = []
        for move in all_moves:
            r, c = move
            if r not in range(len(board)) or c not in range(len(board[0])):
                continue
            if board[r][c] == self.empty:
                valid_moves.append(move)
            elif board[r][c].color != self.color:
                valid_moves.append(move)
        return valid_moves


class Bishop(Piece):
    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.img = pygame.image.load(f"Images/{self.color}B.png")
        self.name = self.color+'B'

    def valid_locations(self, board):
        valid_moves = []
        # top_left
        searching = True
        for r in range(self.row-1, -1, -1):
            if searching:
                for c in range(self.col-1, -1, -1):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                valid_moves.append((r, c))
                                searching = False
                                break
                        else:
                            valid_moves.append((r, c))
        # top_right
        searching = True
        for r in range(self.row-1, -1, -1):
            if searching:
                for c in range(self.col+1, len(board[0])):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                searching = False
                                valid_moves.append((r, c))
                                break
                        else:
                            valid_moves.append((r, c))
        # bottom_left
        searching = True
        for r in range(self.row+1, len(board)):
            if searching:
                for c in range(self.col-1, -1, -1):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                searching = False
                                valid_moves.append((r, c))
                                break
                        else:
                            valid_moves.append((r, c))
        # bottom_right
        searching = True
        for r in range(self.row+1, len(board)):
            if searching:
                for c in range(self.col+1, len(board[0])):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                searching = False
                                valid_moves.append((r, c))
                                break
                        else:
                            valid_moves.append((r, c))
        return valid_moves


class Rook(Piece):
    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.img = pygame.image.load(f"Images/{self.color}R.png")
        self.name = self.color+"R"

    def valid_locations(self, board):
        valid_moves = []
        # up
        for r in range(self.row-1, -1, -1):
            if board[r][self.col] == self.empty:
                valid_moves.append((r, self.col))
            elif board[r][self.col].color != self.color:
                valid_moves.append((r, self.col))
                break
            else:
                break
        # down
        for r in range(self.row+1, len(board)):
            if board[r][self.col] == self.empty:
                valid_moves.append((r, self.col))
            elif board[r][self.col].color != self.color:
                valid_moves.append((r, self.col))
                break
            else:
                break
        # right
        for c in range(self.col+1, len(board[0])):
            if board[self.row][c] == self.empty:
                valid_moves.append((self.row, c))
            elif board[self.row][c].color != self.color:
                valid_moves.append((self.row, c))
                break
            else:
                break
        # left
        for c in range(self.col-1, -1, -1):
            if board[self.row][c] == self.empty:
                valid_moves.append((self.row, c))
            elif board[self.row][c].color != self.color:
                valid_moves.append((self.row, c))
                break
            else:
                break
        return valid_moves


class Queen(Piece):
    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.img = pygame.image.load(f"Images/{self.color}Q.png")
        self.name = self.color+"Q"

    def valid_locations(self, board):
        valid_moves = []
        # top_left
        searching = True
        for r in range(self.row-1, -1, -1):
            if searching:
                for c in range(self.col-1, -1, -1):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                valid_moves.append((r, c))
                                searching = False
                                break
                        else:
                            valid_moves.append((r, c))
        # top_right
        searching = True
        for r in range(self.row-1, -1, -1):
            if searching:
                for c in range(self.col+1, len(board[0])):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                searching = False
                                valid_moves.append((r, c))
                                break
                        else:
                            valid_moves.append((r, c))
        # bottom_left
        searching = True
        for r in range(self.row+1, len(board)):
            if searching:
                for c in range(self.col-1, -1, -1):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                searching = False
                                valid_moves.append((r, c))
                                break
                        else:
                            valid_moves.append((r, c))
        # bottom_right
        searching = True
        for r in range(self.row+1, len(board)):
            if searching:
                for c in range(self.col+1, len(board[0])):
                    if abs(self.row-r) == abs(self.col-c):
                        if board[r][c] != self.empty:
                            if board[r][c].color == self.color:
                                searching = False
                                break
                            else:
                                searching = False
                                valid_moves.append((r, c))
                                break
                        else:
                            valid_moves.append((r, c))
        # up
        for r in range(self.row-1, -1, -1):
            if board[r][self.col] == self.empty:
                valid_moves.append((r, self.col))
            elif board[r][self.col].color != self.color:
                valid_moves.append((r, self.col))
                break
            else:
                break
        # down
        for r in range(self.row+1, len(board)):
            if board[r][self.col] == self.empty:
                valid_moves.append((r, self.col))
            elif board[r][self.col].color != self.color:
                valid_moves.append((r, self.col))
                break
            else:
                break
        # right
        for c in range(self.col+1, len(board[0])):
            if board[self.row][c] == self.empty:
                valid_moves.append((self.row, c))
            elif board[self.row][c].color != self.color:
                valid_moves.append((self.row, c))
                break
            else:
                break
        # left
        for c in range(self.col-1, -1, -1):
            if board[self.row][c] == self.empty:
                valid_moves.append((self.row, c))
            elif board[self.row][c].color != self.color:
                valid_moves.append((self.row, c))
                break
            else:
                break
        return valid_moves


class King(Piece):
    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.img = pygame.image.load(f"Images/{self.color}K.png")
        self.name = self.color+'K'

    def valid_locations(self, board):
        all_moves = [(self.row, self.col-1),
                     (self.row, self.col+1),
                     (self.row-1, self.col),
                     (self.row+1, self.col),
                     (self.row+1, self.col+1),
                     (self.row-1, self.col-1),
                     (self.row+1, self.col-1),
                     (self.row-1, self.col+1)]
        valid_moves = []
        for move in all_moves:
            r, c = move
            if r not in range(len(board)) or c not in range(len(board[0])):
                continue
            if board[r][c] == self.empty:
                valid_moves.append(move)
            elif board[r][c].color != self.color:
                valid_moves.append(move)
        return valid_moves
