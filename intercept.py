

class Intercept(object):
    #point = position
    def __init__(self, point, normal, distance, obj, rayDirection, texCoords):
        self.point = point
        self.normal = normal
        self.distance = distance
        self.texCoords = texCoords
        self.rayDirection = rayDirection
        self.obj = obj