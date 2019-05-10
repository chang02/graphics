from xyz import xyz
import json

class cube:
    def __init__(self, point1, point2, point3, point4, point5, point6, point7, point8):
        self.surface1 = {
            "points": [point1, point2, point3, point4],
            "color": [1, 0, 0]
            # "color": [1, 1, 1]
        }
        self.surface2 = {
            "points": [point6, point5, point8, point7],
            "color": [1, 153/255, 0]
        }
        self.surface3 = {
            "points": [point2, point6, point7, point3],
            "color": [1, 1, 0]
            # "color": [1, 1, 1]
        }
        self.surface4 = {
            "points": [point3, point7, point8, point4],
            "color": [0, 1, 0]
            # "color": [1, 1, 1]
        }
        self.surface5 = {
            "points": [point4, point8, point5, point1],
            "color": [0, 0, 1]
        }
        self.surface6 = {
            "points": [point1, point5, point6, point2],
            "color": [153/255, 0, 153/255]
        }
    
    def getSortedSurfaces(self, eyev):
        surfaceList = [self.surface1, self.surface2, self.surface3, self.surface4, self.surface5, self.surface6]
        def getnv(surface):
            [point1, point2, point3, point4] = surface["points"]
            vector1 = point2 - point3
            vector2 = point4 - point3
            nv = xyz.crossProduct(vector1, vector2)
            return nv

        def compareSurface(surface1, surface2, eyev):
            nv1 = getnv(surface1)
            nv2 = getnv(surface2)
            theta1 = abs(xyz.getTheta(nv1, eyev))
            theta2 = abs(xyz.getTheta(nv2, eyev))
            if theta1 > theta2:
                return 1
            elif theta1 == theta2:
                return 0
            elif theta1 < theta2:
                return -1

        def swap(surfaceList, i, j):
            temp = surfaceList[i]
            surfaceList[i] = surfaceList[j]
            surfaceList[j] = temp
            return surfaceList

        def sort(surfaceList, eyev):
            for i in range(len(surfaceList)-1, 0, -1):
                for j in range(0, i):
                    if compareSurface(surfaceList[j], surfaceList[j+1], eyev) < 0:
                        surfaceList = swap(surfaceList, j, j+1)
            return surfaceList
        
        surfaceList = sort(surfaceList, eyev)
        return surfaceList


    def getFrontBackSurfaces(self, eyev):
        frontSurfaces = []
        backSurfaces = []

        def getnv(surface):
            [point1, point2, point3, point4] = surface["points"]
            vector1 = point2 - point3
            vector2 = point4 - point3
            nv = xyz.crossProduct(vector1, vector2)
            return nv
        
        nv1 = getnv(self.surface1)
        theta1 = abs(xyz.getTheta(nv1, eyev))
        if theta1 <= 1.570796:
            frontSurfaces.append(self.surface1)
        else:
            backSurfaces.append(self.surface1)

        nv2 = getnv(self.surface2)
        theta2 = abs(xyz.getTheta(nv2, eyev))
        if theta2 <= 1.570796:
            frontSurfaces.append(self.surface2)
        else:
            backSurfaces.append(self.surface2)

        nv3 = getnv(self.surface3)
        theta3 = abs(xyz.getTheta(nv3, eyev))
        if theta3 <= 1.570796:
            frontSurfaces.append(self.surface3)
        else:
            backSurfaces.append(self.surface3)

        nv4 = getnv(self.surface4)
        theta4 = abs(xyz.getTheta(nv4, eyev))
        if theta4 <= 1.570796:
            frontSurfaces.append(self.surface4)
        else:
            backSurfaces.append(self.surface4)

        nv5 = getnv(self.surface5)
        theta5 = abs(xyz.getTheta(nv5, eyev))
        if theta5 <= 1.570796:
            frontSurfaces.append(self.surface5)
        else:
            backSurfaces.append(self.surface5)

        nv6 = getnv(self.surface6)
        theta6 = abs(xyz.getTheta(nv6, eyev))
        if theta6 <= 1.570796:
            frontSurfaces.append(self.surface6)
        else:
            backSurfaces.append(self.surface6)
        
        return {
            "frontSurfaces": frontSurfaces,
            "backSurfaces": backSurfaces,
        }