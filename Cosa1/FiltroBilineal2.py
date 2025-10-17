import cv2 as cv
import numpy as np
import math

# Cargar la imagen en escala de grises
img = cv.imread('ejemplo.jpg', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Crear una imagen vacía para almacenar el resultado
escaleted_img1 = np.zeros((x, y), dtype=np.uint8)
xx, yy = escaleted_img1.shape

rotated_es_img1 = np.zeros((x, y), dtype=np.uint8)
xx, yy = rotated_es_img1.shape

escaleted_img1Filtro = np.zeros((x, y), dtype=np.uint8)
xx, yy = escaleted_img1Filtro.shape

rotated_es_img1Filtro = np.zeros((x, y), dtype=np.uint8)
xx, yy = rotated_es_img1Filtro.shape

# Calcular el centro de la imagen
cx, cy = int(x  // 2), int(y  // 2)

# Definir el ángulo de rotación (en grados) y convertirlo a radianes
angle = 45
theta = math.radians(angle)

# Escalar la imagen
for i in range(x):
    for j in range(y):
        new_x = j*2
        new_y = i*2
        if 0 <= new_x < y and 0 <= new_y < x:
            escaleted_img1[new_y, new_x] = img[i, j]
         

# Rotar la imagen
for i in range(x):
    for j in range(y):
        new_x = int((i*math.cos(theta )+(j*math.sin(theta))))
        new_y = int(((j*math.cos(theta )-(i*math.sin(theta)))))
        if 0 <= new_x < y and 0 <= new_y < x:
           rotated_es_img1[new_y, new_x] = escaleted_img1[i, j]
#Filtro Bilineal
for i in range(1, xx-1):
    for j in range(2, yy-2):
        a = rotated_es_img1[i, j]
        b = rotated_es_img1[i, j+1]
        c = rotated_es_img1[i+1, j]
        d = rotated_es_img1[i+1, j+1]
        e=rotated_es_img1[i, j-1]
        f=rotated_es_img1[i-1, j]
        g=rotated_es_img1[i-1, j-1]
        h=rotated_es_img1[i-1, j+1]
        k=rotated_es_img1[i+1, j-1]
        l=rotated_es_img1[i, j-1]
        m= (a + b + c + d+f+g+h+k+l) / 9
        rotated_es_img1Filtro[i, j] = int(m)   

# Mostrar la imagen original y la rotada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada ', escaleted_img1)
cv.imshow('Imagen Rotada y Escalada ', rotated_es_img1)
cv.imshow('Imagen Rotada y Escalada (Filtro Bilineal)', rotated_es_img1Filtro)
cv.waitKey(0)
cv.destroyAllWindows()