import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
indice = None
num1,num2, mult=0,0,1
result='0'
op=''
val, continuar=True, True
# Calculadora manual con numeros en pantalla que señalas con el dedo índice

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
    ancho_alto,baseLine= cv2.getTextSize('1', cv2.FONT_HERSHEY_SIMPLEX, 2, 2) #estimar espacio entre numeros
    ancho, alto = ancho_alto
    # Dibujar números y operaciones en la pantalla
    cv2.putText(frame, '0', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '1', (10+(ancho), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '2', (10+int(ancho*2), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, '3', (10+int(ancho*3), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '4', (10+int(ancho*4), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '5', (10+int(ancho*5), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '6', (10+int(ancho*6), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '7', (10+int(ancho*7), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '8', (10+int(ancho*8), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '9', (10+int(ancho*9), 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 100), 2, cv2.LINE_AA)
    cv2.putText(frame, '+', (int(w-ancho)-10, int(100+alto)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, '-', (int(w-ancho)-10, int(100+(alto*2))), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, '*', (int(w-ancho)-10, int(100+(alto*3))), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, '/', (int(w-ancho)-10, int(100+(alto*4))), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, '^', (int(w-ancho)-10, int(100+(alto*5))), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, '=', (int(w-ancho-10)-10, int(h-alto-10)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100), 2, cv2.LINE_AA)
    # Dibujar puntos de la mano y presionar con índice
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar los puntos de la mano
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            #Obtener coordenadas del índice con hand_landmarks
            indice = hand_landmarks.landmark[8]
            x,y = int(indice.x * w), int(indice.y * h) #Convertir a coordenadas de píxeles
            i=0
            # Detectar si el índice está presionando algún número u operación
            # Revisar números del 0 al 9
            for i in range(0,10):
                # Guardar el número i que está siendo presionado
                if(10+int(ancho*(i))<x<10+int(ancho*i+1)) and (50-alto<y<50+baseLine): #Rango del número i
                    if(val):
                        num1=(num1*10)+i #El número anterior guardado en num1 se multiplica por 10 y se le suma el nuevo dígito
                        result=str(num1)
                        
                    else:
                        num2=(num2*10)+i #El número anterior guardado en num2 se multiplica por 10 y se le suma el nuevo dígito
                        result=str(num2)
                # Salir del ciclo si ya se ha detectado una operación    
                if(x>10+int(ancho*10)) and (50-alto<y<50+baseLine):
                    break
            # Revisar operaciones
            if(int(w-ancho)-10<x<w) and (100+alto<y<100+(alto*2)):
                op='+'
                val=False # Ahora se ingresará el segundo número
                result='+'
            if(int(w-ancho)-10<x<w) and (100+(alto*2)<y<100+(alto*3)):
                op='-'
                val=False
                result='-'
            if(int(w-ancho)-10<x<w) and (100+(alto*3)<y<100+(alto*4)):
                op='*'
                val=False
                result='*'
            if(int(w-ancho)-10<x<w) and (100+(alto*4)<y<100+(alto*5)):
                op='/'
                val=False
                result='/'
            if(int(w-ancho)-10<x<w) and (100+(alto*5)<y<100+(alto*6)):
                op='^'
                val=False
                result='^'
            # Revisar igual y realizar la operación
            if(int(w-ancho-10)-10<x<int(w-10)) and (h-alto-10<y<h-10):
                if op=='+':
                    num1=num1+num2
                    result=str(num1)
                elif op=='-':
                    num1=num1-num2
                    result=str(num1)
                elif op=='*':
                    num1=num1*num2
                    result=str(num1)
                elif op=='/':
                    num1=num1/num2
                    result=str(num1)
                elif op=='^':
                    num1=num1**num2
                    result=str(num1)
    # Mostrar el resultado o los números o la operación en la pantalla            
    cv2.putText(frame, f'Resultado: {result}', (10, h-100-ancho), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100, 0), 2, cv2.LINE_AA)
    # Mostrar el video
    cv2.imshow("Calculadora manual", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
