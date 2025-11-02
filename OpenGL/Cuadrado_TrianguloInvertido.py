import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
#En realidad es un triángulo al revés y un cuadrado
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Establecer color de fondo
    glMatrixMode(GL_PROJECTION) #Seleccionar la matriz de proyección
    glLoadIdentity() #Establecer la matriz de proyección a la identidad
    gluPerspective(45, 1.0, 0.1, 50.0)  # Configuración de perspectiva
    glMatrixMode(GL_MODELVIEW) #Seleccionar la matriz de modelo-vista

#Función para dibujar en la ventana
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar buffers
    glLoadIdentity() #Establecer la matriz de modelo-vista a la identidad
    glTranslatef(0.0, 0.0, -3)  # Mover la cámara hacia atrás

    # Dibujar un triángulo
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glVertex3f(-1.0, 1.0, 0.0) #Coordenadas en x,y,z
    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex3f(1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.8 )  # Azul
    glVertex3f(0.0, -1.0, 0.0)
    glEnd()
    
    
    #Dibujar cuadrado
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 0.0)  # Amarillo
    glVertex3f(-0.5, -0.5, 0.0)
    glColor3f(0.0, 1.0, 1.0)  # Cyan
    glVertex3f(0.5, -0.5, 0.0)
    glColor3f(1.0, 0.0, 1.0)  # Magenta
    glVertex3f(0.5, 0.5, 0.0)
    glColor3f(1.0, 0.5, 0.0)  # Naranja
    glVertex3f(-0.5, 0.5, 0.0)
    glEnd()

    glutSwapBuffers()  # Intercambiar buffers
def main():
    # Inicializar GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) #Doble buffer, color RGB y buffer de profundidad
    glutInitWindowSize(800, 600) #Tamaño de la ventana
    glutCreateWindow("Triángulo con GLUT y Python".encode('utf-8'))
    
    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__": #Ejecutar la función main si este archivo es el principal
    main()