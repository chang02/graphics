import Vector

class Dot:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, another):
        return Dot(self.x + another.x, self.y + another.y, self.z + another.z)
    
    def __sub__(self, another):
        return Vector(self.x - another.x, self.y - another.y, self.z - another.z)
    
    def __mul__(self, scalar):
        assert type(scalar) == int or type(scalar) == float
        return Dot(self.x * scalar, self.y * scalar, self.z * scalar)
