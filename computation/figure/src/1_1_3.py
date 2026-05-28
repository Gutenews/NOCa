# -*- coding: utf-8 -*-
"""
figure 1.1.3
figure représentant l'argument du périastre dans l'espace
"""

import geometry3D as gm3D
from numpy import pi
from numpy import array

arg=pi/3

gm3D.configure(height=90,width=110,scale=5,fontsize=32,phi=pi+pi/8,delta=-pi/6)

plandefault = gm3D.Plane(gm3D.O3D, -pi/2, pi/2, 0.)
plan2 = gm3D.Plane(gm3D.O3D, -pi/3, pi/6, 0.)

vecx = gm3D.Line2D(plandefault, gm3D.O2D, 30., 0.)
vecz = plandefault.normalVector(30.)
vecn = plan2.normalVector(20.)

vecx.draw()
vecx.label("\u03B3",xoff=-9,yoff=-8) #gamma
vecz.draw()
vecz.style('V')
vecz.label("z",xoff=-4,yoff=12)
vecn.draw()
vecn.style('V')
vecn.label("C",xoff=-10,yoff=4)

el1 = gm3D.Ellipse2D(plan2, gm3D.O2D, 50, 0.7, arg)
el2 = el1.copy()

theta0 = el1.theta2E(-arg)
theta1 = el1.theta2E(pi-arg)
el1.draw(theta0,theta1)
el2.draw(theta1,2*pi+theta0,dash=(5,5))

A0 = gm3D.Point2D(plandefault, array([[40.],[-30.]]))
B0 = gm3D.Point2D(plandefault, array([[40.],[30.]]))
C0 = gm3D.Point2D(plandefault, array([[-45.],[30.]]))
A0.label("eq",xoff=4)
D0 = gm3D.Point2D(plandefault, array([[-45.],[-30.]]))

c01 = A0.line2D(B0)
c02 = B0.line2D(C0)
c03 = C0.line2D(D0)
c04 = D0.line2D(A0)

c01.draw()
c02.draw()
c03.draw()
c04.draw()

l=30.
Ped=el1.theta2Line2D(0.)
Ped.length=l
Ped.draw()
Ped.label("Pe",xoff=-8)
RANd=gm3D.Line2D(plan2, gm3D.O2D, l, 0.)
RANd.draw((5,5))
arc = RANd.angle2D(Ped)
arc.radius=l-5
arc.draw()
arc.style('V')
arc.label("\u03C9",yoff=-5) #omega minuscule

gm3D.export("../out/1_1_3")