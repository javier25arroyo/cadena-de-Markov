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
    n = A.shape[0]
    m = max(1, int(n*ratio))
    rng = np.random.default_rng(42)
    groups = rng.integers(low=0, high=m, size=n)
    data, rows, cols = [], [], []
    counts = np.bincount(groups, minlength=m)
    for i in range(n):
        g = groups[i]
        rows.append(i); cols.append(g); data.append(1.0/max(1, counts[g]))
    P_op = sp.csr_matrix((data, (rows, cols)), shape=(n, m))
    R_op = P_op.transpose().tocsr()
    A_c = R_op @ A @ P_op
    return A_c.tocsr(), P_op.tocsr(), R_op.tocsr()


def build_amg_hierarchy(A, max_levels=3):
    levels = []
    A_curr = A.tocsr()
    levels.append(AMGLevel(A=A_curr, P_op=sp.identity(A_curr.shape[0], format='csr'), R_op=sp.identity(A_curr.shape[0], format='csr')))
    for _ in range(1, max_levels):
        if A_curr.shape[0] <= 4:
            break
        A_c, P_op, R_op = naive_aggregate_coarsening(A_curr, ratio=0.5)
        levels.append(AMGLevel(A=A_c, P_op=P_op, R_op=R_op))
        A_curr = A_c
    return AMGHierarchy(levels=levels)
