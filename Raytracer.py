
import random
import pygame
from pygame.locals import *
from model import Model
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture
from Mathlib import rotationElip

width = 700
height = 540

# width = 220
# height = 220

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("texture/park.bmp")
# rt.glClearColor(1.0,0.0,0.0)
# rt.glClear()

black = Material(diffuse=[0.1,0.1,0.1], spec=128, Ks=0.25)
brick = Material(diffuse=[1.0,0.2,0.2], spec=128, Ks=0.25)
wood = Material(diffuse=[0.7, 0.5, 0.3], spec=64, Ks=0.1)
grass = Material(diffuse=[0.20, 0.35, 0.15], spec=64, Ks=0.1)
whiteMat = Material(diffuse=[0.9, 0.9, 0.9], spec=32, Ks=0.05)
white = Material(diffuse=[1,1,1])
ama = Material(diffuse=[0.98, 0.86, 0.13])
gray = Material(diffuse=[0.5,0.5,0.5])
ventana = Material(diffuse=[0.53, 0.81, 0.92], spec=128, Ks=0.5, matType=REFLECTIVE)
paint = Material(texture=Texture("texture/wal.bmp"))





# Figura
noRotElip = rotationElip(0,0,0)

# Casa
rt.scene.append(Sphere(position=[0,1,-15], radius=3, material=black)) #2
rt.scene.append(Sphere(position=[-1.7,4,-17], radius=2, material=black)) #0.3
rt.scene.append(Sphere(position=[3,4,-13], radius=2, material=black)) #5
rt.scene.append(Cylinder([0,-2.5,-15], 0.8, 1.1, black)) #2

#Parte de abajo de la casa
rt.scene.append(Hemisphere(position=[0,-5.8,-15], normal=[0,1,0],radius=3.7, material=brick)) # 2, r=4
rt.scene.append(Cylinder2(position=[3,-4.8,-13], radius=0.8, height=1, material=black, rotation_matrix=rotationElip(-45,0,90))) #2

# Zapato
rt.scene.append(Sphere(position=[4.5,-5.2,-12], material=ama, radius=1.5))
rt.scene.append(Ellipsoid(position=[4.5, -3, -12], material=ama, radii=[1.5,2,1.5], rotation_matrix=noRotElip))
rt.scene.append(Cylinder2(position=[5,-5,-11],height=0.5, radius=1.6, material=ama, rotation_matrix=rotationElip(-45,0,90)))
rt.scene.append(Cylinder2(position=[5,-3,-11],height=0.5, radius=1.8, material=ama, rotation_matrix=rotationElip(-45,0,90)))
rt.scene.append(Disk(position=[5,-5.5,-10.5],radius=1.6, normal=[1,0,1], material=gray)) #[5,-4,-11]
rt.scene.append(Disk(position=[5,-5.5,-10.4],radius=1.2, normal=[1,0,1], material=ama)) #[5,-4,-11]

#Vidrio de la casa
rt.scene.append( Disk(position=[-1.3, -3.2, -10], normal=[-1,0,-1], radius=0.7, material=ventana))
rt.scene.append( Disk(position=[0, -3.2, -10], normal=[-0.8,0,-1], radius=0.7, material=ventana))

# Pared de atras con textura
rt.scene.append(AABB(position=[0, -5, -35], sizes=[50,2,2], material=paint))

# #Mano de atras
rt.scene.append(Cylinder([-6,-2,-15], 0.7, 2.3, black))
rt.scene.append(Cylinder([-6,-1,-15], 1, 0.5, white))
rt.scene.append(Ellipsoid(position=[-6,-0.3,-15],radii=[0.8, 1.1, 0.8], rotation_matrix=noRotElip, material=white))
#Dedos de derecha a izquierda
rt.scene.append(Ellipsoid(position=[-4.9,-0.1,-15.3],radii=[0.8, 0.3, 0.9],rotation_matrix=rotationElip(0,0,10), material=white))
rt.scene.append(Ellipsoid(position=[-5.3,1,-15],radii=[0.8, 0.2, 0.7],rotation_matrix=rotationElip(0,0,60), material=white))
rt.scene.append(Ellipsoid(position=[-6.4,1,-14.85],radii=[0.8, 0.2, 0.7],rotation_matrix=rotationElip(0,0,-80), material=white))
rt.scene.append(Ellipsoid(position=[-7,0.2,-14.7],radii=[0.8, 0.2, 0.7],rotation_matrix=rotationElip(0,0,-45), material=white))

#Suelo
rt.scene.append( Disk(position=[0, -6, -25], normal=[0,1,0], radius=20, material=grass))
rt.scene.append( Disk(position=[15, -6, -40], normal=[0,1,0], radius=5, material=wood))


#Luces
rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8))
rt.lights.append(AmbientLight(intensity = 0.5))
rt.lights.append(DirectionalLight(intensity=0.8, direction=[0,0,1]))
rt.lights.append(DirectionalLight(intensity=0.8, direction=[0,-1,-1]))
rt.lights.append(PointLight(position = [0,-5,-10]))
rt.lights.append(PointLight(position = [-3,-5,-15]))
rt.lights.append(PointLight(position = [6,-3,-10]))
rt.lights.append(PointLight(position = [-6,0,-14]))


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

rt.glGenerateFrameBuffer("BMP/spheres8.bmp")
pygame.quit()
