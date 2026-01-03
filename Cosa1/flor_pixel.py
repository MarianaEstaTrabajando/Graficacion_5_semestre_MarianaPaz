import numpy as np
import cv2 as cv


#Usar solo pixeles para hacer una florecita
# Imagen blanca
img = np.ones((500, 500,3), dtype=np.uint8) * 255

# Centro de la flor
cx, cy = 250, 250

# Color (gris oscuro)
petalo = (203, 192, 255)  
centro = (0, 255, 255)    
tallo = (0, 255, 0)       

#Tallo
for i in range(250, 380):
    img[i, cy] = tallo
    img[i, cy+1] = tallo
    img[i, cy-1] = tallo
    
# Centro de la flor
for i in range(-15, 16):
    for j in range(-15, 16):
        if i*i + j*j <= 150:
            img[cx+i, cy+j] = centro

#Pétalos
for i in range(-800, 800):
    for j in range(-800, 800):
        if i*i + j*j <= 800:
            img[cx-40+i, cy+j] = petalo  # arriba
            img[cx+40+i, cy+j] = petalo  # abajo
            img[cx+i, cy-40+j] = petalo  # izquierda
            img[cx+i, cy+40+j] = petalo  # derecha





# Mostrar imagen
cv.imshow("Flor pixel art", img)
cv.waitKey(0)
cv.destroyAllWindows()
