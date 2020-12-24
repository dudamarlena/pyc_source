# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/v2/Process1D.py
# Compiled at: 2020-01-11 08:49:46
# Size of source mod 2**32: 61555 bytes
"""
    This module contains all the routines needed to process 1D NMR spectra
    
    The following functions realize a set of operations, needed for NMR 1D processing,
    You will find operation for FT analysis, MaxEnt Analysis,
    Inverse Fourier, etc..
    
    Processing are divided in pre - FT - Post phases.
    For instance a typical 1D procesing, would be

    pre()
    ft()
    post()

    but other combinations are possible.

    Most functions take the following arguments :
    arguments :
    audit
        the opened audit file, if empty or set to none, audit will go to the stdout
    filein      the file name of the input file, 
        will loaded before operation, if name is "memory", then processing takes place on the current 2D kernel buffer
    fileout     the file name of the input file, can be "memory"
        will written after operation, if name is "memory", then processing results is left in 2D kernel buffer
    p_in        the dictionary containing all the processing parameters
        most entries are optionnal as entries are protected with try / except
    f_in        the dictionary containing all the details on the spectrum "filein"
    f_out       details on the spectrum "fileout" will be put in this dictionary
    location    the directory where the output files will be written
    
"""
from __future__ import print_function
__author__ = 'Marc A. Delsuc <delsuc@igbmc.fr>'
__date__ = 'Oct 2009'
import math, os
from .Generic import *

def FT1D(audit, p_in_arg, f_in, f_out, inputfilename, outputfilename):
    """
    FT processing of a 1D FID
    
    based on pre_ft_1d() ft_1d() post_ft_1d()
    """
    p_in = build_dict(('pre_ft_1d', 'ft_1d', 'post_ft_1d'), p_in_arg)
    audittrail(audit, 'phase', 'FID preparation phase')
    pre_ft_1d(audit, inputfilename, 'memory', p_in, f_in, f_out)
    audittrail(audit, 'phase', 'Spectral analysis phase')
    ft_1d(audit, 'memory', 'memory', p_in, f_in, f_out)
    audittrail(audit, 'phase', 'Post processing phase')
    post_ft_1d(audit, 'memory', outputfilename, p_in, f_in, f_out)


def MaxEnt1D(audit, p_in_arg, f_in, f_out, inputfilename, outputfilename):
    """
    MaxEnt processing of a 1D FID

    based on pre_ft_1d() maxent_1d() post_maxent_1d()
    """
    p_in = build_dict(('pre_ft_1d', 'maxent_1d', 'post_maxent_1d'), p_in_arg)
    audittrail(audit, 'phase', 'FID preparation phase')
    pre_ft_1d(audit, inputfilename, 'memory', p_in, f_in, f_out)
    audittrail(audit, 'phase', 'Spectral analysis phase by Maximum Entropy')
    maxent_1d(audit, 'memory', 'memory', p_in, f_in, f_out)
    audittrail(audit, 'phase', 'Post processing phase')
    post_maxent_1d(audit, 'memory', outputfilename, p_in, f_in, f_out)


def pre_ft_1d(audit, filein, fileout, p_in, f_in, f_out):
    """
This macro realizes the pre FT operation on a 1D FID

- fid_noise        : evaluate of noise and offset levels in FID
- dc_offset        : corrects for constant offset in FID
- causalize        : changes DSP processed FID (Bruker) to causal FID's by Hilbert transform
- flatten_solvent  : removes solvent signal by FID analysis
- left_shift       : drops first points of the FID 
- right_shift      : adds empty points on the beginning of the FID
- back_extend      : reconstructs missing points in the beginning of the FID by LP analysis

%F1-input-domain%  time
%F1-output-domain% time
%dimensionality%   1

%author% Marc-Andre Delsuc
%version% 6.0
    """
    dim(1)
    if filein != 'memory':
        read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    set_task('FID noise evaluation')
    last = p_in['fid_noise_zone']
    evaln((1 - last) * get_si1_1d(), get_si1_1d())
    f_out['fid_offset'] = get_shift()
    f_in['Noise'] = get_noise()
    f_out['Noise'] = get_noise()
    if key_is_true(p_in, 'dc_offset'):
        set_task('DC-offset correction')
        s = get_shift()
        addbase(s)
        audittrail(audit, 'text', 'vertical shift of FID', 'offset', s)
    if key_is_true(p_in, 'causalize'):
        if key_is_true(p_in, 'causal_corr'):
            raise '\n        causalize and causal_corr are incompatible\n        causality must be corrected only once'
    if key_is_true(p_in, 'causalize'):
        set_task('Causal correction (Bruker digital filter correction')
        causalize(f_in['axisf1_zerotimeposition'])
        f_out['causalize'] = -360 * f_in['axisf1_zerotimeposition']
        audittrail(audit, 'text', 'cauzalisation correction', '1st order phase correction', f_out['causalize'])
    if key_is_true(p_in, 'flatten_solvent'):
        set_task('Solvent flattening')
        flat_solvent(p_in['flat_solv_mode'])
        audittrail(audit, 'text', 'apply solvent flattening', 'algorithm', p_in['flat_solv_mode'])
    if key_is_true(p_in, 'left_shift'):
        set_task('Left shifting of FID')
        left_shift(p_in['left_shift_size'])
        audittrail(audit, 'text', 'FID left shift', 'number of points', p_in['left_shift_size'])
    if key_is_true(p_in, 'right_shift'):
        if key_is_true(p_in, 'b_extend'):
            raise '\n        right_shift and b_extend are incompatible\n        '
    if key_is_true(p_in, 'right_shift'):
        set_task('Right shifting of FID')
        right_shift(p_in['right_shift_size'])
        audittrail(audit, 'text', 'FID right shift', 'number of points', p_in['right_shift_size'])
    if key_is_true(p_in, 'b_extend'):
        set_task('Backward extension')
        n = p_in['b_extend_size']
        order(10)
        if p_in['b_extend_algo'] == 'burg':
            burg_back(get_si1_1d() + n)
        else:
            if p_in['b_extend_algo'] == 'svd':
                dt2svd(get_si1_1d())
                svd2ar(2)
                ar2dt(get_si1_1d() + n, 2)
            f_out['b_extend_order'] = get_order()
            f_out['b_extend_size'] = n
            audittrail(audit, 'text', 'FID back extension', 'number of points', p_in['b_extend_size'], 'algorithm', p_in['b_extend_algo'])
    write_file_1d(audit, fileout)


def ft_1d(audit, filein, fileout, p_in, f_in, f_out):
    """
This macro realizes the FT operation on a 1D FID

- truncate      : truncates the FID by removing the last points
- lp_extend     : extend FID with a Linear Prediction algorithm
- apodize       : standard apodisation by a window
- fourier_transform : performs the Fourier transform
- causal_corr   : performs causal correction of the spectrum if not done on the FID
- reverse       : reverses the spectral axis after FT

%F1-input-domain%  time
%F1-output-domain% frequency
%dimensionality%   1

%author% Marc-Andre Delsuc
%version% 6.0

    """
    dim(1)
    if filein != 'memory':
        read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    if key_is_true(p_in, 'truncate'):
        set_task('FID truncation')
        s = p_in['trunc_size']
        if s <= 0:
            raise 'Cannot truncate to 0'
        if s > get_si1_1d():
            raise 'Error with truncation size (larger than actual size)'
        initial = get_si1_1d()
        s = int(min(get_si1_1d(), s))
        chsize(s)
        audittrail(audit, 'text', 'FID truncation before FT', 'initial_size', initial, 'final size', get_si1_1d())
    if key_is_true(p_in, 'lp_extend'):
        set_task('Linear prediction extension')
        order(int(p_in['lp_ext_order']))
        if p_in['lp_ext_algo'] == 'burg':
            t = get_itype_1d()
            itype(1)
            burg(p_in['lp_ext_size'])
            print('BURG', p_in['lp_ext_size'], get_si1_1d(), get_order(), t)
            itype(t)
        else:
            if p_in['lp_ext_algo'] == 'mirror':
                t = get_itype_1d()
                itype(1)
                burg(p_in['lp_ext_size'])
                burg_mirror(p_in['lp_ext_off'], p_in['lp_ext_size'])
                itype(t)
            else:
                if p_in['lp_ext_algo'] == 'lpsvd':
                    t = get_itype_1d()
                    itype(1)
                    burg(p_in['lp_ext_size'])
                    dt2svd(get_si1_1d())
                    svd2ar(1)
                    ar2dt(p_in['lp_ext_size'], 1)
                    itype(t)
                else:
                    if p_in['lp_ext_algo'] == 'lpsvd_stable':
                        t = get_itype_1d()
                        itype(1)
                        burg(p_in['lp_ext_size'])
                        dt2svd(get_si1_1d())
                        svd2ar(1)
                        ar2rt(1)
                        rtreflect(1)
                        rt2ar(1)
                        ar2dt(p_in['lp_ext_size'], 1)
                        itype(t)
                    audittrail(audit, 'text', 'FID extension before FT', 'algorithm', p_in['lp_ext_algo'], 'LP order', p_in['lp_ext_order'], 'Final size', p_in['lp_ext_size'])
                    if key_is_not_false(p_in, 'lp_ext_apod'):
                        sin(0)
                        audittrail(audit, 'text', 'Apodisation after extension', 'function', 'sin(0)')
    if key_is_true(p_in, 'apodize'):
        if p_in['apodisation'] != 'none':
            set_task('Apodisation')
            apodise(p_in.raw('apodisation'))
            audittrail(audit, 'text', 'FID apodisation before FT', 'function', p_in['apodisation'])
    if key_is_true(p_in, 'fourier_transform'):
        set_task('Fourier transformation')
        if key_is_true(p_in, 'ask_for_ftsize'):
            final = int(p_in['ft_size'])
        else:
            if key_is_true(p_in, 'lp_extend'):
                final = 2 * power2(get_si1_1d() - 2)
            else:
                final = 4 * power2(get_si1_1d() - 2)
        initial = get_si1_1d()
        chsize(final)
        if p_in['ft_type'] != 'none':
            if p_in['ft_type'] == 'ft':
                ft()
            else:
                if p_in['ft_type'] == 'rft':
                    rft()
                else:
                    if p_in['ft_type'] == 'ft_sim':
                        ft_sim()
                    else:
                        if p_in['ft_type'] == 'ft_seq':
                            ft_seq()
                        else:
                            raise 'Unknown Fourier transform'
        f_out['size_for_ft'] = final
        audittrail(audit, 'text', 'Fourier transformation', 'FT type', p_in['ft_type'], 'initial_size', initial, 'final size', final)
    if key_is_true(p_in, 'causal_corr'):
        set_task('Causal correction')
        try:
            delay = float(f_in['axisf1_zerotimeposition'])
        except:
            raise
            delay = 0.0

        com_phase(0.0, -360.0 * delay)
        f_out['causalize'] = -360.0 * delay
        audittrail(audit, 'text', 'Causal correction', '1st order phase correction', f_out['causalize'])
    if key_is_true(p_in, 'reverse'):
        set_task('Spectrum reverse')
        reverse()
        if get_itype_1d() == 1:
            invf()
        audittrail(audit, 'text', 'Reverse spectral axis')
    write_file_1d(audit, fileout)


def post_ft_1d(audit, filein, fileout, p_in, f_in, f_out):
    """
This macro realizes the Post processing of a 1D spectrum

- modulus       : takes the complex modulus of the spectrum
- phase         : applies a phase correction to the spectrum
- autophase     : automatically computes the phase correction of the spectrum
- invHilbert    : apply an inverse Hilbert transform
- calibration   : calibrate the ppm scale on the spectrum
- spectral_zone : extract one spectral zone of the spectrum
- baseline_correction : applies a baseline correction to the spectrum
- smoothing     : apply a smoothing filter to the data-set
- median        : apply a median filter to the data-set
- derivative    : compute the nth derivative of the data-set
- spec_noise    : evaluate noise, estimated by finding an empty zone

%F1-input-domain%  frequency
%F1-output-domain% frequency
%dimensionality%   1

%author% Marc-Andre Delsuc
%version% 6.0
    """
    dim(1)
    if filein != 'memory':
        read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    tocomplex()
    if key_is_true(p_in, 'modulus'):
        set_task('modulus computation')
        modulus()
        audittrail(audit, 'text', 'modulus applied')
    else:
        if key_is_true(p_in, 'phase'):
            set_task('Phase correction')
            phase(p_in['phase_0'], p_in['phase_1'])
            audittrail(audit, 'text', 'phase correction applied', '0th order', p_in['phase_0'], '1th order', p_in['phase_1'])
        if key_is_true(p_in, 'autophase'):
            set_task('Automatic phase correction')
            if p_in['phase_algo'] == 'apmin':
                apmin()
            if p_in['phase_algo'] == 'apsl':
                apsl()
            f_out['autophase_0'] = get_ph0()
            f_out['autophase_1'] = get_ph1()
            audittrail(audit, 'text', 'automatic phase correction applied', 'algorithm', p_in['phase_algo'], '0th order', get_ph0(), '1th order', get_ph1())
        if key_is_true(p_in, 'invhilbert'):
            set_task('Inverse Hilbert Transform')
            invhilbert()
            audittrail(audit, 'text', 'inverse Hilbert transform applied')
        set_task('Calibration')
        offset(p_in['calibration'] * get_freq_1d())
        audittrail(audit, 'text', 'offset applied', 'calibration', p_in['calibration'])
        if key_is_true(p_in, 'spectral_zone'):
            set_task('Spectral zone extraction')
            if p_in['spec_zone_left_unit'] == 'ppm':
                l = ptoi(p_in['spec_zone_left'], 1, 1)
            else:
                if p_in['spec_zone_left_unit'] == 'hz':
                    l = htoi(p_in['spec_zone_left'], 1, 1)
                else:
                    if p_in['spec_zone_left_unit'] == 'index':
                        l = p_in['spec_zone_left']
                    else:
                        raise 'Error with spec_zone_left_unit'
            if p_in['spec_zone_right_unit'] == 'ppm':
                r = ptoi(p_in['spec_zone_right'], 1, 1)
            else:
                if p_in['spec_zone_right_unit'] == 'hz':
                    r = htoi(p_in['spec_zone_right'], 1, 1)
                else:
                    if p_in['spec_zone_right_unit'] == 'index':
                        r = p_in['spec_zone_right']
                    else:
                        raise 'Error with spec_zone_right_unit'
            l = max(1, round(l))
            r = min(get_si1_1d(), round(r))
            if l > r:
                raise 'Wrong spectral zone coordinates'
            if r - l < 8:
                raise 'spectral zone too small'
            if l != 1 | r != get_si1_1d():
                extract(int(l), int(r))
            f_out['spec_zone_left'] = l
            f_out['spec_zone_right'] = r
            audittrail(audit, 'text', 'spectral extraction', 'left point', f_out['spec_zone_left'], 'right point', f_out['spec_zone_right'], 'final size', get_si1_1d())
        else:
            f_out['spec_zone_left'] = 1
        f_out['spec_zone_right'] = get_si1_1d()
    if key_is_true(p_in, 'baseline'):
        set_task('Baseline correction')
        toreal()
        pivots = 'not used'
        bcorder = 'not used'
        bcc = 1
        bc = p_in['bcorr_algo']
        if bc.find('linear') + bc.find('spline') != -2:
            l = p_in['bcorr_pivots']
            n = 0
            pivots = l
            off = 0
            lst = l.split()
            for l in lst:
                n = n + 1
                point_input(float(l))
                point_push()
                off = off + val1d(int(l))

            off = off / n
        lst = bc.split()
        for bcalgo in lst:
            if bcalgo == 'offset':
                spec_noise(p_in['spec_noise_n'])
                addbase(get_shift())
                f_out['spec_offset'] = get_shift()
            else:
                if bcalgo == 'linear':
                    bcorr(1, p_in['bcorr_radius'])
                else:
                    if bcalgo == 'spline':
                        bcorr(2, p_in['bcorr_radius'])
                    else:
                        if bcalgo == 'quest':
                            bcorder = p_in['bcorr_order']
                            bcorr_quest(bcorder)
                        else:
                            if bcalgo == 'polynomial':
                                if get_debug():
                                    print('Baseline correction not available in DEBUG mode')
                                else:
                                    bcorrp0()
                                    bcorr(3)
                            else:
                                if bcalgo == 'moving_average':
                                    if get_debug():
                                        print('Baseline correction not available in DEBUG mode')
                                    else:
                                        bcorrp1()
                                        bcorr(3)
                                        bcorrp0()
                                else:
                                    raise 'Error with baseline correction algorithm'
            audittrail(audit, 'text', 'Baseline correction -' + repr(bcc), 'algorithm', bcalgo, 'pivots', pivots, 'order', bcorder)
            bcc = bcc + 1

    if key_is_true(p_in, 'smoothing'):
        set_task('Smoothing filter applied')
        toreal()
        if key_is_true(p_in, 'smooth_iteration'):
            it = p_in['smooth_iteration']
        else:
            it = 1
        for i in range(it):
            smooth(p_in['smooth_w'])

        audittrail(audit, 'text', 'Smoothing filter', 'Number of points', p_in['smooth_w'], 'Number of iterations', p_in['smooth_iteration'])
    if key_is_true(p_in, 'median'):
        set_task('Median filter applied')
        toreal()
        median(p_in['median_w'], p_in['median_i'])
        audittrail(audit, 'text', 'Median filter', 'number of points', p_in['median_w'], 'index', p_in['median_i'])
    if key_is_true(p_in, 'derivative'):
        set_task('Dataset derivative computed')
        toreal()
        derivative(p_in['deriv_nth'], p_in['deriv_smooth'])
        audittrail(audit, 'text', 'Derivative filter', 'number of points', p_in['deriv_nth'], 'index', p_in['deriv_smooth'])
    if key_is_true(p_in, 'select_state'):
        t1, t2 = get_itype(2)
        if p_in['f1_state'] == 'complex':
            if t1 == 0:
                set_task('complex reconstruction')
            tocomplex('f1')
            p1s = 'complex'
        else:
            if p_in['f1_state'] == 'real':
                toreal('f1')
                p1s = 'real'
            elif t1 == 1:
                t1s = 'complex'
            else:
                t1s = 'real'
            audittrail(audit, 'text', 'Complex state of the data', 'axis', 'was ' + t1s + ' now forced to ' + p1s)
    set_task('Noise evaluation')
    spec_noise(p_in['spec_noise_n'])
    f_out['Noise'] = get_noise()
    if not key_is_true(p_in, 'modulus'):
        tocomplex()
    write_file_1d(audit, fileout)


def write_file_1d(audit, fileout):
    """
    write a 1D file and update the audittrail
    """
    if fileout != 'memory':
        dim(1)
        writec(fileout)
        if get_itype_1d() == 1:
            sz = 'Complex ' + repr(get_si1_1d() / 2)
        else:
            sz = 'Real ' + repr(get_si1_1d())
        audittrail(audit, 'text', 'output file created :', 'file name', fileout, 'size', sz)


def pp_1d(audit, filein, filepeak, p_in, f_in, f_out):
    """
This macro realizes the peak picking of a 1D spectrum
- spec_noise : evaluate noise, estimated by finding an empty zone
- prefilter  : smooths the spectrum before peak-picking, modification is not stored permanently
- restrict   : restricts the peak picking to a certain spectral zone 
- peakpick   : do the peak picking, by detecting local extrema 
- aggregate  : sorts peak list to aggregate peaks close from each other

    
%F1-input-domain%  frequency
%F1-output-domain% frequency
%dimensionality%   1

%author% Marc-Andre Delsuc
%version% 6.0
    """
    dim(1)
    if filein != 'memory':
        read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    if get_itype_1d() == 1:
        real()
        audittrail(audit, 'text', 'complex data-set, removing the imaginary part')
    else:
        size_ini = get_si1_1d()
        put('data')
        set_task('Noise evaluation')
        if p_in['spec_noise']:
            spec_noise(p_in['spec_noise_n'])
            f_out['Noise'] = get_noise()
        else:
            noise(f_in['Noise'])
            f_out['Noise'] = get_noise()
        if key_is_true(p_in, 'prefilter'):
            set_task('Filtering before Peak-Picking')
            chsize(2 * power2(get_si1_1d() - 1))
            size_ft = get_si1_1d()
            iftbis()
            if p_in['peak_sign'] == 'both':
                contrast = 0.7
            else:
                contrast = 1.4
            gaussenh(p_in['prefilter_value'], contrast)
            sqsin(0)
            ftbis()
            chsize(size_ini)
            audittrail(audit, 'text', 'Pre Filter applied to data-set', 'smoothing value in Hz (using gaussenh)', p_in['prefilter_value'])
        if key_is_true(p_in, 'restrict'):
            set_task('Restricting peak-picking zone')
            if p_in['restrict_left_unit'] == 'ppm':
                l = ptoi(p_in['restrict_left'], 1, 1)
            else:
                if p_in['restrict_left_unit'] == 'hz':
                    l = htoi(p_in['restrict_left'], 1, 1)
                else:
                    if p_in['restrict_left_unit'] == 'index':
                        l = p_in['restrict_left']
                    else:
                        raise 'Error with restrict_left_unit'
            if p_in['restrict_right_unit'] == 'ppm':
                r = ptoi(p_in['restrict_right'], 1, 1)
            else:
                if p_in['restrict_right_unit'] == 'hz':
                    r = htoi(p_in['restrict_right'], 1, 1)
                else:
                    if p_in['restrict_right_unit'] == 'index':
                        r = p_in['restrict_right']
                    else:
                        raise 'Error with restrict_right_unit'
            l = max(1, round(l))
            r = min(get_si1_1d(), round(r))
            if l > r:
                raise 'Wrong restrict zone coordinates'
            if r - l < 8:
                raise 'restrict zone too small'
            zoom(1, l, r)
            f_out['restrict_left'] = l
            f_out['restrict_right'] = r
            audittrail(audit, 'text', 'spectral extraction', 'left point', f_out['restrict_left'], 'right point', f_out['restrict_right'])
        else:
            zoom(0)
        f_out['restrict_left'] = 1
        f_out['restrict_right'] = get_si1_1d()
    if key_is_true(p_in, 'peakpick'):
        set_task('Peak-picking')
        com_max()
        mn = max(geta_max(1) / p_in['ratio_thresh'], p_in['noise_thresh'] * get_noise())
        minimax(mn, geta_max(1) + 1)
        print('+++ minimax ' + repr(mn) + ' ' + repr(geta_max(1) + 1))
        f_out['low_limit'] = mn
        if p_in['peak_sign'] == 'negative':
            mult(-1)
        else:
            if p_in['peak_sign'] == 'both':
                com_abs()
            pkclear()
            peak()
            f_out['nb_detect_peaks'] = get_npk1d()
            print('+++ detected ' + repr(get_npk1d()))
            get('data')
            pkreset()
            audittrail(audit, 'text', 'Peak Picking applied', 'low limit for peak detection', repr(mn), 'number of peak detected', repr(get_npk1d()))
    if key_is_true(p_in, 'aggregate'):
        audittrail(audit, 'text', 'aggregate - Reste a faire')
    pkwrite_p(filepeak)
    audittrail(audit, 'text', 'Peak Picking file stored', 'filename', filepeak)


def ift_1d(audit, filein, filout, p_in, f_in, f_out):
    """
This macro Computes the Inverse Fourier transform of a 1D spectrum

- apodize       : standard apodisation
- inverseFourier : performs the inverse Fourier transform
- reverse       : reverses the spectral axis after FT
    
%F1-input-domain%  frequency
%F1-output-domain% time
%dimensionality%   1

%author% Marc-Andre Delsuc
%version% 6.0
    """
    dim(1)
    if filein != memory:
        com_read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    if key_is_true(p_in, 'apodize'):
        if p_in['apodisation'] != 'none':
            apodise(p_in.raw('apodisation'))
            audittrail(audit, 'text', 'spectrum apodisation before iFT', 'function', p_in['apodisation'])
    if key_is_true(p_in, 'inverseFourier'):
        initial = get_si1_1d()
        if p_in['ask_for_iftsize']:
            final = p_in['ift_size']
        else:
            final = 2 * power2(get_si1_1d() - 2)
            if p_in['ift_type'] == 'ifthilbert':
                if get_itype_1d() == 1:
                    final = final / 2
            elif p_in['ift_type'] == 'ift':
                chsize(final)
                if get_itype_1d() == 0:
                    iftbis()
                else:
                    ift()
            else:
                if p_in['ift_type'] == 'ifthilbert':
                    if get_itype_1d() == 0:
                        chsize(final)
                        iftbis()
                    else:
                        chsize(2 * final)
                        real()
                        iftbis()
                else:
                    raise 'error in ift type'
            f_out['size_for_ift'] = get_si1_1d()
            audittrail(audit, 'text', 'inverse Fourier transformation', 'iFT type', p_in['ift_type'], 'initial size', initial, 'final size', f_out['size_for_ift'])
    if key_is_true(p_in, 'reverse'):
        reverse()
        if get_itype_1d() == 1:
            invf()
        auditrail('text', 'Reverse time axis')
    write_file_1d(audit, fileout)


def integ_1d(audit, filein, integratout, p_in, f_in, f_out):
    """
This macro Computes integrales of a 1D spectrum
- integral    : omputes integral positions from peaks

    
%F1-input-domain%  frequency
%F1-output-domain% frequency
%dimensionality%   1

%author% Marc-Andre Delsuc
%version% 6.0
    """
    dim(1)
    if filein != 'memory':
        read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    print('+++ ITYPE = ' + repr(get_itype_1d()))
    if get_itype_1d() == 1:
        real()
        audittrail(audit, 'text', 'complex data-set, removing the imaginary part')
    set_task('integration')
    inte = 0
    exi = p_in['integ_extention'] * get_si1_1d() / get_specw_1d()
    agi = p_in['integ_aggregate'] * get_si1_1d() / get_specw_1d()
    left = {}
    right = {}
    if get_npk1d() == 1:
        inte = 1
        left[1] = max(1, geta_pk1d_f(1) - exi)
        right[1] = min(get_si1_1d(), geta_pk1d_f(1) + exi)
    else:
        if get_npk1d() > 1:
            inte = 0
            left[1] = max(1, geta_pk1d_f(1) - exi)
            i = 2
            while i <= get_npk1d():
                if geta_pk1d_f(i) - geta_pk1d_f(i - 1) > agi:
                    inte = inte + 1
                    right[inte] = min(get_si1_1d(), geta_pk1d_f(i - 1) + exi)
                    left[inte + 1] = max(1, geta_pk1d_f(i) - exi)
                i = i + 1

            inte = inte + 1
            right[inte] = min(get_si1_1d(), geta_pk1d_f(get_npk1d()) + exi)
        f_out['nb_integral'] = inte
        audittrail(audit, 'text', 'Standard aggregation applied', 'aggregate width', p_in['integ_aggregate'], 'extension width', p_in['integ_extention'], 'number of integral detected', inte)
        off = {}
        for i in range(1, inte + 1):
            left[i] = int(round(left[i]))
            right[i] = int(round(right[i]))
            off[i] = 0.5 * (val1d(left[i]) + val1d(right[i]))

        put('data')
        int1d()
        fout = open(integratout, 'w')
        for i in range(1, inte + 1):
            integral = val1d(right[i]) - val1d(left[i]) - off[i] * float(right[i] - left[i])
            if i == 1:
                calibration = integral
            fout.write(repr(i) + '=' + repr(left[i]) + ' ' + repr(right[i]) + ' ' + repr(off[i]) + ' ' + repr(integral) + ' ' + repr(integral / calibration))
            fout.write('\n')

        fout.close()
        get('data')
        audittrail(audit, 'text', 'Integral file stored', 'filename', integratout)


def maxent_1d(audit, filein, fileout, p_in, f_in, f_out):
    """
This macro realizes the MaxEnt analysis of a 1D FID
- freq_massage  : computes a temporary Fourier transform
- truncate   : truncates the FID by removing the last points
- preconvoluate  :apply a preconvolution before analysis, this may help stability of the algorithm and enhance noise rejection
- partialsampling   : set-up for processing data partially sampled in the time domain
- deconvoluate : apply a deconvolution during analysis,
- maxent : apply MaxEnt analysis,

    
%F1-input-domain%  frequency
%F1-output-domain% frequency
%dimensionality%   1

%author% Marc-Andre Delsuc
%version% 6.0
    """
    dim(1)
    if filein != 'memory':
        read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    if key_is_true(p_in, 'freq_massage'):
        final = 4 * power2(get_si1_1d() - 2)
        initial = get_si1_1d()
        chsize(final)
        if p_in['ft_type'] != 'none':
            if p_in['ft_type'] == 'ft':
                ft()
            else:
                if p_in['ft_type'] == 'rft':
                    rft()
                else:
                    if p_in['ft_type'] == 'ft_sim':
                        ft_sim()
                    else:
                        if p_in['ft_type'] == 'ft_seq':
                            ft_seq()
                        else:
                            f_out['size_for_ft'] = final
                            audittrail(audit, 'text', 'temporary Fourier transformation,', 'FT type', p_in['ft_type'], 'initial size', initial, 'final size', f_out['size_for_ft'])
                            if key_is_true(p_in, 'phase'):
                                phase(p_in['phase_0'], p_in['phase_1'])
                                audittrail(audit, 'text', 'phase correction applied', '0th order', p_in['phase_0'], '1th order', p_in['phase_1'])
                            real()
                            iftbis()
                            chsize(initial)
                            f_out['mock_fid_size'] = initial
                            audittrail(audit, 'text', 'Back to time domain', 'final size ', initial)
    if key_is_true(p_in, 'truncate'):
        s = int(p_in['trunc_size'])
        if s <= 0:
            raise 'Cannot truncate to 0'
        if s > get_si1_1d():
            raise 'Error with truncation size (larger than actual size)'
        initial = get_si1_1d()
        chsize(min(get_si1_1d(), s))
        audittrail(audit, 'text', 'FID truncation before FT', 'initial_size', initial, 'final size', get_si1_1d())
    elif key_is_true(p_in, 'preconvoluate'):
        if p_in['preconvolution'] != 'none':
            apodise(p_in.raw('preconvolution'))
            audittrail(audit, 'text', 'FID preconvolution before MaxEnt analysis', 'function', p_in['preconvolution'])
        put('data')
        noise(f_out['Noise'])
        audittrail(audit, 'text', 'Mock FID stored', 'fid size', get_si1_1d(), 'noise value', get_noise())
        if key_is_true(p_in, 'partialsampling'):
            sampf = location + os.sep + p_in['samplingfile']
            sampling(sampf)
            sign = get_returned()
            partial = sign / get_si1_1d()
            audittrail(audit, 'text', 'Set-up for partial sampling during MaxEnt analysis', 'sampling file', sampf, 'number of sampled points', sign, 'mean density of sampling', str(100 * partiall) + '%')
    else:
        partial = 1.0
    if key_is_true(p_in, 'deconvoluate') and p_in['deconvolution'] != 'none':
        itype(0)
        one()
        itype(1)
        apodise(p_in.raw('deconvolution'))
        put('filter')
        audittrail(audit, 'text', 'deconvolution set-up for MaxEnt analysis', 'function', p_in['deconvolution'])
        com_filter(1)
        sumcons(0)
        nchannel(1)
    else:
        com_filter(0)
        nchannel(1)
        audittrail(audit, 'text', 'No deconvolution set-up for MaxEnt analysis')
    if key_is_true(p_in, 'maxent'):
        if key_is_true(p_in, 'me_preset'):
            me_preset(p_in['preset_value'])
            audittrail(audit, 'text', 'Preset for MaxEnt Analysisusing preset level', p_in['preset_value'])
        else:
            me_preset(3)
            com_iter(int(p_in['iteration']))
            ndisp(int(p_in['control']))
            lambsp(float(p_in['lambsp']))
            lambcont(int(p_in['lambcont']))
        noise(get_noise() * p_in['noise_weight'] * partial)
        audittrail(audit, 'text', 'Parameters for MaxEnt Analysis', 'size of reconstruction', p_in['me_size'], 'weighted noise', get_noise(), 'Algorithm flags', get_algo(), 'lambda control', get_lambcont(), 'lambda multiplier', get_lambsp(), 'global iteration', get_iter(), 'control', get_ndisp(), 'line minimisation iteration', get_miniter())
        get('data')
        sz = int(p_in['me_size'])
        put('data')
        maxent(sz)
        audittrail.g('text', 'MaxEnt Analysis applied', 'number of iteration performed', get_iterdone(), 'final chi square', getchi2(), 'final entropy', get_entropy(), 'final lambda', get_lambda(), 'final convergence criterium', get_convergence())
        write_file_1d(audit, fileout)


def post_maxent_1d(audit, filein, fileout, p_in, f_in, f_out):
    """
    post processing of a 1D spectrum processed by MaxEnt
    """
    dim(1)
    if filein != 'memory':
        read(filein)
        if get_dim() != 1:
            raise 'This is not a 1D dataset'
        audittrail(audit, 'text', 'loading in memory', 'filename', filein)
    else:
        audittrail(audit, 'text', 'using data in memory')
    offset(p_in['calibration'] * get_freq_1d())
    audittrail(audit, 'text', 'calibration offset applied', 'calibration', p_in['calibration'])
    if key_is_true(p_in, 'spectral_zone'):
        if p_in['spec_zone_left_unit'] == 'ppm':
            l = ptoi(p_in['spec_zone_left'], 1, 1)
        else:
            if p_in['spec_zone_left_unit'] == 'hz':
                l = htoi(p_in['spec_zone_left'], 1, 1)
            else:
                if p_in['spec_zone_left_unit'] == 'index':
                    l = p_in['spec_zone_left']
                else:
                    raise 'Error with spec_zone_left_unit'
        if p_in['spec_zone_right_unit'] == 'ppm':
            r = ptoi(p_in['spec_zone_right'], 1, 1)
        else:
            if p_in['spec_zone_right_unit'] == 'hz':
                r = htoi(p_in['spec_zone_right'], 1, 1)
            else:
                if p_in['spec_zone_right_unit'] == 'index':
                    r = p_in['spec_zone_right']
                else:
                    raise 'Error with spec_zone_right_unit'
        l = max(1, round(l))
        r = min(get_si1_1d(), round(r))
        if l > r:
            raise 'Wrong spectral zone coordinates'
        if r - l < 8:
            raise 'spectral zone too small'
        if not l != 1:
            if r != get_si1_1d():
                extract(l, r)
            f_out['spec_zone_left'] = l
            f_out['spec_zone_right'] = r
            audittrail(audit, 'text', 'spectral extraction', 'left point', f_out['spec_zone_left'], 'right point', f_out['spec_zone_right'], 'final size', get_si1_1d())
        else:
            f_out['spec_zone_left'] = 1
            f_out['spec_zone_right'] = get_si1_1d()
        if key_is_true(p_in, 'baseline'):
            if get_debug():
                print('Baseline correction not available in DEBUG mode')
    else:
        toreal()
        pivots = 'not used'
        if p_in['bcorr_algo'] == 'linear' or p_in['bcorr_algo'] == 'spline':
            l = p_in['bcorr_pivots']
            n = 0
            pivots = l
            off = 0
            lst = l.split()
            for l in lst:
                n = n + 1
                point_input(int(l))
                point_push()
                off = off + val1d(int(l))

            off = off / n
        elif p_in['bcorr_algo'] == 'offset':
            addbase(off)
            f_out['spec_offset'] = off
        else:
            if p_in['bcorr_algo'] == 'linear':
                bcorr(1, p_in['bcorr_radius'], '%%')
            else:
                if p_in['bcorr_algo'] == 'spline':
                    bcorr(2, p_in['bcorr_radius'], '%%')
                else:
                    if p_in['bcorr_algo'] == 'polynomial':
                        bcorrp0()
                        bcorr(3)
                    else:
                        if p_in['bcorr_algo'] == 'moving_average':
                            bcorrp1()
                            bcorr(3)
                            bcorrp0()
                        else:
                            if p_in['bcorr_algo'] == 'polynomial+moving_average':
                                bcorrp0()
                                bcorr(3)
                                bcorrp1()
                                bcorr(3)
                                bcorrp0()
                            else:
                                if p_in['bcorr_algo'] == 'moving_average+polynomial':
                                    bcorrp1()
                                    bcorr(3)
                                    bcorrp0()
                                    bcorr(3)
                                else:
                                    raise 'Error with baseline correction algorithm'
        audittrail(audit, 'text', 'Baseline correction', 'algorithm', p_in['bcorr_algo'], 'pivots', pivots)
    write_file_1d(audit, fileout)