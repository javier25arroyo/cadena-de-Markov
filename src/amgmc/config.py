# Configuración de optimización para Windows
import os
import numpy as np

# Configuración de threading para mejor rendimiento en Windows
def configure_for_windows():
    """
    Configura las variables de entorno para optimizar el rendimiento
    de NumPy/SciPy en sistemas Windows.
    """
    # Detectar número de núcleos disponibles
    cpu_count = os.cpu_count() or 4
    
    # Configurar threading para BLAS/LAPACK (MKL en Windows)
    os.environ['MKL_NUM_THREADS'] = str(cpu_count)
    os.environ['NUMEXPR_NUM_THREADS'] = str(cpu_count)
    os.environ['OMP_NUM_THREADS'] = str(cpu_count)
    os.environ['OPENBLAS_NUM_THREADS'] = str(cpu_count)
    
    # Optimizaciones específicas de MKL en Windows
    os.environ['MKL_DYNAMIC'] = 'TRUE'
    os.environ['MKL_ENABLE_INSTRUCTIONS'] = 'AVX2'  # Usar instrucciones AVX2 si están disponibles
    
    # Configurar NumPy para usar todos los hilos
    try:
        # Intenta configurar el número de hilos en tiempo de ejecución
        import threadpoolctl
        threadpoolctl.threadpool_limits(limits=cpu_count)
    except ImportError:
        pass  # threadpoolctl es opcional
    
    print(f"Configuración de rendimiento para Windows:")
    print(f"  - CPUs detectados: {cpu_count}")
    print(f"  - Threads configurados: {cpu_count}")
    print(f"  - Backend NumPy: {np.__config__.show()}")

# Configuración automática al importar
if os.name == 'nt':  # Solo en Windows
    configure_for_windows()
