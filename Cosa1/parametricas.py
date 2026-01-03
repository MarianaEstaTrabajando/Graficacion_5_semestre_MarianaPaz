import math
import cv2 as cv
import numpy as np
import random as rnd

# Dimensiones del lienzo donde se dibujan las figuras
canvas_w, canvas_h = 800, 800
mid_x, mid_y = canvas_w // 2, canvas_h // 2

# Crear tres lienzos negros independientes para cada curva
frame_epitrocoide = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
frame_estrellada = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
frame_armonica = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
frame_spiral = np.zeros((canvas_h, canvas_w, 3), np.uint8)
frame_rose = np.zeros((canvas_h, canvas_w, 3), np.uint8)
frame_lemniscata = np.zeros((canvas_h, canvas_w, 3), np.uint8)
frame_spiro = np.zeros((canvas_h, canvas_w, 3), np.uint8)
frame_butterfly = np.zeros((canvas_h, canvas_w, 3), np.uint8)
frame_epi = np.zeros((canvas_h, canvas_w, 3), np.uint8)
frame_chaos = np.zeros((canvas_h, canvas_w, 3), np.uint8)


# Factor de escala general para todas las figuras
base_size = 180

# Parámetro temporal que controla el avance de las curvas
t = 0.0

# Parámetros de la curva estrellada (variante de hipocicloide)
lobes = 8                      # número de picos visibles
R_ext = base_size              # radio del círculo externo
r_int = base_size / lobes      # radio del círculo interno

while True:
    # Seleccionar un color RGB distinto en cada iteración
    

    # 1. Curva tipo cardioide modificada usando una variación polar
    # Se altera la amplitud para cambiar la forma sin perder continuidad
    radius = base_size * (1 - 0.5 * math.sin(t))
    
    px = int(mid_x + radius * math.cos(t))
    py = int(mid_y + radius * math.sin(t))
    
    cv.circle(frame_epitrocoide, (px, py), 3, (0,255,255), -1)

    # 2. Curva estrellada generada por rodamiento interno
    # Se ajusta el signo y la relación angular para variar el patrón
    x_star = int(
        mid_x
        + (R_ext - r_int) * math.cos(t)
        + r_int * math.cos((R_ext / r_int) * t)
    )
    y_star = int(
        mid_y
        + (R_ext - r_int) * math.sin(t)
        - r_int * math.sin((R_ext / r_int) * t)
    )

    cv.circle(frame_estrellada, (x_star, y_star), 3, (140,45,255), -1)

    # 3. Curva armónica tipo Lissajous con desfase angular
    # Se introduce un pequeño desfase para romper simetría perfecta
    x_wave = int(mid_x + 160 * math.sin(4 * t + math.pi / 6))
    y_wave = int(mid_y + 160 * math.sin(7 * t))
    
    cv.circle(frame_armonica, (x_wave, y_wave), 3, (255,255,0), -1)

    # Avanzar el parámetro temporal para animación continua
    t += 0.08

    
        # 4. Espiral logarítmica
    # El radio crece exponencialmente con el parámetro temporal
    spiral_r = 2 * math.exp(0.08 * t)
    x_spiral = int(mid_x + spiral_r * 10* math.cos(t))
    y_spiral = int(mid_y + spiral_r *10* math.sin(t))
    cv.circle(frame_spiral, (x_spiral, y_spiral), 2, (0,255,255), -1)


    # 5. Rosa polar (curva de pétalos)
    # El número de pétalos depende del factor k
    k_petals = 5
    rose_r = base_size * math.cos(k_petals * t)
    x_rose = int(mid_x + rose_r * math.cos(t))
    y_rose = int(mid_y + rose_r * math.sin(t))
    cv.circle(frame_rose, (x_rose, y_rose), 3, (140,45,255), -1)


    # 6. Lemniscata de Bernoulli
    # Curva en forma de infinito usando trigonometría racional
    denom = 1 + math.sin(t) ** 2
    x_lem = int(mid_x + (base_size * math.cos(t)) / denom)
    y_lem = int(mid_y + (base_size * math.sin(t) * math.cos(t)) / denom)
    cv.circle(frame_lemniscata, (x_lem, y_lem), 3,  (255,255,0), -1)


    # 7. Espirografo generalizado
    # Variante más libre combinando radios y velocidades
    x_spiro = int(
        mid_x
        + (base_size - 40) * math.cos(t)
        + 200 * math.cos(6 * t)
    )
    y_spiro = int(
        mid_y
        + (base_size - 40) * math.sin(t)
        - 200 * math.sin(6 * t)
    )
    cv.circle(frame_spiro, (x_spiro, y_spiro), 2, (0,255,255), -1)


    # 8. Curva paramétrica tipo mariposa
    # Produce una figura caótica pero cerrada
    x_butter = int(mid_x + base_size * math.sin(t) * math.exp(math.cos(t)))
    y_butter = int(mid_y + base_size * math.cos(t) * math.exp(math.sin(t)))
    cv.circle(frame_butterfly, (x_butter, y_butter), 2, (140,45,255), -1)


    # 9. Curva de epitrocoide
    # El círculo rueda por fuera del principal
    R_out = base_size
    r_roll = base_size / 4
    x_epi = int(
        mid_x
        + (R_out + r_roll) * math.cos(t)
        - r_roll * math.cos(((R_out + r_roll) / r_roll) * t)
    )
    y_epi = int(
        mid_y
        + (R_out + r_roll) * math.sin(t)
        - r_roll * math.sin(((R_out + r_roll) / r_roll) * t)
    )
    cv.circle(frame_epi, (x_epi, y_epi), 3,  (255,255,0), -1)


    # 10. Curva caótica seno-coseno
    # Se mezclan frecuencias no armónicas
    x_chaos = int(mid_x + 170 * math.sin(t * math.sqrt(2)))
    y_chaos = int(mid_y + 170 * math.cos(t * math.pi))
    cv.circle(frame_chaos, (x_chaos, y_chaos), 2, (255,255,255), -1)

    # Mostrar cada curva en su propia ventana
    cv.imshow("Curva Armónica", frame_armonica)
    cv.imshow(f"Curva Estrellada ({lobes} picos)", frame_estrellada)
    cv.imshow("Curva Polar Modificada", frame_epitrocoide)
    cv.imshow("Curva espiral", frame_spiral)
    cv.imshow("Curva rosa", frame_rose)
    cv.imshow("Curva lemniscata", frame_lemniscata)
    cv.imshow("Curva espiro", frame_spiro)
    cv.imshow("Curva mariposa", frame_butterfly)
    cv.imshow("Curva epicicloide", frame_epi)
    cv.imshow("Curva caos", frame_chaos)

    # Finalizar el programa al presionar ESC
    if cv.waitKey(2) & 0xFF == 27:
        break

# Cerrar todas las ventanas al terminar
cv.destroyAllWindows()
