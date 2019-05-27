from PIL import Image
from Intersection import Intersection
from Vector import Vector
from Sphere import Sphere
from Plane import Plane
from Ray import Ray

width = 900
height = 600
camera = Vector(0, 0, 0)
lightSource = Vector(-300, 300, 0)
backgroundColor = Vector(0.1, 0.1, 0.1)

objects = []

objects.append(Sphere(Vector(0, -180, 500), 80.0, Vector(255,0, 0), 'default'))
objects.append(Plane(Vector(0, -260, 500), Vector(0, 1, 0), Vector(200, 200, 200), 'default'))
def getIntersections(ray):
    intersections = []
    for obj in objects:
        if obj.getIntersection(ray) != None:
            intersections.append(obj.getIntersection(ray))
    return intersections

def getMinIntersection(intersections):
    ret = intersections[0]
    for intersection in intersections:
        if intersection.distance < ret.distance:
            ret = intersection
    return ret

def isShade(obj, surfacePoint):
    lVector = lightSource - surfacePoint
    ray = Ray(surfacePoint, lVector.normal())
    intersections = getIntersections(ray)
    flag = False
    for intersection in intersections:
        if intersection.obj != obj:
            flag = True
    return flag

def getColor(ray, eye):
    intersections = getIntersections(ray)

    if len(intersections) == 0:
        color = backgroundColor
        return color
    else:
        minIntersection = getMinIntersection(intersections)
        lVector = (lightSource - minIntersection.point).normal()
        nVector = minIntersection.normal
        rVector = (nVector * (Vector.dot(lVector, nVector) * 2) - lVector).normal()
        vVector = (eye - minIntersection.point).normal()
        if minIntersection.obj.type == 'default':
            if isShade(minIntersection.obj, minIntersection.point):
                color = minIntersection.obj.color * 0.1
                return color
            else:
                color = minIntersection.obj.color * 0.1 + (minIntersection.obj.color * max(0, Vector.dot(nVector, lVector))) * 0.3 + (minIntersection.obj.color * max(0, Vector.dot(rVector, vVector)**15) * 0.5)
                return color

image = Image.new("RGB",(width,height),(255,255,255))
im = image.load()

for x in range(height):
    print('row', x)
    for y in range(width):
        ray = Ray(camera, (Vector(y - (width / 2), (height / 2) - x, 300) - camera).normal())
        color = getColor(ray, camera)
        im[y,x] = (round(color.x), round(color.y), round(color.z))

image.save("result2.jpg")