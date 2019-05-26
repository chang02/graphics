import math

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"
    
    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z
    
    @staticmethod
    def cross(a, b):
        return Vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normal(self):
        magnitude = self.magnitude()
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)
    
    def __add__(self, another):
        return Vector(self.x + another.x, self.y + another.y, self.z + another.z)
    
    def __sub__(self, another):
        return Vector(self.x - another.x, self.y - another.y, self.z - another.z)
    
    def __mul__(self, scalar):
        assert type(scalar) == int or type(scalar) == float
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)