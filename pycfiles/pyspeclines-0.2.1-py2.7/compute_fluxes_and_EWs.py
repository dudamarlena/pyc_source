# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeclines/compute_fluxes_and_EWs.py
# Compiled at: 2019-02-14 11:07:10
from collections import OrderedDict
import os, json
from astropy.io import fits
from astropy import constants as const
from astropy import log
import dustmaps.sfd, dustmaps.config
from astropy.coordinates import SkyCoord
import astropy.units as units, numpy as np, pyspeckit, matplotlib.pyplot as plt, pkg_resources, pyspeclines, extinction
SEP = '_'
FLUX_PREFIX = 'F' + SEP
EW_PREFIX = 'EW' + SEP
ERR_SUFFIX = SEP + 'err'

def sum_errors_in_quadrature(errors):
    _errors = np.array(errors)
    _err = np.sqrt(np.sum(_errors ** 2))
    return _err


def get_multiple_keys(key):
    _key_sp = key.split(SEP)
    _key_sp.append(key)
    return _key_sp


def velocity_to_pixel(velocity, wl_central, dwl):
    _dwl = velocity / const.c.to('km/s').value * wl_central
    pxl = _dwl / dwl
    return pxl


def pixel_to_velocity(pxl, wl_central, dwl):
    _dwl = pxl * dwl
    velocity = _dwl / wl_central * const.c.to('km/s').value


def compute_fluxes_EWs(file_name, json_file, args):
    with open(json_file) as (f):
        lines = json.load(f, object_pairs_hook=OrderedDict)
    EWs = OrderedDict()
    EWs_errors = OrderedDict()
    integrated_fluxes = OrderedDict()
    integrated_errors = OrderedDict()
    hdulist = fits.open(file_name)
    wl = hdulist[1].data['wl']
    spectrum = hdulist[1].data['flux']
    error = hdulist[1].data['err']
    if args.deredden:
        if 'RA' not in hdulist[1].header:
            raise ValueError("'RA' keyword (in degrees) must be present in the FITS header!")
        if 'DEC' not in hdulist[1].header:
            raise ValueError("'DEC' keyword (in degrees) must be present in the FITS header!")
        package_dir = pyspeclines.__path__[0]
        dust_map_path = os.path.join(os.path.dirname(package_dir), 'PySpecLines', 'files', 'dustmaps')
        dustmaps.config.config['data_dir'] = dust_map_path
        dust_map_ngp = os.path.join(dust_map_path, 'SFD_dust_4096_ngp.fits')
        dust_map_sgp = os.path.join(dust_map_path, 'SFD_dust_4096_sgp.fits')
        if not os.path.isfile(dust_map_ngp) or not os.path.isfile(dust_map_sgp):
            dustmaps.sfd.fetch()
        sfd = dustmaps.sfd.SFDQuery()
        ra, dec = hdulist[1].header['RA'], hdulist[1].header['DEC']
        coord = SkyCoord(ra, dec, frame='icrs', unit=(units.deg, units.deg))
        E_B_V = sfd(coord)
        log.info('Applying a Galactic extinction correction E(B-V) = ' + str(E_B_V))
        R_V = 3.1
        A_V = E_B_V * R_V
        extinction_curve = extinction.fitzpatrick99(wl, -A_V, R_V)
        spectrum = extinction.apply(extinction_curve, spectrum)
        error = extinction.apply(extinction_curve, error)
    redshift = None
    if 'redshift' in hdulist[1].header:
        redshift = hdulist[1].header['redshift']
        log.info('De-redshifting the spectrum using z = ' + str(redshift))
        wl /= 1.0 + redshift
        spectrum *= 1.0 + redshift
        error *= 1.0 + redshift
    for key, value in lines.iteritems():
        print '\nkey: ', key
        if args.gaussian_fit:
            il0 = np.searchsorted(wl, value['continuum_left'][0])
            il0 = max([0, il0 - args.extend_region])
            ir1 = np.searchsorted(wl, value['continuum_right'][1])
            ir1 = min([len(wl) + 1, ir1 + args.extend_region])
            _wl = wl[il0:ir1]
            _dwl = _wl[1] - _wl[0]
            _spectrum = spectrum[il0:ir1]
            _error = error[il0:ir1]
            exclude = None
            if 'exclude' in value:
                exclude = value['exclude']
            sp = pyspeckit.Spectrum(data=_spectrum, error=_error, xarr=_wl, xarrkwargs={'unit': 'AA'}, unit='$erg/s/cm^2/AA$')
            sp.baseline(subtract=False, highlight_fitregion=False, order=args.continuum_degree, excludefit=False, exclude=exclude)
            amplitude_guess = np.mean(spectrum)
            _width_guess = 1.0
            guesses = list()
            tied = list()
            width_velocity = None
            for c, component in enumerate(value['wl_central']):
                center_guess = component
                width_guess = _width_guess
                if 'width' in value:
                    width_velocity = value['width'][c]
                    width_guess = velocity_to_pixel(width_velocity, center_guess, _dwl)
                guesses = guesses + [amplitude_guess, center_guess, width_guess]
                if c == 0:
                    tied = tied + ['', '', '']
                elif width_velocity is None:
                    tied = tied + ['', '', 'p[2]']
                else:
                    width_velocities = list(value['width'][0:c])
                    try:
                        p = width_velocities.index(width_velocity)
                        p = 2 + p * 3
                        tied = tied + ['', '', 'p[2]']
                    except:
                        tied = tied + ['', '', '']

            sp.specfit(fittype='gaussian', guesses=guesses, tied=tied)
            for N in range(args.n_iter):
                sp.baseline(subtract=False, highlight_fitregion=False, order=args.continuum_degree, excludefit=True, exclude=exclude)
                sp.specfit(fittype='gaussian', guesses=guesses, tied=tied)

            sp.plotter(errstyle='fill')
            if args.log_flux:
                plt.yscale('log')
            continuum = sp.baseline.basespec
            print '##########################'
            print '## Gaussian Fit results ##'
            print '##########################'
            integrated_flux = list()
            integrated_error = list()
            EW = list()
            EW_err = list()
            par_values = list()
            for c, component in enumerate(value['wl_central']):
                c0, c1 = c * 3, (c + 1) * 3
                amplitude, center, width = sp.specfit.parinfo.values[c0:c1]
                par_values.append(amplitude)
                par_values.append(center)
                par_values.append(width)
                amplitude_err, center_err, width_err = sp.specfit.parinfo.errors[c0:c1]
                _integrated_flux = np.sqrt(2 * np.pi) * width * amplitude
                integrated_flux.append(_integrated_flux)
                _integrated_error = np.sqrt((amplitude_err / amplitude) ** 2 + (width_err / width) ** 2)
                integrated_error.append(_integrated_error * _integrated_flux)
                i0 = np.searchsorted(_wl, center - 3.0 * width)
                i1 = np.searchsorted(_wl, center + 3 * width)
                _continuum = np.median(continuum[i0:i1 + 1])
                _EW = _integrated_flux / _continuum
                EW.append(_EW)
                _EW_err = _integrated_error
                EW_err.append(_EW * _EW_err)
                if args.continuum_error is not None:
                    _continuum_error = args.continuum_error * _continuum
                    integrated_error[c] = sum_errors_in_quadrature([integrated_error[c], _continuum_error])
                    _continuum_error = args.continuum_error
                    EW_err[c] = sum_errors_in_quadrature([EW_err[c], _continuum_error])
                print 'Flux, error, line center, width: ', integrated_flux[c], integrated_error[c], center, pixel_to_velocity(width, center, _dwl)
                print 'EW, error: ', EW[c], EW_err[c]

            if len(integrated_flux) > 1:
                _integrated_flux = np.sum(integrated_flux)
                _integrated_error = np.sqrt(np.sum(np.array(integrated_error) ** 2))
                integrated_flux.append(_integrated_flux)
                integrated_error.append(_integrated_error)
                _EW = np.sum(EW)
                _EW_err = np.sqrt(np.sum(np.array(EW_err) ** 2))
                EW.append(_EW)
                EW_err.append(_EW_err)
                print '(Sum of components) Flux, error: ', integrated_flux[(-1)], integrated_error[(-1)]
                print '(Sum of components) EW, error: ', EW[(-1)], EW_err[(-1)]
            if args.use_pymc:
                MC_uninformed = sp.specfit.get_pymc()
                burn = int(args.frac_burn * args.n_samples)
                MC_uninformed.sample(args.n_samples, burn=burn, tune_interval=250)
                _perc = [
                 0.5]
                for interval in args.credible_intervals:
                    _p_low, _p_up = 0.5 * (1.0 - interval), 1.0 - 0.5 * (1.0 - interval)
                    _perc = _perc + [_p_low, _p_up]

                _perc = 100.0 * np.array(_perc)
                print '###############################'
                print '## MCMC Gaussian Fit results ##'
                print '###############################'
                integrated_flux = list()
                integrated_error = list()
                EW = list()
                EW_err = list()
                areas = list()
                areas_continuum = list()
                par_values = list()
                for c, component in enumerate(value['wl_central']):
                    _amplitude = MC_uninformed.trace('AMPLITUDE' + str(c))[:]
                    _center = MC_uninformed.trace('SHIFT' + str(c))[:]
                    _width = MC_uninformed.trace('WIDTH' + str(c))[:]
                    amplitude, center, width = np.median(_amplitude), np.median(_center), np.median(_width)
                    par_values.append(amplitude)
                    par_values.append(center)
                    par_values.append(width)
                    _area = np.sqrt(2 * np.pi) * _width * _amplitude
                    areas.append(_area)
                    _integrated_flux, err_low, err_up = np.percentile(_area, _perc)
                    integrated_flux.append(_integrated_flux)
                    integrated_error.append(0.5 * (err_up - err_low))
                    width = np.median(_width)
                    i0 = np.searchsorted(_wl, center - 3.0 * width)
                    i1 = np.searchsorted(_wl, center + 3 * width)
                    _continuum = np.median(continuum[i0:i1 + 1])
                    __EW = _area / _continuum
                    areas_continuum.append(__EW)
                    _EW, err_low, err_up = np.percentile(__EW, _perc)
                    EW.append(_EW)
                    EW_err.append(0.5 * (err_up - err_low))
                    if args.continuum_error is not None:
                        _continuum_error = args.continuum_error * _continuum
                        integrated_error[c] = sum_errors_in_quadrature([integrated_error[c], _continuum_error])
                        _continuum_error = args.continuum_error
                        EW_err[c] = sum_errors_in_quadrature([EW_err[c], _continuum_error])
                    print 'Flux, error: ', integrated_flux[c], integrated_error[c]
                    print 'EW, error: ', EW[c], EW_err[c]

                if len(integrated_flux) > 1:
                    _area = np.zeros(len(areas[0]))
                    _area_continuum = np.zeros(len(areas[0]))
                    for _a, _a_c in zip(areas, areas_continuum):
                        _area = _area + _a
                        _area_continuum = _area_continuum + _a_c

                    _integrated_flux, err_low, err_up = np.percentile(_area, _perc)
                    integrated_flux.append(_integrated_flux)
                    integrated_error.append(0.5 * (err_up - err_low))
                    _EW, err_low, err_up = np.percentile(_area_continuum, _perc)
                    EW.append(_EW)
                    EW_err.append(0.5 * (err_up - err_low))
                    print '(Sum of components) Flux, error: ', integrated_flux[(-1)], integrated_error[(-1)]
                    print '(Sum of components) EW, error: ', EW[(-1)], EW_err[(-1)]
            sp.specfit.plot_fit(pars=par_values)
            integrated_fluxes[key] = integrated_flux
            integrated_errors[key] = integrated_error
            EWs[key] = EW
            EWs_errors[key] = EW_err
            if args.show_plot:
                plt.show()
            fig_name = key + '.pdf'
            sp.plotter.savefig(fig_name)
        else:
            integrated_flux = list()
            integrated_error = list()
            EW = list()
            EW_err = list()
            il0 = np.searchsorted(wl, value['continuum_left'][0])
            il0 -= 1
            il1 = np.searchsorted(wl, value['continuum_left'][1])
            if il0 == il1:
                il0 -= 1
            flux_left = np.trapz(spectrum[il0:il1 + 1], x=wl[il0:il1 + 1]) / (wl[il1] - wl[il0])
            _wlleft = 0.5 * (wl[il0] + wl[il1])
            ir0 = np.searchsorted(wl, value['continuum_right'][0])
            ir0 -= 1
            ir1 = np.searchsorted(wl, value['continuum_right'][1])
            if ir0 == ir1:
                ir0 -= 1
            flux_right = np.trapz(spectrum[ir0:ir1 + 1], x=wl[ir0:ir1 + 1]) / (wl[ir1] - wl[ir0])
            _wlright = 0.5 * (wl[ir0] + wl[ir1])
            grad = (flux_right - flux_left) / (_wlright - _wlleft)
            intercept = flux_right - grad * _wlright
            i0 = np.searchsorted(wl, value['wl_range'][0])
            i0 -= 1
            i1 = np.searchsorted(wl, value['wl_range'][1])
            n_wl = i1 - i0 + 1
            _wl = np.copy(wl[i0:i1 + 1])
            _spectrum = np.copy(spectrum[i0:i1 + 1])
            _error = np.copy(error[i0:i1 + 1])
            _spectrum[0] = _spectrum[0] + (_spectrum[1] - _spectrum[0]) / (_wl[1] - _wl[0]) * (value['wl_range'][0] - _wl[0])
            _spectrum[-1] = _spectrum[(-2)] + (_spectrum[(-2)] - _spectrum[(-1)]) / (_wl[(-2)] - _wl[(-1)]) * (value['wl_range'][1] - _wl[(-2)])
            _wl = np.zeros(n_wl)
            _wl[0] = value['wl_range'][0]
            _wl[-1] = value['wl_range'][1]
            _wl[1:(-1)] = wl[i0 + 1:i1]
            relative_error = _error / _spectrum
            _integrated_relative_error = np.sqrt(np.sum(relative_error ** 2))
            integrand = 1.0 - _spectrum / (grad * _wl + intercept)
            _EW = -np.trapz(integrand, x=_wl)
            EW.append(_EW)
            _EW_err = abs(_EW) * _integrated_relative_error
            EW_err.append(_EW_err)
            EWs[key] = EW
            EWs_errors[key] = EW
            integrand = _spectrum - (grad * _wl + intercept)
            _integrated_flux = np.trapz(integrand, x=_wl)
            integrated_flux.append(_integrated_flux)
            _integrated_error = abs(_integrated_flux) * _integrated_relative_error
            integrated_error.append(_integrated_error)
            integrated_fluxes[key] = integrated_flux
            integrated_errors[key] = integrated_error
            print 'EW, flux, rel_err: ', EW, integrated_flux, integrated_error

    new_hdulist = fits.HDUList([fits.PrimaryHDU()])
    cols = list()
    for key, value in EWs.iteritems():
        if len(value) > 1:
            _key_sp = get_multiple_keys(key)
            for k in _key_sp:
                _key = EW_PREFIX + k
                col = fits.Column(name=_key, format='E')
                cols.append(col)
                _key = _key + ERR_SUFFIX
                col = fits.Column(name=_key, format='E')
                cols.append(col)

        else:
            _key = EW_PREFIX + key
            col = fits.Column(name=_key, format='E')
            cols.append(col)
            _key = _key + ERR_SUFFIX
            col = fits.Column(name=_key, format='E')
            cols.append(col)

    columns = fits.ColDefs(cols)
    new_hdu = fits.BinTableHDU.from_columns(columns, nrows=1)
    new_hdu.name = 'EQUIVALENT WIDTHS'
    for key, value in EWs.iteritems():
        if len(value) > 1:
            _key_sp = get_multiple_keys(key)
            for c, k in enumerate(_key_sp):
                _key = EW_PREFIX + k
                new_hdu.data[_key] = EWs[key][c]
                _key = _key + ERR_SUFFIX
                new_hdu.data[_key] = EWs_errors[key][c]

        else:
            _key = EW_PREFIX + key
            new_hdu.data[_key] = EWs[key]
            _key = _key + ERR_SUFFIX
            new_hdu.data[_key] = EWs_errors[key]

    if new_hdu.name in new_hdulist:
        new_hdulist[new_hdu.name] = new_hdu
    else:
        new_hdulist.append(new_hdu)
    cols = list()
    for key, value in integrated_fluxes.iteritems():
        if len(value) > 1:
            _key_sp = get_multiple_keys(key)
            for k in _key_sp:
                _key = FLUX_PREFIX + k
                col = fits.Column(name=_key, format='E')
                cols.append(col)
                _key = _key + ERR_SUFFIX
                col = fits.Column(name=_key, format='E')
                cols.append(col)

        else:
            _key = FLUX_PREFIX + key
            col = fits.Column(name=_key, format='E')
            cols.append(col)
            _key = _key + ERR_SUFFIX
            col = fits.Column(name=_key, format='E')
            cols.append(col)

    columns = fits.ColDefs(cols)
    new_hdu = fits.BinTableHDU.from_columns(columns, nrows=1)
    new_hdu.name = 'INTEGRATED FLUXES'
    for key, value in integrated_fluxes.iteritems():
        if len(value) > 1:
            _key_sp = get_multiple_keys(key)
            for c, k in enumerate(_key_sp):
                _key = FLUX_PREFIX + k
                new_hdu.data[_key] = integrated_fluxes[key][c]
                _key = _key + ERR_SUFFIX
                new_hdu.data[_key] = integrated_errors[key][c]

        else:
            _key = FLUX_PREFIX + key
            new_hdu.data[_key] = integrated_fluxes[key]
            _key = _key + ERR_SUFFIX
            new_hdu.data[_key] = integrated_errors[key]

    if new_hdu.name in new_hdulist:
        new_hdulist[new_hdu.name] = new_hdu
    else:
        new_hdulist.append(new_hdu)
    if args.gaussian_fit:
        _file_name = file_name.split('.fits')[0] + '_gaussian_fluxes.fits'
    else:
        _file_name = file_name.split('.fits')[0] + '_numerical_fluxes.fits'
    new_hdulist.writeto(_file_name, overwrite=True)
    return