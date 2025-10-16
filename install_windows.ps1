# Script de instalación rápida para Windows (PowerShell)
# Ejecutar en PowerShell: .\install_windows.ps1

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Instalación Rápida de AMG-MC para Windows" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python no está instalado o no está en PATH" -ForegroundColor Red
    Write-Host "Descarga Python desde: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host "✓ $pythonVersion" -ForegroundColor Green

# Crear entorno virtual si no existe
if (!(Test-Path ".venv")) {
    Write-Host "`nCreando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "`n✓ Entorno virtual ya existe" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "`nActivando entorno virtual..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Actualizar pip
Write-Host "`nActualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Instalar dependencias
Write-Host "`nInstalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencias instaladas" -ForegroundColor Green

# Instalar paquete
Write-Host "`nInstalando paquete amgmc..." -ForegroundColor Yellow
pip install -e . --quiet
Write-Host "✓ Paquete instalado" -ForegroundColor Green

# Configurar variables de entorno para rendimiento
Write-Host "`nConfigurando variables de entorno..." -ForegroundColor Yellow
$cpuCount = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
$env:MKL_NUM_THREADS = $cpuCount
$env:OMP_NUM_THREADS = $cpuCount
$env:NUMEXPR_NUM_THREADS = $cpuCount
$env:MKL_DYNAMIC = "TRUE"
Write-Host "✓ Variables configuradas para $cpuCount threads" -ForegroundColor Green

# Ejecutar demo
Write-Host "`nEjecutando demo..." -ForegroundColor Yellow
python scripts\run_demo.py

# Resumen
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Instalación completada exitosamente" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "Para ejecutar el demo nuevamente:" -ForegroundColor Yellow
Write-Host "  python scripts\run_demo.py`n" -ForegroundColor White

Write-Host "Para ejecutar benchmarks:" -ForegroundColor Yellow
Write-Host "  python scripts\benchmark.py`n" -ForegroundColor White

Write-Host "Para desactivar el entorno virtual:" -ForegroundColor Yellow
Write-Host "  deactivate`n" -ForegroundColor White
