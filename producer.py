import time
import random
from kafka import KafkaProducer

try:
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    print("Conexión con Kafka exitosa")
except Exception as e:
    print(f"Error al conectar con kafka: {e}")
    exit()

frases = [
    "Hola Soy Marcos",
    "Este es mi primer stream",
    "El topico fue creado",
    "El producer manda los mensajes",
    "El consumer los lee",
    "Saludos"
]

print("Enviando mensajes a Kafka... Presiona Ctrl+C en el terminal para detener.")

try:
    while True:
        mensaje = random.choice(frases)
        
        producer.send('actividad-topic', mensaje.encode('utf-8'))
        
        print(f"Mensaje enviado: '{mensaje}'")
        
        time.sleep(random.uniform(1,3))

except KeyboardInterrupt:
    print("\nProductor detenido por el usuario.")

finally:
    print("Cerrando productor")
    producer.flush()
    producer.close()