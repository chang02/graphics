import math

class dot:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def cross(self, ov):
        result = vector(0.0, 0.0, 0.0)
        result.x = self.y * ov.z - self.z * ov.y
        result.y = self.z * ov.x - self.x * ov.z
        result.z = self.x * ov.y - self.y * ov.x
        return result

    def dot(self, ov):
        return self.x * ov.x + self.y * ov.y + self.z * ov.z
    
    def getAngle(self, ov):
        cross = self.cross(ov)
        crossSize = math.sqrt(cross.x * cross.x + cross.y * cross.y + cross.z * cross.z)
        dot = self.dot(ov)
        theta = math.atan2(crossSize, dot)
        if math.isnan(theta):
            return 0.0
        else:
            return theta
    
    def normalize(self):
        self.x = self.x / math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))
        self.y = self.y / math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))
        self.z = self.z / math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))
