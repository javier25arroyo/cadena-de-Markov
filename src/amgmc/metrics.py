import numpy as np

def l1_error(x, y):
    return float(np.linalg.norm(x - y, 1))

def l2_error(x, y):
    return float(np.linalg.norm(x - y, 2))
