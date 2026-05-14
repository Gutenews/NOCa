# -*- coding: utf-8 -*-
"""
figure A1.5
figure illustrant l'anomalie vraie
"""

import geometrie as gm

gm.configure(height=110,width=110,scale=5,fontsize=32)

el = gm.ellipse(35, 0, 50, 0.7, 0)
m = el.point(2)
m.label("M")
m.delete()

f = el.foyer1()
f.label("F",yoff=-9)
f.delete()
o = el.centre()
o.label("O")
o.delete()
xm = gm.point(m.x,o.y)
xm.delete()
cx = o.ligne(xm)
cx.label("x",yoff=-8)
cx.style("V")

ad = gm.angle(xm.x, xm.y, 2, 0, 1)
ad.droit()

vc = xm.ligne(m)
vc.pointille((5,5))
r = f.ligne(m)
r.style("V")
r.label("r")

x = el.point(0)
x.delete()
hz = f.ligne(x)
theta = hz.angle(r)
theta.style("V")
theta.label("θ")

hz2 = xm.ligne(f)
hz2.pointille((5,5))

o2 = o.copie()
o2.translate(0, -10)
o2.delete()
f2 = f.copie()
f2.translate(0, -10)
f2.delete()

cg = o2.ligne(o)
cg.pointille((5,5))
cd = f2.ligne(f)
cd.pointille((5,5))
cf = o2.ligne(f2)
cf.style("D")
cf.label("ae",yoff=-8)

gm.export("../out/A1_5")