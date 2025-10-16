import numpy as np
import scipy.sparse.linalg as spla

def solve_singular_system_lgmres(A, b, M=None, tol=1e-10, maxit=10000):
    x, info = spla.lgmres(A, b, M=M, atol=0.0, tol=tol, maxiter=maxit)
    return x, {"info": info}

def residual_norm(A, x, b, ord=2):
    r = A @ x - b
    return float(np.linalg.norm(r, ord=ord))
