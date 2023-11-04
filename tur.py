import turtle

turtle.pencolor("red")
turtle.speed(0)

side=int(input("enter side "))
point=int(input("enter point "))


def drstar(side,point):
    stangle= 360/point
    leftangle= 180-(180-(stangle)*2)
    turtle.penup()
    turtle.goto(0,0)
    turtle.pendown()
    print(stangle,leftangle)
    for g in range(point):
        turtle.forward(side)
        turtle.right(stangle)
        turtle.forward(side)
        turtle.left(leftangle)
drstar(side,point)
turtle.mainloop()