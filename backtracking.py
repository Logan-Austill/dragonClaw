
from board import validate_board, candidates, consistent

def solve_backtracking(board, feasibility_check=None, stats=None):
    """
    Base backtracking algorithm to work from
    """
    validate_board(board)

    # Used for tracking metrics
    if stats is None:
        stats = {}

    # tracks nodes expanded, nodes pruned and assignments tried
    stats["nodes_expanded"] = 0
    stats["nodes_pruned"] = 0
    stats["assignments_tried"] = 0

    # Checking for duplicate values
    if not consistent(board):
        return None

    # Creating the grid used for backtracking
    grid = [list(row) for row in board]

    def search():
        stats["nodes_expanded"] += 1

        # Keeps track of empty cells
        empty = None

        for r in range(len(grid)):
            for c in range(len(grid)):
                if grid[r][c] == 0:
                    empty = (r, c)
                    break
            if empty is not None:
                break

        if empty is None:
            return True

        r, c = empty

        # Tries each candidate value (available values) in empty grid positions
        for value in sorted(candidates(grid, r, c)):
            stats["assignments_tried"] += 1
            grid[r][c] = value

            allowed = True

            if feasibility_check is not None:
                state = tuple(tuple(row) for row in grid)
                allowed = feasibility_check(state)

            if not allowed:
                stats["nodes_pruned"] += 1

            if allowed and search():
                return True

            grid[r][c] = 0

        return False

    # If successful, return the grid
    if search():
        return tuple(tuple(row) for row in grid)

    return None
