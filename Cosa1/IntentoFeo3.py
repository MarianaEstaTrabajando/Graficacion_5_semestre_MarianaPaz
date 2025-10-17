import cv2
import numpy as np
# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)
ls=set() #Conjunto para almacenar las coordenadas de los píxeles detectados
cv2.waitKey(2000) #Esperar 2 segundos para que la cámara se estabilice

valor= True
while cap.isOpened(): #Mientras la cámara esté abierta
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertir la imagen a espacio de color HSV
    #. Definir el rango de color de la tela (verde, en este caso) en HSV
    lower_green = np.array([80, 80, 80])
    upper_green = np.array([140, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green) #Crear una máscara para el color verde
    
    res = cv2.bitwise_and(frame, frame, mask=mask) #Aplicar la máscara a la imagen original
    
    alto=frame.shape[0] #alto de la imagen
    ancho=frame.shape[1] #ancho de la imagen
    for y in range(alto):     
        for x in range(ancho):
            if mask[y, x] != 0:
                ls.add((y, x))

    
    #coords = np.column_stack(np.where(mask == 255))
    for i in ls: 
        frame[i[0],i[1]]= [0,255,0] #Pintar los pixeles detectados del color
    
    cv2.imshow("Seguimiento", frame) #Mostrar el video con el seguimiento
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Seguimiento", cv2.WND_PROP_VISIBLE) < 1:
        break


#. Liberar los recursos
cap.release()
cv2.destroyAllWindows()