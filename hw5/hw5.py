from PIL import Image
from Intersection import Intersection
from Vector import Vector
from Sphere import Sphere
from Plane import Plane
from Ray import Ray

width = 500
height = 500
camera = Vector(0, 0, 0)
lightSource = Vector(0, 10, 0)
backgroundColor = Vector(0.1, 0.1, 0.1)

objects = []

objects.append(Sphere(Vector(0, 0, 25), 50.0, Vector(0, 0, 255), 'default'))

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
        lightVector = (lightSource - minIntersection.point).normal()
        normalVector = minIntersection.normal
        rVector = (normalVector * (Vector.dot(lightVector, normalVector) * 2) - lightVector).normal()
        color = Vector(0.1, 0.1, 0.1) + (minIntersection.obj.color * max(0, Vector.dot(normalVector, lightVector))) + (Vector(1, 1, 1) * max(0, Vector.dot(rVector, lightVector)**5))
        return color

image = Image.new("RGB",(width,height),(255,255,255))
im = image.load()

for x in range(height):
    print('row', x)
    for y in range(width):
        ray = Ray(camera, (Vector(x - (width / 2), (height / 2) - y, 20) - camera).normal())
        color = getColor(ray, camera * (-1))
        im[x,y] = (round(color.x), round(color.y), round(color.z))

image.save("result2.jpg")