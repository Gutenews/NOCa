# -*- coding: utf-8 -*-
"""
Created on Mon May 11 23:04:17 2026

@author: yanni
"""
import geometrie as gm

#doit tracer une ellipse penchée légèrment dans le sens direct avec un angle entre le segment reliant le point le plus proche du foyer droit et le foyer droit,
#segment nommé r reliant le foyer droit avec un point 2,7 radians dans le sens direct par rapport au premier segment et un arc de cercle nommé theta
#entre ces deux 
#affiche le deuxième foyer de l'ellipse
#trace une ligne entre le deuxième foyer et le point à 2,7 radians
#affiche l'origine avec une étiquette

gm.configure(128,128,5)

el = gm.ellipse(40, 0, 50, 0.7,0.3)
l0 = el.ligne(0)
l1 = el.ligne(2.7)
a1=l0.angle(l1)
a1.label("theta")
a1.style('V')
l1.label("r")
p1 = el.point(2.7)
f2 = el.foyer2()
f2.ligne(p1).style('D')
p1.delete()
(gm.point(0,0)).label("O")

#gm.affichage()
gm.export("./out/testgm")