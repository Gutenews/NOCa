# -*- coding: utf-8 -*-
"""*
figure A1.1
figure utilisée dans l'annexe pour illustrer une ellipse
"""

import geometrie as gm
from numpy import pi

gm.configure(height=100,width=110,scale=5,fontsize=32)

el = gm.ellipse(35, 0, 50, 0.7, 0)
m = el.point(2)
m.label("M")
m.delete()

f1 = el.foyer1()
f2 = el.foyer2()
f1.label("F")
f2.label("F'",xoff=-2,yoff=1)

e = f2.ligne(f1)
e.label("2ae")

r1=f1.ligne(m)
r2=f2.ligne(m)
r1.label("r")
r2.label("r'",xoff=-2)

g1 = el.point(pi)
g2 = g1.copie()
g2.translate(0,-40)
d1 = el.point(0)
d2 = d1.copie()
d2.translate(0,-40)

g1.delete()
g2.delete()
d1.delete()
d2.delete()

cg=g1.ligne(g2)
cd=d1.ligne(d2)
a=g2.ligne(d2)

cg.pointille((5,5))
cd.pointille((5,5))
a.style("D")
a.label("2a",yoff=-10)

gm.export("../out/A1_1")