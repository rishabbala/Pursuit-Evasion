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

p1 = [112.53610604299719, 136.84415064453088]
p2 = [69.42804658094389, 164.9037566733044]
p3 = [330.08289875623325, 461.39865437245993]
p4 = [52.7087512043334, 19.70545852490132]
p5 = [217.7464959166333, 430.0326656835838]

#p1 = [random.randint(0,display_width),random.randint(0,display_height)]
#p2 = [random.randint(0,display_width),random.randint(0,display_height)]
#p3 = [random.randint(0,display_width),random.randint(0,display_height)]
#p4 = [random.randint(0,display_width),random.randint(0,display_height)]
#p5 = [random.randint(0,display_width),random.randint(0,display_height)]
#p6 = [random.randint(0,display_width),random.randint(0,display_height)]

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

num_play=5

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
	#points.append(p6)
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
	print("ASAS",n.sort())
	area=0
	peri=0
	neg=0
	for i in range(num_play):
		if i!=num_play-1:
			#peri+=dist(points[neigh[i][1]],points[neigh[i+1][1]])
			#area+=points[neigh[i][1]][0]*points[neigh[i+1][1]][1] - points[neigh[i+1][1]][0]*points[neigh[i][1]][1]
			pygame.draw.line(gameDisplay, black, (points[n[i][1]][0],points[n[i][1]][1]), (points[n[i+1][1]][0],points[n[i+1][1]][1]), 3)
			#peri+=dist(points[n[i][1]],points[n[i+1][1]])
		else:
			#peri+=dist(points[n[i][1]],points[n[0][1]])
			#area+=points[n[i][1]][0]*points[neigh[0][1]][1] - points[neigh[0][1]][0]*points[neigh[i][1]][1]
			pygame.draw.line(gameDisplay, black, (points[n[i][1]][0],points[n[i][1]][1]), (points[n[0][1]][0],points[n[0][1]][1]), 3)	#plot fig
			#peri+=dist(points[n[i][1]],points[n[0][1]])
	#print(neigh)

	for i in range(num_play):
		if n[i][1]==num_play-1:
			pos = i
			print("P",pos)
	neigh.append(n[pos])
	for i in range(pos+1,num_play):
		neigh.append(n[i])
	for i in range(0,pos):
		neigh.append(n[i])
	print("n",n)
	print("NEIGH",neigh)
	#are.append(area)
	#per.append(peri)
	#print("PERI",peri)
	#print("AREA",area)


	for i in range(num_play-1):
		if dist(points[i],points[num_play-1])<15:
			print("caught")
			end = (time.time() - start_time)
			crashed=True
			break


	for i in range(len(obstacle)):
		pygame.draw.circle(gameDisplay, (0,255,0), (int(obstacle[i][0]),int(obstacle[i][1])), int(obstacle[i][2]))



	#print(points[neigh[1][1]])

	for i in range(num_play):

		if neigh[i][1] == num_play-1:
			phi=0
			pass
		else:
			#k = 0.8

			if i==1:
				print("1")
				area = (points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i][1]][1]*points[neigh[i+1][1]][0]) + (points[neigh[i+1][1]][0]*points[num_play-1][1]-points[neigh[i+1][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i][1]][1]-points[num_play-1][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i+1][1]])+dist(points[neigh[i+1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])
				#centx = (points[neigh[i][1]][0]+points[neigh[i+1][1]][0]+points[num_play-1][0])/3
				#centy = (points[neigh[i][1]][1]+points[neigh[i+1][1]][1]+points[num_play-1][1])/3
				print("AREA",area)
				print("PERO",peri)
				#pygame.draw.circle(gameDisplay, (0,255,0), (int(centx),int(centy)), 5)
				#dc = dist([centx,centy],points[num_play-1])
				d = dist(points[neigh[i][1]],points[num_play-1])
				#f = k*d + (1-k)*dc
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				if area>0:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri) + (points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri) - (points[neigh[i+1][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
					print("HERE")
				else:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri) - (points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri) + (points[neigh[i+1][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta = atan2(nu,de)



			elif i==num_play-1:
				print("2")
				area = (points[neigh[i][1]][0]*points[num_play-1][1]-points[neigh[i][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i-1][1]][1]-points[num_play-1][1]*points[neigh[i-1][1]][0]) + (points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i-1][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i-1][1]])+dist(points[neigh[i-1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[i-1][1]][0]+points[num_play-1][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[i-1][1]][1]+points[num_play-1][1])/3
				print("AREA",area)
				print("PERO",peri)
				#pygame.draw.circle(gameDisplay, (0,255,0), (int(centx),int(centy)), 5)
				dc = dist([centx,centy],points[num_play-1])
				d = dist(points[neigh[i][1]],points[num_play-1])
				#f = k*d + (1-k)*dc
				dn = dist(points[neigh[i][1]],points[neigh[0][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				if area>0:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[neigh[0][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri) + (points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[neigh[0][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri) - (points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*abs(area))
					print("HERE")
				else:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[num_play-1][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri) - (points[num_play-1][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[num_play-1][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri) + (points[num_play-1][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta = atan2(nu,de)






			else:
				print("3")
				area = (points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i][1]][1]*points[neigh[i+1][1]][0]) + (points[neigh[i+1][1]][0]*points[num_play-1][1]-points[neigh[i+1][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i][1]][1]-points[num_play-1][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i+1][1]])+dist(points[neigh[i+1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[i+1][1]][0]+points[num_play-1][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[i+1][1]][1]+points[num_play-1][1])/3
				#pygame.draw.circle(gameDisplay, (0,255,0), (int(centx),int(centy)), 5)
				dc = dist([centx,centy],points[num_play-1])
				d = dist(points[neigh[i][1]],points[num_play-1])
				#f = k*d + (1-k)*dc
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[num_play-1])
				if area>0:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[num_play-1][1])/dp)/(peri) + (points[neigh[i+1][1]][0]-points[num_play-1][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[num_play-1][0])/dp)/(peri) - (points[neigh[i+1][1]][1]-points[num_play-1][1])/(2*abs(area))
				else:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[num_play-1][1])/dp)/(peri) - (points[neigh[i+1][1]][0]-points[num_play-1][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[num_play-1][0])/dp)/(peri) + (points[neigh[i+1][1]][1]-points[num_play-1][1])/(2*abs(area))
				beta1 = atan2(nu,de)


				area = (points[neigh[i][1]][0]*points[num_play-1][1]-points[neigh[i][1]][1]*points[num_play-1][0]) + (points[num_play-1][0]*points[neigh[i-1][1]][1]-points[num_play-1][1]*points[neigh[i-1][1]][0]) + (points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i-1][1]][1]*points[neigh[i][1]][0])
				area = area/2
				peri = dist(points[neigh[i][1]],points[neigh[i-1][1]])+dist(points[neigh[i-1][1]],points[num_play-1])+dist(points[num_play-1],points[neigh[i][1]])
				centx = (points[neigh[i][1]][0]+points[neigh[i-1][1]][0]+points[num_play-1][0])/3
				centy = (points[neigh[i][1]][1]+points[neigh[i-1][1]][1]+points[num_play-1][1])/3
				#pygame.draw.circle(gameDisplay, (0,255,0), (int(centx),int(centy)), 5)
				dc = dist([centx,centy],points[num_play-1])
				d = dist(points[neigh[i][1]],points[num_play-1])
				#f = k*d + (1-k)*dc
				dn = dist(points[neigh[i][1]],points[num_play-1])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				if area>0:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[num_play-1][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri) + (points[num_play-1][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[num_play-1][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri) - (points[num_play-1][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				else:
					nu = (points[neigh[i][1]][1]-points[num_play-1][1])/d**2 + ((points[neigh[i][1]][1]-points[num_play-1][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/(peri) - (points[num_play-1][0]-points[neigh[i-1][1]][0])/(2*abs(area))
					de = (points[neigh[i][1]][0]-points[num_play-1][0])/d**2 + ((points[neigh[i][1]][0]-points[num_play-1][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/(peri) + (points[num_play-1][1]-points[neigh[i-1][1]][1])/(2*abs(area))
				beta2 = atan2(nu,de)
				#two triangles
				print("BETAS1,2",beta1,beta2)
				beta = (beta1+beta2)/2
				if dist([points[neigh[i][1]][0]-50*cos(beta),points[neigh[i][1]][1]-50*sin(beta)],points[num_play-1])>dist([points[neigh[i][1]][0]-50*cos(beta+np.pi),points[neigh[i][1]][1]-50*sin(beta+np.pi)],points[num_play-1]):
					beta = np.pi+beta
				#pygame.draw.line(gameDisplay, (0,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(beta1),points[neigh[i][1]][1]-50*sin(beta1)), 3)
				#pygame.draw.line(gameDisplay, (0,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(beta2),points[neigh[i][1]][1]-50*sin(beta2)), 3)
			if abs(ang(points[n[0][1]],points[neigh[i][1]])-ang(points[n[0][1]],points[num_play-1]))<0.1:
				beta = ang(points[neigh[i][1]],points[num_play-1])
			#pygame.draw.line(gameDisplay, (255,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(beta),points[neigh[i][1]][1]-50*sin(beta)), 3)
			print("BETA",beta)
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
			#pygame.draw.line(gameDisplay, (0,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(beta),points[neigh[i][1]][1]-50*sin(beta)), 3)

			ang1 = abs(-(ang(points[num_play-1],points[0]))+(ang(points[num_play-1],points[1])))
			while ang1>np.pi:
				ang1 = ang1-2*np.pi

			flag=0

			"""
			for j in range(len(obstacle)):
				obst_ang = ang([obstacle[j][0],obstacle[j][1]],points[neigh[i][1]])
				obst_ang = wrap(obst_ang)
				if dist(points[neigh[i][1]],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])<2 and dist([points[neigh[i][1]][0]-cos(beta),points[neigh[i][1]][1]-sin(beta)],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])<2:
					c=0
					d=0
					k=0
					flag+=1
					print("Touch")
					if epoch==1 or rotation[i][0] == 0:
						if abs(obst_ang)<np.pi/2:
							print("YES")
							x1 = points[neigh[i][1]][0]-cos((3*np.pi/2)+obst_ang)
							y1 = points[neigh[i][1]][1]-sin((3*np.pi/2)+obst_ang)
							x2 = points[neigh[i][1]][0]-cos((np.pi/2)+obst_ang)
							y2 = points[neigh[i][1]][1]-sin((np.pi/2)+obst_ang)
							if dist([x1,y1],points[num_play-1])<dist([x2,y2],points[num_play-1]):
								c+= -cos(3*np.pi/2+obst_ang)
								d+= -sin(3*np.pi/2+obst_ang)
								rotation[i][0]=1
							else:
								c+= -cos(np.pi/2+obst_ang)
								d+= -sin(np.pi/2+obst_ang)
								rotation[i][0]=2
						else:
							x1 = points[neigh[i][1]][0]-cos((-np.pi/2)+obst_ang)
							y1 = points[neigh[i][1]][1]-sin((-np.pi/2)+obst_ang)
							x2 = points[neigh[i][1]][0]-cos((np.pi/2)+obst_ang)
							y2 = points[neigh[i][1]][1]-sin((np.pi/2)+obst_ang)
							if dist([x1,y1],points[num_play-1])-dist([x2,y2],points[num_play-1])<0:
								c+= -cos(obst_ang-np.pi/2)
								d+= -sin(obst_ang-np.pi/2)
								rotation[i][0]=1
							else:
								c+= -cos(obst_ang+np.pi/2)
								d+= -sin(obst_ang+np.pi/2)
								rotation[i][0]=2
					elif rotation[i][0]==1:
						c+= -cos(obst_ang-np.pi/2)
						d+= -sin(obst_ang-np.pi/2)
					elif rotation[i][0]==2:
						c+= -cos(obst_ang+np.pi/2)
						d+= -sin(obst_ang+np.pi/2)
					rotation[i][1]=neigh[i][1]
					rotation[i][2]=c
					rotation[i][3]=d
					#print(flag,epoch)
			if flag==0 and dist(points[neigh[i][1]],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])>5 and dist([points[neigh[i][1]][0]-cos(beta),points[neigh[i][1]][1]-sin(beta)],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])>5:
				rotation[i][0]=0
				rotation[i][1]=neigh[i][1]
				rotation[i][2]=10
				rotation[i][3]=10

			if rotation[i][0]==1 or rotation[i][0]==2:
				#print("CAC",c,d)
				points[neigh[i][1]][0]+=rotation[i][2]/sqrt(rotation[i][2]**2+rotation[i][3]**2)
				points[neigh[i][1]][1]+=rotation[i][3]/sqrt(rotation[i][2]**2+rotation[i][3]**2)
			else:
				points[neigh[i][1]][0]-=cos(beta)
				points[neigh[i][1]][1]-=sin(beta)

			"""


			points[neigh[i][1]][0]-=cos(beta)
			points[neigh[i][1]][1]-=sin(beta)

			if points[num_play-1] == points[neigh[0][1]]:
				print("TRUE")

			#phi = k*theta2 + (1-k)*theta3



			#if neigh[i][1]==0:
			#	pos1.append([points[neigh[i][1]][0],-points[neigh[i][1]][1]+display_height])
			#if neigh[i][1]==1:
			#	pos2.append([points[neigh[i][1]][0],-points[neigh[i][1]][1]+display_height])
			#if neigh[i][1]==2:
			#	pos3.append([points[neigh[i][1]][0],-points[neigh[i][1]][1]+display_height])
			#if neigh[i][1]==3:
			#	pos4.append([points[neigh[i][1]][0],-points[neigh[i][1]][1]+display_height])


	field_1=0
	field_2=0
	field_x=0
	field_y=0
	for i in range(num_play-1):
		field_1+= -(1/dist(points[i],points[num_play-1])**2)*cos(ang(points[i],points[num_play-1]))
		field_2+= -(1/dist(points[i],points[num_play-1])**2)*sin(ang(points[i],points[num_play-1]))

	for i in range(len(obstacle)):
		obst_ang = ang([obstacle[i][0],obstacle[i][1]],points[num_play-1])
		field_1+= -(1/dist(obstacle[i],points[num_play-1])**2)*cos(obst_ang)
		field_2+= -(1/dist(obstacle[i],points[num_play-1])**2)*sin(obst_ang)

	field_1+= -(1/dist([display_width,points[num_play-1][1]],points[num_play-1])**2)*cos(0) -(1/dist([0,points[num_play-1][1]],points[num_play-1])**2)*cos(np.pi)
	field_2+= -(1/dist([points[num_play-1][0],display_height],points[num_play-1])**2)*cos(0) -(1/dist([points[num_play-1][0],0],points[num_play-1])**2)*cos(np.pi)
	field_x = field_1/sqrt(field_1**2 + field_2**2)
	field_y = field_2/sqrt(field_1**2 + field_2**2)
	points[num_play-1][0]+=field_x
	points[num_play-1][1]+=field_y
	#pos5.append([points[num_play-1][0],-points[num_play-1][1]+display_height])

	#print("PHI",phi)

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

#with open("o6.csv","a") as f: #in write mode
#	writer = csv.writer(f)
#	writer.writerow(row)
#print(pos1)

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
