# -*- coding: utf-8 -*-
"""
figure A2.1
figure pour décrire les coordonnées polaires
"""
import geometrie as gm
from numpy import pi

gm.configure(width=55,height=55,scale=5,fontsize=16)


O = gm.point(-20, -20)
O.label("O",xoff=-3,yoff=-4)
O.delete()
x = gm.ligne(-20, -20, 0, 40)
x.style('V')
x.label("x",xoff=20)
y = gm.ligne(-20, -20, pi/2, 40)
y.style('V')
y.label("y",yoff=20)

r = gm.ligne(-20, -20, pi/6, 35)
r.label("r",yoff=1)

theta = x.angle(r)
theta.style('V')
theta.label("\u03B8",yoff=-2) #theta

M = r.extremite()
M.label('M',yoff=-5)
er = gm.ligne(M.x, M.y, pi/6, 5)
er.style('V')
er.label("e_r",yoff=2)
etheta = gm.ligne(M.x, M.y, 2*pi/3, 5)
etheta.style('V')
etheta.label("e_\u03B8",xoff=-8,yoff=3)

gm.export("../out/A2_1")