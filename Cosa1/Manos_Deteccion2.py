import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
pulgar = None
indice = None

# Dibujar una línea entre el pulgar y el índice

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Obtener dimensiones del frame
    h, w, _ = frame.shape

    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)

    # Dibujar puntos de la mano y dibujar línea entre pulgar e índice
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            #Obtener coordenadas del pulgar e índice con hand_landmarks
            pulgar = hand_landmarks.landmark[4] #esto devuelde un objeto con x e y entre 0 y 1 el cual hay que multiplicar por w y h
            indice = hand_landmarks.landmark[8]

            # Coordenadas en píxeles
            x1, y1 = int(pulgar.x * w), int(pulgar.y * h) #esto convierte a pixeles
            x2, y2 = int(indice.x * w), int(indice.y * h)

        cv2.line(frame,(x1, y1),(x2, y2),(255,0,0),2)   # Línea entre pulgar e índice     
            

    # Mostrar el video
    cv2.imshow("Línea fea", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
