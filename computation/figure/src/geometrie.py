# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:13:10 2026

@author: yanni
"""

import tkinter as tk
import numpy as np
from PIL import Image

SCALE = 1
WIDTH = 128
HEIGHT = 128
WIDTH = SCALE*WIDTH
HEIGHT = SCALE*HEIGHT
FONT = "Courier"
FONTSIZE = 12

#creation de la fenetre
fenetre = None
zone = None

def configure(width = 128, height = 128, scale=1, font = "Courier",fontsize=12) :
    global zone, fenetre, WIDTH, HEIGHT, SCALE, FONT, FONTSIZE
    SCALE = scale
    WIDTH = scale*WIDTH
    HEIGHT = scale*HEIGHT
    FONT = font
    FONTSIZE = fontsize
    fenetre = tk.Tk()
    zone = tk.Canvas(fenetre, width=WIDTH, height=HEIGHT)
    fenetre.resizable(height=False,width=False)

class point :
    def __init__(self,x,y,radius=3,scalable=False) :
        self.x = x
        self.y = y
        self.radius = radius
        self.scalable = scalable        
        self.texte = None
        
        self.dessin()
        
    def dessin(self) :
        if self.scalable :
            self.ID1 = zone.create_line([WIDTH/2+SCALE*(self.x+self.radius),
                                         HEIGHT/2-SCALE*(self.y+self.radius),
                                         WIDTH/2+SCALE*(self.x-self.radius-1),
                                         HEIGHT/2-SCALE*(self.y-self.radius-1)],
                                        width = 1)
            
            self.ID2 = zone.create_line([WIDTH/2+SCALE*(self.x-self.radius),
                                         HEIGHT/2-SCALE*(self.y+self.radius),
                                         WIDTH/2+SCALE*(self.x+self.radius+1),
                                         HEIGHT/2-SCALE*(self.y-self.radius-1)])
        else :
            self.ID1 = zone.create_line([WIDTH/2+SCALE*self.x+self.radius,
                                         HEIGHT/2-SCALE*self.y-self.radius,
                                         WIDTH/2+SCALE*self.x-self.radius-1,
                                         HEIGHT/2-SCALE*self.y+self.radius+1],
                                        width = 1)
            
            self.ID2 = zone.create_line([WIDTH/2+SCALE*self.x-self.radius,
                                         HEIGHT/2-SCALE*self.y-self.radius,
                                         WIDTH/2+SCALE*self.x+self.radius+1,
                                         HEIGHT/2-SCALE*self.y+self.radius+1],
                                        width = 1)
            
    def delete(self) :
        if self.ID1 :
            zone.delete(self.ID1)
            zone.delete(self.ID2)
        self.ID1 = None
        self.ID2 = None
        
    def label(self,texte,xoff=0,yoff=0) :
        if self.texte :
            zone.delete(self.texte)
        self.texte = zone.create_text([WIDTH/2+SCALE*(self.x+xoff),
                                       HEIGHT/2-SCALE*(self.y+yoff)],
                                      text = texte,
                                      anchor = tk.SW,
                                      font=(FONT,FONTSIZE))
        
    def copie(self) :
        return point(self.x,self.y,radius=self.radius,scalable=self.scalable)
    
    def translate(self, dx, dy) :
        self.delete()
        self.x += dx
        self.y += dy
        self.dessin()
    
    def ligne(self, point) :
        d = np.sqrt((self.x-point.x)**2+(self.y-point.y)**2)
        theta = np.atan2(point.y-self.y,point.x-self.x)
        return ligne(self.x,self.y,theta,d)

class ligne :
    def __init__(self,x0,y0,theta,d) :
        self.children = []
        self.x0 = x0
        self.y0 = y0
        self.theta = theta
        self.d = d
        self.texte = None
        self.ID = None
        self.dessin()
        
    def dessin(self) :
        if self.ID :
            zone.delete(self.ID)
        self.ID = zone.create_line([WIDTH/2+self.x0*SCALE,                                  
                                    HEIGHT/2-self.y0*SCALE,                                 
                                    WIDTH/2+(self.x0 + np.cos(self.theta)*self.d)*SCALE,    
                                    HEIGHT/2-(self.y0 + np.sin(self.theta)*self.d)*SCALE])  
    
    def pointille(self, schema=None) :
        if self.ID :
            zone.delete(self.ID)
        if schema :
            self.ID = zone.create_line([WIDTH/2+self.x0*SCALE,                                  
                                        HEIGHT/2-self.y0*SCALE,                                 
                                        WIDTH/2+(self.x0 + np.cos(self.theta)*self.d)*SCALE,    
                                        HEIGHT/2-(self.y0 + np.sin(self.theta)*self.d)*SCALE],
                                       dash = SCALE*schema)
        else :
            self.dessin()
    
    def delete(self) :
        for e in self.children :
            e.delete()
            self.children.remove(e)
        zone.delete(self.ID)
        
    def label(self, texte, xoff=0, yoff=0) :
        if self.texte :
            zone.delete(self.texte)
        self.texte = zone.create_text([WIDTH/2+SCALE*(self.x0+xoff+self.d*np.cos(self.theta)/2),
                                       HEIGHT/2-SCALE*(self.y0+yoff+self.d*np.sin(self.theta)/2)],
                                      text = texte,
                                      anchor=tk.SW,
                                      font=(FONT,FONTSIZE))
    
    def style(self, style, scalable=False) :
        for e in self.children :
            e.delete()
            self.children.remove(e)
        if style=='V' :
            p1 = fleche(self.x0+self.d*np.cos(self.theta), self.y0+self.d*np.sin(self.theta), self.theta, scalable=scalable)
            self.children.append(p1)
        elif style=='D' :
            p1 = fleche(self.x0+self.d*np.cos(self.theta), self.y0+self.d*np.sin(self.theta), self.theta, scalable=scalable)
            p2 = fleche(self.x0, self.y0, np.pi+self.theta, scalable=scalable)
            self.children.append(p1)
            self.children.append(p2)
    
    def origine(self) :
        return point(self.x0,self.y0)
    
    def extremite(self) :
        return point(self.x0 + self.radius*np.cos(self.theta),self.y0 + self.radius*np.sin(self.theta))
    
    def cartesien(self) :
        a = np.tan(self.theta)
        b = a*self.x0 + self.y0
        return a,b
    
    def intersection(self,droite) :
        a1,b1 = self.cartesien()
        a2,b2 = droite.cartesien()
        x = (b1-b2)/(a1-a2)
        y = b1-a1*x
        return x,y

    def angle(self,droite,radius = 10) :
        x,y = self.intersection(droite)
        sortie = angle(x,y,radius,self.theta,droite.theta-self.theta)
        return sortie

class angle :
    def __init__(self,x0,y0,radius,theta0,dtheta) :
        self.children = []
        self.x0 = x0
        self.y0 = y0
        self.radius = radius
        self.theta0 = theta0
        self.dtheta = dtheta
        self.ID = zone.create_arc([WIDTH/2+SCALE*(self.x0-self.radius),  #x1
                                   HEIGHT/2-SCALE*(self.y0-self.radius), #y1
                                   WIDTH/2+SCALE*(self.x0+self.radius),  #x2
                                   HEIGHT/2-SCALE*(self.y0+self.radius)],#y2
                                  start=np.rad2deg(self.theta0),
                                  extent=np.rad2deg(self.dtheta),
                                  style=tk.ARC)
        self.texte = None
        
    def delete(self) :
        for e in self.children :
            e.delete()
            self.children.remove(e)
        zone.delete(self.ID)
    
    def label(self,texte,xoff=0,yoff=0) :
        if self.texte :
            zone.delete(self.texte)
        self.texte = zone.create_text([WIDTH/2+SCALE*(self.x0+xoff+self.radius*np.cos(self.theta0+self.dtheta/2)),
                                       HEIGHT/2-SCALE*(self.y0+yoff+self.radius*np.sin(self.theta0+self.dtheta/2))],
                                      text=texte,
                                      anchor=tk.SW,
                                      font=(FONT,FONTSIZE))

    def style(self, style, scalable=False) :
        for e in self.children :
            e.delete()
            self.children.remove(e)
        if style == 'V' :
            p1 = fleche(self.x0+self.radius*np.cos(self.theta0+self.dtheta), 
                        self.y0+self.radius*np.sin(self.theta0+self.dtheta), 
                        self.theta0+self.dtheta+np.pi/2,
                        scalable=scalable)
            self.children.append(p1)
        elif style == 'D' :
            p1 = fleche(self.x0+self.radius*np.cos(self.theta0+self.dtheta), 
                        self.y0+self.radius*np.sin(self.theta0+self.dtheta), 
                        self.theta0+self.dtheta+np.pi/2,
                        scalable=scalable)
            p2 = fleche(self.x0+self.radius*np.cos(self.theta0), 
                        self.y0+self.radius*np.sin(self.theta0), 
                        self.theta0-np.pi/2,
                        scalable=scalable)
            self.children.append(p1)
            self.children.append(p2)
    
    def droit(self) :
        self.delete()
        self.dtheta = np.pi/2
        self.ID = zone.create_line([WIDTH/2+SCALE*(self.x0+np.cos(self.theta0)*self.radius),
                                    HEIGHT/2-SCALE*(self.y0+np.sin(self.theta0)*self.radius),
                                    WIDTH/2+SCALE*(self.x0+(np.cos(self.theta0)+np.cos(self.theta0+self.dtheta))*self.radius),
                                    HEIGHT/2-SCALE*(self.y0+(np.sin(self.theta0)+np.sin(self.theta0+self.dtheta))*self.radius),
                                    WIDTH/2+SCALE*(self.x0+np.cos(self.theta0+self.dtheta)*self.radius),
                                    HEIGHT/2-SCALE*(self.y0+np.sin(self.theta0+self.dtheta)*self.radius)])

class fleche :
    def __init__(self, x0, y0, theta, dtheta=np.pi/3, radius=7, scalable=False) :
        self.x0 = x0
        self.y0 = y0
        self.theta = theta
        self.dtheta = dtheta
        self.scalable = scalable
        self.radius = radius
        if self.scalable :
            self.ID1 = zone.create_line([WIDTH/2+SCALE*self.x0,
                                         HEIGHT/2-SCALE*self.y0,
                                         WIDTH/2+SCALE*(self.x0-self.radius*np.cos(self.theta-self.dtheta/2)),
                                         HEIGHT/2-SCALE*(self.y0-self.radius*np.sin(self.theta-self.dtheta/2))])
            self.ID2 = zone.create_line([WIDTH/2+SCALE*self.x0,
                                         HEIGHT/2-SCALE*self.y0,
                                         WIDTH/2+SCALE*(self.x0-self.radius*np.cos(self.theta+self.dtheta/2)),
                                         HEIGHT/2-SCALE*(self.y0-self.radius*np.sin(self.theta+self.dtheta/2))])
        else :
            self.ID1 = zone.create_line([WIDTH/2+SCALE*self.x0,
                                         HEIGHT/2-SCALE*self.y0,
                                         WIDTH/2+SCALE*self.x0-self.radius*np.cos(self.theta-self.dtheta/2),
                                         HEIGHT/2-SCALE*self.y0+self.radius*np.sin(self.theta-self.dtheta/2)])
            self.ID2 = zone.create_line([WIDTH/2+SCALE*self.x0,
                                         HEIGHT/2-SCALE*self.y0,
                                         WIDTH/2+SCALE*self.x0-self.radius*np.cos(self.theta+self.dtheta/2),
                                         HEIGHT/2-SCALE*self.y0+self.radius*np.sin(self.theta+self.dtheta/2)])
    def delete(self) :
        zone.delete(self.ID1)
        zone.delete(self.ID2)
            

class ellipse :
    def __init__(self,xf,yf,a,e,theta,morceaux=20) :
        self.xf = xf
        self.yf = yf
        self.a = a
        self.e = e
        self.theta = theta
        b = self.a*np.sqrt(1-self.e**2)
        alpha = np.linspace(0, 2*np.pi,int(morceaux*SCALE))
        x0 = self.a*np.cos(alpha)-self.e*self.a
        y0 = b*np.sin(alpha)
        x = WIDTH/2+SCALE*(x0*np.cos(self.theta)-y0*np.sin(theta)+self.xf)
        y = HEIGHT/2-SCALE*(y0*np.cos(self.theta)+x0*np.sin(theta)+self.yf)
        poly = np.ravel([x,y],'F')
        self.ID = zone.create_polygon(poly.tolist(),fill='',outline='black')
        
    def delete(self) :
        zone.delete(self.ID)
        
    def ligne(self, theta) :
        sortie = ligne(self.xf,self.yf,theta+self.theta,self.a*(1-self.e**2)/(1+self.e*np.cos(theta)))
        return sortie
    
    def point(self,theta) :
        r = self.a*(1-self.e**2)/(1+self.e*np.cos(theta))
        x = self.xf + r*np.cos(self.theta+theta)
        y = self.yf + r*np.sin(self.theta+theta)
        return point(x,y)
    
    def foyer1(self) :
        return point(self.xf, self.yf)
    
    def foyer2(self) :
        return point(self.xf-2*self.e*self.a*np.cos(self.theta),self.yf-2*self.e*self.a*np.sin(self.theta))
    
    def centre(self) :
        return point(self.xf-self.a*self.e*np.cos(self.theta),self.yf-self.a*self.e*np.sin(self.theta))
    
    def petitaxe(self) :
        return self.a*np.sqrt(1-self.e**2)
    
    def E2point(self,E):
        centre = self.centre()
        x0 = self.a*np.cos(E)
        y0 = self.petitaxe()*np.sin(E)
        x = x0*np.cos(self.theta)-y0*np.sin(self.theta)
        y = x0*np.sin(self.theta)+y0*np.cos(self.theta)
        centre.translate(x, y)
        return centre
        
def affichage() :    
    zone.pack()
    fenetre.title("test")
    fenetre.mainloop()

def export(chemin) :
    zone.pack()
    zone.update()
    zone.postscript(file=chemin+".ps",pageheight=HEIGHT,pagewidth=WIDTH,colormode='color')
    capture = Image.open(chemin+".ps")
    capture.save(chemin+".png")
    fenetre.mainloop()    