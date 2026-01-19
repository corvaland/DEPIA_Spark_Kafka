# DEPIA Módulo 5: Integración Spark + Kafka

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5.0-orange.svg)](https://spark.apache.org/)
[![Kafka](https://img.shields.io/badge/Kafka-2.0+-red.svg)](https://kafka.apache.org/)

Este repositorio contiene los entregables del Módulo 5 del Diplomado en Ingeniería y Análisis de Datos (DEPIA), enfocado en la integración de Apache Spark con Apache Kafka para procesamiento de datos en tiempo real y batch.

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Ejemplos de Ejecución](#ejemplos-de-ejecución)
- [Componentes](#componentes)
- [Resultados Esperados](#resultados-esperados)

## 📖 Descripción del Proyecto

Este proyecto demuestra la integración entre Apache Spark y Apache Kafka para el procesamiento de flujos de datos en tiempo real. Se implementan tres componentes principales:

1. **Productor de Kafka**: Genera datos simulados de sensores (temperatura, humedad, presión)
2. **Consumidor con Spark Streaming**: Procesa datos en tiempo real con agregaciones por ventanas de tiempo
3. **Procesador Batch**: Genera reportes estadísticos sobre datos históricos

## 🏗️ Arquitectura

```
┌─────────────────┐
│  Kafka Producer │  (Genera datos de sensores)
│  kafka_producer │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Kafka Topic    │  (input_topic)
│  Input Stream   │
└────────┬────────┘
         │
         ├──────────────────────┬────────────────────┐
         ▼                      ▼                    ▼
┌──────────────────┐   ┌───────────────────┐   ┌──────────────────┐
│ Spark Streaming  │   │  Spark Batch      │   │ Otros Consumers  │
│ (Real-time)      │   │  (Historical)     │   │                  │
└────────┬─────────┘   └─────────┬─────────┘   └──────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐   ┌───────────────────┐
│  Kafka Topic    │   │  Archivos CSV/    │
│  (output_topic) │   │  Parquet Reports  │
└─────────────────┘   └───────────────────┘
```

### Flujo de Datos

1. **Ingesta**: El productor genera eventos de sensores y los publica en `input_topic`
2. **Procesamiento Streaming**: Spark Structured Streaming consume los datos, aplica agregaciones por ventanas de tiempo (5 minutos) y calcula estadísticas promedio
3. **Procesamiento Batch**: Lee un lote completo de datos históricos y genera reportes estadísticos por sensor
4. **Salida**: Resultados se escriben en consola, tópicos de Kafka o archivos

## 📁 Estructura del Proyecto

```
DEPIA_Spark_Kafka/
│
├── src/                          # Código fuente
│   ├── kafka_producer.py         # Productor de mensajes Kafka
│   ├── spark_streaming_consumer.py  # Consumidor streaming con Spark
│   └── spark_batch_processor.py  # Procesador batch con Spark
│
├── config/                       # Archivos de configuración
│   └── config.env               # Variables de entorno
│
├── data/                        # Directorio para datos y reportes
│   └── .gitkeep
│
├── logs/                        # Logs de ejecución
│   └── .gitkeep
│
├── requirements.txt             # Dependencias Python
├── .gitignore                  # Archivos a ignorar en Git
└── README.md                   # Este archivo
```

## 🔧 Requisitos Previos

### Software Necesario

- **Python 3.8+**
- **Java 8 o 11** (requerido por Spark)
- **Apache Kafka 2.0+** (servidor corriendo localmente o remoto)
- **Apache Spark 3.5.0+** (se instala con PySpark)

### Verificación de Java

```bash
java -version
```

### Instalación de Kafka (opcional si no está instalado)

Para sistemas Unix/Linux/Mac:

```bash
# Descargar Kafka
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xzf kafka_2.13-3.6.0.tgz
cd kafka_2.13-3.6.0

# Iniciar Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties &

# Iniciar Kafka Server
bin/kafka-server-start.sh config/server.properties &
```

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/corvaland/DEPIA_Spark_Kafka.git
cd DEPIA_Spark_Kafka
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Preparación: Crear tópicos de Kafka

Antes de ejecutar los scripts, crear los tópicos necesarios:

```bash
# Tópico de entrada
kafka-topics.sh --create --topic input_topic \
    --bootstrap-server localhost:9092 \
    --partitions 3 \
    --replication-factor 1

# Tópico de salida (opcional)
kafka-topics.sh --create --topic output_topic \
    --bootstrap-server localhost:9092 \
    --partitions 3 \
    --replication-factor 1

# Verificar tópicos creados
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Ejecución de Componentes

#### 1. Productor de Kafka

Genera datos simulados de sensores:

```bash
python src/kafka_producer.py
```

Este script:
- Genera 100 mensajes (configurable)
- Envía un mensaje cada 2 segundos
- Simula datos de 10 sensores con temperatura, humedad y presión

#### 2. Consumidor con Spark Streaming

Procesa datos en tiempo real:

```bash
python src/spark_streaming_consumer.py
```

Este script:
- Lee datos desde `input_topic`
- Aplica agregaciones por ventana de 5 minutos
- Calcula promedios de temperatura, humedad y presión por sensor
- Muestra resultados en consola

#### 3. Procesador Batch

Genera reportes estadísticos:

```bash
python src/spark_batch_processor.py
```

Este script:
- Lee todos los datos disponibles en el tópico
- Genera estadísticas (promedio, mínimo, máximo) por sensor
- Guarda el reporte en formato CSV en `data/sensor_report/`

## 📊 Ejemplos de Ejecución

### Ejemplo 1: Pipeline Completo

Terminal 1 - Productor:
```bash
$ python src/kafka_producer.py
Iniciando productor de datos para el tópico 'input_topic'...
Presiona Ctrl+C para detener
Mensaje enviado a input_topic partición 0 offset 0
Mensaje 1: {'timestamp': '2024-01-19T10:30:45.123456', 'sensor_id': 'sensor_3', ...}
```

Terminal 2 - Streaming:
```bash
$ python src/spark_streaming_consumer.py
Iniciando procesamiento con Spark Structured Streaming...
Leyendo datos desde el tópico 'input_topic'...
Procesamiento iniciado. Esperando datos...

-------------------------------------------
Batch: 1
-------------------------------------------
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
|window                                    |sensor_id |avg_temperature   |avg_humidity      |avg_pressure      |num_readings |
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_1  |25.34             |65.22             |1012.45           |15           |
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_2  |23.45             |70.15             |1015.20           |18           |
```

### Ejemplo 2: Reporte Batch

```bash
$ python src/spark_batch_processor.py
=== Procesamiento Batch con Spark ===
Leyendo datos desde Kafka: input_topic

Total de registros leídos: 100

--- Generando reporte por sensor ---
+----------+--------------+-----------------+-----------------+-----------------+
|sensor_id |total_readings|avg_temperature  |min_temperature  |max_temperature  |...
+----------+--------------+-----------------+-----------------+-----------------+
|sensor_1  |10            |24.56            |18.30            |32.10            |...
|sensor_2  |8             |25.12            |19.45            |31.20            |...

✓ Procesamiento completado exitosamente
Reporte guardado en: data/sensor_report
```

## 🔍 Componentes

### 1. kafka_producer.py

**Clase Principal**: `DataProducer`

**Métodos clave**:
- `generate_sample_data()`: Genera datos aleatorios de sensores
- `send_data(data)`: Envía un mensaje a Kafka
- `produce_continuous(interval, num_messages)`: Producción continua de mensajes

**Configuración**:
- Servidor Kafka: `localhost:9092`
- Tópico: `input_topic`
- Intervalo: 2 segundos

### 2. spark_streaming_consumer.py

**Clase Principal**: `SparkKafkaProcessor`

**Métodos clave**:
- `read_from_kafka(topic)`: Lee stream desde Kafka
- `process_data(df)`: Aplica transformaciones y agregaciones
- `write_to_console(df)`: Escribe resultados en consola
- `write_to_kafka(df, topic)`: Escribe resultados a Kafka

**Características**:
- Ventana de tiempo: 5 minutos
- Watermark: 10 minutos
- Modo de salida: Update

### 3. spark_batch_processor.py

**Clase Principal**: `SparkBatchProcessor`

**Métodos clave**:
- `read_batch_from_kafka(kafka_servers, topic)`: Lectura batch
- `generate_report(df)`: Genera estadísticas agregadas
- `save_report(df, output_path)`: Guarda reporte en disco

**Formatos de salida soportados**:
- CSV
- Parquet
- JSON

## 📈 Resultados Esperados

### Métricas Calculadas

#### Streaming (por ventana de 5 minutos):
- Temperatura promedio por sensor
- Humedad promedio por sensor
- Presión promedio por sensor
- Número de lecturas por sensor

#### Batch (histórico completo):
- Total de lecturas por sensor
- Temperatura: promedio, mínima, máxima
- Humedad: promedio, mínima, máxima
- Presión: promedio, mínima, máxima

### Archivos Generados

- `data/sensor_report/*.csv`: Reporte estadístico en CSV
- Checkpoints en `/tmp/spark_checkpoint_*`: Estados de Spark Streaming

## 🔒 Configuración Avanzada

### Ajustar parámetros en config.env

```bash
# Servidores Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Tópicos
KAFKA_INPUT_TOPIC=input_topic
KAFKA_OUTPUT_TOPIC=output_topic

# Spark
SPARK_APP_NAME=DEPIA_Spark_Kafka_Integration
CHECKPOINT_LOCATION=/tmp/spark_checkpoint

# Procesamiento
BATCH_DURATION=10
```

### Escalabilidad

Para ambientes productivos, considerar:

1. **Múltiples particiones**: Aumentar el número de particiones en Kafka
2. **Paralelismo de Spark**: Ajustar `spark.default.parallelism`
3. **Memoria**: Configurar `spark.executor.memory` y `spark.driver.memory`
4. **Checkpointing**: Usar almacenamiento distribuido (HDFS, S3) para checkpoints

## 🛠️ Solución de Problemas

### Error: "Kafka server not found"
- Verificar que Kafka esté corriendo: `netstat -an | grep 9092`
- Revisar configuración de `bootstrap.servers`

### Error: "Java not found"
- Instalar Java: `sudo apt-get install openjdk-11-jdk`
- Configurar JAVA_HOME

### Error: "Checkpoint directory already exists"
- Eliminar checkpoints antiguos: `rm -rf /tmp/spark_checkpoint_*`

## 📚 Referencias

- [Apache Spark Structured Streaming + Kafka](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
- [Kafka Python Client](https://kafka-python.readthedocs.io/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)

## 👥 Autor

Proyecto desarrollado como entregable del Módulo 5 de DEPIA (Diplomado en Ingeniería y Análisis de Datos)

## 📄 Licencia

Este proyecto es material educativo para el curso DEPIA.
