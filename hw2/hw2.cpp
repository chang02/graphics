#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/freeglut.h>
#include <iostream>
#include <cmath>
#include <algorithm>
#include "quaternion.h"
struct xyz {
	GLfloat x;
	GLfloat y;
	GLfloat z;
};
bool leftButton = false;
bool translating = false;
bool dolly = false;
bool zoom = false;
xyz realCenter = {0.0, 0.0, 0.0};
GLfloat mousePosX, mousePosY;
qua::Quaternion globalRQ(1.0, 0.0, 0.0, 0.0);
qua::Quaternion globalRQ_(1.0, 0.0, 0.0, 0.0);
int width = 1200;
int height = 800;
int r = 300;
GLfloat perspectiveAngle = 45.0;
float eye[3] = { 0.0f, 0.0f, 350.0f };
float ori[3] = { 0.0f, 0.0f, 0.0f };
float rot[3] = { 0.0f, 1.0f, 0.0f };
GLdouble rotMatrix[16] =
{
	1, 0, 0, 0,
	0, 1, 0, 0,
	0, 0, 1, 0,
	0, 0, 0, 1
};

void glutMouse(int button, int state, int x, int y);
void glutMotion(int x, int y);
void rotate(GLfloat x1, GLfloat y1, GLfloat x2, GLfloat y2);
void translate(GLfloat x1, GLfloat y1, GLfloat x2, GLfloat y2);
void Timer(int unused);
void keyboard(unsigned char key, int x, int y);
void keyboardUp(unsigned char key, int x, int y);
void specialKeyboard(int key, int x, int y);
void resize(int x, int y);
void loadGlobalCoord();
void display();
void createBox(GLfloat x, GLfloat y, GLfloat z, GLfloat colorR, GLfloat colorG, GLfloat colorB);
void createCylinder(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h, 
GLfloat colorR1, GLfloat colorG1, GLfloat colorB1,
GLfloat colorR2, GLfloat colorG2, GLfloat colorB2);
void createCylinder2(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h);
GLfloat getZ(GLfloat x, GLfloat y);
xyz getSphereXYZ(GLfloat x, GLfloat y);
xyz getRealXYZ(xyz p);

int main(int argc, char **argv) {
    glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
	glutInitWindowSize(width, height);
	glutInitWindowPosition( 0, 0 );
	glutCreateWindow("HW2");

    glutReshapeFunc(resize);
	glutDisplayFunc(display);
	glutTimerFunc(30, Timer, 0);
	glutKeyboardFunc(keyboard);
	glutKeyboardUpFunc(keyboardUp);
	glutSpecialFunc(specialKeyboard);
	glutMouseFunc(glutMouse);
	glutMotionFunc(glutMotion);

	glutMainLoop();

    return 0;
}

xyz getSphereXYZ(GLfloat x, GLfloat y) {
	if ( x * x + y * y <= r * r) {
		return xyz {x, y, sqrt((r * r) - (x * x) - (y * y))};
	} else {
		GLfloat tempx = sqrt((r * r) / (1 + (y * y)/(x * x)));
		GLfloat tempy = sqrt((r * r) / (1 + (x * x)/(y * y)));
		if (x >= 0 && y >= 0) {
			return xyz {tempx, tempy, 0.0f};
		} else if (x >= 0 && y < 0) {
			return xyz {tempx, (-1)*tempy, 0.0f};
		} else if (x < 0 && y >= 0) {
			return xyz {(-1) * tempx, tempy, 0.0f};
		} else if (x < 0 && y < 0) {
			return xyz {(-1) * tempx, (-1) * tempy, 0.0f};
		}
	}
}

xyz getRealXYZ(xyz p) {
	qua::Quaternion a(0, p.x, p.y, p.z);
	a = globalRQ * a * globalRQ_;
	xyz result;
	result.x = a.x();
	result.y = a.y();
	result.z = a.z();
	return result;
}

void rotate(GLfloat x1, GLfloat y1, GLfloat x2, GLfloat y2) {
	auto xyz1 = getSphereXYZ(x1 - width/2, height/2 - y1);
	auto xyz2 = getSphereXYZ(x2 - width/2, height/2 - y2);

	xyz1 = getRealXYZ(xyz1);
	xyz2 = getRealXYZ(xyz2);

	GLfloat crossX = xyz1.y * xyz2.z - xyz1.z * xyz2.y;
	GLfloat crossY = xyz1.z * xyz2.x - xyz1.x * xyz2.z;
	GLfloat crossZ = xyz1.x * xyz2.y - xyz1.y * xyz2.x;
	GLfloat cross = sqrt(crossX * crossX + crossY * crossY + crossZ * crossZ);
	GLfloat dot = xyz1.x * xyz2.x + xyz1.y * xyz2.y + xyz1.z * xyz2.z;
	GLfloat theta = atan2(cross, dot);
	theta = theta * (-1.0);

	if (theta == 0.0) {
		return;
	}
	crossX = crossX / cross;
	crossY = crossY / cross;
	crossZ = crossZ / cross;

	qua::Quaternion rq(cos(0.5 * theta), crossX * sin(theta / 2), crossY * sin(theta / 2), crossZ * sin(theta / 2));
	qua::Quaternion rq_ = rq.conjugate();

	qua::Quaternion p(0, eye[0], eye[1], eye[2]);
	qua::Quaternion up(0, rot[0], rot[1], rot[2]);

	globalRQ = rq * globalRQ;
	globalRQ_ = globalRQ_ * rq_;

	qua::Quaternion p_ = rq * p * rq_;
	qua::Quaternion up_ = rq * up * rq_;

	eye[0] = p_.x();
	eye[1] = p_.y();
	eye[2] = p_.z();
	rot[0] = up_.x();
	rot[1] = up_.y();
	rot[2] = up_.z();
}

void translate(GLfloat x1, GLfloat y1, GLfloat x2, GLfloat y2) {
	xyz xyz1 = 	{x1 - width/2, height/2 - y1, 0};
	xyz xyz2 = 	{x2 - width/2, height/2 - y2, 0};

	xyz1 = getRealXYZ(xyz1);
	xyz2 = getRealXYZ(xyz2);
	
	realCenter.x += xyz2.x - xyz1.x;
	realCenter.y += xyz2.y - xyz1.y;
	realCenter.z += xyz2.z - xyz1.z;
}

void glutMouse(int button, int state, int x, int y) {
	switch( button )
	{
		case GLUT_LEFT_BUTTON:
			if (state == GLUT_DOWN) {
				mousePosX = x;
				mousePosY = y;
				leftButton = true;
			} else if (state == GLUT_UP) {
				leftButton = false;
				mousePosX = -1;
				mousePosY = -1;
			}
			break;
		default: break;
	}
	return;
}

void glutMotion(int x, int y) {
	if (leftButton) {
		if (translating) {
			translate(mousePosX, mousePosY ,x, y);
		} else {
			rotate(mousePosX, mousePosY, x, y);
		}
		mousePosX = x;
		mousePosY = y;
		loadGlobalCoord();
	}
	return;
}

float rotationAngle1 = 0.0;
float rotationAngle2 = 0.0;
float rotationAngle3 = 0.0;
float seta = 0.0;
void Timer(int unused) {
	/* call the display callback and forces the current window to be displayed */
	glutPostRedisplay();
	glutTimerFunc(0, Timer, 0);

	seta += 0.000003;
	rotationAngle1 = 66.0 * (sin(seta));

	rotationAngle2 = rotationAngle2 + 0.0004;

	rotationAngle3 = rotationAngle3 - 0.0008;
}

void keyboard(unsigned char key, int x, int y) {
	switch (key) {
	case 27:
		exit(0);
		break;
	case 't':
	case 'T':
		translating = true;
		break;
	case 'd':
	case 'D':
		dolly = true;
		break;
	case 'z':
	case 'Z':
		zoom = true;
		break;
	default: break;
	}
}

void keyboardUp(unsigned char key, int x, int y) {
	switch (key) {
		case 't':
		case 'T':
			translating = false;
			break;
		case 'd':
		case 'D':
			dolly = false;
			break;
		case 'z':
		case 'Z':
			zoom = false;
			break;
		default: break;
	}
}

void specialKeyboard(int key, int x, int y) {
	switch(key) {
		case 101:	// key up
			if (dolly) {
				xyz direc = {0, 0, -2};
				direc = getRealXYZ(direc);
				eye[0] += direc.x;
				eye[1] += direc.y;
				eye[2] += direc.z;
				loadGlobalCoord();
			} else if (zoom) {
				perspectiveAngle -= 0.5;
				if (perspectiveAngle < 10)
					perspectiveAngle = 10;
				resize(width, height);
			}
			break;
		case 103:	// key down
			if (dolly) {
				xyz direc = {0, 0, 2};
				direc = getRealXYZ(direc);
				eye[0] += direc.x;
				eye[1] += direc.y;
				eye[2] += direc.z;
				loadGlobalCoord();
			} else if (zoom) {
				perspectiveAngle += 0.5;
				if (perspectiveAngle > 80)
					perspectiveAngle = 80;
				resize(width, height);
			}
			break;
	}
}

void resize(int x, int y) {
    width = x;
	height = y;
	glViewport(0, 0, x, y);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(perspectiveAngle, (GLfloat)x / (GLfloat)y, .1f, 1000.0f);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
}

void loadGlobalCoord() {
    glLoadIdentity();
	gluLookAt(eye[0], eye[1], eye[2], ori[0], ori[1], ori[2], rot[0], rot[1], rot[2]);
	glMultMatrixd(rotMatrix);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glEnable(GL_DEPTH_TEST);
	loadGlobalCoord();

	glTranslatef(realCenter.x, realCenter.y, realCenter.z);
	glRotatef(-90,1,0,0);
	glTranslatef(0, 0, 54);

	// 4 column -----------------------------------------
	glPushMatrix();
	{
		glBegin(GL_POLYGON);
		glColor3f(0.4,0.2,0.8);
		glVertex3f(-130, -130, -108);
		glVertex3f(-130, 130, -108);
		glVertex3f(130, 130, -108);
		glVertex3f(130, -130, -108);
		glEnd();
	}
	glPopMatrix();

	glPushMatrix();
    {
        glRotatef(36, 1, 0, 0);
        glRotatef(40, 0, 1, 0);
        createCylinder(0, 7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0);
    }
	glPopMatrix();

    glPushMatrix();
    {
        glRotatef(36, 1, 0, 0);
        glRotatef(-40, 0, 1, 0);
        createCylinder(0, 7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0);
    }
    glPopMatrix();
    
    glPushMatrix();
    {
        glRotatef(-36, 1, 0, 0);
        glRotatef(40, 0, 1, 0);
        createCylinder(0, -7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0);
    }
    glPopMatrix();

    glPushMatrix();
    {
        glRotatef(-36, 1, 0, 0);
        glRotatef(-40, 0, 1, 0);
        createCylinder(0, -7, 0, 2, -180, 1, 1, 1, 1, 204.0/255.0, 0);
    }
    glPopMatrix();
	// -------------------------------------------------------

	glPushMatrix();
	{
		glRotatef(rotationAngle1, 0, 1, 0);

		createCylinder2(0, -5.5, 0, 7, 11);

		glBegin(GL_POLYGON);
		glColor3f(102.0/255.0, 153.0/255.0, 204.0/255.0);
		glVertex3f(-5, 5.5, -3);
		glVertex3f(5, 5.5, -3);
		glVertex3f(5, -5.5, -3);
		glVertex3f(-5, -5.5, -3);
		glEnd();

		glBegin(GL_POLYGON);
		glVertex3f(-5, 5.5, -85);
		glVertex3f(5, 5.5, -85);
		glVertex3f(5, -5.5, -85);
		glVertex3f(-5, -5.5, -85);
		glEnd();

		glBegin(GL_POLYGON);
		glVertex3f(-5, 5.5, -3);
		glVertex3f(5, 5.5, -3);
		glVertex3f(5, 5.5, -85);
		glVertex3f(-5, 5.5, -85);
		glEnd();

		glBegin(GL_POLYGON);
		glVertex3f(5, 5.5, -3);
		glVertex3f(-5, 5.5, -3);
		glVertex3f(-5, 5.5, -85);
		glVertex3f(5, 5.5, -85);
		glEnd();

		glBegin(GL_POLYGON);
		glVertex3f(5, 5.5, -3);
		glVertex3f(5, -5.5, -3);
		glVertex3f(5, -5.5, -85);
		glVertex3f(5, 5.5, -85);
		glEnd();

		glBegin(GL_POLYGON);
		glVertex3f(5, -5.5, -3);
		glVertex3f(5, 5.5, -3);
		glVertex3f(5, 5.5, -85);
		glVertex3f(5, -5.5, -85);
		glEnd();

		glPushMatrix();
		{
			glTranslatef(0, 0, -90.1);
			glRotatef(rotationAngle2, 0, 0, 1);
			createCylinder(0, 0, 0, 45, -7, 153.0/255.0, 204.0/255.0, 204.0/255.0, 153.0/255.0, 153.0/255.0, 204.0/255.0);
			createCylinder(0, 0, 0, 15, 5, 1, 1, 1, 143.0/255.0, 194.0/255.0, 194.0/255.0);

			glPushMatrix();
			{
				GLfloat ang = 2.0 * 3.141593 / 6.0;
				GLfloat x = 35.0 * cos(ang);
				GLfloat y = 35.0 * sin(ang);
				glTranslatef(x, 0, 0);
				glTranslatef(0, y, 0);
				glRotatef(60 + rotationAngle3, 0, 0, 1);
				createBox(0, 0, 0, 1, 0, 0);
			}
			glPopMatrix();

			glPushMatrix();
			{
				GLfloat ang = 4.0 * 3.141593 / 6.0;
				GLfloat x = 35.0 * cos(ang);
				GLfloat y = 35.0 * sin(ang);
				glTranslatef(x, 0, 0);
				glTranslatef(0, y, 0);
				glRotatef(120 + rotationAngle3, 0, 0, 1);
				createBox(0, 0, 0, 1, 0.2, 0);
			}
			glPopMatrix();

			glPushMatrix();
			{
				GLfloat ang = 6.0 * 3.141593 / 6.0;
				GLfloat x = 35.0 * cos(ang);
				GLfloat y = 35.0 * sin(ang);
				glTranslatef(x, 0, 0);
				glTranslatef(0, y, 0);
				glRotatef(180 + rotationAngle3, 0, 0, 1);
				createBox(0, 0, 0, 1, 1, 0);
			}
			glPopMatrix();

			glPushMatrix();
			{
				GLfloat ang = 8.0 * 3.141593 / 6.0;
				GLfloat x = 35.0 * cos(ang);
				GLfloat y = 35.0 * sin(ang);
				glTranslatef(x, 0, 0);
				glTranslatef(0, y, 0);
				glRotatef(240 + rotationAngle3, 0, 0, 1);
				createBox(0, 0, 0, 0, 1, 0);
			}
			glPopMatrix();

			glPushMatrix();
			{
				GLfloat ang = 10.0 * 3.141593 / 6.0;
				GLfloat x = 35.0 * cos(ang);
				GLfloat y = 35.0 * sin(ang);
				glTranslatef(x, 0, 0);
				glTranslatef(0, y, 0);
				glRotatef(300 + rotationAngle3, 0, 0, 1);
				createBox(0, 0, 0, 0, 0, 1);
			}
			glPopMatrix();

			glPushMatrix();
			{
				GLfloat ang = 0;
				GLfloat x = 35.0 * cos(ang);
				GLfloat y = 35.0 * sin(ang);
				glTranslatef(x, 0, 0);
				glTranslatef(0, y, 0);
				glRotatef(rotationAngle3, 0, 0, 1);
				createBox(0, 0, 0, 0.4, 0, 1);
			}
			glPopMatrix();
		}
		glPopMatrix();
	}
	glPopMatrix();

	glutSwapBuffers();
}

void createBox(GLfloat x, GLfloat y, GLfloat z, GLfloat colorR, GLfloat colorG, GLfloat colorB) {
	glBegin(GL_POLYGON);
	glColor3f(1,1,1);
	glVertex3f(10, -10, 0.1);
	glVertex3f(10, 10, 0.1);
	glVertex3f(-10, 10, 0.1);
	glVertex3f(-10, -10, 0.1);
	glEnd();

	glBegin(GL_POLYGON);
	glColor3f(colorR,colorG,colorB);
	glVertex3f(10, -10, 0.1);
	glVertex3f(-10, -10, 0.1);
	glVertex3f(-10, -10, 10);
	glVertex3f(10, -10, 10);
	glEnd();

	glBegin(GL_POLYGON);
	glVertex3f(10, -10, 0.1);
	glVertex3f(10, 10, 0.1);
	glVertex3f(10, 10, 10);
	glVertex3f(10, -10, 10);
	glEnd();

	glBegin(GL_POLYGON);
	glVertex3f(10, 10, 0.1);
	glVertex3f(-10, 10, 0.1);
	glVertex3f(-10, 10, 10);
	glVertex3f(10, 10, 10);
	glEnd();

	glBegin(GL_POLYGON);
	glVertex3f(-10, -10, 0.1);
	glVertex3f(-10, 10, 0.1);
	glVertex3f(-10, 10, 10);
	glVertex3f(-10, -10, 10);
	glEnd();
}

void createCylinder(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h, 
GLfloat colorR1, GLfloat colorG1, GLfloat colorB1,
GLfloat colorR2, GLfloat colorG2, GLfloat colorB2)
{
    GLfloat x, y, angle;
 
    glBegin(GL_TRIANGLE_FAN);           //원기둥의 윗면
    glColor3f(colorR1, colorG1, colorB1);
    glVertex3f(centerx, centery, centerz);
    for(angle = 0.0f; angle < (2.0f*3.141593); angle += (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        y = centery + radius*cos(angle);
        glVertex3f(x, y, centerz);
    }
    glEnd();

    glBegin(GL_QUAD_STRIP);            //원기둥의 옆면
	glColor3f(colorR2, colorG2, colorB2);
    for(angle = 0.0f; angle < (2.0f*3.141593); angle += (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        y = centery + radius*cos(angle);
        glVertex3f(x, y, centerz);
        glVertex3f(x, y, centerz + h);
    }
    glEnd();
 
    glBegin(GL_TRIANGLE_FAN);           //원기둥의 밑면
	glColor3f(colorR1, colorG1, colorB1);
    glVertex3f(centerx, centery, centerz + h);
    for(angle = (2.0f*3.141593); angle > 0.0f; angle -= (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        y = centery + radius*cos(angle);
        glVertex3f(x, y, centerz + h);
    }
    glEnd();
}

void createCylinder2(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h)
{
    GLfloat x, z, angle;
 
    glBegin(GL_TRIANGLE_FAN);           //원기둥의 윗면
    glColor3f(102.0/255.0, 153.0/255.0, 204.0/255.0);
    glVertex3f(centerx, centery, centerz);
    for(angle = 0.0f; angle < (2.0f*3.141593); angle += (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        z = centerz + radius*cos(angle);
        glVertex3f(x, centery, z);
    }
    glEnd();

    glBegin(GL_QUAD_STRIP);            //원기둥의 옆면
    for(angle = 0.0f; angle < (2.0f*3.141593); angle += (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        z = centerz + radius*cos(angle);
        glVertex3f(x, centery, z);
        glVertex3f(x, centery + h, z);
    }
    glEnd();
 
    glBegin(GL_TRIANGLE_FAN);           //원기둥의 밑면
    glVertex3f(centerx, centery + h, centerz);
    for(angle = (2.0f*3.141593); angle > 0.0f; angle -= (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        z = centerz + radius*cos(angle);
        glVertex3f(x, centery + h, z);
    }
    glEnd();
}