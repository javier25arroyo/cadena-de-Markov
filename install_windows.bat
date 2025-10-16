@echo off
REM Script de instalación rápida para Windows (CMD)
REM Ejecutar como: install_windows.bat

echo ============================================================
echo Instalación Rápida de AMG-MC para Windows
echo ============================================================
echo.

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Crear entorno virtual si no existe
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
    echo Entorno virtual creado
) else (
    echo Entorno virtual ya existe
)
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Actualizar pip
echo.
echo Actualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -r requirements.txt --quiet
echo Dependencias instaladas
echo.

REM Instalar paquete
echo Instalando paquete amgmc...
pip install -e . --quiet
echo Paquete instalado
echo.

REM Configurar variables de entorno
echo Configurando variables de entorno...
for /f %%i in ('wmic cpu get NumberOfLogicalProcessors /value ^| find "="') do set %%i
set MKL_NUM_THREADS=%NumberOfLogicalProcessors%
set OMP_NUM_THREADS=%NumberOfLogicalProcessors%
set NUMEXPR_NUM_THREADS=%NumberOfLogicalProcessors%
set MKL_DYNAMIC=TRUE
echo Variables configuradas para %NumberOfLogicalProcessors% threads
echo.

REM Ejecutar demo
echo Ejecutando demo...
set PYTHONPATH=%CD%\src
python scripts\run_demo.py
echo.

REM Resumen
echo ============================================================
echo Instalación completada exitosamente
echo ============================================================
echo.
echo Para ejecutar el demo nuevamente:
echo   python scripts\run_demo.py
echo.
echo Para ejecutar benchmarks:
echo   python scripts\benchmark.py
echo.
echo Para desactivar el entorno virtual:
echo   deactivate
echo.
pause
