#+Begin_SRC python
import cv2 as cv 
import numpy as np 

img= np.ones((500,500,3),np.uint8)*150
#cv.circle(img,(255,255),150,(23,43,144),-1)  #primero va el centro, luego el radio y luego el color en BGR y 
#luego si se rellena o no
#cv.rectangle(img,(100,100),(400,400),(0,255,0),3) #primero va la esquina superior izquierda y luego la esquina inferior derecha, 
#luego el color en BGR y luego el grosor de la linea, si es -1 se rellena
#cv.line(img,(0,0),(500,500),(255,0,0),5) #primero va el punto inicial y luego el punto final, 
#luego el color en BGR y luego el grosor de la linea
h=10
j=10
inc=True
for i in range (400):
    img = np.ones((500, 500, 3), dtype=np.uint8)*255 # Crear una imagen blanca en cada iteración
    cv.circle(img,(i,150),30,(255,0,0),2)
    
    cv.circle(img,(i+10,150),1,(255,0,0),2)
    cv.circle(img,(i-10,150),1,(255,0,0),2)
    cv.line(img,(i-5,165),(i+5,165),(255,0,),2)
    
    
    cv.line(img,(i,180),(i,250),(255,0,),2)
    #img=np.ones((500,500,3),np.uint8)*150
    if(h==20):
        inc=False
        
    if(h==5):
        inc=True
    if(inc):
        h+=1
        if(h%2==0):
            j+=1
    else:
        h-=1
        if(h%2==0):
            j-=1
    cv.line(img,(i,200),(i+h,220-h),(255,0,0),2)
    cv.line(img,(i,250),(i+h,280-h),(255,0,0),2)
    
  
    cv.line(img,(i,200),(i-h,230-j),(255,0,0),2)
    cv.line(img,(i,250),(i-h,290-j),(255,0,0),2) 
    if(i==399):
        cv.line(img,(5,120),(5,290),(255,0,0),2)
        cv.line(img,(5,120),(150,290),(255,0,0),2)
        cv.line(img,(150,290),(150,120),(255,0,0),2)
        cv.circle(img,(300,200),70,(255,0,0),2)
    cv.imshow("Caminata extraña",img)
    cv.waitKey(15)



cv.waitKey(0)
cv.destroyAllWindows()