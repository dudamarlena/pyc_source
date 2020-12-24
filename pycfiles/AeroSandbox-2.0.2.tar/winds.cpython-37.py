# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\library\winds.py
# Compiled at: 2020-03-16 11:46:48
# Size of source mod 2**32: 2522 bytes
import casadi as cas

def wind_speed_conus_summer_99(altitude, latitude):
    r"""
    Returns the 99th-percentile wind speed magnitude over the continental United States (CONUS) in July-Aug. Aggregate of data from 1972 to 2019.
    Fits at C:\Projects\GitHub\Wind_Analysis
    :param altitude: altitude [m]
    :param latitude: latitude [deg]
    :return: 99th-percentile wind speed over the continental United States in the summertime. [m/s]
    """
    l = (latitude - 37.5) / 11.5
    a = (altitude - 24200) / 24200
    agc = -0.5363486000267786
    agh = 1.9569754777072828
    ags = 0.1458701999734713
    aqc = -1.4645014948089652
    c0 = -0.5169694086686631
    c12 = 0.0849519807021402
    c21 = -0.0252010113059998
    c4a = 0.0225856848053377
    c4c = 1.02818773537345
    cg = 0.8050736230004489
    cgc = 0.2786691793571486
    cqa = 0.1866078047914259
    cql = 0.0165126852561671
    cqla = -0.1361667658248024
    lgc = 0.6943655538727291
    lgh = 2.0777449841036777
    lgs = 0.9805766577269118
    lqc = 4.035683459574321
    s = c0 + cql * (l - lqc) ** 2 + cqa * (a - aqc) ** 2 + cqla * a * l + cg * cas.exp(-(cas.fabs(l - lgc) ** lgh / (2 * lgs ** 2) + cas.fabs(a - agc) ** agh / (2 * ags ** 2) + cgc * a * l)) + c4a * (a - c4c) ** 4 + c12 * l * a ** 2 + c21 * l ** 2 * a
    speed = s * 56 + 7
    return speed