# -*- coding: utf-8 -*-
"""
figure A1.2
figure utilisée pour déterminer l'équation cartésienne d'une ellipse
"""

import geometrie as gm

gm.configure(height=100,width=110,scale=5,fontsize=32)

el = gm.ellipse(35, 0, 50, 0.7, 0)
m = el.point(2)
m.label("M")
m.delete()

f1 = el.foyer1()
f2 = el.foyer2()
f1.label("F")
f2.label("F'",xoff=-5,yoff=1)

o = el.centre()
o.label("O",xoff=-2)
g = o.ligne(f2)
g.style("V",scalable=True)
g.label("-ae",xoff=-5,yoff=-10)
p = gm.point(m.x,0)
d = p.ligne(f1)
d.style("V",scalable=True)
d.label("ae-x",xoff=-10,yoff=-10)

x = o.ligne(p)
x.style("V",scalable=True)
x.label("x",xoff=-1)
y = p.ligne(m)
y.style("V",scalable=True)
y.label("y",xoff=-6)

r1=f1.ligne(m)
r2=f2.ligne(m)
r1.label("r")
r2.label("r'",xoff=-2)

gm.export("../out/A1_2")