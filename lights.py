
from Mathlib import *

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
            specularity *= self.intensity

            specColor = [(i * specularity) for i in specColor]




            
        return specColor