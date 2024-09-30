
from Mathlib import *
from refractionFunctions import *
OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse=[1,1,1], spec = 1.0, Ks = 0.0, ior = 1.0, matType = OPAQUE, texture = None):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks
        self.matType = matType
        self.texture = texture
        self.ior = ior

    def GetSurfaceColor(self, intercept, renderer, recursion = 0):
        # Phong reflection model
        # LightColor = LightColor + Specular
        # FinalColor = DiffuseColor * LightColor

        LightColor = [0,0,0]
        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        finalColor = self.diffuse
        
        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [(finalColor[i] * textureColor[i]) for i in range(3)]


        for light in renderer.lights:
            shadowIntercept = None
            lightDir = None

            if light.lightType == "Directional":
                lightDir = [(-i) for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)                
            elif light.lightType == "Point":
                lightDir = subtractVectors(light.position, intercept.point)
                R = magnitudeVector(lightDir)
                lightDir = normalizeVector(lightDir)
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)
                if shadowIntercept:
                    if shadowIntercept.distance >= R:
                        shadowIntercept = None

            if shadowIntercept == None:
                
                LightColor = [(LightColor[i] + light.GetSpecularColor(intercept, renderer.camera.translate)[i]) for i in range(3)]

                # currentLightColor = light.GetLightColor(intercept)
                # currentSpecularColor = light.GetSpecularColor(intercept, renderer.camera.translate)
                if self.matType == OPAQUE:
                    LightColor = [(LightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]

        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectIntercept = renderer.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

        elif self.matType == TRANSPARENT:
            # Revisamos si estamos afuera
            outside = dotProduct(intercept.normal, intercept.rayDirection) < 0

            # Agregar margen de error
            bias = [i * 0.001 for i in intercept.normal]

            # Generamos los rayos de refleccion
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectOrig = sumVectors(intercept.point, bias) if outside else subtractVectors(intercept.point, bias)
            reflectIntercept = renderer.glCastRay(reflectOrig, reflect, None ,recursion + 1)

            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

            # Generamos los rayos de refraccion
            if not totalInternalReflection(intercept.normal, intercept.rayDirection, 1.0, self.ior):
                refract = refractVector(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                refractOrig = subtractVectors(intercept.point, bias) if outside else sumVectors(intercept.point, bias)
                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)

                if refractIntercept != None:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, refract)
                    #refractColor = renderer.glEnvMapColor(intercept.point, reflect)

                # USnado las ecuacionde de fresnel, determinamos cuanta refleccion
                # y cuanta refracion agregar al color final
                Kr, Kt = fresnel(intercept.normal, intercept.rayDirection, 1.0, self.ior)

                reflectColor = [i * Kr for i in reflectColor]
                refractColor = [i * Kt for i in refractColor]


        finalColor = [(finalColor[i] * (LightColor[i]+reflectColor[i]+refractColor[i])) for i in range(3)]
        finalColor= [min(1,finalColor[i]) for i in range(3)]

        return finalColor