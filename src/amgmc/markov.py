import numpy as np
import scipy.sparse as sp

# Numba es opcional - si está disponible, se usará para optimizaciones JIT
try:
    from numba import jit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    # Decorador dummy si Numba no está disponible
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

def build_transition_matrix(P_dense):
    """Construye matriz de transición normalizada y la convierte a formato sparse CSR."""
    P = np.asarray(P_dense, dtype=np.float64)
    # Normalización vectorizada más eficiente
    row_sums = P.sum(axis=1, keepdims=True)
    P = np.divide(P, row_sums, out=P)
    return sp.csr_matrix(P, dtype=np.float64)


def is_stochastic_irreducible(P, tol=1e-12):
    """Verifica si una matriz es estocástica e irreducible usando algoritmo BFS optimizado."""
    # Verificación rápida de estocasticidad
    rowsums = np.abs(P.sum(axis=1).A.ravel() - 1.0)
    if np.any(rowsums > 1e-10):
        return False
    
    n = P.shape[0]
    # Construcción más eficiente del grafo
    G = (P > tol).astype(np.int8)
    
    # BFS forward optimizado
    vis = np.zeros(n, dtype=np.bool_)
    vis[0] = True
    frontier = [0]
    idx = 0
    while idx < len(frontier):
        u = frontier[idx]
        idx += 1
        for v in G[u].indices:
            if not vis[v]:
                vis[v] = True
                frontier.append(v)
    
    if not np.all(vis):
        return False
    
    # BFS backward optimizado
    GT = G.transpose().tocsr()
    vis.fill(False)
    vis[0] = True
    frontier = [0]
    idx = 0
    while idx < len(frontier):
        u = frontier[idx]
        idx += 1
        for v in GT[u].indices:
            if not vis[v]:
                vis[v] = True
                frontier.append(v)
    
    return np.all(vis)


def stationary_distribution_power(P, maxit=10000, tol=1e-12):
    """Calcula la distribución estacionaria usando el método de potencias optimizado."""
    PT = P.transpose().tocsr()
    n = P.shape[0]
    x = np.ones(n, dtype=np.float64) / n
    
    # Pre-alocar para evitar creaciones repetidas
    norm_diff = np.empty(n, dtype=np.float64)
    
    for iteration in range(maxit):
        x_new = PT @ x
        # Normalización in-place
        x_sum = x_new.sum()
        x_new /= x_sum
        
        # Cálculo optimizado de convergencia
        np.subtract(x_new, x, out=norm_diff)
        if np.sum(np.abs(norm_diff)) < tol:
            return x_new
        x = x_new
    
    return x


def build_singular_system(P):
    """Construye el sistema singular (I - P) de forma eficiente."""
    n = P.shape[0]
    I = sp.identity(n, format='csr', dtype=np.float64)
    # Operación más eficiente aprovechando que P ya es CSR
    return (I - P).tocsr()
