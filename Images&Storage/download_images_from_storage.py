import tkinter as tk
from tkinter import filedialog
import os
from firebase_admin import credentials, storage, initialize_app

# Inicializar Firebase
cred = credentials.Certificate('key.json')  # Reemplaza con la ruta a tu archivo JSON de credenciales
initialize_app(cred, {'storageBucket': 'videovigilancia-online.appspot.com'})  # Reemplaza con la URL de tu bucket de almacenamiento

# Configurar la ventana de Tkinter
window = tk.Tk()

def download_images():
    # Obtener la ruta de la carpeta local para descargar las imágenes
    local_folder = filedialog.askdirectory(initialdir='.', title='Seleccione una carpeta local')

    # Obtener una referencia al bucket de almacenamiento de Firebase
    bucket = storage.bucket()

    # Definir la ruta de la carpeta en el almacenamiento de Firebase
    firebase_folder = 'ImagesSecurity/Lab2'

    # Obtener la lista de nombres de archivos en la carpeta de Firebase
    blob_list = bucket.list_blobs(prefix=firebase_folder)
    file_names = [blob.name for blob in blob_list if blob.name.endswith('.jpg')]

    # Descargar las imágenes en la carpeta local
    for file_name in file_names:
        # Obtener el nombre del archivo sin la ruta de la carpeta
        _, image_name = os.path.split(file_name)

        # Definir la ruta local de la imagen
        local_path = os.path.join(local_folder, image_name)

        # Descargar la imagen desde Firebase
        blob = bucket.blob(file_name)
        blob.download_to_filename(local_path)
        print(f"Descargada: {image_name}")

    print("Descarga completa")

# Configurar el botón en la ventana
download_button = tk.Button(window, text="Descargar imágenes", command=download_images)
download_button.pack()

# Ejecutar el bucle principal de Tkinter
window.mainloop()
