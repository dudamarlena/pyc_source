# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mortonc/Projects/RefET-GEE/geerefet/hourly.py
# Compiled at: 2019-12-06 19:22:41
# Size of source mod 2**32: 11049 bytes
import math, ee
from . import calcs

class Hourly:

    def __init__(self, tmean, ea, rs, uz, zw, elev, lat, lon, doy, time, method='asce'):
        """ASCE Hourly Standardized Reference Evapotranspiration (ET)

        .. warning:: Cloudiness fraction at night is not being computed per [1]_

        Arguments
        ---------
        tmean : ee.Image
            Average hourly temperature [C].
        ea : ee.Image
            Actual vapor pressure [kPa].
        rs : ee.Image
            Shortwave solar radiation [MJ m-2 hr-1].
        uz : ee.Image
            Wind speed [m s-1].
        zw : ee.Number
            Wind speed measurement/estimated height [m].
        elev : ee.Image or ee.Number
            Elevation [m]
        lat : ee.Image or ee.Number
            Latitude [degrees]
        lon : ee.Image or ee.Number
            Longitude [degrees].
        doy : ee.Number
            Day of year.
        time : ee.Number
            UTC hour at start of time period.
        method : {'asce' (default), 'refet'}, optional
            Specifies which calculation method to use.
            * 'asce' -- Calculations will follow ASCE-EWRI 2005 [1].
            * 'refet' -- Calculations will follow RefET software.

        Raises
        ------
        ValueError
            If 'method' parameter is invalid.

        Notes
        -----
        Divide solar radiation values by 0.0036 to convert MJ m-2 hr-1 to W m-2.
        Latitude & longitude units are degress, not radians.

        References
        ----------
        .. [1] ASCE-EWRI (2005). The ASCE standardized reference evapotranspiration
            equation. ASCE-EWRI Standardization of Reference Evapotranspiration
            Task Committee Rep., ASCE Reston, Va.
            http://www.kimberly.uidaho.edu/water/asceewri/ascestzdetmain2005.pdf
            http://www.kimberly.uidaho.edu/water/asceewri/appendix.pdf

        """
        if method.lower() not in ('asce', 'refet'):
            raise ValueError('method must be "asce" or "refet"')
        self.time_start = ee.Image(tmean).get('system:time_start')
        self.date = ee.Date(self.time_start)
        self.tmean = tmean
        self.ea = ea
        self.rs = rs
        self.uz = uz
        self.zw = zw
        self.elev = elev
        self.lat = lat.multiply(math.pi / 180)
        self.lon = lon.multiply(math.pi / 180)
        self.doy = doy
        self.time = time
        self.pair = calcs._air_pressure((self.elev), method=method)
        self.psy = self.pair.multiply(0.000665)
        self.es = calcs._sat_vapor_pressure(self.tmean)
        self.es_slope = calcs._es_slope(self.tmean, method)
        self.vpd = self.es.subtract(self.ea)
        time_mid = self.time.add(0.5)
        self.ra = calcs._ra_hourly(lat=(self.lat),
          lon=(self.lon),
          doy=(self.doy),
          time_mid=time_mid,
          method=method)
        if method == 'asce':
            self.rso = calcs._rso_simple(ra=(self.ra), elev=(self.elev))
        else:
            if method == 'refet':
                self.rso = calcs._rso_hourly(ea=(self.ea),
                  ra=(self.ra),
                  pair=(self.pair),
                  doy=(self.doy),
                  time_mid=time_mid,
                  lat=(self.lat),
                  lon=(self.lon),
                  method=method)
        self.fcd = calcs._fcd_hourly(rs=(self.rs),
          rso=(self.rso),
          doy=(self.doy),
          time_mid=(self.time),
          lat=(self.lat),
          lon=(self.lon),
          method=method)
        self.rnl = calcs._rnl_hourly(tmean=(self.tmean), ea=(self.ea), fcd=(self.fcd))
        self.rn = calcs._rn(self.rs, self.rnl)
        self.u2 = calcs._wind_height_adjust(uz=(self.uz), zw=(self.zw))

    def etsz(self, surface):
        """Standardized reference ET

        Parameters
        ----------
        surface : {'alfalfa', 'etr', 'tall', 'grass', 'eto', 'short'}
            Reference surface type.

        Returns
        -------
        ee.Image

        """
        if surface.lower() in ('alfalfa', 'etr', 'tall'):
            return self.etr()
        if surface.lower() in ('grass', 'eto', 'short'):
            return self.eto()
        raise ValueError('unsupported surface type: {}'.format(surface))

    def eto(self):
        """Short (grass) reference surface"""
        self.cn = ee.Number(37.0)
        cd_day = 0.24
        g_rn_day = 0.1
        cd_night = 0.96
        g_rn_night = 0.5
        self.cd = self.rn.multiply(0).add(cd_day).where(self.rn.lt(0), cd_night)
        self.g_rn = self.rn.multiply(0).add(g_rn_day).where(self.rn.lt(0), g_rn_night)
        self.g = self.rn.multiply(self.g_rn)
        return ee.Image(self._etsz().rename(['eto']).set('system:time_start', self.time_start))

    def etr(self):
        """Tall (alfalfa) reference surface"""
        self.cn = ee.Number(66.0)
        cd_day = 0.25
        g_rn_day = 0.04
        cd_night = 1.7
        g_rn_night = 0.2
        self.cd = self.rn.multiply(0).add(cd_day).where(self.rn.lt(0), cd_night)
        self.g_rn = self.rn.multiply(0).add(g_rn_day).where(self.rn.lt(0), g_rn_night)
        self.g = self.rn.multiply(self.g_rn)
        return ee.Image(self._etsz().rename(['etr']).set('system:time_start', self.time_start))

    def _etsz(self):
        """Hourly reference ET (Eq. 1)

        Returns
        -------
        etsz : ee.Image
            Standardized reference ET [mm].

        """
        return self.tmean.expression('(0.408 * es_slope * (rn - g) + (psy * cn * u2 * vpd / (tmean + 273))) / (es_slope + psy * (cd * u2 + 1))', {'cd':self.cd, 
         'cn':self.cn,  'es_slope':self.es_slope,  'g':self.g, 
         'psy':self.psy,  'rn':self.rn,  'tmean':self.tmean,  'u2':self.u2, 
         'vpd':self.vpd})

    @classmethod
    def nldas(cls, input_img, zw=None, elev=None, lat=None, lon=None, method='asce'):
        """Initialize daily RefET from an NLDAS image

        Parameters
        ----------
        input_img : ee.Image
            NLDAS hourly image from the collection NASA/NLDAS/FORA0125_H002.
        zw : ee.Number, optional
            Wind speed height [m] (the default is 10).
        elev : ee.Image or ee.Number, optional
            Elevation image [m].  The SRTM elevation image (CGIAR/SRTM90_V4)
            will be reprojected to the NLDAS grid if not set.
        lat : ee.Image or ee.Number
            Latitude image [degrees].  The latitude will be computed
            dynamically using ee.Image.pixelLonLat() if not set.
        lon : ee.Image or ee.Number
            Longitude image [degrees].  The longitude will be computed
            dynamically using ee.Image.pixelLonLat() if not set.
        method : {'asce' (default), 'refet'}, optional
            Specifies which calculation method to use.
            * 'asce' -- Calculations will follow ASCE-EWRI 2005.
            * 'refet' -- Calculations will follow RefET software.

        Notes
        -----
        Solar radiation is converted from W m-2 to MJ m-2 day-1.
        Actual vapor pressure is computed from specific humidity and air
            pressure (from elevation).

        """
        image_date = ee.Date(input_img.get('system:time_start'))
        if zw is None:
            zw = ee.Number(10)
        if elev is None:
            elev = ee.Image('projects/earthengine-legacy/assets/projects/eddi-noaa/nldas/elevation')
        if lat is None:
            lat = ee.Image('projects/earthengine-legacy/assets/projects/eddi-noaa/nldas/elevation').multiply(0).add(ee.Image.pixelLonLat().select('latitude'))
        if lon is None:
            lon = ee.Image('projects/earthengine-legacy/assets/projects/eddi-noaa/nldas/elevation').multiply(0).add(ee.Image.pixelLonLat().select('longitude'))
        return cls(tmean=(input_img.select(['temperature'])),
          ea=calcs._actual_vapor_pressure(pair=(calcs._air_pressure(elev, method)),
          q=(input_img.select(['specific_humidity']))),
          rs=(input_img.select(['shortwave_radiation']).multiply(0.0036)),
          uz=(input_img.select(['wind_u']).pow(2).add(input_img.select(['wind_v']).pow(2)).sqrt().rename([
         'uz'])),
          zw=zw,
          elev=elev,
          lat=lat,
          lon=lon,
          doy=(ee.Number(image_date.getRelative('day', 'year')).add(1).double()),
          time=(ee.Number(image_date.get('hour'))),
          method=method)