# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\library\atmosphere.py
# Compiled at: 2020-02-23 14:03:03
# Size of source mod 2**32: 3097 bytes
import casadi as cas, numpy as np
R_universal = 8.31432
M_air = 0.0289644
R_air = R_universal / M_air

def get_pressure_at_altitude(altitude):
    """
    Fit to the 1976 COESA model; see C:\\Projects\\GitHub\x0cirefly_aerodynamics\\Gists and Ideas\\Atmosphere Fitting for details.
    Valid from 0 to 40 km.
    :param altitude:
    :return:
    """
    altitude_scaled = altitude / 40000
    p1 = -1.822942
    p2 = 5.366751
    p3 = -5.021452
    p4 = -4.424532
    p5 = 11.51986
    x = altitude_scaled
    logP = p5 + x * (p4 + x * (p3 + x * (p2 + x * p1)))
    pressure = cas.exp(logP)
    return pressure


def get_temperature_at_altitude(altitude):
    """
    Fit to the 1976 COESA model; see C:\\Projects\\GitHub\x0cirefly_aerodynamics\\Gists and Ideas\\Atmosphere Fitting for details.
    Valid from 0 to 40 km.
    :param altitude:
    :return:
    """
    altitude_scaled = altitude / 40000
    p1 = -21.22102
    p2 = 70.00812
    p3 = -87.5917
    p4 = 50.47893
    p5 = -11.76537
    p6 = -0.03566535
    p7 = 5.649588
    x = altitude_scaled
    logT = p7 + x * (p6 + x * (p5 + x * (p4 + x * (p3 + x * (p2 + x * p1)))))
    temperature = cas.exp(logT)
    return temperature


def get_density_at_altitude(altitude):
    P = get_pressure_at_altitude(altitude)
    T = get_temperature_at_altitude(altitude)
    rho = P / (T * R_air)
    return rho


def get_speed_of_sound_from_temperature(temperature):
    """
    Finds the speed of sound from a specified temperature. Assumes ideal gas properties.
    :param temperature: Temperature, in Kelvin
    :return: Speed of sound, in m/s
    """
    return cas.sqrt(1.4 * R_air * temperature)


def get_viscosity_from_temperature(temperature):
    """
    Finds the dynamics viscosity of air from a specified temperature. Uses Sutherland's Law
    :param temperature: Temperature, in Kelvin
    :return: Dynamic viscosity, in kg/(m*s)
    """
    C1 = 1.458e-06
    S = 110.4
    mu = C1 * temperature ** 1.5 / (temperature + S)
    return mu


if __name__ == '__main__':
    test_altitudes = cas.linspace(0, 40000, 201)
    test_pressures = get_pressure_at_altitude(test_altitudes)
    test_temps = get_temperature_at_altitude(test_altitudes)
    import matplotlib.pyplot as plt
    import matplotlib.style as style
    import plotly.express as px
    import plotly.graph_objects as go
    style.use('seaborn')
    plt.semilogy(test_altitudes, test_pressures)
    plt.xlabel('Altitude [m]')
    plt.ylabel('Pressure [Pa]')
    plt.show()
    plt.plot(test_altitudes, test_temps)
    plt.xlabel('Altitude [m]')
    plt.ylabel('Temperature [K]')
    plt.show()