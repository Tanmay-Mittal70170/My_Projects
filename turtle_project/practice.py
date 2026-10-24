from turtle import *

t= Turtle()
t.speed(0)
for i in range(5):
    t.forward(100)
    t.left(144)

t.penup()
t.forward(350)
t.pendown()

for j in range(80):
    t.forward(j*3)
    t.left(91)
done()