import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30): #slices son 
    """Dibuja una esfera usando primitivas OpenGL (sin GLUT)"""
    for i in range(stacks):
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
        

        
def dibujarVenas (radius, slices=30, stacks=10):
    """Dibuja venas en la esfera"""
    cont=20
    for i in range(stacks):
      
        lat1 = math.pi * (-0.5 + i / stacks)
        lat2 = math.pi * (-0.5 + (i + 1) / stacks)
        
        glLineWidth(8)
        glBegin(GL_LINE_STRIP)
        for j in range((slices + 1)//3):
           
            lng = 2 * math.pi * j / slices
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            x2 = math.cos(lat2) * math.cos(lng)
            y2 = math.sin(lat2)
            z2 = math.cos(lat2) * math.sin(lng)
            
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radius, y1 * radius, z1 * radius)
            
            #glNormal3f(x2, y2, z2)
            #glVertex3f(x2 * radius, y2 * radius, z2 * radius)
            
        for j in range((slices + 1)//3):
            j=j+(2*(slices+1)//3)
            
            lng = 2 * math.pi * j / slices
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            x2 = math.cos(lat2) * math.cos(lng)
            y2 = math.sin(lat2)
            z2 = math.cos(lat2) * math.sin(lng)
            
            glNormal3f(x1//4, y1//4, z1)
            glVertex3f(x1 * radius, y1 * radius, z1 * radius)
            
            #glNormal3f(x2, y2, z2)
            #glVertex3f(x2 * radius, y2 * radius, z2 * radius)
        glEnd()
    
    
def dibujar_cilindro(radius):
    """Dibuja un cilindro"""
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(0,360):
        x1=math.cos(math.radians(i))
        y1=math.sin(math.radians(i))
        z1=0.5
        glNormal3f(x1, y1, 0)
        glVertex3f(x1 * radius, y1 * radius, z1 )
        glNormal3f(x1, y1, 0)
        glVertex3f((x1 * radius), (y1 * radius), (z1 *2))
        
    glEnd()
    

def draw_eye():
    """Dibuja dos esferas simples"""
    glPushMatrix()
   
    # Primera esfera (roja) a la izquierda
    glColor3f(0.85, 0.67, 0.65)  # Rojo
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54, 30, 30)
    glPopMatrix()
    
     # Cilindro rojo (piel)
    glColor3f(0.85, 0.67, 0.65)  # Rojo
    glPushMatrix()
    #glTranslatef(0.7,0,0)
    #glTranslatef(0.7*math.cos(math.radians(90)),0,0.7*math.sin(math.radians(90)))
    glRotate(90,0,1,0)
    glTranslate(0,0,0.54)
    dibujar_cilindro(0.2)
    glPopMatrix()

    glColor3f(1, 1, 1)  # Blanco
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6, 30, 30)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
    dibujarVenas(0.6)
    glPopMatrix()
    
    
    
    # Segunda esfera (azul) a la derecha
    glColor3f(0.84, 0.85, 0.92)  # Azul
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55, 30, 30)
    glPopMatrix()

    glColor3f(0, 0, 0)  # Negro
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4, 30, 30)
    glPopMatrix()

    glPopMatrix()

def setup_lighting():
    """Configura iluminación básica"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    light_position = [1.0, 1.0, 1.0, 0.2]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

def main():
    global rotation
    
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Dos Esferas Simples", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        
        # Rotar la escena
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0) 
        
        draw_eye()
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()