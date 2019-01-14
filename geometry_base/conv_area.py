import pygame
from pygame.locals import *
from math import *
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.legend_handler import HandlerLine2D
import time
import csv

########    Implementation of area minimisation. Becomes st line    ########


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


#p1 = [283.4347710356184, 313.09945897007003]
#p2 = [249.08285212928874, 257.00343814809503]
#p3 = [294.9853791929681, 43.99989311028816]
#p4 = [226.11505830458034, 95.99335874010707]
#p5 = [378.2910, 118.7763123]


p1 = [random.randint(0,500),random.randint(0,500)]
p2 = [random.randint(0,500),random.randint(0,500)]
p3 = [random.randint(0,500),random.randint(0,500)]
p4 = [random.randint(0,500),random.randint(0,500)]
p5 = [random.randint(0,500),random.randint(0,500)]

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


			########   CENTROID DISTANCE TO EVADER ALGORITHM
			x1=0
			y1=0
			for j in range(num_play-1):
				x1+=points[j][0]
				y1+=points[j][1]
			x1-=(num_play-1)*points[num_play-1][0]
			y1-=(num_play-1)*points[num_play-1][1]
			alpha = atan2(y1,x1)
			if alpha<0:
				alpha+=2*np.pi
			a1 = alpha
			a2 = alpha+np.pi/2

			temp1 = a1*100
			temp2 = a2*100

			#theta2 = (a1+a2)/2
			d = dist([centx,centy],points[num_play-1])
			for j in range (int(temp1),int(temp2)):
				pointx = points[neigh[i][1]][0]-cos(j/100)
				pointy = points[neigh[i][1]][1]-sin(j/100)
				centnx = ((centx*num_play)-cos(j/100))/num_play
				centny = ((centy*num_play)-sin(j/100))/num_play
				dn = dist([centnx,centny],points[num_play-1])
				#peri3 = peri2+dist([pointx,pointy],points[neigh[i+1][1]])+dist([pointx,pointy],points[neigh[i-1][1]])
				if dn<d:
					d = dn
					theta2=j/100
			pygame.draw.line(gameDisplay, (0,0,255), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(theta2),points[neigh[i][1]][1]-50*sin(theta2)), 3)
			print("BLUE=CENT")








			#### PERIMETER ALGORITHM ####
			if i!=0 and i!=num_play-1:
				d = dist(points[neigh[i][1]],points[neigh[i+1][1]])/(dist(points[neigh[i][1]],points[neigh[i-1][1]])+epsilon)
				beta = atan2(((1+d)*points[neigh[i][1]][1]-points[neigh[i+1][1]][1]-d*points[neigh[i-1][1]][1]),((1+d)*points[neigh[i][1]][0]-points[neigh[i+1][1]][0]-d*points[neigh[i-1][1]][0]))
				peri2 = peri-dist(points[neigh[i][1]],points[neigh[i+1][1]])-dist(points[neigh[i][1]],points[neigh[i-1][1]])
				next = neigh[i+1][1]
				prev = neigh[i-1][1]
			elif i==num_play-1:
				d = dist(points[neigh[i][1]],points[neigh[0][1]])/dist(points[neigh[i][1]],points[neigh[i-1][1]])
				beta = atan2(((1+d)*points[neigh[i][1]][1]-points[neigh[0][1]][1]-d*points[neigh[i-1][1]][1]),((1+d)*points[neigh[i][1]][0]-points[neigh[0][1]][0]-d*points[neigh[i-1][1]][0]))
				peri2 = peri-dist(points[neigh[i][1]],points[neigh[0][1]])-dist(points[neigh[i][1]],points[neigh[i-1][1]])
				next = neigh[0][1]
				prev = neigh[i-1][1]
			elif i==0:
				d = dist(points[neigh[i][1]],points[neigh[i+1][1]])/dist(points[neigh[i][1]],points[neigh[num_play-1][1]])
				beta = atan2(((1+d)*points[neigh[i][1]][1]-points[neigh[i+1][1]][1]-d*points[neigh[num_play-1][1]][1]),((1+d)*points[neigh[i][1]][0]-points[neigh[i+1][1]][0]-d*points[neigh[num_play-1][1]][0]))
				peri2 = peri-dist(points[neigh[i][1]],points[neigh[i+1][1]])-dist(points[neigh[i][1]],points[neigh[num_play-1][1]])
				next = neigh[i+1][1]
				prev = neigh[num_play-1][1]

			if beta<0:
				beta = 2*np.pi+beta

			b1 = beta
			b2 = beta+np.pi/2  #peri based


			temp1 = b1*100
			temp2 = b2*100
			min_p = peri
			for j in range (int(temp1),int(temp2)):
				pointx = points[neigh[i][1]][0]-cos(j/100)
				pointy = points[neigh[i][1]][1]-sin(j/100)
				if i!=0 and i!=num_play-1:
					peri3 = peri2+dist([pointx,pointy],points[neigh[i+1][1]])+dist([pointx,pointy],points[neigh[i-1][1]])
				elif i==0:
					peri3 = peri2+dist([pointx,pointy],points[neigh[i+1][1]])+dist([pointx,pointy],points[neigh[num_play-1][1]])
				elif i==num_play-1:
					peri3 = peri2+dist([pointx,pointy],points[neigh[0][1]])+dist([pointx,pointy],points[neigh[i-1][1]])
				if peri3<min_p:
					min_p = peri3
					theta=j/100
			pygame.draw.line(gameDisplay, (0,255,0), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(theta),points[neigh[i][1]][1]-50*sin(theta)), 3)
			print("GREEN=PERI")







			########AREA ALGORITHM############
			if i!=0 and i!=num_play-1:
				gamma = ang(points[neigh[i+1][1]], points[neigh[i-1][1]])
				#area+=points[neigh[i][1]][0]*points[neigh[i+1][1]][1] - points[neigh[i+1][1]][0]*points[neigh[i][1]][1]
				area2 = (2*area-(points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i][1]][0]*points[neigh[i-1][1]][1])-(points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i+1][1]][0]*points[neigh[i][1]][1]))
				#peri2 = peri-dist(points[neigh[i][1]],points[neigh[i+1][1]])-dist(points[neigh[i][1]],points[neigh[i-1][1]])
				next = neigh[i+1][1]
				prev = neigh[i-1][1]
			elif i==num_play-1:
				gamma = ang(points[neigh[0][1]], points[neigh[i-1][1]])
				area2 = (2*area-(points[neigh[i-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i][1]][0]*points[neigh[i-1][1]][1])-(points[neigh[i][1]][0]*points[neigh[0][1]][1]-points[neigh[0][1]][0]*points[neigh[i][1]][1]))
				#peri2 = peri-dist(points[neigh[i][1]],points[neigh[0][1]])-dist(points[neigh[i][1]],points[neigh[i-1][1]])
				next = neigh[0][1]
				prev = neigh[i-1][1]
			elif i==0:
				gamma = ang(points[neigh[i+1][1]], points[neigh[num_play-1][1]])
				area2 = (2*area-(points[neigh[num_play-1][1]][0]*points[neigh[i][1]][1]-points[neigh[i][1]][0]*points[neigh[num_play-1][1]][1])-(points[neigh[i][1]][0]*points[neigh[i+1][1]][1]-points[neigh[i+1][1]][0]*points[neigh[i][1]][1]))
				#peri2 = peri-dist(points[neigh[i][1]],points[neigh[i+1][1]])-dist(points[neigh[i][1]],points[neigh[num_play-1][1]])
				next = neigh[i+1][1]
				prev = neigh[num_play-1][1]
			#print("AREA2",area2)

			#for minimization must be -pi/2 to 0 and <min
			g1 = gamma
			g2 = gamma+np.pi/2

			temp1 = g1*100
			temp2 = g2*100
			min_a = area
			for j in range (int(temp1),int(temp2)):
				pointx = points[neigh[i][1]][0]-cos(j/100)
				pointy = points[neigh[i][1]][1]-sin(j/100)
				if i!=0 and i!=num_play-1:
					area3 = (area2+(points[neigh[i-1][1]][0]*pointy-pointx*points[neigh[i-1][1]][1])+(pointx*points[neigh[i+1][1]][1]-points[neigh[i+1][1]][0]*pointy))/2
				elif i==0:
					area3 = (area2+(points[neigh[num_play-1][1]][0]*pointy-pointx*points[neigh[num_play-1][1]][1])+(pointx*points[neigh[i+1][1]][1]-points[neigh[i+1][1]][0]*pointy))/2
				elif i==num_play-1:
					area3 = (area2+(points[neigh[i-1][1]][0]*pointy-pointx*points[neigh[i-1][1]][1])+(pointx*points[neigh[0][1]][1]-points[neigh[0][1]][0]*pointy))/2
				if area3>min_a:
					#print("AREA3",area3)
					min_a = area3
					theta3=j/100
			pygame.draw.line(gameDisplay, (120,120,120), (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(theta3),points[neigh[i][1]][1]-50*sin(theta3)), 3)
			print("GREY=AREA")


			theta4 = ang(points[neigh[i][1]],points[num_play-1])

			#if neigh[i][1]==0:
			#	ang1 = abs(-(ang(points[0],points[num_play-1]))+(ang(points[0],points[1])))
			#if neigh[i][1]==1:
			ang1 = abs(-(ang(points[num_play-1],points[0]))+(ang(points[num_play-1],points[1])))
			while ang1>np.pi:
				ang1 = ang1-2*np.pi


			#phi = k*theta2 + (1-k)*theta3


			c1 = -cos(theta)  ##peri
			s1 = -sin(theta)

			c2 = -cos(theta2)  ##centroid
			s2 = -sin(theta2)

			c3 = -cos(theta3)  ##area
			s3 = -sin(theta3)

			c4 = -cos(theta4)  ##direct distance
			s4 = -sin(theta4)

			k=0.8
			k1=0.5
			#if abs(theta2-theta4)<np.pi/2:
			#	k=0.8
			#	k1=0.5
			#	ab = sqrt((k*(k1*c4+(1-k1)*c2)+(1-k)*c3)**2+(k*(k1*s4+(1-k1)*s2)+(1-k)*s3)**2)
			#	fx = (k*(k1*c4+(1-k1)*c2)+(1-k)*c3)/ab
			#	fy = (k*(k1*s4+(1-k1)*s2)+(1-k)*s3)/ab
			#else:
			####   k*(k1*c4+(1-k1)*(k2*c2+(1-k2)*c1))+(1-k)*c3
			ab = sqrt((k*(k1*c4+(1-k1)*c1)+(1-k)*c3)**2+(k*(k1*s4+(1-k1)*s1)+(1-k)*s3)**2)

			if abs(ang1)>np.pi/2:
				k=0.8
				k1=0.5
				ab = sqrt((k*(k1*c4+(1-k1)*c1)+(1-k)*c3)**2+(k*(k1*s4+(1-k1)*s1)+(1-k)*s3)**2)
				fx = (k*(k1*c4+(1-k1)*c1)+(1-k)*c3)/ab
				fy = (k*(k1*s4+(1-k1)*s1)+(1-k)*s3)/ab
			else:
				k=0.8
				k1=0.5
				ab = sqrt((k*(k1*c4+(1-k1)*c2)+(1-k)*c3)**2+(k*(k1*s4+(1-k1)*s2)+(1-k)*s3)**2)
				fx = (k*(k1*c4+(1-k1)*c2)+(1-k)*c3)/ab
				fy = (k*(k1*s4+(1-k1)*s2)+(1-k)*s3)/ab
			#print("FX/Y",fx,fy)

			phi = ang(points[neigh[i][1]],points[num_play-1])
			points[neigh[i][1]][0]+=fx
			points[neigh[i][1]][1]+=fy




			phi = atan2(-fy,-fx)
			phi = wrap(phi)
			pygame.draw.line(gameDisplay, black, (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i][1]][0]-50*cos(phi),points[neigh[i][1]][1]-50*sin(phi)), 3)

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

	clock.tick(20)
	print("POINTS",points)
	print("EPOCH",epoch)
	print("--- %s seconds ---" % (time.time() - start_time))
	break
with open("mylist.csv","a") as f:
	wr = csv.writer(f, dialect='excel')
	wr.writerow([k,k1,epoch])
raw_input()
#with open("mylist.txt","a+") as f: #in write mode
#	f.writelines(([k,k1,end],"\n"))
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
