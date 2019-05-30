from Vector import Vector
from Intersection import Intersection
import math
from PIL import Image

class Sphere:
    def __init__(self, center, radius, color, typ, texture):
        self.center = center
        self.radius = radius
        self.color = color
        self.type = typ
        self.texture = texture
        self.texture = texture
        if texture != None:
            self.im = Image.open(texture)
            self.px = self.im.load()
    
    def normal(self, surfacePoint):
        return (surfacePoint - self.center).normal()

    def getIntersection(self, ray):
        ocVector = ray.origin - self.center
        a = Vector.dot(ray.direction, ray.direction)
        b = Vector.dot(ocVector, ray.direction) * 2
        c = Vector.dot(ocVector, ocVector) - (self.radius * self.radius)
        discriminant = (b * b) - (4 * a * c)
        if discriminant < 0:
            return None
        else:
            t = (-b - math.sqrt(discriminant)) / (2.0 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2.0 * a)
            if t > 0.0001:
                return Intersection(ray.origin + ray.direction * t, t, self.normal(ray.origin + ray.direction * t), self)
            elif t2 > 0.0001:
                return Intersection(ray.origin + ray.direction * t2, t2, self.normal(ray.origin + ray.direction * t2), self)
            else:
                return None
    
    def getColor(self, point):
        if self.texture == None:
            return self.color
        else:
            width, height = self.im.size
            d = (self.center - point).normal()
            u = 0.5 + math.atan2(d.z, d.x) / (2 * 3.1416)
            v = 0.5 - math.asin(d.y) / 3.1416
            uCoord = u * width
            vCoord = (1 - v) * height
            r, g, b = self.px[uCoord, vCoord]
            return Vector(r, g, b)