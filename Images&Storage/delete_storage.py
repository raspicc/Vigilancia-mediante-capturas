import datetime
from firebase_admin import credentials, storage, initialize_app
import time

# Ruta al archivo de credenciales del servicio de Firebase
ruta_credenciales = 'key.json'

# Configurar la aplicación de Firebase con las credenciales del servicio
cred = credentials.Certificate(ruta_credenciales)
initialize_app(cred, {'storageBucket':'videovigilancia-online.appspot.com'})

def eliminar_imagenes():
    bucket = storage.bucket()
    carpeta = 'ImagesSecurity/CTIC-Lab2/'
    blobs = bucket.list_blobs(prefix=carpeta)

    # Obtener la fecha y hora actual en la zona horaria local
    ahora = datetime.datetime.now()

    # Establecer la hora objetivo para eliminar las imágenes (23:59:59)
    hora_objetivo = ahora.replace(hour=23, minute=59, second=59)

    # Calcular la cantidad de segundos restantes hasta la próxima ejecución
    tiempo_restante = (hora_objetivo - ahora).total_seconds()

    # Esperar hasta que sea la hora objetivo
    time.sleep(tiempo_restante)

    # Recorrer y eliminar las imágenes en la carpeta
    for blob in blobs:
        if blob.name.endswith('/') or blob.name == carpeta:
            continue  # Ignorar las carpetas y la carpeta principal
        blob.delete()
        print(f"Imagen eliminada: {blob.name}")

while True:
    # Llamar a la función para eliminar las imágenes
    eliminar_imagenes()
    # Esperar 24 horas antes de la siguiente ejecución
    time.sleep(86400)
