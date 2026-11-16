
from backtracking import solve_backtracking
from lp_relaxation import LPRelaxation
from board_generator import generate_puzzle
import time

board = generate_puzzle()
lp = LPRelaxation()

lp_calls = 0

def lp_check(board):
    """
    Quick sanity check to make sure the board is solvable
    """
    global lp_calls
    lp_calls += 1

    result = lp.analyze(board)
    return result.status != "infeasible"


# Ordinary backtracking
basic_stats = {}

start = time.perf_counter()
basic_solution = solve_backtracking(
    board,
    stats=basic_stats
)
basic_time = time.perf_counter() - start


# LP-assisted backtracking
lp_stats = {}

start = time.perf_counter()
lp_solution = solve_backtracking(
    board,
    feasibility_check=lp_check,
    stats=lp_stats
)
lp_time = time.perf_counter() - start

print("\n--- Ordinary Backtracking ---")
print("Nodes expanded:", basic_stats["nodes_expanded"])
print("Assignments tried:", basic_stats["assignments_tried"])
print(f"Time: {basic_time:.4f} seconds")

print("\n--- LP-Assisted Backtracking ---")
print("Nodes expanded:", lp_stats["nodes_expanded"])
print("Nodes pruned:", lp_stats["nodes_pruned"])
print("Assignments tried:", lp_stats["assignments_tried"])
print("LP calls:", lp_calls)
print(f"Time: {lp_time:.4f} seconds")

# This is for just in casees. I read that the solver can do whatever it wants
if basic_solution != lp_solution:
    print("Warning: Solutions differ!")

# The math on this took forever to figure out
if basic_stats["nodes_expanded"] > 0:
    reduction = (
        1 - lp_stats["nodes_expanded"]
        / basic_stats["nodes_expanded"]
    ) * 100

    print(f"\nNode reduction: {reduction:.2f}%")
