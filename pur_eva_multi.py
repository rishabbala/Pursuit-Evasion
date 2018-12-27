import pygame
from pygame.locals import *
from math import *
import numpy as np
import random
from scipy.spatial import Voronoi, voronoi_plot_2d,Delaunay

pygame.init()

display_width = 500
display_height = 500

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

obstacle = []
obstacle.append([80,250,20])
obstacle.append([170,300,20])
obstacle.append([340,50,20])
obstacle.append([340,420,20])
obstacle.append([250,250,50])

gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay.fill(white)

clock = pygame.time.Clock()
crashed = False

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

play6 = pygame.image.load('/home/rishab/Downloads/images.png')
play6 = pygame.transform.scale(play6,(10,10))

#p1 = [105, 250]
#p2 = [194, 404]
#p3 = [482, 470]
#p4 = [387, 355]
#p5 = [348, 470]
#p6 = [304, 164]

p1 = [random.randint(0,500),random.randint(0,500)]
p2 = [random.randint(0,500),random.randint(0,500)]
p3 = [random.randint(0,500),random.randint(0,500)]
p4 = [random.randint(0,500),random.randint(0,500)]
p5 = [random.randint(0,500),random.randint(0,500)]
p6 = [random.randint(0,500),random.randint(0,500)]

num_play = 6
num_pur = 5
l1 = []
L1 = []
phi = []
v = np.ndarray(shape=(2,2))
u = np.ndarray(shape=(2,2))
theta = 0

def car(play,x,y):
	gameDisplay.blit(play, (x,y))


def dist(x,y):
	return sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

def ang(x,y):
	angle = atan2((x[1]-y[1]),(x[0]-y[0]))
	if angle<0:
		angle = 2*np.pi+angle
	return (angle)

def intersect(l1,l2):
	inter = []
	flag=0
	for i in range(3):
		for j in range(3):
			if l1[i]==l2[j]:
				if flag==0:
					flag+=1
					temp = l2[j]
				else:
					inter = [temp,l2[j]]
	return inter

rotation = np.zeros((num_play-1,4))
epoch = 1
#pygame.draw.rect(gameDisplay, red, (0,0,500,500), 2)
while not crashed:

	epsilon = 0.00001
	gameDisplay.fill(white)
	points = []
	neigh = []

	points.append(p1)
	points.append(p2)
	points.append(p3)
	points.append(p4)
	points.append(p5)
	points.append(p6)
	print(points)

	for i in range(len(obstacle)):
		pygame.draw.circle(gameDisplay, (0,255,0), (int(obstacle[i][0]),int(obstacle[i][1])), int(obstacle[i][2]))

	pos = 0
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

	for i in range(num_play):
		if i!=num_play-1:
			pygame.draw.line(gameDisplay, red, (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[i+1][1]][0],points[neigh[i+1][1]][1]), 3)
		else:
			pygame.draw.line(gameDisplay, red, (points[neigh[i][1]][0],points[neigh[i][1]][1]), (points[neigh[0][1]][0],points[neigh[0][1]][1]), 3)	#plot fig

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True


	d1=0
	d2=0
	d3=0

	tri = Delaunay(points)
	#print("TRII",tri.simplices)
	a = []
	center = []
	radius = []
	obtuse = []
	ps = []
	##print("LEN",len(tri.simplices))
	for p in range(len(tri.simplices)):
		a = []
		for q in range(3):
			tem = points[tri.simplices[p][q]]
			a.append(tem)		#find the points forming the Delaunay triangle
		#print("A",a)

		ang1 = abs(-(ang(a[0],a[1]))+(ang(a[0],a[2])))	#find the obtuse angles
		ang2 = abs(-(ang(a[1],a[2]))+(ang(a[1],a[0])))
		ang3 = abs(-(ang(a[2],a[1]))+(ang(a[2],a[0])))
		while ang1>np.pi:
			ang1 = ang1-2*np.pi
		while ang2>np.pi:
			ang2 = ang2-2*np.pi
		while ang3>np.pi:
			ang3 = ang3-2*np.pi
		##print(ang1,ang2,ang3)
		if abs(ang1)>np.pi/2:
			obt = [1,2]
			obtuse.append([a[obt[0]],a[obt[1]],p])
		elif abs(ang2)>np.pi/2:
			obt = [0,2]
			obtuse.append([a[obt[0]],a[obt[1]],p])
		elif abs(ang3)>np.pi/2:
			obt = [0,1]
			obtuse.append([a[obt[0]],a[obt[1]],p])

		mid1 = [((a[0][0]+a[1][0])/2),((a[0][1]+a[1][1])/2)]
		mid2 = [((a[2][0]+a[1][0])/2),((a[2][1]+a[1][1])/2)]
		m1 = (a[0][1]-a[1][1]+epsilon)/(a[0][0]-a[1][0]+epsilon)
		m2 = (a[2][1]-a[1][1]+epsilon)/(a[2][0]-a[1][0]+epsilon)
		c1 = mid1[1]+(1/m1)*mid1[0]
		c2 = mid2[1]+(1/m2)*mid2[0]
		xc = (c2-c1)/((1/m2)-(1/m1))
		yc = (c1*m1-c2*m2)/(m1-m2)
		rad = dist([xc,yc],a[0])
		#pygame.draw.circle(gameDisplay, (100,200,50), (int(xc),int(yc)), int(rad) , 2)
		center.append([xc,yc])
		radius.append(rad)
		ps.append(a)	#finding points of Delaunay triangle and finding obtuse angles
	#print("PS",ps)
	not_done = []	#points whose lines in vornoi yet to be drawn
	done = []	#points whose lines in vornoi already drawn


	for i in range(len(tri.simplices)-1):
		num=0
		for j in range(i+1,len(tri.simplices)):
			f1=0
			intersection = []
			intersection = intersect(ps[i],ps[j])
			if intersection!=[]:
				pygame.draw.line(gameDisplay, black, (center[i][0],center[i][1]), (center[j][0],center[j][1]), 5)
				done.append([intersection,i,j])	#finding all points contained in the intersection of adjacent circles
	#print("DONE",done)

	L = []	#L from paper
	l = []	#l from paper
	vor_neigh = []
	for i in range(len(done)):
		mid1 = (done[i][0][0][0]+done[i][0][1][0])/2
		mid2 = (done[i][0][0][1]+done[i][0][1][1])/2
		if done[i][0][0]==points[num_play-1]:
			vor_neigh.append(done[i][0][1])
		elif done[i][0][1]==points[num_play-1]:
			vor_neigh.append(done[i][0][0])
		if done[i][0][0][0]==points[num_play-1][0] and done[i][0][0][1]==points[num_play-1][1] and 0<center[done[i][1]][0]<500 and 0<center[done[i][1]][1]<500 and 0<center[done[i][2]][0]<500 and 0<center[done[i][2]][1]<500:
			#print("1")
			L.append([dist(center[done[i][1]],center[done[i][2]]),done[i][0][1]])
			l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
		elif done[i][0][1][0]==points[num_play-1][0] and done[i][0][1][1]==points[num_play-1][1] and 0<center[done[i][1]][0]<500 and 0<center[done[i][1]][1]<500 and 0<center[done[i][2]][0]<500 and 0<center[done[i][2]][1]<500:
			#print("2")
			L.append([dist(center[done[i][1]],center[done[i][2]]),done[i][0][0]])
			l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
		elif (done[i][0][0][0]==points[num_play-1][0] and done[i][0][0][1]==points[num_play-1][1]) or (done[i][0][1][0]==points[num_play-1][0] and done[i][0][1][1]==points[num_play-1][1]):
			#print("3")
			theta = ang(center[done[i][1]],center[done[i][2]])

			midx = (done[i][0][0][0]+done[i][0][1][0])/2
			midy = (done[i][0][0][1]+done[i][0][1][1])/2
			if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
				pass
			elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
				theta = theta+np.pi

			while theta>2*np.pi:
				theta = theta-2*np.pi

			#print(theta)
			if theta>0 and theta<np.pi/2:
				#print("a")
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(0-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(0-center[done[i][1]][1])
				if x_new<0 or x_new>500:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				else:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
			elif theta>np.pi/2 and theta<np.pi:
				#print("b")
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(500-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(0-center[done[i][1]][1])
				if x_new>0 and x_new<500:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				elif y_new>0 and y_new<500:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[500,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[500,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[500,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[500,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
			elif theta>3*np.pi/2 and theta<2*np.pi:
				#print("c")
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(0-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(500-center[done[i][1]][1])
				if x_new>0 and x_new<500:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,500]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,500]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,500]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,500]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				elif y_new>0 and y_new<500:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
			elif theta>np.pi and theta<3*np.pi/2:
				#print("d")
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(500-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(500-center[done[i][1]][1])
				if x_new<0 or x_new>500:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[500,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[500,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[500,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[500,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				else:
					if center[done[i][1]][0]>0 and center[done[i][1]][0]<500 and center[done[i][1]][1]>0 and center[done[i][1]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,500]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,500]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>0 and center[done[i][2]][0]<500 and center[done[i][2]][1]>0 and center[done[i][2]][1]<500:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,500]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,500]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])	#finding all L and l values for drawn points


	for i in range(len(tri.simplices)):
		for q in range(3):
			for o in range(q+1,3):
				flag = 0
				for p in range(len(done)):
					if (ps[i][q] == done[p][0][0] and ps[i][o] == done[p][0][1]) or (ps[i][q] == done[p][0][1] and ps[i][o] == done[p][0][0]):
						pass
					else:
						flag+=1
				if flag==len(done):
					not_done.append([ps[i][q],ps[i][o],i]) # if the points are not yet covered in Voronoi add to not_done
	#print("ND",not_done)


	for i in range(len(not_done)):
		obt = []
		flag = 0
		for j in range(len(obtuse)):
			if obtuse[j][2]==not_done[i][2]:
				obt.append([obtuse[j][0],obtuse[j][1]])
		b1 = not_done[i][0]
		b2 = not_done[i][1]
		if b1==points[num_play-1]:
			vor_neigh.append(b2)
		elif b2==points[num_play-1]:
			vor_neigh.append(b1)
		mid1 = (b1[0]+b2[0])/2
		mid2 = (b1[1]+b2[1])/2
		mp = center[not_done[i][2]]
		theta = ang(mp,[mid1,mid2])

		if 0<mp[0]<500 and 0<mp[1]<500:
			if theta>0 and theta<np.pi/2:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(0-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(0-mp[1])
				if x_new<0 or x_new>500:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (0,y_new), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[0,y_new]),b2])
							l.append([dist([0,y_new],[mid1,mid2]),b2,ang([0,y_new],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[0,y_new]),b1])
							l.append([dist([0,y_new],[mid1,mid2]),b1,ang([0,y_new],[mid1,mid2])])

					y_n = y_new+(mp[1]-y_new)/(mp[0]-0+epsilon) * (500-0)
					x_n = 0+(mp[0]-0)/(mp[1]-y_new+epsilon) * (500-y_new)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b2])
									l.append([dist([x_n,500],[mid1,mid2]),b2,ang([x_n,500],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b1])
									l.append([dist([x_n,500],[mid1,mid2]),b1,ang([x_n,500],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b2])
									l.append([dist([500,y_n],[mid1,mid2]),b2,ang([500,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b1])
									l.append([dist([500,y_n],[mid1,mid2]),b1,ang([500,y_n],[mid1,mid2])])

						if flag == 0:
							pass

				else:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (x_new,0), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,0]),b2])
							l.append([dist([x_new,0],[mid1,mid2]),b2,ang([x_new,0],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,0]),b1])
							l.append([dist([x_new,0],[mid1,mid2]),b1,ang([x_new,0],[mid1,mid2])])

					y_n = 0+(mp[1]-0)/(mp[0]-x_new+epsilon) * (500-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-0+epsilon) * (500-0)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b2])
									l.append([dist([x_n,500],[mid1,mid2]),b2,ang([x_n,500],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b1])
									l.append([dist([x_n,500],[mid1,mid2]),b1,ang([x_n,500],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b2])
									l.append([dist([500,y_n],[mid1,mid2]),b2,ang([500,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b1])
									l.append([dist([500,y_n],[mid1,mid2]),b1,ang([500,y_n],[mid1,mid2])])

						if flag == 0:
							pass
			elif theta>np.pi/2 and theta<np.pi:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(500-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(0-mp[1])
				if x_new>0 and x_new<500:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (x_new,0), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,0]),b2])
							l.append([dist([x_new,0],[mid1,mid2]),b2,ang([x_new,0],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,0]),b1])
							l.append([dist([x_new,0],[mid1,mid2]),b1,ang([x_new,0],[mid1,mid2])])

					y_n = 0+(mp[1]-0)/(mp[0]-x_new+epsilon) * (0-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-0+epsilon) * (500-0)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b2])
									l.append([dist([x_n,500],[mid1,mid2]),b2,ang([x_n,500],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b1])
									l.append([dist([x_n,500],[mid1,mid2]),b1,ang([x_n,500],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b2])
									l.append([dist([0,y_n],[mid1,mid2]),b2,ang([0,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b1])
									l.append([dist([0,y_n],[mid1,mid2]),b1,ang([0,y_n],[mid1,mid2])])

						if flag == 0:
							pass
				elif y_new>0 and y_new<500:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (500,y_new), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[500,y_new]),b2])
							l.append([dist([500,y_new],[mid1,mid2]),b2,ang([500,y_new],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[500,y_new]),b1])
							l.append([dist([500,y_new],[mid1,mid2]),b1,ang([500,y_new],[mid1,mid2])])

					y_n = y_new+(mp[1]-y_new)/(mp[0]-500+epsilon) * (0-500)
					x_n = 500+(mp[0]-500)/(mp[1]-y_new+epsilon) * (500-y_new)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,500), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b2])
									l.append([dist([x_n,500],[mid1,mid2]),b2,ang([x_n,500],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,500]),b1])
									l.append([dist([x_n,500],[mid1,mid2]),b1,ang([x_n,500],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b2])
									l.append([dist([0,y_n],[mid1,mid2]),b2,ang([0,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b1])
									l.append([dist([0,y_n],[mid1,mid2]),b1,ang([0,y_n],[mid1,mid2])])

						if flag == 0:
							pass
			elif theta>3*np.pi/2 and theta<2*np.pi:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(0-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(500-mp[1])
				if x_new>0 and x_new<500:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (x_new,500), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,500]),b2])
							l.append([dist([x_new,500],[mid1,mid2]),b2,ang([x_new,500],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,500]),b1])
							l.append([dist([x_new,500],[mid1,mid2]),b1,ang([x_new,500],[mid1,mid2])])

					y_n = 500+(mp[1]-500)/(mp[0]-x_new+epsilon) * (500-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-500+epsilon) * (0-500)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b2])
									l.append([dist([x_n,0],[mid1,mid2]),b2,ang([x_n,0],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b1])
									l.append([dist([x_n,0],[mid1,mid2]),b1,ang([x_n,0],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b2])
									l.append([dist([500,y_n],[mid1,mid2]),b2,ang([500,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b1])
									l.append([dist([500,y_n],[mid1,mid2]),b1,ang([500,y_n],[mid1,mid2])])

						if flag == 0:
							pass
				elif y_new>0 and y_new<500:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
							pass
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (0,y_new), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[0,y_new]),b2])
							l.append([dist([0,y_new],[mid1,mid2]),b2,ang([0,y_new],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[0,y_new]),b1])
							l.append([dist([0,y_new],[mid1,mid2]),b1,ang([0,y_new],[mid1,mid2])])

					y_n = y_new+(mp[1]-y_new)/(mp[0]-0+epsilon) * (500-0)
					x_n = 0+(mp[0]-0)/(mp[1]-y_new+epsilon) * (0-y_new)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b2])
									l.append([dist([x_n,0],[mid1,mid2]),b2,ang([x_n,0],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b1])
									l.append([dist([x_n,0],[mid1,mid2]),b1,ang([x_n,0],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (500,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b2])
									l.append([dist([500,y_n],[mid1,mid2]),b2,ang([500,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[500,y_n]),b1])
									l.append([dist([500,y_n],[mid1,mid2]),b1,ang([500,y_n],[mid1,mid2])])

						if flag == 0:
							pass
			elif theta>np.pi and theta<3*np.pi/2:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(500-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(500-mp[1])
				if x_new<0 or x_new>500:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
							pass
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (500,y_new), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[500,y_new]),b2])
							l.append([dist([500,y_new],[mid1,mid2]),b2,ang([500,y_new],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[500,y_new]),b1])
							l.append([dist([500,y_new],[mid1,mid2]),b1,ang([500,y_new],[mid1,mid2])])

					y_n = y_new+(mp[1]-y_new)/(mp[0]-500+epsilon) * (0-500)
					x_n = 500+(mp[0]-500)/(mp[1]-y_new+epsilon) * (0-y_new)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b2])
									l.append([dist([x_n,0],[mid1,mid2]),b2,ang([x_n,0],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b1])
									l.append([dist([x_n,0],[mid1,mid2]),b1,ang([x_n,0],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b2])
									l.append([dist([0,y_n],[mid1,mid2]),b2,ang([0,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b1])
									l.append([dist([0,y_n],[mid1,mid2]),b1,ang([0,y_n],[mid1,mid2])])

						if flag == 0:
							pass
				else:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (x_new,500), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,500]),b2])
							l.append([dist([x_new,500],[mid1,mid2]),b2,ang([x_new,500],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,500]),b1])
							l.append([dist([x_new,500],[mid1,mid2]),b1,ang([x_new,500],[mid1,mid2])])

					y_n = 500+(mp[1]-500)/(mp[0]-x_new+epsilon) * (0-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-500+epsilon) * (0-500)
					if x_n>0 and x_n<500:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,0), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b2])
									l.append([dist([x_n,0],[mid1,mid2]),b2,ang([x_n,0],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,0]),b1])
									l.append([dist([x_n,0],[mid1,mid2]),b1,ang([x_n,0],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (0,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b2])
									l.append([dist([0,y_n],[mid1,mid2]),b2,ang([0,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[0,y_n]),b1])
									l.append([dist([0,y_n],[mid1,mid2]),b1,ang([0,y_n],[mid1,mid2])])
						if flag == 0:
							pass	# for the points no done draw the vornoi based on whether they are obtuse or acute and correspondingly calculate L and l

	#print("L",L)
	#print("l",l)


	v = np.zeros((len(l),3))
	n = np.zeros(num_play-1)
	num = np.ones(num_play-1)
	for i in range(len(l)):
		pos = num_play+1
		pt = l[i][1]
		for j in range(num_play-1):
			if pt[0] == points[j][0] and pt[1] == points[j][1]:
				pos = j
				num[pos]-=1
		if pos!=num_play+1:
			v[i][0] = -L[i][0]/2
			v[i][1] = (l[i][0]**2-(L[i][0]-l[i][0])**2)/(2*(dist(pt,points[num_play-1]))+epsilon)
			absol = sqrt(v[i][0]**2+v[i][1]**2+epsilon)
			v[i][0]/= -absol
			v[i][1]/= -absol
			v[i][2] = pos
			n[pos]+=1
			#pygame.draw.line(gameDisplay, (255,0,255), (l[i][1][0],l[i][1][1]), ((l[i][1][0]-100*cos(l[i][2])),(l[i][1][1]-100*sin(l[i][2]))), 5)	# find normalised velocities for points adjacent to evader


	temp = np.zeros(3)
	for i in range(num_play-1):
		if n[i]==0:
			temp[0] = 1
			temp[1] = 0
			temp[2] = i
			v = np.vstack((v,temp))	# for other points velocity is one along line joined to evader

	#print("LLKLK",v)
	u = np.zeros((num_play-1,2))
	for i in range(len(v)):
		if (n[int(v[i][2])])!=0:
			u[i][0] = -v[i][0]*cos(ang(points[int(v[i][2])],points[num_play-1]))-v[i][1]*cos(l[i][2])
			u[i][1] = -v[i][0]*sin(ang(points[int(v[i][2])],points[num_play-1]))-v[i][1]*sin(l[i][2])
			#points[int(v[i][2])][0] = points[int(v[i][2])][0]+u[i][0]
			#points[int(v[i][2])][1] = points[int(v[i][2])][1]+u[i][1]
		else:
			u[i][0] = -v[i][0]*cos(ang(points[int(v[i][2])],points[num_play-1]))
			u[i][1] = -v[i][0]*sin(ang(points[int(v[i][2])],points[num_play-1]))
			#points[int(v[i][2])][0] = points[int(v[i][2])][0]+u[i][0]
			#points[int(v[i][2])][1] = points[int(v[i][2])][1]+u[i][1]	# calculate the x,y velocities for all points


	print(epoch)
	for i in range(num_play-1):
		flag=0
		c=0
		d=0
		k=0
		print(rotation)
		for j in range(len(obstacle)):
		#if epoch==1 or rotation[int(v[i][2])][0] == 0:
			print("IN@")
			obst_ang = ang([obstacle[j][0],obstacle[j][1]],points[int(v[i][2])])
			if dist(points[int(v[i][2])],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])<2 or dist([points[int(v[i][2])][0]+u[i][0],points[int(v[i][2])][1]+u[i][1]],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])<2:
				flag+=1
				print("IN")
				print("Touch")
				if epoch==1 or rotation[int(v[i][2])][0] == 0:
					if obst_ang<np.pi/2:
						x = points[int(v[i][2])][0]-cos(3*np.pi/2+obst_ang)
						y = points[int(v[i][2])][1]-sin(3*np.pi/2+obst_ang)
						if dist([x,y],points[num_play-1])-dist(points[int(v[i][2])],points[num_play-1])<=0:
							c+= -cos(3*np.pi/2+obst_ang)
							d+= -sin(3*np.pi/2+obst_ang)
							rotation[int(v[i][2])][0]=1
							rotation[int(v[i][2])][1]=int(v[i][2])
							rotation[int(v[i][2])][2]=c
							rotation[int(v[i][2])][3]=d
						elif dist([x,y],points[num_play-1])-dist(points[int(v[i][2])],points[num_play-1])>0:
							c+= -cos(np.pi/2+obst_ang)
							d+= -sin(np.pi/2+obst_ang)
							rotation[int(v[i][2])][0]=2
							rotation[int(v[i][2])][1]=int(v[i][2])
							rotation[int(v[i][2])][2]=c
							rotation[int(v[i][2])][3]=d
					else:
						x = points[int(v[i][2])][0]-cos(obst_ang-np.pi/2)
						y = points[int(v[i][2])][1]-sin(obst_ang-np.pi/2)
						if dist([x,y],points[num_play-1])-dist(points[int(v[i][2])],points[num_play-1])<=0:
							c+= -cos(obst_ang-np.pi/2)
							d+= -sin(obst_ang-np.pi/2)
							rotation[int(v[i][2])][0]=1
							rotation[int(v[i][2])][1]=int(v[i][2])
							rotation[int(v[i][2])][2]=c
							rotation[int(v[i][2])][3]=d
						elif dist([x,y],points[num_play-1])-dist(points[int(v[i][2])],points[num_play-1])>0:
							c+= -cos(obst_ang+np.pi/2)
							d+= -sin(obst_ang+np.pi/2)
							rotation[int(v[i][2])][0]=2
							rotation[int(v[i][2])][1]=int(v[i][2])
							rotation[int(v[i][2])][2]=c
							rotation[int(v[i][2])][3]=d
				elif rotation[int(v[i][2])][0]==2:
					c+= -cos(obst_ang-np.pi/2)
					d+= -sin(obst_ang-np.pi/2)
					rotation[int(v[i][2])][2]=c
					rotation[int(v[i][2])][3]=d
				elif rotation[int(v[i][2])][0]==3:
					c+= -cos(obst_ang+np.pi/2)
					d+= -sin(obst_ang+np.pi/2)
					rotation[int(v[i][2])][0]=2
					rotation[int(v[i][2])][1]=int(v[i][2])
					rotation[int(v[i][2])][2]=c
					rotation[int(v[i][2])][3]=d
				#print(flag,epoch)
		if flag==0 and dist(points[int(v[i][2])],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])>5 and dist([points[int(v[i][2])][0]+u[i][0],points[int(v[i][2])][1]+u[i][1]],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])>5:
			rotation[int(v[i][2])][0]=0
			rotation[int(v[i][2])][1]=int(v[i][2])
			rotation[int(v[i][2])][2]=10
			rotation[int(v[i][2])][3]=10
	print(rotation,"ROT")

	for i in range(num_play-1):
		if rotation[int(v[i][2])][0]==1 or rotation[int(v[i][2])][0]==2:
			#print("CAC",c,d)
			points[int(v[i][2])][0]+=rotation[int(v[i][2])][2]/sqrt(rotation[int(v[i][2])][2]**2+rotation[int(v[i][2])][3]**2)
			points[int(v[i][2])][1]+=rotation[int(v[i][2])][3]/sqrt(rotation[int(v[i][2])][2]**2+rotation[int(v[i][2])][3]**2)
		else:
			points[int(v[i][2])][0]+=u[i][0]
			points[int(v[i][2])][1]+=u[i][1]



	#print(v)

	field_1=0
	field_2=0
	for i in range(len(vor_neigh)):
		field_1+= -(1/dist(vor_neigh[i],points[num_play-1])**2)*cos(ang(vor_neigh[i],points[num_play-1]))
		field_2+= -(1/dist(vor_neigh[i],points[num_play-1])**2)*sin(ang(vor_neigh[i],points[num_play-1]))

	field_1+= -(1/dist([500,points[num_play-1][1]],points[num_play-1])**2)*cos(0) -(1/dist([0,points[num_play-1][1]],points[num_play-1])**2)*cos(np.pi)
	field_2+= -(1/dist([points[num_play-1][0],500],points[num_play-1])**2)*cos(0) -(1/dist([points[num_play-1][0],0],points[num_play-1])**2)*cos(np.pi)

	for i in range(len(obstacle)):
		obst_ang = ang([obstacle[i][0],obstacle[i][1]],points[num_play-1])
		field_1+= -(1/dist(obstacle[i],points[num_play-1])**2)*cos(obst_ang)
		field_2+= -(1/dist(obstacle[i],points[num_play-1])**2)*sin(obst_ang)

	field_x = field_1/sqrt(field_1**2 + field_2**2)
	field_y = field_2/sqrt(field_1**2 + field_2**2)

	"""
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
	"""
	points[num_play-1][0]+=field_x
	points[num_play-1][1]+=field_y

	for i in range(num_play-1):
		if dist(points[i],points[num_play-1])<10:
			print("CAUGHT")
			crashed = True
			break

	for i in range(num_play-1):
		car(play1,points[i][0],points[i][1])

	car(play6,p6[0],p6[1])
	pygame.display.update()
	clock.tick(20)
	epoch+=1
	#print(epoch)
	#crashed = True
raw_input()
pygame.quit()
quit()
