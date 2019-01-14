import pygame
from pygame.locals import *
from math import *
import numpy as np
import random

########    Implementation of Angle Based Constraints. Not best functioning    ########


pygame.init()

display_width = 500
display_height = 500

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay.fill(white)

clock = pygame.time.Clock()
crashed = False

play1 = pygame.image.load('/home/rishab/Downloads/player.png')
play1 = pygame.transform.scale(play1,(10,10))

play2 = pygame.image.load('/home/rishab/Downloads/player.png')
play2 = pygame.transform.scale(play2,(10,10))

play3 = pygame.image.load('/home/rishab/Downloads/images.jpeg')
play3 = pygame.transform.scale(play3,(10,10))

p1 = [random.randint(0,500),random.randint(0,500)]
p2 = [random.randint(0,500),random.randint(0,500)]
p3 = [random.randint(0,500),random.randint(0,500)]

num_play=3

def wrap(x):
	while x<-np.pi:
		x+=2*np.pi
	while x>np.pi:
		x-=2*np.pi
	return x

def car(play,x,y):
	gameDisplay.blit(play, (x,y))

def dist(x,y):
	return sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

def ang(x,y):
	angle = np.arctan2((x[1]-y[1]),(x[0]-y[0]))
	if angle<0:
		angle = 2*np.pi+angle
	return (angle)

theta = np.zeros((num_play-1))
velocity = np.zeros((num_play-1,2))
field = np.zeros((num_play-1,2))
min_dist = 20
while not crashed:
	epsilon=0.000001
	points = []
	neigh = []
	velocity=np.zeros((num_play-1,2))
	points.append(p1)
	points.append(p2)
	points.append(p3)
	gameDisplay.fill(white)
	pos = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True

	bottom = p1
	for i in range(1,num_play):
		if points[i][1]<=bottom[1]:
			bottom = points[i]
			pos = i	#to find the point with least y to plot closed figure

	for i in range(0,num_play):
		if i!=pos:
			neigh.append([ang(bottom,points[i]),i])
		else:
			pass	#finding all neighbours to the point and their angles

	neigh.append([0,pos])	#soring angles to form fig
	neigh.sort()
	area=0
	neg=0
	for i in range(num_play):
		if i!=num_play-1:
			#phi.append(ang(points[i],points[num_play-1]))
			area+=points[neigh[i][1]][0]*points[neigh[i+1][1]][1] - points[neigh[i+1][1]][0]*points[neigh[i][1]][1]
			pygame.draw.line(gameDisplay, red, (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i+1][1]][0],points[neigh[i+1][1]][1]), 3)
		else:
			area+=points[neigh[i][1]][0]*points[neigh[0][1]][1] - points[neigh[0][1]][0]*points[neigh[i][1]][1]
			pygame.draw.line(gameDisplay, red, (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[0][1]][0],points[neigh[0][1]][1]), 3)	#plot fig

	#print(neigh)
	print("AREA",area)
	if area<0:
		neg=1
	area = abs(area)/2

	for i in range(num_play-1):
		if dist(points[i],points[num_play-1])<10:
			print("caught")
			crashed=True
			break

	for i in range(num_play-2):
		if dist(neigh[i],neigh[i+1])<20:
			ang1 = ang(neigh[i],neigh[i+1])
			field_x1 = -1/(dist(neigh[i],neigh[i+1]))*cos(ang1)
			field_x2 = -1/(dist(neigh[i],neigh[i+1]))*cos(ang1+np.pi)
			field_y1 = -1/(dist(neigh[i],neigh[i+1]))*sin(ang1)
			field_y2 = -1/(dist(neigh[i],neigh[i+1]))*sin(ang1+np.pi)
			field[i][0]+=field_x1
			field[i][1]+=field_y1
			field[i+1][0]+=field_x2
			field[i+1][1]+=field_y2
		else:
			field[i][0]=0
			field[i][1]=0


	#print(points[neigh[1][1]])

	for i in range(num_play):
		if neigh[i][1] == num_play-1:
			phi=0
			pass
		else:
			a = points[neigh[i][1]][0]-points[num_play-1][0]
			b = points[neigh[i][1]][1]-points[num_play-1][1]
			alpha = ang(points[neigh[i][1]],points[num_play-1])
			if i!=0 and i!=num_play-1:
				beta = ang(points[neigh[i+1][1]],points[neigh[i-1][1]])
				#nu = points[neigh[i+1][1]][1]-points[neigh[i-1][1]][1]
				next = neigh[i+1][1]
				prev = neigh[i-1][1]
			elif i==num_play-1:
				beta = ang(points[neigh[0][1]],points[neigh[i-1][1]])
				#nu = points[neigh[0][1]][1]-points[neigh[i-1][1]][1]
				next = neigh[0][1]
				prev = neigh[i-1][1]
			elif i==0:
				beta = ang(points[neigh[i+1][1]],points[neigh[num_play-1][1]])
				#nu = points[neigh[i+1][1]][1]-points[neigh[num_play-1][1]][1]
				next = neigh[i+1][1]
				prev = neigh[num_play-1][1]
			c = points[next][0]-points[prev][0]
			d = points[next][1]-points[prev][1]
			print("AB",alpha,beta)
			a1 = alpha
			a2 = alpha+np.pi/2
			a3 = alpha+3*np.pi/2
			a4 = alpha+2*np.pi
			b1 = beta+np.pi
			b2 = beta+2*np.pi
			if (b1<a1 and b2>a1) or (a1<b1<a2 and a1<b2<a2) or (b1<a2 and b2>a2):
				phi = (max(a1,b1)+min(a2,b2))/2
				print("1")
			elif (b1<a3 and b2>a3) or (a3<b1<a4 and a3<b2<a4) or (b1<a4 and b2>a4):
				phi = (max(a3,b1)+min(a4,b2))/2
				print("2")
			else:
				print("3")
				phi=0
			print("COS",cos(phi-alpha),dist(points[neigh[i][1]],points[num_play-1]))
			print("SIN",sin(beta-phi))
			print(a1,a2,a3,a4,b1,b2)
			#phi = (max(a1,b1)+min(a2,b2))/2
			print(phi)
			#theta[neigh[i][1]] = phi
			points[neigh[i][1]][0]-=cos(phi)
			points[neigh[i][1]][1]-=sin(phi)

			#print(alpha,beta)
	#print(points)


	#print("FIELD",field)

	field_1=0
	field_2=0
	field_x=0
	field_y=0
	for i in range(num_play-1):
		field_1+= -(1/dist(points[i],points[num_play-1])**2)*cos(ang(points[i],points[num_play-1]))
		field_2+= -(1/dist(points[i],points[num_play-1])**2)*sin(ang(points[i],points[num_play-1]))

	field_1+= -(1/dist([500,points[num_play-1][1]],points[num_play-1])**2)*cos(0) -(1/dist([0,points[num_play-1][1]],points[num_play-1])**2)*cos(np.pi)
	field_2+= -(1/dist([points[num_play-1][0],500],points[num_play-1])**2)*cos(0) -(1/dist([points[num_play-1][0],0],points[num_play-1])**2)*cos(np.pi)
	field_x = field_1/sqrt(field_1**2 + field_2**2)
	field_y = field_2/sqrt(field_1**2 + field_2**2)
	#points[num_play-1][0]+=field_x
	#points[num_play-1][1]+=field_y

	#print("PHI",phi)

	for i in range(num_play-1):
		car(play1,points[i][0],points[i][1])

	car(play3,points[num_play-1][0],points[num_play-1][1])
	pygame.display.update()
	clock.tick(10)

raw_input()
pygame.quit()
quit()
