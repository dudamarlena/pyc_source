# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/SRMspinanalysis/model.py
# Compiled at: 2018-05-29 13:59:57
import numpy as np

class RocketModel:
    """Rocket model includes physical characteristics of launch vehicle.

    Attributes
    ----------
    r1 : Radial location of solid rocket motor for spin-up [m]
    r2 : Radial location of solid rocket motor for spin-up [m]
    d1 : Longitudinal location of solid rocket motor for spin-up [m]
    d2 : Longitudinal location of solid rocket motor for spin-up [m]
    Ixx : Roll inertia of rocket [kg-m^2]
    Iyy : Yaw inertia of rocket [kg-m^2]
    Izz : Pitch inertia of rocket [kg-m^2]
    
    """

    def __init__(self, r1=0.1143, r2=0.1143, d1=0.635, d2=0.635, Ixx=83914.58845000001 * 0.00064516, Iyy=83914.58845000001 * 0.00064516, Izz=1587.5732950000001 * 0.00064516):
        """Initalizes the rocket model with user defined values.
        """
        self.r1 = r1
        self.r2 = r2
        self.d1 = d1
        self.d2 = d2
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz

    def create_design_params(self):
        """Packages the design parameters into a numpy array.
        """
        return np.array([self.r1, self.r2, self.d1, self.d2, self.Ixx, self.Iyy, self.Izz])