# -*- coding: utf-8 -*-
"""
figure A1.3
figure utilisée pour montrer les longueurs du grand et du petit axe
"""

import geometrie as gm
from numpy import pi

gm.configure(height=100,width=120,scale=5,fontsize=32)

el = gm.ellipse(30, 0, 50, 0.7, 0)

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

h1 = el.E2point(pi/2)
h2 = h1.copie()
h2.translate(55, 0)
b1 = el.E2point(-pi/2)
b2 = b1.copie()
b2.translate(55, 0)

h1.delete()
h2.delete()
b1.delete()
b2.delete()

ch = h1.ligne(h2)
cb = b1.ligne(b2)
b = b2.ligne(h2)

ch.pointille((5,5))
cb.pointille((5,5))
b.style("D")
b.label("2b")

gm.export("../out/A1_3")