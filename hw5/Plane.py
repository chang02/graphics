from Vector import Vector
from Intersection import Intersection

class Plane:
    def __init__(self, point, normal, ambColor, difColor, speColor, typ, minxyz, maxxyz):
        self.point = point
        self.normal = normal
        self.ambColor = ambColor
        self.difColor = difColor
        self.speColor = speColor
        self.type = typ
        self.minxyz = minxyz
        self.maxxyz = maxxyz
    
    def getIntersection(self, ray):
        dot = Vector.dot(self.normal, ray.direction)
        if abs(dot) < 0.0001:
            return None
        else:
            difference = self.point - ray.origin
            t = Vector.dot(difference, self.normal) / dot
            if t > 0.0001:
                point = ray.origin + ray.direction * t
                if self.minxyz.x <= point.x <= self.maxxyz.x and self.minxyz.y <= point.y <= self.maxxyz.y and self.minxyz.z <= point.z <= self.maxxyz.z:
                    return Intersection(point, t, self.normal, self)
                else:
                    return None
            else:
                return None