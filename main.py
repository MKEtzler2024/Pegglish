import random as R
import turtle as t
import time as T
import math as math

screen= t.Screen()
has_won = False

class ScoreBoard(t.Turtle):
    def __init__(self):
        super().__init__()
        self.color("Red")
        self.penup()
        self.hideturtle()
        self.goto(0,350)
        self.score = 0
        self.update_score()
    def update_score(self):
        self.clear()
        self.write("Score:" + str(self.score), align="center", font=('Arial', 24, 'normal'))
Score = ScoreBoard()


class Projectile(t.Turtle):
    projs = []
    def __init__(self):
        super().__init__()
        self.penup()
        self.goto(0, 400)
        self.shape("circle")
        self.shapesize(2,2)
        self.fillcolor("#202080")
        self.dist = 1
        self.steps = 50000
        Projectile.projs.append(self)
    def destroy_proj(self):
        Projectile.projs.remove(self)
        self.clear()
        self.hideturtle()
    def check_win(self):
        global has_won
        if has_won:
           for square in squares:
               if self.distance(square) < 100:
                   Projectile.destroy_proj(self)
                   Score.score += square.score
                   Score.update_score()


class Orb(t.Turtle):
    orbs = []
    def __init__(self):
        super().__init__()
        rand_x = R.randint(-380, 380)
        rand_y = R.randint(-380, 380)
        self.penup()
        self.goto(rand_x,rand_y)
        self.shape("circle")
        self.shapesize(1,1)
        self.fillcolor("#FF2030")
        self.speed(0)
        Orb.orbs.append(self)
    def Hit_Orb(self):
        self.setheading(-self.towards(orb) + 5)
        Orb.orbs.remove(orb)
        orb.hideturtle()
        Score.score += 10
        Score.update_score()
        if len(Orb.orbs) == 0:
            global has_won
            has_won = True
            Win_screen()
orb = Orb()

def Spawn_orbs():
    orb_min = R.randint(10, 20)
    orb_max = R.randint(21, 30)
    for _ in range(orb_min, orb_max):
        Orb()

def move_projectile(clickX, clickY):
    for proj in Projectile.projs:
        global orb
        global Score
        angle = proj.towards(clickX, clickY)
        proj.setheading(angle)
        for _ in range(proj.steps):
            Projectile.check_win(proj)
            if proj.ycor() > 401:
                proj.setheading((-proj.heading())+5)
            if proj.ycor() <= -415:
                Projectile.destroy_proj(proj)
                return
            proj.forward(proj.dist)
            for orb in Orb.orbs:
                if proj.distance(orb) < 25:
                    Orb.Hit_Orb(proj)
                    print(len(Orb.orbs))
                    break
            if proj.xcor() > 390 or proj.xcor() < -390:
                proj.setheading((180 - proj.heading())+5)

            t.update()


def clicking(x, y):
    if not Projectile.projs:
        Projectile()
        move_projectile(x, y)
class Square(t.Turtle):
    def __init__(self, x, y, color, score):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.shape("square")
        self.shapesize(5, 10)
        self.fillcolor(color)
        self.score = score
        self.goto(x, y)

s1 = Square(-300, -350, "#202020", 100)
s2 = Square(-100, -350, "#302050", 200)
s3 = Square(100, -350, "#408030", 200)
s4 = Square(300, -350, "#204080", 100)

squares = [s1, s2, s3, s4]

def Win_screen():
    for square in squares:
        square.showturtle()



def Start():
    screen.title("Peggle V0.6")
    screen.setup(width=800,height=800)
    screen.bgcolor("#206020")
    screen.tracer(0)
    Spawn_orbs()

Start()
while True:
    screen.onclick(clicking)
    t.update()
    t.done()