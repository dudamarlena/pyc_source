# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/AMAT/launcher.py
# Compiled at: 2020-05-07 19:40:41
# Size of source mod 2**32: 4290 bytes
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import os

class Launcher:
    """Launcher"""

    def __init__(self, launcherID):
        """
                Initializes the planet object with the planetary constants.
                
                Parameters
                ----------
                launcherID : str
                        Name of the launch vehicle, must be one of the following 
                        Valid entries are: 
                        
                        'atlasV401', 
                        'atlasV551', 
                        'atlasV551-with-kick',
                        'deltaIVH',
                        'deltaIVH-with-kick', 
                        'falconH', 
                        'falconH-recovery', 
                        'sls-block-1B',
                        'sls-block-1B-with-kick'
                """
        if launcherID == 'atlasV401':
            self.ID = 'Atlas V401'
            self.XY = np.loadtxt('../launcher-data/atlasV401.csv', delimiter=',')
        elif launcherID == 'atlasV551':
            self.ID = 'Atlas V551'
            self.XY = np.loadtxt('../launcher-data/atlasV551.csv', delimiter=',')
        elif launcherID == 'atlasV551-with-kick':
            self.ID = 'Atlas V551 with kick'
            self.XY = np.loadtxt('../launcher-data/atlasV551-with-kick.csv', delimiter=',')
        elif launcherID == 'deltaIVH':
            self.ID = 'Delta IVH'
            self.XY = np.loadtxt('deltaIVH.csv', delimiter=',')
        elif launcherID == 'deltaIVH-with-kick':
            self.ID = 'Delta IVH with kick'
            self.XY = np.loadtxt('../launcher-data/deltaIVH-with-kick.csv', delimiter=',')
        elif launcherID == 'falconH':
            self.ID = 'Falcon Heavy'
            self.XY = np.loadtxt('../launcher-data/falconH.csv', delimiter=',')
        elif launcherID == 'falconH-recovery':
            self.ID = 'Falcon Heavy (Recovery)'
            self.XY = np.loadtxt('../launcher-data/falconH-recovery.csv', delimiter=',')
        elif launcherID == 'sls-block-1B':
            self.ID = 'SLS Block 1B'
            self.XY = np.loadtxt('../launcher-data/sls-block-1B.csv', delimiter=',')
        elif launcherID == 'sls-block-1B-with-kick':
            self.ID = 'SLS Block 1B with kick'
            self.XY = np.loadtxt('../launcher-data/sls-block-1B-with-kick.csv', delimiter=',')
        else:
            print(' >>> ERR : Invalid planet identifier provided.')

    def performanceQuery(self, C3):
        """
                Returns the launch capability of the vehicle for a 
                specified C3.

                Parameters
                ----------
                C3 : float
                        launch C3, km2/s2

                Returns
                --------
                mass : float
                        launch mass capability, kg

                """
        f = interp1d((self.XY[:, 0]), (self.XY[:, 1]), kind='cubic', bounds_error=False)
        mass = float(f(C3))
        return mass