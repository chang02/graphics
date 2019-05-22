from Intersection import Intersection
from Vector import Vector
from Sphere import Sphere
from Plane import Plane
from Ray import Ray

width = 500
height = 500

objects = []
lightSource = Vector(0, 0, -10)
camera = Vector(0, 0, 0)

for x in range(height):
    print('row', x)
    for y in range(width):
        ray = Ray(camera, (Vector(x - (width / 2), (height / 2) - y, 20) - camera).normal())