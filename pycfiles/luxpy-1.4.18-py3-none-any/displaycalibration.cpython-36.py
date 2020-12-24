# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\toolboxes\dispcal\displaycalibration.py
# Compiled at: 2020-03-23 12:35:14
# Size of source mod 2**32: 37341 bytes
"""
Module for display calibration
==============================
 :_PATH_DATA: path to package data folder   

 :_RGB:  set of RGB values that work quite well for display characterization
   
 :_XYZ: example set of measured XYZ values corresponding to the RGB values in _RGB
   
 :calibrate(): Calculate TR parameters/lut and conversion matrices
   
 :calibration_performance(): Check calibration performance (cfr. individual and average color differences for each stimulus). 

 :rgb_to_xyz(): Convert input rgb to xyz
    
 :xyz_to_rgb(): Convert input xyz to rgb
     
 :DisplayCalibration(): Calculate TR parameters/lut and conversion matrices and store in object.
       

   
.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import _PKG_PATH, _SEP, np, sp, plt, pd, math, _CMF, cie_interp, colortf, _CSPACE_AXES
__all__ = [
 '_PATH_DATA', 'calibrate', 'calibration_performance', 'rgb_to_xyz', 'xyz_to_rgb', 'DisplayCalibration', '_RGB', '_XYZ']
_PATH = _PKG_PATH + _SEP + 'toolboxes' + _SEP + 'dispcal' + _SEP
_PATH_DATA = _PATH + _SEP + 'data' + _SEP
_RGB = pd.read_csv((_PATH_DATA + 'RGBcal.csv'), sep=',', header=None).values
_XYZ = pd.read_csv((_PATH_DATA + 'XYZcal.csv'), sep=',', header=None).values

def _clamp0(x):
    """Clamp x to 0 to avoid negative values."""
    x[x < 0] = 0
    return x


TR = lambda x, *p: p[1] + p[2] * x ** p[0]
TRi = lambda x, *p: ((x.T - p[1]) / p[2]) ** (1 / p[0])

def _rgb_linearizer(rgb, tr, tr_type='lut'):
    """ Linearize rgb using tr tone response function or lut """
    if tr_type == 'gog':
        return _clamp0(np.array([TR(rgb[:, i], *tr[i]) for i in range(3)]).T)
    if tr_type == 'lut':
        return _clamp0(np.array([tr[(np.asarray((rgb[:, i]), dtype=(np.int)), i)] for i in range(3)]).T)


def _rgb_delinearizer(rgblin, tr, tr_type='lut'):
    """ De-linearize linear rgblin using tr tone response function or lut """
    if tr_type == 'gog':
        return np.array([TRi(rgblin[:, i], *tr[i]) for i in range(3)]).T
    if tr_type == 'lut':
        maxv = tr.shape[0] - 1
        bins = np.vstack((tr - np.diff(tr, axis=0, prepend=0) / 2, tr[-1, :] + 0.01))
        idxs = np.array([np.digitize(rgblin[:, i], bins[:, i]) - 1 for i in range(3)]).T
        idxs[idxs > maxv] = maxv
        rgb = np.arange(tr.shape[0])[idxs]
        return rgb


def _parse_rgbxyz_input(rgb, xyz=None, sep=',', header=None):
    """ Parse the rgb and xyz inputs """
    if isinstance(rgb, str):
        rgb = pd.read_csv(rgb, sep=sep, header=header).values
    else:
        if isinstance(xyz, str):
            xyz = pd.read_csv(xyz, sep=sep, header=header).values
        if xyz is None:
            rgb, xyz = rgb[..., :3], rgb[..., 3:6]
    return (
     rgb, xyz)


def calibrate(rgbcal, xyzcal, L_type='lms', tr_type='lut', cieobs='1931_2', nbit=8, cspace='lab', avg=lambda x: (x ** 2).mean() ** 0.5, verbosity=1, sep=',', header=None):
    """
    Calculate TR parameters/lut and conversion matrices.
    
    Args:
        :rgbcal:
            | ndarray [Nx3] or string with filename of RGB values 
            | rgcal must contain at least the following type of settings:
            | - pure R,G,B: e.g. for pure R: (R != 0) & (G==0) & (B == 0)
            | - white(s): R = G = B = 2**nbit-1
            | - gray(s): R = G = B
            | - black(s): R = G = B = 0
            | - binary colors: cyan (G = B, R = 0), yellow (G = R, B = 0), magenta (R = B, G = 0)
        :xyzcal:
            | ndarray [Nx3] or string with filename of measured XYZ values for 
            | the RGB settings in rgbcal.
        :L_type:
            | 'lms', optional
            | Type of response to use in the derivation of the Tone-Response curves.
            | options:
            |  - 'lms': use cone fundamental responses: L vs R, M vs G and S vs B 
            |           (reduces noise and generally leads to more accurate characterization) 
            |  - 'Y': use the luminance signal: Y vs R, Y vs G, Y vs B
        :tr_type:
            | 'lut', optional
            | options:
            |  - 'lut': Derive/specify Tone-Response as a look-up-table
            |  - 'gog': Derive/specify Tone-Response as a gain-offset-gamma function
        :cieobs:
            | '1931_2', optional
            | CIE CMF set used to determine the XYZ tristimulus values
            | (needed when L_type == 'lms': determines the conversion matrix to
            | convert xyz to lms values)
        :nbit:
            | 8, optional
            | RGB values in nbit format (e.g. 8, 16, ...)
        :cspace:
            | color space or chromaticity diagram to calculate color differences in
            | when optimizing the xyz_to_rgb and rgb_to_xyz conversion matrices.
        :avg:
            | lambda x: ((x**2).mean()**0.5), optional
            | Function used to average the color differences of the individual RGB settings
            | in the optimization of the xyz_to_rgb and rgb_to_xyz conversion matrices.
        :verbosity:
            | 1, optional
            | > 0: print and plot optimization results
        :sep:
            | ',', optional
            | separator in files with rgbcal and xyzcal data
        :header:
            | None, optional
            | header specifier for files with rgbcal and xyzcal data 
            | (see pandas.read_csv)
            
    Returns:
        :M:
            | linear rgb to xyz conversion matrix
        :N:
            | xyz to linear rgb conversion matrix
        :tr:
            | Tone Response function parameters or lut
        :xyz_black:
            | ndarray with XYZ tristimulus values of black
        :xyz_white:
            | ndarray with tristimlus values of white
    """
    rgbcal, xyzcal = _parse_rgbxyz_input(rgbcal, xyz=xyzcal, sep=sep, header=header)
    p_blacks = (rgbcal[:, 0] == 0) & (rgbcal[:, 1] == 0) & (rgbcal[:, 2] == 0)
    xyz_black = xyzcal[p_blacks, :].mean(axis=0, keepdims=True)
    xyz_fc = xyzcal - xyz_black
    p_pure = [
     (rgbcal[:, 1] == 0) & (rgbcal[:, 2] == 0),
     (rgbcal[:, 0] == 0) & (rgbcal[:, 2] == 0),
     (rgbcal[:, 0] == 0) & (rgbcal[:, 1] == 0)]
    if L_type == 'Y':
        L = np.array([xyz_fc[:, 1] for i in range(3)]).T
    else:
        if L_type == 'lms':
            lms = (math.normalize_3x3_matrix(_CMF[cieobs]['M'].copy()) @ xyz_fc.T).T
            L = np.array([lms[:, i] for i in range(3)]).T
        if tr_type == 'gog':
            par = np.array([sp.optimize.curve_fit(TR, (rgbcal[(p_pure[i], i)]), (L[(p_pure[i], i)] / L[(p_pure[i], i)].max()), p0=[1, 0, 1])[0] for i in range(3)])
            tr = par
        elif tr_type == 'lut':
            lut = np.array([cie_interp((np.vstack((rgbcal[(p_pure[i], i)], L[(p_pure[i], i)] / L[(p_pure[i], i)].max()))), (np.arange(2 ** nbit)), kind='cubic')[1, :] for i in range(3)]).T
            for i in range(3):
                p0 = np.where(np.diff(lut[:, i]) <= 0)[0]
                if p0.any():
                    p0 = range(0, p0[(-1)])
                    lut[(p0, i)] = 0

            tr = lut
    if verbosity > 0:
        colors = 'rgb'
        linestyles = ['-', '--', ':']
        rgball = np.repeat((np.arange(256)[:, None]), 3, axis=1)
        Lall = _rgb_linearizer(rgball, tr, tr_type=tr_type)
        plt.figure()
        for i in range(3):
            plt.plot(rgbcal[(p_pure[i], i)], L[(p_pure[i], i)] / L[(p_pure[i], i)].max(), colors[i] + 'o')
            plt.plot((rgball[:, i]), (Lall[:, i]), (colors[i] + linestyles[i]), label=(colors[i]))

        plt.xlabel('Display RGB')
        plt.ylabel('Linear RGB')
        plt.legend()
        plt.title('Tone response curves')
    rgblin = _rgb_linearizer(rgbcal, tr, tr_type=tr_type)
    M = np.linalg.lstsq(rgblin, xyz_fc, rcond=None)[0].T
    N = np.linalg.inv(M)
    p_grays = (rgbcal[:, 0] == rgbcal[:, 1]) & (rgbcal[:, 0] == rgbcal[:, 2])
    p_whites = (rgbcal[:, 0] == 2 ** nbit - 1) & (rgbcal[:, 1] == 2 ** nbit - 1) & (rgbcal[:, 2] == 2 ** nbit - 1)
    xyz_white = xyzcal[p_whites, :].mean(axis=0, keepdims=True)

    def optfcn(x, rgbcal, xyzcal, tr, xyz_black, cspace, p_grays, p_whites, out, verbosity):
        M = x.reshape((3, 3))
        xyzest = rgb_to_xyz(rgbcal, M, tr, xyz_black, tr_type)
        xyzw = xyzcal[p_whites, :].mean(axis=0)
        labcal, labest = colortf(xyzcal, tf=cspace, xyzw=xyzw), colortf(xyzest, tf=cspace, xyzw=xyzw)
        DEs = ((labcal - labest) ** 2).sum(axis=1) ** 0.5
        DEg = DEs[p_grays]
        DEw = DEs[p_whites]
        F = (avg(DEs) ** 2 + avg(DEg) ** 2 + avg(DEw ** 2)) ** 0.5
        if verbosity > 1:
            print('\nPerformance of TR + rgb-to-xyz conversion matrix M:')
            print('all: DE(jab): avg = {:1.4f}, std = {:1.4f}'.format(avg(DEs), np.std(DEs)))
            print('grays: DE(jab): avg = {:1.4f}, std = {:1.4f}'.format(avg(DEg), np.std(DEg)))
            print('whites(s) DE(jab): avg = {:1.4f}, std = {:1.4f}'.format(avg(DEw), np.std(DEw)))
        if out == 'F':
            return F
        else:
            return eval(out)

    x0 = M.ravel()
    res = math.minimizebnd(optfcn, x0, args=(rgbcal, xyzcal, tr, xyz_black, cspace, p_grays, p_whites, 'F', 0), use_bnd=False)
    xf = res['x_final']
    M = optfcn(xf, rgbcal, xyzcal, tr, xyz_black, cspace, p_grays, p_whites, 'M', verbosity)
    N = np.linalg.inv(M)
    return (M, N, tr, xyz_black, xyz_white)


def rgb_to_xyz(rgb, M, tr, xyz_black, tr_type='lut'):
    """
    Convert input rgb to xyz.
    
    Args:
        :rgb:
            | ndarray [Nx3] with RGB values 
        :M:
            | linear rgb to xyz conversion matrix
        :tr:
            | Tone Response function parameters or lut
        :xyz_black:
            | ndarray with XYZ tristimulus values of black
        :tr_type:
            | 'lut', optional
            | Type of Tone Response in tr input argument
            | options:
            |  - 'lut': Tone-Response as a look-up-table
            |  - 'gog': Tone-Response as a gain-offset-gamma function
            
    Returns:
        :xyz:
            | ndarray [Nx3] of XYZ tristimulus values
    """
    return np.dot(M, _rgb_linearizer(rgb, tr, tr_type=tr_type).T).T + xyz_black


def xyz_to_rgb(xyz, N, tr, xyz_black, tr_type='lut'):
    """
    Convert xyz to input rgb. 
    
    Args:
        :xyz:
            | ndarray [Nx3] with XYZ tristimulus values 
        :N:
            | xyz to linear rgb conversion matrix
        :tr:
            | Tone Response function parameters or lut
        :xyz_black:
            | ndarray with XYZ tristimulus values of black
        :tr_type:
            | 'lut', optional
            | Type of Tone Response in tr input argument
            | options:
            |  - 'lut': Tone-Response as a look-up-table
            |  - 'gog': Tone-Response as a gain-offset-gamma function
            
    Returns:
        :rgb:
            | ndarray [Nx3] of display RGB values
    """
    rgblin = _clamp0(np.dot(N, (xyz - xyz_black).T).T)
    return np.round(_rgb_delinearizer(rgblin, tr, tr_type=tr_type))


def _plot_target_vs_predicted_lab(labtarget, labpredicted, cspace='lab', verbosity=1):
    """ Make a plot of target vs predicted color coordinates """
    if verbosity > 0:
        xylabels = _CSPACE_AXES[cspace]
        laball = np.vstack((labtarget, labpredicted))
        ml, ma, mb = laball.min(axis=0)
        Ml, Ma, Mb = laball.max(axis=0)
        fml = 0.95 * ml
        fMl = 1.05 * Ml
        fma = 1.05 * ma if ma < 0 else 0.95 * ma
        fMa = 0.95 * Ma if Ma < 0 else 1.05 * Ma
        fmb = 1.05 * mb if mb < 0 else 0.95 * mb
        fMb = 0.95 * Mb if Mb < 0 else 1.05 * Mb
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))
        ax0.plot((labtarget[(Ellipsis, 1)]), (labtarget[(Ellipsis, 2)]), 'bo', label='target')
        ax0.plot((labpredicted[(Ellipsis, 1)]), (labpredicted[(Ellipsis, 2)]), 'ro', label='predicted')
        ax0.axis([fma, fMa, fmb, fMb])
        ax1.plot((labtarget[(Ellipsis, 1)]), (labtarget[(Ellipsis, 0)]), 'bo', label='target')
        ax1.plot((labpredicted[(Ellipsis, 1)]), (labpredicted[(Ellipsis, 0)]), 'ro', label='predicted')
        ax1.axis([fma, fMa, fml, fMl])
        ax2.plot((labtarget[(Ellipsis, 2)]), (labtarget[(Ellipsis, 0)]), 'bo', label='target')
        ax2.plot((labpredicted[(Ellipsis, 2)]), (labpredicted[(Ellipsis, 0)]), 'ro', label='predicted')
        ax2.axis([fmb, fMb, fml, fMl])
        ax0.set_xlabel(xylabels[1])
        ax0.set_ylabel(xylabels[2])
        ax1.set_xlabel(xylabels[1])
        ax1.set_ylabel(xylabels[0])
        ax2.set_xlabel(xylabels[2])
        ax2.set_ylabel(xylabels[0])
        ax2.legend(loc='upper left')


def _plot_DEs_vs_digital_values(DEslab, DEsl, DEsab, rgbcal, avg=lambda x: (x ** 2).mean() ** 0.5, nbit=8, verbosity=1):
    """ Make a plot of the lab, l and ab color differences for the different calibration stimulus types. """
    if verbosity > 0:
        p_pure = [
         (rgbcal[:, 1] == 0) & (rgbcal[:, 2] == 0),
         (rgbcal[:, 0] == 0) & (rgbcal[:, 2] == 0),
         (rgbcal[:, 0] == 0) & (rgbcal[:, 1] == 0)]
        p_grays = (rgbcal[:, 0] == rgbcal[:, 1]) & (rgbcal[:, 0] == rgbcal[:, 2])
        p_whites = (rgbcal[:, 0] == 2 ** nbit - 1) & (rgbcal[:, 1] == 2 ** nbit - 1) & (rgbcal[:, 2] == 2 ** nbit - 1)
        p_cyans = (rgbcal[:, 0] == 0) & (rgbcal[:, 1] != 0) & (rgbcal[:, 2] != 0)
        p_yellows = (rgbcal[:, 0] != 0) & (rgbcal[:, 1] != 0) & (rgbcal[:, 2] == 0)
        p_magentas = (rgbcal[:, 0] != 0) & (rgbcal[:, 1] == 0) & (rgbcal[:, 2] == 0)
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(15, 4))
        rgb_colors = 'rgb'
        rgb_labels = ['red', 'green', 'blue']
        marker = 'o'
        markersize = 10
        if p_whites.any():
            ax0.plot((rgbcal[(p_whites, 0)]), (DEslab[p_whites]), 'ks', markersize=markersize, label='white')
            ax1.plot((rgbcal[(p_whites, 0)]), (DEsl[p_whites]), 'ks', markersize=markersize, label='white')
            ax2.plot((rgbcal[(p_whites, 0)]), (DEsab[p_whites]), 'ks', markersize=markersize, label='white')
        if p_grays.any():
            ax0.plot((rgbcal[(p_grays, 0)]), (DEslab[p_grays]), color='gray', marker=marker, linestyle='none', label='gray')
            ax1.plot((rgbcal[(p_grays, 0)]), (DEsl[p_grays]), color='gray', marker=marker, linestyle='none', label='gray')
            ax2.plot((rgbcal[(p_grays, 0)]), (DEsab[p_grays]), color='gray', marker=marker, linestyle='none', label='gray')
        for i in range(3):
            if p_pure[i].any():
                ax0.plot((rgbcal[(p_pure[i], i)]), (DEslab[p_pure[i]]), (rgb_colors[i] + marker), label=(rgb_labels[i]))
                ax1.plot((rgbcal[(p_pure[i], i)]), (DEsl[p_pure[i]]), (rgb_colors[i] + marker), label=(rgb_labels[i]))
                ax2.plot((rgbcal[(p_pure[i], i)]), (DEsab[p_pure[i]]), (rgb_colors[i] + marker), label=(rgb_labels[i]))

        if p_cyans.any():
            ax0.plot((rgbcal[(p_cyans, 1)]), (DEslab[p_cyans]), ('c' + marker), label='cyan')
            ax1.plot((rgbcal[(p_cyans, 1)]), (DEsl[p_cyans]), ('c' + marker), label='cyan')
            ax2.plot((rgbcal[(p_cyans, 1)]), (DEsab[p_cyans]), ('c' + marker), label='cyan')
        if p_yellows.any():
            ax0.plot((rgbcal[(p_yellows, 0)]), (DEslab[p_yellows]), ('y' + marker), label='yellow')
            ax1.plot((rgbcal[(p_yellows, 0)]), (DEsl[p_yellows]), ('y' + marker), label='yellow')
            ax2.plot((rgbcal[(p_yellows, 0)]), (DEsab[p_yellows]), ('y' + marker), label='yellow')
        if p_magentas.any():
            ax0.plot((rgbcal[(p_magentas, 0)]), (DEslab[p_magentas]), ('m' + marker), label='magenta')
            ax1.plot((rgbcal[(p_magentas, 0)]), (DEsl[p_magentas]), ('m' + marker), label='magenta')
            ax2.plot((rgbcal[(p_magentas, 0)]), (DEsab[p_magentas]), ('m' + marker), label='magenta')
        ax0.plot((np.array([0, (2 ** nbit - 1) * 1.05])), (np.hstack((avg(DEslab), avg(DEslab)))), color='r', linewidth=2, linestyle='--')
        ax0.set_xlabel('digital values')
        ax0.set_ylabel('Color difference DElab')
        ax0.axis([0, (2 ** nbit - 1) * 1.05, 0, max(DEslab) * 1.1])
        ax0.set_title('DElab')
        ax1.plot((np.array([0, (2 ** nbit - 1) * 1.05])), (np.hstack((avg(DEsl), avg(DEsl)))), color='r', linewidth=2, linestyle='--')
        ax1.set_xlabel('digital values')
        ax1.set_ylabel('Color difference DEl')
        ax1.axis([0, (2 ** nbit - 1) * 1.05, 0, max(DEslab) * 1.1])
        ax1.set_title('DEl')
        ax2.plot((np.array([0, (2 ** nbit - 1) * 1.05])), (np.hstack((avg(DEsab), avg(DEsab)))), color='r', linewidth=2, linestyle='--')
        ax2.set_xlabel('digital values')
        ax2.set_ylabel('Color difference DEab')
        ax2.set_title('DEab')
        ax2.axis([0, (2 ** nbit - 1) * 1.05, 0, max(DEslab) * 1.1])
        ax2.legend(loc='upper left')


def calibration_performance(rgb, xyztarget, M, N, tr, xyz_black, xyz_white, tr_type='lut', cspace='lab', avg=lambda x: (x ** 2).mean() ** 0.5, rgb_is_xyz=False, is_verification_data=False, nbit=8, verbosity=1, sep=',', header=None):
    """
    Check calibration performance. Calculate DE for each stimulus. 
    
    Args:
        :rgb:
            | ndarray [Nx3] or string with filename of RGB values 
            | (or xyz values if argument rgb_to_xyz == True!)
        :xyztarget:
            | ndarray [Nx3] or string with filename of target XYZ values corresponding 
            | to the RGB settings (or the measured XYZ values, if argument rgb_to_xyz == True).
        :M:
            | linear rgb to xyz conversion matrix
        :N:
            | xyz to linear rgb conversion matrix
        :tr:
            | Tone Response function parameters or lut
        :xyz_black:
            | ndarray with XYZ tristimulus values of black
        :xyz_white:
            | ndarray with tristimlus values of white
        :tr_type:
            | 'lut', optional
            | options:
            |  - 'lut': Derive/specify Tone-Response as a look-up-table
            |  - 'gog': Derive/specify Tone-Response as a gain-offset-gamma function
        :cspace:
            | color space or chromaticity diagram to calculate color differences in.
        :avg:
            | lambda x: ((x**2).mean()**0.5), optional
            | Function used to average the color differences of the individual RGB settings
            | in the optimization of the xyz_to_rgb and rgb_to_xyz conversion matrices.
        :rgb_is_xyz:
            | False, optional
            | If True: the data in argument rgb are actually measured XYZ tristimulus values
            |           and are directly compared to the target xyz.
        :is_verification_data:
            | False, optional
            | If False: the data is assumed to be corresponding to RGB value settings used 
            |           in the calibration (i.e. containing whites, blacks, grays, pure and binary mixtures)
            | If True: no assumptions on content of rgb, so use this settings when
            |          checking the performance for a set of measured and target xyz data
            |          different than the ones used in the actual calibration measurements. 
        :nbit:
            | 8, optional
            | RGB values in nbit format (e.g. 8, 16, ...)
        :verbosity:
            | 1, optional
            | > 0: print and plot optimization results
        :sep:
            | ',', optional
            | separator in files with rgbcal and xyzcal data
        :header:
            | None, optional
            | header specifier for files with rgbcal and xyzcal data 
            | (see pandas.read_csv)
            
    Returns:
        :M:
            | linear rgb to xyz conversion matrix
        :N:
            | xyz to linear rgb conversion matrix
        :tr:
            | Tone Response function parameters or lut
        :xyz_black:
            | ndarray with XYZ tristimulus values of black
        :xyz_white:
            | ndarray with tristimlus values of white

    """
    rgb, xyz = _parse_rgbxyz_input(rgb, xyz=xyztarget, sep=sep, header=header)
    if rgb_is_xyz == False:
        xyzest = rgb_to_xyz(rgb, M, tr, xyz_black, tr_type=tr_type)
    else:
        xyzest = rgb
    lab, labest = colortf(xyz, tf=cspace, xyzw=xyz_white), colortf(xyzest, tf=cspace, xyzw=xyz_white)
    DElabi, DEli, DEabi = ((lab - labest) ** 2).sum(axis=1) ** 0.5, ((lab[:, :1] - labest[:, :1]) ** 2).sum(axis=1) ** 0.5, ((lab[:, 1:] - labest[:, 1:]) ** 2).sum(axis=1) ** 0.5
    if verbosity > 0:
        print('\nCalibration performance (all colors): \n    DE(l*a*b*): avg = {:1.2f}, std = {:1.2f}'.format(avg(DElabi), DElabi.std()))
        print('    DE(l*)    : avg = {:1.2f}, std = {:1.2f}'.format(avg(DEli), DEli.std()))
        print('    DE(a*b*)  : avg = {:1.2f}, std = {:1.2f}'.format(avg(DEabi), DEabi.std()))
    if is_verification_data == False:
        _plot_DEs_vs_digital_values(DElabi, DEli, DEabi, rgb, nbit=nbit, avg=avg, verbosity=verbosity)
    _plot_target_vs_predicted_lab(lab, labest, cspace=cspace, verbosity=verbosity)
    return (DElabi, DEli, DEabi)


class DisplayCalibration:
    __doc__ = "\n    Class for display_calibration.\n    \n    Args:\n        :rgbcal:\n            | ndarray [Nx3] or string with filename of RGB values \n            | rgcal must contain at least the following type of settings:\n            | - pure R,G,B: e.g. for pure R: (R != 0) & (G==0) & (B == 0)\n            | - white(s): R = G = B = 2**nbit-1\n            | - gray(s): R = G = B\n            | - black(s): R = G = B = 0\n            | - binary colors: cyan (G = B, R = 0), yellow (G = R, B = 0), magenta (R = B, G = 0)\n        :xyzcal:\n            | None, optional\n            | ndarray [Nx3] or string with filename of measured XYZ values for \n            | the RGB settings in rgbcal.\n            | if None: rgbcal is [Nx6] ndarray containing rgb (columns 0-2) and xyz data (columns 3-5)\n        :L_type:\n            | 'lms', optional\n            | Type of response to use in the derivation of the Tone-Response curves.\n            | options:\n            |  - 'lms': use cone fundamental responses: L vs R, M vs G and S vs B \n            |           (reduces noise and generally leads to more accurate characterization) \n            |  - 'Y': use the luminance signal: Y vs R, Y vs G, Y vs B\n        :tr_type:\n            | 'lut', optional\n            | options:\n            |  - 'lut': Derive/specify Tone-Response as a look-up-table\n            |  - 'gog': Derive/specify Tone-Response as a gain-offset-gamma function\n        :cieobs:\n            | '1931_2', optional\n            | CIE CMF set used to determine the XYZ tristimulus values\n            | (needed when L_type == 'lms': determines the conversion matrix to\n            | convert xyz to lms values)\n        :nbit:\n            | 8, optional\n            | RGB values in nbit format (e.g. 8, 16, ...)\n        :cspace:\n            | color space or chromaticity diagram to calculate color differences in\n            | when optimizing the xyz_to_rgb and rgb_to_xyz conversion matrices.\n        :avg:\n            | lambda x: ((x**2).mean()**0.5), optional\n            | Function used to average the color differences of the individual RGB settings\n            | in the optimization of the xyz_to_rgb and rgb_to_xyz conversion matrices.\n        :verbosity:\n            | 1, optional\n            | > 0: print and plot optimization results\n        :sep:\n            | ',', optional\n            | separator in files with rgbcal and xyzcal data\n        :header:\n            | None, optional\n            | header specifier for files with rgbcal and xyzcal data \n            | (see pandas.read_csv)\n\n    Return:\n        :calobject:\n            | attributes are: \n            |  - M: linear rgb to xyz conversion matrix\n            |  - N: xyz to linear rgb conversion matrix\n            |  - TR: Tone Response function parameters or lut\n            |  - xyz_black: ndarray with XYZ tristimulus values of black\n            |  - xyz_white: ndarray with tristimlus values of white\n            | as well as: \n            |  - rgbcal, xyzcal, cieobs, avg, tr_type, nbit, cspace, verbosity\n            |  - performance: dictionary with various color differences set to np.nan\n            |  -    (run calobject.performance() to fill it with actual values)\n    "

    def __init__(self, rgbcal, xyzcal=None, L_type='lms', cieobs='1931_2', tr_type='lut', nbit=8, cspace='lab', avg=lambda x: (x ** 2).mean() ** 0.5, verbosity=1, sep=',', header=None):
        rgbcal, xyzcal = _parse_rgbxyz_input(rgbcal, xyz=xyzcal, sep=sep, header=header)
        M, N, tr, xyz_black, xyz_white = calibrate(rgbcal, xyzcal=xyzcal, L_type=L_type, cieobs=cieobs,
          tr_type=tr_type,
          nbit=nbit,
          avg=avg,
          cspace=cspace,
          verbosity=verbosity,
          sep=sep,
          header=header)
        self.M = M
        self.N = N
        self.TR = tr
        self.xyz_black = xyz_black
        self.xyz_white = xyz_white
        self.rgbcal = rgbcal
        self.xyzcal = xyzcal
        self.cieobs = cieobs
        self.tr_type = tr_type
        self.nbit = nbit
        self.cspace = cspace
        self.avg = avg
        self.verbosity = verbosity
        self.performance = {'DElab_mean':np.nan,  'DElab_std':np.nan,  'DEli_mean':np.nan, 
         'DEl_std':np.nan,  'DEab_mean':np.nan, 
         'DEab_std':np.nan}

    def check_performance(self, rgb=None, xyz=None, verbosity=None, sep=',', header=None, rgb_is_xyz=False, is_verification_data=True):
        """
        Check calibration performance (if rgbcal is None: use calibration data).
        
        Args:
            :rgb:
                | None, optional
                | ndarray [Nx3] or string with filename of RGB values 
                | (or xyz values if argument rgb_to_xyz == True!)
                | If None: use self.rgbcal
            :xyz:
                | None, optional
                | ndarray [Nx3] or string with filename of target XYZ values corresponding 
                | to the RGB settings (or the measured XYZ values, if argument rgb_to_xyz == True).
                | If None: use self.xyzcal
            :verbosity:
                | None, optional
                | if None: use self.verbosity
                | if > 0: print and plot optimization results
            :sep:
                | ',', optional
                | separator in files with rgb and xyz data
            :header:
                | None, optional
                | header specifier for files with rgb and xyz data 
                | (see pandas.read_csv)
            :rgb_is_xyz:
                | False, optional
                | If True: the data in argument rgb are actually measured XYZ tristimulus values
                |           and are directly compared to the target xyz.
            :is_verification_data:
                | False, optional
                | If False: the data is assumed to be corresponding to RGB value settings used 
                |           in the calibration (i.e. containing whites, blacks, grays, pure and binary mixtures)
                |           Performance results are stored in self.performance.
                | If True: no assumptions on content of rgb, so use this settings when
                |          checking the performance for a set of measured and target xyz data
                |          different than the ones used in the actual calibration measurements. 
        
        Return:
            :performance: 
                | dictionary with various color differences.
        """
        if verbosity is None:
            verbosity = self.verbosity
        else:
            if rgb is None:
                rgb = self.rgbcal
                xyz = self.xyzcal
                is_verification_data = False
                rgb_is_xyz = False
            DElabi, DEli, DEabi = calibration_performance(rgb, xyz, (self.M), (self.N), (self.TR),
              (self.xyz_black), (self.xyz_white), cspace=(self.cspace),
              tr_type=(self.tr_type),
              avg=(self.avg),
              nbit=(self.nbit),
              verbosity=verbosity,
              sep=sep,
              header=header,
              rgb_is_xyz=rgb_is_xyz,
              is_verification_data=is_verification_data)
            performance = {'DElab_mean':DElabi.mean(),  'DElab_std':DElabi.std(),  'DEli_mean':DEli.mean(), 
             'DEl_std':DEli.std(),  'DEab_mean':DEabi.mean(), 
             'DEab_std':DEabi.std()}
            if is_verification_data == False:
                self.performance = performance
        return performance

    def to_xyz(self, rgb):
        """ Convert display rgb to xyz. """
        return rgb_to_xyz(rgb, (self.M), (self.TR), (self.xyz_black), tr_type=(self.tr_type))

    def to_rgb(self, xyz):
        """ Convert xyz to display rgb. """
        return xyz_to_rgb(xyz, (self.N), (self.TR), (self.xyz_black), tr_type=(self.tr_type))


if __name__ == '__main__':
    cieobs = '1931_2'
    tr_type = 'lut'
    L_type = 'lms'
    avg = np.mean
    cspace = 'lab'
    xyzcal = pd.read_csv((_PATH_DATA + 'XYZcal.csv'), sep=',', header=None).values
    rgbcal = pd.read_csv((_PATH_DATA + 'RGBcal.csv'), sep=',', header=None).values
    print('\nFunctional example:')
    M, N, tr, xyz_black, xyz_white = calibrate(rgbcal, xyzcal, L_type=L_type, tr_type=tr_type, avg=avg, cspace=cspace)
    if tr_type == 'gog':
        print('Calibration parameters :\nTR(gamma,offset,gain)=\n', np.round(tr, 5), '\nM=\n', np.round(M, 5), '\nN=\n', np.round(N, 5))
    DElabi, DEli, DEabi = calibration_performance(rgbcal, xyzcal, M, N, tr, xyz_black, xyz_white, cspace=cspace,
      tr_type=tr_type,
      avg=avg,
      verbosity=1,
      is_verification_data=False)
    xyz_test = np.array([[100.0, 100.0, 100.0]]) * 0.5
    print('\nTest calibration for user defined xyz:\n    xyz_test_est:', xyz_test)
    rgb_test_est = xyz_to_rgb(xyz_test, N, tr, xyz_black, tr_type=tr_type)
    print('    rgb_test_est:', rgb_test_est)
    xyz_test_est = rgb_to_xyz(rgb_test_est, M, tr, xyz_black, tr_type=tr_type)
    print('    xyz_test_est:', np.round(xyz_test_est, 1))
    xyz_verification = rgb_to_xyz(rgbcal, M, tr, xyz_black, tr_type=tr_type)
    xyz_target = xyzcal
    DElabi, DEli, DEabi = calibration_performance(xyz_verification, xyz_target, M, N, tr, xyz_black, xyz_white, cspace=cspace,
      tr_type=tr_type,
      avg=avg,
      verbosity=1,
      rgb_is_xyz=True,
      is_verification_data=True)
    print('\nClass  DisplayCalibration example:')
    cal1 = DisplayCalibration(rgbcal, xyzcal=xyzcal, L_type=L_type, cieobs=cieobs, tr_type=tr_type,
      avg=avg,
      cspace=cspace,
      verbosity=0)
    cal1 = DisplayCalibration((_PATH_DATA + 'RGBcal.csv'), xyzcal=(_PATH_DATA + 'XYZcal.csv'), L_type=L_type, cieobs=cieobs, tr_type=tr_type,
      avg=avg,
      cspace=cspace,
      verbosity=1,
      sep=',')
    cal1.check_performance()
    xyz_test = np.array([[100.0, 100.0, 100.0]]) * 0.5
    print('\nTest calibration for user defined xyz:\n    xyz_test_est:', xyz_test)
    rgb_test_est = cal1.to_xyz(rgb_test_est)
    print('    rgb_test_est:', rgb_test_est)
    xyz_test_est = cal1.to_xyz(rgb_test_est)
    print('    xyz_test_est:', np.round(xyz_test_est, 1))
    xyz_verification = cal1.to_xyz(rgbcal)
    xyz_target = xyzcal
    cal1.check_performance(xyz_verification, xyz_target, rgb_is_xyz=True,
      is_verification_data=True)