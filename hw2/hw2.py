import OpenGL
# OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import numpy as np
import math
import xyz
import quaternion

# global variables
class glob:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.center = xyz.dot(0, 0, 0)
        self.rotationAngle1 = 0.0
        self.rotationAngle2 = 0.0
        self.rotationAngle3 = 0.0
        self.seta = 0.0
        self.leftButton = False
        self.translating = False
        self.dolly = False
        self.zoom = False
        self.mousePosX = 0.0
        self.mousePosY = 0.0
        self.r = 300
        self.perspectiveAngle = 45.0
        self.eye = xyz.dot(0.0, 0.0, 350.0)
        self.ori = xyz.dot(0.0, 0.0, 0.0)
        self.up = xyz.dot(0.0, 1.0, 0.0)
        self.rotMatrix = np.array([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ])
        self.q = quaternion.quaternion(1.0, 0.0, 0.0, 0.0)
        self.q_ = quaternion.quaternion(1.0, 0.0, 0.0, 0.0)

def getSphereXYZ(x, y):
    if x * x + y * y <= glo.r * glo.r:
        return xyz.dot(x, y, math.sqrt((glo.r * glo.r) - (x * x) - (y * y)))
    else:
        tempx = math.sqrt((glo.r * glo.r) / (1 + (y * y)/(x * x)))
        tempy = math.sqrt((glo.r * glo.r) / (1 + (x * x)/(y * y)))
        if x >= 0 and y >= 0:
            return xyz.dot(tempx, tempy, 0.0)
        elif x >= 0 and y < 0:
            return xyz.dot(tempx, (-1) * tempy, 0.0)
        elif x < 0 and y >= 0:
            return xyz.dot((-1) * tempx, tempy, 0.0)
        elif x < 0 and y < 0:
            return xyz.dot((-1) * tempx, (-1) * tempy, 0.0)

def getRealXYZ(p):
    a = quaternion.quaternion(0, p.x, p.y, p.z)
    a = glo.q.mul(a).mul(glo.q_)
    result = xyz.dot(0.0, 0.0, 0.0)
    result.x = a.x
    result.y = a.y
    result.z = a.z
    return result

def rotate(x1, y1, x2, y2):
    beforeXYZ = getSphereXYZ(x1 - glo.width/2, glo.height/2 - y1)
    afterXYZ = getSphereXYZ(x2 - glo.width/2, glo.height/2 - y2)

    beforeXYZ = getRealXYZ(beforeXYZ)
    afterXYZ = getRealXYZ(afterXYZ)

    vec1 = xyz.vector(beforeXYZ.x, beforeXYZ.y, beforeXYZ.z)
    vec2 = xyz.vector(afterXYZ.x, afterXYZ.y, afterXYZ.z)
    theta = vec2.getAngle(vec1)
    if theta == 0.0:
        return

    cross =  vec1.cross(vec2)
    cross.normalize()
    
    rq = quaternion.quaternion(math.cos(0.5 * theta), cross.x * math.sin(0.5 * theta), cross.y * math.sin(0.5 * theta), cross.z * math.sin(0.5 * theta))
    rq_ = rq.conjugate()
    
    p = quaternion.quaternion(0, glo.eye.x, glo.eye.y, glo.eye.z)
    up = quaternion.quaternion(0, glo.up.x, glo.up.y, glo.up.z)

    glo.q = rq.mul(glo.q)
    glo.q_ = glo.q_.mul(rq_)

    p_ = rq.mul(p).mul(rq_)
    up_ = rq.mul(up).mul(rq_)

    glo.eye.x = p_.x
    glo.eye.y = p_.y
    glo.eye.z = p_.y
    glo.up.x = up_.x
    glo.up.y = up_.y
    glo.up.z = up_.z

def translate(x1, y1, x2, y2):
    pass

def loadGlobalCoord():
    glLoadIdentity()
    gluLookAt(glo.eye.x, glo.eye.y, glo.eye.z, glo.ori.x, glo.ori.y, glo.ori.z, glo.up.x, glo.up.y, glo.up.z)
    glMultMatrixd(glo.rotMatrix)

def reshape(x, y):
    glo.width = x
    glo.height = y
    glViewport(0, 0, x, y)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(glo.perspectiveAngle, x / y, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def timer(unused):
    glutPostRedisplay()
    glutTimerFunc(0, timer, 0)

    glo.seta = glo.seta + 0.002
    glo.rotationAngle1 = 66.0 * (math.sin(glo.seta))

    glo.rotationAngle2 = glo.rotationAngle2 + 0.15

    glo.rotationAngle3 = glo.rotationAngle3 - 0.2

# def keyboard(key, x, y):
#     if key == 't' or key == 'T':
#         translating = True
#     elif key == 'd' or key == 'D':
#         dolly = True
#     elif key == 'z' or key == 'Z':
#         zoom = True

# def keyboardUp(key, x, y):
#     if key == 't' or key == 'T':
#         translating = False
#     elif key == 'd' or key == 'D':
#         dolly = False
#     elif key == 'z' or key == 'Z':
#         zoom = False

# def special(key, x, y):
#     if key == 101: # key up
#         pass
#     elif key == 103: # key down
#         pass

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            glo.mousePosX = x
            glo.mousePosY = y
            glo.leftButton = True
        elif state == GLUT_UP:
            glo.leftButton = False
            glo.mousePosX = -1
            glo.mousePosY = -1

def motion(x, y):
    if glo.leftButton:
        if glo.translating:
            translate(glo.mousePosX, glo.mousePosY ,x, y)
        else:
            rotate(glo.mousePosX, glo.mousePosY, x, y)
        glo.mousePosX = x
        glo.mousePosY = y
        loadGlobalCoord()

def createBox(x, y, z, colorR, colorG, colorB):
    glBegin(GL_POLYGON)
    glColor3f(1,1,1)
    glVertex3f(10, -10, 0.1)
    glVertex3f(10, 10, 0.1)
    glVertex3f(-10, 10, 0.1)
    glVertex3f(-10, -10, 0.1)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3f(colorR,colorG,colorB)
    glVertex3f(10, -10, 0.1)
    glVertex3f(-10, -10, 0.1)
    glVertex3f(-10, -10, 10)
    glVertex3f(10, -10, 10)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(10, -10, 0.1)
    glVertex3f(10, 10, 0.1)
    glVertex3f(10, 10, 10)
    glVertex3f(10, -10, 10)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(10, 10, 0.1)
    glVertex3f(-10, 10, 0.1)
    glVertex3f(-10, 10, 10)
    glVertex3f(10, 10, 10)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(-10, -10, 0.1)
    glVertex3f(-10, 10, 0.1)
    glVertex3f(-10, 10, 10)
    glVertex3f(-10, -10, 10)
    glEnd()

def createCylinder(centerx, centery, centerz, radius, h, colorR1, colorG1, colorB1, colorR2, colorG2, colorB2):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(colorR1, colorG1, colorB1)
    glVertex3f(centerx, centery, centerz)
    angle = 0.0
    while angle < 2.0 * 3.141593:
        x = centerx + radius*math.sin(angle)
        y = centery + radius*math.cos(angle)
        glVertex3f(x, y, centerz)
        angle = angle + 3.141593/360.0
    glEnd()

    glBegin(GL_QUAD_STRIP)
    glColor3f(colorR2, colorG2, colorB2)
    angle = 0.0
    while angle < 2.0 * 3.141593:
        x = centerx + radius*math.sin(angle)
        y = centery + radius*math.cos(angle)
        glVertex3f(x, y, centerz)
        glVertex3f(x, y, centerz + h)
        angle = angle + 3.141593/360.0
    glEnd()
 
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(colorR1, colorG1, colorB1)
    glVertex3f(centerx, centery, centerz + h)
    angle = 2.0 * 3.141593
    while angle > 0.0:
        x = centerx + radius*math.sin(angle)
        y = centery + radius*math.cos(angle)
        glVertex3f(x, y, centerz + h)
        angle = angle - 3.141593/360
    glEnd()

def createCylinder2(centerx, centery, centerz, radius, h):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(102.0/255.0, 153.0/255.0, 204.0/255.0)
    glVertex3f(centerx, centery, centerz)
    angle = 0.0
    while angle < 2.0 * 3.141593:
        x = centerx + radius*math.sin(angle)
        z = centerz + radius*math.cos(angle)
        glVertex3f(x, centery, z)
        angle = angle + 3.141593/360
    glEnd()

    glBegin(GL_QUAD_STRIP)
    angle = 0.0
    while angle < 2.0 * 3.141593:
        x = centerx + radius*math.sin(angle)
        z = centerz + radius*math.cos(angle)
        glVertex3f(x, centery, z)
        glVertex3f(x, centery + h, z)
        angle = angle + 3.141593/360
    glEnd()
 
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(centerx, centery + h, centerz)
    angle = 2.0 * 3.141593
    while angle > 0.0:
        x = centerx + radius*math.sin(angle)
        z = centerz + radius*math.cos(angle)
        glVertex3f(x, centery + h, z)
        angle = angle - 3.141593/360
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    loadGlobalCoord()

    glTranslatef(glo.center.x, glo.center.y, glo.center.z)
    glRotatef(-90,1,0,0)
    glTranslatef(0, 0, 54)

    # 4 column -----------------------------------------
    glPushMatrix()
    glBegin(GL_POLYGON)
    glColor3f(0.4,0.2,0.8)
    glVertex3f(-130, -130, -108)
    glVertex3f(-130, 130, -108)
    glVertex3f(130, 130, -108)
    glVertex3f(130, -130, -108)
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glRotatef(36, 1, 0, 0)
    glRotatef(40, 0, 1, 0)
    createCylinder(0, 7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0)
    glPopMatrix()

    glPushMatrix()
    glRotatef(36, 1, 0, 0)
    glRotatef(-40, 0, 1, 0)
    createCylinder(0, 7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0)
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(-36, 1, 0, 0)
    glRotatef(40, 0, 1, 0)
    createCylinder(0, -7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0)
    glPopMatrix()

    glPushMatrix()
    glRotatef(-36, 1, 0, 0)
    glRotatef(-40, 0, 1, 0)
    createCylinder(0, -7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0)
    glPopMatrix()
    # -------------------------------------------------------

    glPushMatrix()
    glRotatef(glo.rotationAngle1, 0, 1, 0)

    createCylinder2(0, -5.5, 0, 7, 11)

    glBegin(GL_POLYGON)
    glColor3f(102.0/255.0, 153.0/255.0, 204.0/255.0)
    glVertex3f(-5, 5.5, -3)
    glVertex3f(5, 5.5, -3)
    glVertex3f(5, -5.5, -3)
    glVertex3f(-5, -5.5, -3)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(-5, 5.5, -85)
    glVertex3f(5, 5.5, -85)
    glVertex3f(5, -5.5, -85)
    glVertex3f(-5, -5.5, -85)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(-5, 5.5, -3)
    glVertex3f(5, 5.5, -3)
    glVertex3f(5, 5.5, -85)
    glVertex3f(-5, 5.5, -85)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(5, 5.5, -3)
    glVertex3f(-5, 5.5, -3)
    glVertex3f(-5, 5.5, -85)
    glVertex3f(5, 5.5, -85)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(5, 5.5, -3)
    glVertex3f(5, -5.5, -3)
    glVertex3f(5, -5.5, -85)
    glVertex3f(5, 5.5, -85)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(5, -5.5, -3)
    glVertex3f(5, 5.5, -3)
    glVertex3f(5, 5.5, -85)
    glVertex3f(5, -5.5, -85)
    glEnd()

    glPushMatrix()
    glTranslatef(0, 0, -90.1)
    glRotatef(glo.rotationAngle2, 0, 0, 1)
    createCylinder(0, 0, 0, 45, -7, 153.0/255.0, 204.0/255.0, 204.0/255.0, 153.0/255.0, 153.0/255.0, 204.0/255.0)
    createCylinder(0, 0, 0, 15, 5, 1, 1, 1, 143.0/255.0, 194.0/255.0, 194.0/255.0)

    glPushMatrix()
    ang = 2.0 * 3.141593 / 6.0
    x = 35.0 * math.cos(ang)
    y = 35.0 * math.sin(ang)
    glTranslatef(x, 0, 0)
    glTranslatef(0, y, 0)
    glRotatef(60 + glo.rotationAngle3, 0, 0, 1)
    createBox(0, 0, 0, 1, 0, 0)
    glPopMatrix()

    glPushMatrix()
    ang = 4.0 * 3.141593 / 6.0
    x = 35.0 * math.cos(ang)
    y = 35.0 * math.sin(ang)
    glTranslatef(x, 0, 0)
    glTranslatef(0, y, 0)
    glRotatef(120 + glo.rotationAngle3, 0, 0, 1)
    createBox(0, 0, 0, 1, 0.2, 0)
    glPopMatrix()

    glPushMatrix()
    ang = 6.0 * 3.141593 / 6.0
    x = 35.0 * math.cos(ang)
    y = 35.0 * math.sin(ang)
    glTranslatef(x, 0, 0)
    glTranslatef(0, y, 0)
    glRotatef(180 + glo.rotationAngle3, 0, 0, 1)
    createBox(0, 0, 0, 1, 1, 0)
    glPopMatrix()

    glPushMatrix()
    ang = 8.0 * 3.141593 / 6.0
    x = 35.0 * math.cos(ang)
    y = 35.0 * math.sin(ang)
    glTranslatef(x, 0, 0)
    glTranslatef(0, y, 0)
    glRotatef(240 + glo.rotationAngle3, 0, 0, 1)
    createBox(0, 0, 0, 0, 1, 0)
    glPopMatrix()

    glPushMatrix()
    ang = 10.0 * 3.141593 / 6.0
    x = 35.0 * math.cos(ang)
    y = 35.0 * math.sin(ang)
    glTranslatef(x, 0, 0)
    glTranslatef(0, y, 0)
    glRotatef(300 + glo.rotationAngle3, 0, 0, 1)
    createBox(0, 0, 0, 0, 0, 1)
    glPopMatrix()

    glPushMatrix()
    ang = 0
    x = 35.0 * math.cos(ang)
    y = 35.0 * math.sin(ang)
    glTranslatef(x, 0, 0)
    glTranslatef(0, y, 0)
    glRotatef(glo.rotationAngle3, 0, 0, 1)
    createBox(0, 0, 0, 0.4, 0, 1)
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    glutSwapBuffers()

# main
if __name__ == '__main__':
    glo = glob()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(glo.width, glo.height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("HW2")

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(30, timer, 0)
    # glutKeyboardFunc(keyboard)
    # glutKeyboardUpFunc(keyboardUp)
    # glutSpecialFunc(special)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)

    glutMainLoop()