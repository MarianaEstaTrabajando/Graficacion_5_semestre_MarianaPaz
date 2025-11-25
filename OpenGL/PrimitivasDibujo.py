from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

width, height = 900, 900

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glClearColor(0.1, 0.1, 0.1, 1)

#  Dibujar figura según índice
def draw_shape(index):
    if index == 0: glutWireSphere(0.6, 20, 20)
    elif index == 1: glutSolidSphere(0.6, 20, 20)
    elif index == 2: glutWireCube(1.0)
    elif index == 3: glutSolidCube(1.0)
    elif index == 4: glutWireCone(0.6, 1.0, 20, 4)
    elif index == 5: glutSolidCone(0.6, 1.0, 20, 4)
    elif index == 6: glutWireDodecahedron()
    elif index == 7: glutSolidDodecahedron()
    elif index == 8: glutWireOctahedron()
    elif index == 9: glutSolidOctahedron()
    elif index == 10: glutWireTetrahedron()
    elif index == 11: glutSolidTetrahedron()
    elif index == 12: glutWireIcosahedron()
    elif index == 13: glutSolidIcosahedron()
    elif index == 14: glutWireTeapot(0.5)
    elif index == 15: glutSolidTeapot(0.5)

#  Dibujo principal 
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    rows, cols = 4, 4
    cell_w = width // cols
    cell_h = height // rows
    
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            glViewport(c * cell_w, (rows - 1 - r) * cell_h, cell_w, cell_h)
            
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, cell_w / cell_h, 1, 20)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)
            
            glRotatef(20, 1, 1, 0)  # solo una rotación fija para ver mejor las formas
            
            if i % 2 == 0:
                glColor3f(0.2, 0.8, 1.0)
            else:
                glColor3f(1.0, 0.6, 0.1)
            
            draw_shape(i)
    
    glutSwapBuffers()

#  Redimensionamiento 
def reshape(w, h):
    global width, height
    width, height = w, h

#  Configuración principal 
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Figuras GLUT estaticas - OpenGL Python")

    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()

if __name__ == "__main__":
    main()
