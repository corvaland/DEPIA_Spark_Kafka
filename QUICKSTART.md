# Guía de Inicio Rápido - DEPIA Módulo 5

Esta guía te ayudará a ejecutar el proyecto en menos de 10 minutos.

## Requisitos Mínimos

- ✅ Python 3.8+
- ✅ Java 8 u 11
- ✅ Apache Kafka corriendo localmente

## Pasos de Instalación

### 1. Clonar y Configurar

```bash
# Clonar repositorio
git clone https://github.com/corvaland/DEPIA_Spark_Kafka.git
cd DEPIA_Spark_Kafka

# Ejecutar script de setup
chmod +x setup.sh
./setup.sh

# Activar entorno virtual
source venv/bin/activate
```

### 2. Iniciar Kafka (si no está corriendo)

En terminales separadas:

```bash
# Terminal 1: Zookeeper
cd kafka_2.13-3.6.0
bin/zookeeper-server-start.sh config/zookeeper.properties
```

```bash
# Terminal 2: Kafka Server
cd kafka_2.13-3.6.0
bin/kafka-server-start.sh config/server.properties
```

### 3. Crear Tópicos

```bash
cd kafka_2.13-3.6.0
bin/kafka-topics.sh --create --topic input_topic --bootstrap-server localhost:9092
bin/kafka-topics.sh --create --topic output_topic --bootstrap-server localhost:9092
```

### 4. Ejecutar el Proyecto

#### Opción A: Streaming en Tiempo Real

Terminal 1 - Productor:
```bash
python src/kafka_producer.py
```

Terminal 2 - Consumidor Streaming:
```bash
python src/spark_streaming_consumer.py
```

Deberías ver datos siendo procesados en tiempo real con agregaciones cada 5 minutos.

#### Opción B: Procesamiento Batch

Primero ejecuta el productor para generar datos:
```bash
python src/kafka_producer.py
```

Espera a que se generen algunos mensajes (al menos 30 segundos), luego ejecuta:
```bash
python src/spark_batch_processor.py
```

El reporte se guardará en `data/sensor_report/`.

## Verificación

### Verificar Kafka está funcionando:
```bash
# Listar tópicos
kafka-topics.sh --list --bootstrap-server localhost:9092

# Consumir mensajes manualmente
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic input_topic --from-beginning
```

### Ver logs de Spark:
Los logs se muestran en la consola. Para logs detallados, modificar el nivel en el código:
```python
self.spark.sparkContext.setLogLevel("INFO")  # Cambiar de WARN a INFO
```

## Solución Rápida de Problemas

| Error | Solución |
|-------|----------|
| "Connection refused to localhost:9092" | Kafka no está corriendo. Inicia Kafka y Zookeeper |
| "Java not found" | Instala Java: `sudo apt-get install openjdk-11-jdk` |
| "Module 'pyspark' not found" | Activa el entorno virtual: `source venv/bin/activate` |
| "Checkpoint already exists" | Elimina: `rm -rf /tmp/spark_checkpoint_*` |

## Estructura de Datos

Los mensajes generados tienen este formato:

```json
{
  "timestamp": "2024-01-19T10:30:45.123456",
  "sensor_id": "sensor_3",
  "temperature": 25.34,
  "humidity": 65.22,
  "pressure": 1012.45
}
```

## Resultados Esperados

### Streaming
Verás agregaciones cada 5 minutos mostrando:
- Temperatura promedio por sensor
- Humedad promedio por sensor
- Presión promedio por sensor
- Número de lecturas

### Batch
Un reporte CSV con estadísticas completas:
- Promedios, mínimos y máximos
- Total de lecturas por sensor

## ¿Necesitas Ayuda?

Consulta el `README.md` principal para documentación detallada sobre:
- Arquitectura del sistema
- Configuración avanzada
- Explicación de componentes
- Referencias y recursos adicionales
