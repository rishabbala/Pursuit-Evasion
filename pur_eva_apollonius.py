import pygame
from pygame.locals import *
from math import *
import numpy as np
import random
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from matplotlib import animation
import decimal
from shapely.wkt import loads as load_wkt

pygame.init()

display_width = 1000
display_height = 1000

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay.fill(white)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

play1 = pygame.image.load('/home/rishab/Downloads/player.png')
play1 = pygame.transform.scale(play1,(10,10))

play2 = pygame.image.load('/home/rishab/Downloads/player.png')
play2 = pygame.transform.scale(play2,(10,10))

play3 = pygame.image.load('/home/rishab/Downloads/player.png')
play3 = pygame.transform.scale(play3,(10,10))

play4 = pygame.image.load('/home/rishab/Downloads/player.png')
play4 = pygame.transform.scale(play4,(10,10))

play5 = pygame.image.load('/home/rishab/Downloads/player.png')
play5 = pygame.transform.scale(play5,(10,10))

p1 = [440,199]
p2 = [67,371]
p3 = [186,17]
p4 = [414,437]
p5 = [245,297]
p5_p = p5

phi1=0
phi2=0
phi3=0
phi4=0
phi5=0

w = 0.8 #vel pur/eva
num_pur = 4

crashed = False

def car(x,y):
	gameDisplay.blit(play1, (p1[0],p1[1]))
	gameDisplay.blit(play2, (p2[0],p2[1]))	
	gameDisplay.blit(play3, (p3[0],p3[1]))	
	gameDisplay.blit(play4, (p4[0],p4[1]))	
	gameDisplay.blit(play5, (p5[0],p5[1]))	

def dist(x,y):
	return sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

def ang(x,y):
	angle = np.arctan2((x[1]-y[1]),(x[0]-y[0]))
	if angle<0:
		angle = 2*np.pi+angle
	return (angle)

while not crashed:
	r = []
	rotation = 'u/n'
	c = []
	t = []
	points = []
	phi = []
	points.append(p1)
	points.append(p2)
	points.append(p3)
	points.append(p4)
	points.append(p5)
	gameDisplay.fill(white)


	for i in range (num_pur):
		pygame.draw.circle(gameDisplay, (180,21,146), (int((points[i][0]-points[num_pur][0]*w**2)/(1-w**2)),int((points[i][1]-points[num_pur][1]*w**2)/(1-w**2))), int(w*sqrt((points[i][0]-points[num_pur][0])**2+(points[i][1]-points[num_pur][1])**2)/abs(1-w**2)),2)
		r.append([w*sqrt((points[i][0]-points[num_pur][0])**2+(points[i][1]-points[num_pur][1])**2)/abs(1-w**2),i])
		c.append([int((points[i][0]-points[num_pur][0]*w**2)/(1-w**2)),int((points[i][1]-points[num_pur][1]*w**2)/(1-w**2)),i])
	print("R UNCHANGED",r)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True	 
	for j in range(1,num_pur):
		t.append([ang(points[0],points[j]),j])
	t.sort()
	#print(t)
	l = [[0,0]]
	for i in range(len(t)):
		l.append(t[i])
	print("L",l,len(l))
	for i in range(len(l)):
		for j in range(len(r)):
			if r[j][1] == l[i][1]:
				temp = r[i]
				r[i] = r[j]
				r[j] = temp
				temp = c[i]
				c[i] = c[j]
				c[j] = temp
	print("R",r)
	print("C",c)
			
	if w<1:
		if p5_p == p5:
			for i in range(num_pur):
				tet = ang(points[i],points[num_pur])
				phi.append(tet)
		"""
		else:
			phi1 = ang(p1,[p5[1]-(1/w)*sin(phi5),p5[0]-(1/w)*cos(phi5)])
			phi2 = ang(p2,[p5[1]-(1/w)*sin(phi5),p5[0]-(1/w)*cos(phi5)])
			phi3 = ang(p3,[p5[1]-(1/w)*sin(phi5),p5[0]-(1/w)*cos(phi5)])
			phi4 = ang(p4,[p5[1]-(1/w)*sin(phi5),p5[0]-(1/w)*cos(phi5)])
		"""
		
		print(len(l),"LEN")
		for i in range(len(l)):
			#print(dist([c[i][0],c[i][1]],[c[i+1][0],c[i+1][1]]))
			if i==0:
				if abs(dist([c[i][0],c[i][1]],[c[i+1][0],c[i+1][1]]))>(r[i][0]+r[i+1][0]):
					rotation = 'c'
					print("Case 1")
				elif abs(dist([c[i][0],c[i][1]],[c[num_pur-1][0],c[num_pur-1][1]]))>(r[i][0]+r[num_pur-1][0]):
					rotation = 'cc'
					print("Case 2")
				else:
					rotation = 'u/n'
			elif i==len(l)-1:
				break
			else:
				if abs(dist([c[i][0],c[i][1]],[c[i+1][0],c[i+1][1]]))>(r[i][0]+r[i+1][0])	:
					rotation = 'c'
					print("Case 3")
				else:
					rotation = 'u/n'
					print("case 4")
			print("Rotation for i",rotation)
	for i in range(num_pur):
		pygame.draw.line(gameDisplay, (121,212,84), (points[i][0],points[i][1]), (points[num_pur][0],points[num_pur][1]), 3)
	pygame.draw.rect(gameDisplay, (11,45,98), (0,0,500,500), 15)

	
	p5_p = p5
	print(phi)
	
	for i in range(num_pur):
		points[i][0] = points[i][0]-cos(phi[i])
		points[i][1] = points[i][1]-sin(phi[i])

	for i in range(num_pur+1):
		car(points[i][0],points[i][1])
	#car(p3[0],p3[1])
	pygame.display.update()
	clock.tick(10)
crashed = True
raw_input()
pygame.quit()
quit()
	
