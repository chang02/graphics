from Vector import Vector
from Intersection import Intersection

class Plane:
    def __init__(self, point, normal, color):
        self.normal = normal
        self.point = point
        self.color = color
    
    def getIntersection(self, ray):
        dot = Vector.dot(self.normal, ray.direction)
        if abs(dot) < 0.0001:
            return None
        else:
            difference = self.point - ray.origin
            t = Vector.dot(difference, self.normal) / dot
            if t > 0.0001:
                return Intersection(ray.origin + ray.direction * t, t, self.normal, self)
            else:
                return None