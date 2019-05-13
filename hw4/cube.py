from xyz import xyz
import json

class cube:
    def __init__(self, point1, point2, point3, point4, point5, point6, point7, point8):
        self.surface1 = {
            # white plastic
            "points": [point1, point2, point3, point4],
            "color": [1, 0, 0],
            "ambient": [0, 0, 0, 1],
            "diffuse": [0.55, 0.55, 0.55],
            "specular": [0.70, 0.70, 0.70],
            "shininess": 0.25
        }
        self.surface2 = {
            # yellow rubber
            "points": [point6, point5, point8, point7],
            "color": [1, 153/255, 0],
            "ambient": [0.05, 0.05, 0, 1],
            "diffuse": [0.5, 0.5, 0.4],
            "specular": [0.7, 0.7, 0.04],
            "shininess": 0.78125
        }
        self.surface3 = {
            # silver
            "points": [point2, point6, point7, point3],
            "color": [1, 1, 0],
            "ambient": [0.19225, 0.19225, 0.19225, 1],
            "diffuse": [0.50754, 0.50754, 0.50754],
            "specular": [0.508273, 0.508273, 0.508273],
            "shininess": 0.4
        }
        self.surface4 = {
            # ruby
            "points": [point3, point7, point8, point4],
            "color": [0, 1, 0],
            "ambient": [0.1745, 0.01175, 0.01175, 1],
            "diffuse": [0.61424, 0.04136, 0.04136],
            "specular": [0.727811, 0.626959, 0.626959],
            "shininess": 0.6
        }
        self.surface5 = {
            # gold
            "points": [point4, point8, point5, point1],
            "color": [0, 0, 1],
            "ambient": [0.24725, 0.1995, 0.0745, 1.0],
            "diffuse": [0.75164, 0.60648, 0.22648],
            "specular": [0.628281, 0.555802, 0.366065],
            "shininess": 0.4
        }
        self.surface6 = {
            # bronze
            "points": [point1, point5, point6, point2],
            "color": [153/255, 0, 153/255],
            "ambient": [0.2125, 0.1275, 0.054, 1],
            "diffuse": [0.714, 0.4284, 0.18144],
            "specular": [0.393548, 0.271906, 0.166721],
            "shininess": 0.25
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