import numpy
from math import *
import turtle

wn = turtle.Screen() #320 x ** 280 y
wn.bgcolor("lightgreen") 
tess1 = turtle.Turtle()
tess2 = turtle.Turtle()
tess3 = turtle.Turtle()

global a
global b
global c
a = [0,80]
b = [80,-150]
c = [125,-54]

tess1.setx(a[0])
tess1.sety(a[1])

tess2.setx(b[0])
tess2.sety(b[1])

tess3.setx(c[0])
tess3.sety(c[1])

tess1.color("blue")              # make tess blue
tess1.pensize(3)                 # set the width of her pen


tess2.color("green")              # make tess blue
tess2.pensize(3)

tess3.color("red")              # make tess blue
tess3.pensize(3)

phi10 = 0
phi20 = 0
while (1):
	if -1 < ((c[1]-b[1])/(c[0]-b[0])-(a[1]-b[1])/(a[0]-b[0])) < 1:
		phi1 = atan2((c[1]-a[1]),c[0]-a[0])
		phi2 = atan2((c[1]-b[1]),c[0]-b[0])
		print("SL")
		print(((c[1]-b[1])/(c[0]-b[0])-(a[1]-b[1])/(a[0]-b[0])))
	else:
		if (a[0]*b[1]-b[0]*a[1]+b[0]*c[1]-c[0]*b[1]+c[0]*a[1]-a[0]*c[1])/2 > 1:
			alpha_a = atan2((a[0]-c[0]),(a[1]-c[1]))
			beta_a = atan2((b[1]-c[1]),(c[0]-b[0]))
			alpha_b = atan2((b[0]-c[0]),(b[1]-c[1]))
			beta_b = atan2((c[1]-a[1]),(a[0]-c[0]))

			min_a = max((-1.717-alpha_a),(-1.717-beta_a))
			max_a = min((0-alpha_a),(0-beta_a))
			if min_a < max_a:
				phi1 = (min_a+max_a)/2
				print("a1")
			else:
				phi1 = atan2((c[1]-a[1]),c[0]-a[0])
		
			
			min_b = max((-1.717-alpha_b),(-1.717-beta_b))
			max_b = min((0-alpha_b),(0-beta_b))
			if min_b < max_b:
				phi2 = (min_b+max_b)/2
				print("b1")
			else:
				phi2 = atan2((c[1]-b[1]),c[0]-b[0])
	
		else:
			alpha_a = atan2((a[0]-c[0]),(a[1]-c[1]))
			beta_a = atan2((c[1]-b[1]),(b[0]-c[0]))
			alpha_b = atan2((b[0]-c[0]),(b[1]-c[1]))
			beta_b = atan2((a[1]-c[1]),(c[0]-a[0]))
		
			min_a = max((-1.717-alpha_a),(-1.717-beta_a))
			max_a = min((0-alpha_a),(0-beta_a))
			if min_a < max_a:
				phi1 = (min_a+max_a)/2
				print("a2")
			else:
				phi1 = atan2((c[1]-a[1]),c[0]-a[0])
		
			
			min_b = max((-1.717-alpha_b),(-1.717-beta_b))
			max_b = min((0-alpha_b),(0-beta_b))
			if min_b < max_b:
				phi2 = (min_b+max_b)/2
				print("b2")
			else:
				phi2 = atan2((c[1]-b[1]),c[0]-b[0])
		
	psi1 = atan2((c[1]-a[1]),c[0]-a[0])
	psi2 = atan2((c[1]-b[1]),c[0]-b[0])
	d1 = sqrt((c[0]-a[0])**2 + (c[1]-a[1])**2)
	d2 = sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2)
	if d1<d2:
		phie = psi1
	else:
		phie = psi2

	#phie = 3.141
	print(phi1)
	print(phi2)
	print((a[0]*b[1]-b[0]*a[1]+b[0]*c[1]-c[0]*b[1]+c[0]*a[1]-a[0]*c[1])/2)
	a[0] = a[0]+3*cos(phi1)
	a[1] = a[1]+3*sin(phi1)
	b[0] = b[0]+3*cos(phi2)
	b[1] = b[1]+3*sin(phi2)
	c[0] = c[0]+3*cos(phie)
	c[1] = c[1]+3*sin(phie)

	if sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2) < 10 or sqrt((c[0]-a[0])**2 + (c[1]-a[1])**2) < 10:
		print("caught")
		break
	else:
		print("")
	tess1.left(phi1-phi10)
	tess2.left(phi2-phi20)
	tess3.left(phi2-phi20)
	phi10 = phi1
	phi20 = phi2
	tess1.setx(a[0])
	tess1.sety(a[1])
	tess2.setx(b[0])
	tess2.sety(b[1])
	tess3.setx(c[0])
	tess3.sety(c[1])
wn.exitonclick() 
