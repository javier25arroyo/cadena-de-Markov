from dataclasses import dataclass
import numpy as np
import scipy.sparse as sp

@dataclass
class AMGLevel:
    A: sp.csr_matrix
    P_op: sp.csr_matrix
    R_op: sp.csr_matrix

@dataclass
class AMGHierarchy:
    levels: list


def naive_aggregate_coarsening(A, ratio=0.5):
    """Coarsening por agregación naive optimizado para Windows."""
    n = A.shape[0]
    m = max(1, int(n * ratio))
    
    # Generador de números aleatorios más eficiente
    rng = np.random.default_rng(42)
    groups = rng.integers(low=0, high=m, size=n, dtype=np.int32)
    
    # Pre-conteo para normalización
    counts = np.bincount(groups, minlength=m)
    # Evitar división por cero
    inv_counts = np.zeros_like(counts, dtype=np.float64)
    mask = counts > 0
    inv_counts[mask] = 1.0 / counts[mask]
    inv_counts[~mask] = 1.0
    
    # Construcción más eficiente de la matriz P
    data = inv_counts[groups]
    rows = np.arange(n, dtype=np.int32)
    cols = groups
    
    P_op = sp.csr_matrix((data, (rows, cols)), shape=(n, m), dtype=np.float64)
    R_op = P_op.transpose().tocsr()
    
    # Multiplicación optimizada de matrices sparse
    A_c = (R_op @ A @ P_op).tocsr()
    
    return A_c, P_op, R_op


def build_amg_hierarchy(A, max_levels=3):
    """Construye jerarquía AMG con optimizaciones para rendimiento."""
    levels = []
    A_curr = A.tocsr()
    
    # Nivel más fino
    n = A_curr.shape[0]
    identity = sp.identity(n, format='csr', dtype=np.float64)
    levels.append(AMGLevel(A=A_curr, P_op=identity, R_op=identity))
    
    # Niveles subsecuentes
    for level_idx in range(1, max_levels):
        if A_curr.shape[0] <= 4:
            break
        
        A_c, P_op, R_op = naive_aggregate_coarsening(A_curr, ratio=0.5)
        levels.append(AMGLevel(A=A_c, P_op=P_op, R_op=R_op))
        A_curr = A_c
    
    return AMGHierarchy(levels=levels)
