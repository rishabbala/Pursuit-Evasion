import pygame
from pygame.locals import *
from math import *
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.legend_handler import HandlerLine2D

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

play2 = pygame.image.load('/home/rishab/Downloads/player.png')
play2 = pygame.transform.scale(play2,(10,10))

play3 = pygame.image.load('/home/rishab/Downloads/images.jpeg')
play3 = pygame.transform.scale(play3,(10,10))

#p1 = [144.8976083281567, 408.06829865778843]
#p2 = [168.06261927627483, 412.2115054826292]
#p3 = [118.62178891662386, 186.4257844552803]

p1 = [random.randint(0,500),random.randint(0,500)]
p2 = [random.randint(0,500),random.randint(0,500)]
p3 = [random.randint(0,500),random.randint(0,500)]

num_play=3

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
pos1 = []
pos2 = []
pos3=[]
pos1.append(p1)
pos2.append(p2)
pos3.append(p3)
while not crashed:
	epoch+=1
	if epoch>3000:
		break
	field = np.zeros((num_play,2))
	epsilon=0.000001
	points = []
	neigh = []
	n = []
	points.append(p1)
	points.append(p2)
	points.append(p3)
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
	#print("AREA",area)
	print("PERI",peri)
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
			crashed=True
			break
	centx+=points[num_play-1][0]
	centy+=points[num_play-1][1]
	centx/=num_play
	centy/=num_play
	pygame.draw.circle(gameDisplay, (0,0,255), (int(centx),int(centy)), 10)



############################################################################

	#print(points[neigh[1][1]])

	for i in range(num_play):
		if neigh[i][1] == num_play-1:
			phi=0
			pass
		else:
			p = []
			p.append(points[num_play-1])
			p.append(points[neigh[i][1]])
			p.append([centx,centy])
			#p.append(p3)
			print(p)
			bot = p[0]
			pos=0
			for j in range(1,len(p)):
				if p[j][1]<=bot[1]:
					bot = p[j]
					pos = j

			for j in range(0,len(p)):
				if j!=pos:
					n.append([ang(bot,p[j]),j])
				else:
					pass	#finding all neighbours to the point and their angles

			n.append([0,pos])	#soring angles to form fig
			n.sort()

			areac=0
			peric=0
			for j in range(len(p)):
				if j!=len(p)-1:
					peric+=dist(p[n[j][1]],p[n[j+1][1]])
					areac+=p[n[j][1]][0]*p[n[j+1][1]][1] - p[n[j+1][1]][0]*p[n[j][1]][1]
					#pygame.draw.line(gameDisplay, (0,0,255), (p[n[i][1]][0],p[n[i][1]][1]), (p[n[i+1][1]][0],p[n[i+1][1]][1]), 3)
				else:
					peric+=dist(p[n[j][1]],p[n[0][1]])
					areac+=p[n[j][1]][0]*p[n[0][1]][1] - p[n[0][1]][0]*p[n[j][1]][1]
			print(n)


			#### perimeter algorithm ####
			for j in range(len(p)):
				if p[n[j][1]]!=[centx,centy] and p[n[j][1]]!=points[num_play-1]:
					num = j


			if num!=0 and num!=len(p)-1:
				#print(p[n[num][1]],p[n[num+1][1]],p[n[num-1][1]])
				#d = dist(p[n[num][1]],p[n[num+1][1]])/dist(p[n[num][1]],p[n[num-1][1]])
				ang2 = (ang(p[n[num][1]],points[n[num+1][1]])-ang(points[n[num][1]],points[n[num-1][1]]))
				beta = atan2((p[n[num][1]][1]-p[n[num+1][1]][1]-2*p[n[num-1][1]][1]),(p[n[num][1]][0]-p[n[num+1][1]][0]-2*p[n[num-1][1]][0]))
				peri2 = peric-dist(p[n[num][1]],p[n[num+1][1]])-dist(p[n[num][1]],p[n[num-1][1]])
				next = n[num+1][1]
				prev = n[num-1][1]
			elif num==len(p)-1:
				d = dist(p[n[num][1]],p[n[0][1]])/dist(p[n[num][1]],p[n[num-1][1]])
				ang2 = (ang(p[n[num][1]],points[n[0][1]])-ang(points[n[num][1]],points[n[num-1][1]]))
				beta = atan2((p[n[num][1]][1]-p[n[0][1]][1]-2*p[n[num-1][1]][1]),(p[n[num][1]][0]-p[n[0][1]][0]-2*p[n[num-1][1]][0]))
				peri2 = peric-dist(p[n[num][1]],p[n[0][1]])-dist(p[n[num][1]],p[n[num-1][1]])
				next = n[0][1]
				prev = n[num-1][1]
			elif i==0:
				d = dist(p[n[num][1]],p[n[num+1][1]])/dist(p[n[num][1]],p[n[len(p)-1][1]])
				ang2 = (ang(p[n[num][1]],points[n[num+1][1]])-ang(points[n[num][1]],points[n[len(p)-1][1]]))
				beta = atan2((p[n[num][1]][1]-p[n[num+1][1]][1]-2*p[n[len(p)-1][1]][1]),(p[n[num][1]][0]-p[n[num+1][1]][0]-2*p[n[len(p)-1][1]][0]))
				peri2 = peric-dist(p[n[num][1]],p[n[num+1][1]])-dist(p[n[num][1]],p[n[len(p)-1][1]])
				next = neigh[num+1][1]
				prev = neigh[len(p)-1][1]

			if beta<0:
				beta = 2*np.pi+beta

			b1 = beta
			b2 = beta+np.pi/2  #peri based


			temp1 = b1*100
			temp2 = b2*100
			min_p = peric

			for j in range (int(temp1),int(temp2)):
				pointx = p[n[num][1]][0]-cos(j)
				pointy = p[n[num][1]][1]-sin(j)
				if num!=0 and num!=num_play-1:
					peri3 = peri2+dist([pointx,pointy],p[n[num+1][1]])+dist([pointx,pointy],p[n[num-1][1]])
				elif num==0:
					peri3 = peri2+dist([pointx,pointy],p[n[num+1][1]])+dist([pointx,pointy],p[n[len(p)-1][1]])
				elif num==len(p)-1:
					peri3 = peri2+dist([pointx,pointy],p[n[0][1]])+dist([pointx,pointy],p[n[num-1][1]])
				if peri3<min_p:
					min_p = peri3
					theta=j/100
			pygame.draw.line(gameDisplay, (0,0,0), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(theta),points[neigh[i][1]][1]-50*sin(theta)), 3)

			points[neigh[i][1]][0]-=cos(theta)
			points[neigh[i][1]][1]-=sin(theta)

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
	pos3.append([points[num_play-1][0],-points[num_play-1][1]+500])

	#print("PHI",phi)

	for i in range(num_play-1):
		car(play1,points[i][0],points[i][1])

	car(play3,points[num_play-1][0],points[num_play-1][1])
	pygame.display.update()
	clock.tick(20)
	print("POINTS",points)
	print("EPOCH",epoch)

raw_input()
#print(pos1)

#print(pos1[0:][0],pos1[0:][1])

"""
a, b = zip(*pos1)
plt.plot(a[1],b[1],'bo')
plt.plot(a[1:],b[1:],'b',linewidth=2.0)
a, b = zip(*pos2)
plt.plot(a[1],b[1],'go')
plt.plot(a[1:],b[1:],'g',linewidth=2.0)
a, b = zip(*pos3)
plt.plot(a[1],b[1],'ro')
plt.plot(a[1:],b[1:],'r--',linewidth=2.0)
line1, = plt.plot([0,0], label='Line 1')
line2, = plt.plot([0,0], label='Line 2')
line3, = plt.plot([0,0], label='Line 3')

plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
#plt.scatter(*zip(*pos1))
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
"""
pygame.quit()
quit()
