import cv2 as cv
import numpy as np
import math

# Cargar clasificador de rostros
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)

# Variables de animación
parpadeo = 0
duracion_parpadeo = 5
mov_pupila = 0
boca_abierta = 0
direccion_boca = 1

while True:
    ret, imagen = cap.read()
    gris = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros:
       
        cv.rectangle(imagen, (x, y), (x + w, y + h), (234, 23, 23), 5)
        cv.rectangle(imagen, (x, int(y + h/2)), (x + w, y + h), (0, 255, 0), 5)

        # Parpadeo
        alto_ojo = 20
        if parpadeo > 0:
            alto_ojo = 2

        # Ojos
        ojo_izq = (x + int(w*0.3), y + int(h*0.4))
        ojo_der = (x + int(w*0.7), y + int(h*0.4))
        cv.ellipse(imagen, ojo_izq, (20, alto_ojo), 0, 0, 360, (255,255,255), -1)
        cv.ellipse(imagen, ojo_der, (20, alto_ojo), 0, 0, 360, (255,255,255), -1)

        # Pupilas 
        desplazamiento_x = int(5 * math.sin(mov_pupila))
        desplazamiento_y = int(3 * math.sin(mov_pupila/2))
        cv.circle(imagen, (ojo_izq[0] + desplazamiento_x, ojo_izq[1] + desplazamiento_y), 5, (0, 0, 255), -1)
        cv.circle(imagen, (ojo_der[0] + desplazamiento_x, ojo_der[1] + desplazamiento_y), 5, (0, 0, 255), -1)

        # Orejas
        cv.rectangle(imagen, (x - int(0.1*w), y + int(0.3*h)), (x, y + int(0.7*h)), (0, 0, 255), 5)
        cv.rectangle(imagen, (x + w, y + int(0.3*h)), (x + w + int(0.1*w), y + int(0.7*h)), (0, 0, 255), 2)

        # Nariz
        cv.circle(imagen, (x + int(w*0.5), y + int(h*0.53)), 30, (0, 0, 255), -1)

        # Boca animada
        altura_boca = int(h*0.1 * boca_abierta)
        cv.ellipse(imagen, (x + int(w*0.5), y + int(h*0.75)), (int(w*0.2), altura_boca + 5), 0, 0, 180, (0,0,0), -1)

    # Mostrar imagen
    cv.imshow('cara', imagen)

    # Animaciones feas
    parpadeo = max(0, parpadeo - 1)
    mov_pupila += 0.2
    boca_abierta += 0.1 * direccion_boca
    if boca_abierta > 1 or boca_abierta < 0:
        direccion_boca *= -1

    # Parpadeo raro
    if np.random.rand() < 0.02 and parpadeo == 0:
        parpadeo = duracion_parpadeo

    if cv.waitKey(30) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
