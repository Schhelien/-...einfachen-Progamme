import pygame as pg
from time import time
from random import uniform
from math import sin
from math import cos
from math import pi
pg.init()
r = 120
t0 = time()
dt = 0.01
g = 9.8
mode = 1
dirt = 1
trail = 0
# ------------------------------------------------原理------------------------------------------------


class Point:
    def __init__(self, __angle, __angular_velocity):
        self.angle = __angle
        self.angular_velocity = __angular_velocity

    def pos(self, start_pos):
        x1, y1 = start_pos
        x2 = x1 - r * sin(self.angle)
        y2 = y1 - r * cos(self.angle)
        return x2, y2


point1 = Point(pi / 2, 0)
point2 = Point(pi / 2, 0.1)


def renew1():
    global t0
    point2.angular_velocity += g * dt * sin(point2.angle) / r * dirt
    point1.angular_velocity += g * dt * (
                sin(point1.angle) + cos(point2.angle) * cos(pi / 2 + point1.angle - point2.angle)) / r * dirt
    point1.angle += point1.angular_velocity * dt * dirt
    point2.angle += point2.angular_velocity * dt * dirt
    t0 = time()
# ------------------------------------------------图形------------------------------------------------


win = pg.display.set_mode(size=(500, 500))  # 显示窗口（后简称win）
pg.display.set_caption('作业')  # 设置标题

black = (0, 0, 0)
white = (255, 255, 255)
grey = (64, 64, 64)
ft = pg.font.Font('Songti.ttc', 30)


def speed_txt():
    if dirt == 1:
        a = '>>>'
    else:
        a = '<<<'
    if dt == 0.01:
        b = 'x1'
    else:
        b = 'x10'
    return ''.join([a, b])


def set_text():
    h = 0
    texts = [speed_txt(),
             'point1: ',
             ''.join(['angle=', str(round(point1.angle, 2)), 'rad']),
             ''.join(['angular_velocity=', str(round(point1.angular_velocity, 2)), 'rad/s']),
             '',
             'point2: ',
             ''.join(['angle=', str(round(point2.angle, 2)), 'rad']),
             ''.join(['angular_velocity=', str(round(point2.angular_velocity, 2)), 'rad/s']),
             '',
             'press Space to reset(random)',
             'press Right to accelerate',
             'press Left to back'
             ]
    for text in texts:
        txt = ft.render(text, 1, grey)
        win.blit(txt, (0, h))
        h += 25


pos0 = (250, 250)
pos1 = point1.pos(pos0)
pos2 = point2.pos(pos1)
posed = [pos1, pos2]


def renew2():
    global pos0, pos1, pos2
    win.fill(black)
    pos0 = (250, 250)
    pos1 = point1.pos(pos0)
    pos2 = point2.pos(pos1)
    set_text()
    posed.extend([pos1, pos2])
    for pos in posed:
        pg.draw.circle(win, grey, pos, 1, 1)
    pg.draw.aalines(win, white, False, [pos0, pos1, pos2], 10)
    posed.extend([pos1, pos2])
    for pos in [pos0, pos1, pos2]:
        pg.draw.circle(win, white, pos, 5, 1)


# ------------------------------------------------循环------------------------------------------------
pg_loop = True
while pg_loop:
    event = pg.event.poll()
    if event.type == pg.QUIT:
        pg_loop = False
    if event.dict == {'unicode': ' ', 'key': 32, 'mod': 8192, 'scancode': 44, 'window': None}:
        point1 = Point(pi / 2, uniform(0, 0.1))
        point2 = Point(pi / 2, uniform(0, 0.1))
    elif event.dict == {'unicode': '', 'key': 1073741903, 'mod': 8192, 'scancode': 79, 'window': None}:
        if event.type == 768:
            dt = 0.1
        elif event.type == 769:
            dt = 0.01
    elif event.dict == {'unicode': '', 'key': 1073741904, 'mod': 8192, 'scancode': 80, 'window': None}:
        if event.type == 768:
            dirt = -1
        elif event.type == 769:
            dirt = 1
    renew1()
    renew2()
    pg.display.flip()
