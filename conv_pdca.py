import pygame
from pygame.locals import *
from math import *
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.legend_handler import HandlerLine2D
import time
import csv

pygame.init()

plt.axis([0, 500, 0, 500])

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

play2 = pygame.image.load('/home/rishab/Downloads/images.jpeg')
play2 = pygame.transform.scale(play2,(10,10))


p1 = [211.47418075754817, 208.11957248499888]
p2 = [275.631449850393, 361.22458328207426]
p3 = [274.51256057483147, 306.1413489316792]
p4 = [460.35759239645006, 295.0661222360495]
p5 = [420.6108282192343, 52.92116519965512]



#p1 = [random.randint(0,500),random.randint(0,500)]
#p2 = [random.randint(0,500),random.randint(0,500)]
#p3 = [random.randint(0,500),random.randint(0,500)]
#p4 = [random.randint(0,500),random.randint(0,500)]
#p5 = [random.randint(0,500),random.randint(0,500)]

num_play=5

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
#pos1.append(p1)
#pos2.append(p2)
#pos3.append(p3)

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
	gameDisplay.fill(white)
	pos = 0
	centx=0
	centy=0
	for i in range(num_play):
		centx+=points[i][0]
		centy+=points[i][1]
	centx/=num_play
	centy/=num_play

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
	peri=0
	neg=0
	for i in range(num_play):
		if i!=num_play-1:
			peri+=dist(points[neigh[i][1]],points[neigh[i+1][1]])
			area+=points[neigh[i][1]][0]*points[neigh[i+1][1]][1] - points[neigh[i+1][1]][0]*points[neigh[i][1]][1]
			pygame.draw.line(gameDisplay, red, (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i+1][1]][0],points[neigh[i+1][1]][1]), 3)
			peri+=dist(points[neigh[i][1]],points[neigh[i+1][1]])
		else:
			peri+=dist(points[neigh[i][1]],points[neigh[0][1]])
			area+=points[neigh[i][1]][0]*points[neigh[0][1]][1] - points[neigh[0][1]][0]*points[neigh[i][1]][1]
			pygame.draw.line(gameDisplay, red, (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[0][1]][0],points[neigh[0][1]][1]), 3)	#plot fig
			peri+=dist(points[neigh[i][1]],points[neigh[0][1]])
	#print(neigh)

	print("PERI",peri)
	print("AREA",area)
	if area<0:
		neg=1
	area = abs(area)/2


	centx=0
	centy=0
	for i in range(num_play-1):
		centx+=points[i][0]
		centy+=points[i][1]
		if dist(points[i],points[num_play-1])<20:
			print("caught")
			end = (time.time() - start_time)
			crashed=True
			break
	centx+=points[num_play-1][0]
	centy+=points[num_play-1][1]
	centx/=num_play
	centy/=num_play
	pygame.draw.circle(gameDisplay, (0,0,255), (int(centx),int(centy)), 10)


	#print(points[neigh[1][1]])

	for i in range(num_play):
		if neigh[i][1] == num_play-1:
			phi=0
			pass
		else:



			##################    PERI*(K*DIST+(1-K)*CENT)/AREA ALGORITHM    ################
			k=0.75
			d = dist(points[neigh[i][1]],points[num_play-1])
			dc = dist([centx,centy],points[num_play-1])
			f = k*d + (1-k)*dc
			if i!=0 and i!=num_play-1:
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				nu = (k*(points[neigh[i][1]][1]-points[num_play-1][1])/d + (1-k)*(centy-points[num_play-1][1])/(3*dc))/f + ((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/peri + (points[neigh[i+1][1]][0]-points[neigh[i-1][1]][0])/(2*1.5*area)
				de = (k*(points[neigh[i][1]][0]-points[num_play-1][0])/d + (1-k)*(centx-points[num_play-1][0])/(3*dc))/f + ((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/peri - (points[neigh[i+1][1]][1]-points[neigh[i-1][1]][1])/(2*1.5*area)
				beta = atan2(nu,de)
				#peri2 = peri-dist(points[neigh[i][1]],points[neigh[i+1][1]])-dist(points[neigh[i][1]],points[neigh[i-1][1]])
				next = neigh[i+1][1]
				prev = neigh[i-1][1]
			elif i==num_play-1:
				dn = dist(points[neigh[i][1]],points[neigh[0][1]])
				dp = dist(points[neigh[i][1]],points[neigh[i-1][1]])
				nu = (k*(points[neigh[i][1]][1]-points[num_play-1][1])/d + (1-k)*(centy-points[num_play-1][1])/(3*dc))/f + ((points[neigh[i][1]][1]-points[neigh[0][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[i-1][1]][1])/dp)/peri + (points[neigh[0][1]][0]-points[neigh[i-1][1]][0])/(2*1.5*area)
				de = (k*(points[neigh[i][1]][0]-points[num_play-1][0])/d + (1-k)*(centx-points[num_play-1][0])/(3*dc))/f + ((points[neigh[i][1]][0]-points[neigh[0][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[i-1][1]][0])/dp)/peri - (points[neigh[0][1]][1]-points[neigh[i-1][1]][1])/(2*1.5*area)
				beta = atan2(nu,de)
				#peri2 = peri-dist(points[neigh[i][1]],points[neigh[0][1]])-dist(points[neigh[i][1]],points[neigh[i-1][1]])
				next = neigh[0][1]
				prev = neigh[i-1][1]
			elif i==0:
				dn = dist(points[neigh[i][1]],points[neigh[i+1][1]])
				dp = dist(points[neigh[i][1]],points[neigh[num_play-1][1]])
				nu = (k*(points[neigh[i][1]][1]-points[num_play-1][1])/d + (1-k)*(centy-points[num_play-1][1])/(3*dc))/f + ((points[neigh[i][1]][1]-points[neigh[i+1][1]][1])/dn + (points[neigh[i][1]][1]-points[neigh[num_play-1][1]][1])/dp)/peri + (points[neigh[i+1][1]][0]-points[neigh[num_play-1][1]][0])/(2*1.5*area)
				de = (k*(points[neigh[i][1]][0]-points[num_play-1][0])/d + (1-k)*(centx-points[num_play-1][0])/(3*dc))/f + ((points[neigh[i][1]][0]-points[neigh[i+1][1]][0])/dn + (points[neigh[i][1]][0]-points[neigh[num_play-1][1]][0])/dp)/peri - (points[neigh[i+1][1]][1]-points[neigh[num_play-1][1]][1])/(2*1.5*area)
				beta = atan2(nu,de)
				#peri2 = peri-dist(points[neigh[i][1]],points[neigh[i+1][1]])-dist(points[neigh[i][1]],points[neigh[num_play-1][1]])
				next = neigh[i+1][1]
				prev = neigh[num_play-1][1]

			if beta<0:
				beta = 2*np.pi+beta

			b1 = beta
			b2 = beta+np.pi/2  #peri based


			temp1 = b1*100
			temp2 = b2*100
			min_p = -1
			for j in range (int(temp1),int(temp2)):
				if cos(j/100-beta)>min_p:
					min_p = cos(j/100-beta)
					theta = j/100
			pygame.draw.line(gameDisplay, (0,255,0), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(theta),points[neigh[i][1]][1]-50*sin(theta)), 3)
			print("GREEN=PERI/AREA")




			ang1 = abs(-(ang(points[num_play-1],points[0]))+(ang(points[num_play-1],points[1])))
			while ang1>np.pi:
				ang1 = ang1-2*np.pi


			#phi = k*theta2 + (1-k)*theta3

			phi = ang(points[neigh[i][1]],points[num_play-1])
			points[neigh[i][1]][0]-=cos(theta)
			points[neigh[i][1]][1]-=sin(theta)


			#if neigh[i][1]==0:
			#	pos1.append([points[neigh[i][1]][0],-points[neigh[i][1]][1]+500])
			#if neigh[i][1]==1:
			#	pos2.append([points[neigh[i][1]][0],-points[neigh[i][1]][1]+500])


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
	points[num_play-1][0]+=field_x
	points[num_play-1][1]+=field_y
	#pos3.append([points[num_play-1][0],-points[num_play-1][1]+500])

	#print("PHI",phi)

	for i in range(num_play-1):
		car(play1,points[i][0],points[i][1])

	car(play2,points[num_play-1][0],points[num_play-1][1])
	pygame.display.update()

	clock.tick(25)
	print("POINTS",points)
	print("EPOCH",epoch)
	print("--- %s seconds ---" % (time.time() - start_time))
	#break
#with open("mylist.csv","a") as f:
#	wr = csv.writer(f, dialect='excel')
#	wr.writerow([k,k1,epoch])
raw_input()
#with open("mylist.txt","a+") as f: #in write mode
#	f.writelines(([k,k1,end],"\n"))
#print(pos1)

#print(pos1[0:][0],pos1[0:][1])
pygame.quit()
quit()
