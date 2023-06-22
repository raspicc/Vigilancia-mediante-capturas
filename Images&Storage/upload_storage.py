import time
import os.path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from firebase_admin import credentials, storage, initialize_app

# Ruta al archivo de credenciales del servicio de Firebase
ruta_credenciales = 'key.json'

# Configurar la aplicación de Firebase con las credenciales del servicio
cred = credentials.Certificate(ruta_credenciales)
initialize_app(cred, {'storageBucket':'videovigilancia-online.appspot.com'})

def subir_imagen(nombre_archivo, ruta_local):
    bucket = storage.bucket()
    destino = "ImagesSecurity/Lab2/" + nombre_archivo  # Ruta de destino dentro del bucket
    blob = bucket.blob(destino)
    blob.upload_from_filename(ruta_local)
    url = blob.public_url
    print(f"Imagen subida con éxito. URL pública: {url}")


class NuevoArchivoHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_uploaded = None

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.jpg'):
            archivo = os.path.basename(event.src_path)
            peso = os.path.getsize(event.src_path)

            if peso != 0:
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
                if fecha_actual in archivo:
                    if archivo != self.last_uploaded:
                        print(f"Se ha creado un nuevo archivo coincidente con la fecha actual: {archivo}")
                        print(f"Peso del archivo: {peso} bytes")

                        ruta_local = event.src_path
                        subir_imagen(archivo, ruta_local)
                        self.last_uploaded = archivo


carpeta = 'C:/Users/Luis Chanquetti/Desktop/Security/ImagesSecurity'
event_handler = NuevoArchivoHandler()
observer = Observer()
observer.schedule(event_handler, path=carpeta, recursive=False)
observer.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    observer.stop()

observer.join()



