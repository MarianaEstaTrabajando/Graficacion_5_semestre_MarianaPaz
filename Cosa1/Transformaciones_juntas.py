import cv2
import numpy as np

img = cv2.imread("ejemplo.jpg")
alto, ancho = img.shape[:2]

traslacion = np.zeros_like(img)
escalado = np.zeros((alto, ancho, 3), dtype=np.uint8)
rotacion = np.zeros_like(img)




# Transformaciones geométricas

alto, ancho = img.shape[:2]

# 1. Traslación
tx, ty = 50, 30

for y in range(alto):
    for x in range(ancho):
        nx = x + tx
        ny = y + ty

        if 0 <= nx < ancho and 0 <= ny < alto:
            traslacion[ny, nx] = img[y, x]


# 2. Escalamiento
sx, sy = 0.5, 0.5

for y in range(alto):
    for x in range(ancho):
        ox = int(x / sx)
        oy = int(y / sy)

        if 0 <= ox < ancho and 0 <= oy < alto:
            escalado[y, x] = img[oy, ox]


# 3. Rotación
angulo = np.deg2rad(45)
cos_t = np.cos(angulo)
sin_t = np.sin(angulo)

cx, cy = ancho // 2, alto // 2

for y in range(alto):
    for x in range(ancho):
        xt = x - cx
        yt = y - cy

        xr = int(xt * cos_t - yt * sin_t + cx)
        yr = int(xt * sin_t + yt * cos_t + cy)

        if 0 <= xr < ancho and 0 <= yr < alto:
            rotacion[yr, xr] = img[y, x]


# 4. Reflexión horizontal
reflexion = cv2.flip(img, 1)

# Mostrar 

cv2.imshow("Traslacion", traslacion)
cv2.imshow("Escalado", escalado)
cv2.imshow("Rotacion", rotacion)
cv2.imshow("Reflexion", reflexion)

cv2.waitKey(0)
cv2.destroyAllWindows()
 