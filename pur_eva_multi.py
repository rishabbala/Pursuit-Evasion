import pygame
from pygame.locals import *
from math import *
import numpy as np
import random
from scipy.spatial import Voronoi, voronoi_plot_2d,Delaunay
import time

pygame.init()

display_width = 500
display_height = 500

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

####  These are the position of obstacles if any
obstacle = []
#obstacle.append([80,250,20])
#obstacle.append([170,300,20])
#obstacle.append([340,50,20])
#obstacle.append([340,420,20])
obstacle.append([250,250,0])

gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay.fill(white)

clock = pygame.time.Clock()
crashed = False

play1 = pygame.image.load('/home/rishab/Downloads/player.png')
play1 = pygame.transform.scale(play1,(10,10))

play2 = pygame.image.load('/home/rishab/Downloads/images.png')
play2 = pygame.transform.scale(play2,(10,10))

####  These are the initial position of points with the last point as the evader

p1 = [52.759508790094905, 277.650497039016]
p2 = [142.71605203993622, 115.698046901077]
p3 = [95.54952540345857, 131.83547700803413]
p4 = [417.769424996615, 271.97305455541505]
p5 = [313.0646713125531, 292.35377994069603]




#p1 = [random.randint(0,display_width),random.randint(0,display_height)]
#p2 = [random.randint(0,display_width),random.randint(0,display_height)]
#p3 = [random.randint(0,display_width),random.randint(0,display_height)]
#p4 = [random.randint(0,display_width),random.randint(0,display_height)]
#p5 = [random.randint(0,display_width),random.randint(0,display_height)]
#p6 = [random.randint(0,500),random.randint(0,500)]

num_play = 5
num_pur = 4
l1 = []
L1 = []
phi = []
v = np.ndarray(shape=(2,2))
u = np.ndarray(shape=(2,2))
theta = 0

####  Function to create the players
def car(play,x,y):
	gameDisplay.blit(play, (x,y))

####  Function to find the l2 norm distance ||x||
def dist(x,y):
	return sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

####  To return the angle. Note that in pygame the y axis points downwards and all angles in the program
####  are adjusted accordingly. Every cos(x) becomes -cos(x) and sin(x) becomes -sin(x)
def ang(x,y):
	angle = atan2((x[1]-y[1]),(x[0]-y[0]))
	if angle<=0:
		angle = 2*np.pi+angle
	return (angle)

####  Finds if there is any common chord between two circumcircles formed from the Delaunay triangles
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
start_time = time.time()
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
	print(points)

	for i in range(len(obstacle)):
		pygame.draw.circle(gameDisplay, (0,255,0), (int(obstacle[i][0]),int(obstacle[i][1])), int(obstacle[i][2]))

####  To find the point with least y to plot closed figure in cyclic manner with minimal change in angle
	pos = 0
	bottom = p1
	for i in range(1,num_play):
		if points[i][1]<=bottom[1]:
			bottom = points[i]
			pos = i

####  Finding all neighbours to the point and their angles
	for i in range(0,num_play):
		if i!=pos:
			neigh.append([ang(bottom,points[i]),i])
		else:
			pass

#####  Soring angles to form fig
	neigh.append([0,pos])
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
	a = []
	center = []
	radius = []
	obtuse = []
	ps = []
####  The process is repeated for every Delaunay triangle
####  Find the points forming the Delaunay triangle and append to a
	for p in range(len(tri.simplices)):
		a = []
		for q in range(3):
			tem = points[tri.simplices[p][q]]
			a.append(tem)
		#print("A",a)

####  Find the obtuse angles as the circumcenter lies outside the triangle in case of obtuse triangles
####  opposite to the largest angle
		ang1 = abs(-(ang(a[0],a[1]))+(ang(a[0],a[2])))
		ang2 = abs(-(ang(a[1],a[2]))+(ang(a[1],a[0])))
		ang3 = abs(-(ang(a[2],a[1]))+(ang(a[2],a[0])))
		while ang1>=np.pi:
			ang1 = ang1-2*np.pi
		while ang2>=np.pi:
			ang2 = ang2-2*np.pi
		while ang3>=np.pi:
			ang3 = ang3-2*np.pi
		if abs(ang1)>=np.pi/2:
			obt = [1,2]
			obtuse.append([a[obt[0]],a[obt[1]],p])
		elif abs(ang2)>=np.pi/2:
			obt = [0,2]
			obtuse.append([a[obt[0]],a[obt[1]],p])
		elif abs(ang3)>=np.pi/2:
			obt = [0,1]
			obtuse.append([a[obt[0]],a[obt[1]],p])

#####  Here we plot the circumcircle. The circumcenter is the point of intersection of perpendicular bisectors
#####  The Delaunay triangle is formed in a way such that no other point of the polygon lies within the circumcircle of
#####  formed by any other three points. The voronoi can be constructed by joining adjacent circumcenters if the share
#####  a common chord.

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
		ps.append(a)	#contains all the points forming the Delaunay triangle in order
	not_done = []	#points whose lines in vornoi yet to be drawn
	done = []	#points whose lines in vornoi already drawn


	for i in range(len(tri.simplices)-1):
		num=0
		for j in range(i+1,len(tri.simplices)):
			f1=0
			intersection = []
			intersection = intersect(ps[i],ps[j])
			if intersection!=[]:  #if there is an intersecting chord connect the circumcenters
				pygame.draw.line(gameDisplay, black, (center[i][0],center[i][1]), (center[j][0],center[j][1]), 5)
				done.append([intersection,i,j])  #include the points in done

	L = []	#L from paper
	l = []	#l from paper
	vor_neigh = []  #  These are the voronoi neighbours of the evader
	for i in range(len(done)):
		mid1 = (done[i][0][0][0]+done[i][0][1][0])/2
		mid2 = (done[i][0][0][1]+done[i][0][1][1])/2
		if done[i][0][0]==points[num_play-1]:
			vor_neigh.append(done[i][0][1])
		elif done[i][0][1]==points[num_play-1]:
			vor_neigh.append(done[i][0][0])
####  We check if the two centers of the respective circumcircles lie in our specified arena. This is to find the corresponding
####  values of L and l. If they lie in the arena, then L is the length of line and l is the length to mid-point of the bisector
		if done[i][0][0]==points[num_play-1] and 0<=center[done[i][1]][0]<=display_width and 0<=center[done[i][1]][1]<=display_height and 0<=center[done[i][2]][0]<=display_width and 0<=center[done[i][2]][1]<=display_height:
			L.append([dist(center[done[i][1]],center[done[i][2]]),done[i][0][1]])
			l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
		elif done[i][0][1]==points[num_play-1] and 0<=center[done[i][1]][0]<=display_width and 0<=center[done[i][1]][1]<=display_height and 0<=center[done[i][2]][0]<=display_width and 0<=center[done[i][2]][1]<=display_height:
			L.append([dist(center[done[i][1]],center[done[i][2]]),done[i][0][0]])
			l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
		elif (done[i][0][0]==points[num_play-1]) or (done[i][0][1]==points[num_play-1]):
			theta = ang(center[done[i][1]],center[done[i][2]])
			midx = (done[i][0][0][0]+done[i][0][1][0])/2
			midy = (done[i][0][0][1]+done[i][0][1][1])/2
####  Care should be taken with the angles
			if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
				pass
			elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
				theta = theta+np.pi
			while theta>=2*np.pi:
				theta = theta-2*np.pi
####  Now depending on the angle of the line there are several possibilities of intersection with the arena. These are apparent when drawing
####  the figure and are prudent in the calculation of L and l
			if theta>=0 and theta<=np.pi/2:
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(0-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(0-center[done[i][1]][1])
				if x_new<=0 or x_new>=display_width:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				else:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
			elif theta>=np.pi/2 and theta<=np.pi:
				#print("b")
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(display_width-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(0-center[done[i][1]][1])
				if x_new>=0 and x_new<=display_width:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,0]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				elif y_new>=0 and y_new<=display_height:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[display_width,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[display_width,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[display_width,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[display_width,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
			elif theta>=3*np.pi/2 and theta<=2*np.pi:
				#print("c")
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(0-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(display_height-center[done[i][1]][1])
				if x_new>=0 and x_new<=display_width:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,display_height]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,display_height]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,display_height]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,display_height]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				elif y_new>=0 and y_new<=display_height:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[0,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
			elif theta>=np.pi and theta<=3*np.pi/2:
				#print("d")
				y_new = center[done[i][1]][1]+(center[done[i][2]][1]-center[done[i][1]][1])/(center[done[i][2]][0]-center[done[i][1]][0]+epsilon)*(display_width-center[done[i][1]][0])
				x_new = center[done[i][1]][0]+(center[done[i][2]][0]-center[done[i][1]][0])/(center[done[i][2]][1]-center[done[i][1]][1]+epsilon)*(display_height-center[done[i][1]][1])
				if x_new<=0 or x_new>=display_width:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[display_width,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[display_width,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[display_width,y_new]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[display_width,y_new]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])
				else:
					if center[done[i][1]][0]>=0 and center[done[i][1]][0]<=display_width and center[done[i][1]][1]>=0 and center[done[i][1]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][1]],[x_new,display_height]),done[i][0][1]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][1],ang(center[done[i][1]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][1]],[x_new,display_height]),done[i][0][0]])
							l.append([dist(center[done[i][1]],[mid1,mid2]),done[i][0][0],ang(center[done[i][1]],[mid1,mid2])])
					elif center[done[i][2]][0]>=0 and center[done[i][2]][0]<=display_width and center[done[i][2]][1]>=0 and center[done[i][2]][1]<=display_height:
						if done[i][0][0]==points[num_play-1]:
							L.append([dist(center[done[i][2]],[x_new,display_height]),done[i][0][1]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][1],ang(center[done[i][2]],[mid1,mid2])])
						else:
							L.append([dist(center[done[i][2]],[x_new,display_height]),done[i][0][0]])
							l.append([dist(center[done[i][2]],[mid1,mid2]),done[i][0][0],ang(center[done[i][2]],[mid1,mid2])])	#finding all L and l values for drawn points
####  We now take all the pairs of points between whom a partition has not already been drawn
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

####  We again repeat the above process for drawing the Voronoi partitions
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

		if 0<=mp[0]<=display_width and 0<=mp[1]<=display_height:
			if theta>=0 and theta<=np.pi/2:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(0-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(0-mp[1])
				if x_new<=0 or x_new>=display_width:
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

					y_n = y_new+(mp[1]-y_new)/(mp[0]-0+epsilon) * (display_width-0)
					x_n = 0+(mp[0]-0)/(mp[1]-y_new+epsilon) * (display_height-y_new)
					if x_n>=0 and x_n<=display_width:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,display_height), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b2])
									l.append([dist([x_n,display_height],[mid1,mid2]),b2,ang([x_n,display_height],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b1])
									l.append([dist([x_n,display_height],[mid1,mid2]),b1,ang([x_n,display_height],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (display_width,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b2])
									l.append([dist([display_width,y_n],[mid1,mid2]),b2,ang([display_width,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b1])
									l.append([dist([display_width,y_n],[mid1,mid2]),b1,ang([display_width,y_n],[mid1,mid2])])

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

					y_n = 0+(mp[1]-0)/(mp[0]-x_new+epsilon) * (display_width-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-0+epsilon) * (display_height-0)
					if x_n>=0 and x_n<=display_width:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,display_height), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b2])
									l.append([dist([x_n,display_height],[mid1,mid2]),b2,ang([x_n,display_height],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b1])
									l.append([dist([x_n,display_height],[mid1,mid2]),b1,ang([x_n,display_height],[mid1,mid2])])

						if flag == 0:
							pass
					else:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (display_width,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b2])
									l.append([dist([display_width,y_n],[mid1,mid2]),b2,ang([display_width,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b1])
									l.append([dist([display_width,y_n],[mid1,mid2]),b1,ang([display_width,y_n],[mid1,mid2])])

						if flag == 0:
							pass
			elif theta>=np.pi/2 and theta<=np.pi:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(display_width-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(0-mp[1])
				if x_new>=0 and x_new<=display_width:
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
					x_n = x_new+(mp[0]-x_new)/(mp[1]-0+epsilon) * (display_height-0)
					if x_n>=0 and x_n<=display_width:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,display_height), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b2])
									l.append([dist([x_n,display_height],[mid1,mid2]),b2,ang([x_n,display_height],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b1])
									l.append([dist([x_n,display_height],[mid1,mid2]),b1,ang([x_n,display_height],[mid1,mid2])])

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
				elif y_new>=0 and y_new<=display_height:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (display_width,y_new), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[display_width,y_new]),b2])
							l.append([dist([display_width,y_new],[mid1,mid2]),b2,ang([display_width,y_new],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[display_width,y_new]),b1])
							l.append([dist([display_width,y_new],[mid1,mid2]),b1,ang([display_width,y_new],[mid1,mid2])])

					y_n = y_new+(mp[1]-y_new)/(mp[0]-display_width+epsilon) * (0-display_width)
					x_n = display_width+(mp[0]-display_width)/(mp[1]-y_new+epsilon) * (display_height-y_new)
					if x_n>=0 and x_n<=display_width:
						for j in range(len(obt)):
							if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
								flag+=1
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (x_n,display_height), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b2])
									l.append([dist([x_n,display_height],[mid1,mid2]),b2,ang([x_n,display_height],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[x_n,display_height]),b1])
									l.append([dist([x_n,display_height],[mid1,mid2]),b1,ang([x_n,display_height],[mid1,mid2])])

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
			elif theta>=3*np.pi/2 and theta<=2*np.pi:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(0-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(display_height-mp[1])
				if x_new>=0 and x_new<=display_width:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (x_new,display_height), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,display_height]),b2])
							l.append([dist([x_new,display_height],[mid1,mid2]),b2,ang([x_new,display_height],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,display_height]),b1])
							l.append([dist([x_new,display_height],[mid1,mid2]),b1,ang([x_new,display_height],[mid1,mid2])])

					y_n = display_height+(mp[1]-display_height)/(mp[0]-x_new+epsilon) * (display_width-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-display_height+epsilon) * (0-display_height)
					if x_n>=0 and x_n<=display_width:
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
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (display_width,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b2])
									l.append([dist([display_width,y_n],[mid1,mid2]),b2,ang([display_width,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b1])
									l.append([dist([display_width,y_n],[mid1,mid2]),b1,ang([display_width,y_n],[mid1,mid2])])

						if flag == 0:
							pass
				elif y_new>=0 and y_new<=display_height:
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

					y_n = y_new+(mp[1]-y_new)/(mp[0]-0+epsilon) * (display_width-0)
					x_n = 0+(mp[0]-0)/(mp[1]-y_new+epsilon) * (0-y_new)
					if x_n>=0 and x_n<=display_width:
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
								pygame.draw.line(gameDisplay, (121,35,218), (mp[0], mp[1]), (display_width,y_n), 3)
								if b1 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b2])
									l.append([dist([display_width,y_n],[mid1,mid2]),b2,ang([display_width,y_n],[mid1,mid2])])
								elif b2 == points[num_play-1]:
									L.append([dist([mp[0],mp[1]],[display_width,y_n]),b1])
									l.append([dist([display_width,y_n],[mid1,mid2]),b1,ang([display_width,y_n],[mid1,mid2])])

						if flag == 0:
							pass
			elif theta>=np.pi and theta<=3*np.pi/2:
				y_new = mp[1]+(mid2-mp[1])/(mid1-mp[0]+epsilon)*(display_width-mp[0])
				x_new = mp[0]+(mid1-mp[0])/(mid2-mp[1]+epsilon)*(display_height-mp[1])
				if x_new<=0 or x_new>=display_width:
					for j in range(len(obt)):
						if (b1 == obt[j][0] and b2 == obt[j][1]) or (b1 == obt[j][1] and b2 == obt[j][0]):
							flag+=1
							pass
					if flag == 0:
						pygame.draw.line(gameDisplay, black, (display_width,y_new), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[display_width,y_new]),b2])
							l.append([dist([display_width,y_new],[mid1,mid2]),b2,ang([display_width,y_new],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[display_width,y_new]),b1])
							l.append([dist([display_width,y_new],[mid1,mid2]),b1,ang([display_width,y_new],[mid1,mid2])])

					y_n = y_new+(mp[1]-y_new)/(mp[0]-display_width+epsilon) * (0-display_width)
					x_n = display_width+(mp[0]-display_width)/(mp[1]-y_new+epsilon) * (0-y_new)
					if x_n>=0 and x_n<=display_width:
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
						pygame.draw.line(gameDisplay, black, (x_new,display_height), (mp[0],mp[1]), 3)
						if b1 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,display_height]),b2])
							l.append([dist([x_new,display_height],[mid1,mid2]),b2,ang([x_new,display_height],[mid1,mid2])])
						elif b2 == points[num_play-1]:
							L.append([dist([mp[0],mp[1]],[x_new,display_height]),b1])
							l.append([dist([x_new,display_height],[mid1,mid2]),b1,ang([x_new,display_height],[mid1,mid2])])

					y_n = display_height+(mp[1]-display_height)/(mp[0]-x_new+epsilon) * (0-x_new)
					x_n = x_new+(mp[0]-x_new)/(mp[1]-display_height+epsilon) * (0-display_height)
					if x_n>=0 and x_n<=display_width:
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
							pass	# for the points not done draw the vornoi based on whether they are obtuse or acute and correspondingly calculate L and l

####  Now that the Voronoi is plotted we start calculating the velocities. v is used to represent the velocity along the line
####  joining the point and the evader and perpendicular to the line. u is used to represent the velocities in the x and y axes
####  This velocity is only for those points which are in the neighbourhood of the evader. For the other points velocity is
####  directly along the line joining them to the evader
	v = np.zeros((len(l),3))
	n = np.zeros(num_play-1)
	num = np.ones(num_play-1)
	for i in range(len(l)):
		pos = num_play+1
		pt = l[i][1]
		for j in range(num_play-1):
			if pt == points[j]:
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

	u = np.zeros((num_play-1,2))
	for i in range(len(v)):
		if (n[int(v[i][2])])!=0:
			u[i][0] = -v[i][0]*cos(ang(points[int(v[i][2])],points[num_play-1]))-v[i][1]*cos(l[i][2])
			u[i][1] = -v[i][0]*sin(ang(points[int(v[i][2])],points[num_play-1]))-v[i][1]*sin(l[i][2])
		else:
			u[i][0] = -v[i][0]*cos(ang(points[int(v[i][2])],points[num_play-1]))
			u[i][1] = -v[i][0]*sin(ang(points[int(v[i][2])],points[num_play-1]))

####  This part contains the direction of rotation in the presence of obstacles
	for i in range(num_play-1):
		flag=0
		c=0
		d=0
		k=0
		for j in range(len(obstacle)):
			obst_ang = ang([obstacle[j][0],obstacle[j][1]],points[int(v[i][2])])
####  If the player is in the vicinity of the obstacle and has a velocity towards it
			if dist(points[int(v[i][2])],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])<=2 or dist([points[int(v[i][2])][0]+u[i][0],points[int(v[i][2])][1]+u[i][1]],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])<=2:
				flag+=1
				print("Touch")
				if epoch==1 or rotation[int(v[i][2])][0] == 0:
					if obst_ang<=np.pi/2:
						x = points[int(v[i][2])][0]-cos(3*np.pi/2+obst_ang)
						y = points[int(v[i][2])][1]-sin(3*np.pi/2+obst_ang)
						if dist([x,y],points[num_play-1])-dist(points[int(v[i][2])],points[num_play-1])<=0:
							c+= -cos(3*np.pi/2+obst_ang)
							d+= -sin(3*np.pi/2+obst_ang)
							rotation[int(v[i][2])][0]=1
							rotation[int(v[i][2])][1]=int(v[i][2])
							rotation[int(v[i][2])][2]=c
							rotation[int(v[i][2])][3]=d
						elif dist([x,y],points[num_play-1])-dist(points[int(v[i][2])],points[num_play-1])>=0:
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
						elif dist([x,y],points[num_play-1])-dist(points[int(v[i][2])],points[num_play-1])>=0:
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
		if flag==0 and dist(points[int(v[i][2])],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])>=5 and dist([points[int(v[i][2])][0]+u[i][0],points[int(v[i][2])][1]+u[i][1]],[obstacle[j][0]-obstacle[j][2]*cos(obst_ang),obstacle[j][1]-obstacle[j][2]*sin(obst_ang)])>=5:
			rotation[int(v[i][2])][0]=0
			rotation[int(v[i][2])][1]=int(v[i][2])
			rotation[int(v[i][2])][2]=10
			rotation[int(v[i][2])][3]=10
	#print(rotation,"ROT")

	for i in range(num_play-1):
		if rotation[int(v[i][2])][0]==1 or rotation[int(v[i][2])][0]==2:
			points[int(v[i][2])][0]+=rotation[int(v[i][2])][2]/sqrt(rotation[int(v[i][2])][2]**2+rotation[int(v[i][2])][3]**2)
			points[int(v[i][2])][1]+=rotation[int(v[i][2])][3]/sqrt(rotation[int(v[i][2])][2]**2+rotation[int(v[i][2])][3]**2)
		else:
			points[int(v[i][2])][0]+=u[i][0]
			points[int(v[i][2])][1]+=u[i][1]


####  Fields for the evader due to pursuers and obstacles
	field_1=0
	field_2=0
	for i in range(len(vor_neigh)):
		field_1+= -(1/dist(vor_neigh[i],points[num_play-1])**2)*cos(ang(vor_neigh[i],points[num_play-1]))
		field_2+= -(1/dist(vor_neigh[i],points[num_play-1])**2)*sin(ang(vor_neigh[i],points[num_play-1]))

	field_1+= -(1/dist([display_width,points[num_play-1][1]],points[num_play-1])**2)*cos(0) -(1/dist([0,points[num_play-1][1]],points[num_play-1])**2)*cos(np.pi)
	field_2+= -(1/dist([points[num_play-1][0],display_height],points[num_play-1])**2)*cos(0) -(1/dist([points[num_play-1][0],0],points[num_play-1])**2)*cos(np.pi)

	for i in range(len(obstacle)):
		obst_ang = ang([obstacle[i][0],obstacle[i][1]],points[num_play-1])
		field_1+= -(1/dist(obstacle[i],points[num_play-1])**2)*cos(obst_ang)
		field_2+= -(1/dist(obstacle[i],points[num_play-1])**2)*sin(obst_ang)

	field_x = field_1/sqrt(field_1**2 + field_2**2)
	field_y = field_2/sqrt(field_1**2 + field_2**2)

	points[num_play-1][0]+=field_x
	points[num_play-1][1]+=field_y

####  Capture of evader
	for i in range(num_play-1):
		if dist(points[i],points[num_play-1])<=10:
			print("CAUGHT")
			crashed = True
			break

	for i in range(num_play-1):
		car(play1,points[i][0],points[i][1])

	car(play2,p5[0],p5[1])
	pygame.display.update()
	clock.tick(20)
	epoch+=1
	print(epoch)
	print("--- %s seconds ---" % (time.time() - start_time))
	#crashed = True
raw_input()
pygame.quit()
quit()
