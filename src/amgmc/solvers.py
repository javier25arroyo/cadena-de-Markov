import numpy as np
import scipy.sparse.linalg as spla

def solve_singular_system_lgmres(A, b, M=None, tol=1e-10, maxit=10000):
    """
    Resuelve un sistema singular usando LGMRES con precondicionador.
    Optimizado para rendimiento en Windows.
    """
    # Configuración optimizada de LGMRES
    # Nota: scipy usa 'atol' y 'rtol' en lugar de 'tol'
    x, info = spla.lgmres(
        A, 
        b, 
        M=M, 
        atol=tol,     # Tolerancia absoluta
        rtol=0.0,     # Tolerancia relativa (usamos solo absoluta)
        maxiter=maxit,
        inner_m=30,   # Tamaño óptimo para memoria cache
        outer_k=3     # Balance entre memoria y convergencia
    )
    return x, {"info": info, "converged": info == 0}

def residual_norm(A, x, b, ord=2):
    """Calcula la norma del residual de forma eficiente."""
    # Evita copia innecesaria usando operaciones in-place cuando sea posible
    r = A @ x
    r -= b
    return float(np.linalg.norm(r, ord=ord))
