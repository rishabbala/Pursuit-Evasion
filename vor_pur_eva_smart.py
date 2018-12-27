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

p1 = [340,210]
p2 = [320,471]
p3 = [250,407]
l1 = []
L1 = []
phi = []
v = np.ndarray(shape=(2,2))
u = np.ndarray(shape=(2,2))
point = np.zeros(2)
neigh = np.zeros(2)
theta = 0

def car(x,y):
	gameDisplay.blit(play1, (p1[0],p1[1]))
	gameDisplay.blit(play2, (p2[0],p2[1]))
	gameDisplay.blit(play3, (p3[0],p3[1]))


def dist(x,y):
	return sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

def ang(x,y):
	angle = np.arctan2((x[1]-y[1]),(x[0]-y[0]))
	if angle<0:
		angle = 2*np.pi+angle
	return (angle)

pygame.draw.rect(gameDisplay, red, (0,0,500,500), 2)
while not crashed:
	pur_co = []
	cent = []
	ang1 = abs(-(ang(p1,p2))+(ang(p1,p3)))
	ang2 = abs(-(ang(p2,p3))+(ang(p2,p1)))
	ang3 = abs(-(ang(p3,p2))+(ang(p3,p1)))
	while ang1>np.pi:
		ang1 = ang1-2*np.pi
	while ang2>np.pi:
		ang2 = ang2-2*np.pi
	while ang3>np.pi:
		ang3 = ang3-2*np.pi
	print(ang1,ang2,ang3)
	if abs(ang1)>np.pi/2:
		obt = [2,3]
	elif abs(ang2)>np.pi/2:
		obt = [1,3]
	elif abs(ang3)>np.pi/2:
		obt = [1,2]
	else:
		obt = [0,0]
	points = [p1[0],p1[1]]
	print(obt)
	i=0
	gameDisplay.fill(white)
	pygame.draw.line(gameDisplay, red, (p1[0],p1[1]), (p3[0],p3[1]), 3)
	pygame.draw.line(gameDisplay, red, (p2[0],p2[1]), (p3[0],p3[1]), 3)
	pygame.draw.line(gameDisplay, red, (p2[0],p2[1]), (p1[0],p1[1]), 3)
	pygame.draw.circle(gameDisplay, (100,120,160), (250,250), 50)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True
	points = np.vstack((points,p1))
	points = np.vstack((points,p2))
	points = np.vstack((points,p3))
	vor = Voronoi(points)
	vert = vor.vertices
	d1=0
	d2=0
	d3=0
	l1 = []
	L1 = []
	cent = []
	for i in range (len(vert)):

		d1 = dist(p1,vert[i])
		d2 = dist(p2,vert[i])
		d3 = dist(p3,vert[i])
		if (abs(d1-d2))<10 and abs(d1-d3)<10:
			mp = vert[i]
			pos = i
	for j in range(3):
		for k in range(j+1,3):
			mid1 = (points[j+1][0]+points[k+1][0])/2
			mid2 = (points[j+1][1]+points[k+1][1])/2
			theta = ang(mp,[mid1,mid2])
			if theta>0 and theta<np.pi/2:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0])*(0-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1])*(0-mp[1])
				if x_new<0 or x_new>500:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([0,y_new])
					else:
						pygame.draw.line(gameDisplay, black, (0,y_new), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[0,y_new])
						l = dist([0,y_new],[mid1,mid2])
						if k+1 == 3:
							cent.append([0,y_new])
					y_n = y_new+(mp[1]-y_new)/(mp[0]-0) * (500-0)
					x_n = 0+(mp[0]-0)/(mp[1]-y_new) * (500-y_new)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
							L = dist([mp[0],mp[1]],[x_n,500])
							l = dist([x_n,500],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,500])
						else:
							pur_co.append([x_n,500])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
							L = dist([mp[0],mp[1]],[500,y_n])
							l = dist([500,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([500,y_n])
						else:
							pur_co.append([500,y_n])

				else:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([x_new,0])
					else:
						pygame.draw.line(gameDisplay, black, (x_new,0), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[x_new,0])
						l = dist([x_new,0],[mid1,mid2])
						if k+1 == 3:
							cent.append([x_new,0])
					y_n = 0+(mp[1]-0)/(mp[0]-x_new) * (500-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-0) * (500-0)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
							L = dist([mp[0],mp[1]],[x_n,500])
							l = dist([x_n,500],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,500])
						else:
							pur_co.append([x_n,500])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
							L = dist([mp[0],mp[1]],[500,y_n])
							l = dist([500,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([500,y_n])
						else:
							pur_co.append([x_n,500])
			elif theta>np.pi/2 and theta<np.pi:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0])*(500-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1])*(0-mp[1])
				if x_new>0 and x_new<500:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([x_new,0])
					else:
						pygame.draw.line(gameDisplay, black, (x_new,0), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[x_new,0])
						l = dist([x_new,0],[mid1,mid2])
						if k+1 == 3:
							cent.append([x_new,0])
					y_n = 0+(mp[1]-0)/(mp[0]-x_new) * (0-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-0) * (500-0)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
							L = dist([mp[0],mp[1]],[x_n,500])
							l = dist([x_n,500],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,500])
						else:
							pur_co.append([x_n,500])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
							L = dist([mp[0],mp[1]],[0,y_n])
							l = dist([0,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([0,y_n])
						else:
							pur_co.append([0,y_n])
				elif y_new>0 and y_new<500:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([500,y_new])
					else:
						pygame.draw.line(gameDisplay, black, (500,y_new), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[500,y_new])
						l = dist([500,y_new],[mid1,mid2])
						if k+1 == 3:
							cent.append([500,y_new])
					y_n = y_new+(mp[1]-y_new)/(mp[0]-500) * (0-500)
					x_n = 500+(mp[0]-500)/(mp[1]-y_new) * (500-y_new)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
							L = dist([mp[0],mp[1]],[x_n,500])
							l = dist([x_n,500],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,500])
						else:
							pur_co.append([x_n,500])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
							L = dist([mp[0],mp[1]],[0,y_n])
							l = dist([0,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([0,y_n])
						else:
							pur_co.append([0,y_n])
			elif theta>3*np.pi/2 and theta<2*np.pi:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0])*(0-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1])*(500-mp[1])
				if x_new>0 and x_new<500:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([x_new,500])
					else:
						pygame.draw.line(gameDisplay, black, (x_new,500), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[x_new,500])
						l = dist([x_new,500],[mid1,mid2])
						if k+1 == 3:
							cent.append([x_new,500])
					y_n = 500+(mp[1]-500)/(mp[0]-x_new) * (500-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-500) * (0-500)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
							L = dist([mp[0],mp[1]],[x_n,0])
							l = dist([x_n,0],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,0])
						else:
							pur_co.append([x_n,0])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
							L = dist([mp[0],mp[1]],[500,y_n])
							l = dist([500,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([500,y_new])
						else:
							pur_co.append([500,y_n])
				elif y_new>0 and y_new<500:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([0,y_new])
					else:
						pygame.draw.line(gameDisplay, black, (0,y_new), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[0,y_new])
						l = dist([0,y_new],[mid1,mid2])
						if k+1 == 3:
							cent.append([0,y_new])
					y_n = y_new+(mp[1]-y_new)/(mp[0]-0) * (500-0)
					x_n = 0+(mp[0]-0)/(mp[1]-y_new) * (0-y_new)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
							L = dist([mp[0],mp[1]],[x_n,0])
							l = dist([x_n,0],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,0])
						else:
							pur_co.append([x_n,0])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
							L = dist([mp[0],mp[1]],[500,y_n])
							l = dist([500,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([500,y_n])
						else:
							pur_co.append([500,y_n])
			elif theta>np.pi and theta<3*np.pi/2:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0])*(500-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1])*(500-mp[1])
				if x_new<0 or x_new>500:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([500,y_new])
					else:
						pygame.draw.line(gameDisplay, black, (500,y_new), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[500,y_new])
						l = dist([500,y_new],[mid1,mid2])
						if k+1 == 3:
							cent.append([500,y_new])
					y_n = y_new+(mp[1]-y_new)/(mp[0]-500) * (0-500)
					x_n = 500+(mp[0]-500)/(mp[1]-y_new) * (0-y_new)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
							L = dist([mp[0],mp[1]],[x_n,0])
							l = dist([x_n,0],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,0])
						else:
							pur_co.append([x_n,0])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
							L = dist([mp[0],mp[1]],[0,y_n])
							l = dist([0,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([0,y_n])
						else:
							pur_co.append([0,y_n])
				else:
					if j+1 == obt[0] and k+1 == obt[1]:
						pur_co.append([x_new,500])
					else:
						pygame.draw.line(gameDisplay, black, (x_new,500), (mp[0],mp[1]), 3)
						L = dist([mp[0],mp[1]],[x_new,500])
						l = dist([x_new,500],[mid1,mid2])
						if k+1 == 3:
							cent.append([x_new,500])
					y_n = 500+(mp[1]-500)/(mp[0]-x_new) * (0-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-500) * (0-500)
					if x_n>0 and x_n<500:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
							L = dist([mp[0],mp[1]],[x_n,0])
							l = dist([x_n,0],[mid1,mid2])
							if k+1 == 3:
								cent.append([x_n,0])
						else:
							pur_co.append([x_n,0])
					else:
						if j+1 == obt[0] and k+1 == obt[1]:
							pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
							L = dist([mp[0],mp[1]],[0,y_n])
							l = dist([0,y_n],[mid1,mid2])
							if k+1 == 3:
								cent.append([0,y_n])
						else:
							pur_co.append([0,y_n])

			l1.append(l)
			L1.append(L)


	eps1 = dist(p1,p3)
	eps2 = dist(p2,p3)
	if eps1<20 or eps2<20:
		print("caught")
		crashed = True
	phi1 = ang(p1,p3)
	phi2 = ang(p2,p3)
	pang1 = ang(([(points[1][0]+points[3][0])/2,(points[1][1]+points[3][1])/2]),pur_co[1])
	pang2 = ang(([(points[2][0]+points[3][0])/2,(points[2][1]+points[3][1])/2]),pur_co[2])
	pygame.draw.line(gameDisplay, (112,122,81), (p1[0],p1[1]), (p1[0]-100*cos(pang1),p1[1]-100*sin(pang1)), 3)
	pygame.draw.line(gameDisplay, (112,122,81), (p1[0],p1[1]), (p1[0]-100*cos(phi1),p1[1]-100*sin(phi1)), 3)
	pygame.draw.line(gameDisplay, (112,122,81), (p2[0],p2[1]), (p2[0]-100*cos(pang2),p2[1]-100*sin(pang2)), 3)
	pygame.draw.line(gameDisplay, (112,122,81), (p2[0],p2[1]), (p2[0]-100*cos(phi2),p2[1]-100*sin(phi2)), 3)

	v[0][0] = -(L1[1])/2
	v[0][1] = (l1[1]**2-(L1[1]-l1[1])**2)/(2*(eps1))
	v[1][0] = -(L1[2])/2
	v[1][1] = (l1[2]**2-(L1[2]-l1[2])**2)/(2*(eps2))
	abs1 = sqrt(v[0][0]**2+v[0][1]**2)
	abs2 = sqrt(v[1][0]**2+v[1][1]**2)
	v[0] /= -abs1
	v[1] /= -abs2


	u[0][0] = -v[0][0]*cos(phi1) - v[0][1]*cos(pang1)
	u[0][1] = -v[0][0]*sin(phi1) - v[0][1]*sin(pang1)
	u[1][0] = -v[1][0]*cos(phi2) - v[1][1]*cos(pang2)
	u[1][1] = -v[1][0]*sin(phi2) - v[1][1]*sin(pang2)


	if (cent[0][0]==500 and cent[1][1]==500) or (cent[1][0]==500 and cent[0][1]==500):
		cent.append([500,500])
	elif (cent[0][0]==0 and cent[1][1]==500) or (cent[1][0]==0 and cent[0][1]==500):
		cent.append([0,500])
	elif (cent[0][0]==0 and cent[1][1]==0) or (cent[1][0]==0 and cent[0][1]==0):
		cent.append([0,0])
	elif (cent[0][0]==500 and cent[1][1]==0) or (cent[1][0]==500 and cent[0][1]==0):
		cent.append([500,0])

	elif (((cent[0][0]==500 and cent[1][0]==0) or (cent[1][0]==500 and cent[0][0]==0)) and ((mp[0]-cent[0][0])*(cent[1][1]-cent[0][1])-(mp[1]-cent[0][1])*(cent[1][0]-cent[0][0]))>0):
		cent.append([0,500])
		cent.append([500,500])

	elif (((cent[0][0]==500 and cent[1][0]==0) or (cent[1][0]==500 and cent[0][0]==0)) and ((mp[0]-cent[0][0])*(cent[1][1]-cent[0][1])-(mp[1]-cent[0][1])*(cent[1][0]-cent[0][0]))<0):
		cent.append([0,0])
		cent.append([500,0])

	elif (((cent[0][1]==500 and cent[1][1]==0) or (cent[1][1]==500 and cent[0][1]==0)) and ((mp[0]-cent[0][0])*(cent[1][1]-cent[0][1])-(mp[1]-cent[0][1])*(cent[1][0]-cent[0][0]))<0):
		cent.append([500,0])
		cent.append([500,500])
	elif (((cent[0][1]==500 and cent[1][1]==0) or (cent[1][1]==500 and cent[0][1]==0)) and ((mp[0]-cent[0][0])*(cent[1][1]-cent[0][1])-(mp[1]-cent[0][1])*(cent[1][0]-cent[0][0]))>0):
		cent.append([0,0])
		cent.append([0,500])


	cent.append([mp[0],mp[1]])
	centroid = [0,0]
	for t in range (len(cent)):
		centroid[0]+=cent[t][0]
		centroid[1]+=cent[t][1]
	centroid[0] /= len(cent)
	centroid[1] /= len(cent)
	pygame.draw.circle(gameDisplay, (85,221,126), (int(centroid[0]),int(centroid[1])), 10)


	for i in range(2):
		obst_ang = ang([250,250],points[i+1])
		if dist(points[i+1],[250-50*cos(obst_ang),250-50*sin(obst_ang)])<2 and dist([points[i+1][0]+u[i][0],points[i+1][1]+u[i][1]],[250-50*cos(obst_ang),250-50*sin(obst_ang)])<2:
			if obst_ang<np.pi/2:
				x = points[i+1][0]-cos(3*np.pi/2+obst_ang)
				y = points[i+1][1]-sin(3*np.pi/2+obst_ang)
				if dist([x,y],p3)-dist(points[i+1],p3)>=0:
					points[i+1][0] = points[i+1][0]-cos(3*np.pi/2+obst_ang)
					points[i+1][1] = points[i+1][1]-sin(3*np.pi/2+obst_ang)
				elif dist([x,y],p3)-dist(points[i+1],p3)<0:
					points[i+1][0] = points[i+1][0]-cos(np.pi/2+obst_ang)
					points[i+1][1] = points[i+1][1]-sin(np.pi/2+obst_ang)
			else:
				x = points[i+1][0]-cos(obst_ang-np.pi/2)
				y = points[i+1][1]-sin(obst_ang-np.pi/2)
				if dist([x,y],p3)-dist(points[i+1],p1)>0:
					points[i+1][0] = points[i+1][0]-cos(-np.pi/2+obst_ang)
					points[i+1][1] = points[i+1][1]-sin(-np.pi/2+obst_ang)
				elif dist([x,y],p3)-dist(points[i+1],p3)<0:
					points[i+1][0] = p3[0]-cos(obst_ang+np.pi/2)
					points[i+1][1] = p3[1]-sin(obst_ang+np.pi/2)
		else:
			points[i+1][0]+=u[i][0]
			points[i+1][1]+=u[i][1]
	p1 = points[1]
	p2 = points[2]


	field_1 = -(1/eps1**2)*cos(phi1) -(1/eps2**2)*cos(phi2)
	field_2 = -(1/eps1**2)*sin(phi1) -(1/eps2**2)*sin(phi2)
	field_x = field_1/sqrt(field_1**2 + field_2**2)
	field_y = field_2/sqrt(field_1**2 + field_2**2)

	field_ang = ang([250,250],p3)
	cen_ang = ang(p3,centroid)
	p3_new = p3
	m = (centroid[1]-p3[1])/(centroid[0]-p3[0])

	print("p3",p3)
	if p3[0] <= 0 and field_x<0:
		field_x = 0
		if field_y<0:
			field_y=-1
		else:
			field_y=1
	elif p3[0] >= 500 and field_x>0:
		field_x = 0
		if field_y<0:
			field_y=-1
		else:
			field_y=1
	if p3[1] <= 0 and field_y<0:
		field_y=0
		if field_x<0:
			field_x=-1
		else:
			field_x=1
	elif p3[1] >= 500 and field_y>0:
		field_y=0
		if field_x<0:
			field_x=-1
		else:
			field_x=1
	print("field",field_x,field_y)
	p3[0]+=field_x
	p3[1]+=field_y
	"""
	if ((centroid[0]-250)**2+(centroid[1]-250)**2)<50**2 or (abs((m*250-250+p3[1]-m*p3[0])/sqrt(m*m+1))< 50 and (dist(p3,centroid)>dist([250-50*cos(field_ang),250-50*cos(field_ang)],p3) and dist(p3,centroid)>dist([250,250],centroid))) and dist(p3,[250-50*cos(field_ang),250-50*sin(field_ang)])<2:
		if field_ang<np.pi/2:
			p3_new[0] = p3_new[0]-cos(3*np.pi/2+field_ang)
			p3_new[1] = p3_new[1]-sin(3*np.pi/2+field_ang)
			if dist(p3,p1)<dist(p3,p2):
				if dist(p3_new,p1)-dist(p3,p1)>0:
					p3[0] = p3[0]-cos(3*np.pi/2+field_ang)
					p3[1] = p3[1]-sin(3*np.pi/2+field_ang)
				elif dist(p3_new,p1)-dist(p3,p1)<0:
					p3[0] = p3[0]-cos(np.pi/2+field_ang)
					p3[1] = p3[1]-sin(np.pi/2+field_ang)
			elif dist(p3,p2)<dist(p3,p1):
				if dist(p3_new,p2)-dist(p3,p2)>0:
					p3 = p3_new
				elif dist(p3_new,p1)-dist(p3,p1)<0:
					p3[0] = p3[0]-cos(field_ang+np.pi/2)
					p3[1] = p3[1]-sin(field_ang+np.pi/2)
			else:
				print("DEQ")
		else:
			p3_new[0] = p3[0]-cos(field_ang-np.pi/2)
			p3_new[1] = p3[1]-sin(field_ang-np.pi/2)
			if dist(p3,p1)<dist(p3,p2):
				if dist(p3_new,p1)-dist(p3,p1)>0:
					p3[0] = p3[0]-cos(-np.pi/2+field_ang)
					p3[1] = p3[1]-sin(-np.pi/2+field_ang)
				else:
					p3[0] = p3[0]-cos(field_ang+np.pi/2)
					p3[1] = p3[1]-sin(field_ang+np.pi/2)

			elif dist(p3,p2)<dist(p3,p1):
				if dist(p3_new,p2)-dist(p3,p2)>0:
					p3[0] = p3[0]-cos(-np.pi/2+field_ang)
					p3[1] = p3[1]-sin(-np.pi/2+field_ang)
				elif dist(p3_new,p1)-dist(p3,p1)<0:
					p3[0] = p3[0]-cos(field_ang+np.pi/2)
					p3[1] = p3[1]-sin(field_ang+np.pi/2)
			else:
				print("DEQ")
	else:
		p3[0] = p3[0]-cos(cen_ang)
		p3[1] = p3[1]-sin(cen_ang)
	"""


	print("V",v)
	print("U",u)
	for t in range (len(cent)):
		pygame.draw.circle(gameDisplay, (180,21,146), (int(cent[t][0]),int(cent[t][1])), 20)


	#p3[0] = p3[0]-cos(cen_ang)
	#p3[1] = p3[1]-sin(cen_ang)
	#pygame.draw.rect(gameDisplay, (121,212,98), (0,0,500,500), 15)
	car(p1[0],p1[1])
	car(p2[0],p2[1])
	car(p3[0],p3[1])
	pygame.display.update()
	clock.tick(15)
	#crashed = True
raw_input()
pygame.quit()
quit()
