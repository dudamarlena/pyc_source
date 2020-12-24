# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/guest/Documents/Astro/projects/reduction/reduction/stars/algol.py
# Compiled at: 2017-12-04 16:13:49
import logging
logger = logging.getLogger(__name__)
import numpy as np, astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from reduction.stars.binary_orbit import BinaryOrbit
from reduction.stars.variable_stars import RegularVariableObject
algol_coordinate = SkyCoord(47.04221855, 40.95564667, unit=u.deg, frame='icrs')
algol_unknown = RegularVariableObject(Time(2457403.333, format='jd'), 2.867328 * u.day, authority='unknown', coordinate=algol_coordinate)
algol_GCVS = RegularVariableObject(Time(2445641.5135, format='jd'), 2.8673043 * u.day, authority='GCVS', coordinate=algol_coordinate)
algol_FilipeDiaz_GCVS = RegularVariableObject(Time('2017-08-14T03:40:00', format='isot'), 2.8673043 * u.day, authority='Filipe Diaz', coordinate=algol_coordinate)
algol_Kosmos = RegularVariableObject(Time('2018-01-01T16:16:00', format='isot'), 2.8673043 * u.day, authority='Kosmos Himmelsjahr 2018', coordinate=algol_coordinate)
algol_Interstellarum = RegularVariableObject(Time('2018-01-18T20:34:00', format='isot'), 2.8673043 * u.day, authority='Himmels-Almanach 2018', coordinate=algol_coordinate)
algol_Baron2012 = RegularVariableObject(Time(2441771.353, format='jd'), 2.867328 * u.day, authority='Baron2012', coordinate=algol_coordinate)
algol_Zavala2010 = RegularVariableObject(Time(2441773.49, format='jd'), 2.867328 * u.day, authority='Zavala2010', coordinate=algol_coordinate)
algol_Zavala2010_via_Baron2012 = RegularVariableObject(Time(2441771.3395, format='jd'), 2.867328 * u.day, authority='Baron about Zavala?', coordinate=algol_coordinate)
algol_AAVSO_my = RegularVariableObject(Time(2456181.84, format='jd'), 2.86736 * u.day, authority='AAVSO my calculation', coordinate=algol_coordinate)
algol_AAVSO_self = RegularVariableObject(Time('2017-11-28T06:24', format='isot'), 2.86736 * u.day, authority='AAVSO their calculation', coordinate=algol_coordinate)

class Algol:
    """
    TODO: verify definition of period 
    """

    def __init__(self):
        self.rv = 3.7 * u.km / u.s
        self.distance_AB = 90 * u.lyr
        self.distance_AB_error = 3 * u.lyr
        self.AB = BinaryOrbit(name1='AlgolA', name2='AlgolB', period=algol_unknown.period, epoch=algol_unknown.epoch, m1=3.7 * u.solMass, m2=0.81 * u.solMass, e=0, incl=98.6 * u.degree, omega1=90 * u.degree, Omega=47.4 * u.degree)
        self.AB_C = BinaryOrbit(name1='AlgolAB', name2='AlgolC', period=680.1 * u.day, epoch=Time(2446936.4, format='jd'), m1=self.AB.M, m2=1.6 * u.solMass, e=0.227, incl=83.76 * u.degree, omega1=313.2 * u.degree, Omega=132.7)
        T_A = 12550 * u.K

    def phase_AB(self, time):
        return self.AB.phase(time)

    def phase_AB_C(self, time):
        return self.AB_C.phase(time)

    def rv_A(self, time):
        return self.rv + self.AB_C.v1(time) + self.AB.v1(time)

    def rv_B(self, time):
        return self.rv + self.AB_C.v1(time) + self.AB.v2(time)

    def rv_AB(self, time):
        return self.rv + self.AB_C.v1(time)

    def rv_C(self, time):
        return self.rv + self.AB_C.v2(time)


def plot_algol():
    import matplotlib.pyplot as plt
    algol = Algol()
    fig = plt.figure(figsize=(6, 9))
    fig.subplots_adjust(hspace=0.6)
    algol.AB_C.plot_orbit(fig.add_subplot(111), 0)
    plt.show()


def plot_comparison():
    import matplotlib.pyplot as plt
    axes = plt.axes()
    now = Time.now()
    than = now + 3 * u.day
    plt.axhline(y=0)
    for var in [algol_unknown, algol_Kosmos, algol_Interstellarum, algol_FilipeDiaz_GCVS, algol_GCVS,
     algol_Zavala2010, algol_Zavala2010_via_Baron2012, algol_Baron2012,
     algol_AAVSO_my, algol_AAVSO_self]:
        var.plot(axes, now, than)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    plot_comparison()