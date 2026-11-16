import random

def generate_solved_board(box_rows=3, box_cols=3):
    """
    Generates a valid, fully solved N x N Sudoku board where N = box_rows * box_cols.
    Supports non-square sub-grids for testing just because
    Note to self: This solution is NOT part of the solving algorithm
    """
    side = box_rows * box_cols

    # Generalized baseline pattern for R x C sub-grids
    def pattern(r, c):
        return (box_cols * (r % box_rows) + r // box_rows + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    # Shuffle bands (box_cols groups of box_rows) and rows within each band
    rows = [
        g * box_rows + r
        for g in shuffle(range(box_cols))
        for r in shuffle(range(box_rows))
    ]
    
    # Shuffle stacks (box_rows groups of box_cols) and columns within each stack
    cols = [
        g * box_cols + c
        for g in shuffle(range(box_rows))
        for c in shuffle(range(box_cols))
    ]
    
    nums = shuffle(range(1, side + 1))

    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def generate_puzzle(box_rows=3, box_cols=3, empty_ratio=0.5):
    """
    Creates a playable Sudoku puzzle with a guaranteed unique solution.
    empty_ratio controls the fraction of cells to clear (0.0 to 1.0)
    """
    side = box_rows * box_cols
    total_cells = side * side
    target_empty = int(total_cells * empty_ratio)

    board = generate_solved_board(box_rows, box_cols)
    cells = [(r, c) for r in range(side) for c in range(side)]
    random.shuffle(cells)

    removed = 0
    for r, c in cells:
        if removed >= target_empty:
            break
        board[r][c] = 0
    return board
