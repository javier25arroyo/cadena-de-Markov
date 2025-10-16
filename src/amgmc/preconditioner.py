from dataclasses import dataclass
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

@dataclass
class SVDBasedPreconditioner:
    A: sp.csr_matrix
    k: int = 4
    reg: float = 1e-8

    def _approx_inverse_with_svd(self, b):
        A_dense = self.A.toarray()
        U, s, Vt = np.linalg.svd(A_dense, full_matrices=False)
        s_inv = np.array([1/x if x > self.reg else 0.0 for x in s])
        A_pinv = (Vt.T * s_inv) @ U.T
        return A_pinv @ b

    def as_linear_operator(self):
        n = self.A.shape[0]
        def matvec(v):
            return self._approx_inverse_with_svd(np.asarray(v))
        return spla.LinearOperator((n, n), matvec=matvec, dtype=float)
