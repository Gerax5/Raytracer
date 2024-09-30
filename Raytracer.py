
import random
import pygame
from pygame.locals import *
from model import Model
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture


width = 700
height = 540

# width = 220
# height = 220

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("texture/room.bmp")
# rt.glClearColor(1.0,0.0,0.0)
# rt.glClear()

brick = Material(diffuse=[1.0,0.2,0.2], spec=128, Ks=0.25)
wood = Material(diffuse=[0.7, 0.5, 0.3], spec=64, Ks=0.1)
whiteMat = Material(diffuse=[0.9, 0.9, 0.9], spec=32, Ks=0.05)
techo = Material(diffuse=[0.95, 0.95, 0.95], spec=16, Ks=0.02)
# grass = Material(diffuse=[0.2,1.0,0.2], spec=64, Ks=0.2)
mirror = Material(diffuse=[0.54, 0.17, 0.89], spec=128, Ks=0.2, matType=REFLECTIVE)
# texture=Texture("texture/dots.bmp"),
# blueMirror = Material(diffuse=[0.5,0.5,1.0], spec=128, Ks=0.2, matType=REFLECTIVE)
# glass = Material(ior=1.5, spec=128, Ks=0.2, matType=TRANSPARENT)
box = Material(texture=Texture("texture/woodenBox.bmp"))
box2 = Material(texture=Texture("texture/tex1.bmp"))
box3 = Material(texture=Texture("texture/tex2.bmp"))
box4 = Material(texture=Texture("texture/concrete.bmp"))
box5 = Material(texture=Texture("texture/Grama.bmp"))

# earth = Material(texture=Texture("texture/gold.bmp"))
# gold = Material(texture=Texture("texture/gold.bmp"), spec=128, Ks=0.6, matType=REFLECTIVE)
# blackMarble = Material(texture=Texture("texture/black.bmp"), spec=200, Ks=0.8, matType=REFLECTIVE)
# dotsGlass = Material(texture=Texture("texture/dots.bmp"), ior=1.5, spec=128, Ks=0.2, matType=TRANSPARENT)
# glassPurple = Material(diffuse=[0.54, 0.17, 0.89], ior=1.77, spec=128, Ks=0.2, matType=TRANSPARENT)
grass = Material(texture=Texture("texture/Grama.bmp"), spec=128, Ks=0.2)
# voltorb = Material(texture=Texture("texture/voltorb.bmp"), spec=128)


rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8))
# # rt.lights.append(DirectionalLight(direction=[0.5,-0.5,-1], intensity=0.8, color=[1,1,1]))
# rt.lights.append(AmbientLight(intensity=0.1))

# Arriba
# rt.scene.append(Sphere(position=[-5,2,-10], radius=1.5, material=voltorb))
# rt.scene.append(Sphere(position=[0,2,-10], radius=1.5, material=gold))
# rt.scene.append(Sphere(position=[5,2,-10], radius=1.5, material=dotsGlass))

#Abajo
# rt.scene.append(Sphere(position=[-5,-2,-10], radius=1.5, material=grass))
# rt.scene.append(Sphere(position=[0,-2,-10], radius=1.5, material=blackMarble))
# rt.scene.append(Sphere(position=[5,-2,-10], radius=1.5, material=glassPurple))

# rt.scene.append(Plane(position=[0,-5,-5],  normal=[0,1,0], material=brick))
# rt.scene.append(Sphere(position=[0,0,-5], radius=1.5, material=glass))

# rt.lights.append(PointLight( position=[0,0,-5], intensity=1))

rt.scene.append(AABB(position=[-1,0,-8], sizes=[1,1,1], material=box4))
rt.scene.append(AABB(position=[1,0,-8], sizes=[1,1,1], material=box3))

rt.scene.append( Disk(position=[0, -4, -8], normal=[0,1,0], radius=1.5, material=mirror))
rt.scene.append( Disk(position=[0, 4, -8], normal=[0,-1,0], radius=1.5, material=mirror))
rt.scene.append( Disk(position=[0, 0, -18], normal=[0,0,1], radius=1.5, material=mirror))
rt.scene.append( Disk(position=[-4, 0, -8], normal=[1,0,0], radius=1, material=mirror))
rt.scene.append( Disk(position=[4, 0, -8], normal=[-1,0,0], radius=1, material=mirror))

# # rt.scene.append(Sphere(position=[1,0,-5], radius=1, material=blueMirror))
# rt.scene.append(Sphere([-1.5,0,-5], 1, material=brick))
# rt.scene.append(Sphere([1.5,0,-5], 1, material=brick))

rt.lights.append(AmbientLight(intensity = 0.3) )
rt.lights.append(PointLight(position = [0,0,-3]))
# rt.lights.append(PointLight(position = [0,0,-19]))
# rt.lights.append(SpotLight(position = [2,0,-5], direction = [-1,0,0])) # direction = [-1,0,0] 

rt.scene.append(Plane(position = [0,-5,-5], normal = [0,1,0], material=wood))
rt.scene.append(Plane(position = [0,7,-5], normal = [0,-1,0], material=techo))
rt.scene.append(Plane(position = [0,-7,-20], normal = [0,0,1], material=whiteMat))
rt.scene.append(Plane(position = [8,0,-5], normal = [-1,0,0], material=whiteMat))
rt.scene.append(Plane(position = [-8,0,-5], normal = [1,0,0], material=whiteMat))

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
	
rt.glGenerateFrameBuffer("BMP/spheres6.bmp")
pygame.quit()
