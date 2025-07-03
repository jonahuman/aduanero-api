@echo off
echo ========================================
echo     INICIANDO API SISTEMA ADUANERO
echo ========================================
echo.

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Iniciando servidor Flask...
echo.
echo API disponible en: http://localhost:5000
echo Frontend debe ejecutarse en: http://localhost:5173
echo.
echo Credenciales:
echo   Email: admin@aduana.gov  
echo   Password: admin123
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python run.py