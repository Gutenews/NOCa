# -*- coding: utf-8 -*-
"""
Newtonian Orbital Calculator
A library to compute trajectories and maneuvers for spacecraft orbiting one body
"""

try:
    import numpy as np
except ImportError as exc:
        msg = f"""
        Numpy could not be imported but is mandatory for this librairy.
        Link to the project : https://numpy.org/install/
        
        Original error : {exc}
        """
        raise ImportError(msg) from exc
        
try :
    import fast_kepler as fk
except ImportError as exc :
        msg = f"""
        fast_kepler could not be imported but is mandatory for this librairy.
        Link to the project : https://pypi.org/project/fast-kepler/
        
        Original error : {exc}
        
        """
        raise ImportError(msg) from exc

G=6.67430*10**(-11)

class NOCaError(ValueError):
    """
    Error type used by NOCa library raised by NOCa functions if when a condition
    would prevent correct resolution of the programm
    """

class Body :
    """
    A body to orbit around and have orbits.

    Parameters
    ----------
    radius : float
        the radius of the body
    mass : float, optional
        the mass of the body at least one of mass and mu should be specified. The default is 0..
    mu : float, optional
        the standard gravitation parameter of the body at least one of mass and mu should be specified. The default is 0..

    Returns
    -------
    out : NOCaBody
        A body object with the above specifications
    """
    def __init__(self, radius:float, mass:float=0., mu:float=0.) :
        
        if not isinstance(radius, (float, int)) :
            raise TypeError(f"excpecting radius to be a float recieved {type(radius)} instead")
            
        if not isinstance(mass, (float, int)) :
            raise TypeError(f"excpecting mass to be a float recieved {type(radius)} instead")
        
        if not isinstance(mu, (float, int)) :
            raise TypeError(f"excpecting mu to be a float recieved {type(radius)} instead")
            
        if mass==0. and mu ==0. :
            raise NOCaError("both mu and mass were 0. but at least one should be specified")
        
        if mass<0. :
            raise NOCaError(f"mass should be a positive real number, but {mu} recieved")
        
        if mu<0. :
            raise NOCaError(f"mu should be a positive real number, but {mu} recieved")
            
        self.mu = mu or G*mass
        self.mass=mu/G or mass
        self.radius=radius
    
class Orbit :
    """
    An orbit to be used by spacecrafts.

    Parameters
    ----------
    body : NOCa body
        The body around which the orbit is defined
    inclination : float
        The inclination of the orbit, must be between 0. (included) and pi (included).
    lRAN : float
        The longitude of the Ascending node must be between 0. (included) and 2pi (excluded).
    a : float
        The semi major axis of the orbit must be higher than 0..
    eccentricity : float
        The eccentricity of the orbit must be between 0. (included) and 1. (excluded).
    omega : float
        The argument of the periapsis must be between 0. (included) and 2pi (excluded).

    Returns
    -------
    out : NOCaOrbit
        An orbit object with the above specifications
    """
    def __init__(self, body:Body, inclination:float, lRAN:float, a:float, eccentricity:float, omega:float) :
        
        if not isinstance(body, Body) :
            raise TypeError(f"expecting body to be a NOCa body, recieved {type(body)} instead")
        
        if not isinstance(inclination, (float, int)) :
            raise TypeError(f"expecting inclination to be a float, recieved {type(inclination)} instead")
        
        if not isinstance(lRAN, (float, int)) :
            raise TypeError(f"expecting lRAN to be a float recieved, {type(lRAN)} instead")
        
        if not isinstance(a, (float, int)) :
            raise TypeError(f"expecting a to be a float recieved, {type(a)} instead")
        
        if not isinstance(eccentricity, (float, int)) :
            raise TypeError(f"expecting eccentricity to be a float recieved, {type(eccentricity)} instead")
        
        if not isinstance(omega, (float, int)) :
            raise TypeError(f"expecting omega to be a float recieved, {type(omega)} instead")
        
        if not (inclination>=0. and inclination<=np.pi) :
            raise NOCaError(f"inclination should be between 0. (included) and pi (included), but recieved {inclination} instead")
        
        if not (lRAN>=0. and lRAN<2*np.pi) :
            raise NOCaError(f"inclination should be between 0. (included) and 2 pi (excluded), but recieved {lRAN} instead")
        
        if not a>0. :
            raise NOCaError(f"a should be a positive real number, but recieved {a} instead")
        
        if not (eccentricity>=0. and eccentricity<1.) :
            raise NOCaError(f"eccentricity should be between 0. (included) and 1. (excluded), but recieved {eccentricity} instead")
        
        if not (omega>=0. and omega<2*np.pi) :
            raise NOCaError(f"omega should be between 0. (included) and 2 pi (excluded), but recieved {omega} instead")
        
        self.body = body
        self.inclination=inclination
        self.lRAN=lRAN
        self.a=a
        self.eccentricity=eccentricity
        self.omega=omega

class Spacecraft :
    """
    A spacecraft that moves around a list of orbits.

    Parameters
    ----------
    orbit : Orbit
        the first orbit that the spacecraft uses.
    theta0 : float, optional
        the true anomly of the spacecraft as its beginning, at least one of theta0, E0 and M0 should be specified, between 0. (included) and 2 pi (excluded). The default is 0..
    E0 : float, optional
        the eccentric anomaly of the spacecraft as its beginning, at least one of theta0, E0 and M0 should be specified, between 0. (included) and 2 pi (excluded). The default is 0..
    M0 : float, optional
        the mean anomly of the spacecraft as its beginning, at least one of theta0, E0 and M0 should be specified, between 0. (included) and 2 pi (excluded). The default is 0..
    T0 : float, optional
        The time of its beginning. Before this time the spacecraft does not exist. At T0, the satellite is at the position provided by the other parameters. The default is 0..

    Returns
    -------
    out : NOCaSpacecraft
        A spacecraft object with the above specifications
    """
    def __init__(self, orbit:Orbit, theta0:float=0., E0:float=0., M0:float=0., T0:float=0.):
        if not isinstance(orbit, Orbit) :
            raise TypeError(f"expecting orbit to be a NOCa orbit, recieved {type(orbit)} instead")
        
        if not isinstance(theta0, (float, int)) :
            raise TypeError(f"expecting theta0 to be a float, recieved {type(theta0)} instead")
            
        if not isinstance(E0, (float, int)) :
            raise TypeError(f"expecting E0 to be a float, recieved {type(E0)} instead")
        
        if not isinstance(M0, (float, int)) :
            raise TypeError(f"expecting M0 to be a float, recieved {type(M0)} instead")
        
        if not isinstance(T0, (float, int)) :
            raise TypeError(f"expecting T0 to be a float, recieved {type(T0)} instead")
        
        if not (theta0>=0. and theta0<2*np.pi) :
            raise NOCaError(f"theta0 should be between 0. (included) and 2 pi (excluded), but recieved {theta0} instead")
        
        if not (E0>=0. and E0<2*np.pi) :
            raise NOCaError(f"E0 should be between 0. (included) and 2 pi (excluded), but recieved {E0} instead")
        
        if not (M0>=0. and M0<2*np.pi) :
            raise NOCaError(f"M0 should be between 0. (included) and 2 pi (excluded), but recieved {M0} instead")
        
class Maneuver :
    """
    A maneuver which can be performed by a spacecraft.

    Parameters
    ----------
    orbit : Orbit
        The orbit before the maneuver
    deltaV : np.array
        A vertical vector containing the component of the impulsion vector of the maneuver.
    time : float
        the time at which the maneuver is executed
    theta : float
        The true anomaly where the maneuver takes place, at least one of theta, E and M should be specified, between 0. (included) and 2 pi (excluded). The default is 0..
    E : float
        The eccentric anomaly where the maneuver takes place, at least one of theta, E and M should be specified, between 0. (included) and 2 pi (excluded). The default is 0..
    M : float
        The mean anomaly where the maneuver takes place, at least one of theta, E and M should be specified, between 0. (included) and 2 pi (excluded). The default is 0..
    Returns
    -------
    None
    """
    def __init__(self, orbit:Orbit, deltaV:np.array, time:float, theta:float=0., E:float=0., M:float=0.) :
        if not isinstance(orbit, Orbit) :
            raise TypeError(f"expecting orbit to be a NOCa orbit, recieved {type(orbit)} instead")
        
        if not isinstance(theta, (float, int)) :
            raise TypeError(f"expecting theta0 to be a float, recieved {type(theta)} instead")
            
        if not isinstance(E, (float, int)) :
            raise TypeError(f"expecting E0 to be a float, recieved {type(E)} instead")
        
        if not isinstance(M, (float, int)) :
            raise TypeError(f"expecting M0 to be a float, recieved {type(M)} instead")
        
        if not isinstance(time, (float, int)) :
            raise TypeError(f"expecting T0 to be a float, recieved {type(time)} instead")
        
        if not (theta>=0. and theta<2*np.pi) :
            raise NOCaError(f"theta0 should be between 0. (included) and 2 pi (excluded), but recieved {theta} instead")
        
        if not (E>=0. and E<2*np.pi) :
            raise NOCaError(f"E0 should be between 0. (included) and 2 pi (excluded), but recieved {E} instead")
        
        if not (M>=0. and M<2*np.pi) :
            raise NOCaError(f"M0 should be between 0. (included) and 2 pi (excluded), but recieved {M} instead")
        
        self.orbit = orbit
        self.time = time