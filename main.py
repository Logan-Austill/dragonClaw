from backtracking import solve_backtracking
from lp_relaxation import LPRelaxation

board = (
    (1, 0, 0, 4),
    (0, 4, 1, 0),
    (0, 1, 4, 0),
    (4, 0, 0, 1)
)

lp = LPRelaxation()

def lp_check(board):
    result = lp.analyze(board)

    # Reject only proven-infeasible branches
    return result.status != "infeasible"

solution = solve_backtracking(
    board,
    feasibility_check=lp_check
)

if solution is None:
    print("No solution found.")
else:
    for row in solution:
        print(row)
