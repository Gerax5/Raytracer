
import random
import pygame
from pygame.locals import *
from model import Model
from gl import RendererRT
from figures import *
from material import Material
from lights import *


width = 520
height = 520

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rt = RendererRT(screen)


# snow = Material(diffuse=[1.0,1.0,1.0])
snow = Material(diffuse=[1.0, 0.98, 0.98], spec=128, Ks=0.5)
black = Material(diffuse=[0.0, 0.0, 0.0], spec=0, Ks=0.0)
carrot = Material(diffuse=[1.0, 0.55, 0.2], spec=32, Ks=0.1)
eyes = Material(diffuse=[0.9, 0.9, 0.9], spec=256, Ks=0.7)

# brick = Material(diffuse=[1.0,0.2,0.2], spec=128, Ks=0.25)
# grass = Material(diffuse=[0.2,1.0,0.2], spec=64, Ks=0.2)

# rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8))
rt.lights.append(DirectionalLight(direction=[0,0,-1], intensity=0.8))
# rt.lights.append(DirectionalLight(direction=[0.5,-0.5,-1], intensity=0.6, color=[0,0,1]))
#rt.lights.append(AmbientLight())

#Body
rt.scene.append(Sphere(position=[0,-2,-7], radius=1.5, material=snow))
rt.scene.append(Sphere(position=[0,0,-7], radius=1.2, material=snow))
rt.scene.append(Sphere(position=[0,1.8,-7], radius=1, material=snow))
#Buttons
rt.scene.append(Sphere(position=[0,-1.8,-6], radius=0.55, material=black))
rt.scene.append(Sphere(position=[0,-0.7,-6], radius=0.3, material=black))
rt.scene.append(Sphere(position=[0,0.3,-6], radius=0.3, material=black))
#Face
#Smile
rt.scene.append(Sphere(position=[-0.2,1.2,-6], radius=0.09, material=black))
rt.scene.append(Sphere(position=[0.2,1.2,-6], radius=0.09, material=black))
rt.scene.append(Sphere(position=[0.5,1.4,-6], radius=0.09, material=black))
rt.scene.append(Sphere(position=[-0.5,1.4,-6], radius=0.09, material=black))
#Nose
rt.scene.append(Sphere(position=[0,1.6,-6], radius=0.2, material=carrot))
#eyes
#Right
rt.scene.append(Sphere(position=[-0.3,1.9,-6], radius=0.09, material=eyes))
rt.scene.append(Sphere(position=[-0.25,1.6,-5], radius=0.06, material=black))
#Left
rt.scene.append(Sphere(position=[0.3,1.9,-6], radius=0.09, material=eyes))
rt.scene.append(Sphere(position=[0.25,1.6,-5], radius=0.06, material=black))


# rt.scene.append(Sphere(position=[1,1,-3], radius=0.5, material=grass))
# rt.scene.append(Sphere([2,-3,-5], 1))

rt.glRender()
					
isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False


	pygame.display.flip()
	clock.tick(60)

rt.glGenerateFrameBuffer("BMP/snowman5.bmp")
	
pygame.quit()
