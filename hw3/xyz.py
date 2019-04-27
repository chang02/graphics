import math

class xyz:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'

    @staticmethod
    def crossProduct(a, b):
        tempx = a.y * b.z - a.z * b.y
        tempy = a.z * b.x - a.x * b.z
        tempz = a.x * b.y - a.y * b.x
        result = xyz(tempx, tempy, tempz)
        return result

    @staticmethod
    def dotProduct(a, b):
        return a.x * b.x + a.y * b.y
    
    @staticmethod
    def getTheta(a, b):
        cross = xyz.crossProduct(a, b)
        crossScale = math.sqrt(cross.x * cross.x + cross.y * cross.y + cross.z * cross.z)
        dot = a.x * b.x + a.y * b.y + a.z * b.z
        theta = math.atan2(crossScale, dot)
        return theta

    def normalize(self):
        scale = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        if scale == 0:
            return xyz(0, 0, 0)
        else:
            tempx = self.x / scale
            tempy = self.y / scale
            tempz = self.z / scale
            result = xyz(tempx, tempy, tempz)
            return result