import numpy as np
from amgmc.markov import build_transition_matrix, stationary_distribution_power, build_singular_system
from amgmc.hierarchy import build_amg_hierarchy
from amgmc.preconditioner import SVDBasedPreconditioner
from amgmc.solvers import solve_singular_system_lgmres, residual_norm


def main():
    P_dense = np.array([
        [0.10, 0.30, 0.20, 0.20, 0.20],
        [0.25, 0.10, 0.25, 0.20, 0.20],
        [0.20, 0.20, 0.10, 0.30, 0.20],
        [0.20, 0.25, 0.20, 0.10, 0.25],
        [0.25, 0.20, 0.25, 0.20, 0.10],
    ])
    P = build_transition_matrix(P_dense)
    A = build_singular_system(P)

    pi = stationary_distribution_power(P)
    print("pi (power method) sum:", pi.sum())

    hierarchy = build_amg_hierarchy(A)
    M = SVDBasedPreconditioner(A).as_linear_operator()

    y = np.random.rand(A.shape[0])
    b = A @ y
    x, info = solve_singular_system_lgmres(A, b, M=M, tol=1e-12, maxit=5000)
    print("LGMRES info:", info)
    print("Residual norm:", residual_norm(A, x, b))

if __name__ == "__main__":
    main()
