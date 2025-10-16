# Guía Rápida de Uso - AMG-MC

## 🚀 Inicio Rápido (2 minutos)

### Instalación Express

Abre PowerShell en el directorio del proyecto y ejecuta:

```powershell
.\install_windows.ps1
```

¡Eso es todo! El script instalará y configurará todo automáticamente.

---

## 📖 Uso Básico

### 1. Ejecutar Demo

```powershell
python scripts\run_demo.py
```

**Salida esperada:**
```
pi (power method) sum: 1.0
LGMRES info: {'info': 0, 'converged': True}
Residual norm: 3.00e-16
```

### 2. Medir Rendimiento

```powershell
python scripts\benchmark.py
```

**Salida esperada:**
```
============================================================
BENCHMARK DE RENDIMIENTO - AMG-MC
============================================================
Sistema: Windows 11
Python: 3.13.2
NumPy: 2.3.1

Tamaño     Build (ms)   Power (ms)   Solve (ms)   Total (ms)
------------------------------------------------------------
10         0.29         0.29         0.41         1.97
50         0.19         0.22         0.24         4.83
100        0.28         0.22         0.24         7.17
```

---

## 💻 Uso en tu Código

### Ejemplo Completo

```python
import numpy as np
from amgmc.markov import (
    build_transition_matrix,
    stationary_distribution_power,
    build_singular_system
)
from amgmc.hierarchy import build_amg_hierarchy
from amgmc.preconditioner import SVDBasedPreconditioner
from amgmc.solvers import solve_singular_system_lgmres, residual_norm

# 1. Define tu matriz de transición
P_dense = np.array([
    [0.10, 0.30, 0.20, 0.20, 0.20],
    [0.25, 0.10, 0.25, 0.20, 0.20],
    [0.20, 0.20, 0.10, 0.30, 0.20],
    [0.20, 0.25, 0.20, 0.10, 0.25],
    [0.25, 0.20, 0.25, 0.20, 0.10],
])

# 2. Construye la matriz sparse
P = build_transition_matrix(P_dense)

# 3. Calcula la distribución estacionaria (método de potencias)
pi = stationary_distribution_power(P)
print(f"Distribución estacionaria: {pi}")
print(f"Suma: {pi.sum()}")  # Debe ser 1.0

# 4. Construye el sistema singular (I - P)
A = build_singular_system(P)

# 5. Construye la jerarquía AMG (opcional)
hierarchy = build_amg_hierarchy(A, max_levels=3)
print(f"Niveles AMG: {len(hierarchy.levels)}")

# 6. Crea el precondicionador SVD
M = SVDBasedPreconditioner(A).as_linear_operator()

# 7. Resuelve el sistema lineal
y = np.random.rand(A.shape[0])
b = A @ y
x, info = solve_singular_system_lgmres(A, b, M=M, tol=1e-12, maxit=5000)

# 8. Verifica la solución
print(f"Convergencia: {info['converged']}")
print(f"Residual: {residual_norm(A, x, b):.2e}")
```

---

## 🔧 Configuración Avanzada

### Activar Multi-threading Manual

Si quieres controlar el número de threads manualmente:

```powershell
# En PowerShell
$cpuCount = 8  # o el número que prefieras
$env:MKL_NUM_THREADS = $cpuCount
$env:OMP_NUM_THREADS = $cpuCount
$env:NUMEXPR_NUM_THREADS = $cpuCount
```

### Habilitar AVX2 (si tu CPU lo soporta)

```powershell
$env:MKL_ENABLE_INSTRUCTIONS = "AVX2"
```

Para verificar si tu CPU soporta AVX2:

```powershell
Get-WmiObject -Class Win32_Processor | Select-Object Name
```

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Cadena de Markov Simple

```python
from amgmc.markov import build_transition_matrix, stationary_distribution_power
import numpy as np

# Matriz de transición 3x3
P_dense = [[0.7, 0.2, 0.1],
           [0.3, 0.4, 0.3],
           [0.2, 0.3, 0.5]]

P = build_transition_matrix(P_dense)
pi = stationary_distribution_power(P)

print("Distribución estacionaria:", pi)
# Output: [0.4375 0.3125 0.25  ]
```

### Ejemplo 2: Sistema Grande con Precondicionador

```python
from amgmc.markov import build_transition_matrix, build_singular_system
from amgmc.preconditioner import SVDBasedPreconditioner
from amgmc.solvers import solve_singular_system_lgmres
import numpy as np

# Matriz grande (100x100)
n = 100
P_dense = np.random.rand(n, n)
P = build_transition_matrix(P_dense)
A = build_singular_system(P)

# Con precondicionador
M = SVDBasedPreconditioner(A).as_linear_operator()
b = np.random.rand(n)
x, info = solve_singular_system_lgmres(A, b, M=M)

print(f"Convergió: {info['converged']}")
```

### Ejemplo 3: Benchmarking Personalizado

```python
import time
from amgmc.markov import build_transition_matrix
import numpy as np

# Medir tiempo de construcción
sizes = [10, 50, 100, 200]

for n in sizes:
    P_dense = np.random.rand(n, n)
    
    start = time.perf_counter()
    P = build_transition_matrix(P_dense)
    elapsed = time.perf_counter() - start
    
    print(f"Matriz {n}x{n}: {elapsed*1000:.2f} ms")
```

---

## 🐛 Troubleshooting

### Problema: "No module named 'amgmc'"

**Solución:**
```powershell
pip install -e .
```

O temporalmente:
```powershell
$env:PYTHONPATH = "$PWD\src"
```

### Problema: Script PowerShell no ejecuta

**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: Rendimiento bajo

**Verificar:**
1. Variables de entorno configuradas
2. NumPy usando MKL (no OpenBLAS básico)
3. Todos los núcleos del CPU siendo usados

**Diagnosticar:**
```powershell
python scripts\benchmark.py
```

### Problema: Numba no instala

Numba es opcional. El código funcionará sin él, solo será un poco más lento en algunas operaciones.

**Intentar:**
```powershell
pip install numba --no-cache-dir
```

Si falla, continuar sin Numba - no es crítico.

---

## 📚 Documentación Adicional

- **README.md**: Documentación completa e instrucciones de instalación
- **OPTIMIZATIONS.md**: Detalles técnicos de las optimizaciones
- **CHANGELOG.md**: Resumen de todos los cambios y mejoras
- Este archivo: Guía rápida de uso

---

## 🎯 Comandos Útiles

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Desactivar entorno virtual
deactivate

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Reinstalar paquete
pip install -e . --force-reinstall --no-deps

# Ejecutar demo
python scripts\run_demo.py

# Ejecutar benchmarks
python scripts\benchmark.py

# Ver versiones instaladas
pip list

# Limpiar cache de Python
python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python -Bc "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
```

---

## ✅ Verificación de Instalación

Ejecuta estos comandos para verificar que todo está bien:

```powershell
# 1. Verificar Python
python --version

# 2. Verificar NumPy
python -c "import numpy; print(f'NumPy {numpy.__version__}')"

# 3. Verificar SciPy
python -c "import scipy; print(f'SciPy {scipy.__version__}')"

# 4. Verificar paquete amgmc
python -c "import amgmc; print('amgmc OK')"

# 5. Ejecutar demo
python scripts\run_demo.py
```

Si todos estos comandos funcionan, ¡estás listo!

---

## 📞 Contacto y Soporte

Este es un proyecto académico. Para preguntas o problemas:

1. Revisa la documentación en README.md
2. Consulta OPTIMIZATIONS.md para detalles técnicos
3. Ejecuta el benchmark para diagnosticar problemas

---

**¡Disfruta usando AMG-MC!** 🎉
