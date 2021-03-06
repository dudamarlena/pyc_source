# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/generator.py
# Compiled at: 2020-03-25 17:23:14
# Size of source mod 2**32: 11796 bytes
__doc__ = '\nCreated on Wed Mar  4 13:37:00 2020\n\n@author: \nDr. Maximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nGitHub: https://github.com/MNGuenther\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os, ellc
from astropy.constants import G
from astropy import units as u
import allesfitter.exoworlds_rdx.lightcurves as lct
from .translator import translate
from . import plotter
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})

def make_lc_model(time, flux=None, flux_err=None, epoch=0.0, period=1.0, R_companion=1.0, M_companion=1.0, R_companion_unit='Rearth', M_companion_unit='Mearth', R_host=1.0, M_host=1.0, incl=90, ecc=0, omega=0, ldc=[
 0.6, 0.2], ld='quad', dil=0, sbratio=0, show_plot=False, save_plot=False, save_csv=False, fname_plot='lc.pdf', fname_csv='lc.csv'):
    """
    Inputs:
    -------
    time : array of float
        time in days
        
    Optional Inputs:
    ----------------
    flux : array of float
        flux of the 'underlying' lightcurve
    flux_err : array of float
        flux error of the 'underlying' lightcurve
    epoch : float
        epoch in days
    period : float
        period in days
    R_companion: float
        radius of the companion
        default is 1 Rearth
    M_companion: float
        mass of the companion
        default is 1 Mearth
    R_companion: float
        radius of the companion
        default is 1 Rearth
    M_companion: float
        mass of the companion
        default is 1 Mearth
    R_host : float
        radius of the star, in Rsun
        default is 1
    M_host: float
        mass of the star, in Msun
        default is 1
    show_plot : bool
        show the plot in the terminal, or close it
        default is False
    save_plot : bool
        save the plot to a file, or not
        default is False
    save_csv : bool
        save the lightcurve to a file, or not
        default is False
        
    Returns:
    --------
    model_flux : array of float
        relative flux of the model
    """
    if flux is None:
        flux = np.ones_like(time)
    else:
        if flux_err is None:
            flux_err = np.zeros_like(time)
        params = translate(quiet=True, R_companion=R_companion, M_companion=M_companion, R_companion_unit=R_companion_unit, M_companion_unit=M_companion_unit, R_host=R_host, M_host=M_host, epoch=epoch, period=period, incl=incl, ecc=ecc, omega=omega, ldc=ldc, ld=ld)

        def ellc_lc_short(time):
            return ellc.lc(t_obs=time, radius_1=(params['R_host/a']), radius_2=(params['R_companion/a']), sbratio=sbratio, incl=(params['incl']), light_3=(dil / (1.0 - dil)), t_zero=(params['epoch']), period=(params['period']), a=(params['a']), q=1, f_c=(params['f_c']), f_s=(params['f_s']), ldc_1=ldc, ldc_2=None, gdc_1=None, gdc_2=None, didt=None, domdt=None, rotfac_1=1, rotfac_2=1, hf_1=1.5, hf_2=1.5, bfac_1=None, bfac_2=None, heat_1=None, heat_2=None, lambda_1=None, lambda_2=None, vsini_1=None, vsini_2=None, t_exp=None, n_int=None, grid_1='default', grid_2='default', ld_1=ld, ld_2=None, shape_1='sphere', shape_2='sphere', spots_1=None, spots_2=None, exact_grav=False, verbose=1)

        model_flux = ellc_lc_short(time)
        flux += model_flux - 1
        if show_plot or save_plot:
            time_grid = np.linspace(time[0], time[(-1)], 10001)
            model_flux_grid = ellc_lc_short(time_grid)
            phase, phaseflux, phaseflux_err, N, phi = lct.phase_fold(time, flux, period, epoch, dt=0.002, ferr_type='medsig', ferr_style='sem', sigmaclip=True)
            phase_grid = np.linspace(-0.25, 0.75, 10001)
            model_phaseflux_grid = ellc_lc_short(params['epoch'] + phase_grid * params['period'])
            fig = plt.figure(figsize=(15, 10), tight_layout=True)
            gs = gridspec.GridSpec(3, 3)
            plotter.plot_lc_full(fig.add_subplot(gs[0, :]), time, flux, flux_err, time_grid, model_flux_grid)
            plotter.plot_lc_phase(fig.add_subplot(gs[(1, 0)]), phi, flux, phase, phaseflux, phaseflux_err, phase_grid, model_phaseflux_grid)
            plotter.plot_lc_phasezoom(fig.add_subplot(gs[(1, 1)]), phi, flux, phase, phaseflux, phaseflux_err, phase_grid, model_phaseflux_grid, params['period'] * 24.0 * 60.0)
            plotter.plot_info((fig.add_subplot(gs[(2, 0)])), text=0, params=params)
            plotter.plot_info((fig.add_subplot(gs[(2, 1)])), text=1, params=params)
            if save_plot:
                if len(os.path.dirname(fname_plot)) > 0:
                    if not os.path.exists(os.path.dirname(fname_plot)):
                        os.makedirs(os.path.dirname(fname_plot))
                fig.savefig(fname_plot)
                plt.close(fig)
            if show_plot:
                plt.show(fig)
            else:
                plt.close(fig)
    if save_csv:
        if len(os.path.dirname(fname_csv)) > 0:
            if not os.path.exists(os.path.dirname(fname_csv)):
                os.makedirs(os.path.dirname(fname_csv))
        X = np.column_stack((time, flux, flux_err))
        np.savetxt(fname_csv, X, delimiter=',')
    return flux


def inject_lc_model(time, flux, flux_err, **kwargs):
    """
    Wrapper around make_lc_model()
    """
    return make_lc_model(time, flux=flux, flux_err=flux_err, **kwargs)


def make_rv_model(time, rv=None, rv_err=None, epoch=0.0, period=1.0, R_companion=1.0, M_companion=1.0, R_companion_unit='Rearth', M_companion_unit='Mearth', R_host=1.0, M_host=1.0, sbratio=0, incl=90, ecc=0, omega=0, dil=0, ldc=[
 0.6, 0.2], ld='quad', show_plot=False, save_plot=False, save_csv=False, fname_plot='rv.pdf', fname_csv='rv.csv'):
    """
    Inputs:
    -------
    time : array of float
        time in days
    rv : array of float
        RV of the 'underlying' series
    rv_err : array of float
        error of RV of the 'underlying' series
    epoch : float
        epoch in days
    period : float
        period in days
    R_companion: float
        radius of the planet, in R_earth
        
    Optional Inputs:
    ----------------
    M_companion: float
        mass of the planet, in M_earth
        default is 0
    R_host : float
        radius of the star, in R_sun
        default is 1
    M_host: float
        mass of the star, in M_sun
        default is 1
    show_plot : bool
        show the plot in the terminal, or close it
        default is False
    save_plot : bool
        save the plot to a file, or not
        default is False
    save_csv : bool
        save the lightcurve to a file, or not
        default is False
        
    Returns:
    --------
    flux2 : array of float
        relative flux with injected signal
    """
    if rv is None:
        rv = np.zeros_like(time)
    else:
        if rv_err is None:
            rv_err = np.zeros_like(time)
        params = translate(quiet=True, R_companion=R_companion, M_companion=M_companion, R_companion_unit=R_companion_unit, M_companion_unit=M_companion_unit, R_host=R_host, M_host=M_host, epoch=epoch, period=period, incl=incl, ecc=ecc, omega=omega, ldc=ldc, ld=ld)

        def ellc_rv_short(time):
            return ellc.rv(t_obs=time, radius_1=(params['R_host/a']), radius_2=(params['R_companion/a']), sbratio=sbratio, incl=(params['incl']), t_zero=epoch, period=(params['period']), a=(params['a']), q=1, f_c=(params['f_c']), f_s=(params['f_s']), ldc_1=ldc, ldc_2=None, gdc_1=None, gdc_2=None, didt=None, domdt=None, rotfac_1=1, rotfac_2=1, hf_1=1.5, hf_2=1.5, bfac_1=None, bfac_2=None, heat_1=None, heat_2=None, lambda_1=None, lambda_2=None, vsini_1=None, vsini_2=None, t_exp=None, n_int=None, grid_1='default', grid_2='default', ld_1=ld, ld_2=None, shape_1='sphere', shape_2='sphere', spots_1=None, spots_2=None, verbose=1)[0]

        model_rv = ellc_rv_short(time)
        rv += model_rv
        if show_plot or save_plot:
            phi = lct.calc_phase(time, period, epoch)
            phi[(phi > 0.75)] -= 1.0
            time_grid = np.linspace(time[0], time[(-1)], 10001)
            model_rv_grid = ellc_rv_short(time_grid)
            phase_grid = np.linspace(-0.25, 0.75, 10001)
            model_phaserv_grid = ellc_rv_short(epoch + phase_grid * period)
            fig = plt.figure(figsize=(15, 10), tight_layout=True)
            gs = gridspec.GridSpec(3, 3)
            plotter.plot_rv_full(fig.add_subplot(gs[0, :]), time, rv, rv_err, time_grid, model_rv_grid)
            plotter.plot_rv_phase(fig.add_subplot(gs[(1, 0)]), phi, rv, rv_err, phase_grid, model_phaserv_grid)
            plotter.plot_info((fig.add_subplot(gs[(2, 0)])), text=0, params=params)
            plotter.plot_info((fig.add_subplot(gs[(2, 1)])), text=1, params=params)
            if save_plot:
                if len(os.path.dirname(fname_plot)) > 0:
                    if not os.path.exists(os.path.dirname(fname_plot)):
                        os.makedirs(os.path.dirname(fname_plot))
                fig.savefig(fname_plot)
            if show_plot:
                plt.show(fig)
            else:
                plt.close(fig)
    if save_csv:
        if len(os.path.dirname(fname_csv)) > 0:
            if not os.path.exists(os.path.dirname(fname_csv)):
                os.makedirs(os.path.dirname(fname_csv))
        X = np.column_stack((time, rv, rv_err))
        np.savetxt(fname_csv, X, delimiter=',')
    return rv


def inject_rv_model(time, rv, rv_err, **kwargs):
    """
    Wrapper around make_lc_model()
    """
    return make_rv_model(time, rv=rv, rv_err=rv_err, **kwargs)


if __name__ == '__main__':
    time = np.linspace(0, 100, 101)
    make_lc_model(time, period=30.7, R_host=0.4, M_host=0.4, show_plot=True)
    make_rv_model(time, period=30.7, R_host=0.4, M_host=0.4, show_plot=True)