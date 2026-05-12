# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:13:10 2026

@author: yanni
"""

import tkinter as tk
import numpy as np

SCALE = 2
WIDTH = 128
HEIGHT = 128
WIDTH = SCALE*WIDTH
HEIGHT = SCALE*HEIGHT

#creation de la fenetre
fenetre = tk.Tk()
zone = tk.Canvas(fenetre, width=WIDTH, height=HEIGHT)
fenetre.resizable(height=False,width=False)

class ligne :
    def __init__(self,x0,y0,theta,d) :
        self.children = []
        self.x0 = x0
        self.y0 = y0
        self.theta = theta
        self.d = d
        self.ID = zone.create_line([WIDTH/2+self.x0*SCALE,                                  #x1
                                    HEIGHT/2-self.y0*SCALE,                                 #y1
                                    WIDTH/2+(self.x0 + np.cos(self.theta)*self.d)*SCALE,    #x2
                                    HEIGHT/2-(self.y0 + np.sin(self.theta)*self.d)*SCALE]) #y2
        self.texte = None
    
    def delete(self) :
        zone.delete(self.ID)
        
    def label(self, texte, xoff=0, yoff=0) :
        if self.texte :
            zone.delete(self.texte)
        self.texte = zone.create_text([WIDTH/2+SCALE*(self.x0+xoff+self.d*np.cos(self.theta)/2),
                                       HEIGHT/2-SCALE*(self.y0+yoff+self.d*np.sin(self.theta)/2)],
                                      text = texte,
                                      anchor=tk.SW)
    
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
        zone.delete(self.ID)
    
    def label(self,texte,xoff=0,yoff=0) :
        if self.texte :
            zone.delete(self.texte)
        self.texte = zone.create_text([WIDTH/2+SCALE*(self.x0+xoff+self.radius*np.cos(self.theta0+self.dtheta/2)),
                                       HEIGHT/2-SCALE*(self.y0+yoff+self.radius*np.sin(self.theta0+self.dtheta/2))],
                                      text=texte,
                                      anchor=tk.SW)

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
        
def affichage() :
    fenetre.mainloop()
    
zone.pack()
fenetre.title("test")
