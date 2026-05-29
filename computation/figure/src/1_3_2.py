# -*- coding: utf-8 -*-
"""
figure 1.3.2
figure illustrant le repère transitoire pour calculer r(theta) dans l'espace
"""

import geometry3D as gm3D
from numpy import pi
from numpy import array

arg=pi/3

gm3D.configure(height=90,width=110,scale=5,fontsize=32,phi=pi+pi/8,delta=-pi/6)

plandefault = gm3D.Plane(gm3D.O3D, -pi/2, pi/2, 0.)
plan2 = gm3D.Plane(gm3D.O3D, -pi/3, pi/6, 0.)

vecx = gm3D.Line2D(plandefault, gm3D.O2D, 30., 0.)
vecx.draw()
vecx.label("\u03B3",xoff=-9,yoff=-8) #gamma

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
r=el1.theta2Line2D(1.)
r.draw()
r.style('V')
r.label("r",xoff=-3)
r1=gm3D.Line2D(plan2, r.endCoor2D(), l-r.length, r.theta)
r1.draw((5,5))

RANd=gm3D.Line2D(plan2, gm3D.O2D, l, 0.)
RANd.draw((5,5))
eRAN=gm3D.Line2D(plan2, RANd.endCoor2D(), 10., 0.)
eRAN.draw()
eRAN.style('V')
eRAN.label("e_RAN",yoff=-10,xoff=-10)

Oplandefault=gm3D.Point2D(plandefault, gm3D.O2D)
RAN=plandefault.coorProjection(RANd.endCoor3D())
RANd2D=Oplandefault.line2D(RAN)
Omega=vecx.angle2D(RANd2D)
Omega.radius=20.
Omega.draw()
Omega.style('V')
Omega.label("\u038F",xoff=-3, yoff=-8) #Omega majuscule

ei=gm3D.Line2D(plan2, RANd.endCoor2D(), 10., pi/2)
ei.draw()
ei.style('V')
ei.label("e_i",yoff=5)
eif=gm3D.Point3D(ei.endCoor3D())
eifp=plandefault.pointProjection(eif)
eiproj=RAN.line2D(eifp)
eiproj.length=10.
eiproj.draw((5,5))
ei3D=ei.line3D()
eiproj3D=eiproj.line3D()
i=eiproj3D.angle(ei3D)
i.radius=7.
i.draw()
i.style('V')
i.label("i",yoff=-3)

DNd =gm3D.Line2D(plan2, gm3D.O2D, 45., pi) 
DNd.draw((5,5))
arc = RANd.angle2D(r)
arc.radius=l-7
arc.draw()
arc.style('V')
arc.label("\u03C9+\u03B8",yoff=-5) #omega minuscule+theta minuscule

gm3D.export("../out/1_3_2")