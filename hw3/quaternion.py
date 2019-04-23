import math

class quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def magnitude(self):
        return math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)
    
    def conjugate(self):
        result = quaternion(self.w, self.x * (-1), self.y * (-1), self.z * (-1))
        return result
    
    @staticmethod
    def multiply(a, b):
        tempw = a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z
        tempx = a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y
        tempy = a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x
        tempz = a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w
        result = quaternion(tempw, tempx, tempy, tempz)
        return result

    @staticmethod
    def rotate(rotateQuaternion, pointQuaternion):
        rotateQuaternion_ = rotateQuaternion.conjugate()
        result = quaternion.multiply(rotateQuaternion, pointQuaternion)
        result = quaternion.multiply(result, rotateQuaternion_)
        return result
        