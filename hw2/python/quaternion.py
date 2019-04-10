class quaternion:
    def __init__(self, w, x, y, z):
        self.w = round(w, 6)
        self.x = round(x, 6)
        self.y = round(y, 6)
        self.z = round(z, 6)

    def mul(self, oq):
        return quaternion(
            round(self.w * oq.w - self.x * oq.x - self.y * oq.y - self.z * oq.z, 6),
            round(self.w * oq.x + self.x * oq.w + self.y * oq.z - self.z * oq.y, 6),
            round(self.w * oq.y - self.x * oq.z + self.y * oq.w + self.z * oq.x, 6),
            round(self.w * oq.z + self.x * oq.y - self.y * oq.x + self.z * oq.w, 6)
        )

    def conjugate(self):
        return quaternion(
            self.w, (-1) * self.x, (-1) * self.y, (-1) * self.z
        )