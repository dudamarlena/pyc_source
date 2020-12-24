# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fluid/test.py
# Compiled at: 2006-12-04 09:19:16
"""It's an example how to reach turbulent heat fluxes
"""
import numarray, fluid.atmosphere.atmospheric_functions, fluid.DataSet
Atm = fluid.DataSet.Atmosphere()
print dir(Atm)
HF = fluid.DataSet.HeatFlux()
print dir(HF)
HF.Ta = numarray.array([27.7, 28.4, 27.6, 28.0])
HF.q = numarray.array([17.6, 18.0, 17.3, 18.8]) * 0.001
HF.p = 100800
HF.DOY = numarray.array([350.0, 351.0, 352.0, 353.0])
HF.Lat = numarray.array([10.0])
HF.z_u = 4.0
HF.z_T = 3.0
HF.z_q = 3.0
HF.Qswi = numarray.array([100, 200, 220, 300])
HF.SST = numarray.array([29.0, 29.2, 29.0, 29.3])
HF.U = numarray.array([4.7, 2.5, 5.9, 2.8])
HF.RH = fluid.atmosphere.atmospheric_functions.vapor_pressure(fluid.atmosphere.atmospheric_functions.q2w(HF.q), 100800) / fluid.atmosphere.atmospheric_functions.saturation_vapor_pressure(HF.Ta)
HF.recalculate()
print 'Ta', HF.Ta
print HF.Ka
print HF.Atm.Ta
print HF.RH
print HF.Atm.RH
print HF.p
print HF.Atm.p
print HF.ea
print 'SST', HF.SST
print 'NSA', HF.NSA
print 'Qcs', HF.Qcs
print 'FracQ', HF.FracQ
print 'C', HF.C
print 'Qlw', HF.Qlw
print 'nu_air', HF.nu_air
print 'U', HF.U
print 'u_star', HF.u_star
print 'Tv', HF.Tv
print 'q_sea', HF.q_sea
print 'HF.Atm.q', HF.Atm.q
print 'u_star', HF.u_star
print 'T_star', HF.T_star
print 'q_star', HF.q_star
print 'Le', HF.Le
print 'HF.Atm.rho_air', HF.Atm.rho_air
HF.set_tubulent_heat_fluxes()
print 'HF.Hs', HF.Hs
print 'HF.Hl', HF.Hl