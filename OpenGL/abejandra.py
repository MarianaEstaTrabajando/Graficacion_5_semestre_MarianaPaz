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
        
    
def dibujar_parte_circulo(radius, grados,grosor):
    """Dibuja una parte de un circulo"""
    glLineWidth(grosor)
    glBegin(GL_LINE_STRIP)
    for i in range(0,grados):
        x1=math.cos(math.radians(i))
        y1=math.sin(math.radians(i))
        z1=0.5
        glNormal3f(x1, y1, 0)
        glVertex3f(x1 * radius, y1 * radius, z1 )
        glNormal3f(x1, y1, 0)
        glVertex3f(x1 * radius, y1 * radius, z1+0.3 )
        
        
    glEnd()
    

def draw_bee():
    """Dibuja dos esferas simples"""
    glPushMatrix()
   
    #Cuerpo amarillo
    glColor3f(6, 1, 0)  # amarilla
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(1, 30, 30)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
    glPopMatrix()
    
    #Ojo negro
    glColor3f(0, 0, 0)  # negro
    glPushMatrix()
    glTranslatef(1.3, 0.4, -0.5)
    draw_sphere(0.2, 30, 30)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
    glPopMatrix()
    
    #Ojo negro
    glColor3f(0, 0, 0)  # negro
    glPushMatrix()
    glTranslatef(1.3, 0.4, 0.5)
    draw_sphere(0.2, 30, 30)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
    glPopMatrix()
    
    #Línea negra
    glColor3f(0, 0, 0)  # negro
    glPushMatrix()
    glRotate(180,1,0,1)
    glTranslatef(0, 0, 0)
    dibujar_parte_circulo(1,360,8)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
    glPopMatrix()
    
    #sonrisa
    glColor3f(0, 0, 0)  # negro
    glPushMatrix()
    glRotate(180,1,0,1)
    glTranslatef(0, 0, 0.7)
    dibujar_parte_circulo(0.5,180,8)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
    glPopMatrix()
    
    #alita
    glColor3f(1, 1, 1)  # blanco
    glPushMatrix()
    glRotate(45,1,1,1)
    glTranslatef(0.3, 0.6, -0.5)
    dibujar_parte_circulo(0.7,360,0.7)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
    glPopMatrix()
    
    #alita
    glColor3f(1, 1, 1)  # blanco
    glPushMatrix()
    glRotate(45,0,0,1)
    glRotate(165,1,1,0)
    #glRotate(45,0,1,1)
    glTranslatef(0.3, 0.6, -0.3)
    dibujar_parte_circulo(0.7,360,0.7)
    glColor3f(0.2, 0.2, 0.9)  # Blanco
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
        
        draw_bee()
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()