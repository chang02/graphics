#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/freeglut.h>
#include <iostream>
#include <cmath>
#include <algorithm>
void glutMouse(int button, int state, int x, int y);
void glutMotion(int x, int y);
void Timer(int unused);
void keyboard(unsigned char key, int x, int y);
void resize(int x, int y);
void loadGlobalCoord();
void display();
void createBox(GLfloat x, GLfloat y, GLfloat z, GLfloat colorR, GLfloat colorG, GLfloat colorB);
void createCylinder(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h, 
GLfloat colorR1, GLfloat colorG1, GLfloat colorB1,
GLfloat colorR2, GLfloat colorG2, GLfloat colorB2);
void createCylinder2(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h);

int width, height;
float eye[3] = { 0.0f, 0.0f, 300.0f };
float ori[3] = { 0.0f, 0.0f, 0.0f };
float rot[3] = { 0.0f, 0.0f, 0.0f };
bool leftButton = false;
GLfloat mousePosX, mousePosY;
GLdouble rotMatrix[16] =
{
	1, 0, 0, 0,
	0, 1, 0, 0,
	0, 0, 1, 0,
	0, 0, 0, 1
};

int main(int argc, char **argv) {
    glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
	glutInitWindowSize(1200, 800);
	glutInitWindowPosition( 50, 0 );
	glutCreateWindow("HW1");

    glutReshapeFunc(resize);
	glutDisplayFunc(display);
	glutTimerFunc(30, Timer, 0);
	glutKeyboardFunc(keyboard);
	glutMouseFunc(glutMouse);
	glutMotionFunc(glutMotion);

	glutMainLoop();

    return 0;
}

void glutMouse(int button, int state, int x, int y) {
	switch ( button )
	{
		case GLUT_LEFT_BUTTON:
			if ( state == GLUT_DOWN )
			{
				mousePosX = x;
				mousePosY = y;
				leftButton = true;
			}
			else if ( state == GLUT_UP )
			{
				leftButton = false;
			}
			break;
		case GLUT_RIGHT_BUTTON:break;
		case 3:break;
		default:break;
	}
	return;
}

void glutMotion(int x, int y) {
	if ( leftButton ) {
		float dx = x - mousePosX;
		float dy = y - mousePosY;

		mousePosX = x;
		mousePosY = y;

		ori[0] -= dx*0.04;
		ori[1] += dy*0.04;

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
	default:
		break;
	}
}

void resize(int x, int y) {
    width = x;
	height = y;
	glViewport(0, 0, x, y);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(45.0f, (GLfloat)x / (GLfloat)y, .1f, 500.0f);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
}

void loadGlobalCoord() {
    glLoadIdentity();
	gluLookAt(eye[0], eye[1], eye[2], ori[0], ori[1], ori[2], 0, 1, 0);
	glMultMatrixd(rotMatrix);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glEnable(GL_DEPTH_TEST);
	loadGlobalCoord();

	glRotatef(-60,1,0,0);
	glRotatef(25,0,0,1);
    glTranslatef(0, -10, 100);

	// 4 column -----------------------------------------
	glPushMatrix();
	{
		glBegin(GL_POLYGON);
		glColor3f(0.4,0.2,0.8);
		glVertex3f(-130, -130, -107);
		glVertex3f(-130, 130, -107);
		glVertex3f(130, 130, -107);
		glVertex3f(130, -130, -107);
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