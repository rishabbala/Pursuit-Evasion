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


#p1 = [309.5508152051168, 154.1065611268555]
#p2 = [8.95395249427385, 29.299957728136317]
#p3 = [277.24118836985724, 93.34868985117679]
#p4 = [102.24169947132748, 340.02964884420123]
#p5 = [476.00984484756555, 62.139974190862084]
#p6 = [17.99996863138275, 194.99207937814862]

p1 = [random.randint(0,display_width),random.randint(0,display_height)]
p2 = [random.randint(0,display_width),random.randint(0,display_height)]
p3 = [random.randint(0,display_width),random.randint(0,display_height)]
p4 = [random.randint(0,display_width),random.randint(0,display_height)]
p5 = [random.randint(0,display_width),random.randint(0,display_height)]
p6 = [random.randint(0,display_width),random.randint(0,display_height)]
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

num_play=6

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
	points.append(p5)
	points.append(p6)
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
		if dist(points[i],points[num_play-1])<15:
			print("caught")
			end = (time.time() - start_time)
			crashed=True
			break


	for i in range(len(obstacle)):
		pygame.draw.circle(gameDisplay, (0,255,0), (int(obstacle[i][0]),int(obstacle[i][1])), int(obstacle[i][2]))


	for i in range(num_play):
		if neigh[i][1] == num_play-1:
			pass
		else:
			if i==1:
				area = (points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i][1]][1]*points[neigh[i+1][1]][0]) + (points[neigh[i+1][1]][0]*points[num_play-1][1]-points[neigh[i+1][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i][1]][1]-points[num_play-1][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i+1][1]])+dist(points[neigh[i+1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])

				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][0]-points[neigh[i+1][1]][0]) + points[neigh[i][1]][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[i+1][1]][0]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[i+1][1]][1]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0]) + points[neigh[i-1][1]][0]*points[neigh[i+1][1]][1] - points[neigh[i-1][1]][1]*points[neigh[i+1][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[num_play-1])
				d = dist(points[neigh[i][1]],points[num_play-1])
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(xc),int(yc)), int(rad) , 2)
				print("REAL",(points[neigh[i][1]][1]-points[num_play-1][1]),(points[neigh[i][1]][0]-points[num_play-1][0]))
				dc = rad

				nu = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][1]-points[neigh[i+1][1]][1]) -2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*bx*(points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2
				nu += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][0]-points[neigh[i+1][1]][0]) -2*by*(points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2)
				nu = nu/dc**2 + (points[neigh[i][1]][1]-points[num_play-1][1])/d**2
				de = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-2*a*2*points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[i+1][1]][1]) -2*bx*(points[neigh[i-1][1]][1]-points[neigh[i+1][1]][1]))/(2*a)**2)
				de += (points[neigh[i][1]][1]+by/(2*a))*(2*a*2*points[neigh[i][1]][0]*(points[neigh[i-1][1]][0]-points[neigh[i+1][1]][0]) +2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*by*(points[neigh[i-1][1]][1]-points[neigh[i+1][1]][1]))/(2*a)**2
				de = de/dc**2 + (points[neigh[i][1]][0]-points[num_play-1][0])/d**2
				if area>0:
					nu = nu + (points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de - (points[neigh[i+1][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				else:
					nu = nu - (points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de + (points[neigh[i+1][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta = atan2(nu,de)
				print("IMG",nu,de)
				print("DIFF",tan(beta),tan(ang(points[neigh[i][1]],[xc,yc])))


			elif i==num_play-1:
				area = (points[neigh[i][1]][0]*points[num_play-1][1]-points[neigh[i][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i-1][1]][1]-points[num_play-1][1]*points[neigh[i-1][1]][0]) + (points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i-1][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i-1][1]])+dist(points[neigh[i-1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])

				print("REAL",(points[neigh[i][1]][1]-points[num_play-1][1]),(points[neigh[i][1]][0]-points[num_play-1][0]))
				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) + points[neigh[i][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[0][1]][0]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][0]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[neigh[0][1]][1]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][1]*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) + points[neigh[i][1]][1]*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]) + points[neigh[i-1][1]][0]*points[neigh[0][1]][1] - points[neigh[i-1][1]][1]*points[neigh[0][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[num_play-1])
				#pygame.draw.circle(gameDisplay, (100,200,50), (int(xc),int(yc)), int(rad) , 2)
				dc = rad
				d = dist(points[neigh[i][1]],points[num_play-1])
				dn = dist(points[neigh[i][1]],points[neigh[0][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])

				nu = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) -2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*bx*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2
				nu += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) -2*by*(points[neigh[0][1]][0]-points[neigh[i-1][1]][0]))/(2*a)**2)
				nu = nu/dc**2 + (points[neigh[i][1]][1]-points[num_play-1][1])/d**2
				de = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-2*a*2*points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]) -2*bx*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]))/(2*a)**2)
				de += (points[neigh[i][1]][1]+by/(2*a))*(2*a*2*points[neigh[i][1]][0]*(points[neigh[i-1][1]][0]-points[neigh[0][1]][0]) +2*a*(points[neigh[0][1]][0]**2+points[neigh[0][1]][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*by*(points[neigh[i-1][1]][1]-points[neigh[0][1]][1]))/(2*a)**2
				de = de/dc**2 + (points[neigh[i][1]][0]-points[num_play-1][0])/d**2
				if area>0:
					nu = nu + (points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de - (points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				else:
					nu = nu - (points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de + (points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta = atan2(nu,de)
				print("IMG",nu,de)
				print("DIFF",tan(beta),tan(ang(points[neigh[i][1]],[xc,yc])))
				#print(beta,"BB")


			else:
				#print("3")
				area = (points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i][1]][1]*points[neigh[i+1][1]][0]) + (points[neigh[i+1][1]][0]*points[num_play-1][1]-points[neigh[i+1][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i][1]][1]-points[num_play-1][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i+1][1]])+dist(points[neigh[i+1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])

				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[num_play-1][0]-points[neigh[i+1][1]][0]) + points[neigh[i][1]][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[num_play-1][0]**2-points[num_play-1][1]**2) + points[neigh[i+1][1]][0]*(points[num_play-1][0]**2+points[num_play-1][1]**2) - points[num_play-1][0]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[num_play-1][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[num_play-1][0]**2-points[num_play-1][1]**2) + points[neigh[i+1][1]][1]*(points[num_play-1][0]**2+points[num_play-1][1]**2) - points[num_play-1][1]*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2))
				a = points[neigh[i][1]][0]*(points[num_play-1][1]-points[neigh[i+1][1]][1]) + points[neigh[i][1]][1]*(points[neigh[i+1][1]][0]-points[num_play-1][0]) + points[num_play-1][0]*points[neigh[i+1][1]][1] - points[num_play-1][1]*points[neigh[i+1][1]][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[num_play-1])
				pygame.draw.circle(gameDisplay, (100,200,50), (int(xc),int(yc)), int(rad) , 2)
				print("REAL",(points[neigh[i][1]][1]-points[num_play-1][1]),(points[neigh[i][1]][0]-points[num_play-1][0]))
				dc = rad
				d = dist(points[neigh[i][1]],points[num_play-1])
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[num_play-1])

				nu = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[num_play-1][1]-points[neigh[i+1][1]][1]) -2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[num_play-1][0]**2-points[num_play-1][1]**2) -2*bx*(points[neigh[i+1][1]][0]-points[num_play-1][0]))/(2*a)**2
				nu += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[num_play-1][0]-points[neigh[i+1][1]][0]) -2*by*(points[neigh[i+1][1]][0]-points[num_play-1][0]))/(2*a)**2)
				nu = nu/dc**2 + (points[neigh[i][1]][1]-points[num_play-1][1])/d**2
				de = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-2*a*2*points[neigh[i][1]][0]*(points[num_play-1][1]-points[neigh[i+1][1]][1]) -2*bx*(points[num_play-1][1]-points[neigh[i+1][1]][1]))/(2*a)**2)
				de += (points[neigh[i][1]][1]+by/(2*a))*(2*a*2*points[neigh[i][1]][0]*(points[num_play-1][0]-points[neigh[i+1][1]][0]) +2*a*(points[neigh[i+1][1]][0]**2+points[neigh[i+1][1]][1]**2-points[num_play-1][0]**2-points[num_play-1][1]**2) -2*by*(points[num_play-1][1]-points[neigh[i+1][1]][1]))/(2*a)**2
				de = de/dc**2 + (points[neigh[i][1]][0]-points[num_play-1][0])/d**2
				if area>0:
					nu = nu + (points[neigh[i+1][1]][0]-points[num_play-1][0])/(2*abs(area))
					de = de - (points[neigh[i+1][1]][1]-points[num_play-1][1])/(2*abs(area))
				else:
					nu = nu - (points[neigh[i+1][1]][0]-points[num_play-1][0])/(2*abs(area))
					de = de + (points[neigh[i+1][1]][1]-points[num_play-1][1])/(2*abs(area))
				beta1 = atan2(nu,de)
				print("IMG",nu,de)
				print("DIFF",tan(beta),tan(ang(points[neigh[i][1]],[xc,yc])))

				area = (points[neigh[i][1]][0]*points[num_play-1][1]-points[neigh[i][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i-1][1]][1]-points[num_play-1][1]*points[neigh[i-1][1]][0]) + (points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i-1][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i-1][1]])+dist(points[neigh[i-1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])

				by = (points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][0]-points[num_play-1][0]) + points[neigh[i][1]][0]*(points[num_play-1][0]**2+points[num_play-1][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[num_play-1][0]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][0]*(points[num_play-1][0]**2+points[num_play-1][1]**2)
				bx = -((points[neigh[i][1]][0]**2+points[neigh[i][1]][1]**2)*(points[neigh[i-1][1]][1]-points[num_play-1][1]) + points[neigh[i][1]][1]*(points[num_play-1][0]**2+points[num_play-1][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) + points[num_play-1][1]*(points[neigh[i-1][1]][0]**2+points[neigh[i-1][1]][1]**2) - points[neigh[i-1][1]][1]*(points[num_play-1][0]**2+points[num_play-1][1]**2))
				a = points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[num_play-1][1]) + points[neigh[i][1]][1]*(points[num_play-1][0]-points[neigh[i-1][1]][0]) + points[neigh[i-1][1]][0]*points[num_play-1][1] - points[neigh[i-1][1]][1]*points[num_play-1][0]
				xc = -bx/(2*a)
				yc = -by/(2*a)
				rad = dist([xc,yc],points[num_play-1])
				pygame.draw.circle(gameDisplay, (100,200,50), (int(xc),int(yc)), int(rad) , 2)
				print("REAL",(points[neigh[i][1]][1]-points[num_play-1][1]),(points[neigh[i][1]][0]-points[num_play-1][0]))
				dc = rad
				d = dist(points[neigh[i][1]],points[num_play-1])
				dn = dist(points[neigh[i][1]],points[num_play-1])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])

				nu = (points[neigh[i][1]][0]+bx/(2*a))*(-2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][1]-points[num_play-1][1]) -2*a*(points[num_play-1][0]**2+points[num_play-1][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*bx*(points[num_play-1][0]-points[neigh[i-1][1]][0]))/(2*a)**2
				nu += (points[neigh[i][1]][1]+by/(2*a))*(1+(2*a*2*points[neigh[i][1]][1]*(points[neigh[i-1][1]][0]-points[num_play-1][0]) -2*by*(points[num_play-1][0]-points[neigh[i-1][1]][0]))/(2*a)**2)
				nu = nu/dc**2 + (points[neigh[i][1]][1]-points[num_play-1][1])/d**2
				de = (points[neigh[i][1]][0]+bx/(2*a))*(1+ (-2*a*2*points[neigh[i][1]][0]*(points[neigh[i-1][1]][1]-points[num_play-1][1]) -2*bx*(points[neigh[i-1][1]][1]-points[num_play-1][1]))/(2*a)**2)
				de += (points[neigh[i][1]][1]+by/(2*a))*(2*a*2*points[neigh[i][1]][0]*(points[neigh[i-1][1]][0]-points[num_play-1][0]) +2*a*(points[num_play-1][0]**2+points[num_play-1][1]**2-points[neigh[i-1][1]][0]**2-points[neigh[i-1][1]][1]**2) -2*by*(points[neigh[i-1][1]][1]-points[num_play-1][1]))/(2*a)**2
				de = de/dc**2 + (points[neigh[i][1]][0]-points[num_play-1][0])/d**2
				if area>0:
					nu = nu + (points[num_play-1][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de - (points[num_play-1][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				else:
					nu = nu - (points[num_play-1][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = de + (points[num_play-1][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta2 = atan2(nu,de)
				print("IMG",nu,de)
				print("DIFF",tan(beta),tan(ang(points[neigh[i][1]],[xc,yc])))
				beta = (beta1+beta2)/2
				if dist([points[neigh[i][1]][0]-50*cos(beta),points[neigh[i][1]][1]-50*sin(beta)],points[num_play-1])>dist([points[neigh[i][1]][0]-50*cos(beta+np.pi),points[neigh[i][1]][1]-50*sin(beta+np.pi)],points[num_play-1]):
					beta = np.pi+beta
			#if abs(ang(points[n[0][1]],points[neigh[i][1]])-ang(points[n[0][1]],points[num_play-1]))<0.1:
			#	beta = ang(points[neigh[i][1]],points[num_play-1])
			#print("BETA",beta)

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

			if abs(neigh[i][0]-neigh[pos][0])<0.2:
				beta = ang(points[neigh[i][1]],points[num_play-1])

			print(neigh[i][1],beta)
			pygame.draw.line(gameDisplay, (255,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(beta),points[neigh[i][1]][1]-50*sin(beta)), 3)
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

with open("5_cir.csv","a") as f: #in write mode
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
