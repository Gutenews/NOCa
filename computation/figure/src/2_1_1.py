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

Ped=el.ligne(0.)
Ped.pointille((5,5))
Pe = Ped.extremite()
Pe.delete()
Pe.label("Pe",xoff=1,yoff=-4)

arg=Ped.angle(r,10.)
arg.style('V')
arg.label("\u03B8",yoff=-2) #theta minuscule

prograde=el.tangente(r.theta, 10.)
prograde.style('V')
prograde.label("e_p",xoff=-8,yoff=5)
radial=gm.ligne(prograde.x0, prograde.y0, prograde.theta-pi/2, 10.)
radial.style('V')
radial.label("e_e",xoff=5)

gm.export("../out/2_1_1")