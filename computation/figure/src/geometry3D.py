# -*- coding: utf-8 -*-
"""
Created on Mon May 18 17:19:01 2026

@author: yanni
"""

import tkinter as tk
import numpy as np
from PIL import Image

SCALE = 1
PRECISION = 2.**(-15)
WIDTH = 128
HEIGHT = 128
FONT = "Courier"
FONT_SIZE = 12
PHI = 0     #angle de vue de la figure, longitude
DELTA = 0   #angle de vue de la figure, latitude
OMEGA = 0   #angle de vue de la figure, rotation
PROJECTION_MATRIX = np.matrix([[0,1,0],[0,0,1]])
WINDOW = None
CANVAS = None
O2D = np.array([[0.],[0.]])
O3D = np.array([[0.],[0.],[0.]])

def configure(scale=1, precision=2.**(-15), width=128, height=128, font="Courier", fontsize=12, phi=0, delta=0) :
    """
    to configure the settings of geometry3D. Must be called before doing anything with this library

    Parameters
    ----------
    scale : float, optional
        to scale up or scale down the drawing. The default is 1.
    precision : TYPE, optional
        the precision of checks like in intersections, scales automatically with scale. The default is 2.**(-15).
    width : int, optional
        the width of the unscaled drawing. The default is 128.
    height : int, optional
        the height of the unscaled drawing. The default is 128.
    font : string, optional
        the font used for the labels. The default is "Courier".
    fontsize : int, optional
        the size of the font used for the label. The default is 12.
    phi : float, optional
        longitude of where the camera is pointing TO. The default is 0.
    delta : TYPE, optional
        latitude of where the camera is pointing TO. The default is 0.

    Returns
    -------
    None
    """
    
    global SCALE, PRECISION, WIDTH, HEIGHT, FONT, FONT_SIZE, PHI, DELTA, WINDOW, CANVAS, PROJECTION_MATRIX
    SCALE = scale
    PRECISION = precision*scale
    WIDTH = width*scale
    HEIGHT = height*scale
    FONT = font
    FONT_SIZE = fontsize
    PHI = phi
    DELTA = delta
    WINDOW = tk.Tk()
    CANVAS = tk.Canvas(WINDOW,width=WIDTH,height=HEIGHT)
    WINDOW.resizable(height=False,width=False)
    PROJECTION_MATRIX = np.matrix([[np.cos(OMEGA)*np.sin(PHI)-np.sin(OMEGA)*np.cos(PHI)*np.sin(DELTA),
                                    -np.cos(OMEGA)*np.cos(PHI)-np.sin(OMEGA)*np.sin(PHI)*np.sin(DELTA),
                                    np.sin(OMEGA)*np.cos(DELTA)],
                                   [-np.sin(OMEGA)*np.sin(PHI)+np.cos(OMEGA)*np.cos(PHI)*np.sin(DELTA),
                                    np.sin(OMEGA)*np.cos(PHI)+np.cos(OMEGA)*np.sin(PHI)*np.sin(DELTA),
                                    -np.cos(DELTA)*np.cos(OMEGA)]])

def show():
    CANVAS.pack()
    WINDOW.title("geometry 3D")
    WINDOW.mainloop()

def export(chemin) :
    CANVAS.pack()
    CANVAS.update()
    CANVAS.postscript(file=chemin+".ps",pageheight=HEIGHT,pagewidth=WIDTH,colormode='color')
    capture = Image.open(chemin+".ps")
    capture.save(chemin+".png")
    WINDOW.title("geometry 3D")
    WINDOW.after(1, lambda:WINDOW.destroy())
    WINDOW.mainloop()  

def screenProjection(point) :
    return np.array([[WIDTH/2],[HEIGHT/2]]) @ np.ones((1,point.shape[1])) +SCALE*np.dot(PROJECTION_MATRIX,point)

def positionMatrix(phi, delta, omega=0.) :
    positionmatrix = np.matrix([[-np.cos(omega)*np.sin(phi)+np.sin(omega)*np.cos(phi)*np.sin(delta),
                                 np.sin(omega)*np.sin(phi)-np.cos(omega)*np.cos(phi)*np.sin(delta)],
                                [np.cos(omega)*np.cos(phi)+np.sin(omega)*np.sin(phi)*np.sin(delta),
                                 -np.sin(omega)*np.cos(phi)-np.cos(omega)*np.sin(phi)*np.sin(delta)],
                                [-np.sin(omega)*np.cos(delta),
                                 np.cos(omega)*np.cos(delta)]])
    return positionmatrix

def cartesian2Spherical(vec) :
    radius = np.linalg.norm(vec)
    delta = np.arcsin(vec[2,0]/radius)
    phi = np.arctan2(vec[1,0],vec[0,0])
    return radius, phi, delta

def standardisation(phi, delta) :
    resphi = phi
    resdelta = delta
    if delta > np.pi :
        resdelta = np.pi - delta
        resphi = phi + np.pi
    elif delta < -np.pi :
        resdelta = -np.pi + delta
        resphi = phi + np.pi
    resphi = resphi%(2*np.pi)
    return resphi, resdelta        
        

class GeometricObject3D :
    def __init__(self,origin) :
        self.origin = origin
        self.ID = None
        self.lbl = None
    
    def undraw(self) :
        if self.ID :
            CANVAS.delete(self.ID)
        self.ID = None
        
    def label(self, text, xoff=0., yoff=0., aoff=np.array([[0.],[0.],[0.]])) :
        if self.lbl :
            CANVAS.delete(self.lbl)
        pos = SCALE*np.array([[xoff],[-yoff]])+screenProjection(aoff+self.origin)
        self.lbl = CANVAS.create_text(pos.tolist(), text=text,anchor=tk.SW,font=(FONT,FONT_SIZE))

class GeometricObject2D :
    def __init__(self,plane,origin) :
        self.origin = origin
        self.plane = plane
        self.lbl = None
        self.ID = None
        
    def undraw(self) :
        if self.ID :
            CANVAS.delete(self.ID)
        self.ID = None
    
    def label(self,text,xoff=0.,yoff=0.,roff=np.array([[0.],[0.]])) :
        if self.lbl :
            CANVAS.delete(self.lbl)
        pos = SCALE*np.array([[xoff],[-yoff]])+self.plane.screenPosition(self.origin+roff)
        self.lbl = CANVAS.create_text([pos[0,0],pos[1,0]],text=text,anchor=tk.SW,font=(FONT,FONT_SIZE))
    
    def originCoor2D(self):
        return self.origin.copy()
    
    def originCoor3D(self) :
        return self.plane.absolutePosition(self.origin)

class Point3D(GeometricObject3D) :
    def __init__(self, origin, radius=5, scalable=False) :
        super().__init__(origin)
        self.radius = radius/(SCALE**(not scalable))
        self.scalable = scalable
        
    def coord(self) :
        return self.origin.copy()
    
    def line3D(self,point) :
        temp = point.origin - self.origin
        length, phi, delta = cartesian2Spherical(temp)
        return Line3D(self.origin, length, phi, delta)

class Line3D(GeometricObject3D) :
    def __init__(self, origin, length, phi, delta) :
        super().__init__(origin)
        self.length = length
        self.phi = phi
        self.delta = delta
        self.children = []
                
    def endCoor3D(self) :
        return self.origin+self.length*np.array([[np.cos(self.phi)*np.cos(self.delta)],
                                                 [np.sin(self.phi)*np.cos(self.delta)],
                                                 [np.sin(self.delta)]])
    
    def endPoint3D(self) :
        return Point3D(self.endCoor3D())
    
    def draw(self, dash=None) :
        self.undraw()
        start = screenProjection(self.origin)
        end = screenProjection(self.endCoor3D())
        line = np.concat((start,end),axis=1)
        line=np.ravel(line,order='F')
        if dash :
            self.ID = CANVAS.create_line(line.tolist(),dash=SCALE*dash)
        else :
            self.ID = CANVAS.create_line(line.tolist())

    def label(self, text, xoff=0., yoff=0.) :
        pos = self.cartesianVector()/2
        super().label(text,xoff,yoff,pos)

    def style(self, style) :
        for e in self.children :
            e.undraw()
            self.children.remove(e)
        if style=='V' :
            arw1 = Arrow3D(self.endCoor3D(), self.phi, self.delta)
            arw1.draw()
            self.children.append(arw1)
        
    def cartesianVector(self) :
        return self.length*np.array([[np.cos(self.phi)*np.cos(self.delta)],
                                     [np.sin(self.phi)*np.cos(self.delta)],
                                     [np.sin(self.delta)]])

    def crossProduct(self, line3D) :
        vec1 = self.endCoor3D()-self.origin
        vec2 =line3D.endCoor3D()-line3D.origin
        length, phi, delta = cartesian2Spherical(np.linalg.cross(vec1,vec2,axis=0))
        return Line3D(self.origin,length,phi,delta)
    
    def samePlane(self,line3D) :
        return np.dot((self.origin-line3D.origin).T,(self.crossProduct(line3D)).cartesianVector())<PRECISION
    
    def intersectionCoor(self, line3D) :
        if not self.samePlane(line3D) :
            raise Exception("the two vectors are not in the same plane")
        d1 = self.cartesianVector()
        d2 = line3D.cartesianVector()
        
        D1 = np.matrix([[0.,    -d1[2,0],   d1[1,0]],   #pour définir le produit vectoriel car un droite est l'ensemble de point
                        [d1[2,0],0.     ,   -d1[0,0]],  # où le produit vectoriel avec le vecteur directeur reste constant
                        [-d1[1,0], d1[0,0],    0.]])
        D2 = np.matrix([[0.,    -d2[2,0],   d2[1,0]],
                        [d2[2,0],0.     ,   -d2[0,0]],
                        [-d2[1,0], d2[0,0],    0.]])
        c1 = np.dot(D1,self.origin)
        c2 = np.dot(D2,line3D.origin)
        c=np.concat((c1,c2),axis=0)
        D=np.concat((D1,D2),axis=0)
        x = np.linalg.lstsq(D, c)
        
        return x[0]
    
    def angle(self,line3D) :
        if not self.samePlane(line3D) :
            raise Exception("the two vectors are not in the same plane")
        _,phi,delta = cartesian2Spherical(self.crossProduct(line3D).cartesianVector())
        x,y = positionMatrix(phi, delta).T @ self.cartesianVector()
        omega0 = np.atan2(y,x)
        domega = np.acos(np.dot(self.cartesianVector().T,line3D.cartesianVector())
                         /(np.linalg.norm(self.cartesianVector())*np.linalg.norm(line3D.cartesianVector())))
        return Angle3D(self.intersectionCoor(line3D), phi, delta, omega0.item(), domega.item())

class Angle3D(GeometricObject3D):
    def __init__(self, origin, phi, delta, omega0, domega, radius=10., part=5, scalable=True) :
        super().__init__(origin)
        self.phi = phi
        self.delta = delta
        self.omega0 = omega0
        self.domega = domega
        self.radius=radius/(SCALE**(not scalable))
        self.part = part*(SCALE**scalable)
        self.children = []
    
    def startCoor3D(self) :
        return self.origin.copy()
    
    def endCoor3D(self) :
        return self.origin+self.radius*np.dot(positionMatrix(self.phi, self.delta),np.array([[np.cos(self.omega0+self.domega)],[np.sin(self.omega0+self.domega)]]))
    
    def draw(self, dash=None) :
        omega = np.linspace(self.omega0, self.omega0+self.domega,num=self.part)
        circle = np.stack((np.cos(omega),np.sin(omega)),axis=0)
        circle = self.radius*np.matmul(positionMatrix(self.phi, self.delta),circle)
        circle = self.origin @ np.ones((1,circle.shape[1]))+circle
        circle = screenProjection(circle)
        circle = np.ravel(circle,order='F')
        if dash :
            self.ID = CANVAS.create_line(circle.tolist(),dash=SCALE*dash)
        else :
            self.ID = CANVAS.create_line(circle.tolist())
    
    def label(self,text,xoff=0.,yoff=0.):
        pos=self.radius*np.dot(positionMatrix(self.phi, self.delta),np.array([[np.cos(self.omega0+self.domega/2)],[np.sin(self.omega0+self.domega/2)]]))
        super().label(text,xoff,yoff,aoff=pos)
    
    def style(self, style) :
        for e in self.children :
            e.undraw()
            self.children.remove(e)
        if style =='V':
            mat = positionMatrix(self.phi,self.delta)
            n=np.array([[np.cos(self.delta)*np.cos(self.phi)],[np.cos(self.delta)*np.sin(self.phi)],[np.sin(self.delta)]])
            t1=np.dot(mat, np.array([[np.cos(self.omega0+self.domega+np.pi/2)],[np.sin(self.omega0+self.domega+np.pi/2)]]))
            r1=np.linalg.cross(t1, n,axis=0)
            omega1=np.atan2((np.dot(np.array([0.,0.,1.]),n)).item(),(np.dot(np.array([0.,0.,1.]),r1)).item())
            _,phi1,delta1=cartesian2Spherical(t1)
            arw1=Arrow3D(self.endCoor3D(), phi1, delta1,omega1)
            arw1.draw()
            self.children.append(arw1)
        elif style=='D':
            mat = positionMatrix(self.phi,self.delta)
            n=np.array([[np.cos(self.delta)*np.cos(self.phi)],[np.cos(self.delta)*np.sin(self.phi)],[np.sin(self.delta)]])
            t1=np.dot(mat, np.array([[np.cos(self.omega0+self.domega+np.pi/2)],[np.sin(self.omega0+self.domega+np.pi/2)]]))
            r1=np.linalg.cross(t1, n,axis=0)
            omega1=np.atan2((np.dot(np.array([0.,0.,1.]),n)).item(),(np.dot(np.array([0.,0.,1.]),r1)).item())
            _,phi1,delta1=cartesian2Spherical(t1)
            arw1=Arrow3D(self.endCoor3D(), phi1, delta1,omega1)
            arw1.draw()
            self.children.append(arw1)

            t2=np.dot(mat, np.array([[np.cos(self.omega0-np.pi/2)],[np.sin(self.omega0-np.pi/2)]]))
            r2=np.linalg.cross(t2, n,axis=0)
            omega2=np.atan2((np.dot(np.array([0.,0.,1.]),n)).item(),(np.dot(np.array([0.,0.,1.]),r2)).item())
            _,phi2,delta2=cartesian2Spherical(t2)
            arw2=Arrow3D(self.endCoor3D(), phi2, delta2,omega2)
            arw2.draw()
            self.children.append(arw2)

class Arrow3D(GeometricObject3D) :
    def __init__(self, origin, phi, delta, omega=0., dtheta=np.pi/6, radius=7., scalable=False) :
        super().__init__(origin)
        self.phi = phi
        self.delta = delta
        self.omega = omega
        self.dtheta = dtheta
        self.radius = radius/(SCALE**(not scalable))
        self.scalable = False
    
    def draw(self) :
        ddelta = np.asin(np.cos(self.omega)*np.sin(self.dtheta))
        dphi = np.asin(-np.sin(self.omega)*np.sin(self.dtheta))
        phir, deltar = standardisation(self.phi+dphi, self.delta+ddelta)
        phil, deltal = standardisation(self.phi-dphi, self.delta-ddelta)
        left = self.origin - self.radius*np.array([[np.cos(deltal)*np.cos(phil)],[np.cos(deltal)*np.sin(phil)],[np.sin(deltal)]])
        right= self.origin - self.radius*np.array([[np.cos(deltar)*np.cos(phir)],[np.cos(deltar)*np.sin(phir)],[np.sin(deltar)]])
        line = np.concat((left,self.origin,right),axis=1)
        line = screenProjection(line)
        line = np.ravel(line,order='F')
        self.ID = CANVAS.create_line(line.tolist())
        
class Plane(GeometricObject3D) :
    def __init__(self,origin,phi,delta,omega) :
        """
        Create a plane to draw 2D figures on it

        Parameters
        ----------
        origin : numpy float array
            vertical vector representing the absolute coordinates of a point in the plane which will be its origin
        phi : float
            longitude of the normal vector of the plane
        delta : float
            latitude of the normal vector of the plane
        omega : float
            angle rotation (anti-clockwise) of the plane around the normal vector, with omega=0 x is horizontal, y pointing somewhat up. x, y, n is in direct order no matter what
        """
        super().__init__(origin)
        self.phi = phi
        self.delta = delta
        self.omega = omega
        self.positionMatrix()
    
    def positionMatrix(self) :
        self.positionmatrix = positionMatrix(self.phi, self.delta, self.omega)
        return self.positionmatrix.copy()
    
    def absolutePosition(self,point) :
        return self.origin @ np.ones((1,point.shape[1]))+np.dot(self.positionmatrix,point)
    
    def screenPosition(self,point) :
        return screenProjection(self.absolutePosition(point))
    
    def normalVector(self, length) :
        return Line3D(self.origin, length, self.phi, self.delta)
    
    def coorProjection(self, coor) :
        projcoor = np.dot(self.positionmatrix.T,(coor-self.origin))
        return Point2D(self, projcoor)
    
    def pointProjection(self, point) :
        return self.coorProjection(point.origin)

class Sphere(GeometricObject3D):
    def __init__(self, origin, radius, phi=-np.pi/2, delta=np.pi/2) :
        super().__init__(origin)
        self.radius = radius
        self.phi = phi
        self.delta = delta
        self.plane = Plane(self.origin, phi, delta, 0.)
        
        away = Line3D(self.origin, 1., PHI, DELTA)
        _,phi1,delta1 = cartesian2Spherical((self.plane.normalVector(1.).crossProduct(away)).cartesianVector())
        tempvec=Line3D(self.origin, self.radius, phi1, delta1)
        _,phi2,delta2 = cartesian2Spherical((tempvec.crossProduct(away)).cartesianVector())
        tempvec2 = Line3D(self.origin, 1., phi2, delta2)
        
        rivet=tempvec.endPoint3D()
        rivet2D = self.plane.coorProjection(rivet.origin)
        theta = np.atan2(rivet2D.origin[1,0], rivet2D.origin[0,0])
        self.backarc =Angle2D(self.plane, O2D, theta,-np.pi,radius=self.radius)
        self.frontarc=Angle2D(self.plane, O2D, theta, np.pi,radius=self.radius)
        
        temparc=tempvec.angle(tempvec2)
        self.downarc=Angle3D(self.origin, temparc.phi, temparc.delta, temparc.omega0, np.pi, radius=radius)
        self.uparc=Angle3D(self.origin, temparc.phi, temparc.delta, temparc.omega0,-np.pi, radius=radius)
        
    def undraw(self) :
        self.backarc.undraw()
        self.downarc.undraw()
        self.frontarc.undraw()
        self.uparc.undraw()
    
    def draw(self) :
        self.undraw()
        self.backarc.draw((5,5))
        self.downarc.draw((5,5))
        self.uparc.draw()
        self.frontarc.draw()

class Point2D(GeometricObject2D):
    def __init__(self, plane, origin, radius=3, scalable=False) :
        super().__init__(plane, origin)
        self.radius = radius/(SCALE**(not scalable))
        self.scalable = scalable
        
    def point3D(self) :
        return Point3D(self.plane.absolutePosition(self.origin))

    def line2D(self, point) :
        if self.plane != point.plane :
            raise Exception("the two points are not in the same plane, convert them in Point3D and use .line3D")
        temp = point.origin - self.origin
        theta = np.arctan2(temp[1,0],temp[0,0])
        return Line2D(self.plane, self.origin, np.linalg.norm(temp), theta)

class Line2D(GeometricObject2D):
    def __init__(self, plane, origin, length, theta) :
        super().__init__(plane, origin)
        self.length = length
        self.theta = theta
        self.children = []
    
    def draw(self,dash=None):
        self.undraw()
        start = self.plane.screenPosition(self.origin)
        end = self.plane.screenPosition(self.endCoor2D())
        if dash :
            self.ID = CANVAS.create_line([start[0,0],start[1,0],end[0,0],end[1,0]],dash=SCALE*dash)
        else:
            self.ID = CANVAS.create_line([start[0,0],start[1,0],end[0,0],end[1,0]])

    def label(self, text, xoff=0., yoff=0.) :
        pos = self.length*np.array([[np.cos(self.theta)],[np.sin(self.theta)]])/2
        super().label(text,xoff,yoff,pos)
    
    def endCoor2D(self) :
        return self.origin + self.length*np.array([[np.cos(self.theta)],[np.sin(self.theta)]])
    
    def endCoor3D(self) :
        return self.plane.absolutePosition(self.endCoor2D())
    
    def style(self, style) :
        for e in self.children :
            e.undraw()
        if style=='V' :
            arw1 = Arrow2D(self.plane, self.endCoor2D(), self.theta)
            arw1.draw()
            self.children.append(arw1)
        
        elif style=='D' :
            arw1 = Arrow2D(self.plane, self.endCoor2D(), self.theta)
            arw1.draw()
            self.children.append(arw1)
            arw2 = Arrow2D(self.plane, self.endCoor2D(), (self.theta+np.pi)%(2*np.pi))
            arw2.draw()
            self.children.append(arw2)
    
    def intersectionCoor(self, line2D) :
        if self.theta%np.pi==line2D.theta%np.pi :
            raise Exception("the two vectors are colinear")
        A1 = np.array([np.tan(self.theta),-1.])
        A2 = np.array([np.tan(line2D.theta),-1.])
        b1 = (np.dot(A1, self.origin)).item()
        b2 = (np.dot(A2, line2D.origin)).item()
        A = np.stack((A1,A2),axis=0)
        return np.linalg.solve(A, np.array([[b1],[b2]]))
    
    def angle2D(self, line2D) :
        origin = self.intersectionCoor(line2D)
        return Angle2D(self.plane, origin, self.theta, line2D.theta-self.theta)
    
    def line3D(self) :
        origin = Point3D(self.originCoor3D())
        endpoint = Point3D(self.endCoor3D())
        return origin.line3D(endpoint)
    
    def visualIntersection2DCoor(self,line2D) :
        x1 = self.plane.screenPosition(self.origin)/SCALE
        y1 = self.plane.screenPosition(self.endCoor2D())/SCALE
        x2=line2D.plane.screenPosition(line2D.origin)/SCALE
        y2=line2D.plane.screenPosition(line2D.endCoor2D())/SCALE
        
        rot = np.matrix([[0.,1.],[-1.,0.]])
        n1 = np.dot(rot, y1-x1)
        n2 = np.dot(rot, y2-x2)
        N = np.concat((n1.T,n2.T),axis=0)
        
        c1 = (np.dot(n1.T,x1)).item()
        c2 = (np.dot(n2.T,x2)).item()
        visintersect = np.linalg.solve(N, np.array([[c1],[c2]]))
        visintersect -= np.array([[WIDTH/2],[HEIGHT/2]])/SCALE

        coor= np.linalg.solve(PROJECTION_MATRIX @ self.plane.positionmatrix, visintersect-np.dot(PROJECTION_MATRIX, self.plane.origin))

        return Point2D(self.plane, coor)
    
    def IntersectPlanePoint(self,plane) :
        directionvect = self.plane.absolutePosition(self.endCoor2D()-self.origin)
        normalvector = np.array([[np.cos(plane.delta)*np.cos(plane.phi)],
                                 [np.cos(plane.delta)*np.sin(plane.phi)],
                                 [np.sin(plane.delta)]])
        k = np.dot((self.plane.absolutePosition(self.origin)-plane.origin).T,normalvector)
        k1= np.dot(directionvect.T,normalvector)
        return Point2D(self.plane, self.origin-(k.item()/k1.item())*self.length*np.array([[np.cos(self.theta)],[np.sin(self.theta)]]))

class Angle2D(GeometricObject2D) :
    def __init__(self, plane, origin, theta0, dtheta, radius = 10., part=5,scalable=True) :
        super().__init__(plane, origin)
        self.theta0 = theta0
        self.dtheta = dtheta
        self.radius = radius/(SCALE**(not scalable))
        self.part = (SCALE**scalable)*part
        self.children = []
    
    def draw(self, dash=None) :
        self.undraw()
        theta = np.linspace(self.theta0,self.theta0+self.dtheta,num=self.part)
        circle = np.stack((np.cos(theta),np.sin(theta)),axis=0)
        circle = self.plane.screenPosition(self.radius*circle)
        circle = np.ravel(circle, order='F')
        if dash :
            self.ID = CANVAS.create_line(circle.tolist(),dash = SCALE*dash)
        else :
            self.ID = CANVAS.create_line(circle.tolist())
        
    def label(self, text, xoff=0., yoff=0.) :
        pos = self.radius*np.array([[np.cos(self.theta0+self.dtheta/2)],[np.sin(self.theta0+self.dtheta/2)]])
        super().label(text,xoff,yoff,pos)
    
    def startCoor2D(self) :
        return self.origin + self.radius*np.array([[np.cos(self.theta0)],[np.sin(self.theta0)]])
    
    def endCoor2D(self) :
        return self.origin + self.radius*np.array([[np.cos(self.theta0+self.dtheta)],[np.sin(self.theta0+self.dtheta)]])
        
    def style(self, style) :
        for e in self.children :
            e.undraw()
            self.children.remove(e)
        if style=='V':
            arw1 = Arrow2D(self.plane,self.endCoor2D(),self.theta0+self.dtheta+np.pi/2)
            arw1.draw()
            self.children.append(arw1)
        
        elif style=='D' :
            arw1 = Arrow2D(self.plane,self.endCoor2D(),self.theta0+self.dtheta+np.pi/2)
            arw1.draw()
            self.children.append(arw1)
            arw2 = Arrow2D(self.plane,self.endCoor2D(),self.theta0-np.pi/2)
            arw2.draw()
            self.children.append(arw2)

class Arrow2D(GeometricObject2D) :
    def __init__(self, plane, origin, theta0, dtheta=np.pi/6, radius=7., scalable=False) :
        super().__init__(plane, origin)
        self.theta0 = theta0
        self.dtheta = dtheta
        self.scalable = scalable
        self.radius = radius/(SCALE**(not scalable))
    
    def draw(self) :
        left = self.origin + self.radius * np.array([[-np.cos(self.theta0+self.dtheta)],[-np.sin(self.theta0+self.dtheta)]])
        right= self.origin + self.radius * np.array([[-np.cos(self.theta0-self.dtheta)],[-np.sin(self.theta0-self.dtheta)]])
        line = np.concat((left,self.origin,right),axis=1)
        line = self.plane.screenPosition(line)
        line = np.ravel(line, order='F')
        self.ID = CANVAS.create_line(line.tolist())

class Ellipse2D(GeometricObject2D) :
    def __init__(self, plane, origin, a, e, theta0, part=20) :
        super().__init__(plane, origin)
        self.a = a
        self.e = e
        self.theta0 = theta0
        self.part=SCALE*part
    
    def minorAxis(self):
        return self.a*np.sqrt(1-self.e**2)
    
    def E2theta(self,E) :
        return 2*np.atan(np.sqrt((1+self.e)/(1-self.e))*np.tan(E/2))
    
    def theta2E(self, theta) :
        return 2*np.atan(np.sqrt((1-self.e)/(1+self.e))*np.tan(theta/2))
    
    def theta2Length(self, theta) :
        return self.a*(1-self.e**2)/(1+self.e*np.cos(theta))
    
    def theta2Coor2D(self, theta) :
        return self.origin+self.theta2Length(theta)*np.array([[np.cos(self.theta0+theta)],[np.sin(self.theta0+theta)]])
    
    def theta2Point2D(self, theta):
        return Point2D(self.plane, self.theta2Coor2D(theta))
    
    def theta2Line2D(self, theta) :
        return Line2D(self.plane, self.origin, self.theta2Length(theta), theta)
    
    def draw(self,theta0=0., theta1= 2*np.pi, dash=None) :
        self.undraw()
        centre = self.origin-self.a*self.e*np.array([[np.cos(self.theta0)],[np.sin(self.theta0)]])
        theta = np.linspace(theta0, theta1, num=self.part)
        ellipse = np.stack((self.a*np.cos(theta),self.minorAxis()*np.sin(theta)),axis=0)
        rotation = np.matrix([[np.cos(self.theta0),-np.sin(self.theta0)],[np.sin(self.theta0),np.cos(self.theta0)]])
        poly = centre @ np.ones((1,self.part)) + rotation @ ellipse
        poly = self.plane.screenPosition(poly)
        poly = np.ravel(poly, order='F')
        print(poly)
        self.ID = CANVAS.create_line(poly.tolist(), dash=dash)
    
    def copy(self):
        return Ellipse2D(self.plane, self.origin, self.a, self.e, self.theta0)
    
class Rectangle(GeometricObject2D) :
    def __init__(self, plane, origin, theta, length, height) :
        super().__init__(plane, origin)
        self.theta = theta
        self.length = length
        self.height = height
        
    def draw(self,dash=None) :
        self.undraw()
        point0 = self.plane.screenPosition(self.point0Coor2D())
        point1 = self.plane.screenPosition(self.point1Coor2D())
        point2 = self.plane.screenPosition(self.point2Coor2D())
        point3 = self.plane.screenPosition(self.point3Coor2D())
        poly=np.concat((point0,point1,point2,point3,point0),axis=1)
        poly=np.ravel(poly,order='F')        
        if dash :
            self.ID = CANVAS.create_line(poly.tolist(),dash=SCALE*dash)
        else :
            self.ID = CANVAS.create_line(poly.tolist())
    
    def point0Coor2D(self) :
        return self.origin.copy()
    
    def point1Coor2D(self) :
        return self.origin+self.length*np.array([[np.cos(self.theta)],[-np.sin(self.theta)]])
    
    def point2Coor2D(self) :
        return self.point1Coor2D()+self.height*np.array([[np.sin(self.theta)],[np.cos(self.theta)]])
    
    def point3Coor2D(self) :
        return self.origin+self.height*np.array([[np.sin(self.theta)],[np.cos(self.theta)]])