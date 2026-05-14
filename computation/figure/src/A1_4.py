# -*- coding: utf-8 -*-
"""
figure A1.4
figure illustrant l'anomalie excentrique
"""

import geometrie as gm
from numpy import pi

gm.configure(height=110,width=110,scale=5,fontsize=32)

el = gm.ellipse(35, 0, 50, 0.7, 0)
o = el.centre()
o.label("O",xoff=-6)
o.delete()
m = el.E2point(1.16)
m.label("M",xoff=2)

ca = gm.ellipse(o.x, o.y, el.a, 0, 0)
cb = gm.ellipse(o.x, o.y, el.petitaxe(), 0, 0)

cam = ca.point(1.16)
cam.delete()
cbm = cb.point(1.16)
cbm.delete()

c = o.ligne(cam)

x = el.point(0)
x.delete()
y = el.E2point(pi/2)
y.delete()

pym = gm.point(o.x,m.y)
pym.delete()
pxm = gm.point(m.x,o.y)
pxm.delete()

cpy = pym.ligne(m)
cpx = pxm.ligne(cam)
cpy.pointille((5,5))
cpx.pointille((5,5))
cx = o.ligne(pxm)
cx.style("V")
cx.label("x",yoff=-8)
cy = o.ligne(pym)
cy.style("V")
cy.label("y",xoff=-4)

hz = pxm.ligne(x)
hz.pointille((5,5))
vc = pym.ligne(y)
vc.pointille((5,5))

E = cx.angle(c,10)
E.label("E")
E.style("V")

b = cb.E2point(-3*pi/4)
a = ca.point(-pi/4)
b.delete()
a.delete()

ca = a.ligne(o)
ca.style("D")
ca.label("a")
cb = b.ligne(o)
cb.style("D")
cb.label("b",xoff=-2)

gm.export("../out/A1_4")