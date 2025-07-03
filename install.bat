@echo off
echo ========================================
echo    INSTALACION API SISTEMA ADUANERO
echo ========================================
echo.

echo 1. Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo 2. Activando entorno virtual...
call venv\Scripts\activate.bat

echo 3. Actualizando pip...
python -m pip install --upgrade pip

echo 4. Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo 5. Creando directorio de uploads...
if not exist "uploads" mkdir uploads

echo.
echo ========================================
echo        INSTALACION COMPLETADA
echo ========================================
echo.
echo Para ejecutar la API:
echo   1. Activar entorno: venv\Scripts\activate
echo   2. Ejecutar servidor: python run.py
echo.
echo Credenciales por defecto:
echo   Email: admin@aduana.gov
echo   Password: admin123
echo.
echo API estará disponible en: http://localhost:5000
echo.
pause