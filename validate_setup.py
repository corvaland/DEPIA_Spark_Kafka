#!/usr/bin/env python3
"""
Script de validación para verificar que el entorno está correctamente configurado
"""

import sys
import subprocess

def check_python_version():
    """Verifica la versión de Python"""
    print("✓ Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} - Se requiere Python 3.8+")
        return False

def check_java():
    """Verifica que Java esté instalado"""
    print("\n✓ Verificando Java...")
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Java imprime la versión en stderr
            version_line = result.stderr.split('\n')[0]
            print(f"  ✓ {version_line} - OK")
            return True
        else:
            print("  ✗ Java no encontrado")
            return False
    except Exception as e:
        print(f"  ✗ Error al verificar Java: {e}")
        return False

def check_dependencies():
    """Verifica que las dependencias de Python estén instaladas"""
    print("\n✓ Verificando dependencias de Python...")
    dependencies = ['pyspark', 'kafka']
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✓ {dep} - OK")
        except ImportError:
            print(f"  ✗ {dep} - NO INSTALADO")
            all_ok = False
    
    return all_ok

def check_code_syntax():
    """Verifica que los archivos Python no tengan errores de sintaxis"""
    print("\n✓ Verificando sintaxis de código...")
    files = [
        'src/kafka_producer.py',
        'src/spark_streaming_consumer.py',
        'src/spark_batch_processor.py'
    ]
    
    all_ok = True
    for file in files:
        try:
            result = subprocess.run(['python3', '-m', 'py_compile', file],
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"  ✓ {file} - OK")
            else:
                print(f"  ✗ {file} - ERROR DE SINTAXIS")
                all_ok = False
        except Exception as e:
            print(f"  ✗ {file} - Error: {e}")
            all_ok = False
    
    return all_ok

def check_kafka_connection():
    """Verifica si Kafka está disponible (opcional)"""
    print("\n✓ Verificando conexión a Kafka (opcional)...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 9092))
        sock.close()
        
        if result == 0:
            print("  ✓ Kafka está corriendo en localhost:9092")
            return True
        else:
            print("  ⚠ Kafka no está corriendo (no es obligatorio para validación)")
            return True  # No es crítico para la validación del setup
    except Exception as e:
        print(f"  ⚠ No se pudo verificar Kafka: {e}")
        return True  # No es crítico

def main():
    """Función principal"""
    print("=" * 60)
    print("DEPIA Módulo 5 - Validación de Entorno")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_java(),
        check_dependencies(),
        check_code_syntax(),
        check_kafka_connection()
    ]
    
    print("\n" + "=" * 60)
    if all(checks[:4]):  # Los primeros 4 son críticos
        print("✓✓✓ VALIDACIÓN EXITOSA ✓✓✓")
        print("El entorno está correctamente configurado")
        print("\nPróximos pasos:")
        print("1. Inicia Kafka si no está corriendo")
        print("2. Ejecuta: python src/kafka_producer.py")
        print("3. Ejecuta: python src/spark_streaming_consumer.py")
        return 0
    else:
        print("✗✗✗ VALIDACIÓN FALLIDA ✗✗✗")
        print("Hay problemas con la configuración del entorno")
        print("\nRevisa los errores anteriores y:")
        print("1. Ejecuta ./setup.sh para instalar dependencias")
        print("2. Verifica que Java esté instalado")
        return 1

if __name__ == "__main__":
    sys.exit(main())
