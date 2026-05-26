# -*- coding: utf-8 -*-
"""
figure A3.1
figure illustrant le repère sphérique
"""

import geometry3D as gm3D
from numpy import pi
from numpy import array

gm3D.configure(height=84,width=84,scale=7,fontsize=32,phi=pi+pi/8,delta=-pi/6)
rayon = 10.

terre = gm3D.Sphere(array([[20.],[0.],[0.]]), rayon)
terre.draw()
terre.downarc.draw()
plan = terre.plane
O = gm3D.Point2D(plan, gm3D.O2D)

vecx1 = gm3D.Line2D(plan, gm3D.O2D, rayon, 0.)
vecx2 = gm3D.Line2D(plan,array([[rayon],[0.]]), 40.-rayon, 0.)
vecx1.draw((5,5))
vecx2.draw()
vecx2.style('V')
vecx2.label("\u03B3",xoff=-11, yoff=-10) #gamma
vecy1 = gm3D.Line2D(plan, gm3D.O2D, rayon, pi/2)
vecy2 = gm3D.Line2D(plan,array([[0.],[rayon]]), 40.-rayon, pi/2)
vecy1.draw((5,5))
vecy2.draw()
vecy2.style('V')
vecy2.label("y", xoff =12, yoff =-7)
vecz1 = plan.normalVector(rayon)
vecz2 = gm3D.Line3D(plan.origin+array([[0.],[0.],[rayon]]), 40.-rayon, 0., pi/2)
vecz1.draw((5,5))
vecz2.draw()
vecz2.style('V')
vecz2.label("z", xoff=-5, yoff=13)

rotation = gm3D.Angle3D(plan.origin+array([[0.],[0.],[rayon + 10.]]), 0., pi/2, pi, 3*pi/2,radius=5.)
rotation.draw()
rotation.style('V')

r1 = gm3D.Line3D(plan.origin, rayon, pi/3, pi/3)
r2 = gm3D.Line3D(r1.endCoor3D(), 60.-rayon, r1.phi, r1.delta)
r1.draw((5,5))
r2.draw()
r2.label("r",xoff=-3,yoff=-2)
M = r2.endPoint3D()
M.label("M",xoff=2,yoff=-5)

Mproj = plan.pointProjection(M)
Mproj3D = Mproj.point3D()
proj = Mproj3D.line3D(M)
proj.draw((5,5))

rproj2D = O.line2D(Mproj)
rproj2D.draw((5,5))
rproj3D = rproj2D.line3D()

phi = vecx1.angle2D(rproj2D)
phi.radius=28.
phi.draw()
phi.label("\u03D5",yoff=-6) #phi
phi.style('V')

delta = rproj3D.angle(r1)
delta.radius=25.
delta.draw()
delta.style('V')
delta.label("\u03B4") #delta

plan2 = gm3D.Plane(M.origin, r1.phi, r1.delta, 0.)
er=gm3D.Line3D(M.origin, 10., r1.phi, r1.delta)
er.draw()
er.style('V')
er.label("e_r",yoff=5)
ephi=gm3D.Line2D(plan2, gm3D.O2D, 10., 0.)
ephi.draw()
ephi.style('V')
ephi.label("e_\u03D5",xoff=5) #e_phi
edelta=gm3D.Line2D(plan2, gm3D.O2D, 10., pi/2)
edelta.draw()
edelta.style('V')
edelta.label("e_\u03B4",xoff=-12,yoff=3) #e_delta

gm3D.export("../out/A3_1")