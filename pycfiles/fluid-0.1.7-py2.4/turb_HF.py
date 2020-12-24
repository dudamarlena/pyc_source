# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fluid/turb_HF.py
# Compiled at: 2006-12-04 09:19:16
"""It's an example how to reach turbulent heat fluxes
"""
import numarray, fluid.common.common, fluid.common.gfd, fluid.atmosphere.atmospheric_functions, fluid.interaction.heat_flux, fluid.interaction.others
from fluid import DataSet
Air = DataSet.Atmosphere()
Lat = numarray.array([15.0, -5.0, 8.0, 4.0, 0.0, 15.0, 4.0, 0.0, 0.0])
Ts = numarray.array([27.24, 25.6, 28.39, 27.13, 28.15, 26.97, 28.1, 29.33, 28.81])
Ks = Ts + 273.15
Ta = numarray.array([27.07, 25.21, 27.94, 26.5, 27.27, 26.9, 28.14, 28.39, 27.99])
Ka = Ta + 273.15
Air.Ta = Ta
Air.p = 100800.0
Air.RH = numarray.array([0.841, 0.813, 0.792, 0.847, 0.848, 0.899, 0.802, 0.839, 0.81])
u = numarray.array([3.9, 7.0, 5.6, 8.6, 5.7, 4.8, 5.1, 3.2, 3.4])
z_u = numarray.array([4.0])
z_T = numarray.array([3.0])
z_q = numarray.array([3.0])
p = 100800.0
g = fluid.common.gfd.gravity(Lat)
w_sat_sea = fluid.atmosphere.atmospheric_functions.saturation_mixing_ratio(Ts, p)
q_sat_sea = fluid.atmosphere.atmospheric_functions.specific_humidity(w_sat_sea)
q_sea = q_sat_sea * 0.98
Dq = Air.q - q_sea
DT = Air.Ta - Ts
Kv = fluid.atmosphere.atmospheric_functions.virtual_temperature(Ka, Air.ea, p=p)
Tv = fluid.common.common.K2C(Kv)
u_star = fluid.interaction.others.find_u_star(u, Air.nu_air, z_u, g=g)
z0 = fluid.interaction.others.set_z0(u_star, Air.nu_air)
(u_star, T_star, q_star) = fluid.interaction.others.find_transfer_coefficients(Air.Ta, Tv, Ts, Air.q, q_sea, u, z_u, z_T, z_q, Air.nu_air, u_star)
Le = fluid.interaction.others.latent_heat(Ts)
air_rho = fluid.atmosphere.atmospheric_functions.air_density(p, Kv)
(Hs, Hl) = fluid.interaction.others.turbulent_heat_fluxes(air_rho, u_star, T_star, q_star, Le)
CD = (u_star / u) ** 2
CT = u_star * T_star / (u * DT)
CQ = u_star * q_star / (u * Dq)
stress = fluid.interaction.others.wind_stress(air_rho, CD, u)
RI = fluid.interaction.others.richardson_number(Air.Ta, DT, Tv, Dq, u, z_u, g)