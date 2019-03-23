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
void createCylinder(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h);

int width, height;
float eye[3] = { 0.0f, 0.0f, 100.0f };
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
	glutInitWindowSize(400, 400);
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

void Timer(int unused) {
	/* call the display callback and forces the current window to be displayed */
	glutPostRedisplay();
	glutTimerFunc(0, Timer, 0);
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
	glPushMatrix();

    createCylinder(0, 0, 0, 30, -3);

	glutSwapBuffers();
}

void createCylinder(GLfloat centerx, GLfloat centery, GLfloat centerz, GLfloat radius, GLfloat h)
{
    GLfloat x, y, angle;
 
    glBegin(GL_TRIANGLE_FAN);           //원기둥의 윗면
    glNormal3f(0.0f, 0.0f, -1.0f);
    glColor3f(1, 1, 1);
    glVertex3f(centerx, centery, centerz);
 
    for(angle = 0.0f; angle < (2.0f*3.141593); angle += (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        y = centery + radius*cos(angle);
        glNormal3f(0.0f, 0.0f, -1.0f);
        glVertex3f(x, y, centerz);
    }
    glEnd();
 
    glBegin(GL_QUAD_STRIP);            //원기둥의 옆면
	glColor3f(0.2, 0.8, 0.7);
    for(angle = 0.0f; angle < (2.0f*3.141593); angle += (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        y = centery + radius*cos(angle);
        glNormal3f(sin(angle), cos(angle), 0.0f);
        glVertex3f(x, y, centerz);
        glVertex3f(x, y, centerz + h);
    }
    glEnd();
 
    glBegin(GL_TRIANGLE_FAN);           //원기둥의 밑면
    glNormal3f(0.0f, 0.0f, 1.0f);
	glColor3f(1, 1, 1);
    glVertex3f(centerx, centery, centerz + h);
    for(angle = (2.0f*3.141593); angle > 0.0f; angle -= (3.141593/360.0f))
    {
        x = centerx + radius*sin(angle);
        y = centery + radius*cos(angle);
        glNormal3f(0.0f, 0.0f, 1.0f);
        glVertex3f(x, y, centerz + h);
    }
    glEnd();
}