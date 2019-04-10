class quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def mul(self, oq):
        return quaternion(
            self.w * oq.w - self.x * oq.x - self.y * oq.y - self.z * oq.z,
            self.w * oq.x + self.x * oq.w + self.y * oq.z - self.z * oq.y,
            self.w * oq.y - self.x * oq.z + self.y * oq.w + self.z * oq.x,
            self.w * oq.z + self.x * oq.y - self.y * oq.x + self.z * oq.w
        )

    def conjugate(self):
        return quaternion(
            self.w, (-1) * self.x, (-1) * self.y, (-1) * self.z
        )