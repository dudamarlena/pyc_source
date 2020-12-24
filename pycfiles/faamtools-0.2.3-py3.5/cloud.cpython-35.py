# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faamtools/cloud.py
# Compiled at: 2016-03-08 08:50:31
# Size of source mod 2**32: 7718 bytes
"""
Functions to read data from 2DS, CIP, CDP, Nevzorov cloud probes
"""
import datetime, netCDF4 as nc, numpy as np, warnings
from . import utils

def read_nevzorov_nc(fname, tbase=None, tstep_sec=None, time2datetime=True, interpnan=True):
    """
    Read data from Nevzorov probe stored in NetCDF file.

    Example: read_nevzorov_nc('b763_nevzorov_20130326_1hz_r1.nc',
                               tbase=datetime.datetime(2013,3,26), tstep_sec=1)

    Args:
    -----
        fname: str, file name
    Kwargs:
    -------
        tbase: datetime.datetime, time start. If None, will be extracted from time units
        tstep_sec: numeric, time frequency in seconds. If None, will be extracted from time units
        time2datetime: boolean, optional.
                       If True, convert time array to `datetime.datetime` objects.
                       Defaults to True.
    Returns:
    --------
        probe_time: array-like of observations time
        twc_liq: array-like of condensed water content from TWC sensor, [kg m :sup:`-3`]
        twc_ice: array-like of condensed water content from TWC sensor, [kg m :sup:`-3`]
        lwc_liq: array-like of condensed water content from LWC sensor, [kg m :sup:`-3`]
        lwc_ice: array-like of condensed water content from LWC sensor, [kg m :sup:`-3`]
    """
    with nc.Dataset(fname) as (dataset):
        probe_time = dataset['TIME']
        probe_time_val = probe_time[:]
        if time2datetime:
            if tbase is None and tstep_sec is None and hasattr(probe_time, 'units'):
                try:
                    tbase, tstep_sec = utils.timestr2datetime(probe_time.units)
                except ValueError:
                    warnings.warn('Unable to parse time units correctly, return the original time values')

                probe_time_val = np.array([tbase + datetime.timedelta(seconds=int(x) * tstep_sec) for x in probe_time_val])
        twc_liq = dataset['TWC_Q_liq'][:] * 0.001
        twc_ice = dataset['TWC_Q_ice'][:] * 0.001
        lwc_liq = dataset['LWC_Q_liq'][:] * 0.001
        lwc_ice = dataset['LWC_Q_ice'][:] * 0.001
    if interpnan:
        twc_liq, twc_ice, lwc_liq, lwc_ice = [utils.interp_nan(i) for i in (twc_liq, twc_ice, lwc_liq, lwc_ice)]
    return (probe_time_val, twc_liq, twc_ice, lwc_liq, lwc_ice)


def read_cloud_hdf(fname, tbase=datetime.datetime(2013, 3, 26), time2datetime=True, interpnan=True):
    """
    Read cloud particle data from HDF5 file. Requires `h5py` package.
    Sum mass concentration data over all channels and convert to [kg m :sup:`-3`].

    Instruments: 2DS, CIP

    Input file has usuallly name ending in '_v1.h5' and contains cloud particle data categorised as following:

    S - Small - All particles too small to be further categorised. (2DS cut-off = 50, all other cut-off = 30)
    LI - Low Irregular - All particles larger than the small cut off with Sphericity between 0.9 and 1.2
    MI - Med Irregular - All particles larger than the small cut off with Sphericity between 1.2 and 1.4
    HI - High Irregular - All particles larger than the small cut off with Sphericity greater than 1.4
    E - Edge - All particles that touch the edge of the array cannot be accurately categorised at present

    Units:
    Time - seconds from midnight
    Size - micrometres
    Number concentration - #/litre
    Mass concentration - g/m3

    Args:
    -----
        fname: str, file name
    Kwargs:
    -------
        tbase: datetime.datetime, time start. Defaults to datetime.datetime(2013, 3, 26, 0, 0, 0).
        time2datetime: boolean, optional.
                       If True, convert time array to `datetime.datetime` objects
                       adding time values to `tbase` kwarg.
                       Defaults to True.
    Returns:
    --------
        time: array-like of observations time
        li_mc: array-like, mass concentration of LI [kg m :sup:`-3`]
        mi_mc: array-like, mass concentration of MI [kg m :sup:`-3`]
        hi_mc: array-like, mass concentration of HI [kg m :sup:`-3`]
        e_mc: array-like, mass concentration of Edge [kg m :sup:`-3`]
    """
    import h5py
    with h5py.File(fname) as (dataset):
        probe_time = dataset['Time_mid']
        if time2datetime:
            probe_time = np.array([tbase + datetime.timedelta(seconds=i) for i in probe_time.value])
        else:
            probe_time = probe_time.value
        li_mc = np.nansum(dataset['PSD_Mass_LI'].value, 1)
        mi_mc = np.nansum(dataset['PSD_Mass_MI'].value, 1)
        hi_mc = np.nansum(dataset['PSD_Mass_HI'].value, 1)
        e_mc = np.nansum(dataset['PSD_Mass_E'].value, 1)
    li_mc, mi_mc, hi_mc, e_mc = [i * 0.001 for i in (li_mc, mi_mc, hi_mc, e_mc)]
    if interpnan:
        li_mc, mi_mc, hi_mc, e_mc = [utils.interp_nan(i) for i in (li_mc, mi_mc, hi_mc, e_mc)]
    return (probe_time, li_mc, mi_mc, hi_mc, e_mc)


def read_cdp_nc(fname, tbase=None, tstep_sec=None, time2datetime=True, interpnan=True):
    """
    Read CDP data from a NetCDF file.

    Args:
    -----
        fname: str, file name
    Kwargs:
    -------
        tbase: datetime.datetime, time start. If None, will be extracted from time units
        tstep_sec: numeric, time frequency in seconds. If None, will be extracted from time units
        time2datetime: boolean, optional.
                       If True, convert time array to `datetime.datetime` objects.
                       Defaults to True.
    Returns:
    --------
        probe_time_val: array-like of observations time
        cdp_lwc_dens: liquid water content density [kg m :sup:`-3`]
    """
    with nc.Dataset(fname) as (cdp):
        probe_time = cdp['Time']
        probe_time_val = probe_time[:]
        if time2datetime:
            if tbase is None and tstep_sec is None and hasattr(probe_time, 'units'):
                try:
                    tbase, tstep_sec = utils.timestr2datetime(probe_time.units)
                except ValueError:
                    warnings.warn('Unable to parse time units correctly, return the original time values')

                probe_time_val = np.array([tbase + datetime.timedelta(seconds=int(x) * tstep_sec) for x in probe_time_val])
        ch_lims = np.vstack((cdp['CDP_D_L_NOM'][:], cdp['CDP_D_U_NOM'][:]))
        ch_mean_diam = np.mean(ch_lims, 0)
        ch_mean_vol = 1.3333333333333333 * np.pi * (0.5 * ch_mean_diam) ** 3
        h2o_d = 9.9997e-13
        ch_mean_mass = ch_mean_vol * h2o_d
        assert len(ch_mean_mass) == len(cdp['CDP_D_L_NOM'][:]), 'Check the shape of arrays'
        cdp_lwc_dens_all_ch = []
        for ich, mass in enumerate(ch_mean_mass):
            cdp_conc = cdp['CDP_{0:02d}'.format(ich + 1)][:]
            cdp_conc[cdp['CDP_FLAG'][:] != 0] = np.nan
            cdp_lwc_g_per_m3 = cdp_conc * mass * 1000000.0
            cdp_lwc_dens_all_ch.append(cdp_lwc_g_per_m3 * 0.001)

        cdp_lwc_dens = sum(np.array(cdp_lwc_dens_all_ch))
    if interpnan:
        cdp_lwc_dens = utils.interp_nan(cdp_lwc_dens)
    return (probe_time_val, cdp_lwc_dens)