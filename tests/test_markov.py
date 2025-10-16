import numpy as np
from amgmc.markov import build_transition_matrix, stationary_distribution_power

def test_stationary_distribution_power_basic():
    P_dense = np.array([[0.5, 0.5],[0.5, 0.5]])
    P = build_transition_matrix(P_dense)
    pi = stationary_distribution_power(P, maxit=1000, tol=1e-14)
    assert np.isclose(pi.sum(), 1.0)
    assert np.all(pi >= 0)
