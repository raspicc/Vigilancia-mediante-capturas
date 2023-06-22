import cv2
import os
import time
from datetime import datetime

# Crear la carpeta para almacenar las imágenes si no existe
folder_name = "ImagesSecurity"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Inicializar la cámara web
cap = cv2.VideoCapture(0)

# Variable para contar el número de imágenes capturadas
image_count = 1

# Variables para el cálculo del movimiento
previous_frame = None
movement_threshold = 1000  # Ajusta este umbral según tu entorno

while True:
    # Leer un cuadro de la cámara
    ret, frame = cap.read()

    # Mostrar el cuadro en una ventana
    cv2.imshow("Camera", frame)

    # Convertir el cuadro a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Inicializar el cuadro anterior en la primera iteración
    if previous_frame is None:
        previous_frame = gray
        continue

    # Calcular la diferencia absoluta entre el cuadro actual y el anterior
    frame_delta = cv2.absdiff(previous_frame, gray)

    # Aplicar un umbral a la diferencia absoluta
    _, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)

    # Realizar una dilatación para llenar agujeros en los objetos detectados
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Encontrar los contornos de los objetos en el cuadro
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Verificar si se detectó movimiento
    movement_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > movement_threshold:
            movement_detected = True
            break

    if movement_detected:
        # Obtener la fecha y hora actual con microsegundos
        current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S-%f")

        # Generar el nombre de la imagen con el formato especificado
        image_name = f"{current_time}.jpg"
        image_path = os.path.join(folder_name, image_name)

        # Guardar el cuadro como una imagen
        cv2.imwrite(image_path, frame)

        # Incrementar el contador de imágenes
        image_count += 1

    # Actualizar el cuadro anterior con el cuadro actual
    previous_frame = gray.copy()

    # Esperar n segundos
    time.sleep(0.1)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
