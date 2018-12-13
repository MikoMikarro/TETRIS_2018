import pygame,sys
from pygame.locals import *
from pygame.draw import line,rect
import random
import time

cells = [10,20]
size = 45
divisor = 2
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (140,140,140)
windowSurface = pygame.display.set_mode(((cells[0]+5)*size,(cells[1]+2)*size))
pygame.display.set_caption("TETRIS 2018")
pygame.font.init()
windowSurface.fill(BLACK)

d_color = {'I':(0,255,255),'O':(255,255,0),'T':(128,0,128),'S':(0,255,0),'Z':(255,0,0),'J':(0,0,255),'L':(255,165,0)}
# 1 - Cyan I
# 2 - Yellow O
# 3 - Purple T
# 4 - Green S
# 5 - Red Z
# 6 - Blue J
# 7 - Orange L

forms = {'J':[(0,1),(1,0),(-1,1),(-1,0),(0,0)],'I':[(.5,.5),(-.5,-.5),(-1.5,-.5),(.5,-.5),(1.5,-.5)],'O':[(.5,-.5),(-.5,-.5),(-.5,.5),(.5,-.5),(.5,.5)],
         'T':[(0,0),(0,-1),(0,0),(-1,0),(1,0)],'S':[(0,0),(0,0),(1,0),(0,1),(-1,1)],'Z':[(0,0),(0,0),(0,1),(-1,0),(1,1)],
         'L':[(0,1),(0,0),(1,0),(-1,0),(1,1)]}

appiled = []
for i in range(cells[0]):
    appiled.append([])
    for l in range(cells[1]):
        appiled[i].append(0)

font = pygame.font.SysFont("waltograph.ttf", 20)
text1 = font.render("Next", True, WHITE)
text2 = font.render("Hold", True, WHITE)



def draw_grid():
    for i in range(1,cells[0]+2):
        line(windowSurface,WHITE,(i*size,size),(i*size,(cells[1]+1)*size))
    for i in range(1,cells[1]+2):
        line(windowSurface,WHITE,(size,i*size),((cells[0]+1)*size,i*size))
    for i in pre_pieza.form:
        rect(windowSurface,pre_pieza.c,(size*(cells[0]+3)+size*i[0]/divisor,(size*(i[1]+4)/divisor),int(float(size+1)/divisor),int((float(size+1)/divisor))))
    if holded_p != None:
        for i in holded_p.form:
            rect(windowSurface,holded_p.c,(size*(cells[0]+3)+size*i[0]/divisor,(size*(i[1]+8)/divisor),int(float(size+1)/divisor),int((float(size+1)/divisor))))
    windowSurface.blit(text1,(size*(cells[0]+3),size))
    windowSurface.blit(text2,(size*(cells[0]+3),size*9/3))

def draw_pieces(p):
    for i in range(cells[0]):
        for l in range(cells[1]):
            if appiled[i][l] != 0:
                rect(windowSurface,GRAY,((i+1)*size,(l+1)*size,size,size))
    for i in p.form:
        if p.y+i[1]>=0:
            rect(windowSurface,p.c,((p.x+1+i[0])*size,(p.y+1+i[1])*size,size,size))

class Pieza():
    def __init__(self,t,x=5, y=0):
        self.t = t
        self.centre = forms[t][0]
        self.x = 5-self.centre[0]
        self.y = 0-self.centre[0]
        self.form = forms[t][1:]
        self.c = d_color[t]
    def left(self):
        m_l = 0
        unable = False
        for i in self.form:
            if i[0]<m_l:
                m_l = i[0]
        for i in self.form:
            if self.x+m_l >0:
                if appiled[int(self.x-1+i[0])][int(self.y+i[1])] != 0:
                    break
            else:
                break
        else:
            self.x-=1
    def right(self):
        m_l = 0
        unable = False
        for i in self.form:
            if i[0]>m_l:
                m_l = i[0]

        for i in self.form:
            if self.x+m_l <9:
                if appiled[int(self.x+1+i[0])][int(self.y+i[1])] != 0:
                    break
            else:
                break
        else:
            self.x+=1

def step(p):
    dead = False
    for i in p.form:
        if i[1]+p.y == cells[1]-1:
            dead = True

        elif appiled[int(p.x+i[0])][int(p.y+1+i[1])] == 1:
            dead = True

    if dead == True:
        for i in p.form:
            appiled[int(p.x+i[0])][int(p.y+i[1])] = 1
        return True
    else:
        p.y+=1
        return False

def check():
    what_to_anihilate = []

    for i in range(cells[1]):
        sum = 0
        for l in range(cells[0]):
            if appiled[l][i] == 1:
                sum+=1
        if sum == 10:
            what_to_anihilate.append(i)
    what_to_anihilate.sort()
    if len(what_to_anihilate) != 0:
        for i in what_to_anihilate:
            for l in range(cells[0]):
                rect(windowSurface,WHITE,((l+1)*size,(i+1)*size,size,size))
        pygame.display.update()
        time.sleep(.15)
    for i in what_to_anihilate:
        for l in range(cells[0]):
            appiled[l].pop(i)
            appiled[l].insert(0,0)

def rotate(p):
    new_form = []
    for i in p.form:
        new_form.append((-i[1],i[0]))

    translate = 0
    for i in new_form:
        if i[0]+p.x<0 and translate == 0:
            translate = 1
        elif i[0]+p.x<-1 :
            translate = 2
        if i[0]+p.x >9 and translate == 0:
            translate = -1
        elif i[0]+p.x >10:
            translate = -2


    for i in new_form:
        if appiled[int(p.x+i[0]+translate)][int(p.y+i[1])] == 1:
            break
    else:
        p.x+=translate
        p.form = new_form

dt =.50
delay = dt
dw_s = 0.075
pygame.init()
t = time.clock()
types = list(d_color.keys())
pre_pieza = Pieza(random.choice(d_color.keys()))
pieza = Pieza(random.choice(types))
t_t = .4
tt =.1
loop = False
holded = True
holded_p = None

while True:
    if time.clock()-t > delay:
        if step(pieza):
            types = list(d_color.keys())
            types.remove(pre_pieza.t)
            pieza = pre_pieza
            pre_pieza = Pieza(random.choice(types))

            time.sleep(0.25)
            holded = True
        t= time.clock()

    draw_pieces(pieza)
    draw_grid()

    for event in pygame.event.get():
        if event == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                 pieza.left()
                 t+=dw_s
                 tc = time.clock()+t_t
            if event.key == pygame.K_RIGHT:
                 pieza.right()
                 t+=dw_s
                 tc = time.clock()+t_t
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP:
                try:
                    rotate(pieza)
                    t+=dw_s
                except IndexError: pass
            if event.key == K_RCTRL and holded:
                holded = False
                if holded_p == None:
                    holded_p = Pieza(pieza.t)
                    types = list(d_color.keys())
                    types.remove(pre_pieza.t)
                    pieza = Pieza(pre_pieza.t)
                    pre_pieza = Pieza(random.choice(types))
                else:
                    c = Pieza(pieza.t)
                    pieza = Pieza(holded_p.t)
                    holded_p = c

    keys = pygame.key.get_pressed()
    if keys[K_DOWN]:
        delay = dw_s
    else:
        delay= dt
    if keys[K_LEFT] and time.clock()-tc > tt:
        tc = time.clock()
        pieza.left()
    if keys[K_RIGHT] and time.clock()-tc > tt:
        tc = time.clock()
        pieza.right()

    check()
    pygame.display.update()
    windowSurface.fill(BLACK)
