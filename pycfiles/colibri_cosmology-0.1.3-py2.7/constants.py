# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/colibri/constants.py
# Compiled at: 2020-04-15 05:34:59
import numpy as np, math

def explanatory():
    r"""
        This file contains a series of physical constants and conversion factors which are used in the other codes.
        Also useful quantities not strictly related to cosmology are defined.

        Conversion factors, distance

         - ``km_to_cm``: 1 km in cm
         - ``km_to_m``: 1 km in m 
         - ``pc_to_cm``: 1 pc in cm 
         - ``pc_to_m``: 1 pc in m 
         - ``pc_to_km``: 1 pc in km 
         - ``kpc_to_cm``: 1 kpc in cm 
         - ``kpc_to_m``: 1 kpc in m 
         - ``kpc_to_km``: 1 kpc in km 
         - ``Mpc_to_cm``: 1 Mpc in cm 
         - ``Mpc_to_m``: 1 Mpc in m 
         - ``Mpc_to_km``: 1 Mpc in km 

        Conversion factors, time

         - ``yr_to_s``: 1 yr in s 
         - ``Myr_to_s``: 1 Myr in s 

        Conversion factors, energy

         - ``eV``: electron-Volt in :math:`\mathrm{J}`
         - ``keV``: kilo Electron-Volt in :math:`\mathrm{J}` 
         - ``MeV``: mega Electron-Volt in :math:`\mathrm{J}` 
         - ``GeV``: giga Electron-Volt in :math:`\mathrm{J}` 
         - ``TeV``: tera Electron-Volt in :math:`\mathrm{J}` 

        Proton & electron mass & charges

         - ``mp``: proton mass in :math:`\mathrm{eV}`
         - ``mp_g``: proton mass in :math:`\mathrm{g}` 
         - ``mp_J``: proton mass in :math:`\mathrm{J}`
         - ``me``: eletron mass in :math:`\mathrm{eV^2}` 
         - ``me_g``: eletron mass in :math:`\mathrm{g}` 
         - ``me_J``: eletron mass in :math:`\mathrm{J}` 
         - ``q``: electron/proton charge in :math:`\mathrm{C}` 

        Neutrino properties

         - ``Delta_m21_squared``: difference of squared masses in :math:`\mathrm{eV^2}`
         - ``Delta_m32_squared_IH``: difference of squared masses in :math:`\mathrm{eV^2}`
         - ``Delta_m32_squared_NH``: difference of squared masses in :math:`\mathrm{eV^2}`
         - ``sin_theta_21_squared``: sine squared of mixing angle 
         - ``sin_theta_23_squared_IH``: sine squared of mixing angle, inverted hierarchy
         - ``sin_theta_23_squared_NH``: sine squared of mixing angle, normal hierarchy
         - ``sin_theta_13_squared``: sine squared of mixing angle 

        Constants of physics

         - ``G``: Newton's gravitational constant in units of :math:`\mathrm{Mpc} \ M_\odot (\mathrm{km/s})^2`
         - ``eps_0``: vacuum permittivity in :math:`\mathrm{F/m = C/V \ m}`
         - ``mu_0``: magnetic permeability in :math:`\mathrm{H/m = T \ m^2/A = V \ s/A}`  
         - ``kB``: Boltzmann constant in :math:`\mathrm{eV/K}`  
         - ``c``: speed of light in :math:`\mathrm{km/s}`
         - ``hP``: Planck constant in units of :math:`\mathrm{eV \ s}`
         - ``sSB``: Stefan-Boltzmann constant in :math:`\mathrm{W \ m^{-2} \ K^{-4}}` 
         - ``N_A``: Avogadro constant in :math:`\mathrm{mol^{-1}}`  
         - ``PI``: :math:`\mathrm{\pi = 3.14159265... }`

        Derived constants

         - ``e2``: electron/proton charge (squared!) in CGS units 
         - ``hPb``: reduced Planck constant (:math:`\bar{h}`) in :math:`\mathrm{eV \ s}`
         - ``hPJ``: Planck constant in :math:`\mathrm{J \ s}`
         - ``hPJb``: reduced Planck constant (:math:`\bar{h}`) in :math:`\mathrm{J \ s}`
         - ``sSB_eV``: Stefan-Boltzmann constant in :math:`\mathrm{eV \ m^{-2} \ K^{-4}}`
         - ``alpha_BB``: constant for blackbody energy density in :math:`\mathrm{J \ m^{-3} \ K^{-4}}`
         - ``R``: perfect gas constant in :math:`\mathrm{J \ mol^{-1} \ K^{-1}}`  
         - ``alpha_EM``: fine structure constant 
         - ``lambda_e``: Compton wavelength for electron in :math:`\mathrm{m}` 
         - ``r_e``: electron classical radius in :math:`\mathrm{m}` 
         - ``sigma_T``: Thomson scattering cross section in :math:`\mathrm{m}^2`
         - ``rhoch2``: critical density of the Universe :math:`h^2 \ M_\odot \ \mathrm{Mpc}^{-3}`

        Planck units

         - ``l_Pl``: Planck length in :math:`\mathrm{m}` 
         - ``t_Pl``: Planck time in :math:`\mathrm{s}`  
         - ``m_Pl``: Planck mass in :math:`\mathrm{g}` 
         - ``T_Pl``: Planck temperatur in :math:`\mathrm{K}`  
         - ``q_Pl``: Planck charge in :math:`\mathrm{C}`  

        Solar units

         - ``Msun``: solar mass in :math:`\mathrm{g}` 
         - ``Rsun``: solar radius in :math:`\mathrm{cm}` 
         - ``Tsun``: solar surface temperature in :math:`\mathrm{K}`
         - ``Lsun``: solar luminosity in :math:`\mathrm{erg \ s^{-1}}`
        """
    return 0


km_to_cm = 100000.0
km_to_m = 1000.0
pc_to_cm = 3.085677581e+18
pc_to_m = 3.085677581e+16
pc_to_km = 30856675810000.0
kpc_to_cm = 3.085677581e+21
kpc_to_m = 3.085677581e+19
kpc_to_km = 3.085667581e+16
Mpc_to_cm = 3.085677581e+24
Mpc_to_m = 3.085677581e+22
Mpc_to_km = 3.085667581e+19
yr_to_s = 31536000.0
Myr_to_s = 31536000000000.0
eV = 1.60217663e-19
keV = 1000.0 * eV
MeV = 1000000.0 * eV
GeV = 1000000000.0 * eV
TeV = 1000000000000.0 * eV
mp = 938000000.0
mp_g = 1.6726e-24
mp_J = 0.938 * GeV
me = 511000.0
me_g = 9.10938356e-28
me_J = 511.0 * keV
q = 1.60217663e-19
Delta_m21_squared = 7.53e-05
Delta_m32_squared_IH = -0.00256
Delta_m32_squared_NH = 0.00251
sin_theta_21_squared = 0.307
sin_theta_23_squared_IH = 0.592
sin_theta_23_squared_NH = 0.597
sin_theta_13_squared = 0.0212
G = 4.299e-09
eps_0 = 8.85418781762e-12
mu_0 = 1.25663706144e-06
kB = 8.614e-05
c = 299792.458
hP = 4.135668e-15
sSB = 5.6704e-08
N_A = 6.022140857e+23
PI = math.pi
e2 = q ** 2.0 / (4.0 * PI * eps_0)
hPb = hP / (2.0 * PI)
hPJ = hP * eV
hPJb = hPb * eV
sSB_eV = sSB / eV
alpha_BB = 4.0 * sSB / (c * km_to_m)
R = kB * eV * N_A
alpha_EM = e2 / (hPJb * c * km_to_m)
lambda_e = hP * c * km_to_m / me
r_e = alpha_EM * lambda_e / (2.0 * PI)
sigma_T = 8.0 * PI / 3.0 * r_e ** 2.0
rhoch2 = 3.0 * 10000.0 / (8 * PI * G)
l_Pl = 1.616252e-35
t_Pl = 5.39124e-44
m_Pl = 2.17644e-05
T_Pl = 1.416785e+32
q_Pl = 1.87554587e-18
Msun = 1.989e+33
Rsun = 69570000000.0
Tsun = 5772.0
Lsun = 3.848e+33