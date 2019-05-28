from Vector import Vector
from Intersection import Intersection
import math

class Sphere:
    def __init__(self, center, radius, color, typ, texture):
        self.center = center
        self.radius = radius
        self.color = color
        self.type = typ
        self.texture = texture
    
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
            if t > 0.0001:
                return Intersection(ray.origin + ray.direction * t, t, self.normal(ray.origin + ray.direction * t), self)
            else:
                return None
    
    def getColor(self, point):
        if self.texture == None:
            return self.color