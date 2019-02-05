import pygame
from pygame.locals import *
from math import *
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib
from matplotlib.legend_handler import HandlerLine2D
import time
import csv

pygame.init()

display_width = 570
display_height = 570

#plt.axis([0, display_width, 0, display_height])

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay.fill(white)

clock = pygame.time.Clock()
crashed = False

play1 = pygame.image.load('/home/rishab/Downloads/player.png')
play1 = pygame.transform.scale(play1,(12,12))

play2 = pygame.image.load('/home/rishab/Downloads/images.png')
play2 = pygame.transform.scale(play2,(12,12))


#p1 = [206.68920211838824, 104.27543085905542]
#p2 = [496.4703735095169, 379.1175325719638]
#p3 = [268.52246762857413, 497.1473408787258]
#p4 = [543.4032461853177, 38.802424379404115]
#p5 = [165.04459640629858, 337.704696811493]
#p6 = [531.0114361949285, 137.15080319394033]

p1 = [random.randint(0,display_width),random.randint(0,display_height)]
p2 = [random.randint(0,display_width),random.randint(0,display_height)]
p3 = [random.randint(0,display_width),random.randint(0,display_height)]
p4 = [random.randint(0,display_width),random.randint(0,display_height)]
#p5 = [random.randint(0,display_width),random.randint(0,display_height)]
#p6 = [random.randint(0,display_width),random.randint(0,display_height)]
#p7 = [random.randint(0,display_width),random.randint(0,display_height)]
#p8 = [random.randint(0,display_width),random.randint(0,display_height)]

#p1 = [129.98191062626807, 25.189344981506917]
#p2 = [188.99861728752686, 175.94743087358057]
#p3 = [170.98845644533068, 31.84849470080486]
#p4 = [384.83889902363086, 101.98693792885516]

#obst = []
obstacle = []
#obstacle.append([80,250,20])
#obst.append([80,display_height-250,10])
#obstacle.append([140,300,20])
#obst.append([140,display_height-300,20])
#obstacle.append([340,50,20])
#obst.append([340,display_height-50,35])
#obstacle.append([340,420,20])
#obst.append([340,display_height-420,20])
#obstacle.append([250,250,20])
#obst.append([310,display_height-220,0])
obstacle.append([70,350,0])

num_play=4

rotation = np.zeros((num_play,4))

def wrap(x):
	while x<0:
		x+=2*np.pi
	while x>2*np.pi:
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

epoch=0
#pos1 = []
#pos2 = []
#pos3 = []
#pos4 = []
#pos5 = []
#are = []
#per = []
#dis = []

#pos1.append(p1)
#pos2.append(p2)
#pos3.append(p3)
#pos4.append(p4)
#pos5.append(p5)

prev = np.zeros(num_play)
start_time = time.time()
while not crashed:
	epoch+=1
	if epoch>3000:
		end = (time.time() - start_time)
		break
	#field = np.zeros((num_play,2))
	epsilon=0.000001
	points = []
	neigh = []
	points.append(p1)
	points.append(p2)
	points.append(p3)
	points.append(p4)
	#points.append(p5)
	#points.append(p6)
	#points.append(p7)
	#points.append(p8)
	gameDisplay.fill(white)
	pos = 0
	centx=0
	centy=0
	n = []

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
			n.append([ang(bottom,points[i]),i])
		else:
			pass	#finding all neighbours to the point and their angles
	temp = []
	min = []
	n.append([0,pos])#soring angles to form fig
	temp = n[num_play-1]
	n[num_play-1] = n[0]
	n[0] = temp
	n.sort()
	#print("ASAS",n.sort())
	area=0
	peri=0
	neg=0
	for i in range(num_play):
		if i!=num_play-1:
			pygame.draw.line(gameDisplay, black, (points[n[i][1]][0],points[n[i][1]][1]), (points[n[i+1][1]][0],points[n[i+1][1]][1]), 3)
		else:
			pygame.draw.line(gameDisplay, black, (points[n[i][1]][0],points[n[i][1]][1]), (points[n[0][1]][0],points[n[0][1]][1]), 3)	#plot fig

	for i in range(num_play):
		if n[i][1]==num_play-1:
			pos = i
			#print("P",pos)
	neigh.append(n[pos])

	for i in range(pos+1,num_play):
		neigh.append(n[i])
	for i in range(0,pos):
		neigh.append(n[i])
	print("n",n)
	print("NEIGH",neigh)

	for i in range(num_play-1):
		if dist(points[i],points[num_play-1])<10:
			print("caught")
			end = (time.time() - start_time)
			crashed=True
			break


	for i in range(len(obstacle)):
		pygame.draw.circle(gameDisplay, (0,255,0), (int(obstacle[i][0]),int(obstacle[i][1])), int(obstacle[i][2]))


	for i in range(num_play):
		max = display_width*display_height
		if neigh[i][1] == num_play-1:
			pass
		else:
			nu1=0
			de1=0
			nu=0
			de=0
			count = 0
			for j in range(num_play):
				if dist(points[neigh[i][1]],points[neigh[j][1]])<max and j!=0 and j!=i:
					max = dist(points[neigh[i][1]],points[neigh[j][1]])
					pos2 = j
			print(i,pos2,"wewe")
			if i==1:
				print("POS",pos2)
				area = (points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i][1]][1]*points[neigh[i+1][1]][0]) + (points[neigh[i+1][1]][0]*points[neigh[0][1]][1]-points[neigh[i+1][1]][1]*points[neigh[0][1]][0]) + (points[neigh[0][1]][0]*points[neigh[i][1]][1]-points[neigh[0][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i+1][1]])+dist(points[neigh[i+1][1]],points[neigh[0][1]])+dist(points[neigh[0][1]],points[neigh[i][1]])
				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[0][1]][0]-points[neigh[i+1][1]][0]) + points[neigh[i][1]][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) + points[neigh[i+1][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2) - points[neigh[0][1]][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) + points[neigh[i+1][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2) - points[neigh[0][1]][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0]) + points[neigh[0][1]][0]*points[neigh[i+1][1]][1] - points[neigh[0][1]][1]*points[neigh[i+1][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[neigh[0][1]])
				d = dist(points[neigh[i][1]],points[neigh[0][1]])
				d2 = dist(points[neigh[i][1]],points[neigh[pos2][1]])
				d3 = dist([centx,centy],points[neigh[i][1]])
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[neigh[0][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[i+1][1]][0]+points[neigh[0][1]][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[i+1][1]][1]+points[neigh[0][1]][1])/3
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(-bx/(2*a)),int(-by/(2*a))), int(rad), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(3), 2)
				#print("REAL",(points[neigh[i][1]][1]-points[neigh[0][1]][1]),(points[neigh[i][1]][0]-points[neigh[0][1]][0]))
				dc = rad

				nu1 = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) -2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) -2*bx*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0]))/((2*a)**2)
				nu1 += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[0][1]][0]-points[neigh[i+1][1]][0]) -2*by*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0]))/((2*a)**2))

				nu = 0*nu1/dc**2 + 0*(points[neigh[i][1]][1]-centy)*2/(3*d3**2) + 0*(points[neigh[i][1]][1]-points[neigh[0][1]][1])/d**2 - 0*(points[neigh[i][1]][1]-points[neigh[pos2][1]][1])/d2**2
				nu += 1*((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[0][1]][1])/dp)/(peri)

				de1 = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-4*a*points[neigh[i][1]][0]*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) -2*bx*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]))/((2*a)**2))
				de1 += (points[neigh[i][1]][1]+by/(2*a))*(4*a*points[neigh[i][1]][0]*(points[neigh[0][1]][0]-points[neigh[i+1][1]][0]) +2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) -2*by*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]))/((2*a)**2)

				de = 0*de1/dc**2 + 0*(points[neigh[i][1]][0]-centx)*2/(3*d3**2) + 0*(points[neigh[i][1]][0]-points[neigh[0][1]][0])/d**2 - 0*(points[neigh[i][1]][0]-points[neigh[pos2][1]][0])/d2**2
				de += 1*((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[0][1]][0])/dp)/(peri)

				if area>0:
					nu = nu + 0*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0])/(2*abs(area))
					de = de - 0*(points[neigh[i+1][1]][1]-points[neigh[0][1]][1])/(2*abs(area))
				else:
					nu = nu - 0*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0])/(2*abs(area))
					de = de + 0*(points[neigh[i+1][1]][1]-points[neigh[0][1]][1])/(2*abs(area))
				beta1 = atan2(nu,de)


				print("POS",pos2)
				area = (points[neigh[i][1]][0]*points[neigh[num_play-1][1]][1]-points[neigh[i][1]][1]*points[neigh[num_play-1][1]][0]) + (points[neigh[num_play-1][1]][0]*points[neigh[0][1]][1]-points[neigh[num_play-1][1]][1]*points[neigh[0][1]][0]) + (points[neigh[0][1]][0]*points[neigh[i][1]][1]-points[neigh[0][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[num_play-1][1]])+dist(points[neigh[num_play-1][1]],points[neigh[0][1]])+dist(points[neigh[0][1]],points[neigh[i][1]])
				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[0][1]][0]-points[neigh[num_play-1][1]][0]) + points[neigh[i][1]][0]*(points[neigh[num_play-1][1]][0]**2+points[neigh[num_play-1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) + points[neigh[num_play-1][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2) - points[neigh[0][1]][0]*(points[neigh[num_play-1][1]][0]**2+points[neigh[num_play-1][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[0][1]][1]-points[neigh[num_play-1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[num_play-1][1]][0]**2+points[neigh[num_play-1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) + points[neigh[num_play-1][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2) - points[neigh[0][1]][1]*(points[neigh[num_play-1][1]][0]**2+points[neigh[num_play-1][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[0][1]][1]-points[neigh[num_play-1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[num_play-1][1]][0]-points[neigh[0][1]][0]) + points[neigh[0][1]][0]*points[neigh[num_play-1][1]][1] - points[neigh[0][1]][1]*points[neigh[num_play-1][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[neigh[0][1]])
				d = dist(points[neigh[i][1]],points[neigh[0][1]])
				d2 = dist(points[neigh[i][1]],points[neigh[pos2][1]])
				d3 = dist([centx,centy],points[neigh[i][1]])
				dn = dist(points[neigh[i][1]],points[neigh[num_play-1][1]])
				dp = dist(points[neigh[i][1]],points[neigh[0][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[num_play-1][1]][0]+points[neigh[0][1]][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[num_play-1][1]][1]+points[neigh[0][1]][1])/3
				pygame.draw.circle(gameDisplay, (100,200,50), (int(-bx/(2*a)),int(-by/(2*a))), int(rad), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(3), 2)
				#print("REAL",(points[neigh[i][1]][1]-points[neigh[0][1]][1]),(points[neigh[i][1]][0]-points[neigh[0][1]][0]))
				dc = rad

				nu1 = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[0][1]][1]-points[neigh[num_play-1][1]][1]) -2*a*(points[neigh[num_play-1][1]][0]**2+points[neigh[num_play-1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) -2*bx*(points[neigh[num_play-1][1]][0]-points[neigh[0][1]][0]))/((2*a)**2)
				nu1 += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[0][1]][0]-points[neigh[num_play-1][1]][0]) -2*by*(points[neigh[num_play-1][1]][0]-points[neigh[0][1]][0]))/((2*a)**2))

				nu = 0*nu1/dc**2 + 0*(points[neigh[i][1]][1]-centy)*2/(3*d3**2) + 0*(points[neigh[i][1]][1]-points[neigh[0][1]][1])/d**2 - 0*(points[neigh[i][1]][1]-points[neigh[pos2][1]][1])/d2**2
				nu += 1*((points[neigh[i][1]][1]-points[neigh[num_play-1][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[0][1]][1])/dp)/(peri)

				de1 = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-4*a*points[neigh[i][1]][0]*(points[neigh[0][1]][1]-points[neigh[num_play-1][1]][1]) -2*bx*(points[neigh[0][1]][1]-points[neigh[num_play-1][1]][1]))/((2*a)**2))
				de1 += (points[neigh[i][1]][1]+by/(2*a))*(4*a*points[neigh[i][1]][0]*(points[neigh[0][1]][0]-points[neigh[num_play-1][1]][0]) +2*a*(points[neigh[num_play-1][1]][0]**2+points[neigh[num_play-1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) -2*by*(points[neigh[0][1]][1]-points[neigh[num_play-1][1]][1]))/((2*a)**2)

				de = 0*de1/dc**2 + 0*(points[neigh[i][1]][0]-centx)*2/(3*d3**2) + 0*(points[neigh[i][1]][0]-points[neigh[0][1]][0])/d**2 - 0*(points[neigh[i][1]][0]-points[neigh[pos2][1]][0])/d2**2
				de += 1*((points[neigh[i][1]][0]-points[neigh[num_play-1][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[0][1]][0])/dp)/(peri)

				if area>0:
					nu = nu + 0*(points[neigh[num_play-1][1]][0]-points[neigh[0][1]][0])/(2*abs(area))
					de = de - 0*(points[neigh[num_play-1][1]][1]-points[neigh[0][1]][1])/(2*abs(area))
				else:
					nu = nu - 0*(points[neigh[num_play-1][1]][0]-points[neigh[0][1]][0])/(2*abs(area))
					de = de + 0*(points[neigh[num_play-1][1]][1]-points[neigh[0][1]][1])/(2*abs(area))
				beta2 = atan2(nu,de)
				beta3 = (beta1+beta2)/2
				beta = (beta3+prev[i])/2
				prev[i] = beta3


				pygame.draw.line(gameDisplay, (0,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(beta),points[neigh[i][1]][1]-50*sin(beta)), 3)

				#print("NUS",nu1,de1,beta)
				#if beta<0:
				#	beta+=2*np.pi
				#if beta>2*np.pi:
				#	beta-=2*np.pi

			elif i==num_play-1:
				area = (points[neigh[i][1]][0]*points[neigh[0][1]][1]-points[neigh[i][1]][1]*points[neigh[0][1]][0]) + (points[neigh[0][1]][0]*points[neigh[i-1][1]][1]-points[neigh[0][1]][1]*points[neigh[i-1][1]][0]) + (points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i-1][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i-1][1]])+dist(points[neigh[i-1][1]],points[neigh[0][1]])+dist(points[neigh[0][1]],points[neigh[i][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[i-1][1]][0]+points[neigh[0][1]][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[i-1][1]][1]+points[neigh[0][1]][1])/3
				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) + points[neigh[i][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[0][1]][0]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[0][1]][1]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]) + points[neigh[i-1][1]][0]*points[neigh[0][1]][1] - points[neigh[i-1][1]][1]*points[neigh[0][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[neigh[0][1]])
				dc = rad
				d = dist(points[neigh[i][1]],points[neigh[0][1]])
				d2 = dist(points[neigh[i][1]],points[neigh[pos2][1]])
				dn = dist(points[neigh[i][1]],points[neigh[0][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				d3 = dist([centx,centy],points[neigh[i][1]])
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(-bx/(2*a)),int(-by/(2*a))), int(rad), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(3), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(5))


				nu1 = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) -2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*bx*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2
				nu1 += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) -2*by*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2)
				#if abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]]))<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])-np.pi)<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])+np.pi)<0.087:
				#	print("MAKING Z")
				#	nu1 = 0
				nu = 0*nu1/dc**2 + 0*(points[neigh[i][1]][1]-centy)*2/(3*d3**2) + 0*(points[neigh[i][1]][1]-points[neigh[0][1]][1])/d**2 - 0*(points[neigh[i][1]][1]-points[neigh[pos2][1]][1])/d2**2
				nu += 1*((points[neigh[i][1]][1]-points[neigh[0][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri)

				de1 = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-4*a*points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) -2*bx*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]))/(2*a)**2)
				de1 += (points[neigh[i][1]][1]+by/(2*a))*(4*a*points[neigh[i][1]][0]*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) +2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*by*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]))/((2*a)**2)
				#if abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]]))<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])-np.pi)<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])+np.pi)<0.087:
				#	de1 = 0
				de = 0*de1/dc**2 + 0*(points[neigh[i][1]][0]-centx)*2/(3*d3**2) + 0*(points[neigh[i][1]][0]-points[neigh[0][1]][0])/d**2 - 0*(points[neigh[i][1]][0]-points[neigh[pos2][1]][0])/d2**2
				de += 1*((points[neigh[i][1]][0]-points[neigh[0][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri)
				if area>0:
					nu = nu + 0*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de - 0*(points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				else:
					nu = nu - 0*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de + 0*(points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta1 = atan2(nu,de)


				area = (points[neigh[i][1]][0]*points[neigh[0][1]][1]-points[neigh[i][1]][1]*points[neigh[0][1]][0]) + (points[neigh[0][1]][0]*points[neigh[1][1]][1]-points[neigh[0][1]][1]*points[neigh[1][1]][0]) + (points[neigh[1][1]][0]*points[neigh[i][1]][1]-points[neigh[1][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[1][1]])+dist(points[neigh[1][1]],points[neigh[0][1]])+dist(points[neigh[0][1]],points[neigh[i][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[1][1]][0]+points[neigh[0][1]][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[1][1]][1]+points[neigh[0][1]][1])/3
				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[1][1]][0]-points[neigh[0][1]][0]) + points[neigh[i][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[1][1]][0]**2-points[neigh[1][1]][1]**2) + points[neigh[0][1]][0]*(points[neigh[1][1]][0]**2+points[neigh[1][1]][1]**2) - points[neigh[1][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[1][1]][0]**2-points[neigh[1][1]][1]**2) + points[neigh[0][1]][1]*(points[neigh[1][1]][0]**2+points[neigh[1][1]][1]**2) - points[neigh[1][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]-points[neigh[1][1]][0]) + points[neigh[1][1]][0]*points[neigh[0][1]][1] - points[neigh[1][1]][1]*points[neigh[0][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[neigh[0][1]])
				dc = rad
				d = dist(points[neigh[i][1]],points[neigh[0][1]])
				d2 = dist(points[neigh[i][1]],points[neigh[pos2][1]])
				dn = dist(points[neigh[i][1]],points[neigh[0][1]])
				dp = dist(points[neigh[i][1]],points[neigh[1][1]])
				d3 = dist([centx,centy],points[neigh[i][1]])
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(-bx/(2*a)),int(-by/(2*a))), int(rad), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(3), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(5))


				nu1 = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[1][1]][1]-points[neigh[0][1]][1]) -2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[1][1]][0]**2-points[neigh[1][1]][1]**2) -2*bx*(points[neigh[0][1]][0]-points[neigh[1][1]][0]))/(2*a)**2
				nu1 += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[1][1]][0]-points[neigh[0][1]][0]) -2*by*(points[neigh[0][1]][0]-points[neigh[1][1]][0]))/(2*a)**2)
				#if abs(ang(points[neigh[i][1]],points[neigh[1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]]))<0.087 or abs(ang(points[neigh[i][1]],points[neigh[1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])-np.pi)<0.087 or abs(ang(points[neigh[i][1]],points[neigh[1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])+np.pi)<0.087:
				#	print("MAKING Z")
				#	nu1 = 0
				nu = 0*nu1/dc**2 + 0*(points[neigh[i][1]][1]-centy)*2/(3*d3**2) + 0*(points[neigh[i][1]][1]-points[neigh[0][1]][1])/d**2 - 0*(points[neigh[i][1]][1]-points[neigh[pos2][1]][1])/d2**2
				nu += 1*((points[neigh[i][1]][1]-points[neigh[0][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[1][1]][1])/dp)/(peri)

				de1 = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-4*a*points[neigh[i][1]][0]*(points[neigh[1][1]][1]-points[neigh[0][1]][1]) -2*bx*(points[neigh[1][1]][1]-points[neigh[0][1]][1]))/(2*a)**2)
				de1 += (points[neigh[i][1]][1]+by/(2*a))*(4*a*points[neigh[i][1]][0]*(points[neigh[1][1]][0]-points[neigh[0][1]][0]) +2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[1][1]][0]**2-points[neigh[1][1]][1]**2) -2*by*(points[neigh[1][1]][1]-points[neigh[0][1]][1]))/((2*a)**2)
				#if abs(ang(points[neigh[i][1]],points[neigh[1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]]))<0.087 or abs(ang(points[neigh[i][1]],points[neigh[1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])-np.pi)<0.087 or abs(ang(points[neigh[i][1]],points[neigh[1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])+np.pi)<0.087:
				#	de1 = 0
				de = 0*de1/dc**2 + 0*(points[neigh[i][1]][0]-centx)*2/(3*d3**2) + 0*(points[neigh[i][1]][0]-points[neigh[0][1]][0])/d**2 - 0*(points[neigh[i][1]][0]-points[neigh[pos2][1]][0])/d2**2
				de += 1*((points[neigh[i][1]][0]-points[neigh[0][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[1][1]][0])/dp)/(peri)
				if area>0:
					nu = nu + 0*(points[neigh[0][1]][0]-points[neigh[1][1]][0])/(2*abs(area))
					de = de - 0*(points[neigh[0][1]][1]-points[neigh[1][1]][1])/(2*abs(area))
				else:
					nu = nu - 0*(points[neigh[0][1]][0]-points[neigh[1][1]][0])/(2*abs(area))
					de = de + 0*(points[neigh[0][1]][1]-points[neigh[1][1]][1])/(2*abs(area))
				beta2 = atan2(nu,de)
				beta3 = beta2
				beta = (beta3+prev[i])/2
				prev[i] = beta3
				#print("NUS",nu1,de1,beta)
				#if beta<0:
				#	beta+=2*np.pi
				#if beta>2*np.pi:
				#	beta-=2*np.pi

			else:
				print("POS",pos2)
				area = (points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i][1]][1]*points[neigh[i+1][1]][0]) + (points[neigh[i+1][1]][0]*points[neigh[0][1]][1]-points[neigh[i+1][1]][1]*points[neigh[0][1]][0]) + (points[neigh[0][1]][0]*points[neigh[i][1]][1]-points[neigh[0][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i+1][1]])+dist(points[neigh[i+1][1]],points[neigh[0][1]])+dist(points[neigh[0][1]],points[neigh[i][1]])
				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[0][1]][0]-points[neigh[i+1][1]][0]) + points[neigh[i][1]][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) + points[neigh[i+1][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2) - points[neigh[0][1]][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) + points[neigh[i+1][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2) - points[neigh[0][1]][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0]) + points[neigh[0][1]][0]*points[neigh[i+1][1]][1] - points[neigh[0][1]][1]*points[neigh[i+1][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[neigh[0][1]])
				d = dist(points[neigh[i][1]],points[neigh[0][1]])
				d2 = dist(points[neigh[i][1]],points[neigh[pos2][1]])
				d3 = dist([centx,centy],points[neigh[i][1]])
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[neigh[0][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[i+1][1]][0]+points[neigh[0][1]][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[i+1][1]][1]+points[neigh[0][1]][1])/3
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(-bx/(2*a)),int(-by/(2*a))), int(rad), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(3), 2)
				#print("REAL",(points[neigh[i][1]][1]-points[neigh[0][1]][1]),(points[neigh[i][1]][0]-points[neigh[0][1]][0]))
				dc = rad

				nu1 = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) -2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) -2*bx*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0]))/((2*a)**2)
				nu1 += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[0][1]][0]-points[neigh[i+1][1]][0]) -2*by*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0]))/((2*a)**2))

				nu = 0*nu1/dc**2 + 0*(points[neigh[i][1]][1]-centy)*2/(3*d3**2) + 0*(points[neigh[i][1]][1]-points[neigh[0][1]][1])/d**2 - 0*(points[neigh[i][1]][1]-points[neigh[pos2][1]][1])/d2**2
				nu += 1*((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[0][1]][1])/dp)/(peri)

				de1 = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-4*a*points[neigh[i][1]][0]*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]) -2*bx*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]))/((2*a)**2))
				de1 += (points[neigh[i][1]][1]+by/(2*a))*(4*a*points[neigh[i][1]][0]*(points[neigh[0][1]][0]-points[neigh[i+1][1]][0]) +2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[0][1]][0]**2-points[neigh[0][1]][1]**2) -2*by*(points[neigh[0][1]][1]-points[neigh[i+1][1]][1]))/((2*a)**2)

				de = 0*de1/dc**2 + 0*(points[neigh[i][1]][0]-centx)*2/(3*d3**2) + 0*(points[neigh[i][1]][0]-points[neigh[0][1]][0])/d**2 - 0*(points[neigh[i][1]][0]-points[neigh[pos2][1]][0])/d2**2
				de += 1*((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[0][1]][0])/dp)/(peri)

				if area>0:
					nu = nu + 0*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0])/(2*abs(area))
					de = de - 0*(points[neigh[i+1][1]][1]-points[neigh[0][1]][1])/(2*abs(area))
				else:
					nu = nu - 0*(points[neigh[i+1][1]][0]-points[neigh[0][1]][0])/(2*abs(area))
					de = de + 0*(points[neigh[i+1][1]][1]-points[neigh[0][1]][1])/(2*abs(area))
				beta1 = atan2(nu,de)


				#if beta1<0:
				#	beta1+=2*np.pi

				area = (points[neigh[i][1]][0]*points[neigh[0][1]][1]-points[neigh[i][1]][1]*points[neigh[0][1]][0]) + (points[neigh[0][1]][0]*points[neigh[i-1][1]][1]-points[neigh[0][1]][1]*points[neigh[i-1][1]][0]) + (points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i-1][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i-1][1]])+dist(points[neigh[i-1][1]],points[neigh[0][1]])+dist(points[neigh[0][1]],points[neigh[i][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[i-1][1]][0]+points[neigh[0][1]][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[i-1][1]][1]+points[neigh[0][1]][1])/3
				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) + points[neigh[i][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[0][1]][0]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[0][1]][1]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]) + points[neigh[i-1][1]][0]*points[neigh[0][1]][1] - points[neigh[i-1][1]][1]*points[neigh[0][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[neigh[0][1]])
				dc = rad
				d = dist(points[neigh[i][1]],points[neigh[0][1]])
				d2 = dist(points[neigh[i][1]],points[neigh[pos2][1]])
				dn = dist(points[neigh[i][1]],points[neigh[0][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				d3 = dist([centx,centy],points[neigh[i][1]])
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(-bx/(2*a)),int(-by/(2*a))), int(rad), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(3), 2)
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(centx),int(centy)), int(5))


				nu1 = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) -2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*bx*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2
				nu1 += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) -2*by*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2)
				#if abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]]))<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])-np.pi)<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])+np.pi)<0.087:
				#	print("MAKING Z")
				#	nu1 = 0
				nu = 0*nu1/dc**2 + 0*(points[neigh[i][1]][1]-centy)*2/(3*d3**2) + 0*(points[neigh[i][1]][1]-points[neigh[0][1]][1])/d**2 - 0*(points[neigh[i][1]][1]-points[neigh[pos2][1]][1])/d2**2
				nu += 1*((points[neigh[i][1]][1]-points[neigh[0][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri)

				de1 = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-4*a*points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) -2*bx*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]))/(2*a)**2)
				de1 += (points[neigh[i][1]][1]+by/(2*a))*(4*a*points[neigh[i][1]][0]*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) +2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*by*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]))/((2*a)**2)
				#if abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]]))<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])-np.pi)<0.087 or abs(ang(points[neigh[i][1]],points[neigh[i-1][1]])-ang(points[neigh[i][1]],points[neigh[0][1]])+np.pi)<0.087:
				#	de1 = 0
				de = 0*de1/dc**2 + 0*(points[neigh[i][1]][0]-centx)*2/(3*d3**2) + 0*(points[neigh[i][1]][0]-points[neigh[0][1]][0])/d**2 - 0*(points[neigh[i][1]][0]-points[neigh[pos2][1]][0])/d2**2
				de += 1*((points[neigh[i][1]][0]-points[neigh[0][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri)
				if area>0:
					nu = nu + 0*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de - 0*(points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				else:
					nu = nu - 0*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de + 0*(points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta2 = atan2(nu,de)
				#if beta2<0:
				#	beta2+=2*np.pi
				#print("BETA2",nu,de)
				beta3 = (beta1+beta2)/2
				beta = (beta3+prev[i])/2
				print("BETA",beta3,prev[i],beta)
				prev[i] = beta3

				#pygame.draw.line(gameDisplay, (255,0,0), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(nu1/de1),points[neigh[i][1]][1]-50*sin(nu1/de1)), 3)


			if (points[neigh[i][1]][0]<=0 and -cos(beta)<0) or (points[neigh[i][1]][0]>=display_width and -cos(beta)>0) :
				if -sin(beta)>0:
					beta = -np.pi/2-epsilon
				else:
					beta = np.pi/2+epsilon
			if  (points[neigh[i][1]][1]<=0 and -sin(beta)<0) or (points[neigh[i][1]][1]>=display_height and -sin(beta)>0):
				if -cos(beta)>0:
					beta = np.pi-epsilon
				else:
					beta = 0+epsilon

			ang1 = abs(-(ang(points[num_play-1],points[0]))+(ang(points[num_play-1],points[1])))
			while ang1>np.pi:
				ang1 = ang1-2*np.pi

			flag=0

			#if abs(neigh[i][0]-neigh[pos][0])<0.087:
			#	beta = ang(points[neigh[i][1]],points[num_play-1])

			print(neigh[i][1],beta)
			#pygame.draw.line(gameDisplay, (255,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(beta),points[neigh[i][1]][1]-50*sin(beta)), 3)

			points[neigh[i][1]][0]-=cos(beta)
			points[neigh[i][1]][1]-=sin(beta)

	field_1=0
	field_2=0
	field_x=0
	field_y=0
	for i in range(num_play-1):
		field_1+= -(1/dist(points[i],points[num_play-1])**2)*cos(ang(points[i],points[num_play-1]))
		field_2+= -(1/dist(points[i],points[num_play-1])**2)*sin(ang(points[i],points[num_play-1]))

	field_1+= -(1/dist([display_width,points[num_play-1][1]],points[num_play-1])**2)*cos(0) -(1/dist([0,points[num_play-1][1]],points[num_play-1])**2)*cos(np.pi)
	field_2+= -(1/dist([points[num_play-1][0],display_height],points[num_play-1])**2)*cos(0) -(1/dist([points[num_play-1][0],0],points[num_play-1])**2)*cos(np.pi)
	field_x = field_1/sqrt(field_1**2 + field_2**2)
	field_y = field_2/sqrt(field_1**2 + field_2**2)
	points[num_play-1][0]+=field_x
	points[num_play-1][1]+=field_y

	for i in range(num_play-1):
		car(play1,points[i][0],points[i][1])

	car(play2,points[num_play-1][0],points[num_play-1][1])
	pygame.display.update()

	clock.tick(20)
	print("POINTS",points)
	print("EPOCH",epoch)
	print("--- %s seconds ---" % (time.time() - start_time))
	#break
row = []
row.append(time.time() - start_time)

with open("3_new-2.csv","a") as f: #in write mode
	writer = csv.writer(f)
	writer.writerow(row)

#print(pos1[0:][0],pos1[0:][1])

"""
a, b = zip(*pos1)
plt.plot(a[1],b[1],'ro')
plt.plot(a[1:],b[1:],'r--',linewidth=2.0)
a, b = zip(*pos2)
plt.plot(a[1],b[1],'ro')
plt.plot(a[1:],b[1:],'r--',linewidth=2.0)
a, b = zip(*pos3)
plt.plot(a[1],b[1],'ro')
plt.plot(a[1:],b[1:],'r--',linewidth=2.0)
a, b = zip(*pos4)
plt.plot(a[1],b[1],'ro')
plt.plot(a[1:],b[1:],'r--',linewidth=2.0)
a, b = zip(*pos5)
plt.plot(a[1],b[1],'bo')
plt.plot(a[1:],b[1:],'b',linewidth=2.0)
line1, = plt.plot([0,0], 'r--', label='Pursuers')
line2, = plt.plot([0,0], 'b', label='Evader')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.xlabel('x Position in px')
plt.ylabel('y Position in px')
a, b, c = zip(*obst)
#plt.Circle((a,b), c, color='g')
 # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

for i in range(len(obst)):
	plt.scatter(a[i],b[i],s=c[i]**2, color='k')
#print(row[0],row[1])
#plt.scatter((500-row[0]),(500-row[1]),c='b')
#print(q[0],r[0])
#plt.scatter(q[0],r[0],c='b')
#plt.scatter(s[0],t[0],c='r')
#plt.scatter(u[0],v[0],c='g')
#plt.plot(q[1:], r[1:])
#plt.plot(s[1:], t[1:])
#plt.plot(u[1:], v[1:])
#plt.plot([pos2[0],pos2[1]])
plt.gca().autoscale_view()
#plt.savefig('[257,220][456,119][458,216],k=%f,epoch=%d.png'%(k,epoch))
plt.show()
plt.plot(are, 'c')
line1, = plt.plot([0,0], 'c', label='Area')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.xlabel('epoch')
plt.ylabel('Area in px^2')
plt.show()

plt.plot(per, 'm')
line2, = plt.plot([0,0], 'm', label='Perimeter')
plt.xlabel('epoch')
plt.ylabel('Peri in px')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.show()

plt.plot(dis[0:len(dis)-1], 'r')
line2, = plt.plot([0,0], 'r', label='Distance of centroid from evader')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
plt.xlabel('epoch')
plt.ylabel('Distance in px')
plt.show()

"""


raw_input()
pygame.quit()
quit()
