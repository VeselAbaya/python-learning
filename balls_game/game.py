import tkinter as tk
import random
from math import sqrt

WIDTH = 640
HEIGHT = 480
BG_COLOR = 'white'
BALL_COLOR = 'blue'
COLORS = ['black', 'violet', 'purple', 'green', 'pink',
          'orange', 'aqua', 'fuchsia', 'yellow', 'gold']
RADIUS = 20
INIT_DX = 1
INIT_DY = 1
DELAY = 8


class Ball:
    def __init__(self, x, y, radius, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.color = color
        self.id = None

    def draw(self):
        self.id = canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                     self.x + self.radius, self.y + self.radius,
                                     fill=self.color, outline=self.color)

    def hide(self):
        canvas.delete(self.id)  # remove instead paint

    def is_collision(self, other):
        a = abs(self.x + self.dx - other.x)
        b = abs(self.y + self.dy - other.y)
        return sqrt(a*a + b*b) <= self.radius + other.radius

    def move(self):
        # colliding with walls
        if (self.x + self.radius + self.dx >= WIDTH) or \
                (self.x - self.radius + self.dx <= 0):
            self.dx = -self.dx
        if (self.y + self.radius + self.dy >= HEIGHT) or \
                (self.y - self.radius + self.dy <= 0):
            self.dy = -self.dy

        # colliding with balls
        for ball in balls:
            if self.is_collision(ball):
                ball.hide()
                balls.remove(ball)
                self.dx = -self.dx
                self.dy = -self.dy

        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


def mouse_click(event):
    global main_ball
    if event.num == 1:
        if 'main_ball' not in globals():
            main_ball = Ball(event.x, event.y, RADIUS, BALL_COLOR, INIT_DX, INIT_DY)
            main_ball.draw()
        else:  # turn_left
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dy = -main_ball.dy
            else:
                main_ball.dx = -main_ball.dx
    elif event.num == 3:  # turn_right
        if main_ball.dx * main_ball.dy > 0:
            main_ball.dx = -main_ball.dx
        else:
            main_ball.dy = -main_ball.dy


def create_Balls(amount):
    balls = [Ball(random.choice(range(WIDTH)),
                  random.choice(range(HEIGHT)),
                  random.choice(range(15, 35)),
                  random.choice(COLORS)) for _ in range(amount)]

    for ball in balls:
        ball.draw()

    return balls


def main():
    if 'main_ball' in globals():
        main_ball.move()
    root.after(DELAY, main)


root = tk.Tk()
root.title('Colliding balls')
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
canvas.pack()
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-3>', mouse_click, '+')
if 'main_ball' in globals():
    del main_ball
balls = create_Balls(10)
main()
root.mainloop()
