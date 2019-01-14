import turtle

wn = turtle.Screen()
wn.bgcolor("lightgreen")        # set the window background color


########    Basic implementation of tutrle sim in python    ########


tess1 = turtle.Turtle()
tess2 = turtle.Turtle()
tess3 = turtle.Turtle()

tess1.setx(0)
tess1.sety(0)

tess2.setx(30)
tess2.sety(0)

tess3.setx(30)
tess3.sety(40)

tess1.color("blue")              # make tess blue
tess1.pensize(3)                 # set the width of her pen


tess2.color("green")              # make tess blue
tess2.pensize(3)

tess3.color("red")              # make tess blue
tess3.pensize(3)



tess1.forward(50)
tess2.left(120)
tess2.left(180)
tess3.forward(50)

wn.exitonclick()                # wait for a user click on the canvas

