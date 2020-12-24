# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\library\power_solar.py
# Compiled at: 2020-04-19 00:21:05
# Size of source mod 2**32: 9676 bytes
import casadi as cas
from aerosandbox.tools.casadi_tools import sind, cosd

def solar_flux_outside_atmosphere_normal(day_of_year):
    """
    Normal solar flux at the top of the atmosphere (variation due to orbital eccentricity)
    :param day_of_year: Julian day (1 == Jan. 1, 365 == Dec. 31)
    :return: Solar flux [W/m^2]
    """
    return 1366 * (1 + 0.033 * cosd(360 * (day_of_year - 2) / 365))


def declination_angle(day_of_year):
    """
    Declination angle, in degrees, as a func. of day of year. (Seasonality)
    :param day_of_year: Julian day (1 == Jan. 1, 365 == Dec. 31)
    :return: Declination angle [deg]
    """
    return -23.45 * cosd(0.9863013698630136 * (day_of_year + 10))


def solar_elevation_angle(latitude, day_of_year, time):
    """
    Elevation angle of the sun [degrees] for a local observer.
    :param latitude: Latitude [degrees]
    :param day_of_year: Julian day (1 == Jan. 1, 365 == Dec. 31)
    :param time: Time after local solar noon [seconds]
    :return: Solar elevation angle [degrees] (angle between horizon and sun). Returns 0 if the sun is below the horizon.
    """
    declination = declination_angle(day_of_year)
    solar_elevation_angle = cas.asin(sind(declination) * sind(latitude) + cosd(declination) * cosd(latitude) * cosd(time / 86400 * 360)) * 180 / cas.pi
    solar_elevation_angle = cas.fmax(solar_elevation_angle, 0)
    return solar_elevation_angle


def incidence_angle_function(latitude, day_of_year, time, scattering=True):
    """
    What is the fraction of insolation that a horizontal surface will receive as a function of sun position in the sky?
    :param latitude: Latitude [degrees]
    :param day_of_year: Julian day (1 == Jan. 1, 365 == Dec. 31)
    :param time: Time since (local) solar noon [seconds]
    :param scattering: Boolean: include scattering effects at very low angles?
    """
    elevation_angle = solar_elevation_angle(latitude, day_of_year, time)
    theta = 90 - elevation_angle
    cosine_factor = cosd(theta)
    if not scattering:
        return cosine_factor
    return cosine_factor * scattering_factor(elevation_angle)


def scattering_factor(elevation_angle):
    """
    Calculates a scattering factor (a factor that gives losses due to atmospheric scattering at low elevation angles).
    Source: AeroSandbox/studies/SolarPanelScattering
    :param elevation_angle: Angle between the horizon and the sun [degrees]
    :return: Fraction of the light that is not lost to scattering.
    """
    elevation_angle = cas.fmin(cas.fmax(elevation_angle, 0), 90)
    theta = 90 - elevation_angle
    theta_rad = theta * cas.pi / 180
    c = (-0.04636, -0.3171)
    scattering_factor = cas.exp(c[0] * (cas.tan(theta_rad * 0.999) + c[1] * theta_rad))
    return scattering_factor


def solar_flux_on_horizontal(latitude, day_of_year, time, scattering=True):
    """
    What is the solar flux on a horizontal surface for some given conditions?
    :param latitude: Latitude [degrees]
    :param day_of_year: Julian day (1 == Jan. 1, 365 == Dec. 31)
    :param time: Time since (local) solar noon [seconds]
    :param scattering: Boolean: include scattering effects at very low angles?
    :return:
    """
    return solar_flux_outside_atmosphere_normal(day_of_year) * incidence_angle_function(latitude, day_of_year, time, scattering)


def peak_sun_hours_per_day_on_horizontal(latitude, day_of_year, scattering=True):
    """
    How many hours of equivalent peak sun do you get per day?
    :param latitude: Latitude [degrees]
    :param day_of_year: Julian day (1 == Jan. 1, 365 == Dec. 31)
    :param time: Time since (local) solar noon [seconds]
    :param scattering: Boolean: include scattering effects at very low angles?
    :return:
    """
    times = np.linspace(0, 86400, 1000)
    dt = np.diff(times)
    normalized_fluxes = incidence_angle_function(latitude, day_of_year, times, scattering)
    sun_hours = np.sum((normalized_fluxes[1:] + normalized_fluxes[:-1]) / 2 * dt) / 3600
    return sun_hours


if __name__ == '__main__':
    import numpy as np
    latitudes = np.linspace(26, 49, 200)
    day_of_years = np.arange(0, 365) + 1
    times = np.linspace(0, 86400, 400)
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(font_scale=1)
    fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
    lats_to_plot = [26, 49]
    lats_to_plot = np.linspace(0, 90, 7)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(lats_to_plot)))[::-1]
    [plt.plot((times / 3600), (solar_flux_on_horizontal(lats_to_plot[i], 244, times)), label=('%iN Latitude' % lats_to_plot[i]), color=(colors[i]), linewidth=3) for i in range(len(lats_to_plot))]
    plt.grid(True)
    plt.legend()
    plt.title('Solar Flux on a Horizontal Surface (Aug. 31)')
    plt.xlabel('Time after Solar Noon [hours]')
    plt.ylabel('Solar Flux [W/m$^2$]')
    plt.tight_layout()
    plt.savefig('C:/Users/User/Downloads/temp.png')
    plt.show()