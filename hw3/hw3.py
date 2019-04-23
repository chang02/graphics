import sys
import math
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from xyz import xyz
from quaternion import quaternion

width = 1200
height = 800
r = 340
perspectiveAngle = 45.0
eye = xyz(0.0, 0.0, 100.0)
ori = xyz(0.0, 0.0, 0.0)
up = xyz(0.0, 1.0, 0.0)
rotMatrix = [
	1, 0, 0, 0,
	0, 1, 0, 0,
	0, 0, 1, 0,
	0, 0, 0, 1
]
mousePosX = -1
mousePosY = -1
leftButton = False
rq = quaternion(1, 0, 0, 0)
rq_ = quaternion(1, 0, 0, 0)

def reshape(x, y):
    global width
    global height
    global r
    global perspectiveAngle
    width = x
    height = y
    min = 0
    if width < height:
        min = width
    else:
        min = height
    r = min / 2 * 0.85
    glViewport(0, 0, x, y)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(perspectiveAngle, x / y, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def loadGlobalCoord():
    global eye
    global ori
    global up
    global rotMatrix
    glLoadIdentity()
    gluLookAt(eye.x, eye.y, eye.z, ori.x, ori.y, ori.z, up.x, up.y, up.z)
    glMultMatrixd(rotMatrix)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    loadGlobalCoord()

    glPushMatrix()

    glBegin(GL_POLYGON)
    glColor(15/255,80/255,50/255)
    glVertex(10, -10, -10)
    glVertex(10, 10, -10)
    glVertex(-10, 10, -10)
    glVertex(-10, -10, -10)
    glEnd()

    glBegin(GL_POLYGON)
    glColor(50/255,50/255,50/255)
    glVertex(10, -10, -10)
    glVertex(-10, -10, -10)
    glVertex(-10, -10, 10)
    glVertex(10, -10, 10)
    glEnd()

    glBegin(GL_POLYGON)
    glColor(100/255,100/255,100/255)
    glVertex(10, -10, -10)
    glVertex(10, 10, -10)
    glVertex(10, 10, 10)
    glVertex(10, -10, 10)
    glEnd()

    glBegin(GL_POLYGON)
    glColor(150/255,150/255,150/255)
    glVertex(10, 10, -10)
    glVertex(-10, 10, -10)
    glVertex(-10, 10, 10)
    glVertex(10, 10, 10)
    glEnd()

    glBegin(GL_POLYGON)
    glColor(200/255,200/255,200/255)
    glVertex(-10, -10, -10)
    glVertex(-10, 10, -10)
    glVertex(-10, 10, 10)
    glVertex(-10, -10, 10)
    glEnd()

    glBegin(GL_POLYGON)
    glColor(100/255,150/255,200/255)
    glVertex(-10, -10, 10)
    glVertex(-10, 10, 10)
    glVertex(10, 10, 10)
    glVertex(10, -10, 10)
    glEnd()
    
    glPopMatrix()

    glutSwapBuffers()

def getSphereCoord(x, y):
    global width
    global height
    global r
    coordx = x - width/2
    coordy = height/2 - y

    if coordx * coordx + coordy * coordy <= r * r:
        result = xyz(coordx, coordy, math.sqrt(r * r - coordx * coordx - coordy * coordy))
        return result
    else:
        tempx = math.sqrt((r * r) / (1 + (coordy * coordy) / (coordx * coordx)))
        tempy = math.sqrt((r * r) / (1 + (coordx * coordx) / (coordy * coordy)))
        if coordx >= 0 and coordy >= 0:
            return xyz(tempx, tempy, 0.0)
        elif coordx >= 0 and coordy < 0:
            return xyz(tempx, (-1)*tempy, 0.0)
        elif coordx < 0 and coordy >= 0:
            return xyz((-1) * tempx, tempy, 0.0)
        elif coordx < 0 and coordy < 0:
            return xyz((-1) * tempx, (-1) * tempy, 0.0)

def getRealCoord(coord):
    global rq
    global rq_
    p = quaternion(0, coord.x, coord.y, coord.z)
    p = quaternion.multiply(rq, p)
    p = quaternion.multiply(p, rq_)
    return xyz(p.x, p.y, p.z)

def rotate(x1, y1, x2, y2):
    global eye
    global up
    global rq
    global rq_

    xyz1 = getSphereCoord(x1, y1)
    xyz2 = getSphereCoord(x2, y2)
    xyz1 = getRealCoord(xyz1)
    xyz2 = getRealCoord(xyz2)

    axis = xyz.normalize(xyz.crossProduct(xyz1, xyz2))
    theta = xyz.getTheta(xyz1, xyz2)
    theta = (-1) * theta

    q = quaternion(math.cos(0.5 * theta), axis.x * math.sin(0.5 * theta), axis.y * math.sin(0.5 * theta), axis.z * math.sin(0.5 * theta))
    q_ = q.conjugate()

    rq = quaternion.multiply(q, rq)
    rq_ = quaternion.multiply(rq_, q_)

    eyep = quaternion(0, eye.x, eye.y, eye.z)
    upp = quaternion(0, up.x, up.y, up.z)
    
    eyep = quaternion.rotate(q, eyep)
    upp = quaternion.rotate(q, upp)

    eye.x = eyep.x
    eye.y = eyep.y
    eye.z = eyep.z
    up.x = upp.x
    up.y = upp.y
    up.z = upp.z

    loadGlobalCoord()
    glutPostRedisplay()

def glutMouse(button, state, x, y):
    global mousePosX
    global mousePosY
    global leftButton

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mousePosX = x
            mousePosY = y
            leftButton = True
        elif state == GLUT_UP:
            leftButton = False
            mousePosX = -1
            mousePosY = -1

def glutMotion(x, y):
    global mousePosX
    global mousePosY

    if leftButton:
        # if translating:
        #     translate(mousePosX, mousePosY ,x, y)
        # else:
        rotate(mousePosX, mousePosY, x, y)
        mousePosX = x
        mousePosY = y

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("HW3")

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    # glutKeyboardFunc(keyboard)
    # glutKeyboardUpFunc(keyboardUp)
    # glutSpecialFunc(specialKeyboard)
    glutMouseFunc(glutMouse)
    glutMotionFunc(glutMotion)

    glutMainLoop()