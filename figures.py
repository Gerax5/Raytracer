
from Mathlib import *
from intercept import Intercept
from math import atan2, acos, pi

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None

    

class Sphere(Shape):

    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Shphere"

    def ray_intersect(self, orig, dir):
        #return super().ray_intersect(orig, dir)
        L = subtractVectors(self.position, orig)

        tca = dotProduct(L, dir)

        d = (magnitudeVector(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d **2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None
            
        P = sumVectors(orig, 
                        multiplyVectorScalar(dir, t0)
                        )
        normal = subtractVectors(P, self.position)
        normal = normalizeVector(normal)

        u = (atan2(normal[2], normal[0]) / (2*pi) + 0.5) 
        v = acos(-normal[1]) / pi

        # P1 = orig + dir*t1

        return Intercept(point = P, 
                         normal= normal,
                         distance=t0,
                         obj= self,
                         texCoords=[u,v],
                         rayDirection = dir
                         )