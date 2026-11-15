from dataclasses import dataclass
from math import isqrt
import pulp

from board import validate_board, consistent

@dataclass
class LPResult:
    status: str
    integral: bool = False
    solution: tuple | None = None

class LPRelaxation:
    def analyze(self, board):
        n = validate_board(board)
        N = n * n

        # Checking if the board is legal or not
        if not consistent(board):
            return LPResult("infeasible")

        cells = range(N)
        digits = range(1, N + 1)

        # What it is and what we're doing
        model = pulp.LpProblem(
            "SudokuRelaxation",
            pulp.LpMinimize
        )

        # Continuous variables: 0 <= x <= 1
        x = pulp.LpVariable.dicts(
            "x",
            (cells, cells, digits),
            lowBound=0,
            upBound=1,
            cat=pulp.LpContinuous
        )

        # IDK man
        model += 0

        # Exactly one value per cell
        for r in cells:
            for c in cells:
                model += pulp.lpSum(
                    x[r][c][v] for v in digits
                ) == 1

        # Every value appears once in each row
        for r in cells:
            for v in digits:
                model += pulp.lpSum(
                    x[r][c][v] for c in cells
                ) == 1

        # Every value appears once in each column
        for c in cells:
            for v in digits:
                model += pulp.lpSum(
                    x[r][c][v] for r in cells
                ) == 1

        # Every value appears once in each subgrid
        for br in range(0, N, n):
            for bc in range(0, N, n):
                for v in digits:
                    model += pulp.lpSum(
                        x[r][c][v]
                        for r in range(br, br + n)
                        for c in range(bc, bc + n)
                    ) == 1

        # Fix original clues and search assignments
        for r in cells:
            for c in cells:
                if board[r][c] != 0:
                    model += (
                        x[r][c][board[r][c]] == 1
                    )

        status = model.solve(
            pulp.PULP_CBC_CMD(msg=False)
        )

        if pulp.LpStatus[status] == "Infeasible":
            return LPResult("infeasible")

        if pulp.LpStatus[status] != "Optimal":
            return LPResult("unknown")

        # Check whether every variable is integral
        tolerance = 1e-6
        integral = all(
            abs(pulp.value(x[r][c][v]) -
                round(pulp.value(x[r][c][v]))) < tolerance
            for r in cells
            for c in cells
            for v in digits
        )

        if not integral:
            return LPResult("feasible", integral=False)

        # Extract the integral solution
        # This is an interesting thing, should we not just return this as the solution?
        # Are there situations where this could not return the final solution?
        solution = tuple(
            tuple(
                next(
                    v for v in digits
                    if pulp.value(x[r][c][v]) > 0.5
                )
                for c in cells
            )
            for r in cells
        )

        # Just taking a peek
        print(f"status = {status}; integral = {integral}; solution = {solution}")
        return LPResult(
            status="feasible",
            integral=True,
            solution=solution
        )
