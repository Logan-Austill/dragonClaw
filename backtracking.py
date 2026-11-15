from board import validate_board, candidates, consistent

def solve_backtracking(board, feasibility_check=None):
    validate_board(board)

    if not consistent(board):
        return None

    # Make a mutable copy of the input
    grid = [list(row) for row in board]

    def search():
        # Find first empty cell
        empty = None

        for r in range(len(grid)):
            for c in range(len(grid)):
                if grid[r][c] == 0:
                    empty = (r, c)
                    break
            if empty is not None:
                break

        # No empty cells: puzzle solved
        if empty is None:
            return True

        r, c = empty

        for value in sorted(candidates(grid, r, c)):
            grid[r][c] = value

            allowed = True

            if feasibility_check is not None:
                state = tuple(tuple(row) for row in grid)
                allowed = feasibility_check(state)

            if allowed and search():
                return True

            # Undo the assignment
            grid[r][c] = 0

        return False

    if search():
        return tuple(tuple(row) for row in grid)

    return None
