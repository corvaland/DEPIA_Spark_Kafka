"""
Productor de Kafka para DEPIA Módulo 5
Este script genera y envía datos de ejemplo a un tópico de Kafka
"""

from kafka import KafkaProducer
import json
import time
from datetime import datetime
import random

class DataProducer:
    def __init__(self, bootstrap_servers='localhost:9092', topic='input_topic'):
        """
        Inicializa el productor de Kafka
        
        Args:
            bootstrap_servers: Dirección del servidor Kafka
            topic: Nombre del tópico donde se enviarán los mensajes
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic
    
    def generate_sample_data(self):
        """
        Genera datos de ejemplo simulando eventos de sensores
        
        Returns:
            dict: Diccionario con datos de ejemplo
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'sensor_id': f'sensor_{random.randint(1, 10)}',
            'temperature': round(random.uniform(15.0, 35.0), 2),
            'humidity': round(random.uniform(30.0, 90.0), 2),
            'pressure': round(random.uniform(980.0, 1030.0), 2)
        }
    
    def send_data(self, data):
        """
        Envía datos al tópico de Kafka
        
        Args:
            data: Datos a enviar (serán serializados a JSON)
        """
        try:
            future = self.producer.send(self.topic, data)
            record_metadata = future.get(timeout=10)
            print(f"Mensaje enviado a {record_metadata.topic} "
                  f"partición {record_metadata.partition} "
                  f"offset {record_metadata.offset}")
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
    
    def produce_continuous(self, interval=2, num_messages=None):
        """
        Produce mensajes de forma continua
        
        Args:
            interval: Intervalo en segundos entre mensajes
            num_messages: Número de mensajes a enviar (None para continuo)
        """
        count = 0
        try:
            while num_messages is None or count < num_messages:
                data = self.generate_sample_data()
                self.send_data(data)
                print(f"Mensaje {count + 1}: {data}")
                count += 1
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nProducción detenida por el usuario")
        finally:
            self.close()
    
    def close(self):
        """Cierra la conexión del productor"""
        self.producer.flush()
        self.producer.close()
        print("Productor cerrado")

if __name__ == "__main__":
    # Configuración
    KAFKA_SERVERS = 'localhost:9092'
    TOPIC_NAME = 'input_topic'
    
    # Crear y ejecutar productor
    producer = DataProducer(bootstrap_servers=KAFKA_SERVERS, topic=TOPIC_NAME)
    
    print(f"Iniciando productor de datos para el tópico '{TOPIC_NAME}'...")
    print("Presiona Ctrl+C para detener")
    
    # Producir 100 mensajes con intervalo de 2 segundos
    producer.produce_continuous(interval=2, num_messages=100)
