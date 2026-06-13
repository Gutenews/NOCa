# -*- coding: utf-8 -*-
"""
tests for NOCa 0.1
"""

import unittest
import numpy as np

import NOCa

class TestBody(unittest.TestCase):
    
    def test_error_body_init(self) :
        with self.assertRaises(TypeError, msg="Body wrong type radius test 1") :
            NOCa.Body(radius="a",mass=2)
        
        with self.assertRaises(TypeError, msg="Body wrong type mass test 1") :
            NOCa.Body(radius=5, mass="a")
        
        with self.assertRaises(TypeError, msg="Body wrong type mu test 1") :
            NOCa.Body(radius=5, mu="a")
        
        with self.assertRaises(NOCa.NOCaError, msg="Body mu and mass =0 test 1") :
            NOCa.Body(5)
        
        with self.assertRaises(NOCa.NOCaError, msg="Body mu and mass =0 test 2") :
            NOCa.Body(5, mass=0)
        
        with self.assertRaises(NOCa.NOCaError, msg="Body mu and mass =0 test 3") :
            NOCa.Body(5, mu=0)
        
        with self.assertRaises(NOCa.NOCaError, msg="Body negative mass test 1"):
            NOCa.Body(5,mass =-2.5)
        
        with self.assertRaises(NOCa.NOCaError, msg="Body negative mass test 1"):
            NOCa.Body(5,mu =-2.5)

    def test_body_init(self) :
        #Terre
        radius = 6.378137e6
        mass = 5.97217e24
        mu = 3.986004418e14
        
        earth1 = NOCa.Body(radius=radius, mass=mass)
        earth2 = NOCa.Body(radius=radius, mu=mu)
        
        self.assertEqual(radius, earth1.radius, msg="Body radius test 1")
        self.assertEqual(mass, earth1.mass, msg="Body mass test 1")
        self.assertAlmostEqual(mass, earth2.mass, msg="Body mass test 2",delta=6e18)
        self.assertEqual(mu, earth2.mu, msg="Body mu test 1")
        self.assertAlmostEqual(mu, earth1.mu, msg="Body mu test 2",delta=4e8)
    
    def test_body_str(self) :
        radius = 6.378137e6
        mu = 3.986004418e14
        earth = NOCa.Body(radius=radius, mu=mu)
        print(f"Body str test :\n{earth!s}")
    
    def test_body_repr(self) :
        radius = 6.378137e6
        mu = 3.986004418e14
        earth = NOCa.Body(radius=radius, mu=mu)
        print(f"Body repr test :\n{earth!r}")


class TestOrbit(unittest.TestCase) :
    radius = 6.378137e6
    mu = 3.986004418e14
    earth = NOCa.Body(radius=radius, mu=mu)
    
    #Lune
    a=3.84399e8
    eccentricity=0.0549
    inclination=0.0898
    T=2371834.3
    
    #valeur arbitraires
    lRAN = 1.618
    omega = 0.7
    
    
    moon = NOCa.Orbit(earth, inclination, lRAN, a, eccentricity, omega)
    def test_error_orbit_init(self) :
        radius = 6.378137e6
        mu = 3.986004418e14
        earth = NOCa.Body(radius=radius, mu=mu)
        
        #Lune
        a=3.84399e8
        eccentricity=0.0549
        inclination=0.0898
        
        #valeur arbitraires
        lRAN = 1.618
        omega = 0.7
        
        with self.assertRaises(TypeError, msg="Orbit wrong type Body test 1") :
            NOCa.Orbit(3., inclination, lRAN, a, eccentricity, omega)
        
        with self.assertRaises(TypeError, msg="Orbit wrong type inclination test 1") :
            NOCa.Orbit(earth, "a", lRAN, a, eccentricity, omega)
        
        with self.assertRaises(TypeError, msg="Orbit wrong type lRAN test 1") :
            NOCa.Orbit(earth, inclination, "a", a, eccentricity, omega)

        with self.assertRaises(TypeError, msg="Orbit wrong type a test 1") :
            NOCa.Orbit(earth, inclination, lRAN, "a", eccentricity, omega)

        with self.assertRaises(TypeError, msg="Orbit wrong type eccentricity test 1") :
            NOCa.Orbit(earth, inclination, lRAN, a, "a", omega)
        
        with self.assertRaises(TypeError, msg="Orbit wrong type omega test 1") :
            NOCa.Orbit(earth, inclination, lRAN, a, eccentricity, "a")
    
    def test_orbit_init(self) :
        
        self.assertEqual(TestOrbit.earth, TestOrbit.moon.body, msg="Orbit body test 1")
        self.assertEqual(TestOrbit.inclination, TestOrbit.moon.inclination, msg="Orbit inclination test 1")
        self.assertEqual(TestOrbit.lRAN, TestOrbit.moon.lRAN, msg="Orbit lRAN test 1")
        self.assertEqual(TestOrbit.a, TestOrbit.moon.a, msg="Orbit semi major axis test 1")
        self.assertEqual(TestOrbit.eccentricity, TestOrbit.moon.eccentricity, msg="Orbit eccentricity test 1")
        self.assertEqual(TestOrbit.omega, TestOrbit.moon.omega, msg="Orbit omega test 1")
        self.assertAlmostEqual(TestOrbit.T, TestOrbit.moon.T, msg="Orbit period test 1",delta=1e2)
        self.assertAlmostEqual(TestOrbit.moon._c*TestOrbit.T/2, np.pi*np.sqrt(1-TestOrbit.eccentricity**2)*TestOrbit.moon.a**2, msg="Orbit C test 1",delta=1e-6*TestOrbit.moon._c*TestOrbit.T/2)
        temp = TestOrbit.moon._positionMatrix.T@TestOrbit.moon._positionMatrix-np.eye(3)
        self.assertAlmostEqual(0., np.linalg.norm(temp), msg="Orbit _position matrix test 1", delta=1.e-6)
    
    def test_orbit_periapsis(self) :
        self.assertAlmostEqual(TestOrbit.moon.periapsis(), 362600e3, delta=2e7, msg="Orbtit periapsis test 1")
        self.assertAlmostEqual(TestOrbit.moon.periapsis(), TestOrbit.moon.theta2height(0.), msg="Orbtit periapsis test 2")
    
    def test_orbit_apoapsis(self) :
        self.assertAlmostEqual(TestOrbit.moon.apoapsis(), 405400e3, delta=2e7, msg="Orbtit apoapsis test 1")
        self.assertAlmostEqual(TestOrbit.moon.apoapsis(), TestOrbit.moon.theta2height(np.pi), msg="Orbtit apoapsis test 2")
    
    def test_orbit_theta2E(self) :
        self.assertAlmostEqual(0., TestOrbit.moon._theta2E(0.), msg="Orbit _theta2E test 1")
        self.assertAlmostEqual(np.pi, TestOrbit.moon._theta2E(np.pi), msg="Orbit _theta2E test 2")
        theta=[0.,1.7,2.1]
        for i in range(len(theta)) :
            self.assertAlmostEqual(theta[i], TestOrbit.moon._E2theta(TestOrbit.moon._theta2E(theta[i])),msg = f"Orbit _theta2E test {3+i}")
    
    def test_orbit_M2E(self) :
        self.assertAlmostEqual(0., TestOrbit.moon._M2E(0.), msg="Orbit _M2E test 1")
        self.assertAlmostEqual(np.pi, TestOrbit.moon._M2E(np.pi), msg="Orbit _M2E test 2")
        M=[0.,1.7,2.1]
        for i in range(len(M)) :
            self.assertAlmostEqual(M[i], TestOrbit.moon._E2M(TestOrbit.moon._M2E(M[i])),msg = f"Orbit _M2E test {3+i}")
    
    def test_orbit_E2theta(self) :
        self.assertAlmostEqual(0., TestOrbit.moon._E2theta(0.), msg="Orbit _E2theta test 1")
        self.assertAlmostEqual(np.pi, TestOrbit.moon._E2theta(np.pi), msg="Orbit _E2theta test 2")
        E=[0.,1.7,2.1]
        for i in range(len(E)) :
            self.assertAlmostEqual(E[i], TestOrbit.moon._theta2E(TestOrbit.moon._E2theta(E[i])),msg = f"Orbit _E2theta test {3+i}")
    
    def test_orbit_E2M(self) :
        self.assertAlmostEqual(0., TestOrbit.moon._E2M(0.), msg="Orbit _E2M test 1")
        self.assertAlmostEqual(np.pi, TestOrbit.moon._E2M(np.pi), msg="Orbit _E2M test 2")
        E=[0.,1.7,2.1]
        for i in range(len(E)) :
            self.assertAlmostEqual(E[i], TestOrbit.moon._M2E(TestOrbit.moon._E2M(E[i])),msg = f"Orbit _E2M test {3+i}")
    
    def test_orbit_theta2postion(self) :
        with self.assertRaises(TypeError, msg="Orbit theta2position wrong type theta test 1") :
            TestOrbit.moon.theta2position("a")
        
        theta=[0.,1.7,2.1]
        for i in range(3) :
            self.assertAlmostEqual(TestOrbit.moon.theta2height(theta[i]), np.linalg.norm(TestOrbit.moon.theta2position(theta[i])), msg=f"Orbit theta2position test {i+1}", delta=1e-3)
    
    def test_orbit_theta2speedVector(self) :
        with self.assertRaises(TypeError, msg="Orbit theta2position wrong type theta test 1") :
            TestOrbit.moon.theta2speedVector("a")
        
        thetalist = [0.,1.7,2.1]
        self.assertAlmostEqual(0., np.dot(TestOrbit.moon.theta2position(0.).T,TestOrbit.moon.theta2speedVector(0.)).item(), msg="Orbit theta2speedVector test 1", delta=1e-3)
        self.assertAlmostEqual(0., np.dot(TestOrbit.moon.theta2position(np.pi).T,TestOrbit.moon.theta2speedVector(np.pi)).item(), msg="Orbit theta2speedVector test 2", delta=1e-3)
        ref_em = -TestOrbit.moon.body.mu/(2*TestOrbit.moon.a)
        em = [-TestOrbit.moon.body.mu/TestOrbit.moon.theta2height(theta)+0.5*(np.linalg.norm(TestOrbit.moon.theta2speedVector(theta)))**2 for theta in thetalist]
        for i in range(len(thetalist)) :
            self.assertAlmostEqual(ref_em, em[i], msg=f"Orbit theta2speedVector test {3+i}")    
            
    def test_orbit_str(self) :
        print(f"Orbit str test :\n{TestOrbit.moon!s}")

    def test_orbit_repr(self) :
        print(f"Orbit repr test :\n{TestOrbit.moon!r}")
        
class TestSpacecraft(unittest.TestCase) :
    radius = 6.378137e6
    mu = 3.986004418e14
    earth = NOCa.Body(radius=radius, mu=mu)
    
    T = 43082.
    inclination = np.deg2rad(63.4)
    a = ((0.5*T/np.pi)**2*earth.mu)**(1/3)
    e = 0.737
    molniya = NOCa.Orbit(earth, inclination, 1.2, a, e, 3*np.pi/2)
    satellite = NOCa.Spacecraft(molniya,theta0=2.3, T0=-50000.)
    #vérifier le produit scalaire de la vitesse avec le vecteur deltaV lors d'une manoeuvre
    def test_error_spacecraft_init(self) :
        with self.assertRaises(TypeError, msg="Spacecraft wrong type orbit test 1") :
            NOCa.Spacecraft("a")
        
        with self.assertRaises(TypeError, msg="Spacecraft wrong type theta0 test 1") :
            NOCa.Spacecraft(TestSpacecraft.molniya, theta0="a")
        
        with self.assertRaises(TypeError, msg="Spacecraft wrong type E0 test 1") :
            NOCa.Spacecraft(TestSpacecraft.molniya, E0="a")
        
        with self.assertRaises(TypeError, msg="Spacecraft wrong type M0 test 1") :
            NOCa.Spacecraft(TestSpacecraft.molniya, M0="a")
        
        with self.assertRaises(TypeError, msg="Spacecraft wrong type T0 test 1") :
            NOCa.Spacecraft(TestSpacecraft.molniya, T0="a")
    
    def test_spacecraft_init(self) :
        orbit,M0 = TestSpacecraft.satellite._orbits[0]
        self.assertEqual(orbit, TestSpacecraft.molniya, msg="Spacecraft orbit test 1")
        self.assertAlmostEqual(TestSpacecraft.molniya._E2M(TestSpacecraft.molniya._theta2E(2.3)), M0, msg="Spacecraft M0 test 1")
        self.assertEqual(-50000., TestSpacecraft.satellite._time[0])
    
    def test_spacecraft_time2position(self) :
        with self.assertRaises(NOCa.NOCaError, msg="Spacecraft time2position test 1") :
            TestSpacecraft.satellite.time2position(-100000)
        
        t = [-5706.32,11986.,77632.1]
        for i in range(len(t)) :
            temp = TestSpacecraft.satellite.time2position(t[i])-TestSpacecraft.satellite.time2position(t[i]+TestSpacecraft.T)
            self.assertAlmostEqual(0., np.linalg.norm(temp), msg=f"Spacecraft time2position test {2+i}", delta = 1.e-06)
    
    def test_spacecraft_time2speedVector(self) :
        with self.assertRaises(NOCa.NOCaError, msg="Spacecraft time2speedVector test 1") :
            TestSpacecraft.satellite.time2position(-100000)
        
        t = [-5706.32,11986.,77632.1]
        for i in range(len(t)) :
            temp = TestSpacecraft.satellite.time2speedVector(t[i])-TestSpacecraft.satellite.time2speedVector(t[i]+TestSpacecraft.T)
            self.assertAlmostEqual(0., np.linalg.norm(temp), msg=f"Spacecraft time2speedVector test {2+i}", delta = 1.e-06)
            
    def test_spacecraft_addManeuver(self) :
        #manoeuvre de circularisation
        _,M0 = TestSpacecraft.satellite._orbits[0]
        t_ap = TestSpacecraft.T*(150000//TestSpacecraft.T)+(TestSpacecraft.T*(np.pi-M0)/(2*np.pi)+TestSpacecraft.satellite._time[0])
        self.assertAlmostEqual(0., (np.dot(TestSpacecraft.satellite.time2position(t_ap).T,TestSpacecraft.satellite.time2speedVector(t_ap))).item(),
                               delta = 1.e-2, msg="Spacecraft addManeuver test 1")
        r = np.linalg.norm(TestSpacecraft.satellite.time2position(t_ap))
        dv = np.sqrt(TestSpacecraft.molniya.body.mu/r)*(1-np.sqrt(1-TestSpacecraft.e))
        mnv = TestSpacecraft.satellite.addManeuver(np.array([[dv],[0.],[0.]]), t_ap, add=False)
        self.assertAlmostEqual(mnv.orbit.inclination, mnv.postorbit.inclination, msg="Spacecraft test 2")
        self.assertAlmostEqual(mnv.orbit.lRAN, mnv.postorbit.lRAN, msg="Spacecraft test 3")
        self.assertAlmostEqual(0., mnv.postorbit.eccentricity, msg="Spacecraft addManeuver test 4")
        
        #manoeuvre hors-plan
        t_RAN = TestSpacecraft.T*(150000//TestSpacecraft.T)+(TestSpacecraft.T*(TestSpacecraft.molniya._E2M(-TestSpacecraft.molniya._theta2E(TestSpacecraft.molniya.omega))-M0)/(2*np.pi)+TestSpacecraft.satellite._time[0])
        self.assertAlmostEqual(0., TestSpacecraft.satellite.time2position(t_RAN)[2,0], msg="SpaceCraft addManeuver test 5", delta=1.e-6)
        V = TestSpacecraft.satellite.time2speedVector(t_RAN)
        r = np.linalg.norm(TestSpacecraft.satellite.time2position(t_RAN))
        Ci = np.cos(TestSpacecraft.molniya.inclination)
        Si = np.sin(TestSpacecraft.molniya.inclination)
        Co = np.cos(TestSpacecraft.molniya.omega)
        Ne = np.sqrt(TestSpacecraft.molniya.eccentricity**2+2*TestSpacecraft.molniya.eccentricity*Co+1)
        Ce = (1+TestSpacecraft.molniya.eccentricity*Co)/Ne
        Se = TestSpacecraft.molniya.eccentricity*np.sin(TestSpacecraft.molniya.omega)/Ne
        b = TestSpacecraft.molniya._c*(Ci**2)/r+V[2,0]*Si
        dvt= -b + np.sqrt(b**2-V[2,0]**2)
        dvn= -(dvt*Si+V[2,0])/Ci
        mnv = TestSpacecraft.satellite.addManeuver(np.array([[Ce*dvt],[dvn],[Se*dvt]]), t_RAN, add=False)
        self.assertAlmostEqual(mnv.orbit.eccentricity, mnv.postorbit.eccentricity, msg="Spacecraft addManeuver 6")
        self.assertAlmostEqual(mnv.orbit.a, mnv.postorbit.a, msg="Spacecraft addManeuver 7", delta=1.e-6)
        self.assertAlmostEqual(mnv.postorbit.inclination, 0., msg="Spacecraft addManeuver 8", delta=1.e-6)

    def test_spacecraft_str(self):
        temp = TestSpacecraft.satellite.copy()
        #ajout mnv circularisation
        _,M0 = TestSpacecraft.satellite._orbits[0]
        t_ap = TestSpacecraft.T*(150000//TestSpacecraft.T)+(TestSpacecraft.T*(np.pi-M0)/(2*np.pi)+TestSpacecraft.satellite._time[0])
        r = np.linalg.norm(TestSpacecraft.satellite.time2position(t_ap))
        dv = np.sqrt(TestSpacecraft.molniya.body.mu/r)*(1-np.sqrt(1-TestSpacecraft.e))
        temp.addManeuver(np.array([[dv],[0.],[0.]]), t_ap, add=True)
        
        #ajout mnv hors-plan
        orbit, M1=temp._orbits[1]
        t_RAN = orbit.T*(200000//orbit.T)+(orbit.T*(orbit._E2M(-orbit._theta2E(orbit.omega))-M1)/(2*np.pi)+temp._time[1])
        V = temp.time2speedVector(t_RAN)
        r = np.linalg.norm(temp.time2position(t_RAN))
        Ci = np.cos(orbit.inclination)
        Si = np.sin(orbit.inclination)
        Co = np.cos(orbit.omega)
        Ne = np.sqrt(orbit.eccentricity**2+2*orbit.eccentricity*Co+1)
        Ce = (1+orbit.eccentricity*Co)/Ne
        Se = orbit.eccentricity*np.sin(orbit.omega)/Ne
        b = orbit._c*(Ci**2)/r+V[2,0]*Si
        dvt= -b + np.sqrt(b**2-V[2,0]**2)
        dvn= -(dvt*Si+V[2,0])/Ci
        temp.addManeuver(np.array([[Ce*dvt],[dvn],[Se*dvt]]), t_RAN, add=True)
        
        print(f"\nSpacecraft str test :\n{temp!s}")
        
    def test_spacecraft_repr(self) :
        temp = TestSpacecraft.satellite.copy()
        #ajout mnv circularisation
        _,M0 = TestSpacecraft.satellite._orbits[0]
        t_ap = TestSpacecraft.T*(150000//TestSpacecraft.T)+(TestSpacecraft.T*(np.pi-M0)/(2*np.pi)+TestSpacecraft.satellite._time[0])
        r = np.linalg.norm(TestSpacecraft.satellite.time2position(t_ap))
        dv = np.sqrt(TestSpacecraft.molniya.body.mu/r)*(1-np.sqrt(1-TestSpacecraft.e))
        temp.addManeuver(np.array([[dv],[0.],[0.]]), t_ap, add=True)
        
        #ajout mnv hors-plan
        orbit, M1=temp._orbits[1]
        t_RAN = orbit.T*(200000//orbit.T)+(orbit.T*(orbit._E2M(-orbit._theta2E(orbit.omega))-M1)/(2*np.pi)+temp._time[1])
        V = temp.time2speedVector(t_RAN)
        r = np.linalg.norm(temp.time2position(t_RAN))
        Ci = np.cos(orbit.inclination)
        Si = np.sin(orbit.inclination)
        Co = np.cos(orbit.omega)
        Ne = np.sqrt(orbit.eccentricity**2+2*orbit.eccentricity*Co+1)
        Ce = (1+orbit.eccentricity*Co)/Ne
        Se = orbit.eccentricity*np.sin(orbit.omega)/Ne
        b = orbit._c*(Ci**2)/r+V[2,0]*Si
        dvt= -b + np.sqrt(b**2-V[2,0]**2)
        dvn= -(dvt*Si+V[2,0])/Ci
        temp.addManeuver(np.array([[Ce*dvt],[dvn],[Se*dvt]]), t_RAN, add=True)
        
        print(f"\nSpacecraft repr test :\n{temp!r}")

class testManeuver(unittest.TestCase) :
    radius = 6.378137e6
    mu = 3.986004418e14
    earth = NOCa.Body(radius=radius, mu=mu)
    
    T = 43082.
    inclination = np.deg2rad(63.4)
    a = ((0.5*T/np.pi)**2*earth.mu)**(1/3)
    e = 0.737
    molniya = NOCa.Orbit(earth, inclination, 1.2, a, e, 3*np.pi/2)
    
    deltaV = np.array([[500.],[150.],[-80.]])
    time = 43545.
    theta = 1.67
    
    maneuver = NOCa.Maneuver(molniya, deltaV, time, theta=theta)
    def test_error_maneuver_init(self) :
        with self.assertRaises(TypeError, msg="Maneuver wrong type orbit test 1") :
            NOCa.Maneuver("orbit", testManeuver.deltaV, testManeuver.time, theta=testManeuver.theta)
        
        with self.assertRaises(TypeError, msg="Maneuver wrong type deltaV test 1") :
            NOCa.Maneuver(testManeuver.molniya, "a", testManeuver.time, theta=testManeuver.theta)
        
        with self.assertRaises(NOCa.NOCaError, msg="Maneuver wrong type deltaV test 2") :
            NOCa.Maneuver(testManeuver.molniya, np.array([0.]), testManeuver.time, theta=testManeuver.theta)
        
        with self.assertRaises(TypeError, msg="Maneuver wrong type theta test 1") :
            NOCa.Maneuver(testManeuver.molniya, testManeuver.deltaV, testManeuver.time, theta ="a")
        
        with self.assertRaises(TypeError, msg="Maneuver wrong type E test 1") :
            NOCa.Maneuver(testManeuver.molniya, testManeuver.deltaV, testManeuver.time, E="a")
        
        with self.assertRaises(TypeError, msg="Maneuver wrong type M test 1") :
            NOCa.Maneuver(testManeuver.molniya, testManeuver.deltaV, testManeuver.time, M="a")
        
        with self.assertRaises(TypeError, msg="Maneuver wrong type time test 1") :
            NOCa.Maneuver(testManeuver.molniya, testManeuver.deltaV, "a", theta=testManeuver.theta)
        
    def test_maneuver_str(self) :
        print(f"\nManeuver str test :\n{testManeuver.maneuver!s}")
    
    def test_maneuver_repr(self) :
        print(f"\nManeuver repr test :\n{testManeuver.maneuver!r}")
    
    #the other tests are unnecessary with the tests done for SpaceCraft, the same goes for PosSpeed2orbit
unittest.main() 