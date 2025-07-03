@echo off
echo ========================================
echo    API Sistema Aduanero - Servidor
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️ No se encontro .venv, usando Python global
)

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r requirements.txt

REM Inicializar base de datos
echo 🔧 Inicializando base de datos...
python init_db.py

REM Iniciar servidor
echo 🚀 Iniciando servidor...
python app.py

pause