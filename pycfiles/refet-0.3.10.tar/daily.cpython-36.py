# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\RefET\refet\daily.py
# Compiled at: 2019-02-26 15:00:13
# Size of source mod 2**32: 9407 bytes
import math, numpy as np
from . import calcs

class Daily:

    def __init__(self, tmin, tmax, ea, rs, uz, zw, elev, lat, doy, method='asce', rso_type=None, rso=None, input_units={}):
        """ASCE Daily Standardized Reference Evapotranspiration (ET)

        Arguments
        ---------
        tmin : ndarray
            Minimum daily temperature [C].
        tmax : ndarray
            Maximum daily temperature [C].
        ea : ndarray
            Actual vapor pressure [kPa].
        rs : ndarray
            Incoming shortwave solar radiation [MJ m-2 day-1].
        uz : ndarray
            Wind speed [m s-1].
        zw : float
            Wind speed height [m].
        elev : ndarray
            Elevation [m].
        lat : ndarray
            Latitude [degrees].
        doy : ndarray
            Day of year.
        method : {'asce' (default), 'refet'}, optional
            Specifies which calculation method to use.
            * 'asce' -- Calculations will follow ASCE-EWRI 2005 [1]_ equations.
            * 'refet' -- Calculations will follow RefET software.
        rso_type : {None (default), 'full' , 'simple', 'array'}, optional
            Specifies which clear sky solar radiation (Rso) model to use.
            * None -- Rso type will be determined from "method" parameter
            * 'full' -- Full clear sky solar formulation
            * 'simple' -- Simplified clear sky solar formulation
            * 'array' -- Read Rso values from "rso" function parameter
        rso : array_like or None, optional
            Clear sky solar radiation [MJ m-2 day-1] (the default is None).
            Only used if rso_type == 'array'.
        input_units : dict, optional
            Input unit types.

        Returns
        -------
        etsz : ndarray
            Standardized reference ET [mm].

        Notes
        -----
        cn: 900 for ETo, 1600 for ETr
        cd: 0.34 for ETo, 0.38 for ETr

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
        self.tmin = np.array(tmin, copy=True, ndmin=1)
        self.tmax = np.array(tmax, copy=True, ndmin=1)
        self.ea = np.array(ea, copy=True, ndmin=1)
        self.rs = np.array(rs, copy=True, ndmin=1)
        self.uz = np.array(uz, copy=True, ndmin=1)
        self.elev = np.array(elev, copy=True, ndmin=1)
        self.lat = np.array(lat, copy=True, ndmin=1)
        self.zw = zw
        self.doy = doy
        for variable, unit in input_units.items():
            if unit == '':
                continue
            else:
                if unit.lower() in ('c', 'celsius', 'mj m-2 day-1', 'mj m-2 d-1', 'kpa',
                                    'm s-1', 'm/s', 'm', 'meter', 'meters', 'deg',
                                    'degree', 'degrees'):
                    continue
                else:
                    if unit.lower() not in ('k', 'kelvin', 'f', 'fahrenheit', 'pa',
                                            'langleys', 'w m-2', 'w/m2', 'mph', 'ft',
                                            'feet', 'rad', 'radian', 'radians'):
                        raise ValueError('unsupported unit conversion for {} {}'.format(variable, unit))
            if variable == 'tmax':
                if unit.lower() in ('f', 'fahrenheit'):
                    self.tmax -= 32
                    self.tmax *= 0.5555555555555556
                elif unit.lower() in ('k', 'kelvin'):
                    self.tmax -= 273.15
            else:
                if variable == 'tmin':
                    if unit.lower() in ('f', 'fahrenheit'):
                        self.tmin -= 32
                        self.tmin *= 0.5555555555555556
                    elif unit.lower() in ('k', 'kelvin'):
                        self.tmin -= 273.15
                else:
                    if variable == 'ea':
                        if unit.lower() in ('pa', ):
                            self.ea /= 1000.0
                    else:
                        if variable == 'rs':
                            if unit.lower() in ('langleys', ):
                                self.rs *= 0.041868
                            elif unit.lower() in ('w m-2', 'w/m2'):
                                self.rs *= 0.0864
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

        if method.lower() not in ('asce', 'refet'):
            raise ValueError('method must be "asce" or "refet"')
        if rso_type is None:
            pass
        else:
            if rso_type.lower() not in ('simple', 'full', 'array'):
                raise ValueError('rso_type must be None, "simple", "full", or "array')
            else:
                if rso_type.lower() in 'array':
                    pass
                self.lat *= math.pi / 180.0
                self.pair = calcs._air_pressure(self.elev, method)
                self.psy = 0.000665 * self.pair
                self.tmean = 0.5 * (self.tmax + self.tmin)
                self.es_slope = calcs._es_slope(self.tmean, method)
                self.es = 0.5 * (calcs._sat_vapor_pressure(self.tmax) + calcs._sat_vapor_pressure(self.tmin))
                self.vpd = calcs._vpd(self.es, self.ea)
                self.ra = calcs._ra_daily(self.lat, self.doy, method)
                if rso_type is None:
                    if method.lower() == 'asce':
                        self.rso = calcs._rso_simple(self.ra, self.elev)
                    else:
                        if method.lower() == 'refet':
                            self.rso = calcs._rso_daily(self.ra, self.ea, self.pair, self.doy, self.lat)
                else:
                    if rso_type.lower() == 'simple':
                        self.rso = calcs._rso_simple(self.ra, elev)
                    else:
                        if rso_type.lower() == 'full':
                            self.rso = calcs._rso_daily(self.ra, self.ea, self.pair, self.doy, self.lat)
                        elif rso_type.lower() == 'array':
                            self.rso = rso
            self.fcd = calcs._fcd_daily(self.rs, self.rso)
            self.rnl = calcs._rnl_daily(self.tmax, self.tmin, self.ea, self.fcd)
            self.rn = calcs._rn_daily(self.rs, self.rnl)
            self.g = 0
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
        """Grass reference surface"""
        self.cn = 900
        self.cd = 0.34
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
        """Alfalfa reference surface"""
        self.cn = 1600
        self.cd = 0.38
        return calcs._etsz(rn=(self.rn),
          g=(self.g),
          tmean=(self.tmean),
          u2=(self.u2),
          vpd=(self.vpd),
          es_slope=(self.es_slope),
          psy=(self.psy),
          cn=(self.cn),
          cd=(self.cd))