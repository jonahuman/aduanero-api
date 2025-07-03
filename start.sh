#!/bin/bash
echo "🚀 Iniciando API Sistema Aduanero..."

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "🔧 Activando entorno virtual..."
    source .venv/Scripts/activate
else
    echo "⚠️ No se encontró .venv, usando Python global"
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Inicializar base de datos
echo "🔧 Inicializando base de datos..."
python init_db.py

# Iniciar servidor
echo "🚀 Iniciando servidor en puerto 3000..."
python app.py