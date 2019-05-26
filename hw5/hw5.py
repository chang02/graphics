from PIL import Image
from Intersection import Intersection
from Vector import Vector
from Sphere import Sphere
from Plane import Plane
from Ray import Ray

width = 500
height = 500
camera = Vector(0, 0, 0)
lightSource = Vector(-300, 300, 0)
backgroundColor = Vector(0.1, 0.1, 0.1)

objects = []

objects.append(Sphere(Vector(0, 0, 500), 100.0, Vector(255,255, 0), 'default'))

def getMinIntersection(intersections):
    ret = intersections[0]
    for intersection in intersections:
        if intersection.distance < ret.distance:
            ret = intersection
    return ret

def getColor(ray, eye):
    intersections = []
    for obj in objects:
        if obj.getIntersection(ray) != None:
            intersections.append(obj.getIntersection(ray))
    if len(intersections) == 0:
        color = backgroundColor
        return color
    else:
        minIntersection = getMinIntersection(intersections)
        lVector = (lightSource - minIntersection.point).normal()
        nVector = minIntersection.normal
        rVector = (nVector * (Vector.dot(lVector, nVector) * 2) - lVector).normal()
        vVector = (eye - minIntersection.point).normal()
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