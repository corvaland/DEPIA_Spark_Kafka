"""
Procesamiento Batch con Spark
Lee datos desde Kafka en modo batch y genera reportes
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, max, min, count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

class SparkBatchProcessor:
    def __init__(self, app_name="DEPIA_Spark_Batch"):
        """
        Inicializa la sesión de Spark para procesamiento batch
        
        Args:
            app_name: Nombre de la aplicación Spark
        """
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars.packages", 
                   "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        
        # Esquema de datos
        self.schema = StructType([
            StructField("timestamp", StringType(), True),
            StructField("sensor_id", StringType(), True),
            StructField("temperature", DoubleType(), True),
            StructField("humidity", DoubleType(), True),
            StructField("pressure", DoubleType(), True)
        ])
    
    def read_batch_from_kafka(self, kafka_servers, topic):
        """
        Lee un lote de datos desde Kafka
        
        Args:
            kafka_servers: Dirección del servidor Kafka
            topic: Nombre del tópico
            
        Returns:
            DataFrame: DataFrame con los datos leídos
        """
        df = self.spark \
            .read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_servers) \
            .option("subscribe", topic) \
            .option("startingOffsets", "earliest") \
            .option("endingOffsets", "latest") \
            .load()
        
        # Parsear JSON
        parsed_df = df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), self.schema).alias("data")) \
            .select("data.*")
        
        return parsed_df
    
    def generate_report(self, df):
        """
        Genera reporte con estadísticas por sensor
        
        Args:
            df: DataFrame de entrada
            
        Returns:
            DataFrame: Reporte con estadísticas agregadas
        """
        report = df.groupBy("sensor_id") \
            .agg(
                count("*").alias("total_readings"),
                avg("temperature").alias("avg_temperature"),
                min("temperature").alias("min_temperature"),
                max("temperature").alias("max_temperature"),
                avg("humidity").alias("avg_humidity"),
                min("humidity").alias("min_humidity"),
                max("humidity").alias("max_humidity"),
                avg("pressure").alias("avg_pressure"),
                min("pressure").alias("min_pressure"),
                max("pressure").alias("max_pressure")
            ) \
            .orderBy("sensor_id")
        
        return report
    
    def save_report(self, df, output_path, format="csv"):
        """
        Guarda el reporte en disco
        
        Args:
            df: DataFrame a guardar
            output_path: Ruta de salida
            format: Formato de salida (csv, parquet, json)
        """
        df.coalesce(1) \
            .write \
            .mode("overwrite") \
            .option("header", "true") \
            .format(format) \
            .save(output_path)
        
        print(f"Reporte guardado en: {output_path}")
    
    def stop(self):
        """Detiene la sesión de Spark"""
        self.spark.stop()

def main():
    """Función principal para procesamiento batch"""
    # Configuración
    KAFKA_SERVERS = "localhost:9092"
    INPUT_TOPIC = "input_topic"
    OUTPUT_PATH = "data/sensor_report"
    
    print("=== Procesamiento Batch con Spark ===")
    print(f"Leyendo datos desde Kafka: {INPUT_TOPIC}")
    
    # Crear procesador
    processor = SparkBatchProcessor(app_name="DEPIA_Modulo5_Batch")
    
    try:
        # Leer datos
        df = processor.read_batch_from_kafka(KAFKA_SERVERS, INPUT_TOPIC)
        
        print(f"\nTotal de registros leídos: {df.count()}")
        
        # Mostrar muestra de datos
        print("\n--- Muestra de datos ---")
        df.show(5, truncate=False)
        
        # Generar reporte
        print("\n--- Generando reporte por sensor ---")
        report = processor.generate_report(df)
        report.show(truncate=False)
        
        # Guardar reporte
        processor.save_report(report, OUTPUT_PATH, format="csv")
        
        print("\n✓ Procesamiento completado exitosamente")
        
    except Exception as e:
        print(f"\n✗ Error durante el procesamiento: {e}")
    finally:
        processor.stop()

if __name__ == "__main__":
    main()
