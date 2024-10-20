
import random
import pygame
from pygame.locals import *
from model import Model
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture


from math import cos, sin, pi
from Mathlib import rotationElip

# width = 700
# height = 540

width = 220
height = 220

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

ventana = Material(diffuse=[0.53, 0.81, 0.92])
paint = Material(texture=Texture("texture/wal.bmp"))

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
gold = Material(texture=Texture("texture/gold.bmp"), spec=128, Ks=0.6)
blackMarble = Material(texture=Texture("texture/black.bmp"), spec=200, Ks=0.8)
# dotsGlass = Material(texture=Texture("texture/dots.bmp"), ior=1.5, spec=128, Ks=0.2, matType=TRANSPARENT)
glassPurple = Material(diffuse=[0.36, 0.54, 0.85], ior=1.77, spec=128, Ks=0.2, matType=TRANSPARENT)
# grass = Material(texture=Texture("texture/Grama.bmp"), spec=128, Ks=0.2)
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

# rt.scene.append(AABB(position=[-1,0,-8], sizes=[1,1,1], material=box4))


noRotElip = rotationElip(0,0,0)

# Casa
rt.scene.append(Sphere(position=[0,1,-15], radius=3, material=black)) #2
rt.scene.append(Sphere(position=[-1.7,4,-17], radius=2, material=black)) #0.3
rt.scene.append(Sphere(position=[3,4,-13], radius=2, material=black)) #5
rt.scene.append(Cylinder([0,-2.5,-15], 0.8, 1.1, black)) #2

#Parte de abajo de la casa
rt.scene.append(Hemisphere(position=[0,-5.8,-15], normal=[0,1,0],radius=3.7, material=brick)) # 2, r=4
#Videio
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

# theta_x = pi/4#30 * pi / 180
# theta_y = pi/4
# theta_z = pi/4#30 * pi / 180

# pitch = 0    # Rotación alrededor del eje x
# yaw = 0      # Rotación alrededor del eje y
# roll = 45    # Rotación de 45 grados alrededor del eje z

# rotation_mat = rotationElip(pitch, yaw, roll)


# rt.scene.append(Ellipsoid(position=[0,-0.2,-6],radii=[1, 0.3, 1],rotation_matrix=rotation_mat, material=white))


# rt.scene.append( Disk(position=[0, 4, -8], normal=[0,-1,0], radius=1.5, material=mirror))
# rt.scene.append( Disk(position=[0, 0, -18], normal=[0,0,1], radius=1.5, material=mirror))
# rt.scene.append( Disk(position=[-4, 0, -8], normal=[1,0,0], radius=1, material=mirror))
# rt.scene.append( Disk(position=[4, 0, -8], normal=[-1,0,0], radius=1, material=mirror))

# rt.scene.append(Triangle([0, 0, -5], [1, 0, -5], [0.5, 1, -3], material=glassPurple))
# rt.scene.append(Triangle([-2, 0, -5], [-1, 0, -5], [-1.5, 1, -5], material=glassPurple))
# rt.scene.append(Triangle([2, 1, -5], [3, 1, -5], [1.5, 2, -5], material=glassPurple))

# rt.scene.append(Ellipsoid([0, -2, -7], [1, 0.5, 0.5], material=mirror))
# rt.scene.append(Ellipsoid([-3, -2, -7], [1, 2, 0.5], material=mirror))
# rt.scene.append(Ellipsoid([3, -2, -7], [1, 2, 0.5], material=mirror))

# rt.scene.append(Cylinder([0,2,-5], 0.5, 1, gold))
# rt.scene.append(Cylinder([0.5,-0.5,-5], 0.2, 0.7, gold))
# rt.scene.append(Cylinder([-2,2,-5], 0.1, 0.5, gold))
# rt.scene.append(Torus([0,0,-5], 3, 1, material=brick))

# # rt.scene.append(Sphere(position=[1,0,-5], radius=1, material=blueMirror))
# rt.scene.append(Sphere([-1.5,0,-5], 1, material=brick))
# rt.scene.append(Sphere([1.5,0,-5], 1, material=brick))

rt.lights.append(AmbientLight(intensity = 0.8) )
# rt.lights.append(PointLight(position = [0,0,-3]))
# rt.lights.append(PointLight(position = [0,0,-19]))
# rt.lights.append(SpotLight(position = [2,0,-5], direction = [-1,0,0])) # direction = [-1,0,0]

# rt.scene.append(Plane(position = [0,-5,-5], normal = [0,1,0], material=wood))
# rt.scene.append(Plane(position = [0,7,-5], normal = [0,-1,0], material=techo))
# rt.scene.append(Plane(position = [0,-7,-20], normal = [0,0,1], material=whiteMat))
# rt.scene.append(Plane(position = [8,0,-5], normal = [-1,0,0], material=whiteMat))
# rt.scene.append(Plane(position = [-8,0,-5], normal = [1,0,0], material=whiteMat))

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

rt.glGenerateFrameBuffer("BMP/spheres7.bmp")
pygame.quit()
