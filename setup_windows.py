# Script de instalación optimizada para Windows
# Ejecutar como: python setup_windows.py

import os
import sys
import subprocess
import platform

def print_section(title):
    """Imprime un título de sección."""
    print("\n" + "="*60)
    print(title)
    print("="*60)

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    print_section("Verificando versión de Python")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        sys.exit(1)
    
    print("✓ Versión de Python compatible")

def check_windows():
    """Verifica que el sistema sea Windows."""
    print_section("Verificando sistema operativo")
    if platform.system() != 'Windows':
        print("⚠ Advertencia: Este script está optimizado para Windows")
    else:
        print(f"✓ Sistema: {platform.system()} {platform.release()}")

def upgrade_pip():
    """Actualiza pip a la última versión."""
    print_section("Actualizando pip")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print("✓ pip actualizado")

def install_requirements():
    """Instala las dependencias del proyecto."""
    print_section("Instalando dependencias")
    
    # Instalar NumPy primero (algunas librerías dependen de él)
    print("\nInstalando NumPy...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy>=1.26"])
    
    # Instalar SciPy
    print("\nInstalando SciPy...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy>=1.11"])
    
    # Instalar Numba para optimizaciones JIT
    print("\nInstalando Numba...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numba>=0.58.0"])
    
    # Instalar threadpoolctl para control de threads (opcional pero recomendado)
    print("\nInstalando threadpoolctl (opcional)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "threadpoolctl"])
        print("✓ threadpoolctl instalado")
    except:
        print("⚠ threadpoolctl no se pudo instalar (opcional)")
    
    print("\n✓ Todas las dependencias instaladas")

def install_package():
    """Instala el paquete en modo desarrollo."""
    print_section("Instalando paquete amgmc")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    print("✓ Paquete instalado en modo desarrollo")

def configure_environment():
    """Configura variables de entorno para mejor rendimiento."""
    print_section("Configurando variables de entorno")
    
    cpu_count = os.cpu_count() or 4
    
    # Configurar variables de entorno para esta sesión
    env_vars = {
        'MKL_NUM_THREADS': str(cpu_count),
        'NUMEXPR_NUM_THREADS': str(cpu_count),
        'OMP_NUM_THREADS': str(cpu_count),
        'OPENBLAS_NUM_THREADS': str(cpu_count),
        'MKL_DYNAMIC': 'TRUE',
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"  {key} = {value}")
    
    print(f"\n✓ Variables configuradas para {cpu_count} threads")

def run_tests():
    """Ejecuta el script de demostración para verificar la instalación."""
    print_section("Verificando instalación")
    
    try:
        print("\nEjecutando demo...")
        subprocess.check_call([sys.executable, "scripts/run_demo.py"])
        print("\n✓ Demo ejecutado correctamente")
    except Exception as e:
        print(f"\n⚠ Error al ejecutar demo: {e}")

def print_summary():
    """Imprime un resumen de la instalación."""
    print_section("Instalación completada")
    print("""
✓ Python verificado
✓ Dependencias instaladas
✓ Paquete amgmc instalado
✓ Configuración optimizada

Próximos pasos:
  1. Para ejecutar el demo:
     python scripts\\run_demo.py
  
  2. Para ejecutar benchmarks:
     python scripts\\benchmark.py
  
  3. Para usar el paquete en tu código:
     from amgmc import markov, hierarchy, preconditioner, solvers

Para mejores resultados, asegúrate de que tu CPU soporte instrucciones AVX2.
    """)

def main():
    """Función principal de instalación."""
    print_section("Instalación de AMG-MC para Windows")
    
    try:
        check_python_version()
        check_windows()
        upgrade_pip()
        install_requirements()
        install_package()
        configure_environment()
        run_tests()
        print_summary()
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la instalación: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
