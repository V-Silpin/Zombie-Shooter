import pygame as P
import random as R
import pygame.mouse as M
import pygame.key as K
import math as m

class Player(object):
    def __init__(self, x=400, y=270, h=10000, s=0) -> None:
        self.x=x
        self.y=y
        self.h=h
        self.s=s
        self.a=0
        self.img=P.image.load("Data/player.png").convert_alpha()
        self.img=P.transform.scale_by(self.img,0.25)
        self.img_o=self.img
        self.rect=self.img.get_rect()
    def movement(self, t, p):
        if t:
            self.h-=1
        if p:
            self.s+=1
        if self.x > 30:
            if keys[P.K_LEFT]:
                self.x-=0.05
        if self.x < 770:
            if keys[P.K_RIGHT]:
                self.x+=0.05
        if self.y > 30:
            if keys[P.K_UP]:
                self.y-=0.05
        if self.y < 510:
            if keys[P.K_DOWN]:
                self.y+=0.05
            pass
    def point(self,c_x,c_y):
        a_x=self.x-c_x
        a_y=self.y-c_y
        self.a=90 - m.degrees(m.atan2(a_y,a_x))
        self.img_o =  P.transform.rotate(self.img, q.a)
        self.rect = self.img_o.get_rect(center = (q.x,q.y))  
        pass

class Zombie(object):
    def __init__(self, x=0, y=0, rect=0) -> None:
        self.x=x
        self.y=y
        self.a=0
        self.img=P.image.load("Data/zombie.png")
        self.img=P.transform.scale_by(self.img,0.25)
        self.img_o=self.img
        self.rect=self.img.get_rect()
    def movement(self, rect):
        if self.rect.colliderect(rect):
            self.x=R.randint(0,800)
            self.y=R.randint(0,540)
        self.y+=(m.sin(self.a)/16)
        self.x+=(m.cos(self.a)/16)
    def point(self, p_x, p_y):
        self.a=m.atan2((p_y-self.y),(p_x-self.x))
        self.img_o =  P.transform.rotate(self.img, 270 - m.degrees(self.a))
        self.rect = self.img_o.get_rect(center = (self.x,self.y))  
        pass

class Bullet(object):
    def __init__(self, x=0, y=0) -> None:
        self.x=x
        self.y=y
        self.a=0
        self.p=0
        self.img=P.image.load("Data/bullet.png")
        self.img=P.transform.scale_by(self.img,0.25)
        self.img_o=self.img
        self.rect=self.img.get_rect()
    def movement(self, t):
        if (-10 < self.x < 810) and (-10 < self.y < 550) and self.p:
            if t:
                self.x = -10
                self.y = -10
                self.p=0
            self.y+=(m.sin(self.a)/16)
            self.x+=(m.cos(self.a)/16)
        else:
            self.p=0
    def point(self, c_x, c_y, p_x, p_y):
        if M.get_pressed() == (1,0,0):
            self.x=p_x
            self.y=p_y
            self.a=m.atan2((c_y-self.y),(c_x-self.x))
            self.p=1
        self.img_o =  P.transform.rotate(self.img, 270 - m.degrees(self.a))
        self.rect = self.img_o.get_rect(center = (self.x,self.y))  
        pass

class Border(object):
    def __init__(self, x = 0, y = 0, w = 0, h = 0, R = (255,0,0)) -> None:
        self.rect = P.Rect(x,y,w,h)
        self.R=R
        pass
    def rekah(self, surface,):
        P.draw.rect(surface, self.R, self.rect)
        pass

class Display(object):
    def __init__(self, B = (0,0,0), R = (255,0,0), G = (0,255,0)) -> None:
        self.font_style=P.font.Font('freesansbold.ttf',26)
        self.s_txt="Score  = "
        self.h_txt="Health = "
        self.s_dgt=""
        self.h_dgt=""
        self.B=B
        self.R=R
        self.G=G
        pass
    def show(self, surface, h, s, x = 700, y = 26):
        self.sx_ren=self.font_style.render(self.s_txt,True,self.B)
        self.sx_ren_rect=self.sx_ren.get_rect(center = (600,26))
        self.hx_ren=self.font_style.render(self.h_txt,True,self.B)
        self.hx_ren_rect=self.hx_ren.get_rect(center = (600,56))
        self.sd_ren=self.font_style.render(str(s),True,self.G)
        self.sd_ren_rect=self.sd_ren.get_rect(center = (x,y))
        self.hd_ren=self.font_style.render(str(h),True,self.R)
        self.hd_ren_rect=self.hd_ren.get_rect(center = (700,56))
        surface.blit(self.hx_ren,self.hx_ren_rect)
        surface.blit(self.hd_ren,self.hd_ren_rect)
        surface.blit(self.sx_ren,self.sx_ren_rect)
        surface.blit(self.sd_ren,self.sd_ren_rect)
P.init()
surface=P.display.set_mode((800,540))
fld=P.image.load("Data/field.png")
govr=P.image.load("Data/Score Board.png")
govr_rect=govr.get_rect(center=(400,270))
clock=P.time.Clock()
q=Player()
z=(Zombie(x = R.randint(0,800), y = R.randint(0,540)), Zombie(x = R.randint(0,800), y = R.randint(0,540)), Zombie(x = R.randint(0,800), y = R.randint(0,540)))
b=(Border(x = 0, y = 0, w = 2, h = 800), Border(x = 0, y = 0, w = 800, h = 2),Border(x = 0, y = 538, w = 800, h = 3),Border(x = 797, y = 0, w = 3, h = 540),)
s=Bullet()
d=Display()
loop = True

while loop:
    for event in P.event.get():
        if event.type == P.QUIT:
            loop=False
    pos=M.get_pos()
    keys=K.get_pressed()
    if q.h > 0:
        q.point(pos[0],pos[1])
        s.point(pos[0],pos[1],q.x,q.y)
        surface.blit(fld,(0,0))
        if s.p:
            surface.blit(s.img_o,s.rect)
        for i in range(len(z)):
            z[i].point(q.x,q.y)
            z[i].movement(s.rect)
            s.movement(z[i].rect.colliderect(s.rect))
            q.movement(q.rect.colliderect(z[i].rect),z[i].rect.colliderect(s.rect))
        surface.blit(q.img_o,q.rect)
        for i in range(len(z)):
            surface.blit(z[i].img_o,z[i].rect)
        for i in range(len(b)):
            b[i].rekah(surface)
        d.show(surface,q.h,q.s,x = 700,y = 26)
    if q.h <= 0:
        surface.fill((0,0,0))
        surface.blit(govr,govr_rect)
        d.show(surface,q.h,q.s,x = 400,y = 270)
    if keys[P.K_ESCAPE]:
        loop=False
    P.display.update()
    clock.tick(1500)
P.quit()