"""
Consumidor y Procesador con Spark Structured Streaming
Lee datos desde Kafka, los procesa y escribe resultados
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

class SparkKafkaProcessor:
    def __init__(self, app_name="DEPIA_Spark_Kafka", kafka_servers="localhost:9092"):
        """
        Inicializa la sesión de Spark
        
        Args:
            app_name: Nombre de la aplicación Spark
            kafka_servers: Dirección del servidor Kafka
        """
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars.packages", 
                   "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        self.kafka_servers = kafka_servers
        
        # Definir el esquema de los datos
        self.schema = StructType([
            StructField("timestamp", StringType(), True),
            StructField("sensor_id", StringType(), True),
            StructField("temperature", DoubleType(), True),
            StructField("humidity", DoubleType(), True),
            StructField("pressure", DoubleType(), True)
        ])
    
    def read_from_kafka(self, topic):
        """
        Lee datos desde un tópico de Kafka
        
        Args:
            topic: Nombre del tópico de Kafka
            
        Returns:
            DataFrame: DataFrame de Spark con los datos del stream
        """
        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_servers) \
            .option("subscribe", topic) \
            .option("startingOffsets", "latest") \
            .load()
        
        # Parsear el valor JSON
        parsed_df = df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), self.schema).alias("data")) \
            .select("data.*")
        
        # Convertir timestamp a tipo TimestampType
        parsed_df = parsed_df.withColumn(
            "timestamp", 
            col("timestamp").cast(TimestampType())
        )
        
        return parsed_df
    
    def process_data(self, df):
        """
        Procesa los datos aplicando transformaciones
        
        Args:
            df: DataFrame de entrada
            
        Returns:
            DataFrame: DataFrame procesado con agregaciones
        """
        # Calcular estadísticas por sensor y ventana de tiempo
        aggregated_df = df \
            .withWatermark("timestamp", "10 minutes") \
            .groupBy(
                window(col("timestamp"), "5 minutes"),
                col("sensor_id")
            ) \
            .agg(
                avg("temperature").alias("avg_temperature"),
                avg("humidity").alias("avg_humidity"),
                avg("pressure").alias("avg_pressure"),
                count("*").alias("num_readings")
            )
        
        return aggregated_df
    
    def write_to_console(self, df, checkpoint_location="/tmp/checkpoint_console"):
        """
        Escribe los resultados a la consola
        
        Args:
            df: DataFrame a escribir
            checkpoint_location: Ubicación del checkpoint
        """
        query = df \
            .writeStream \
            .outputMode("update") \
            .format("console") \
            .option("truncate", "false") \
            .option("checkpointLocation", checkpoint_location) \
            .start()
        
        return query
    
    def write_to_kafka(self, df, topic, checkpoint_location="/tmp/checkpoint_kafka"):
        """
        Escribe los resultados a un tópico de Kafka
        
        Args:
            df: DataFrame a escribir
            topic: Tópico de destino
            checkpoint_location: Ubicación del checkpoint
        """
        # Convertir DataFrame a formato Kafka (key, value)
        kafka_df = df.selectExpr("CAST(sensor_id AS STRING) AS key",
                                  "to_json(struct(*)) AS value")
        
        query = kafka_df \
            .writeStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_servers) \
            .option("topic", topic) \
            .option("checkpointLocation", checkpoint_location) \
            .start()
        
        return query
    
    def stop(self):
        """Detiene la sesión de Spark"""
        self.spark.stop()

def main():
    """Función principal"""
    # Configuración
    KAFKA_SERVERS = "localhost:9092"
    INPUT_TOPIC = "input_topic"
    OUTPUT_TOPIC = "output_topic"
    CHECKPOINT_CONSOLE = "/tmp/spark_checkpoint_console"
    CHECKPOINT_KAFKA = "/tmp/spark_checkpoint_kafka"
    
    print("Iniciando procesamiento con Spark Structured Streaming...")
    
    # Crear procesador
    processor = SparkKafkaProcessor(
        app_name="DEPIA_Modulo5_Streaming",
        kafka_servers=KAFKA_SERVERS
    )
    
    # Leer datos desde Kafka
    print(f"Leyendo datos desde el tópico '{INPUT_TOPIC}'...")
    input_df = processor.read_from_kafka(INPUT_TOPIC)
    
    # Procesar datos
    print("Procesando datos (agregaciones por ventana de tiempo)...")
    processed_df = processor.process_data(input_df)
    
    # Escribir resultados a la consola
    console_query = processor.write_to_console(processed_df, CHECKPOINT_CONSOLE)
    
    # Escribir resultados a Kafka (comentado por defecto)
    # kafka_query = processor.write_to_kafka(processed_df, OUTPUT_TOPIC, CHECKPOINT_KAFKA)
    
    print("Procesamiento iniciado. Esperando datos...")
    print("Presiona Ctrl+C para detener")
    
    try:
        console_query.awaitTermination()
        # Si también escribes a Kafka, descomenta:
        # kafka_query.awaitTermination()
    except KeyboardInterrupt:
        print("\nDeteniendo procesamiento...")
        console_query.stop()
        # kafka_query.stop()
        processor.stop()
        print("Procesamiento detenido")

if __name__ == "__main__":
    main()
