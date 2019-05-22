import math

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    @staticmethod
    def dot(self, another):
        return self.x * another.x + self.y * another.y + self.z * another.z
    
    @staticmethod
    def cross(self, another):
        return Vector(self.y * another.z - self.z * another.y, self.z * another.b - self.x * another.z, self.x * another.y - self.y * another.x)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normal(self):
        magnitude = self.magnitude
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)
    
    def __add__(self, another):
        return Vector(self.x + another.x, self.y + another.y, self.z + another.z)
    
    def __sub__(self, another):
        return Vector(self.x - another.x, self.y - another.y, self.z + another.z)
    
    def __mul__(self, scalar):
        assert type(another) == int or type(another) == float
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)