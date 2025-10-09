import cv2 as cv 

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
#cuando parpadees,ojos, lengua
#orejas creo y sepa la bola qué más
while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    
    for(x,y,w,h) in rostros:
        res = int((w+h)/8)
        img = cv.rectangle(img, (x,y), (x+w, y+h), (234, 23,23), 5) #rostro
        img = cv.rectangle(img, (x,int(y+h/2)), (x+w, y+h), (0,255,0),5 ) #rostro
        
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 21, (0, 0, 0), 2 ) #ojo izq
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 21, (0, 0, 0), 2 ) #ojo der
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 20, (255, 255, 255), -1 ) #ojo izq blanco
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 20, (255, 255, 255), -1 ) #ojo der blanco
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , 5, (0, 0, 255), -1 ) #ojo izq pupila
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , 5, (0, 0, 255), -1 ) #ojo der pupila
        img = cv.rectangle(img, (x - int(0.1*w),y +int( 0.3*h)),(x,y+int(0.7*h)), (0,0,255), 5) #oreja izquierda
        img=cv.rectangle(img, (x + w ,y +int( 0.3*h)),(x + w + int(0.1*w),y+int(0.7*h)), (0,0,255), 2) #oreja derecha
        img=cv.circle(img, (x + int(w*0.5), y + int(h*0.53)) , 30, (0, 0, 255), -1 ) #nariz
        img=cv.ellipse(img, (x + int(w*0.5), y + int(h*0.75)), (int(w*0.2), int(h*0.1)), 0, 0, 180, (0,0,0), -1) #boca

    cv.imshow('img', img)
    if cv.waitKey(1)== ord('q'):
        break
    
cap.release
cv.destroyAllWindows()