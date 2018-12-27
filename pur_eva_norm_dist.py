import numpy as np
from math import *
import turtle
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,



wn = turtle.Screen()
width, height = wn.window_width() / 2, wn.window_height() / 2
print(wn.window_width())
wn.bgcolor("lightgreen") 
tess1 = turtle.Turtle()
tess2 = turtle.Turtle()
tess3 = turtle.Turtle()

tess1.setx(-300)
tess1.sety(-280)

tess2.setx(50)
tess2.sety(100)

tess3.setx(70)
tess3.sety(30)

tess1.color("blue")              # make tess blue
tess1.pensize(3)                 # set the width of her pen


tess2.color("green")              # make tess blue
tess2.pensize(3)

tess3.color("red")              # make tess blue
tess3.pensize(3)

print(height, width)
global a
global b
global c
a1_x = []
b1_x = []
c1_x = []
a1_y = []
b1_y = []
c1_y = []
v = []
a = [-300,-280]
b = [50,100]
c = [70,30]
points = np.ndarray(2)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
	a1_x.append(a[0])
	b1_x.append(b[0])
	c1_x.append(c[0])
	a1_y.append(a[1])
	b1_y.append(b[1])
	c1_y.append(c[1])
	v.append(vor)
	ax1.clear()
	ax1.plot(a1_x,a1_y)
	ax1.plot(b1_x,b1_y)
	ax1.plot(c1_x,c1_y)
phi10 = 0
phi20 = 0
while (1):
	phi1 = atan2((c[1]-a[1]),(c[0]-a[0]))
	phi2 = atan2((c[1]-b[1]),(c[0]-b[0]))
	d1 = sqrt((c[0]-a[0])**2 + (c[1]-a[1])**2)
	d2 = sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2)
	d = d1-d2
	print(d)
	print(phi1)
	print(phi2)
	if c[0]<(width-80) and c[0]>(-width+80) and c[1]<(height-80) and c[1]>(-height+80):
		if d<0:
			phie = phi1
		else:
			phie = phi2
		
		if sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2) < 5 or sqrt((c[0]-a[0])**2 + (c[1]-a[1])**2) < 5:
			print("caught")
			break
		else:
			print("running")
	else:
		print("bound reach")
		if c[0] >= (width-80):
			if (c[1] <= (-height+80) or c[1] >= (height-80)):
				phie=3.34
			else:
				if cos(phie)>0:
					if d>0:
						if phi1>0:
							phie = 1.570796
						else:
							phie = -1.570796
					else:	
						if phi2>0:
							phie = 1.570796
						else:
							phie = -1.570796
		if c[0] <= (-width+80):
			if (c[1] <= (-height+80) or c[1] >= (height-80)):
				phie=0.2
			else:
				if cos(phie)<0:
					if d>0:
						if phi1>0:
							phie = 1.570796
						else:
							phie =-1.570796
					else:	
						if phi2>0:
							phie = 1.570796
						else:
							phie =-1.570796

		
		if c[1] >= (height-80):
			if (c[0] <= (-width+80) or c[0] >= (width-80)):
				phie=-1.370796
				
			else:
				if sin(phie)>0:
					if d>0:
						if phi1>0:
							phie = 3.1417
						else:
							phie = 0
					else:	
						if phi2>0:
							phie = 3.1417
						else:
							phie = 0	
		if c[1] <= (-height+80):
			if (c[0] <= (-width+80) or c[0] >= (width-80)):
				phie=1.70796
			else:
				if sin(phie)<0:
					if d>0:
						if cos(phi1)>0:
							phie = 0
						else:
							phie = 3.1417
					else:	
						if cos(phi2)>0:
							phie = 0
						else:
							phie = 3.1417	
				

		if sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2) < 5 or sqrt((c[0]-a[0])**2 + (c[1]-a[1])**2) < 5:
			print("caught")
			break
		else:
			print("running")
	print(phie)
	a[0] = a[0]+3*cos(phi1)
	a[1] = a[1]+3*sin(phi1)
	b[0] = b[0]+3*cos(phi2)
	b[1] = b[1]+3*sin(phi2)
	c[0] = c[0]+3*cos(phie)
	c[1] = c[1]+3*sin(phie)
	points = a
	points = np.vstack((points,b))
	points = np.vstack((points,c))
	vor = Voronoi(points)
	print(vor.vertices)
	#voronoi_plot_2d(vor, show_vertices=True, line_colors='red',line_width=2, line_alpha=0.6, point_size=5)
	ani = animation.FuncAnimation(fig, animate, blit=True, interval=100)
	plt.show(block=False)
	plt.pause(0.05)
	#plt.show(block=False)
	#plt.pause(0.5)
	#plt.close()
	tess1.left(phi1-phi10)
	tess2.left(phi2-phi20)
	phi10 = phi1
	phi20 = phi2
	tess1.setx(a[0])
	tess1.sety(a[1])
	tess2.setx(b[0])
	tess2.sety(b[1])
	tess3.setx(c[0])
	tess3.sety(c[1])
	#
	
wn.exitonclick() 
#plt.show()
