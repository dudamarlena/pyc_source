# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\library\airfoils.py
# Compiled at: 2020-04-18 12:03:13
# Size of source mod 2**32: 3521 bytes
from aerosandbox.geometry import *
from aerosandbox.library.aerodynamics import *
generic_cambered_airfoil = Airfoil(name='Generic Cambered Airfoil',
  coordinates=None,
  CL_function=(lambda alpha, Re, mach, deflection: alpha * np.pi / 180 * (2 * np.pi) + 0.455),
  CDp_function=(lambda alpha, Re, mach, deflection: (1 + (alpha / 5) ** 2) * 2 * Cf_flat_plate(Re_L=Re)),
  Cm_function=(lambda alpha, Re, mach, deflection: -0.1))
generic_airfoil = Airfoil(name='Generic Airfoil',
  coordinates=None,
  CL_function=(lambda alpha, Re, mach, deflection: alpha * np.pi / 180 * (2 * np.pi)),
  CDp_function=(lambda alpha, Re, mach, deflection: (1 + (alpha / 5) ** 2) * 2 * Cf_flat_plate(Re_L=Re)),
  Cm_function=(lambda alpha, Re, mach, deflection: 0))
e216 = Airfoil(name='e216',
  coordinates=None,
  CL_function=(lambda alpha, Re, mach, deflection: Cl_e216(alpha=alpha, Re_c=Re)),
  CDp_function=(lambda alpha, Re, mach, deflection: Cd_profile_e216(alpha=alpha, Re_c=Re) + Cd_wave_e216(Cl=Cl_e216(alpha=alpha, Re_c=Re), mach=mach)),
  Cm_function=(lambda alpha, Re, mach, deflection: -0.15))
rae2822 = Airfoil(name='rae2822',
  coordinates=None,
  CL_function=(lambda alpha, Re, mach, deflection: Cl_rae2822(alpha=alpha, Re_c=Re)),
  CDp_function=(lambda alpha, Re, mach, deflection: Cd_profile_rae2822(alpha=alpha, Re_c=Re) + Cd_wave_rae2822(Cl=Cl_rae2822(alpha=alpha, Re_c=Re), mach=mach)),
  Cm_function=(lambda alpha, Re, mach, deflection: -0.05))
naca0008 = Airfoil(name='naca0008',
  coordinates=None,
  CL_function=(lambda alpha, Re, mach, deflection: Cl_flat_plate(alpha=alpha, Re_c=Re)),
  CDp_function=(lambda alpha, Re, mach, deflection: (1 + (alpha / 5) ** 2) * 2 * Cf_flat_plate(Re_L=Re)),
  Cm_function=(lambda alpha, Re, mach, deflection: 0))
flat_plate = Airfoil(name='Flat Plate',
  coordinates=None,
  CL_function=(lambda alpha, Re, mach, deflection: Cl_flat_plate(alpha=alpha, Re_c=Re)),
  CDp_function=(lambda alpha, Re, mach, deflection: Cf_flat_plate(Re_L=Re) * 2),
  Cm_function=(lambda alpha, Re, mach, deflection: 0))