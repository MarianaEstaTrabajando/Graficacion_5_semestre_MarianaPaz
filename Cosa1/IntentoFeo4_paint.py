import cv2
import numpy as np
# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)
verde= set()#Conjunto para almacenar las coordenadas de los píxeles detectados de color verde
rosa= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color rosa
rojo= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color rojo
morado= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color morado
naranja= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color naranja
amarillo= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color amarillo
azul= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color azul
cyan= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color cyan
cv2.waitKey(2000) #Esperar 2 segundos para que la cámara se estabilice
valor= (0,255,0)
while cap.isOpened(): #Mientras la cámara esté abierta
    ret, frame = cap.read()
    frame2 = frame.copy()
    if not ret:
        break
    
    cv2.rectangle(frame2, (50, 50), (100, 100), (0, 255, 0), -1) #verde
    cv2.rectangle(frame2, (50, 100), (100, 150), (255, 0, 136), -1) #rosa
    cv2.rectangle(frame2, (50, 150), (100, 200), (0, 0, 255), -1) #rojo
    cv2.rectangle(frame2, (50, 200), (100, 250), (255, 0, 255), -1) #morado
    cv2.rectangle(frame2, (50, 250), (100, 300), (0, 136, 255), -1) #naranja
    cv2.rectangle(frame2, (50, 300), (100, 350), (0, 255, 255), -1) #amarillo
    cv2.rectangle(frame2, (50, 350), (100, 400), (255, 0, 0), -1) #azul
    cv2.rectangle(frame2, (50, 400), (100, 450), (255, 255, 0), -1) #cyan
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertir la imagen a espacio de color HSV
    #. Definir el rango de color de la tela (verde, en este caso) en HSV
    lower_green = np.array([80, 80, 80])
    upper_green = np.array([140, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green) #Crear una máscara para el color verde
    
    res = cv2.bitwise_and(frame, frame, mask=mask) #Aplicar la máscara a la imagen original
    
    alto=frame.shape[0] #alto de la imagen
    ancho=frame.shape[1] #ancho de la imagen
    for y in range(alto):     
        #Checar cada píxel en la máscara
        for x in range(ancho):
            if mask[y, x] != 0: #Si el píxel pertenece al color de la tela
                if(valor==[0,255,0]):
                    verde.add((y, x)) #Agregar las coordenadas al conjunto de color verde
                elif(valor==[255,0,136]):
                    rosa.add((y, x)) #Agregar las coordenadas al conjunto de color rosa
                elif(valor==[0,0,255]):
                    rojo.add((y, x)) #Agregar las coordenadas al conjunto de color rojo
                elif(valor==[255,0,255]):
                    morado.add((y, x))  #Agregar las coordenadas al conjunto de color morado
                elif(valor==[0,136,255]):
                    naranja.add((y, x)) #Agregar las coordenadas al conjunto de color naranja
                elif(valor==[0,255,255]):
                    amarillo.add((y, x)) #Agregar las coordenadas al conjunto de color amarillo
                elif(valor==[255,0,0]):
                    azul.add((y, x)) #Agregar las coordenadas al conjunto de color azul
                elif(valor==[255,255,0]):
                    cyan.add((y, x)) #Agregar las coordenadas al conjunto de color cyan
                    
                if(50<x<130): #Si el píxel está en la zona de selección de color
                    if(50<y<100):
                        valor=[0,255,0]
                    elif(100<y<150):  
                        valor=[255,0,136]
                    elif(150<y<200):    
                        valor=[0,0,255]
                    elif(200<y<250):
                        valor=[255,0,255]
                    elif(250<y<300):
                        valor=[0,136,255]
                    elif(300<y<350):
                        valor=[0,255,255]
                    elif(350<y<400):
                        valor=[255,0,0]
                    elif(400<y<450):
                        valor=[255,255,0]
                    
    
    #coords = np.column_stack(np.where(mask == 255))
    for i in verde: 
        frame2[i[0],i[1]]= [0,255,0] #Pintar los pixeles detectados del color
    for i in rosa: 
        frame2[i[0],i[1]]= [255,0,136]
    for i in rojo: 
        frame2[i[0],i[1]]= [0,0,255]
    for i in morado: 
        frame2[i[0],i[1]]= [255,0,255]
    for i in naranja: 
        frame2[i[0],i[1]]= [0,136,255]
    for i in amarillo:
        frame2[i[0],i[1]]= [0,255,255]
    for i in azul: 
        frame2[i[0],i[1]]= [255,0,0]
    for i in cyan: 
        frame2[i[0],i[1]]= [255,255,0]
    
    cv2.imshow("Seguimiento", frame2) #Mostrar el video con el seguimiento
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Seguimiento", cv2.WND_PROP_VISIBLE) < 1:
        break


#. Liberar los recursos
cap.release()
cv2.destroyAllWindows()