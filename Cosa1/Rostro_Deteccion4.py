import cv2 as cv 
import numpy as np
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
#cuando parpadees,ojos, lengua
#orejas creo y sepa la bola qué más
cantidadceros_ant=0; b=0
centro_x=0; centro_y=0
while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)  
    
    
    for(x,y,w,h) in rostros:
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        roi = hsv[y + int(h*0.4):y + int(h*0.6), x + int(w*0.4):x + int(w*0.6)]
        color_rostro = cv.mean(roi)[:3]  # Promedio H, S, V
        h_, s, v = color_rostro

        delta_h = 20
        delta_s = 100
        delta_v = 150

        bajo = np.array([max(h_ - delta_h, 0), max(s - delta_s, 50), max(v - delta_v, 50)], dtype=np.uint8)
        alto = np.array([min(h_ + delta_h, 179), min(s + delta_s, 200), min(v + delta_v, 220)], dtype=np.uint8)
        mask = cv.inRange(hsv, bajo, alto)
        
        
        res = int((w+h)/8)
        img = cv.rectangle(img, (x,y), (x+w, y+h), (234, 23,23), 5) #rostro
        img = cv.rectangle(img, (x,int(y+h/2)), (x+w, y+h), (0,255,0),5 ) #rostro
        img = cv.rectangle(img, (x - int(0.1*w),y +int( 0.3*h)),(x,y+int(0.7*h)), (0,0,255), 5) #oreja izquierda
        img=cv.rectangle(img, (x + w ,y +int( 0.3*h)),(x + w + int(0.1*w),y+int(0.7*h)), (0,0,255), 2) #oreja derecha
        img=cv.circle(img, (x + int(w*0.5), y + int(h*0.53)) , 30, (0, 0, 255), -1 ) #nariz
        
        
        # Ojos
        
        roi = mask[y + int(h*0.4)-28:y + int(h*0.4)+28, x + int(w*0.3)-28:x + int(w*0.3)+28] 
        # Obtener las coordenadas donde hay ceros
        coords_ceros1 = np.column_stack(np.where(roi == 0))
        if len(coords_ceros1) > 0:
            # Promedio de filas (Y) y columnas (X)
            centro_y = int(np.mean(coords_ceros1[:, 0]))
            centro_x = int(np.mean(coords_ceros1[:, 1]))
        
        # Ojo izquierdo
        img = cv.ellipse(img, (x + int(w*0.3), y + int(h*0.4)), (28, 28), 0, 0, 360, (0, 0, 0), 2)  # contorno negro
        img = cv.ellipse(img, (x + int(w*0.3), y + int(h*0.4)), (27, 27), 0, 0, 360, (255, 255, 255), -1)  # blanco
        img = cv.ellipse(img, (x + int(w*0.3)-28+centro_x, y + int(h*0.4)-28+centro_y), (5, 5), 0, 0, 360, (0, 0, 255), -1)  # pupila

        # Ojo derecho
        img = cv.ellipse(img, (x + int(w*0.7), y + int(h*0.4)), (28, 28), 0, 0, 360, (0, 0, 0), 2)  # contorno negro
        img = cv.ellipse(img, (x + int(w*0.7), y + int(h*0.4)), (27, 27), 0, 0, 360, (255, 255, 255), -1)  # blanco
        img = cv.ellipse(img, (x + int(w*0.7)-28+centro_x, y + int(h*0.4)-28+centro_y), (5, 5), 0, 0, 360, (0, 0, 255), -1)  # pupila

        # Boca
        
        roi = mask[y + int(h*0.75)-int(h*0.1):y + int(h*0.75)+int(h*0.1), x + int(w*0.5)-int(w*0.2):x + int(w*0.5)+int(w*0.2)] 
        # Obtener las coordenadas donde hay ceros
        coords_ceros1 = np.column_stack(np.where(roi == 0))
        cantidadceros=coords_ceros1.shape[0]
        if cantidadceros>cantidadceros_ant and b< int(h*0.15):
            b+=int(cantidadceros-cantidadceros_ant)/20
        if cantidadceros<cantidadceros_ant and b>1:
            b-=int(cantidadceros_ant-cantidadceros)/20
        cantidadceros_ant=cantidadceros
        if(b<0):
            b=0   
        cantidadceros_ant=cantidadceros
        
        img=cv.ellipse(img, (x + int(w*0.5), y + int(h*0.75)), (int(w*0.2), int(h*0.01)+int(b)), 0, 0, 180, (0,0,0), -1) #boca
        
        
        
    

    cv.imshow('img', img)
    cv.imshow('mask', mask)
    if cv.waitKey(1)== ord('q'):
        break
    
cap.release
cv.destroyAllWindows()