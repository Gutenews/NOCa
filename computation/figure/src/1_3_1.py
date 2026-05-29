# -*- coding: utf-8 -*-
"""
figure 1.3.1
figure illustrant le repère transitoire pour calculer r(theta) dans le plan
"""

import geometrie as gm
from numpy import pi

gm.configure(height=100,width=110,scale=5,fontsize=32)

el = gm.ellipse(20, 0, 50, 0.7, 0)
r=el.ligne(1.)
r.style('V')
r.label("r",xoff=-3)

RANd=el.ligne(-pi/3)
RANd.pointille((5,5))
RAN = RANd.extremite()
eqd=el.ligne(RANd.theta+pi)
eqd.pointille((5,5))
eqd.label("eq",xoff=-8,yoff=-8)
RAN.delete()
RAN.label("RAN",xoff=-13,yoff=-6)

arg=RANd.angle(r,10.)
arg.style('V')
arg.label("\u03C9+\u03B8",yoff=-3) #omega minuscule + theta minuscule

eRAN=gm.ligne(RAN.x, RAN.y, RANd.theta, 10.)
eRAN.style('V')
eRAN.label("e_RAN",yoff=-10)
ei=gm.ligne(RAN.x, RAN.y, RANd.theta+pi/2, 10.)
ei.style('V')
ei.label("e_i",xoff=7)

#gm.affichage()
gm.export("../out/1_3_1")