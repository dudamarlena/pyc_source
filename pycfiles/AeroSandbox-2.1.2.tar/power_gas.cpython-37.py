# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\library\power_gas.py
# Compiled at: 2020-03-06 12:02:17
# Size of source mod 2**32: 450 bytes


def mass_gas_engine(max_power):
    """
    Estimates the mass of a small piston-driven motor.
    Source: https://docs.google.com/spreadsheets/d/103VPDwbQ5PfIE3oQl4CXxM5AP6Ueha-zbw7urElkQBM/edit#gid=0
    :param max_power: Maximum power output [W]
    :return: Estimated motor mass [kg]
    """
    max_power_hp = max_power / 745.7
    mass_lbm = 6.12 * max_power_hp ** 0.588
    mass = mass_lbm * 0.453592
    return mass