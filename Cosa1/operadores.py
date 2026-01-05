import cv2
import numpy as np

# Cargar imagen
img = cv2.imread("ejemplo.jpg")
if img is None:
    print("No se pudo cargar la imagen")
    exit()

# Convertir a escala de grises para operadores puntuales
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Operadores puntuales

# 1. Negativo
negativo = 255 - gray

# 2. Aumento de brillo
brillo_alto = cv2.add(gray, 50)

# 3. Disminución de brillo
brillo_bajo = cv2.subtract(gray, 50)

# 4. Aumento de contraste
contraste = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

# 5. Umbralización
_, umbral = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)



# Mostrar resultados
cv2.imshow("Original", img)
cv2.imshow("Negativo", negativo)
cv2.imshow("Brillo +", brillo_alto)
cv2.imshow("Brillo -", brillo_bajo)
cv2.imshow("Contraste", contraste)
cv2.imshow("Umbral", umbral)



cv2.waitKey(0)
cv2.destroyAllWindows()
