import cv2
import numpy as np

# Captura de video desde la cámara, utiliza la primera camara conectada, la camara de la laptop a mí no me sirve xd, así que uso una externa
#No la encontraba pero al colocar 0 de nuevo si la encontró:
cap = cv2.VideoCapture(0)

#.Permitir que la cámara se estabilice:
cv2.waitKey(2000)
#Hace que el programa espere 2000 milisegundos.
#Esto permite que la cámara se estabilice antes de tomar la primera imagen.

#.Capturar el fondo durante unos segundos:
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()
#cap.read() captura un frame de la cámara.
#ret es True si la captura fue exitosa, False si falló.
#background guarda la imagen del fondo, que se usará luego para rellenar la zona donde está la tela azul en este caso.
#Si no se pudo capturar el fondo, se liberan los recursos con cap.release() y se termina el programa con exit().

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    #Se inicia un bucle que lee continuamente frames de la cámara mientras esté abierta.
    #Si no se puede leer un frame, se rompe el bucle ret.
    
    #. Convertir el cuadro a espacio de color HSV:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #. Definir el rango de color de la tela (verde, en este caso) en HSV
    lower_green = np.array([80, 80, 80])
    upper_green = np.array([140, 255, 255])
    #Convierte la imagen de BGR (formato por defecto de OpenCV) a HSV.
    #HSV es más fácil para detectar colores específicos porque separa en...
    #H: tono (color)
    #S: saturación (intensidad)
    #V: valor (brillo)
    
    #. Crear una máscara que detecta el área del color
    mask = cv2.inRange(hsv, lower_green, upper_green)
    #cv2.inRange genera una máscara binaria.
    #Pixeles dentro del rango verde: 255 (blanco)
    #Pixeles fuera del rango: 0 (negro)
    
    #. Refinar la máscara (puedes ajustar los parámetros para mejorar la detección)
    #. Invertir la máscara para obtener las áreas que no son verdes
    mask_inv = cv2.bitwise_not(mask)
    
    
    #. Aplicar la máscara a la imagen original para mostrar solo las partes no verdes
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    

    #. Aplicar la máscara al fondo para cubrir las partes verdes
    res2 = cv2.bitwise_and(background, background, mask=mask)
    

    #. Combinar ambas imágenes
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 
    

    #. Mostrar el resultado final
    cv2.imshow("Capa de Invisibilidad", final_output)
    cv2.imshow('mask', mask)
    

    #. Presionar 'q' para salir o cerrar la ventana, esto porque me da un error ya que mi camara en realidad no es por defecto, pero no supe
    #arreglarlo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Capa de Invisibilidad", cv2.WND_PROP_VISIBLE) < 1:
        break


#. Liberar los recursos
cap.release()
cv2.destroyAllWindows()
