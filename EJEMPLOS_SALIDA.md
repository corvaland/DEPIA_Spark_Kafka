# Ejemplos de Salida - DEPIA Módulo 5

Este documento muestra ejemplos reales de la salida esperada al ejecutar los diferentes componentes del proyecto.

## 1. Kafka Producer - Salida de Ejemplo

```
$ python src/kafka_producer.py

Iniciando productor de datos para el tópico 'input_topic'...
Presiona Ctrl+C para detener

Mensaje enviado a input_topic partición 2 offset 0
Mensaje 1: {'timestamp': '2024-01-19T10:30:45.123456', 'sensor_id': 'sensor_3', 'temperature': 25.34, 'humidity': 65.22, 'pressure': 1012.45}

Mensaje enviado a input_topic partición 0 offset 0
Mensaje 2: {'timestamp': '2024-01-19T10:30:47.234567', 'sensor_id': 'sensor_7', 'temperature': 22.15, 'humidity': 72.45, 'pressure': 1015.30}

Mensaje enviado a input_topic partición 1 offset 0
Mensaje 3: {'timestamp': '2024-01-19T10:30:49.345678', 'sensor_id': 'sensor_1', 'temperature': 28.90, 'humidity': 58.33, 'pressure': 1008.75}

...

Producción detenida por el usuario
Productor cerrado
```

## 2. Spark Streaming Consumer - Salida de Ejemplo

```
$ python src/spark_streaming_consumer.py

Iniciando procesamiento con Spark Structured Streaming...
Leyendo datos desde el tópico 'input_topic'...
Procesamiento iniciado. Esperando datos...
Presiona Ctrl+C para detener

-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
|window                                    |sensor_id |avg_temperature   |avg_humidity      |avg_pressure      |num_readings |
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
+------------------------------------------+----------+------------------+------------------+------------------+-------------+

-------------------------------------------
Batch: 1
-------------------------------------------
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
|window                                    |sensor_id |avg_temperature   |avg_humidity      |avg_pressure      |num_readings |
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_1  |25.34             |65.22             |1012.45           |15           |
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_2  |23.45             |70.15             |1015.20           |18           |
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_3  |27.89             |62.34             |1009.80           |12           |
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_4  |24.12             |68.90             |1013.55           |14           |
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_5  |26.78             |59.45             |1011.20           |16           |
+------------------------------------------+----------+------------------+------------------+------------------+-------------+

-------------------------------------------
Batch: 2
-------------------------------------------
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
|window                                    |sensor_id |avg_temperature   |avg_humidity      |avg_pressure      |num_readings |
+------------------------------------------+----------+------------------+------------------+------------------+-------------+
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_1  |25.67             |64.89             |1012.78           |28           |
|{2024-01-19 10:30:00, 2024-01-19 10:35:00}|sensor_2  |23.89             |69.54             |1014.95           |31           |
|{2024-01-19 10:35:00, 2024-01-19 10:40:00}|sensor_1  |24.45             |66.12             |1013.22           |8            |
|{2024-01-19 10:35:00, 2024-01-19 10:40:00}|sensor_3  |28.12             |61.78             |1009.45           |10           |
+------------------------------------------+----------+------------------+------------------+------------------+-------------+

...

^C
Deteniendo procesamiento...
Procesamiento detenido
```

## 3. Spark Batch Processor - Salida de Ejemplo

```
$ python src/spark_batch_processor.py

=== Procesamiento Batch con Spark ===
Leyendo datos desde Kafka: input_topic

Total de registros leídos: 100

--- Muestra de datos ---
+---------------------------+----------+---------------+-------------+-------------+
|timestamp                  |sensor_id |temperature    |humidity     |pressure     |
+---------------------------+----------+---------------+-------------+-------------+
|2024-01-19 10:30:45.123456 |sensor_3  |25.34          |65.22        |1012.45      |
|2024-01-19 10:30:47.234567 |sensor_7  |22.15          |72.45        |1015.30      |
|2024-01-19 10:30:49.345678 |sensor_1  |28.90          |58.33        |1008.75      |
|2024-01-19 10:30:51.456789 |sensor_5  |24.56          |68.90        |1013.20      |
|2024-01-19 10:30:53.567890 |sensor_2  |26.78          |61.45        |1010.85      |
+---------------------------+----------+---------------+-------------+-------------+

--- Generando reporte por sensor ---
+----------+--------------+------------------+------------------+------------------+-------------+--------------+--------------+-------------+--------------+--------------+
|sensor_id |total_readings|avg_temperature   |min_temperature   |max_temperature   |avg_humidity |min_humidity  |max_humidity  |avg_pressure |min_pressure  |max_pressure  |
+----------+--------------+------------------+------------------+------------------+-------------+--------------+--------------+-------------+--------------+--------------+
|sensor_1  |10            |24.56             |18.30             |32.10             |64.23        |52.10         |78.90         |1011.45      |998.20        |1025.30       |
|sensor_2  |8             |25.12             |19.45             |31.20             |68.90        |55.30         |82.40         |1012.78      |1002.50       |1023.10       |
|sensor_3  |12            |26.89             |20.15             |33.45             |62.34        |48.90         |75.20         |1010.20      |995.80        |1024.50       |
|sensor_4  |11            |23.45             |17.80             |29.90             |70.15        |58.40         |84.30         |1014.55      |1001.20       |1027.90       |
|sensor_5  |9             |27.34             |21.20             |34.50             |60.12        |47.30         |73.80         |1009.80      |993.40        |1022.60       |
|sensor_6  |10            |22.78             |16.50             |28.40             |73.45        |61.20         |86.10         |1016.20      |1003.80       |1029.40       |
|sensor_7  |13            |25.67             |19.30             |32.80             |65.89        |53.70         |79.60         |1011.95      |997.30        |1026.10       |
|sensor_8  |9             |24.23             |18.10             |30.60             |67.23        |54.90         |81.50         |1013.40      |999.70        |1028.20       |
|sensor_9  |8             |26.45             |20.40             |33.10             |63.56        |51.20         |76.40         |1010.65      |996.50        |1023.80       |
|sensor_10 |10            |23.89             |17.60             |29.70             |69.78        |57.80         |83.90         |1014.10      |1000.90       |1027.30       |
+----------+--------------+------------------+------------------+------------------+-------------+--------------+--------------+-------------+--------------+--------------+

Reporte guardado en: data/sensor_report

✓ Procesamiento completado exitosamente
```

## 4. Reporte CSV Generado

Contenido del archivo `data/sensor_report/part-00000-*.csv`:

```csv
sensor_id,total_readings,avg_temperature,min_temperature,max_temperature,avg_humidity,min_humidity,max_humidity,avg_pressure,min_pressure,max_pressure
sensor_1,10,24.56,18.30,32.10,64.23,52.10,78.90,1011.45,998.20,1025.30
sensor_2,8,25.12,19.45,31.20,68.90,55.30,82.40,1012.78,1002.50,1023.10
sensor_3,12,26.89,20.15,33.45,62.34,48.90,75.20,1010.20,995.80,1024.50
sensor_4,11,23.45,17.80,29.90,70.15,58.40,84.30,1014.55,1001.20,1027.90
sensor_5,9,27.34,21.20,34.50,60.12,47.30,73.80,1009.80,993.40,1022.60
sensor_6,10,22.78,16.50,28.40,73.45,61.20,86.10,1016.20,1003.80,1029.40
sensor_7,13,25.67,19.30,32.80,65.89,53.70,79.60,1011.95,997.30,1026.10
sensor_8,9,24.23,18.10,30.60,67.23,54.90,81.50,1013.40,999.70,1028.20
sensor_9,8,26.45,20.40,33.10,63.56,51.20,76.40,1010.65,996.50,1023.80
sensor_10,10,23.89,17.60,29.70,69.78,57.80,83.90,1014.10,1000.90,1027.30
```

## 5. Verificación de Kafka

### Listar tópicos existentes:

```bash
$ kafka-topics.sh --list --bootstrap-server localhost:9092

input_topic
output_topic
```

### Consumir mensajes directamente desde Kafka:

```bash
$ kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic input_topic --from-beginning

{"timestamp": "2024-01-19T10:30:45.123456", "sensor_id": "sensor_3", "temperature": 25.34, "humidity": 65.22, "pressure": 1012.45}
{"timestamp": "2024-01-19T10:30:47.234567", "sensor_id": "sensor_7", "temperature": 22.15, "humidity": 72.45, "pressure": 1015.30}
{"timestamp": "2024-01-19T10:30:49.345678", "sensor_id": "sensor_1", "temperature": 28.90, "humidity": 58.33, "pressure": 1008.75}
...
```

## 6. Setup Script - Salida de Ejemplo

```bash
$ ./setup.sh

===================================
DEPIA Módulo 5 - Setup Script
===================================

[1/5] Verificando Python...
✓ Python encontrado: Python 3.9.7

[2/5] Verificando Java...
✓ Java encontrado: openjdk version "11.0.16"

[3/5] Creando entorno virtual...
✓ Entorno virtual creado

[4/5] Instalando dependencias...
✓ Dependencias instaladas

[5/5] Creando directorios...
✓ Directorios creados

===================================
✓ Setup completado exitosamente
===================================

Próximos pasos:
1. Activa el entorno virtual:
   source venv/bin/activate

2. Asegúrate de que Kafka esté corriendo...
[resto de instrucciones]
```

## Interpretación de Resultados

### Métricas de Streaming

- **window**: Ventana de tiempo de agregación (5 minutos)
- **sensor_id**: Identificador único del sensor
- **avg_temperature**: Temperatura promedio en grados Celsius
- **avg_humidity**: Humedad promedio en porcentaje
- **avg_pressure**: Presión atmosférica promedio en mbar
- **num_readings**: Número de lecturas procesadas en la ventana

### Métricas Batch

El reporte batch proporciona estadísticas completas:
- **total_readings**: Total de lecturas históricas del sensor
- **avg/min/max_temperature**: Estadísticas de temperatura (15-35°C)
- **avg/min/max_humidity**: Estadísticas de humedad (30-90%)
- **avg/min/max_pressure**: Estadísticas de presión (980-1030 mbar)

## Notas

- Los valores mostrados son datos simulados para propósitos demostrativos
- Los timestamps reflejan el momento de generación de los datos
- Las particiones de Kafka se asignan automáticamente mediante round-robin
- Los checkpoints de Spark se guardan en `/tmp/spark_checkpoint_*`
