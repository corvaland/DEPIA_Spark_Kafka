#!/bin/bash

# Script de configuración inicial para DEPIA Módulo 5
# Este script configura el entorno necesario para ejecutar el proyecto

echo "==================================="
echo "DEPIA Módulo 5 - Setup Script"
echo "==================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${YELLOW}[1/5]${NC} Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python encontrado: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 no encontrado. Por favor instala Python 3.8 o superior."
    exit 1
fi

# Verificar Java
echo -e "${YELLOW}[2/5]${NC} Verificando Java..."
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1)
    echo -e "${GREEN}✓${NC} Java encontrado: $JAVA_VERSION"
else
    echo -e "${RED}✗${NC} Java no encontrado. Spark requiere Java 8 u 11."
    echo "   Instala Java con: sudo apt-get install openjdk-11-jdk"
    exit 1
fi

# Crear entorno virtual
echo -e "${YELLOW}[3/5]${NC} Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Entorno virtual creado"
else
    echo -e "${GREEN}✓${NC} Entorno virtual ya existe"
fi

# Activar entorno virtual e instalar dependencias
echo -e "${YELLOW}[4/5]${NC} Instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencias instaladas"

# Crear directorios necesarios
echo -e "${YELLOW}[5/5]${NC} Creando directorios..."
mkdir -p data logs
echo -e "${GREEN}✓${NC} Directorios creados"

echo ""
echo -e "${GREEN}==================================="
echo "✓ Setup completado exitosamente"
echo "===================================${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Activa el entorno virtual:"
echo "   source venv/bin/activate"
echo ""
echo "2. Asegúrate de que Kafka esté corriendo:"
echo "   # Iniciar Zookeeper"
echo "   bin/zookeeper-server-start.sh config/zookeeper.properties"
echo "   # Iniciar Kafka"
echo "   bin/kafka-server-start.sh config/server.properties"
echo ""
echo "3. Crea los tópicos de Kafka:"
echo "   kafka-topics.sh --create --topic input_topic \\"
echo "       --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1"
echo "   kafka-topics.sh --create --topic output_topic \\"
echo "       --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1"
echo ""
echo "4. Ejecuta el productor:"
echo "   python src/kafka_producer.py"
echo ""
echo "5. En otra terminal, ejecuta el consumidor:"
echo "   python src/spark_streaming_consumer.py"
echo ""
