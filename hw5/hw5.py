from PIL import Image
from Intersection import Intersection
from Vector import Vector
from Sphere import Sphere
from Plane import Plane
from Ray import Ray
import math

width = 900
height = 600
camera = Vector(0, 100, 0)
lightSource = Vector(-300, 300, 0)
backgroundColor = Vector(0.1, 0.1, 0.1)

objects = []

objects.append(Sphere(Vector(0, -200, 630), 40.0, Vector(255, 0, 0), Vector(255, 0, 0), Vector(255, 0, 0), 'default'))
objects.append(Sphere(Vector(0, -200, 520), 40.0, Vector(255, 0, 255), Vector(255, 0, 255), Vector(255, 0, 255), 'default'))

objects.append(Plane(Vector(0, -240, 500), Vector(0, 1, 0), Vector(0, 255, 255), Vector(0, 255, 255), Vector(0, 255, 255), 'default', Vector(-10000, -241, -10000), Vector(10000, -239, 10000)))
objects.append(Plane(Vector(0, -240, 800), Vector(1.5, 0, -1).normal(), Vector(0, 0, 0), Vector(0, 0, 0), Vector(255, 255, 255), 'reflection', Vector(-220, -239, 100), Vector(0, 10, 800)))
objects.append(Plane(Vector(0, -240, 800), Vector(-1.5, 0, -1).normal(), Vector(0, 0, 0), Vector(0, 0, 0),  Vector(255, 255, 255), 'reflection', Vector(0, -239, 100), Vector(220, 10, 800)))

objects.append(Sphere(Vector(-500, -200, 620), 50, Vector(255, 0, 0), Vector(255, 0, 0),  Vector(255, 0, 0), 'default'))
objects.append(Sphere(Vector(-400, -200, 350), 50, Vector(255, 255, 0), Vector(255, 255, 0),  Vector(255, 255, 0), 'default'))
objects.append(Sphere(Vector(-450, -200, 500), 50, Vector(0, 0, 0), Vector(150, 171, 186),  Vector(230, 230, 230), 'reflection_refraction'))

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
        if intersection.obj != obj and intersection.obj.type != 'reflection_refraction':
            flag = True
    return flag

def getColor(ray, eye, recur):
    intersections = getIntersections(ray)

    if recur > 15:
        color = backgroundColor * 0.1
        return color

    if len(intersections) == 0:
        color = backgroundColor * 0.1
        return color
    else:
        minIntersection = getMinIntersection(intersections)
        lVector = (lightSource - minIntersection.point).normal()
        nVector = minIntersection.normal
        vVector = (eye - minIntersection.point).normal()
        rVector = (nVector * (Vector.dot(lVector, nVector) * 2) - lVector).normal()
        hVector = (nVector * (Vector.dot(vVector, nVector) * 2) - vVector).normal()
        if minIntersection.obj.type == 'default':
            if isShade(minIntersection.obj, minIntersection.point):
                color = minIntersection.obj.ambColor * 0.1
                return color
            else:
                color = minIntersection.obj.ambColor * 0.1 + (minIntersection.obj.difColor * max(0, Vector.dot(nVector, lVector))) * 0.3 + (minIntersection.obj.speColor * max(0, Vector.dot(rVector, vVector)**15) * 0.5)
                return color
        elif minIntersection.obj.type == 'reflection':
            newRay = Ray(minIntersection.point, hVector)
            newEye = minIntersection.point
            color = getColor(newRay, newEye, recur + 1)
            return color
        elif minIntersection.obj.type == 'reflection_refraction':
            ndotv = Vector.dot(nVector, vVector)
            if ndotv > 0:
                nr = 1 / 1.2
                d = nVector * (ndotv * nr - math.sqrt(1 - (nr * nr * (1 - (ndotv * ndotv))))) - (vVector * nr)

                color = minIntersection.obj.ambColor * 0.1 + (minIntersection.obj.difColor * max(0, Vector.dot(nVector, lVector))) * 0.3 + (minIntersection.obj.speColor * max(0, Vector.dot(rVector, vVector)**15) * 0.5)

                newRay1 = Ray(minIntersection.point, d)
                newEye1 = minIntersection.point
                color1 = getColor(newRay1, newEye1, recur + 1)
                newRay2 = Ray(minIntersection.point, hVector)
                newEye2 = minIntersection.point
                color2 = getColor(newRay2, newEye2, recur + 1)
                return color * 0.333 + color1 * 0.333 + color2 * 0.333
            elif ndotv < 0:
                nr = 1.2 / 1
                nVector = nVector * (-1)
                d = nVector * (ndotv * nr - math.sqrt(1 - (nr * nr * (1 - (ndotv * ndotv))))) - (vVector * nr)
                newRay1 = Ray(minIntersection.point, d)
                newEye1 = minIntersection.point
                color1 = getColor(newRay1, newEye1, recur + 1)

                vVector = (eye - minIntersection.point).normal()
                rVector = (nVector * (Vector.dot(lVector, nVector) * 2) - lVector).normal()
                hVector = (nVector * (Vector.dot(vVector, nVector) * 2) - vVector).normal()
                newRay2 = Ray(minIntersection.point, hVector)
                newEye2 = minIntersection.point
                color2 = getColor(newRay2, newEye2, recur + 1)

                color = minIntersection.obj.ambColor * 0.1 + (minIntersection.obj.difColor * max(0, Vector.dot(nVector, lVector))) * 0.3 + (minIntersection.obj.speColor * max(0, Vector.dot(rVector, vVector)**15) * 0.5)
                return color * 0.333 + color1 * 0.333 + color2 * 0.333

            else:
                color = backgroundColor * 0.1
                return color
        # elif minIntersection.obj.type == 'refraction':
        #     ndotv = Vector.dot(nVector, vVector)
        #     if ndotv > 0:
        #         nr = 1 / 1.1
        #         d = nVector * (ndotv * nr - math.sqrt(1 - (nr * nr * (1 - (ndotv * ndotv))))) - (vVector * nr)
        #         newRay = Ray(minIntersection.point, d)
        #         newEye = minIntersection.point
        #         color = getColor(newRay, newEye, recur + 1)
        #         return color
        #     elif ndotv < 0:
        #         nr = 1.1 / 1
        #         nVector = nVector * (-1)
        #         d = nVector * (ndotv * nr - math.sqrt(1 - (nr * nr * (1 - (ndotv * ndotv))))) - (vVector * nr)
        #         newRay = Ray(minIntersection.point, d)
        #         newEye = minIntersection.point
        #         color = getColor(newRay, newEye, recur + 1)
        #         return color

        #     else:
        #         color = backgroundColor * 0.1
        #         return color
                            
        else:
            color = backgroundColor * 0.1
            return color

image = Image.new("RGB",(width,height),(255,255,255))
im = image.load()

for x in range(height):
    print('row', x)
    for y in range(width):
        ray = Ray(camera, (Vector(y - (width / 2), (height / 2) - x, 300) - camera).normal())
        color = getColor(ray, camera, 0)
        im[y,x] = (round(color.x), round(color.y), round(color.z))

image.save("result2.jpg")