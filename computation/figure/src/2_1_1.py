# -*- coding: utf-8 -*-
"""
figure 2.1.1
figure illustrant le repère de manoeuvre dans le plan
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

prograde=el.tangente(r.theta, 10.)
prograde.style('V')
prograde.label("e_p",xoff=-8,yoff=5)
radial=gm.ligne(prograde.x0, prograde.y0, prograde.theta-pi/2, 10.)
radial.style('V')
radial.label("e_e",xoff=5)

gm.export("../out/2_1_1")