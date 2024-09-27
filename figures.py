
from Mathlib import *
from intercept import Intercept
from math import atan2, acos, pi, isclose

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

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normalizeVector(normal)
        self.type = "Plane"
    
    def ray_intersect(self, orig, dir):
        # Distancia = ((planePos - rayOrig) . normal) / (rayDir )

        denom = dotProduct(dir, self.normal)

        if isclose(0, denom):
            return None
        
        num = dotProduct(subtractVectors(self.position, orig), self.normal)

        t = num / denom

        if t < 0:
            return None
        
        P = sumVectors(orig, multiplyVectorScalar(dir, t))

        return Intercept(point=P,
                         normal= self.normal,
                         distance=t,
                         texCoords= None,
                         rayDirection=dir,
                         obj=self)



class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"

    def ray_intersect(self, orig, dir):
        planeIntercept =  super().ray_intersect(orig, dir)

        if planeIntercept is None:
            return None
        
        contact = subtractVectors(planeIntercept.point, self.position)
        contact = normalizeVector(contact)

        if contact > self.radius:
            return None

        return planeIntercept
    
        
class AABB(Shape):
    # Axis Aligned Bounding Box
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        # Planes
        self.planes = []

        rightPlane = Plane([self.position[0] + sizes[0]/2, self.position[1], self.position[2]], [1,0,0], material)
        leftPlane = Plane([self.position[0] - sizes[0]/2, self.position[1], self.position[2]], [-1,0,0], material)

        
        upPlane = Plane([self.position[0], self.position[1] + sizes[1]/2, self.position[2]], [0,1,0], material)
        downPlane = Plane([self.position[0], self.position[1] - sizes[1]/2, self.position[2]], [0,-1,0], material)

        
        fontPlane = Plane([self.position[0], self.position[1], self.position[2] + sizes[2]/2], [0,0,1], material)
        backPlane = Plane([self.position[0], self.position[1] , self.position[2] - sizes[2]/2], [0,0,-1], material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(fontPlane)
        self.planes.append(backPlane)

        # Bouce
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i]/2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i]/2)
        
    def ray_intersect(self, orig, dir):
        
        intercept = None
        t = float("inf")

        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:
                planePoint = planeIntercept.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:

                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept

        if intercept == None:
            return None

        u, v = 0,0

        if abs(intercept.normal[0]) > 0:
            # Mapear las uvs para el jee x, usando las coordenadas de Y y Z
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[1]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]

        elif abs(intercept.normal[2]) > 0:
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
        
        return Intercept(point=intercept.point,
                         normal=intercept.normal,
                         distance=t, 
                         texCoords=[u,v],
                         rayDirection=dir,
                         obj=self)


