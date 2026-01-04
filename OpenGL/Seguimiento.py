import cv2
import numpy as np

# Definición del intervalo de color azul en HSV
color_min = np.array([100, 140, 60])
color_max = np.array([145, 255, 255])

# Abrir la cámara principal
camera = cv2.VideoCapture(0)

# Imagen acumulativa donde se guardará el recorrido
canvas = None

while camera.isOpened():
    success, image = camera.read()
    if not success:
        break

    # Crear el lienzo una sola vez con el tamaño del video
    if canvas is None:
        canvas = np.zeros(image.shape, dtype=np.uint8)

    # Conversión de BGR a HSV
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Aislar el color seleccionado
    color_mask = cv2.inRange(hsv_img, color_min, color_max)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, None, iterations=2)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, None, iterations=2)

    # Detección de regiones del color
    shapes, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(shapes) > 0:
        main_shape = max(shapes, key=cv2.contourArea)
        (cx, cy), size = cv2.minEnclosingCircle(main_shape)

        if size > 6:
            # Pintar el punto detectado sobre el lienzo
            cv2.circle(canvas, (int(cx), int(cy)), int(size), (255, 0, 0), -1)

    # Superponer el dibujo sobre la imagen original
    final_view = cv2.addWeighted(image, 0.75, canvas, 0.25, 0)

    cv2.imshow("Seguimiento de color", final_view)

    # Presionar ESC para cerrar
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
