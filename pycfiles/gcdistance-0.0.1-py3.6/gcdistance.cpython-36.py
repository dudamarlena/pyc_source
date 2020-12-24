# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\gcdistance\gcdistance.py
# Compiled at: 2019-09-30 09:21:11
# Size of source mod 2**32: 1099 bytes
"""
Created on Mon Sep 30 10:00:48 2019

@author: lealp
"""
import numpy as np

def great_circle_distance(point1, point2, Earth_Radius=6371000.0):
    """Calculate great-circle distance between two points.

    PARAMETERS
    ----------
    point1 : tuple
        A (lat, lon) pair of coordinates in degrees
    
    point2 : tuple
        A (lat, lon) pair of coordinates in degrees
    
    Earth_Radius: (float) == 6.371e6
    
        the earth's radius for evaluation of the distance
    
    RETURNS
    -------
    distance : float
    """
    lat1, lon1 = point1
    lat2, lon2 = point2
    phi1, lambda1, phi2, lambda2 = [np.deg2rad(v) for v in point1 + point2]
    return Earth_Radius * np.arccos(np.sin(phi1) * np.sin(phi2) + np.cos(phi1) * np.cos(phi2) * np.cos(lambda2 - lambda1))