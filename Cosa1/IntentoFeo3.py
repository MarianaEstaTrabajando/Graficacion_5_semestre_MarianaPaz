import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ls=set()
cv2.waitKey(2000)

valor= True
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #. Definir el rango de color de la tela (verde, en este caso) en HSV
    lower_green = np.array([80, 80, 80])
    upper_green = np.array([140, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    alto=frame.shape[0]
    ancho=frame.shape[1]
    for y in range(alto):     
        for x in range(ancho):
            if mask[y, x] != 0:
                ls.add((y, x))

    
    #coords = np.column_stack(np.where(mask == 255))
    for i in ls: 
        frame[i[0],i[1]]= [0,255,0]
    
    cv2.imshow("Seguimiento", frame)
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Seguimiento", cv2.WND_PROP_VISIBLE) < 1:
        break


#. Liberar los recursos
cap.release()
cv2.destroyAllWindows()