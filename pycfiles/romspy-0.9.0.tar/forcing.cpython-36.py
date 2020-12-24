# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicomuen/PycharmProjects/roms_tools/romspy/settings/forcing.py
# Compiled at: 2019-09-04 06:14:29
# Size of source mod 2**32: 7036 bytes
"""
Author: Nicolas Munnich
License: GNU GPL2+
"""

def str_adjustment(preprocessor, file: str, group_files: str, flags: dict):
    """
    Add attributes to sustr and svstr
    :param preprocessor: PreProcessor object, contains a lot of necessary settings
    :param file: file which contains all necessary parameters to calculate dQdSST
    :param group_files: list of all files which contain necessary parameters to calculate dQdSST
    :param flags: any extra info necessary
    :return:
    """
    if preprocessor.verbose:
        print('Adjusting for surface stress')
    preprocessor.cdo.setattribute(("sustr@long_name='surface u-momentum stress',svstr@long_name='surface v-momentum stress',sustr@unit='Newton meter-2',svstr@unit='Newton meter-2',sustr@files='" + group_files + "',svstr@files='" + group_files + "'"),
      input=file, output=file, options=(preprocessor.options))
    if preprocessor.verbose:
        print('surface stress has been added')


def dust_adjustment(preprocessor, file: str, group_files: str, flags: dict):
    """
    Calculate iron
    :param preprocessor: PreProcessor object, contains a lot of necessary settings
    :param file: file which contains all necessary parameters to calculate dQdSST
    :param group_files: list of all files which contain necessary parameters to calculate dQdSST
    :param flags: any extra info necessary
    :return:
    """
    if preprocessor.verbose:
        print('Adjusting dust to add iron')
    iron_factor = 62668.0
    preprocessor.cdo.setattribute(("iron@long_name='iron_flux',iron@units='nmol/cm2/s',iron@files='" + group_files + "'"),
      input=("-aexpr,'iron=" + str(iron_factor) + " * dust' " + file),
      options=(preprocessor.options),
      output=file)
    if preprocessor.verbose:
        print('Iron has been added')


def swflux_adjustment(preprocessor, file: str, group_files: str, flags: dict):
    """
    Calculate surface fresh water flux
    :param preprocessor: PreProcessor object, contains a lot of necessary settings
    :param file: file which contains all necessary parameters to calculate dQdSST
    :param group_files: list of all files which contain necessary parameters to calculate dQdSST
    :param flags: any extra info necessary
    :return:
    """
    if preprocessor.verbose:
        print('Adjusting for swflux')
    preprocessor.cdo.setattribute(("swflux@long_name='surface fresh water flux',swflux@unit='cm day-1',swflux@files='" + group_files + "'"),
      input=('-delname,evap' + (',precip' if not flags['include_precip'] else '') + " -aexpr,'swflux=precip+evap' " + file),
      options=(preprocessor.options),
      output=file)
    if preprocessor.verbose:
        print('swflux has been added')


def shflux_adjustment(preprocessor, file: str, group_files: str, flags: dict):
    """
    Compute the surface net heat flux
    :param preprocessor: PreProcessor object, contains a lot of necessary settings
    :param file: file which contains all necessary parameters to calculate dQdSST
    :param group_files: list of all files which contain necessary parameters to calculate dQdSST
    :param flags: any extra info necessary
    :return:
    """
    if preprocessor.verbose:
        print('Adjusting for shflux')
    preprocessor.cdo.setattribute(("shflux@long_name='surface net heat flux',shflux@unit='Watt meter-2',shflux@files='" + group_files + "'"),
      input=("-delname,lwrad,sensheat,latheat -aexpr,'shflux=swrad+sshf+slhf+str' " + file),
      options=(preprocessor.options),
      output=file)
    if preprocessor.verbose:
        print('shflux has been added')


def dqdsst_adjustment(preprocessor, file: str, group_files: str, flags: dict):
    """
        Compute the kinematic surface net heat flux sensitivity to the sea surface temperature: dQdSST
        Q_model ~ Q + dQdSST * (T_model - SST)
        dQdSST = - 4 * eps * stef * T^3 - rho_atm * Cp * CH * U - rho_atm * CE * L * U * 2353 * ln(10 * q_s / T^2)
        SST: sea surface temperature
        t_air: sea surface atmospheric temperature
        rho_air: atmospheric density
        u_air: wind speed
        humidity: sea level specific humidity
        dQdSST: kinematic surface net heat flux sensitivity to the sea surface temperature (Watts meter-2 Celsius-1)
        :param preprocessor: PreProcessor object, contains a lot of necessary settings
        :param file: file which contains all necessary parameters to calculate dQdSST
        :param group_files: list of all files which contain necessary parameters to calculate dQdSST
        :param flags: any extra info necessary
    """
    if preprocessor.verbose:
        print('Calculating dQdSST')
    Cp = str(1004.8)
    Ch = str(0.00066)
    Ce = str(0.00115)
    stef = str(5.6697e-08)
    sstk_formula = '_sst = sst + 273.15;'
    l = '(2.008E6 - 2.3E3 * t_air)'
    q1 = '(-4.0 * ' + stef + '* _sst * _sst * _sst)'
    q2 = '(-rho_air * ' + Cp + ' * ' + Ch + '* u_air)'
    dqsdt = '(5417.9827238149900949792936444282531738281250 * humidity / (_sst * _sst))'
    q3 = '(-rho_air * ' + Ce + ' * ' + l + ' * u_air * ' + dqsdt + ' )'
    dqdsst_formula = "'" + sstk_formula + 'dQdSST=' + q1 + ' + ' + q2 + ' + ' + q3 + "'"
    preprocessor.cdo.setattribute(("dQdSST@long_name='surface net heat flux sensitivity to SST',dQdSST@unit='Watts meter-2 Celsius-1',dQdSST@files='" + group_files + "'"),
      input=('-delname,sat,rho_atm,U,qsea -aexpr,' + dqdsst_formula + ' ' + file),
      options=(preprocessor.options),
      output=file)
    if preprocessor.verbose:
        print('dQdSST has been added.')


forcing_adjustments = [
 {'out_var_names':set(), 
  'in_var_names':{'sustr', 'svstr'},  'func':str_adjustment},
 {'out_var_names':{
   'shflux'}, 
  'in_var_names':{'swrad', 'lwrad', 'sensheat', 'latheat'},  'func':shflux_adjustment},
 {'out_var_names':{
   'swflux'}, 
  'in_var_names':{'evap', 'precip'},  'flags':'include_precip',  'func':swflux_adjustment},
 {'out_var_names':{
   'iron'}, 
  'in_var_names':{'dust'},  'func':dust_adjustment},
 {'out_var_names':{
   'dQdSST'}, 
  'in_var_names':{'SST', 't_air', 'rho_air', 'u_air', 'humidity'},  'func':dqdsst_adjustment}]