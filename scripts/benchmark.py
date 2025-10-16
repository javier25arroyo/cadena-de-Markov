# Script de benchmarking para medir el rendimiento
import time
import numpy as np
from amgmc.markov import build_transition_matrix, stationary_distribution_power, build_singular_system
from amgmc.hierarchy import build_amg_hierarchy
from amgmc.preconditioner import SVDBasedPreconditioner
from amgmc.solvers import solve_singular_system_lgmres, residual_norm


def benchmark_markov_chain(size=100):
    """Benchmark de cadena de Markov de tamaño variable."""
    print(f"\n{'='*60}")
    print(f"Benchmark: Cadena de Markov {size}x{size}")
    print(f"{'='*60}")
    
    # Generar matriz de transición aleatoria
    np.random.seed(42)
    P_dense = np.random.rand(size, size)
    
    # Test 1: Construcción de matriz de transición
    start = time.perf_counter()
    P = build_transition_matrix(P_dense)
    t_build = time.perf_counter() - start
    print(f"Construcción de matriz de transición: {t_build*1000:.2f} ms")
    
    # Test 2: Distribución estacionaria (método de potencias)
    start = time.perf_counter()
    pi = stationary_distribution_power(P, maxit=1000, tol=1e-10)
    t_power = time.perf_counter() - start
    print(f"Distribución estacionaria (power method): {t_power*1000:.2f} ms")
    print(f"  Sum(pi) = {pi.sum():.10f}")
    
    # Test 3: Construcción de sistema singular
    start = time.perf_counter()
    A = build_singular_system(P)
    t_singular = time.perf_counter() - start
    print(f"Construcción de sistema singular: {t_singular*1000:.2f} ms")
    
    # Test 4: Construcción de jerarquía AMG
    start = time.perf_counter()
    hierarchy = build_amg_hierarchy(A, max_levels=3)
    t_hierarchy = time.perf_counter() - start
    print(f"Construcción de jerarquía AMG: {t_hierarchy*1000:.2f} ms")
    print(f"  Niveles: {len(hierarchy.levels)}")
    
    # Test 5: Construcción de precondicionador SVD
    start = time.perf_counter()
    M = SVDBasedPreconditioner(A).as_linear_operator()
    t_precond = time.perf_counter() - start
    print(f"Construcción de precondicionador SVD: {t_precond*1000:.2f} ms")
    
    # Test 6: Solución del sistema con LGMRES
    y = np.random.rand(A.shape[0])
    b = A @ y
    start = time.perf_counter()
    x, info = solve_singular_system_lgmres(A, b, M=M, tol=1e-10, maxit=5000)
    t_solve = time.perf_counter() - start
    res = residual_norm(A, x, b)
    print(f"Solución con LGMRES: {t_solve*1000:.2f} ms")
    print(f"  Iteraciones: {info}")
    print(f"  Residual: {res:.2e}")
    
    # Resumen
    total_time = t_build + t_power + t_singular + t_hierarchy + t_precond + t_solve
    print(f"\nTiempo total: {total_time*1000:.2f} ms")
    
    return {
        'size': size,
        'build': t_build,
        'power': t_power,
        'singular': t_singular,
        'hierarchy': t_hierarchy,
        'precond': t_precond,
        'solve': t_solve,
        'total': total_time
    }


def main():
    print("\n" + "="*60)
    print("BENCHMARK DE RENDIMIENTO - AMG-MC")
    print("Optimizado para Windows")
    print("="*60)
    
    # Información del sistema
    import platform
    print(f"\nSistema: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print(f"NumPy: {np.__version__}")
    
    # Ejecutar benchmarks de diferentes tamaños
    sizes = [10, 50, 100]
    results = []
    
    for size in sizes:
        result = benchmark_markov_chain(size)
        results.append(result)
    
    # Comparación de resultados
    print(f"\n{'='*60}")
    print("RESUMEN DE BENCHMARKS")
    print(f"{'='*60}")
    print(f"{'Tamaño':<10} {'Build (ms)':<12} {'Power (ms)':<12} {'Solve (ms)':<12} {'Total (ms)':<12}")
    print("-" * 60)
    for r in results:
        print(f"{r['size']:<10} {r['build']*1000:<12.2f} {r['power']*1000:<12.2f} {r['solve']*1000:<12.2f} {r['total']*1000:<12.2f}")


if __name__ == "__main__":
    main()
