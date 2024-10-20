
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
        
        contact = magnitudeVector(subtractVectors(planeIntercept.point, self.position))

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


class Triangle(Plane):
    def __init__(self, v0, v1, v2, material ):
        super().__init__(v0, normalizeVector(crossProduct(subtractVectors(v1, v0), subtractVectors(v2, v0))), material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def ray_intersect(self, orig, dir):
        t = super().ray_intersect(orig, dir)
        epsilon = 0.001
        # t = self.ray_intersect_plane(orig, dir)
        if t is None:
            return None

        P = sumVectors(orig, multiplyVectorScalar(dir, t.distance))

        # Algoritmo de Moller-Trumbore usando coordenadas baricéntricas
        edge1 = subtractVectors(self.v1, self.v0)
        edge2 = subtractVectors(self.v2, self.v0)
        h = crossProduct(dir, edge2)
        a = dotProduct(edge1, h)

        if abs(a) < epsilon:
            return None 

        f = 1.0 / a
        s = subtractVectors(orig, self.v0)
        u = f * dotProduct(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = crossProduct(s, edge1)
        v = f * dotProduct(dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        return Intercept(point=P, normal=self.normal, distance=t.distance, texCoords=[u, v], rayDirection=dir, obj=self)


class Cylinder(Shape):
    def __init__(self, position, radius, height, material, rotation_matrix = rotationElip(0,0,0)):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cylinder"
        # Crear las dos tapas del cilindro (son dos discos)
        self.top_disk = Disk([position[0], position[1] + height / 2, position[2]], [0, 1, 0], radius, material)
        self.bottom_disk = Disk([position[0], position[1] - height / 2, position[2]], [0, -1, 0], radius, material)

    def ray_intersect(self, orig, dir):
        # Primero comprobar intersección con las tapas
        top_intercept = self.top_disk.ray_intersect(orig, dir)
        bottom_intercept = self.bottom_disk.ray_intersect(orig, dir)

        # Ahora verificamos la intersección con la superficie lateral del cilindro
        # Transformar las coordenadas a un sistema local donde el cilindro está alineado con el eje y
        oc = subtractVectors(orig, self.position)
        
        a = dir[0]**2 + dir[2]**2  # x^2 + z^2
        b = 2 * (oc[0] * dir[0] + oc[2] * dir[2])
        c = oc[0]**2 + oc[2]**2 - self.radius**2

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            lateral_intercept = None
        else:
            sqrt_discriminant = discriminant ** 0.5
            t0 = (-b - sqrt_discriminant) / (2 * a)
            t1 = (-b + sqrt_discriminant) / (2 * a)

            # Escoger el t más cercano y positivo
            if t0 < 0:
                t0 = t1
            if t0 < 0:
                lateral_intercept = None
            else:
                # Calcular el punto de intersección
                P = sumVectors(orig, multiplyVectorScalar(dir, t0))
                
                # Verificar si la intersección está dentro de los límites del cilindro (en el eje y)
                y = P[1]
                if self.position[1] - self.height / 2 <= y <= self.position[1] + self.height / 2:
                    normal = normalizeVector([P[0] - self.position[0], 0, P[2] - self.position[2]])
                    lateral_intercept = Intercept(point=P, normal=normal, distance=t0, texCoords=None, rayDirection=dir, obj=self)
                else:
                    lateral_intercept = None

        # Devolver el intercepto más cercano entre tapas y superficie lateral
        closest_intercept = None
        min_t = float('inf')

        for intercept in [top_intercept, bottom_intercept, lateral_intercept]:
            if intercept is not None and intercept.distance < min_t:
                closest_intercept = intercept
                min_t = intercept.distance

        return closest_intercept


class Ellipsoid(Shape):
    def __init__(self, position, radii, rotation_matrix, material):
        super().__init__(position, material)
        self.radii = radii
        self.rotation = rotation_matrix  # Matriz de rotación 3x3
        self.type = "Ellipsoid"
        
    def ray_intersect(self, orig, dir):
        # Vector desde el origen del rayo hasta el centro de la elipsoide
        oc = subtractVectors(orig, self.position)
        
        # Aplicar la rotación inversa (traspuesta de la matriz de rotación)
        R_inv = transposeMatrix(self.rotation)
        
        # Transformar al espacio local
        oc_local = multiplyMatrixVector(R_inv, oc)
        dir_local = multiplyMatrixVector(R_inv, dir)
        
        # Normalizar por los radios
        norm_oc = [oc_local[0] / self.radii[0], oc_local[1] / self.radii[1], oc_local[2] / self.radii[2]]
        norm_dir = [dir_local[0] / self.radii[0], dir_local[1] / self.radii[1], dir_local[2] / self.radii[2]]
        
        # Coeficientes de la ecuación cuadrática
        A = dotProduct(norm_dir, norm_dir)
        B = 2 * dotProduct(norm_oc, norm_dir)
        C = dotProduct(norm_oc, norm_oc) - 1
        
        discriminant = B ** 2 - 4 * A * C
        
        if discriminant < 0:
            return None 
            
        sqrt_discriminant = sqrt(discriminant)
        t0 = (-B - sqrt_discriminant) / (2 * A)
        t1 = (-B + sqrt_discriminant) / (2 * A)
        
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # Punto de intersección en el espacio local
        P_local = sumVectors(oc_local, multiplyVectorScalar(dir_local, t0))
        
        # Transformar de vuelta al espacio mundial
        P = sumVectors(self.position, multiplyMatrixVector(self.rotation, P_local))
    
        # Calcular la normal en el espacio local
        normal_local = [
            P_local[0] / (self.radii[0] ** 2), 
            P_local[1] / (self.radii[1] ** 2), 
            P_local[2] / (self.radii[2] ** 2)
        ]
        normal_local = normalizeVector(normal_local)
    
        # Transformar la normal al espacio mundial
        normal = multiplyMatrixVector(self.rotation, normal_local)
        normal = normalizeVector(normal)
        
        u = (atan2(normal_local[2], normal_local[0]) / (2 * pi)) + 0.5
        v = acos(normal_local[1]) / pi
        
        return Intercept(point=P, 
                         normal=normal, 
                         distance=t0, 
                         texCoords=[u, v], 
                         rayDirection=dir, 
                         obj=self)


class Hemisphere(Sphere):
    def __init__(self, position, radius, normal, material):
        super().__init__(position, radius, material)
        self.normal = normalizeVector(normal)
        self.type = "Hemisphere"

    def ray_intersect(self, orig, dir):
        intercept = super().ray_intersect(orig, dir)

        if intercept is None:
            return None

        P_to_center = subtractVectors(intercept.point, self.position)


        if dotProduct(self.normal, P_to_center) < 0:
            return None

        return intercept
