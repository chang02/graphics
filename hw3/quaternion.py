import math
from xyz import xyz

class quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, scalar):
        return quaternion(self.w / scalar, self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __mul__(self, other):
        if isinstance(other, quaternion):
            tempw = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            tempx = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            tempy = self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z
            tempz = self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x
            return quaternion(tempw, tempx, tempy, tempz)
        else:
            return quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
    
    def normalize(self):
        length = self.magnitude()
        tempw = self.w / length
        tempx = self.x / length
        tempy = self.y / length
        tempz = self.z / length
        return quaternion(tempw, tempx, tempy, tempz)

    def magnitude(self):
        return math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)
    
    def conjugate(self):
        result = quaternion(self.w, self.x * (-1), self.y * (-1), self.z * (-1))
        return result
    
    def toAngleAxis(self):
        angle = 2 * math.acos(self.w)
        tempx = self.x / math.sqrt(1 - self.w * self.w)
        tempy = self.y / math.sqrt(1 - self.w * self.w)
        tempz = self.z / math.sqrt(1 - self.w * self.w)
        axis = xyz(tempx, tempy, tempz)
        return (angle, axis)
    
    @staticmethod
    def slerp(q1, q2, t):
        if q1.w * q2.w + q1.x + q2.x + q1.y + q2.y + q1.z + q2.z > 0.999:
            return quaternion(q1.w * (1 - t) + q2.w * t, q1.x * (1 - t) + q2.x * t, q1.y * (1 - t) + q2.y * t, q1.z * (1 - t) + q2.z * t)
        else:
            return (q1 * (q1.conjugate() * q2) * t)

    #     if (q1.s_ * q2.s_ + Vector<T, 3>::DotProduct(q1.v_, q2.v_) > 0.999999f)
    #      return Quaternion<T>(q1.s_ * (1 - s1) + q2.s_ * s1,
    #                           q1.v_ * (1 - s1) + q2.v_ * s1);
    #    return q1 * ((q1.Inverse() * q2) * s1);

    @staticmethod
    def rotate(rotateQuaternion, point):
        pointQuaternion = quaternion(0, point.x, point.y, point.z)
        rotateQuaternion_ = rotateQuaternion.conjugate()
        result = rotateQuaternion * pointQuaternion * rotateQuaternion_
        return xyz(result.x, result.y, result.z)
        