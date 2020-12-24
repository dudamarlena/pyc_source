# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/guest/Documents/Astro/projects/reduction/reduction/stars/binary_orbit.py
# Compiled at: 2017-12-01 09:00:35
""" Compute the radial velocity of the components of a binary system.

"""
import numpy as np, astropy.units as u, astropy.constants as const
from astropy.time import Time
import matplotlib.pyplot as plt
from reduction.constants import H_ALPHA

class BinaryOrbit:

    def __init__(self, name1='A', name2='B', m1=None, m2=None, M=None, a1=None, a2=None, a=None, e=None, omega1=None, omega2=None, Omega=None, incl=None, period=None, epoch=None):
        """
        :param name1: name of component1
        :param name2: name of component2
        :param m1: mass of component1
        :param m2: mass of component2
        :param M: None or m1 + m2
        :param a1: semi major axis of component1
        :param a2: semi major axis of component2
        :param a: None pr a1 + a2
        :param e: eccentricity
        :param omega1: argument of periapsis of component1
        :param omega2: None or omega1 + 180deg
        :param Omega: longitude of the ascending node (unused)
        :param incl: inclination of the orbit
        :param period: orbital period
        :param epoch: T_0

        Define either masses or orbital radii, not both.
        The missing values are calculated from:
        $$a = a_1 + a_2$$
        $$M = m_1 + m_2$$
        $$a_1 M_1 = a_2 M_2$$ and
        $$M * period^2 = a^3$$
        Note that the last formula is relative to our solar system, so M needs to be in solar masses,
        P in years and a in astronomical units.

        """
        self.name1 = name1
        self.name2 = name2
        self.e = e
        assert 0 <= self.e <= 1
        self.incl = incl.to(u.rad)
        self.period = period.to(u.day)
        self.epoch = epoch
        assert isinstance(epoch, Time)
        self.Omega = Omega
        if omega1:
            assert not omega2 or omega2 == omega1 + 180.0 * u.degree
            self.omega1 = omega1
            self.omega2 = omega1 + 180.0 * u.degree
        elif omega2:
            assert not omega1 or omega1 == omega2 + 180.0 * u.degree
            self.omega1 = omega2 + 180.0 * u.degree
            self.omega2 = omega2
        else:
            raise ValueError('omaga1 or omega2 M has to be defined')
        if m1 and m2 or m1 and M or m2 and M:
            assert not (a1 or a2 or a), 'either mass or radii can be defined'
            if m1 and m2:
                assert not M or M == m1 + m2, 'masses do not add up'
                self.m1 = m1.to(u.solMass)
                self.m2 = m2.to(u.solMass)
                self.M = m1 + m2
            elif m1 and M:
                assert not m2 or M == m1 + m2, 'masses do not add up'
                self.m1 = m1.to(u.solMass)
                self.M = M.to(u.solMass)
                self.m2 = self.M - self.m1
            elif m2 and M:
                assert not m1 or M == m1 + m2, 'masses do not add up'
                self.m2 = m2.to(u.solMass)
                self.M = M.to(u.solMass)
                self.m1 = self.M - self.m2
            self.a = np.power(self.M.to(u.solMass).value * (self.period.to(u.year) ** 2).value, 1.0 / 3.0) * u.AU
            self.a1 = self.a * self.m2 / self.M
            self.a2 = self.a - self.a1
        elif a1 and a2 or a1 and a or a2 and a:
            if a1 and a2:
                assert not a or a == a1 + a2, 'radii do not add up'
                self.a1 = a1.to(u.AU)
                self.a2 = a2.to(u.AU)
                self.a = self.a1 + self.a2
            elif a1 and a:
                assert not a2 or a == a1 + a2, 'radii do not add up'
                self.a1 = a1.to(u.AU)
                self.a = a.to(u.AU)
                self.a2 = self.a - self.a1
            elif a2 and a:
                assert not a1 or a == a1 + a2, 'radii do not add up'
                self.a2 = a2.to(u.AU)
                self.a = a.to(u.AU)
                self.a1 = self.a - self.a2
            self.M = (self.a.to(u.AU) ** 3).value / (self.period.to(u.year) ** 2).value * u.solMass
            self.m1 = self.a2 * self.M / self.a
            self.m2 = self.M - self.m1
        else:
            raise ValueError('either mass or radii have be defined')
        k = 2.0 * np.pi / self.period * self.a * np.sin(self.incl) / np.sqrt(1.0 - self.e ** 2)
        self.k_1 = self.m2 / self.M * k
        self.k_2 = self.m1 / self.M * k
        assert self.period > 0
        assert self.m1 > 0
        assert self.m2 > 0
        assert self.M > 0
        assert self.a1 > 0
        assert self.a2 > 0
        assert self.a > 0
        assert (self.m1 >= self.m2) == (self.a1 <= self.a2)

    def true_from_eccentric_anomaly(self, eccentric_anomaly):
        y = np.sqrt(1 + self.e) * np.sin(eccentric_anomaly / 2)
        x = np.sqrt(1 - self.e) * np.cos(eccentric_anomaly / 2)
        return 2 * np.arctan2(y, x)

    def eccentric_from_mean_anomaly(self, mean_anomaly):

        def inverse(M):
            eps = 1e-07
            E = 0
            for i in range(1, 100):
                dE = M + self.e * np.sin(E) - E
                E += dE
                if -eps < dE < +eps:
                    return E

            raise ValueError('true_anomaly calculation did not converge for M=%s and e=%s' % (M, self.e))

        if isinstance(mean_anomaly, u.Quantity):
            mean_anomaly = mean_anomaly.to(u.radian).value
        if isinstance(mean_anomaly, np.ndarray):
            return np.array([ inverse(mi) for mi in mean_anomaly ]) * u.radian
        else:
            return inverse(mean_anomaly) * u.radian

    @staticmethod
    def _into_0_2pi(x):
        x = x.to(u.radian).value
        res = x - 2 * np.pi * np.floor(x / 2 / np.pi)
        return res * u.radian

    def mean_anomaly(self, time):
        """ return the mean anomaly at a given time in the range 0 .. 2pi
        """
        return self._into_0_2pi(2 * np.pi * u.radian * (time - self.epoch) / self.period)

    def phase(self, time):
        return self.true_anomaly(time) / 2 / np.pi

    def true_anomaly(self, time):
        """ return the true anomaly at a given time in the range 0 .. 2pi
        """
        ma = self.mean_anomaly(time)
        ea = self.eccentric_from_mean_anomaly(ma)
        ta = self.true_from_eccentric_anomaly(ea)
        return self._into_0_2pi(ta)

    def _v(self, k, true_anomaly, omega):
        return k * (np.cos(true_anomaly + omega) + self.e * np.cos(omega))

    def v1(self, time):
        """ return the radial velocity of the first component at a given time
        """
        ta = self.true_anomaly(time)
        v1 = self._v(self.k_1, ta, self.omega1)
        return v1

    def v2(self, time):
        """ return the radial velocity of the second component at a given time
        """
        ta = self.true_anomaly(time)
        v2 = self._v(self.k_2, ta, self.omega2)
        return v2

    def plot_orbit(self, plot, v0=None, points=401):
        """Plot a single orbit via matplotlib 
         
        :param plot: target matplotlib plot or subplot
        :param v0: system radial velocity 
        :param points: number of points in x directions
        """
        t0 = self.epoch
        p = self.period
        t = Time(np.linspace(t0.jd, (t0 + p).jd, points), format='jd')
        addx = plot.twiny()
        addy = plot.twinx()
        v_1 = self.v1(t).to('km/s')
        if v0:
            v_1 += v0
        plot.plot(t.jd, v_1, label='%s m1=%.1f' % (self.name1, self.m1.value))
        v_2 = self.v2(t).to('km/s')
        if v0:
            v_2 += v0
        plot.plot(t.jd, v_2, label='%s m2=%.1f' % (self.name2, self.m2.value))
        if v0:
            v_0 = np.ones(t.size) * v0
            plot.plot(t.jd, v_0, label='%.0f %s' % (v0.to('km/s').value, v0.to('km/s').unit))
        plot.set_xlim((t0 - 0.1 * p).jd, (t0 + 1.1 * p).jd)
        addx.set_xlim(-0.1, 1.1)
        v_min, v_max = plot.get_ylim() * u.km / u.s
        l_min = (v_min / const.c).to(1) * H_ALPHA
        l_max = (v_max / const.c).to(1) * H_ALPHA
        addy.set_ylim(l_min.value, l_max.value)
        plot.xaxis.set_major_locator(plt.MaxNLocator(5))
        plot.xaxis.set_minor_locator(plt.MultipleLocator(1))
        plot.xaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
        addx.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
        plot.set_ylabel('Radial velocity (km/s)')
        plot.set_xlabel('Julian date')
        addy.set_ylabel('$\\delta\\lambda \\| H\\alpha (\\AA)$')
        plot.legend()