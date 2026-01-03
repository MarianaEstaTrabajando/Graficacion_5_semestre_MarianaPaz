import cv2
import numpy as np
import keyboard as key
import mediapipe as mp
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Conjuntos para almacenar las coordenadas de los píxeles detectados de cada color y figura
verde= set()#Conjunto para almacenar las coordenadas de los píxeles detectados de color verde
rosa= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color rosa
rojo= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color rojo
morado= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color morado
naranja= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color naranja
amarillo= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color amarillo
azul= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color azul
cyan= set() #Conjunto para almacenar las coordenadas de los píxeles detectados de color cyan
rectangulo = set() #Conjunto para almacenar las coordenadas de los píxeles detectados de la figura rectángulo
circulo = set() #Conjunto para almacenar las coordenadas de los píxeles detect
linea=set()
triangulo=set()

#Un montón de variables globales
valor= (0,255,0) #Color inicial (verde)

lado_mitad= 20 #Mitad del lado de la figura a dibujar
altura_mitad= 20 #Mitad de la altura de la figura a dibujar
x1,x2,y1,y2,x3,y3,x4,y4,cx,cy, angle=0,0,0,0,0,0,0,0,0,0,0 #Coordenadas de la figura a dibujar
d=10


funcion= 0 #1 paint, 2 circulo, 3 rectangulo, 4 línea, 5 triángulo, 6 borrar poco, 7 borrar...

borrar= False

frame2= None


def dibujar_paint(y,x):
    if(valor==(0,255,0)):
        verde.add((y, x)) #Agregar las coordenadas al conjunto de color verde
    elif(valor==(255,0,136)):
        rosa.add((y, x)) #Agregar las coordenadas al conjunto de color rosa
    elif(valor==(0,0,255)):
        rojo.add((y, x)) #Agregar las coordenadas al conjunto de color rojo
    elif(valor==(255,0,255)):
        morado.add((y, x))  #Agregar las coordenadas al conjunto de color morado
    elif(valor==(0,136,255)):
        naranja.add((y, x)) #Agregar las coordenadas al conjunto de color naranja
    elif(valor==(0,255,255)):
        amarillo.add((y, x)) #Agregar las coordenadas al conjunto de color amarillo
    elif(valor==(255,0,0)):
        azul.add((y, x)) #Agregar las coordenadas al conjunto de color azul
    elif(valor==(255,255,0)):
        cyan.add((y, x)) #Agregar las coordenadas al conjunto de color cyan
        
def borrar_paint(y,x):
    verde.discard((y,x))
    rosa.discard((y,x))
    rojo.discard((y,x))
    morado.discard((y,x))
    naranja.discard((y,x))
    amarillo.discard((y,x))
    azul.discard((y,x))
    cyan.discard((y,x))
    
    

#dibujar_Rectángulo
def dibujar_Rectangulo():
    global y1,x1,x2,y2,x3,y3,x4,y4,d,angle
    cx=(x2+x1)/2
    cy=(y2+y1)/2
    
    #ángulo entre la línea de los puntos y el eje x
    angle = math.atan2(y2 - y1, x2 - x1)
    
    #distancia 
    d=(((x2-x1)**2+(y2-y1)**2)**(1/2))
    
    #///////////////////////
    x1= (math.cos(angle) * (-10) - math.sin(angle) * (-5))*(d/10) + cx
    y1= (math.sin(angle) * (-10) + math.cos(angle) * (-5))*(d/10)  + cy
    x2= (math.cos(angle) * (10) - math.sin(angle) * (5))*(d/10)  + cx
    y2= (math.sin(angle) * (10) + math.cos(angle) * (5))*(d/10)  + cy
    x3=(math.cos(angle) *(-10) - math.sin(angle) *(5))*(d/10)  + cx
    y3=(math.sin(angle) *(-10) + math.cos(angle) *(5))*(d/10)  + cy
    x4=(math.cos(angle) *(10) - math.sin(angle) *(-5))*(d/10)  + cx
    y4=(math.sin(angle) *(10) + math.cos(angle) *(-5))*(d/10)  + cy
    
    if(key.is_pressed('g')):
         rectangulo.add((int(x1),int(y1),int(x2),int(y2),int(x3), int(y3),int(x4),int(y4),valor))
    
    
#dibujar_Circulo
def dibujar_circulo():
    global y1,x1,y2,x2,cx,cy,d
    cx=(x2+x1)/2
    cy=(y2+y1)/2
    d=(((x2-x1)**2+(y2-y1)**2)**(1/2))
    
    if(key.is_pressed('g')):
        circulo.add((int(cx),int(cy),int(10*(d/10)), valor))
  
         

def dibujar_triangulo():
    global y1,x1,x2,y2,x3,y3,d,angle
    cx=(x2+x1)/2
    cy=(y2+y1)/2
    
    #ángulo entre la línea de los puntos y el eje x
    angle = math.atan2(y2 - y1, x2 - x1)
    
    #distancia 
    d=(((x2-x1)**2+(y2-y1)**2)**(1/2))
    
   
    x1= int ((math.cos(angle)  - math.sin(angle) * (3))*(d/5) + cx)
    y1= int((math.sin(angle)  + math.cos(angle) * (3))*(d/5)  + cy)
    x2= int((math.cos(angle) * (3) - math.sin(angle) * (-2))*(d/5)  + cx)
    y2= int((math.sin(angle) * (3) + math.cos(angle) * (-2))*(d/5)  + cy)
    x3=int((math.cos(angle) *(-3) - math.sin(angle) *(-2))*(d/5)  + cx)
    y3=int((math.sin(angle) *(-3) + math.cos(angle) *(-2))*(d/5)  + cy)
   
    
    if(key.is_pressed('g')):
         triangulo.add((int(x1),int(y1),int(x2),int(y2),int(x3), int(y3),valor))
        

    

# Inicializar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)
cv2.waitKey(2000) #Esperar 2 segundos para que la cámara se estabilice


while cap.isOpened(): #Mientras la cámara esté abierta
    ret, frame = cap.read() #Lectura del frame actual
    frame2 = frame.copy() #Hacer una copia del frame actual
    if not ret:
        break
    
    #Opciones en pantalla para seleccionar color
    cv2.rectangle(frame2, (50, 50), (100, 100), (0, 255, 0), -1) #verde
    cv2.rectangle(frame2, (50, 100), (100, 150), (255, 0, 136), -1) #rosa
    cv2.rectangle(frame2, (50, 150), (100, 200), (0, 0, 255), -1) #rojo
    cv2.rectangle(frame2, (50, 200), (100, 250), (255, 0, 255), -1) #morado
    cv2.rectangle(frame2, (50, 250), (100, 300), (0, 136, 255), -1) #naranja
    cv2.rectangle(frame2, (50, 300), (100, 350), (0, 255, 255), -1) #amarillo
    cv2.rectangle(frame2, (50, 350), (100, 400), (255, 0, 0), -1) #azul
    cv2.rectangle(frame2, (50, 400), (100, 450), (255, 255, 0), -1) #cyan
    
    
    alto=frame.shape[0] #alto de la imagen
    ancho=frame.shape[1] #ancho de la imagen
    
    #Color actual
    cv2.rectangle(frame2, (ancho-100, alto-100), (ancho-50, alto-50), valor, -1) 
    
    
    cv2.rectangle(frame2, (ancho-50, 50), (ancho-100, 100), (255, 255, 255), 2) #Cambiar a rectagulo 
    cv2.circle(frame2, (ancho-75, 125), 20, (255, 255, 255), 2) #Cambiar a círculo 
    cv2.line(frame2, (ancho-50, 150), (ancho-100, 200), (255, 255, 255), 2) #Cambiar a paint
    cv2.line(frame2, (ancho-50,225), (ancho-100, 225), (255, 255, 255), 2) #Cambiar a línea seguida
    
    #triangulo
    cv2.line(frame2,(ancho-50,250),(ancho-100,250),(255, 255, 255), 2) 
    cv2.line(frame2,(ancho-50,250),(ancho-75,300),(255, 255, 255), 2) 
    cv2.line(frame2,(ancho-100,250),(ancho-75,300),(255, 255, 255), 2) 
    
    
    
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertir la imagen a espacio de color HSV
    
    #. Definir el rango de color de la tela en HSV
    # lower_green = np.array([35, 80, 80])
    # upper_green = np.array([85, 255, 255])
    # lower_green = np.array([0, 150, 150])    
    # upper_green = np.array([10, 255, 255]) 
    
    # mask = cv2.inRange(hsv, lower_green, upper_green) #Crear una máscara 
 
    lower_blue = np.array([100, 80, 40])   # H bajo, S alto, V alto
    upper_blue = np.array([140, 255, 255])  # H alto, S máximo, V máximo

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(frame, frame, mask=mask)
    
    #Landmarks

    h, w, _ = frame.shape # Obtener dimensiones del frame

    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)
    
    #puntos para diferenciar indices de 2 manos
    xl,yl,xr,yr=None,None,None,None
    xpl,ypl=0,0

    
        
  
        
    # Dibujar puntos de la mano y dibujar figura que se escale entre pulgar e índice
    
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            
            mp_drawing.draw_landmarks(frame2, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            label = handedness.classification[0].label
            
            #Obtener coordenadas del pulgar e índice con hand_landmarks
            pulgar = hand_landmarks.landmark[4] #esto devuelde un objeto con x e y entre 0 y 1 el cual hay que multiplicar por w y h
            indice = hand_landmarks.landmark[8]

            # Coordenadas en píxeles
            x1, y1 = int(pulgar.x * w), int(pulgar.y * h) #esto convierte a pixeles
            x2, y2 = int(indice.x * w), int(indice.y * h)
            
            if(key.is_pressed('0')):
                funcion=0
            
            if(key.is_pressed('b')):
                borrar= True
            
            if(ancho-100<x2<ancho-50):
                if(50<y2<100):
                    if(borrar):
                        funcion=9
                        borrar=False
                    else:
                        funcion=3 #rectangulo
                elif(100<y2<150):
                    if(borrar):
                        funcion=8
                        borrar=False
                    else:
                        funcion=2 #circulo
                elif(150<y2<200):
                    if(borrar):
                        funcion=7
                        borrar=False
                    else:
                        funcion=1 #paint
                elif(200<y2<250):
                    if(borrar):
                        funcion=10
                        borrar=False
                    else:
                        funcion=4 #linea
                elif(250<y2<300):
                    if(borrar):
                        funcion=11
                        borrar=False
                    else:
                        funcion=5 #triangulo
            
            if(funcion==3):
                dibujar_Rectangulo()
                frame2= cv2.line(frame2, (int(x1), int(y1)), (int(x3), int(y3)), valor,3) #1 y 3
                frame2= cv2.line(frame2, (int(x2), int(y2)), (int(x4), int(y4)), valor,3) #2 y 4
                frame2= cv2.line(frame2, (int(x1), int(y1)), (int(x4), int(y4)), valor,3) #1 y 4
                frame2= cv2.line(frame2, (int(x2), int(y2)), (int(x3), int(y3)), valor,3) #2 y 3
            
            if(funcion==2):
                dibujar_circulo()
                frame2=cv2.circle(frame2,(int(cx),int(cy)),int(10*(d/10)),valor,3)
            
            if(funcion==4): #línea recta con los 2 dedos
                
                if label == 'Left':
                    xl,yl=x2,y2
                    xpl,ypl=x1,y1
                elif label == 'Right':
                    xr,yr=x2,y2
                    
                if xl and yl and xr and yr:
                    frame2= cv2.line(frame2, (int(xl), int(yl)), (int(xr), int(yr)), valor,3) #1 y 2
                    
                    if(xpl,ypl):
                        if(abs(xpl-xl)<4):
                            linea.add((xl,yl,xr,yr,valor ))
                    
                    if(key.is_pressed('g')):
                        linea.add((xl,yl,xr,yr,valor ))
                        
            if(funcion==5):
                dibujar_triangulo()
                frame2= cv2.line(frame2, (x1, y1), (x2, y2), valor,3) #1 y 2
                frame2= cv2.line(frame2, (x2, y2), (x3, y3), valor,3) #2 y 3
                frame2= cv2.line(frame2, (x3, y3), (x1, y1), valor,3) #3 y 1
                
                
            
            if(funcion==7):
                verde.clear()
                rosa.clear()
                rojo.clear()
                morado.clear()
                naranja.clear()
                amarillo.clear()
                azul.clear()
                cyan.clear()
            
            if(funcion==8):
                circulo.clear()
                
            if(funcion==9):
                rectangulo.clear()
                
            if(funcion==10):
                linea.clear()
            
            if(funcion==11):
                triangulo.clear()
    
    #Rectángulo rotandose y eso
    if(funcion==0 or funcion==1 or funcion==4):
        #Ciclo para procesar las coordenadas detectadas
        coords = np.column_stack(np.where(mask == 255))
        for y, x in coords:
            
            if(funcion==1):
                dibujar_paint(y,x)
                
            if(funcion==4):
                borrar_paint(y,x)
                        
            if(funcion==1 or funcion==0):
                #Cambio de color al tocar la paleta
                if(50<x<100): #Si el píxel está en la zona de selección de color
                    if(50<y<100):
                        valor=(0,255,0)
                    elif(100<y<150):  
                        valor=(255,0,136)
                    elif(150<y<200):    
                        valor=(0,0,255)
                    elif(200<y<250):
                        valor=(255,0,255)
                    elif(250<y<300):
                        valor=(0,136,255)
                    elif(300<y<350):
                        valor=(0,255,255)
                    elif(350<y<400):
                        valor=(255,0,0)
                    elif(400<y<450):
                        valor=(255,255,0)
                    
    
    #Pintar los pixeles detectados de cada color que ya fueron almacenados
    #coords = np.column_stack(np.where(mask == 255))
    for i in verde: 
        frame2[i[0],i[1]]= (0,255,0)#Pintar los pixeles detectados del color
    for i in rosa: 
        frame2[i[0],i[1]]=(255,0,136)
    for i in rojo: 
        frame2[i[0],i[1]]= (0,0,255)
    for i in morado: 
        frame2[i[0],i[1]]= (255,0,255)
    for i in naranja: 
        frame2[i[0],i[1]]= (0,136,255)
    for i in amarillo:
        frame2[i[0],i[1]]= (0,255,255)
    for i in azul: 
        frame2[i[0],i[1]]= (255,0,0)
    for i in cyan: 
        frame2[i[0],i[1]]= (255,255,0)
    for i in rectangulo:
        frame2= cv2.line(frame2, (i[0], i[1]), (i[4], i[5]), i[8],3) #1 y 3
        frame2= cv2.line(frame2, (i[2], i[3]), (i[6], i[7]), i[8],3) #2 y 4
        frame2= cv2.line(frame2, (i[0], i[1]), (i[6], i[7]), i[8],3) #1 y 4
        frame2= cv2.line(frame2, (i[2], i[3]), (i[4], i[5]), i[8],3) #2 y 3
    for i in circulo:
        frame2= cv2.circle(frame2, (i[0], i[1]), i[2], i[3], 3) #Dibujar el círculo almacenado
    
    for i in linea:
        frame2= cv2.line(frame2, (i[0], i[1]), (i[2], i[3]), i[4],3) #1 y 2
    
    for i in triangulo:
        frame2= cv2.line(frame2, (i[0], i[1]), (i[2], i[3]), i[6],3) #1 y 2
        frame2= cv2.line(frame2, (i[2], i[3]), (i[4], i[5]), i[6],3) #2 y 3
        frame2= cv2.line(frame2, (i[4], i[5]), (i[0], i[1]), i[6],3) #3 y 1
     
    
    cv2.imshow("Seguimiento", frame2) #Mostrar el video con el seguimiento
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("Seguimiento", cv2.WND_PROP_VISIBLE) < 1:
        break


#. Liberar los recursos
cap.release()
cv2.destroyAllWindows()

