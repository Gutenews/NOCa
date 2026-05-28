# -*- coding: utf-8 -*-
"""
figure 1.2.1
figure pour montrer le calcul de la longitude du noeud ascendant ainsi que de l'inclinaison
"""

import geometry3D as gm3D
from numpy import pi
from numpy import array

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

A0 = gm3D.Point2D(plandefault, array([[40.],[-30.]]))
B0 = gm3D.Point2D(plandefault, array([[40.],[30.]]))
C0 = gm3D.Point2D(plandefault, array([[-30.],[30.]]))
A0.label("eq",xoff=4)
D0 = gm3D.Point2D(plandefault, array([[-30.],[-30.]]))

c01 = A0.line2D(B0)
c02 = B0.line2D(C0)
c03 = C0.line2D(D0)
c04 = D0.line2D(A0)

A1 = gm3D.Point2D(plan2, array([[30.],[-30.]]))
B1 = gm3D.Point2D(plan2, array([[30.],[30.]]))
C1 = gm3D.Point2D(plan2, array([[-30.],[30.]]))
C1.label("st",xoff=1,yoff=-4)
D1 = gm3D.Point2D(plan2, array([[-30.],[-30.]]))

c11 = A1.line2D(B1)
c12 = B1.line2D(C1)
c13 = C1.line2D(D1)
c14 = D1.line2D(A1)

c01.draw()
c02.draw()
c03b = c03.visualIntersection2DCoor(c13)
c03a = c03.visualIntersection2DCoor(c12)
c03d = C0.line2D(c03a)
c03d.draw()
c03m = c03a.line2D(c03b)
c03m.draw((5,5))
c03g = c03b.line2D(D0)
c03g.draw()
c04.draw()

c11a=c11.visualIntersection2DCoor(c01)
c11b=c11.IntersectPlanePoint(plandefault)
c11u=c11b.line2D(B1)
c11m=c11a.line2D(c11b)
c11d=A1.line2D(c11a)
c11u.draw()
c11m.draw((5,5))
c11d.draw()
c12.draw()
c13m = c13.IntersectPlanePoint(plandefault)
c13u = C1.line2D(c13m)
c13u.draw()
c13d = c13m.line2D(D1)
c13d.draw((5,5))
c14m=c14.visualIntersection2DCoor(c01)
c14u=D1.line2D(c14m)
c14d=c14m.line2D(A1)
c14u.draw((5,5))
c14d.draw()

ran = c11b.point3D()
ran.label("RAN",xoff=-5,yoff=-7)
ran0= plandefault.pointProjection(ran)
Oplandefault = gm3D.Point2D(plandefault, gm3D.O2D)
l=Oplandefault.line2D(ran0)
l.draw((5,5))
lRAN = gm3D.Angle2D(plandefault, gm3D.O2D, 0., l.theta)
lRAN.draw()
lRAN.style('V')
lRAN.label("\u038F",xoff=-2,yoff=-7) #Omega majuscule

norm0 = gm3D.Line2D(plandefault, ran0.origin, 10., l.theta+pi/2)
norm0.draw((5,5))
norm=norm0.line3D()
c113D=c11.line3D()
inclinaison = norm.angle(c113D)
inclinaison.draw()
inclinaison.style('V')
inclinaison.label("i")

Oeq=gm3D.Point2D(plandefault, gm3D.O2D)
projC = plandefault.pointProjection(vecn.endPoint3D())
projC3D=projC.point3D()
projcd=Oeq.line2D(projC)
projcd.draw((5,5))
projcd3D=projcd.line3D()
arc = vecz.angle(vecn)
arc.draw()
arc.style('V')
arc.label("i",xoff=-1,yoff=1)
arc2=vecx.angle2D(projcd)
arc2.radius=15.
arc2.draw()
arc2.style('V')
arc2.label("\u038F-\u03C0/2",xoff=-15,yoff=-5) #Omega-pi
arc2.children[0].radius=2.
arc2.children[0].draw()

#gm3D.show()
gm3D.export("../out/1_2_1")