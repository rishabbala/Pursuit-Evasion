import numpy
from math import *
import turtle
import time


########    Initial implementation of area based pursuer evader game with turtle sim. Convergence to a single line is observed  ########

 
turtle.setup(400,500)
wn = turtle.Screen() 
wn.title("Handling keypresses!") 
wn.bgcolor("lightgreen")
tess1 = turtle.Turtle()
tess2 = turtle.Turtle()
tess3 = turtle.Turtle() 
 
tess3.speed('slowest')
def h1():
  tess3.forward(0.5)
 
def h2():
 tess3.left(15)
 
def h3():
   tess3.right(15)
 
def h4():
   wn.bye() 

tess1.setx(-100)
tess1.sety(-180)

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

global a
global b
global c
a = [-100,-180]
b = [50,100]
c = [70,30]

phi10 = 0
phi20 = 0
wn.onkey(h1, "Up")
wn.onkey(h2, "Left")
wn.onkey(h3, "Right")
wn.onkey(h4, "q")

while (1):
	wn.listen()
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
				phi1 = 2*(min_a+max_a)/3
				#print("a1")
			else:
				phi1 = atan2((c[1]-a[1]),c[0]-a[0])
		
			
			min_b = max((-1.717-alpha_b),(-1.717-beta_b))
			max_b = min((0-alpha_b),(0-beta_b))
			if min_b < max_b:
				phi2 = 2*(min_b+max_b)/3
				#print("b1")
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
				phi1 = 2*(min_a+max_a)/3
				#print("a1")
			else:
				phi1 = atan2((c[1]-a[1]),c[0]-a[0])
		
			
			min_b = max((-1.717-alpha_b),(-1.717-beta_b))
			max_b = min((0-alpha_b),(0-beta_b))
			if min_b < max_b:
				phi2 = 2*(min_b+max_b)/3
				#print("b1")
			else:
				phi2 = atan2((c[1]-b[1]),c[0]-b[0])
		

	print(phi1)
	print(phi2)
	print((a[0]*b[1]-b[0]*a[1]+b[0]*c[1]-c[0]*b[1]+c[0]*a[1]-a[0]*c[1])/2)
	a[0] = a[0]+cos(phi1)
	a[1] = a[1]+sin(phi1)
	b[0] = b[0]+cos(phi2)
	b[1] = b[1]+sin(phi2)
	c[0] = tess3.xcor()
	c[1] = tess3.ycor()

	tess1.setx(a[0])
	tess1.sety(a[1])
	tess2.setx(b[0])
	tess2.sety(b[1])
	if sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2) < 10 or sqrt((c[0]-a[0])**2 + (c[1]-a[1])**2) < 10:
		print("caught")
		break
	else:
		print("")
	
	print("TURTLE1")
	print(tess1.xcor(),tess1.ycor())
	print("TURTLE2")
	print(tess2.xcor(),tess1.ycor())
	print("TURTLE_e")
	print(tess3.xcor(),tess3.ycor())
	
	#time.sleep(1)
	
	#wn.mainloop()
wn.exitonclick()
