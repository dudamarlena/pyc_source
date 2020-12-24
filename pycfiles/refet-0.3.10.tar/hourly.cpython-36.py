# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\RefET\refet\hourly.py
# Compiled at: 2019-02-26 15:00:13
# Size of source mod 2**32: 9320 bytes
import math, numpy as np
from . import calcs

class Hourly:

    def __init__(self, tmean, ea, rs, uz, zw, elev, lat, lon, doy, time, method='asce', input_units={}):
        """ASCE Hourly Standardized Reference Evapotranspiration (ET)

        .. warning:: Cloudiness fraction at night is not being computed per [1]_

        Arguments
        ---------
        tmean : ndarray
            Average hourly temperature [C].
        ea : ndarray
            Actual vapor pressure [kPa].
        rs : ndarray
            Shortwave solar radiation [MJ m-2 hr-1].
        uz : ndarray
            Wind speed [m s-1].
        zw : float
            Wind speed measurement/estimated height [m].
        elev : ndarray
            Elevation [m]
        lat : ndarray
            Latitude [degrees]
        lon : ndarray
            Longitude [degrees].
        doy : ndarray
            Day of year.
        time : ndarray
            UTC hour at start of time period.
        method : {'asce' (default), 'refet'}, optional
            Specifies which calculation method to use.
            * 'asce' -- Calculations will follow ASCE-EWRI 2005 [1]_ equations.
            * 'refet' -- Calculations will follow RefET software.
        input_units : dict, optional
            Input unit types.

        Returns
        -------
        etsz : ndarray
            Standardized reference ET [mm].

        Notes
        -----
        The Langleys to MJ m-2 conversion factor is the value used in the RefET
        program, although there are other factors that could be applied:
        https://www.aps.org/policy/reports/popa-reports/energy/units.cfm

        References
        ----------
        .. [1] ASCE-EWRI (2005). The ASCE standardized reference
           evapotranspiration equation. ASCE-EWRI Standardization of Reference
           Evapotranspiration Task Committee Rep., ASCE Reston, Va.
           http://www.kimberly.uidaho.edu/water/asceewri/ascestzdetmain2005.pdf
           http://www.kimberly.uidaho.edu/water/asceewri/appendix.pdf

        """
        self.tmean = np.array(tmean, copy=True, ndmin=1)
        self.ea = np.array(ea, copy=True, ndmin=1)
        self.rs = np.array(rs, copy=True, ndmin=1)
        self.uz = np.array(uz, copy=True, ndmin=1)
        self.elev = np.array(elev, copy=True, ndmin=1)
        self.lat = np.array(lat, copy=True, ndmin=1)
        self.lon = np.array(lon, copy=True, ndmin=1)
        self.doy = np.array(doy, copy=True, ndmin=1)
        self.time = np.array(time, copy=True, ndmin=1)
        self.time_mid = self.time + 0.5
        self.zw = zw
        self.doy = doy
        for variable, unit in input_units.items():
            if unit == '':
                continue
            else:
                if unit.lower() in ('c', 'celsius', 'mj m-2 hour-1', 'mj m-2 h-1',
                                    'kpa', 'm s-1', 'm/s', 'm', 'meter', 'meters',
                                    'deg', 'degree', 'degrees'):
                    continue
                else:
                    if unit.lower() not in ('k', 'kelvin', 'f', 'fahrenheit', 'pa',
                                            'langleys', 'w m-2', 'w/m2', 'mph', 'ft',
                                            'feet', 'rad', 'radian', 'radians'):
                        raise ValueError('unsupported unit conversion for {} {}'.format(variable, unit))
            if variable == 'tmean':
                if unit.lower() in ('f', 'fahrenheit'):
                    self.tmean -= 32
                    self.tmean *= 0.5555555555555556
                elif unit.lower() in ('k', 'kelvin'):
                    self.tmean -= 273.15
            else:
                if variable == 'ea':
                    if unit.lower() in ('pa', ):
                        self.ea /= 1000.0
                else:
                    if variable == 'rs':
                        if unit.lower() in ('langleys', ):
                            self.rs *= 0.041868
                        elif unit.lower() in ('w m-2', 'w/m2'):
                            self.rs *= 0.0036
                    else:
                        if variable == 'uz':
                            if unit.lower() in ('mph', ):
                                self.uz *= 0.44704
                        else:
                            if variable == 'zw':
                                if unit.lower() in ('ft', 'feet'):
                                    self.zw *= 0.3048
                            else:
                                if variable == 'elev':
                                    if unit.lower() in ('ft', 'feet'):
                                        self.elev *= 0.3048
                                else:
                                    if variable == 'lat':
                                        if unit.lower() in ('rad', 'radian', 'radians'):
                                            self.lat *= 180.0 / math.pi
                                    else:
                                        if variable == 'lon':
                                            if unit.lower() in ('rad', 'radian', 'radians'):
                                                self.lon *= 180.0 / math.pi

        if method.lower() not in ('asce', 'refet'):
            raise ValueError('method must be "asce" or "refet"')
        self.lat *= math.pi / 180.0
        self.lon *= math.pi / 180.0
        self.pair = calcs._air_pressure(self.elev, method)
        self.psy = 0.000665 * self.pair
        self.es = calcs._sat_vapor_pressure(self.tmean)
        self.es_slope = calcs._es_slope(self.tmean, method)
        self.vpd = self.es - self.ea
        self.ra = calcs._ra_hourly(self.lat, self.lon, self.doy, self.time_mid, method)
        if method == 'asce':
            self.rso = calcs._rso_simple(self.ra, self.elev)
        else:
            if method == 'refet':
                self.rso = calcs._rso_hourly(self.ra, self.ea, self.pair, self.doy, self.time_mid, self.lat, self.lon, method)
        self.fcd = calcs._fcd_hourly(self.rs, self.rso, self.doy, self.time, self.lat, self.lon, method)
        self.rnl = calcs._rnl_hourly(self.tmean, self.ea, self.fcd)
        self.rn = calcs._rn_hourly(self.rs, self.rnl)
        self.u2 = calcs._wind_height_adjust(self.uz, self.zw)

    def etsz(self, surface):
        """Standardized reference ET

        Parameters
        ----------
        surface : {'alfalfa', 'etr', 'tall', 'grass', 'eto', 'short'}
            Reference surface type.

        Returns
        -------
        ndarray

        """
        if surface.lower() in ('alfalfa', 'etr', 'tall'):
            return self.etr()
        if surface.lower() in ('grass', 'eto', 'short'):
            return self.eto()
        raise ValueError('unsupported surface type: {}'.format(surface))

    def eto(self):
        """Short (grass) reference surface"""
        self.cn = 37.0
        self.cd = np.full(self.rn.shape, 0.24)
        self.g_rn = np.full(self.rn.shape, 0.1)
        self.cd[self.rn < 0] = 0.96
        self.g_rn[self.rn < 0] = 0.5
        self.g = self.rn * self.g_rn
        return calcs._etsz(rn=(self.rn),
          g=(self.g),
          tmean=(self.tmean),
          u2=(self.u2),
          vpd=(self.vpd),
          es_slope=(self.es_slope),
          psy=(self.psy),
          cn=(self.cn),
          cd=(self.cd))

    def etr(self):
        """Tall (alfalfa) reference surface"""
        self.cn = 66.0
        self.cd = np.full(self.rn.shape, 0.25)
        self.g_rn = np.full(self.rn.shape, 0.04)
        self.cd[self.rn < 0] = 1.7
        self.g_rn[self.rn < 0] = 0.2
        self.g = self.rn * self.g_rn
        return calcs._etsz(rn=(self.rn),
          g=(self.g),
          tmean=(self.tmean),
          u2=(self.u2),
          vpd=(self.vpd),
          es_slope=(self.es_slope),
          psy=(self.psy),
          cn=(self.cn),
          cd=(self.cd))