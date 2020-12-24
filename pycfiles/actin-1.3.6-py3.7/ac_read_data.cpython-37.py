# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgsilva/Astrophysics/Packages/ACTIN/actin/actin_files/ac_read_data.py
# Compiled at: 2019-12-05 17:01:50
# Size of source mod 2**32: 17132 bytes
from __future__ import print_function
from __future__ import division
import sys, os, numpy as np, glob
import astropy.io.fits as pyfits
import matplotlib.pylab as plt
import ac_tools, ac_settings as ac_set

def check_for_calib_files(e2ds_header, file_type, folder, dif_time_max=1.0, plot_spec=False):
    """
    Check for calibration files (wave or blaze) in the working directory
    in case of predetermined files are not present and choses the ones with
    less than 1 day difference from the original e2ds file.

    Parameters:
    -----------
    e2ds_header : fits header
        Fits header of e2ds fits file.
    file_type : str
        File type to be searched, either 'wave' or 'blaze'.
    folder : str
        Path to the fits files.
    dif_time_max : float (optional)
        Maximum difference in time between e2ds and
        the chosen calib file [days].

    Returns:
    --------
    calib_pfile : {str, None}
        Selected calibration file with path included, None if
        file not found.
    """
    print('Executing: check_for_calib_files')
    mjd_e2ds = e2ds_header['MJD-OBS']
    filename = os.path.join(folder, '*{}_A.fits'.format(file_type))
    calib_pfiles = glob.glob(filename)
    if len(calib_pfiles) > 0:
        time_dif = []
        for k in range(len(calib_pfiles)):
            w = pyfits.open(calib_pfiles[k])
            mjd = w[0].header['MJD-OBS']
            w.close()
            time_dif.append(abs(mjd_e2ds - mjd))

        if min(time_dif) < dif_time_max:
            index = time_dif.index(min(time_dif))
            calib_pfile = calib_pfiles[index]
            calib_file = os.path.split(calib_pfile)[(-1)]
            print('New {} file used:\t{}'.format(file_type, calib_file))
            print('{} file time difference to e2ds = {:.2f} days'.format(file_type, min(time_dif)))
            return calib_pfile
        print('*** WARNING: Closest {} file was produced longer than {} day(s)'.format(file_type, dif_time_max))
        return
    else:
        print('*** WARNING: No more {} files in folder'.format(file_type))
        return


def calc_wave(e2ds_pfile, obs):
    """
    Compute wavelength from e2ds headers.

    Parameters:
    -----------
    e2ds_pfile : str
        e2ds file name with path to its location.
    obs : str
        Code related to instrument to be used in fits headers.

    Returns:
    --------
    wave : list of lists
        2d wavelength list where len(wave) is number of orders [angstroms].
    """
    print('Executing: calc_wave')
    e2ds = pyfits.open(e2ds_pfile)
    deg = e2ds[0].header['HIERARCH {} DRS CAL TH DEG LL'.format(obs)]
    ll_coeff = np.zeros((len(e2ds[0].data), deg + 1))
    for i in range(len(e2ds[0].data)):
        for j in range(deg + 1):
            ll_coeff[(i, j)] = e2ds[0].header['HIERARCH {} DRS CAL TH COEFF LL{}'.format(obs, j + (deg + 1) * i)]

    x = np.arange(e2ds[0].data.shape[1])
    wave = np.zeros(e2ds[0].data.shape)
    for i in range(len(wave)):
        wave[i] = np.poly1d(ll_coeff[i][::-1])(x)

    e2ds.close()
    return wave


def read_data_rdb(file):
    """
    Read spectrum from rdb file with the following headers:
    'obj', 'obs_date', 'bjd', 'wave', 'flux', 'error_pixel' (optional)
    """
    print('Reading file:\t{}'.format(file))
    try:
        data, hdr = ac_tools.read_rdb(file)
    except:
        print('*** ERROR: Cannot read {}'.format(file))
        sys.exit()

    print('Object:\t\t{}'.format(data['obj'][0]))
    data['wave'] = np.asarray(data['wave'])
    data['flux'] = np.asarray(data['flux'])
    data['tel'] = 'unknown'
    data['instr'] = 'unknown'
    data['obj'] = data['obj'][0]
    data['obs_date'] = data['obs_date'][0]
    data['bjd'] = data['bjd'][0]
    data['blaze'] = np.ones(len(data['flux']))
    data['snr'] = None
    data['median_snr'] = None
    data['ccf_noise'] = 0.0
    return data


def read_data(pfile, rv_in=None, obj_name=None, force_calc_wave=False, plot_spec=False):
    """
    Reads data from 'S2D', 'S1D', 'e2ds', 's1d', 's1d_*_rv', 'ADP', and 'rdb' files.
    - force_calc_wave is for testing purposes.
    - plot_spec is for testing purposes.
    """
    print()
    print('READING DATA FROM FILE:')
    print('-----------------------')
    flg = None
    file_type = ac_tools.get_file_type(pfile)
    if file_type == 'rdb':
        data = read_data_rdb(pfile)
        data['file_type'] = file_type
        return data
    else:
        folder, file = os.path.split(pfile)
        file_info = file.split('_')[0]
        print('Working folder:\t{}{}'.format(folder, os.path.sep))
        print('Reading file:\t{}'.format(file))
        hdu = pyfits.open(pfile)
        hdr = hdu[0].header
        tel = hdr['TELESCOP']
        instr = hdr['INSTRUME']
        date_obs = hdr['DATE-OBS']
        print('Telescope:\t{}'.format(tel))
        print('Instrument:\t{}'.format(instr))
        if instr == 'HARPS':
            obs = 'ESO'
            ords = 72
        else:
            if instr == 'HARPN':
                obs = 'TNG'
                ords = 69
            else:
                if instr == 'ESPRESSO':
                    obs = 'ESO'
                    ords = 170
                else:
                    sys.exit("*** ERROR: Instrument not recognized. ACTIN only accepts HARPS, HARPS-N, and ESPRESSO fits files. If using another instrument make an '.rdb' table with the headers 'obj', 'obs_date', 'bjd', 'wave', 'flux', 'error_pixel' (optional) and run ACTIN on that file.")
    obj = ac_tools.get_target(pfile)
    print('Object:\t\t{}'.format(obj))
    if obj in ('WAVE,WAVE,THAR1', 'WAVE,WAVE,THAR2'):
        print('*** WARNING: File is ThAr flux.')
        print('*** ACTION: Ignoring Measurement.')
        return
    if obj_name:
        obj = ac_tools.override_obj(obj, obj_name)
        print('Object name changed to:', obj)
    if instr in 'ESPRESSO':
        if file_type == 'S2D':
            flux = hdu[1].data
            flux_err = hdu[2].data
            wave_raw = hdu[5].data
        else:
            if file_type == 'S1D':
                data = hdu[1].data
                flux = data['flux']
                flux_err = data['error']
                wave_raw = data['wavelength_air']
            bjd = hdr['HIERARCH {} QC BJD'.format(obs)]
            snr = [hdr['HIERARCH {} QC ORDER{} SNR'.format(obs, k + 1)] for k in range(ords)]
            snr = np.asarray(snr)
            median_snr = np.median(snr)
            try:
                bv = hdr['HIERARCH {} OCS OBJ BV'.format(obs)]
            except:
                bv = None

        try:
            airmass = hdr['AIRMASS']
        except KeyError:
            airmass = None

        try:
            exptime = hdr['EXPTIME']
        except KeyError:
            exptime = None

    if instr in ('HARPS', 'HARPN'):
        bjd = hdr['HIERARCH {} DRS BJD'.format(obs)]
        berv = hdr['HIERARCH {} DRS BERV'.format(obs)]
        try:
            bv = hdr['HIERARCH {} OCS OBJ BV'.format(obs)]
        except:
            bv = None

        try:
            airmass = hdr['AIRMASS']
        except KeyError:
            airmass = None

        try:
            exptime = hdr['EXPTIME']
        except KeyError:
            exptime = None

        if file_type in ('s1d', 'e2ds'):
            flux = hdu[0].data
            flux_err = None
            hdu.close()
            snr = [hdr['HIERARCH {} DRS SPE EXT SN{}'.format(obs, k)] for k in range(ords)]
            snr = np.asarray(snr)
            median_snr = np.median(snr)
        if file_type == 'ADP':
            flux = hdu[1].data[0][1]
            flux_err = None
            wave_raw = hdu[1].data[0][0]
            hdu.close()
            median_snr = hdr['SNR']
            blaze = np.ones(len(flux))
            snr = None
    if file_type == 's1d':
        wave_raw = hdr['CRVAL1'] + hdr['CDELT1'] * np.arange(hdr['NAXIS1'])
        blaze = np.ones(len(flux))
    elif file_type in ('e2ds', 'ADP'):
        if file_type != 'ADP':
            wave_file = hdr['HIERARCH {} DRS CAL TH FILE'.format(obs)]
            print('Wave file:\t{}'.format(wave_file))
            wave_pfile = os.path.join(folder, wave_file)
            if force_calc_wave == False:
                try:
                    wave_hdu = pyfits.open(wave_pfile)
                except:
                    print('*** INFO: Could not open', wave_pfile)
                    wave_pfile = check_for_calib_files(hdr, 'wave', folder)
                    try:
                        wave_hdu = pyfits.open(wave_pfile)
                    except:
                        print('*** INFO: Could not open:')
                        print('***', wave_pfile)
                        print('*** ACTION: Computing wavelength from', file_type)
                        wave_raw = calc_wave(pfile, obs)
                        wave_raw = np.asarray(wave_raw)
                    else:
                        wave_raw = wave_hdu[0].data
                        wave_hdu.close()
                else:
                    wave_raw = wave_hdu[0].data
                    wave_hdu.close()
            if force_calc_wave == True:
                print('*** ACTION: Computing wavelength from', file_type)
                wave_raw = calc_wave(pfile, obs)
                wave_raw = np.asarray(wave_raw)
        blaze_file = hdr['HIERARCH {} DRS BLAZE FILE'.format(obs)]
        print('Blaze file:\t{}'.format(blaze_file))
        blaze_pfile = os.path.join(folder, blaze_file)
        try:
            blaze_hdu = pyfits.open(blaze_pfile)
        except:
            print('*** WARNING: The blaze file associated with this e2ds is not present.')
            print('*** Looking for other blaze files in the folder...')
            blaze_pfile = check_for_calib_files(hdr, 'blaze', folder)
            try:
                blaze_hdu = pyfits.open(blaze_pfile)
            except:
                print('*** WARNING: Flux not deblazed. This can introduce artificial variations in the indices values.')
                if file_type == 'e2ds':
                    blaze = np.ones([len(flux), len(flux[0])])
                if file_type == 'ADP':
                    blaze = np.ones(len(flux))
                flg = 'noDeblazed'
            else:
                blaze = blaze_hdu[0].data
                blaze_hdu.close()
        else:
            blaze = blaze_hdu[0].data
            blaze_hdu.close()
        if instr in 'ESPRESSO':
            rv = hdr['HIERARCH {} QC CCF RV'.format(obs)]
            rv_err = hdr['HIERARCH {} QC CCF RV ERROR'.format(obs)]
            fwhm = hdr['HIERARCH {} QC CCF FWHM'.format(obs)]
            fwhm_err = hdr['HIERARCH {} QC CCF FWHM ERROR'.format(obs)]
            cont = hdr['HIERARCH {} QC CCF CONTRAST'.format(obs)]
            cont_err = hdr['HIERARCH {} QC CCF CONTRAST ERROR'.format(obs)]
            try:
                bv = hdr['HIERARCH {} OCS OBJ BV'.format(obs)]
            except:
                bv = None

            berv = hdr['HIERARCH {} QC BERV'.format(obs)]
            rv = rv * 1000
            rv_err = rv_err * 1000
            berv = berv * 1000
            fwhm = fwhm * 1000
            fwhm_err = fwhm_err * 1000
            bis = None
            bis_err = None
            ccf_noise = 0.0
            if file_type == 'S2D':
                blaze = np.ones([len(flux), len(flux[0])])
            if file_type == 'S1D':
                blaze = np.ones([len(flux)])
        if instr in ('HARPS', 'HARPN'):
            if file_type == 'ADP':
                ccf_search = '{}.{}*ccf_*_A.fits'.format(instr, date_obs[:-2])
            else:
                ccf_search = '{}*_ccf_*_A.fits'.format(file_info[:-2])
            ccf_search = os.path.join(folder, ccf_search)
            try:
                ccf_pfile = glob.glob(ccf_search)[0]
                ccf_hdu = pyfits.open(ccf_pfile)
            except:
                print('*** WARNING: Could not find or open:')
                print('***', ccf_search)
                print('*** WARNING: No CCF data available.')
                rv = None
                rv_err = None
                fwhm = None
                fwhm_err = None
                cont = None
                cont_err = None
                ccf_noise = None
                berv = None
            else:
                ccf_file = os.path.split(ccf_pfile)[(-1)]
                print('CCF file:\t{}'.format(ccf_file))
                ccf_hdr = ccf_hdu[0].header
                ccf_hdu.close()
                try:
                    rv = ccf_hdr['HIERARCH {} DRS CCF RVC'.format(obs)]
                    rv_err = ccf_hdr['HIERARCH {} DRS DVRMS'.format(obs)]
                except KeyError as err:
                    try:
                        print('*** ERROR: {}, Ignoring measurement.'.format(err))
                        return
                    finally:
                        err = None
                        del err

                ccf_noise = ccf_hdr['HIERARCH {} DRS CCF NOISE'.format(obs)]
                fwhm = ccf_hdr['HIERARCH {} DRS CCF FWHM'.format(obs)]
                fwhm_err = None
                cont = ccf_hdr['HIERARCH {} DRS CCF CONTRAST'.format(obs)]
                cont_err = None
                rv = rv * 1000
                berv = berv * 1000
                fwhm = fwhm * 1000
                ccf_noise = ccf_noise * 1000
            if file_type == 'ADP':
                bis_search = '{}.{}*bis_*_A.fits'.format(instr, date_obs[:-2])
    else:
        bis_search = '{}*_bis_*_A.fits'.format(file_info[:-2])
    bis_search = os.path.join(folder, bis_search)
    try:
        bis_pfile = glob.glob(bis_search)[0]
        bis_hdu = pyfits.open(bis_pfile)
    except:
        print('*** WARNING: Could not find or open:')
        print('***', bis_search)
        print('*** WARNING: No BIS data available.')
        bis = None
        bis_err = None
    else:
        bis_file = os.path.split(bis_pfile)[(-1)]
        print('BIS file:\t{}'.format(bis_file))
        bis_hdr = bis_hdu[0].header
        bis_hdu.close()
        bis = bis_hdr['HIERARCH {} DRS BIS SPAN'.format(obs)]
        bis = bis * 1000
        bis_err = None
    c = 299792458.0
    if rv_in is not None:
        rv = rv_in * 1000
    else:
        if instr in 'ESPRESSO':
            wave = wave_raw - rv * wave_raw / c
        if instr in ('HARPS', 'HARPN'):
            if file_type in ac_set.ftypes['1d']:
                rest_frame = file.split('_')[(-1)].split('.')[0]
                if not rv:
                    if rest_frame != 'rv':
                        print('*** ERROR: No rv data available to calibrate wavelength.')
                        return
                if rest_frame == 'rv':
                    wave = wave_raw
                if rv:
                    if rest_frame != 'rv':
                        dwave = rv * wave_raw / c
                        wave = wave_raw - dwave
            if file_type in ac_set.ftypes['2d']:
                if rv:
                    dwave = (rv - berv) * wave_raw / c
                    wave = wave_raw - dwave
                else:
                    print('*** ERROR: No rv data available to calibrate wavelength.')
                    return
    plot_spec = False
    if plot_spec == True:
        ord = 6
        dif_wave = np.diff(wave_raw)
        wave = wave_raw[1:]
        if type(wave[0]) in (list, np.ndarray):
            wave = wave[ord]
            plt.xlabel('Wave_raw ord {} [Ang]'.format(ord))
            plt.ylabel('diff_wave_raw ord {} [Ang]'.format(ord))
        else:
            plt.xlabel('Wave_raw [Ang]')
            plt.ylabel('diff_wave_raw')
        dif_wave = np.diff(wave)
        wave = wave[1:]
        plt.plot(wave, dif_wave, 'k.')
        plt.show()
    data = {}
    data['fits_file'] = os.path.basename(pfile)
    data['flux'] = flux
    data['flux_err'] = flux_err
    data['wave'] = wave
    data['blaze'] = blaze
    data['obs_date'] = date_obs
    data['obj'] = obj
    data['bjd'] = bjd
    data['median_snr'] = median_snr
    data['snr'] = snr
    data['rv'] = rv
    data['rv_err'] = rv_err
    data['fwhm'] = fwhm
    data['fwhm_err'] = fwhm_err
    data['cont'] = cont
    data['cont_err'] = cont_err
    data['bis'] = bis
    data['bis_err'] = bis_err
    data['ccf_noise'] = ccf_noise
    data['airmass'] = airmass
    data['exptime'] = exptime
    data['bv'] = bv
    data['tel'] = tel
    data['instr'] = instr
    data['file_type'] = file_type
    data['data_flg'] = flg
    return data