
from Mathlib import *
from math import cos, pi

class Light(object):
    def __init__(self, color = [1,1,1], intensity = 1.0, lightType = "None"):
        self.color = color
        self.intensity = intensity
        self.lightType = lightType

    def GetLightColor(self, intercept = None):
        return [(i * self.intensity) for i in self.color]
    
    def GetSpecularColor(self, intercept, viewPos):
        return [0,0,0]


class AmbientLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1):
        super().__init__(color, intensity, "Ambient")


class DirectionalLight(Light):

    def __init__(self, color=[1, 1, 1], intensity=1, direction = [0,-1,0]):
        super().__init__(color, intensity, "Directional")
        self.direction = normalizeVector(direction)

    def GetLightColor(self, intercept = None):
        lightColor = super().GetLightColor()

        if intercept:
            dirLightNegative = [-x for x in self.direction]
            internsity = dotProduct(intercept.normal, dirLightNegative)
            internsity = max(0, min(1, internsity))
            internsity *= (1 - intercept.obj.material.Ks)
            internsity *= self.intensity
            lightColor = [(i * internsity) for i in lightColor]

        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dirLightNegative = [-x for x in self.direction]
            reflect = reflectVector(intercept.normal, dirLightNegative)

            viewDir = subtractVectors(viewPos, intercept.point)
            viewDir = normalizeVector(viewDir)

            #((V. R) ^n)*Ks
            specularity = max(0, dotProduct(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specColor = [(i * specularity) for i in specColor]




            
        return specColor

class PointLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0,0,0]):
        super().__init__(color, intensity)
        self.position = position
        self.lightType = "Point"

    def GetLightColor(self, intercept=None):
        # return super().GetLightColor(intercept)
        lightColor = super().GetLightColor(intercept)

        if intercept:
            dir = subtractVectors(self.position, intercept.point)

            R = magnitudeVector(dir)
            dir = normalizeVector(dir)
            # dir /= R

            internsity = dotProduct(intercept.normal, dir)
            internsity = max(0, min(1, internsity))
            internsity *= (1 - intercept.obj.material.Ks)
            lightColor = [(i * internsity) for i in lightColor]

            # Ley de cuadrados inversos
            # Attenuation = intensity / R^2
            # R es la distancia del punto intercepto a la luz punto

            if R != 0:
                internsity /= R**2

        return lightColor

    def GetSpecularColor(self, intercept, viewpos):
        specColor = self.color
      
        if intercept:
            dir = subtractVectors(self.position, intercept.point)
            R = magnitudeVector(dir) #np.linalg.norm(dir)
            dir = normalizeVector(dir) #dir/ R
            
            reflect = reflectVector(intercept.normal, dir)

            viewDir = subtractVectors(viewpos, intercept.point)
            viewDir = normalizeVector(viewDir)
            
            #specular = ((V .R )^n)* Ks
            specularity = max(0,dotProduct(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity
            
            if R!= 0:
                specularity /= (R**2)


            specColor = [(i)* specularity for i in specColor]
        return specColor

class SpotLight(PointLight):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0], direction = [0,-1,0], innerAngle = 50, outerAngle = 60):
        super().__init__(color, intensity, position)
        # self.direction = direction
        self.direction = normalizeVector(direction)
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.lightType = "Spot"

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)

        if intercept:
            lightColor=  [i * self.SpotlightAttenuation(intercept) for i in lightColor]

        return lightColor

    def GetSpecularColor(self, intercept, viewpos):
        specularColor = super().GetSpecularColor(intercept, viewpos)

        if intercept:
            specularColor = [i * self.SpotlightAttenuation(intercept) for i in specularColor]

        return specularColor

    def SpotlightAttenuation(self, intercept):
        if intercept == None:
            return 0
        wi = subtractVectors(self.position, intercept.point)
        wi = normalizeVector(wi)

        innerAngleRads = self.innerAngle * pi / 180
        outerAngleRads = self.outerAngle * pi / 180

        attenuation = (-dotProduct(self.direction, wi) - cos(outerAngleRads)) / (cos(innerAngleRads) - cos(outerAngleRads))

        attenuation = min(1, max(0, attenuation))

        return attenuation

