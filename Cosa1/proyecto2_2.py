import glfw
import cv2
import mediapipe as mp
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ============================================================
# Configuración
# ============================================================
#WINDOW_WIDTH
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Mascara 3D Extendida + Mediapipe"

# Conexiones para dibujar el contorno facial
contorno_cara  = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
             397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
             172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

# Cejas
LEFT_EYEBROW = [70, 63, 105, 66, 107]
RIGHT_EYEBROW = [336, 296, 334, 293, 300]

def init_glfw():
    if not glfw.init():
        raise Exception("No se pudo inicializar GLFW")
    
 # Crear ventana GLFW
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
    
    if not window:
        glfw.terminate()
        raise Exception("No se pudo crear la ventana GLFW")
    
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    return window

# ============================================================
# Configuracion inicial de OpenGL
# ============================================================

# Ajustes iniciales de OpenGL
def setup_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

def create_video_texture():
    video_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return video_tex

def setup_lights():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)  # Luz adicional
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Luz principal frontal
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))
    
    # Luz de relleno lateral
    glLightfv(GL_LIGHT1, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))

# ============================================================
# Funciones de dibujo
# ============================================================
def draw_sphere(x, y, z, radius, color=(1, 1, 1)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_line(p1, p2, color=(1, 1, 1), width=2.0):
    """Dibuja una línea entre dos puntos 3D"""
    glDisable(GL_LIGHTING)
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex3f(*p1)
    glVertex3f(*p2)
    glEnd()
    glEnable(GL_LIGHTING)
    
# def draw_paraboloide(h,k,w, p, m=4,radio_r=100,angulo_r=360,color=(1,1,1)):
#     glPushMatrix()
#     try:
#         glTranslatef(h, k, w)
#         glColor3f(*color)
        
#         glBegin(GL_TRIANGLE_STRIP)
#         for i in range(radio_r):
#             for angulo in range(angulo_r):
#                 rad=math.radians(angulo)
#                 x1=i*math.cos(rad)
#                 y1=(-(i**2)+p)/m
#                 z1= i*math.sin(rad)
                
                
#                 x2 = (i+1) * math.cos(rad)
#                 y2 = ( -((i+1)**2) + p ) / m
#                 z2 = (i+1) * math.sin(rad)
                

#                 glVertex3f(x1, y1, z1)
#                 glVertex3f(x2, y2, z2)
#         glEnd()
#     finally:
#         glPopMatrix()



#El paraboloide pasado quedaba como un cono, así que use este que funciona mucho mejor y sí tiene la forma del pou
#Se usará para el cuerpo y la boca

def draw_paraboloide(h, k, w, altura=1.0, radio_max=1.0, pasos_r=80, pasos_ang=80,color=(1,1,1)):
    
    glPushMatrix()
    try:
        glTranslatef(h, k, w)
        glColor3f(*color)  
        for i in range(pasos_r):
            r1 = (i / pasos_r) * radio_max
            r2 = ((i + 1) / pasos_r) * radio_max

            glBegin(GL_TRIANGLE_STRIP)
            for j in range(pasos_ang + 1):
                theta = 2 * math.pi * j / pasos_ang

                # Primer radio
                x1 = r1 * math.cos(theta)
                z1 = r1 * math.sin(theta)
                y1 = -(r1 **2) / altura

                # Segundo radio
                x2 = r2 * math.cos(theta)
                z2 = r2 * math.sin(theta)
                y2 = -(r2 ** 2) / altura

                
                glNormal3f(x1, y1, z1)
                glVertex3f(x1, y1, z1)
                glNormal3f(x2, y1, z2)
                glVertex3f(x2, y2, z2)

            glEnd()

    finally:
        glPopMatrix()




def draw_parpado(x,y,z,radius,inicio, cerrado, color=(1,1,1), slices=30, stacks=30):
    #Utilizando la función de dibujar esfera del código del ojo, aproveché que funcionaba con rebanadas para hacer el parpado
    """Dibuja una esfera usando primitivas OpenGL (sin GLUT)"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    quad = gluNewQuadric()
    #Dependiendo de los valores de inicio y cerrado, se dibuja el parpado
    for i in range(inicio,stacks-cerrado):
        lat1 = math.pi * (-0.5 + i / stacks)
        lat2 = math.pi * (-0.5 + (i + 1) / stacks)
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * j / slices
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            x2 = math.cos(lat2) * math.cos(lng)
            y2 = math.sin(lat2)
            z2 = math.cos(lat2) * math.sin(lng)
            
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radius, y1 * radius, z1 * radius)
            
            glNormal3f(x2, y2, z2)
            glVertex3f(x2 * radius, y2 * radius, z2 * radius)
        glEnd()
    glPopMatrix()
        


def norm_landmark(p):
    return ((p.x - 0.5)*2, -2*(p.y - 0.5), (p.z)*2)

# ============================================================
# Renderizado
# ============================================================
def render_video_background(frame_rgb, video_tex):
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glBindTexture(GL_TEXTURE_2D, video_tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 
                 frame_rgb.shape[1], frame_rgb.shape[0],
                 0, GL_RGB, GL_UNSIGNED_BYTE, frame_rgb)
    
    glColor3f(1.0, 1.0, 1.0)
    
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(0, 0)
    glTexCoord2f(1, 1); glVertex2f(1, 0)
    glTexCoord2f(1, 0); glVertex2f(1, 1)
    glTexCoord2f(0, 0); glVertex2f(0, 1)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_face_contour(landmarks, indices, color=(0.3, 0.8, 0.4)):
    glDisable(GL_LIGHTING)
    glLineWidth(1.5)
    glColor3f(*color)
    
    glBegin(GL_LINE_STRIP)
    for idx in indices:
        p = norm_landmark(landmarks[idx])
        glVertex3f(*p)
    # Cerrar el contorno
    p = norm_landmark(landmarks[indices[0]])
    glVertex3f(*p)
    glEnd()
    
    glEnable(GL_LIGHTING)

def render_3d_mask_extended(face_landmarks):
    """Renderiza la máscara 3D extendida"""
    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 100)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0, 0, 2, 0, 0, 0, 0, 1, 0)
    
    setup_lights()
    
    lm = face_landmarks.landmark
    
 
    
    # ============================================================
    # 2. OJOS
    # ============================================================
    
    # left_eye = lm[386]
    # right_eye = lm[159]
    
    # Globos oculares (blancos)
    
    lx1,ly1,lz1= norm_landmark(lm[133])
    lx2,ly2,lz2= norm_landmark(lm[33])
    
    rx1,ry1,rz1= norm_landmark(lm[362])
    rx2,ry2,rz2= norm_landmark(lm[263])
    
    radiusl=abs(lx2-lx1)/1.15
    radiusr=abs(rx2-rx1)/1.15
    
    lx, ly, lz = ((lx1+lx2)/2),((ly1+ly2)/2),((lz1+lz2)/2)
    rx, ry, rz = ((rx1+rx2)/2), ((ry1+ry2)/2), ((rz1+rz2)/2)
    
    distancia_cuerpo_z= radiusr*3
    
    glColor3f(1.0, 1.0, 1.0)
    draw_sphere(lx, ly, lz, radiusl, (1, 1, 1))
    draw_sphere(rx, ry, rz,radiusr, (1, 1, 1))
    
    # Púpila
                                
    rx1,ry1,rz1= norm_landmark(lm[474])
    
    radiusl=radiusl*0.8
    radiusr=radiusr*0.8
    
    glColor3f(0.0, 0.0, 0.0)
    draw_sphere(lx, ly, lz+(radiusl/2),radiusl, (0, 0, 0))
    draw_sphere(rx, ry, rz+(radiusr/2),radiusr ,(0, 0, 0))
    
    #Brillo de la púpila

    dl=radiusl/3
    radiusl=radiusl*0.4
    
    dr=radiusr/3
    radiusr=radiusr*0.4
    
    draw_sphere(lx+dl, ly+dl, lz+(radiusl*2.5), radiusl, (1, 1, 1))
    draw_sphere(rx+dr, ry+dr, rz+ (radiusr*2.5),radiusr,(1, 1, 1))
    
    # ============================================================
    # Parpados
    # ============================================================
    
    #Movimiento puntos del parpado como tal:
    left_eye_p1 = lm[386]
    left_eye_p2 = lm[374]
    
    right_eye_p1 = lm[159]
    right_eye_p2 = lm[145]
    
    
    
    lx1p, ly1p, lz1p = norm_landmark(left_eye_p1)
    lx2p, ly2p, lz2p = norm_landmark(left_eye_p2)
    
    rx1p, ry1p, rz1p = norm_landmark(right_eye_p1)
    rx2p, ry2p, rz2p = norm_landmark(right_eye_p2)
    
    
    #Posición de la parte blanca para calcular el radio del parpado
    lx1,ly1,lz1= norm_landmark(lm[133])
    lx2,ly2,lz2= norm_landmark(lm[33])
    
    rx1,ry1,rz1= norm_landmark(lm[362])
    rx2,ry2,rz2= norm_landmark(lm[263])
    
    radiusl=abs(lx2-lx1)
    radiusr=abs(rx2-rx1)
    
    #Centro
    lx, ly, lz = ((lx1+lx2)/2),((ly1+ly2)/2),((lz1+lz2)/2)
    rx, ry, rz = ((rx1+rx2)/2), ((ry1+ry2)/2), ((rz1+rz2)/2)
    
    #Posición puntos de los lagrimales para poder medir las distancias de los ojos y redimensionar, usé esto para comparar esta distancia 
    #que no cambia con la de los parapados que pues sí cambia al parpadear
    lx1,ly1,lz1= norm_landmark(lm[107])
    lx2,ly2,lz2= norm_landmark(lm[46])
    
    rx1,ry1,rz1= norm_landmark(lm[336])
    rx2,ry2,rz2= norm_landmark(lm[276])
    
    #Parpadeo, aquí se calcula la distancia de los lagrimales
    distancia_parpadol=abs(ly2-ly1)
    distancia_parpador=abs(ry2-ry1)
    
    
    #Aquí se usa la distancia de los lagrimales para calcular el valor del parpadeo ya que este va por rebanadas su valor máximo es 30
    #Pero usé 30 originalmente y pues no quedó bien xd así que lo fui cambiando
    valorl= int(abs(ly2p-ly1p)*45/distancia_parpadol)
    valorr= int(abs(ry2p-ry1p)*45/distancia_parpador)
    
    glColor3f(1.0, 1.0, 1.0)
    draw_parpado(lx, ly, lz,radiusl,valorl,0,(0.54, 0.36, 0.23))
    draw_parpado(lx, ly, lz,radiusl,0,valorl,(0.54, 0.36, 0.23))
    
    draw_parpado(rx, ry, rz,radiusr,valorr,0,(0.54, 0.36, 0.23))
    draw_parpado(rx, ry, rz, radiusr,0,valorr,(0.54, 0.36, 0.23))
    
    
    
    # ============================================================
    # 3. CEJAS
    # ============================================================
    draw_face_contour(lm, LEFT_EYEBROW, color=(0.3, 0.2, 0.1))
    draw_face_contour(lm, RIGHT_EYEBROW, color=(0.3, 0.2, 0.1))
    
    # Agregar esferas a las  cejas para hacerlas mas visibles
    for idx in LEFT_EYEBROW[::2]:  # Cada dos puntos
        px, py, pz = norm_landmark(lm[idx])
        draw_sphere(px, py, pz, 0.008, (0.4, 0.3, 0.2))
    
    for idx in RIGHT_EYEBROW[::2]:
        px, py, pz = norm_landmark(lm[idx])
        draw_sphere(px, py, pz, 0.008, (0.4, 0.3, 0.2))
        

    
 
    
    # ============================================================
    # 5. BOCA
    # ============================================================
    
    #draw_paraboloide(fx,fy,distancia_cuerpo_z,5*abs(cy-fy)/9,0.8*abs(cy-fy),80,80,(0.54, 0.36, 0.23))
    #def draw_paraboloide(h, k, w, altura=1.0, radio_max=1.0, pasos_r=80, pasos_ang=80,color=(1,1,1))   
    mouth_left = lm[61]
    mouth_right = lm[291]
    mouth_top = lm[13]
    mouth_bottom = lm[14]
    
    mlx, mly, mlz = norm_landmark(mouth_left)
    mrx, mry, mrz = norm_landmark(mouth_right)
    mtx, mty, mtz = norm_landmark(mouth_top) #labio superior
    mbx, mby, mbz = norm_landmark(mouth_bottom) #labio inferior
    

    
    #Boca
    draw_paraboloide(mtx,mty,lz,5*abs(mty-mby)/9, 0.8*abs(mty-mby),80,80,(1, 0.3, 0.50))
    

    
     # ============================================================
    # 7. Cuerpo
    # ============================================================
    
    #Estas distancias fueron variando mucho hasta que quedó bien
    forehead = lm[10]
    chin = lm[152]
    
    fx, fy, fz = norm_landmark(forehead)
    cx, cy, cz = norm_landmark(chin)
    
    #Este valor toma en cuenta a los ojos ya que el cuerpo debe estar atrás de ellos y antes no quedaba bien 
    distancia_cuerpo_z=distancia_cuerpo_z- (abs(cy - fy) *0.8)
    
    # Punto en la frente (color suave)
    draw_paraboloide(fx,fy,distancia_cuerpo_z,5*abs(cy-fy)/9,0.8*abs(cy-fy),80,80,(0.54, 0.36, 0.23))
    

    
    # Restaurar matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
  
    
   


# ============================================================
# Función principal
# ============================================================
def main():
    
    try:
        window = init_glfw()
    except Exception as e:
        print(f" Error al inicializar GLFW: {e}")
        return
    
    setup_opengl()
    video_tex = create_video_texture()
    
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(" No se pudo abrir la camara")
        glfw.terminate()
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    print("Camara inicializada")
    
    
    frame_count = 0
    fps_timer = glfw.get_time()
    
    try:
        while not glfw.window_should_close(window):
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = face_mesh.process(frame_rgb)
            
            glfw.poll_events()
            
            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                break
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            render_video_background(frame_rgb, video_tex)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    render_3d_mask_extended(face_landmarks)
            
            glfw.swap_buffers(window)
            
            
            frame_count += 1
            current_time = glfw.get_time()
            if current_time - fps_timer >= 1.0:
                fps = frame_count / (current_time - fps_timer)
                glfw.set_window_title(window, f"{WINDOW_TITLE} - FPS: {fps:.1f}")
                frame_count = 0
                fps_timer = current_time
    
    except Exception as e:
        print(f" Error en el loop principal: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nCerrando aplicación...")
        cap.release()
        face_mesh.close()
        glfw.terminate()
      
if __name__ == "__main__":
    main()
