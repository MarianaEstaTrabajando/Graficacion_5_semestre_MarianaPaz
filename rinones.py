import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

#Código basado en el hueso y el ojo pero pare riñones

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
        
def draw_cilindro(radius):
    """Dibuja un cilindro"""
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(0,361):
        x1=math.cos(math.radians(i))
        y1=math.sin(math.radians(i))
        z1=0.25
        glNormal3f(x1, y1, 0)
        glVertex3f(x1 * radius, y1 * radius, z1 )
        glNormal3f(x1, y1, 0)
        glVertex3f((x1 * radius), (y1 * radius), (z1 *4))
        
    glEnd()
    
def draw_rinon():
    glPushMatrix()

    # Color del riñón
    glColor3f(0.65, 0.15, 0.2)

    # Bolitas 
    glPushMatrix()
    draw_sphere(0.9)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0.6, 0.3)
    draw_sphere(0.7)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -0.6, 0.3)
    draw_sphere(0.7)
    glPopMatrix()

    #Tubo
    glPushMatrix()
    glColor3f(0,0,1)
    glTranslatef(0.35, 0, 0)
 

    draw_cilindro(0.1)
    glPopMatrix()

    glPopMatrix()
    
    
    #Riñon 2, rotado y separado del primer riñon:
    
    glPushMatrix()
    glTranslatef(0,0,2.5)
    glRotatef(180,0,1,0)
    glRotatef(180,0,0,1)
    # Color del riñón
    glColor3f(0.65, 0.15, 0.2)

    # Bolitas 
    glPushMatrix()
    draw_sphere(0.9)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0.6, 0.3)
    draw_sphere(0.7)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -0.6, 0.3)
    draw_sphere(0.7)
    glPopMatrix()

    #Tubo
    glPushMatrix()
    glColor3f(0,0,1)
    glTranslatef(0.35, 0, 0)
 

    draw_cilindro(0.1)
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
    global rotation # Variable global para la rotación de la escena
    
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Dos Esferas Simples", None, None) #Crea ventana
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
        #El gluPerspectiv tiene los parametros: angulo de vision, proporcion de aspecto, plano cercano, plano lejano
        gluPerspective(45, 800/600, 0.1, 100.0) 
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        
        # Rotar la escena
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0) 
        
        draw_rinon()
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
