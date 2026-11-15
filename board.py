from math import isqrt

def validate_board(board):
    N = len(board)
    n = isqrt(N)

    if N == 0 or n * n != N:
        raise ValueError("Board size must be n^2.")

    if any(len(row) != N for row in board):
        raise ValueError("Board must be square.")

    if any(
        type(value) is not int or not 0 <= value <= N
        for row in board for value in row
    ):
        raise ValueError("Invalid cell value.")

    return n

def candidates(board, r, c):
    N = len(board)
    n = isqrt(N)

    if board[r][c] != 0:
        return set()

    used = set(board[r])

    used.update(board[i][c] for i in range(N))

    br = (r // n) * n
    bc = (c // n) * n

    for i in range(br, br + n):
        for j in range(bc, bc + n):
            used.add(board[i][j])

    return set(range(1, N + 1)) - used

def consistent(board):
    """Check for duplicate nonzero values in houses."""
    N = len(board)
    n = isqrt(N)

    houses = []

    houses.extend(board)

    houses.extend(
        [board[r][c] for r in range(N)]
        for c in range(N)
    )

    for br in range(0, N, n):
        for bc in range(0, N, n):
            houses.append([
                board[r][c]
                for r in range(br, br + n)
                for c in range(bc, bc + n)
            ])

    for house in houses:
        values = [v for v in house if v != 0]
        if len(values) != len(set(values)):
            return False

    return True
