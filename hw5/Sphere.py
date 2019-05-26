from Vector import Vector
from Intersection import Intersection
import math

class Sphere:
    def __init__(self, center, radius, color, typ):
        self.center = center
        self.radius = radius
        self.color = color
        self.type = typ
    
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
            return Intersection(ray.origin + ray.direction * t, t, self.normal(ray.origin + ray.direction * t), self)
    # def getIntersection(self, ray):
    #     q = Vector.dot(ray.direction, ray.origin - self.center)**2 - Vector.dot(ray.origin - self.center, ray.origin - self.center) + self.radius**2
    #     if q < 0:
    #         return None
    #     else:
    #         d = Vector.dot(ray.direction * (-1), ray.origin - self.center)
    #         d1 = d - math.sqrt(q)
    #         d2 = d + math.sqrt(q)
    #         if 0 < d1 and ( d1 < d2 or d2 < 0):
    #             return Intersection(ray.origin + ray.direction * d1, d1, self.normal(ray.origin + ray.direction * d1), self)
    #         elif 0 < d2 and ( d2 < d1 or d1 < 0):
    #             return Intersection(ray.origin + ray.direction * d2, d2, self.normal(ray.origin+ray.direction * d2), self)
    #         else:
    #             return None