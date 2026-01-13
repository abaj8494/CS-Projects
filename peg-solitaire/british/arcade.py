N = 7
EMPTY = 0
PEG = 1
HOLE = -1


class PegSolitaire:
    def __init__(self, board):
        self.board = board
        self.moves = []
        self.expanded = 0  # number of unique board-states expanded

    # ---------- Core logic ----------

    def is_solved(self):
        """Solved if exactly one peg remains."""
        pegs = sum(cell > 0 for row in self.board for cell in row)
        return pegs == 1

    def get_valid_moves(self):
        """
        Returns a list of moves of the form:
        (row, col, direction, jumped_value)
        """
        moves = []

        for r in range(N):
            for c in range(N):
                if self.board[r][c] <= 0:
                    continue

                # up
                if r > 1 and self.board[r - 1][c] > 0 and self.board[r - 2][c] < 0:
                    moves.append((r, c, "w", self.board[r - 1][c]))

                # left
                if c > 1 and self.board[r][c - 1] > 0 and self.board[r][c - 2] < 0:
                    moves.append((r, c, "a", self.board[r][c - 1]))

                # down
                if r < N - 2 and self.board[r + 1][c] > 0 and self.board[r + 2][c] < 0:
                    moves.append((r, c, "s", self.board[r + 1][c]))

                # right
                if c < N - 2 and self.board[r][c + 1] > 0 and self.board[r][c + 2] < 0:
                    moves.append((r, c, "d", self.board[r][c + 1]))

        return moves

    def make_move(self, move):
        """Apply a move to the board."""
        r, c, direction, jumped = move
        self.moves.append(move)

        if direction == "w":
            self.board[r][c] = HOLE
            self.board[r - 1][c] = HOLE
            self.board[r - 2][c] = PEG

        elif direction == "a":
            self.board[r][c] = HOLE
            self.board[r][c - 1] = HOLE
            self.board[r][c - 2] = PEG

        elif direction == "s":
            self.board[r][c] = HOLE
            self.board[r + 1][c] = HOLE
            self.board[r + 2][c] = PEG

        elif direction == "d":
            self.board[r][c] = HOLE
            self.board[r][c + 1] = HOLE
            self.board[r][c + 2] = PEG

    def undo_move(self):
        """Undo the most recent move."""
        r, c, direction, jumped = self.moves.pop()

        if direction == "w":
            self.board[r][c] = PEG
            self.board[r - 1][c] = jumped
            self.board[r - 2][c] = HOLE

        elif direction == "a":
            self.board[r][c] = PEG
            self.board[r][c - 1] = jumped
            self.board[r][c - 2] = HOLE

        elif direction == "s":
            self.board[r][c] = PEG
            self.board[r + 1][c] = jumped
            self.board[r + 2][c] = HOLE

        elif direction == "d":
            self.board[r][c] = PEG
            self.board[r][c + 1] = jumped
            self.board[r][c + 2] = HOLE

    # ---------- Search ----------

    def encode_board(self):
        """
        Encode the board as a bitstring integer.
        Peg = 1, Hole / Empty = 0
        """
        bits = []
        for row in self.board:
            for cell in row:
                bits.append("1" if cell > 0 else "0")
        return int("".join(bits), 2)

    def dfs(self, visited=None):
        """
        Depth-first search with state memoization.
        Counts each unique expanded board-state.
        """
        if visited is None:
            visited = set()

        state = self.encode_board()
        if state in visited:
            return False

        visited.add(state)
        self.expanded += 1

        if self.is_solved():
            return True

        for move in self.get_valid_moves():
            self.make_move(move)
            if self.dfs(visited):
                return True
            self.undo_move()

        return False

    # ---------- Debug / Output ----------

    def print_board(self):
        for row in self.board:
            for cell in row:
                if cell > 0:
                    print(".", end="")
                elif cell < 0:
                    print("O", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def print_moves(self):
        print("Moves:")
        for m in self.moves:
            print(m)
        print(f"\nMove count: {len(self.moves)}")
        print(f"Board-states expanded: {self.expanded}")


# ---------- Entry point ----------

if __name__ == "__main__":
    board = [
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, -1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
    ]

    game = PegSolitaire(board)
    game.dfs()
    game.print_moves()
