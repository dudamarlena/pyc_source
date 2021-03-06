# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fluid/DataSet.py
# Compiled at: 2006-12-04 09:19:16
import fluid.atmosphere.atmospheric_functions, fluid.common.common

class Atmosphere(object):
    """Class for atmospheric related functions
    """
    __module__ = __name__

    def __init__(self, Ta=None, p=None):
        """Define variables default values
        """
        pass

    def _getTa(self):
        return self.__Ta

    def _setTa(self, Ta):
        self.__Ta = Ta
        self.recalculate()

    Ta = property(_getTa, _setTa)

    def _getp(self):
        return self.__p

    def _setp(self, p):
        self.__p = p
        self.recalculate()

    p = property(_getp, _setp)

    def _getRH(self):
        return self.__RH

    def _setRH(self, RH):
        self.__RH = RH
        self.recalculate()

    RH = property(_getRH, _setRH)

    def _getrho_air(self):
        return fluid.atmosphere.atmospheric_functions.air_density(self.p, self.Kv)

    def _setrho_air(self, rho_air):
        pass

    rho_air = property(_getrho_air, _setrho_air)

    def default_values(self):
        """Default variables values

        """
        pass

    def _need(self, who):
        """
        """
        for dependence in who:
            if not hasattr(self, dependence):
                return

        return 1

    def set_air_viscosity(self):
        """
        """
        print 'Hey ho!'
        if hasattr(self, 'nu_air'):
            return
        if self._need(['Ta']):
            self.nu_air = fluid.atmosphere.atmospheric_functions.air_viscosity(self.Ta)
        print self.nu_air

    def set_saturation_vapor_pressure(self):
        """
        """
        if hasattr(self, 'es'):
            return
        if self._need(['Ta']):
            self.es = fluid.atmosphere.atmospheric_functions.saturation_vapor_pressure(self.Ta)

    def set_saturation_mixing_ratio(self):
        """
        """
        if hasattr(self, 'ws'):
            return
        if self._need(['Ta', 'p']):
            self.ws = fluid.atmosphere.atmospheric_functions.saturation_mixing_ratio(self.Ta, self.p)

    def set_saturation_specific_humidity(self):
        """
        """
        if hasattr(self, 'qs'):
            return
        if self._need(['ws']):
            self.qs = fluid.atmosphere.atmospheric_functions.specific_humidity(self.ws)

    def set_vapor_pressure(self):
        """
        """
        if hasattr(self, 'ea'):
            return
        if self._need(['w', 'p']):
            self.ea = fluid.atmosphere.atmospheric_functions.vapor_pressure(self.w, self.p)
        elif self._need(['RH', 'ws', 'p']):
            self.ea = fluid.atmosphere.atmospheric_functions.RH2e(self.RH, self.ws, self.p)

    def set_mixing_ratio(self):
        """
        """
        if hasattr(self, 'w'):
            return
        if self._need(['ea', 'p']):
            self.w = fluid.atmosphere.atmospheric_functions.mixing_ratio(self.ea, self.p)
        elif self._need(['RH', 'ws']):
            self.w = fluid.atmosphere.atmospheric_functions.RH2w(self.RH, self.ws)

    def set_specific_humidity(self):
        """
        """
        if hasattr(self, 'q'):
            return
        if self._need(['w']):
            self.q = fluid.atmosphere.atmospheric_functions.specific_humidity(self.w)

    def set_virtual_temperature(self):
        """
        """
        if hasattr(self, 'Tv'):
            return
        if self._need(['Ta', 'ea', 'p']):
            self.Tv = fluid.atmosphere.atmospheric_functions.virtual_temperature(self.Ta, self.ea, self.p)
            self.Kv = fluid.common.common.C2K(self.Tv)

    def recalculate(self):
        self.set_air_viscosity()
        self.set_saturation_vapor_pressure()
        self.set_saturation_mixing_ratio()
        self.set_saturation_specific_humidity()
        self.set_mixing_ratio()
        self.set_vapor_pressure()
        self.set_specific_humidity()
        self.set_virtual_temperature()


class Seawater(object):
    """Class for ocean related functions
    """
    __module__ = __name__

    def __init__(self, SST=None):
        """Define variables default values
        """
        pass

    def _getSST(self):
        return self.__SST

    def _setSST(self, SST):
        self.__SST = SST

    SST = property(_getSST, _setSST)


import fluid.interaction.heat_flux, fluid.interaction.others, fluid.common.common

class HeatFlux(object):
    """Class for heat fluxes related functions
    """
    __module__ = __name__

    def __init__(self, Ta=None, p=None):
        """Define variables default values
        """
        self.Atm = Atmosphere()
        self.Water = Seawater()

    def _getTa(self):
        return self.__Ta

    def _setTa(self, Ta):
        self.__Ta = Ta
        self.Atm.Ta = Ta
        self.recalculate()

    Ta = property(_getTa, _setTa)

    def _getKa(self):
        return fluid.common.common.C2K(self.Ta)

    def _setKa(self, Ka):
        self.__Ta = fluid.common.common.K2C(Ka)
        self.recalculate()

    Ka = property(_getKa, _setKa)

    def _getTv(self):
        return self.Atm.Tv

    def _setTv(self, Tv):
        self.Atm.Tv = Tv
        self.Atm.recalculate()
        self.recalculate()

    Tv = property(_getTv, _setTv)

    def _getRH(self):
        return self.Atm.RH

    def _setRH(self, RH):
        self.Atm.RH = RH
        self.recalculate()

    RH = property(_getRH, _setRH)

    def _getp(self):
        return self.Atm.p

    def _setp(self, p):
        self.Atm.p = p
        self.recalculate()

    p = property(_getp, _setp)

    def _getea(self):
        return self.Atm.ea

    def _setea(self, ea):
        self.Atm.ea = ea
        self.recalculate()

    ea = property(_getea, _setea)

    def _getq(self):
        return self.Atm.q

    def _setq(self, q):
        self.Atm.q = q
        self.recalculate()

    q = property(_getq, _setq)

    def _getnu_air(self):
        return self.Atm.nu_air

    def _setnu_air(self, nu_air):
        self.Atm.nu_air = nu_air
        self.recalculate()

    nu_air = property(_getnu_air, _setnu_air)

    def _getrho_air(self):
        return self.Atm.rho_air

    def _setrho_air(self, rho_air):
        self.Atm.rho_air = rho_air
        self.recalculate()

    rho_air = property(_getrho_air, _setrho_air)

    def _getSST(self):
        return self.Water.SST

    def _setSST(self, SST):
        self.Water.SST = SST
        self.recalculate()

    SST = property(_getSST, _setSST)

    def _getq_sea(self):
        ws_sea = fluid.atmosphere.atmospheric_functions.saturation_mixing_ratio(self.SST, self.p)
        return 0.98 * fluid.atmosphere.atmospheric_functions.specific_humidity(ws_sea)

    def _setq_sea(self, q_sea):
        pass

    q_sea = property(_getq_sea, _setq_sea)

    def _getLe(self):
        return fluid.interaction.others.latent_heat(self.SST)

    def _setLe(self, Le):
        pass

    Le = property(_getLe, _setLe)

    def _getQswi(self):
        return self.__Qswi

    def _setQswi(self, Qswi):
        self.__Qswi = Qswi
        self.recalculate()

    Qswi = property(_getQswi, _setQswi)

    def _getz_0(self):
        return self.__z_0

    def _setz_0(self, z_0):
        self.__z_0 = z_0
        self.recalculate()

    z_0 = property(_getz_0, _setz_0)

    def default_values(self):
        """Default variables values

        """
        pass

    def _need(self, who):
        """
        """
        for dependence in who:
            if not hasattr(self, dependence):
                return

        return 1

    def set_short_wave(self):
        """
        """
        if hasattr(self, 'Qsw'):
            return
        if self._need(['Qswi']):
            self.Qsw = fluid.interaction.heat_flux.short_wave_radiation(self.Qswi)

    def set_NSA(self):
        """
        """
        if hasattr(self, 'NSA'):
            return
        if self._need(['DOY', 'Lat']):
            self.NSA = fluid.interaction.heat_flux.noon_solar_altitude(self.DOY, self.Lat)

    def set_short_wave_clear_sky(self):
        """
        """
        if hasattr(self, 'Qcs'):
            return
        if self._need(['DOY', 'Lat']):
            self.Qcs = fluid.interaction.heat_flux.short_wave_clear_sky(self.Lat, self.DOY)

    def set_cloud_cover_fraction(self):
        """
        """
        if hasattr(self, 'FracQ'):
            return
        if self._need(['Qswi', 'Qcs']):
            self.FracQ = self.Qswi / self.Qcs

    def set_cloud_cover(self):
        """
        """
        if hasattr(self, 'C'):
            return
        if self._need(['Lat', 'FracQ', 'NSA']):
            self.C = fluid.interaction.heat_flux.cloud_cover(self.Lat, self.FracQ, self.NSA)

    def set_long_wave_radiation(self):
        """
        """
        if hasattr(self, 'Qlw'):
            return
        print hasattr(self, 'C')
        if self._need(['SST', 'Ta', 'ea', 'C', 'Lat']):
            self.Qlw = fluid.interaction.heat_flux.long_wave_radiation(self.SST, self.Ta, self.ea, self.C, self.Lat)

    def set_u_star(self):
        """
        """
        if hasattr(self, 'u_star'):
            return
        if self._need(['U', 'nu_air', 'z_u']):
            self.u_star = fluid.interaction.others.find_u_star(self.U, self.nu_air, self.z_u)

    def set_transfer_coefficients(self):
        """
        """
        if hasattr(self, 'T_star') & hasattr(self, 'q_star'):
            return
        if self._need(['Ta', 'Tv', 'SST', 'q', 'q_sea', 'U', 'z_u', 'z_T', 'z_q', 'nu_air', 'u_star']):
            (self.u_star, self.T_star, self.q_star) = fluid.interaction.others.find_transfer_coefficients(self.Ta, self.Tv, self.SST, self.q, self.q_sea, self.U, self.z_u, self.z_T, self.z_q, self.nu_air, self.u_star)

    def set_tubulent_heat_fluxes(self):
        """
        """
        if hasattr(self, 'Hs') & hasattr(self, 'Hl'):
            return
        if self._need(['u_star', 'T_star', 'q_star', 'Le']):
            (self.Hs, self.Hl) = fluid.interaction.others.turbulent_heat_fluxes(self.Atm.rho_air, self.u_star, self.T_star, self.q_star, self.Le)

    def recalculate(self):
        self.set_short_wave()
        self.set_NSA()
        self.set_short_wave_clear_sky()
        self.set_cloud_cover_fraction()
        self.set_cloud_cover()
        self.set_long_wave_radiation()
        self.set_u_star()
        self.set_transfer_coefficients()