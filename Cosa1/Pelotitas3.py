import cv2 as cv
import numpy as np
import random

img = np.ones((500, 500, 3), dtype=np.uint8)*255 
i=0; j=0; h=0; k=0
valorx1=1; valory1=2
valorx2=2; valory2=1
huir=False
while(True):
    img = np.ones((500, 500, 3), dtype=np.uint8)*255 
    cv.circle(img, (20+i, 20+j), 20, (230,0,150), -1)
    cv.circle(img, (230, 230), 20, (5,192,255), -1)
    i+=valorx1; j+=valory1
 
    
    #if(((65+h)-(20+i))<=80 and ((65+h)-(20+i))>=-80 and
     #  ((65+k)-(20+j)<=80) and ((65+k)-(20+j))>=-80):
      #  ang=np.arctan2((valorx1-(i+20)),(valory1)-(j+20))
        
    dist = np.sqrt((230 - (20+i))**2 + (230 - (20+j))**2)
    if dist <= 40:    
        valorx1=-valorx1
        valory1=-valory1
       
  
    
    if(img.shape[0]-20-i<=0 ):
        valorx1=-random.randint(0,6)
    if(img.shape[1]-20-j<=0):
        valory1=-random.randint(0,9)
    if(i+20<=0):
         valorx1=random.randint(0,6)
    if(j+20<=0):
        valory1=random.randint(0,9)

        

            
        
    cv.imshow('¿Pong?', img)
    cv.waitKey(5)
    
    if(cv.getWindowProperty("¿Pong?", cv.WND_PROP_VISIBLE) < 1 or (i==h and j==k )):
        break
    
        

cv.waitKey(0)
cv.destroyAllWindows()

#Hacer una pelotita que rebote en las paredes
#Y luego una pelotita que esquive a la otra pelotita