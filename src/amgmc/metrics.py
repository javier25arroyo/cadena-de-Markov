import numpy as np

def l1_error(x, y):
    """Calcula el error L1 de forma optimizada."""
    return float(np.sum(np.abs(x - y)))

def l2_error(x, y):
    """Calcula el error L2 de forma optimizada."""
    diff = x - y
    return float(np.sqrt(np.dot(diff, diff)))
