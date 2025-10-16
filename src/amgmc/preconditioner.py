from dataclasses import dataclass
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

@dataclass
class SVDBasedPreconditioner:
    A: sp.csr_matrix
    k: int = 4
    reg: float = 1e-8
    _A_pinv: np.ndarray = None  # Cache de la pseudo-inversa
    
    def __post_init__(self):
        """Pre-calcula la pseudo-inversa para mejor rendimiento."""
        A_dense = self.A.toarray()
        
        # SVD con mejores opciones de rendimiento
        U, s, Vt = np.linalg.svd(A_dense, full_matrices=False, hermitian=False)
        
        # Vectorización de la inversión de valores singulares
        s_inv = np.where(s > self.reg, 1.0 / s, 0.0)
        
        # Pre-cálculo de la pseudo-inversa (más eficiente que recalcular cada vez)
        self._A_pinv = (Vt.T * s_inv) @ U.T
    
    def _approx_inverse_with_svd(self, b):
        """Aplica la pseudo-inversa pre-calculada."""
        return self._A_pinv @ b

    def as_linear_operator(self):
        """Retorna un operador lineal optimizado para usar como precondicionador."""
        n = self.A.shape[0]
        
        def matvec(v):
            # Conversión eficiente a array
            v_arr = np.asarray(v, dtype=np.float64)
            return self._approx_inverse_with_svd(v_arr)
        
        return spla.LinearOperator(
            (n, n), 
            matvec=matvec, 
            dtype=np.float64
        )
