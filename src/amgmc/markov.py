import numpy as np
import scipy.sparse as sp

def build_transition_matrix(P_dense):
    P = np.array(P_dense, dtype=float, copy=True)
    row_sums = P.sum(axis=1, keepdims=True)
    P = P / row_sums
    return sp.csr_matrix(P)


def is_stochastic_irreducible(P, tol=1e-12):
    rowsums = np.abs(P.sum(axis=1).A.ravel() - 1.0)
    if (rowsums > 1e-10).any():
        return False
    n = P.shape[0]
    G = (P > tol).astype(int)
    vis = np.zeros(n, dtype=bool); frontier=[0]; vis[0]=True
    while frontier:
        u = frontier.pop()
        for v in G[u].indices:
            if not vis[v]: vis[v]=True; frontier.append(v)
    if not vis.all(): return False
    GT = G.transpose().tocsr()
    vis = np.zeros(n, dtype=bool); frontier=[0]; vis[0]=True
    while frontier:
        u = frontier.pop()
        for v in GT[u].indices:
            if not vis[v]: vis[v]=True; frontier.append(v)
    return vis.all()


def stationary_distribution_power(P, maxit=10000, tol=1e-12):
    import numpy as np
    PT = P.transpose().tocsr()
    n = P.shape[0]
    x = np.ones(n)/n
    for _ in range(maxit):
        x_new = PT @ x
        x_new = x_new / x_new.sum()
        if np.linalg.norm(x_new - x, 1) < tol:
            return x_new
        x = x_new
    return x


def build_singular_system(P):
    n = P.shape[0]
    I = sp.identity(n, format='csr')
    return (I - P).tocsr()
