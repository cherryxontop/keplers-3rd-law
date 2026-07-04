import argparse
import astropy.units as u
from astropy.constants import G
import numpy as np

#hm now we define variables?

def period_from_semimajor_axis(a: u.Quantity, M: u.Quantity) -> u.Quantity:
    """solve p = 2*pi*sqrt(a^3/G*M))"""
    P = 2*np.pi*(a**3/(G*M))**0.5
    return P.to(u.day)
#apparently u.day coverts whatever messy unit into days. it should throw an error if i make a unit mistake. nice

def semimajor_axis_from_period(P: u.Quantity, M: u.Quantity) -> u.Quantity:
    """solve a = (G*M*P^2/(4*pi^2))^(1/3)"""
    a = (G*M*P**2/(4*np.pi**2))**(1/3)
    return a.to(u.AU)
 
 
def mass_from_period_and_axis(P: u.Quantity, a: u.Quantity) -> u.Quantity:
    """solve M = 4*pi^2*a^3/(G*P^2)"""
    M = 4*np.pi**2*a**3/(G * P**2)
    return M.to(u.M_sun)

def main():
    parser = argparse.ArgumentParser(description="kepler's third law calculator")
    parser.add_argument("--a", type=float, help="semi-major axis in AU")
    parser.add_argument("--P", type=float, help="orital period in days")
    parser.add_argument("--M", type=float, default=1.0, help="mass of central body in M\u2609")    

    args = parser.parse_args() #reads whatever typed in and stores

    M = args.M*u.M_sun #mass of central body in solar masses

    if args.a is not None and args.P is None:
        a = args.a*u.AU 
        P = period_from_semimajor_axis(a, M)
        print(f"semimajor axis: {P} ({P.to(u.yr):.4f})")
        print(f"central mass: {M}")
        print(f"--> semimajor axis: {a:.5f}")

    elif args.P is not None and args.a is None:
        P = args.P*u.day
        a = semimajor_axis_from_period(P, M)
        print(f"orbital period: {P} ({P.to(u.yr):.4f})")
        print(f"central mass: {M}")
        print(f"--> semimajor axis: {a:.5f}")
 
    elif args.a is not None and args.P is not None:
        a = args.a*u.AU
        P = args.P*u.day
        M_solved = mass_from_period_and_axis(P, a)
        print(f"semimajor axis: {a}")
        print(f"orbital period: {P} ({P.to(u.yr):.4f})")
        print(f"--> central mass: {M_solved:.5f} ({M_solved.to(u.kg):.3e})")
 
    else:
        print("provide --a and/or --P (plus optional --M). Examples below.\n")

if __name__ == "__main__":
    main()