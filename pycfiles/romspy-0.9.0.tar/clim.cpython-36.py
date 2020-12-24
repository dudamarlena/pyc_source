# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicomuen/PycharmProjects/roms_tools/romspy/settings/clim.py
# Compiled at: 2019-09-04 10:20:40
# Size of source mod 2**32: 4207 bytes
from romspy.interpolation.vertical.levels import z_levels, sigma_stretch_cs, sigma_stretch_sc
from romspy.interpolation.shift_grid import shift
import netCDF4, numpy as np

def stress_bar_adjustment(preprocessor, file: str, group_files: str, flags: dict):
    if preprocessor.verbose:
        print('Getting ubar and vbar')
    h = preprocessor.h
    sc = sigma_stretch_sc(preprocessor.vertical_options['layers'], False)
    cs = sigma_stretch_cs(preprocessor.vertical_options['theta_s'], preprocessor.vertical_options['theta_b'], sc, preprocessor.vertical_options['sigma_type'])
    hc = preprocessor.hc
    zeta = preprocessor.zeta
    delta_z_levs_u = z_levels((shift(h, 1)), sc, cs, hc, (shift(zeta, 1)), sigma_type=3, verbose=(preprocessor.verbose))
    delta_z_levs_u = delta_z_levs_u[1:] - delta_z_levs_u[:-1]
    delta_z_levs_u_inv = 1 / sum(delta_z_levs_u)
    delta_z_levs_v = z_levels((shift(h, 2)), sc, cs, hc, (shift(zeta, 2)), sigma_type=3, verbose=(preprocessor.verbose))
    delta_z_levs_v = delta_z_levs_v[1:] - delta_z_levs_v[:-1]
    delta_z_levs_v_inv = 1 / sum(delta_z_levs_v)
    with netCDF4.Dataset(file, mode='r+') as (my_file):
        time_len = len(my_file.dimensions['time'])
        ubar = my_file.createVariable('ubar', 'f', ('time', 'eta_rho', 'xi_u'))
        vbar = my_file.createVariable('vbar', 'f', ('time', 'eta_v', 'xi_rho'))
        u = my_file.variables['u']
        v = my_file.variables['v']
        u.setncattr('long_name', 'u-velocity component')
        v.setncattr('long_name', 'v-velocity component')
        ubar_attrs = {x:u.getncattr(x) for x in u.ncattrs()}
        ubar_attrs['long_name'] = 'vertically integrated u-velocity component'
        vbar_attrs = {x:v.getncattr(x) for x in v.ncattrs()}
        vbar_attrs['long_name'] = 'vertically integrated v-velocity component'
        ubar.setncatts(ubar_attrs)
        vbar.setncatts(vbar_attrs)
        with netCDF4.Dataset(preprocessor.target_grid) as (grd):
            rmask = grd.variables['mask'][:]
            pn = grd.variables['pn'][:]
            pm = grd.variables['pm'][:]
        for t in range(time_len):
            ubar_vals = sum(u[t] * delta_z_levs_u)
            vbar_vals = sum(v[t] * delta_z_levs_v)
            ubar_vals, vbar_vals = get_obcvolcons(ubar_vals, vbar_vals, pm, pn, rmask, flags['obc'], preprocessor.verbose)
            ubar_vals *= delta_z_levs_u_inv
            vbar_vals *= delta_z_levs_v_inv
            ubar[t] = ubar_vals
            vbar[t] = vbar_vals


def get_obcvolcons(ubar, vbar, pm, pn, rmask, obc, verbose):
    """
    Enforce integral flux conservation around the domain
    :param ubar: u averaged over depth
    :param vbar: v averaged over depth
    :param pm: curvilinear coordinate metric in xi
    :param pn: curvilinear coordinate metric in eta
    :param rmask: rho-grid mask
    :param obc: open boundary conditions, (1=open 0=closed, [S E N W])
    :param verbose: whether to print runtime information
    :return: 
    """
    umask = 2 * shift(rmask, 1)
    vmask = 2 * shift(rmask, 2)
    dy_u = 2 * umask / (2 * shift(pn, 1))
    dx_v = 2 * vmask / (2 * shift(pm, 2))
    udy = ubar * dy_u
    vdx = vbar * dx_v
    flux = obc[0] * np.sum(vdx[1:, 0]) - obc[1] * np.sum(udy[-1, 1:]) - obc[2] * np.sum(vdx[1:, -1]) + obc[3] * np.sum(udy[0, 1:])
    cross = obc[0] * np.sum(dx_v[1:, 0]) + obc[1] * np.sum(dy_u[-1, 1:]) + obc[2] * np.sum(dx_v[1:, -1]) + obc[3] * np.sum(dy_u[0, 1:])
    vcorr = flux / cross
    if verbose:
        print('Flux correction: ' + str(vcorr))
    vbar[:, 0] = obc[0] * (vbar[:, 0] - vcorr)
    ubar[-1, :] = obc[1] * (ubar[-1, :] + vcorr)
    vbar[:, -1] = obc[2] * (vbar[:, -1] + vcorr)
    ubar[0, :] = obc[3] * (ubar[0, :] - vcorr)
    ubar = ubar * umask
    vbar = vbar * vmask
    return (ubar, vbar)


clim_adjustments = [
 {'out_var_names':{
   'ubar', 'vbar'}, 
  'in_var_names':{'u', 'v'},  'flags':'obc',  'func':stress_bar_adjustment}]