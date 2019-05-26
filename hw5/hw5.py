from Intersection import Intersection
from Vector import Vector
from Sphere import Sphere
from Plane import Plane
from Ray import Ray

width = 500
height = 500
camera = Vector(0, 0, 0)
lightSource = Vector(0, 10, 0)
lightAmb = Vector(0.1, 0.1, 0.1)

objects = []

objects.append(Sphere(Vector(0, 0, 30), 5.0, Vector(0, 0, 255)))

def getMinIntersection(intersections):
        ret = intersections[0]
        for intersection in intersections:
                if intersection.distance < ret.distance:
                        ret = intersection
        return ret

def getColor(ray):
        intersections = []
        for obj in objects:
                if obj.getIntersection != None:
                        intersections.append(obj.getIntersection)
        if len(intersections) == 0:
                color = lightAmb
                return color
        else:
                minIntersection = getMinIntersection(intersections)


for x in range(height):
    print('row', x)
    for y in range(width):
        ray = Ray(camera, (Vector(x - (width / 2), (height / 2) - y, 20) - camera).normal())
        color = getColor(ray)
        