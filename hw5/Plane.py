from Vector import Vector
from Intersection import Intersection
from PIL import Image

class Plane:
    def __init__(self, point, normal, color, typ, minxyz, maxxyz, texture):
        self.point = point
        self.normal = normal
        self.color = color
        self.type = typ
        self.minxyz = minxyz
        self.maxxyz = maxxyz
        self.texture = texture
        if texture != None:
            self.im = Image.open(texture)
            self.px = self.im.load()
    
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
        
    def getColor(self, point):
        if self.texture == None:
            return self.color
        else:
            width, height = self.im.size
            u = Vector(self.normal.y, self.normal.x * (-1), 0)
            v = Vector.cross(u, self.normal)
            uCoord = Vector.dot(u, point) % width - 1
            vCoord = Vector.dot(v, point) % height - 1
            r, g, b = self.px[uCoord, vCoord]
            return Vector(r, g, b)