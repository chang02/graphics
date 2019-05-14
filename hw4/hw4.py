import sys
import math
import json
import copy
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from xyz import xyz
from quaternion import quaternion
from cube import cube

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
translating = False
dolly = False
zoom = False

lightPos0 = xyz(0, 0, 50)
lightPos1 = xyz(0, 0, -50)

rq = quaternion(1, 0, 0, 0)
rq_ = quaternion(1, 0, 0, 0)
globalTranslate = xyz(0.0, 0.0, 0.0)
splinePoints1 = []
splinePoints2 = []

def scaleRotatePosition(crossSections):
    result = []
    for crossSection in crossSections:
        controllPoints = crossSection['controllPoints']
        scale = crossSection['scale']
        rotate = crossSection['rotation']
        position = crossSection['position']
        tempResult = []
        for controllPoint in controllPoints:
            realControllPoint = xyz(controllPoint.x * scale, controllPoint.y * scale, controllPoint.z * scale)
            realControllPoint = quaternion.rotate(rotate, realControllPoint)
            realControllPoint = xyz(realControllPoint.x + position.x, realControllPoint.y + position.y, realControllPoint.z + position.z)
            tempResult.append(realControllPoint)
        result.append(tempResult)
    return result

def toBsplinePoints(realControllPoint):
    i = 0
    result = []
    p = copy.deepcopy(realControllPoint)
    p.append(p[0])
    p.append(p[1])
    p.append(p[2])
    while i + 4 <= len(p):
        t = 0
        while t <= 1.0:
            it = 1.0 - t
            b0 = it*it*it/6
            b1 = (3*t*t*t - 6*t*t +4)/6
            b2 = (-3*t*t*t +3*t*t + 3*t + 1)/6
            b3 =  t*t*t/6
            x = b0 * p[i].x + b1 * p[i+1].x + b2 * p[i+2].x + b3 * p[i+3].x
            y = b0 * p[i].y + b1 * p[i+1].y + b2 * p[i+2].y + b3 * p[i+3].y
            z = b0 * p[i].z + b1 * p[i+1].z + b2 * p[i+2].z + b3 * p[i+3].z
            result.append(xyz(x, y, z))
            t += 0.3333
        i += 1
    return result

def toCatmullRomPoints(realControllPoint):
    i = 0
    result = []
    p = copy.deepcopy(realControllPoint)
    p.append(p[0])
    p.append(p[1])
    p.append(p[2])
    while i + 4 <= len(p):
        t = 0
        while t <= 1.0:
            t2 = t * t
            t3 = t2 * t
            x = ((2 * p[i+1].x) + ((-p[i].x + p[i+2].x) * t) + ((2 * p[i].x - 5 * p[i+1].x + 4 * p[i+2].x - p[i+3].x) * t2) + ((-p[i].x + 3 * p[i+1].x - 3 * p[i+2].x + p[i+3].x) * t3)) * 0.5
            y = ((2 * p[i+1].y) + ((-p[i].y + p[i+2].y) * t) + ((2 * p[i].y - 5 * p[i+1].y + 4 * p[i+2].y - p[i+3].y) * t2) + ((-p[i].y + 3 * p[i+1].y - 3 * p[i+2].y + p[i+3].y) * t3)) * 0.5
            z = ((2 * p[i+1].z) + ((-p[i].z + p[i+2].z) * t) + ((2 * p[i].z - 5 * p[i+1].z + 4 * p[i+2].z - p[i+3].z) * t2) + ((-p[i].z + 3 * p[i+1].z - 3 * p[i+2].z + p[i+3].z) * t3)) * 0.5
            result.append(xyz(x, y, z))
            t += 0.3333
        i += 1
    return result

def toCatmullRomSurface(crossSections):
    result = []
    sections = copy.deepcopy(crossSections)
    i = 0
    while i + 4 <= len(sections):
        t = 0
        controllPoints = []
        scale = None
        rotation = None
        position = None
        while t <= 1.0:
            t2 = t * t
            t3 = t2 * t
            for p0, p1, p2, p3 in zip(sections[i]["controllPoints"], sections[i+1]["controllPoints"], sections[i+2]["controllPoints"], sections[i+3]["controllPoints"]):
                x = ((2 * p1.x) + ((-p0.x + p2.x) * t) + ((2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2) + ((-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * t3)) * 0.5
                y = ((2 * p1.y) + ((-p0.y + p2.y) * t) + ((2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2) + ((-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * t3)) * 0.5
                z = ((2 * p1.z) + ((-p0.z + p2.z) * t) + ((2 * p0.z - 5 * p1.z + 4 * p2.z - p3.z) * t2) + ((-p0.z + 3 * p1.z - 3 * p2.z + p3.z) * t3)) * 0.5
                controllPoints.append(xyz(x, y, z))
            scale = ((2 * sections[i+1]["scale"]) + ((-sections[i]["scale"] + sections[i+2]["scale"]) * t) + ((2 * sections[i]["scale"] - 5 * sections[i+1]["scale"] + 4 * sections[i+2]["scale"] - sections[i+3]["scale"]) * t2) + ((-sections[i]["scale"] + 3 * sections[i+1]["scale"] - 3 * sections[i+2]["scale"] + sections[i+3]["scale"]) * t3)) * 0.5
            position = ((sections[i+1]["position"]  * 2) + ((sections[i]["position"] * (-1) + sections[i+2]["position"]) * t) + ((sections[i]["position"] * 2 - sections[i+1]["position"] * 5 + sections[i+2]["position"] * 4 - sections[i+3]["position"]) * t2) + ((sections[i]["position"] * (-1) + sections[i+1]["position"] * 3 - sections[i+2]["position"] * 3 + sections[i+3]["position"]) * t3)) * 0.5
            rotation = ((sections[i+1]["rotation"]  * 2) + ((sections[i]["rotation"] * (-1) + sections[i+2]["rotation"]) * t) + ((sections[i]["rotation"] * 2 - sections[i+1]["rotation"] * 5 + sections[i+2]["rotation"] * 4 - sections[i+3]["rotation"]) * t2) + ((sections[i]["rotation"] * (-1) + sections[i+1]["rotation"] * 3 - sections[i+2]["rotation"] * 3 + sections[i+3]["rotation"]) * t3)) * 0.5
            result.append({
                "controllPoints": controllPoints,
                "scale": scale,
                "rotation": rotation,
                "position": position,
            })
            t += 0.33
        i += 1
    return result

def processInputFile():
    global splinePoints1
    global splinePoints2

    f = open('myinput.txt', 'r')
    lines = f.readlines()

    # parse
    for idx, line in enumerate(lines):
        lines[idx] = line.split('#')[0]
    
    i = 0
    while i < len(lines):
        if lines[i].isspace() or lines[i] == '':
            lines.remove(lines[i])
        else:
            i += 1

    for idx, line in enumerate(lines):
        if line.isspace() or line == '':
            lines.remove(line)
    
    curveType = lines[0].split()[0]
    crossSectionNum = int(lines[1].split()[0])
    controllPointNum = int(lines[2].split()[0])
    crossSections = []
    for i in range(0, crossSectionNum):
        controllPoints = []
        for j in range(0, controllPointNum):
            x = float(lines[3 + i * (controllPointNum + 3) + j].split()[0])
            z = float(lines[3 + i * (controllPointNum + 3) + j].split()[1])
            controllPoint = xyz(x, 0, z)
            controllPoints.append(controllPoint)
        scaleFactor = float(lines[3 + i * (controllPointNum + 3) + controllPointNum].split()[0])
        theta = float(lines[3 + i * (controllPointNum + 3) + controllPointNum + 1].split()[0])
        x = float(lines[3 + i * (controllPointNum + 3) + controllPointNum + 1].split()[1])
        y = float(lines[3 + i * (controllPointNum + 3) + controllPointNum + 1].split()[2])
        z = float(lines[3 + i * (controllPointNum + 3) + controllPointNum + 1].split()[3])
        rotation = quaternion(math.cos(0.5 * theta), x * math.sin(0.5 * theta), y * math.sin(0.5 * theta), z * math.sin(0.5 * theta))
        x = float(lines[3 + i * (controllPointNum + 3) + controllPointNum + 2].split()[0])
        y = float(lines[3 + i * (controllPointNum + 3) + controllPointNum + 2].split()[1])
        z = float(lines[3 + i * (controllPointNum + 3) + controllPointNum + 2].split()[2])
        position = xyz(x, y, z)
        crossSections.append({
            "controllPoints": controllPoints,
            "scale": scaleFactor,
            "rotation": rotation,
            "position": position,
        })

    crossSections.insert(0, crossSections[0])
    crossSections.append(crossSections[len(crossSections) - 1])

    realControllPoints = scaleRotatePosition(crossSections)
    if curveType == 'BSPLINE':
        for realControllPoint in realControllPoints:
            splinePoints1.append(toBsplinePoints(realControllPoint))
    elif curveType == 'CATMULL_ROM':
        for realControllPoint in realControllPoints:
            splinePoints1.append(toCatmullRomPoints(realControllPoint))    

    catmullRomCrossSections = toCatmullRomSurface(crossSections)
    realControllPoints = scaleRotatePosition(catmullRomCrossSections)
    if curveType == 'BSPLINE':
        for realControllPoint in realControllPoints:
            splinePoints2.append(toBsplinePoints(realControllPoint))
    elif curveType == 'CATMULL_ROM':
        for realControllPoint in realControllPoints:
            splinePoints2.append(toCatmullRomPoints(realControllPoint))


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

def drawCrossSections(sections):
    for idx, splinePoint in enumerate(sections):
        glBegin(GL_LINE_STRIP)
        glColor3f(1, 0, 0)
        for point in splinePoint:
            glVertex3f(point.x, point.y, point.z)
        glEnd()

def drawCatmullRomSections(sections):
    i = 0
    while i + 1 < len(sections):
        j = 0
        while j + 1 < len(sections[i]):
            # glColor3f(204/255, 1, 204/255)
            # glBegin(GL_LINE_STRIP)
            # glVertex3f(sections[i][j].x, sections[i][j].y, sections[i][j].z)
            # glVertex3f(sections[i+1][j].x, sections[i+1][j].y, sections[i+1][j].z)
            # glVertex3f(sections[i+1][j+1].x, sections[i+1][j+1].y, sections[i+1][j+1].z)
            # glVertex3f(sections[i][j+1].x, sections[i][j+1].y, sections[i][j+1].z)
            # glEnd()

            glBegin(GL_POLYGON)
            # emerald
            # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0215, 0.1745, 0.0215, 1.0])
            # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.07568, 0.61424, 0.07568])
            # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.633, 0.727811, 0.633])
            # glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.6 * 128.0)
            # glColor3f(0.07568, 0.61424, 0.07568)
            glColor3f(204/255, 1, 204/255)
            glVertex3f(sections[i][j].x, sections[i][j].y, sections[i][j].z)
            glVertex3f(sections[i+1][j].x, sections[i+1][j].y, sections[i+1][j].z)
            glVertex3f(sections[i+1][j+1].x, sections[i+1][j+1].y, sections[i+1][j+1].z)
            glVertex3f(sections[i][j+1].x, sections[i][j+1].y, sections[i][j+1].z)
            glEnd()
            j += 1
        i += 1

def drawMaterialSurfaces(surfaces):    
    for surface in surfaces:
        glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, surface["ambient"])
        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, surface["diffuse"])
        glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, surface["specular"])
        glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, surface["shininess"] * 128.0)
        glColor3f(surface["diffuse"][0], surface["diffuse"][1], surface["diffuse"][2])
        glBegin(GL_POLYGON)
        glVertex3f(surface["points"][0].x, surface["points"][0].y, surface["points"][0].z)
        glVertex3f(surface["points"][1].x, surface["points"][1].y, surface["points"][1].z)
        glVertex3f(surface["points"][2].x, surface["points"][2].y, surface["points"][2].z)
        glVertex3f(surface["points"][3].x, surface["points"][3].y, surface["points"][3].z)
        glEnd()

def drawTranslucentSurfaces(surfaces):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for surface in surfaces:
        glBegin(GL_POLYGON)
        glColor4f(surface["color"][0], surface["color"][1], surface["color"][2], 0.5)
        glVertex3f(surface["points"][0].x, surface["points"][0].y, surface["points"][0].z)
        glVertex3f(surface["points"][1].x, surface["points"][1].y, surface["points"][1].z)
        glVertex3f(surface["points"][2].x, surface["points"][2].y, surface["points"][2].z)
        glVertex3f(surface["points"][3].x, surface["points"][3].y, surface["points"][3].z)
        glEnd()


def display():
    global globalTranslate
    global splinePoints1
    global splinePoints2
    global eye

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    loadGlobalCoord()

    glPushMatrix()
    
    glTranslatef(globalTranslate.x, globalTranslate.y, globalTranslate.z)

    drawCrossSections(splinePoints1)
    drawCatmullRomSections(splinePoints2)

    c1 = cube(xyz(-25, 10, 10), xyz(-25, 10, -10), xyz(-5, 10, -10), xyz(-5, 10, 10), xyz(-25, -10, 10), xyz(-25, -10, -10), xyz(-5, -10, -10), xyz(-5, -10, 10))
    s1 = c1.getSortedSurfaces(eye)
    drawMaterialSurfaces(s1)

    c2 = cube(xyz(5, 10, 10), xyz(5, 10, -10), xyz(25, 10, -10), xyz(25, 10, 10), xyz(5, -10, 10), xyz(5, -10, -10), xyz(25, -10, -10), xyz(25, -10, 10))
    s2 = c2.getSortedSurfaces(eye)
    drawTranslucentSurfaces(s2)
    

    glPopMatrix()

    glutSwapBuffers()

def lightOn():
    global lightPos0
    global lightPos1
    # glEnable(GL_COLOR_MATERIAL)
    # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)    
    glEnable(GL_LIGHT1)

    ambient0 = [0.0, 0.0, 0.0, 1]
    diffuse0 = [1, 1, 1, 1]
    specular0 = [1, 1, 1, 1]

    ambient1 = [0, 0, 0, 1]
    diffuse1 = [1, 1, 1, 1]
    specular1 = [1, 1, 1, 1]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular0)
    glLightfv(GL_LIGHT0, GL_POSITION, [lightPos0.x, lightPos0.y, lightPos0.z, 1])
    glLightf( GL_LIGHT0, GL_SPOT_CUTOFF , 50.0 )
    glLightf( GL_LIGHT0, GL_SPOT_EXPONENT, 50.0 )
    glLightfv( GL_LIGHT0, GL_SPOT_DIRECTION, [-lightPos0.x, -lightPos0.y, -lightPos0.z])
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, [lightPos1.x, lightPos1.y, lightPos1.z, 1])
    glLightf( GL_LIGHT1, GL_SPOT_CUTOFF , 50.0 )
    glLightf( GL_LIGHT1, GL_SPOT_EXPONENT, 50.0 )
    glLightfv( GL_LIGHT1, GL_SPOT_DIRECTION, [-lightPos1.x, -lightPos1.y, -lightPos1.z])
    
    glEnable(GL_NORMALIZE)
    glEnable(GL_DEPTH_TEST)

def keyboard(key, x, y):
    global translating
    global dolly
    global zoom
    global width
    global height
    if key == b't' or key == b'T':
        translating = True
    elif key == b'd' or key == b'D':
        dolly = True
    elif key == b'z' or key == b'Z':
        zoom = True

def keyboardUp(key, x, y):
    global translating
    global dolly
    global zoom
    if key == b't' or key == b'T':
        translating = False
    elif key == b'd' or key == b'D':
        dolly = False
    elif key == b'z' or key == b'Z':
        zoom = False

def specialKeyboard(key, x, y):
    global dolly
    global zoom
    global perspectiveAngle
    global eye
    global width
    global height
    if key == 101:
        if dolly:
            direc = eye.normalize()
            eye.x -= direc.x
            eye.y -= direc.y
            eye.z -= direc.z
        elif zoom:
            perspectiveAngle -= 0.5
            if perspectiveAngle < 10:
                perspectiveAngle = 10
            reshape(width, height)

    elif key == 103:
        if dolly:
            direc = eye.normalize()
            eye.x += direc.x
            eye.y += direc.y
            eye.z += direc.z
        elif zoom:
            perspectiveAngle += 0.5
            if perspectiveAngle > 80:
                perspectiveAngle = 80
            reshape(width, height)
    glutPostRedisplay()

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
        try:
            tempx = math.sqrt((r * r) / (1 + (coordy * coordy) / (coordx * coordx)))
        except:
            tempx = 0
        try:
            tempy = math.sqrt((r * r) / (1 + (coordx * coordx) / (coordy * coordy)))
        except:
            tempy = 0
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
    p = rq * p * rq_
    return xyz(p.x, p.y, p.z)

def translate(x1, y1, x2, y2):
    global globalTranslate
    xyz1 = 	xyz(x1 - width/2, height/2 - y1, 0)
    xyz2 = 	xyz(x2 - width/2, height/2 - y2, 0)
    xyz1 = getRealCoord(xyz1)
    xyz2 = getRealCoord(xyz2)

    globalTranslate.x += 0.1 * (xyz2.x - xyz1.x)
    globalTranslate.y += 0.1 * (xyz2.y - xyz1.y)
    globalTranslate.z += 0.1 * (xyz2.z - xyz1.z)

    glutPostRedisplay()


def rotate(x1, y1, x2, y2):
    global eye
    global up
    global rq
    global rq_
    global lightPos0
    global lightPos1

    xyz1 = getSphereCoord(x1, y1)
    xyz2 = getSphereCoord(x2, y2)
    xyz1 = getRealCoord(xyz1)
    xyz2 = getRealCoord(xyz2)

    axis = xyz.normalize(xyz.crossProduct(xyz1, xyz2))
    theta = xyz.getTheta(xyz1, xyz2)
    theta = (-1) * theta

    q = quaternion(math.cos(0.5 * theta), axis.x * math.sin(0.5 * theta), axis.y * math.sin(0.5 * theta), axis.z * math.sin(0.5 * theta))
    q_ = q.conjugate()

    rq = q * rq
    rq_ = rq_ * q_
    
    eye = quaternion.rotate(q, eye)
    up = quaternion.rotate(q, up)
    nowLightPos0 = quaternion.rotate(rq, lightPos0)
    nowLightPos1 = quaternion.rotate(rq, lightPos1)

    glLightfv(GL_LIGHT0, GL_POSITION, [nowLightPos0.x, nowLightPos0.y, nowLightPos0.z, 1])
    glLightfv( GL_LIGHT0, GL_SPOT_DIRECTION, [-nowLightPos0.x, -nowLightPos0.y, -nowLightPos0.z])

    glLightfv(GL_LIGHT1, GL_POSITION, [nowLightPos1.x, nowLightPos1.y, nowLightPos1.z, 1])
    glLightfv( GL_LIGHT1, GL_SPOT_DIRECTION, [-nowLightPos1.x, -nowLightPos1.y, -nowLightPos1.z])

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
        if translating:
            translate(mousePosX, mousePosY ,x, y)
            mousePosX = x
            mousePosY = y
        else:
            rotate(mousePosX, mousePosY, x, y)
            mousePosX = x
            mousePosY = y

if __name__ == "__main__":

    processInputFile()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("HW4")

    lightOn()

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboardUp)
    glutSpecialFunc(specialKeyboard)
    glutMouseFunc(glutMouse)
    glutMotionFunc(glutMotion)

    glutMainLoop()