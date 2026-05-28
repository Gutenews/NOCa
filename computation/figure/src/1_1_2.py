# -*- coding: utf-8 -*-
"""
Figure 1.1.2
figure représentant l'argument du périastre dans le plan de la trajectoire
"""

import geometrie as gm
from numpy import pi

gm.configure(height=100,width=110,scale=5,fontsize=32)

el = gm.ellipse(35, 0, 50, 0.7, 0)
Pe = el.point(0.)
Pe.delete()
Pe.label("Pe",xoff=-3)
RANd=el.ligne(-pi/3)
RANd.pointille((5,5))
RAN = RANd.extremite()
eqd=el.ligne(RANd.theta+pi)
eqd.pointille((5,5))
eqd.label("eq",xoff=-8,yoff=-8)
RAN.delete()
RAN.label("RAN",xoff=-8,yoff=-8)

Ped=el.ligne(0.)

arg=RANd.angle(Ped,10.)
arg.style('V')
arg.label("\u03C9",yoff=-5) #omega minuscule

gm.export("../out/1_1_2")