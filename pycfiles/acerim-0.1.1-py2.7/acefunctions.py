# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\acerim\acefunctions.py
# Compiled at: 2017-09-26 00:44:01
"""
This file contains several functions used in the ACERIM workflow.

For usage, see sample/tutorial.rst.
"""
from __future__ import division, print_function, absolute_import
import numpy as np, scipy as sp, pandas as pd, scipy.optimize as opt, matplotlib.pyplot as plt
from acerim import acestats as acs

def ejecta_profile_stats(cdf, ads, ejrad=2, rspacing=0.25, stats=None, plot_roi=False, vmin=None, vmax=None, strict=False, plot_stats=False, savepath=None, timer=False, dt=60):
    """Compute stat profiles across ejecta blankets by computing stats in a
    series of concentric rings beginning at the crater rim and extending to
    ejrad crater radii from the crater centre. Each ring is rspacing thick and
    the crater floor is excluded. Output is a dictionary of cdf.index values to
    pandas.DataFrame of stats containing the computed stats as columns and
    ring radius as rows.

    Parameters
    ----------

    Returns
    -------
    stat_df : dict of (index: pandas.DataFrame)
        Dictionary of stats with cdf index as keys and pandas.DataFrame of
        statistics as values (see example).

    Example
    -------
    >>> compute_ejecta_profile_stats(my_cdf, my_ads, 2, 0.25, stats=['mean',
                                    'median','maximum'],savepath='/tmp/')

    /tmp/index1_ejecta_stats.csv
        radius,mean,median,maximum
        1,     55,  45,    70
        1.25,  50,  40,    65
        1.5,   35,  35,    45
        1.75,  30,  33,    42

    """
    if timer:
        from timeit import default_timer as timer
        Tstart, Tnow = timer(), timer()
        count = 1
    if savepath:
        import os.path as p
        savename = p.join(savepath, '{}_ejpstats.csv')
    if stats is None:
        stats = acs._listStats()
    stat_dict = {}
    for ind in cdf.index:
        lat = cdf.loc[(ind, cdf.latcol)]
        lon = cdf.loc[(ind, cdf.loncol)]
        rad = cdf.loc[(ind, cdf.radcol)]
        try:
            roi, extent = ads.get_roi(lat, lon, rad, ejrad, get_extent=True)
            ring_array = np.arange(1, ejrad + rspacing, rspacing)
            ring_darray = ring_array * rad
            stat_df = pd.DataFrame(index=ring_array[:-1], columns=stats)
            for i in range(len(ring_array) - 1):
                rad_inner = ring_darray[i]
                rad_outer = ring_darray[(i + 1)]
                mask = crater_ring_mask(ads, roi, lat, lon, rad_inner, rad_outer)
                roi_masked = mask_where(roi, ~mask)
                filtered_roi = filter_roi(roi_masked, vmin, vmax, strict)
                roi_notnan = filtered_roi[(~np.isnan(filtered_roi))]
                for stat, function in acs._getFunctions(stats):
                    stat_df.loc[(ring_array[i], stat)] = function(roi_notnan)

                if plot_roi:
                    ads.plot_roi(filtered_roi, extent=extent)

            stat_dict[ind] = stat_df
            if plot_stats:
                plot_ejecta_stats(stat_df)
            if savepath:
                stat_df.to_csv(savename.format(ind))
        except ImportError as e:
            print(e, '. Skipping....')

        if timer:
            if timer() - Tnow > dt or count == len(cdf):
                update = ('Finished crater {} out of {}').format(count, len(cdf))
                elapsed = timer() - Tstart
                update += ('\n  Time elapsed:                           {}h:{}m:{}s').format(int(elapsed // 3600), int(elapsed % 3600 // 60), round(elapsed % 3600 % 60, 2))
                print(update)
                Tnow = timer()
            count += 1

    return stat_dict


def ejecta_stats(cdf, ads, ejrad=2, stats=None, plot=False, vmin=None, vmax=None, strict=False):
    """Compute the specified stats from acestats.py on a circular ejecta ROI
    extending ejsize crater radii from the crater center. Return results as
    CraterDataFrame with stats appended as extra columns.

    Parameters
    ----------
    cdf : CraterDataFrame object
        Contains the crater locations and sizes to locate ROIs in aceDS. Also
        form the basis of the returned CraterDataFrame
    ads : AceDataset object
        AceDataset of image data used to compute stats.
    ejrad : int, float
        The radius of ejecta blanket measured in crater radii from the
        crater center to the ejecta extent.
    stats : Array-like of str
        Indicates the stat names to compute. Stat functions must be defined in
        acestats.py. Default: all stats in acestats.py.
    plot : bool
        Plot the ejecta ROI.
    vmin : int, float
        The minimum valid image pixel value. Filter all values lower.
    vmax : int, float
        The maximum valid image pixel value. Filter all values higher.
    strict : bool
        How strict the (vmin, vmax) range is. If true, exclude values <= vmin
        and values >= vmax, if they are specified.

    Returns
    -------
    CraterDataFrame
        Same length as cdf with stats included as new columns.
    """
    if stats is None:
        stats = acs._listStats()
    ret_cdf = cdf
    for stat in stats:
        ret_cdf.loc[:, stat] = ret_cdf.index

    for i in cdf.index:
        lat = cdf.loc[(i, cdf.latcol)]
        lon = cdf.loc[(i, cdf.loncol)]
        rad = cdf.loc[(i, cdf.radcol)]
        roi, extent = ads.get_roi(lat, lon, rad, ejrad, get_extent=True)
        mask = crater_ring_mask(ads, roi, lat, lon, rad, rad * ejrad)
        roi_masked = mask_where(roi, ~mask)
        filtered_roi = filter_roi(roi_masked, vmin, vmax, strict)
        roi_notnan = filtered_roi[(~np.isnan(filtered_roi))]
        for stat, function in acs._getFunctions(stats):
            ret_cdf.loc[(i, stat)] = function(roi_notnan)

        if plot:
            ads.plot_roi(filtered_roi, extent=extent)

    return ret_cdf


def plot_roi(ads, roi, figsize=(8, 8), extent=None, title='ROI', vmin=None, vmax=None, cmap='gray', **kwargs):
    """Plot roi 2D array.

    If extent, cname and cdiam are supplied, the axes will display the
    lats and lons specified and title will inclue cname and cdiam.

    Parameters
    ----------
    ads : AceDataset object
        The parent dataset of roi.
    roi : 2D array
        The roi from ads to plot.
    figsize : tuple
        The (length,width) of plot in inches.
    extent : array-like
        The [minlon, maxlon, minlat, maxlat] extents of the roi in degrees.
    title : str
        Title of the roi.
    vmin : int, float
        Minimum pixel data value for plotting.
    vmax : int, float
        Maximum pixel data value for plotting.
    cmap : str
        Color map name for plotting. Must be a valid colorbar in
        matplotlib.cm.cmap_d. See help(matplotlib.cm) for full list.

    Other parameters
    ----------------
    **kwargs : object
        Additional keyword arguments to be passed to the imshow function. See
        help(matplotlib.pyplot.imshow) for more info.
    """
    plt.figure('ROI', figsize=figsize)
    plt.imshow(roi, extent=extent, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)
    plt.title(title)
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Latitude (degrees)')
    plt.show()


def plot_ejecta_stats():
    """Plot ejecta statistics.
    """
    pass


def plot_ejecta_profile_stats():
    """Plot ejecta profile statistics.
    """
    pass


def filter_roi(roi, vmin=None, vmax=None, strict=False):
    """
    Filter values outside (vmin, vmax) by setting them to np.nan. If strict,
    keep only values strictly less than vmax and strictly greater than vmin.

    E.g. strict=False keeps vmin <= roi <= vmax
         strict=True keeps vmin < roi < vmax
    """
    if vmin is None:
        vmin = -np.inf
    if vmax is None:
        vmax = np.inf
    nanmask = ~np.isnan(roi)
    if not strict:
        nanmask[nanmask] &= roi[nanmask] > vmax
        nanmask[nanmask] &= roi[nanmask] < vmin
    else:
        nanmask[nanmask] &= roi[nanmask] >= vmax
        nanmask[nanmask] &= roi[nanmask] <= vmin
    roi[nanmask] = np.nan
    return roi


def mask_where(ndarray, condition):
    """
    Return copy of ndarray with nan entries where condition is True.

    >>> arr = np.array([1.,2.,3.,4.,5.])
    >>> masked = mask_where(arr, arr > 3)
    >>> np.isnan(masked[3:]).all()
    True
    """
    mask = np.array(np.ones(ndarray.shape))
    mask[np.where(condition)] = np.nan
    return ndarray * mask


def circle_mask(roi, radius, center=(None, None)):
    """
    Return boolean array of True inside circle of radius at center.

    >>> roi = np.ones((3,3))
    >>> masked = circle_mask(roi, 1)
    >>> masked[1,1]
    True
    >>> masked[0,0]
    False
    """
    if not center[0]:
        center = np.array(roi.shape) / 2 - 0.5
    cx, cy = center
    width, height = roi.shape
    x = np.arange(width) - cx
    y = np.arange(height).reshape(-1, 1) - cy
    if radius > 0:
        return x * x + y * y <= radius * radius
    else:
        return np.zeros(roi.shape, dtype=bool)


def ellipse_mask(roi, a, b, center=(None, None)):
    """
    Return boolean array of True inside ellipse with horizontal major axis a
    and vertical minor axis b centered at center.

    >>> roi = np.ones((9,9))
    >>> masked = ellipse_mask(roi, 3, 2)
    >>> masked[4,1]
    True
    >>> masked[4,0]
    False
    """
    if not center[0]:
        center = np.array(roi.shape) / 2 - 0.5
    cx, cy = center
    width, height = roi.shape
    y, x = np.ogrid[-cx:width - cx, -cy:height - cy]
    return x * x / (a * a) + y * y / (b * b) <= 1


def ring_mask(roi, rmin, rmax, center=(None, None)):
    """
    Return boolean array of True in a ring from rmin to rmax radius around
    center. Returned array is same shape as roi.
    """
    inner = circle_mask(roi, rmin, center)
    outer = circle_mask(roi, rmax, center)
    return outer * ~inner


def crater_floor_mask(aceds, roi, lat, lon, rad):
    """
    Mask the floor of the crater lat, lon, with radius rad.
    """
    pixwidth = m2pix(rad, aceds.calc_mpp(lat))
    pixheight = m2pix(rad, aceds.calc_mpp())
    return ellipse_mask(roi, pixwidth, pixheight)


def crater_ring_mask(aceds, roi, lat, lon, rmin, rmax):
    """
    Mask a ring around a crater with inner radius rmin and outer radius rmax
    crater radii.
    """
    rmax_pixheight = m2pix(rmax, aceds.calc_mpp())
    rmax_pixwidth = m2pix(rmax, aceds.calc_mpp(lat))
    rmin_pixheight = m2pix(rmin, aceds.calc_mpp())
    rmin_pixwidth = m2pix(rmin, aceds.calc_mpp(lat))
    outer = ellipse_mask(roi, rmax_pixwidth, rmax_pixheight)
    inner = ellipse_mask(roi, rmin_pixwidth, rmin_pixheight)
    return outer * ~inner


def inbounds(lat, lon, mode='std'):
    """True if lat and lon within global coordinates.
    Standard: mode='std' for lat in (-90, 90) and lon in (-180, 180).
    Positive: mode='pos' for lat in (0, 180) and lon in (0, 360)

    >>> lat = -10
    >>> lon = -10
    >>> inbounds(lat, lon)
    True
    >>> inbounds(lat, lon, 'pos')
    False
    """
    if mode == 'std':
        return -90 <= lat <= 90 and -180 <= lon <= 180
    if mode == 'pos':
        return 0 <= lat <= 180 and 0 <= lon <= 360


def m2deg(dist, mpp, ppd):
    """Return dist converted from meters to degrees."""
    return dist / (mpp * ppd)


def m2pix(dist, mpp):
    """Return dist converted from meters to pixels"""
    return int(dist / mpp)


def deg2pix(dist, ppd):
    """Return dist converted from degrees to pixels."""
    return int(dist * ppd)


def get_ind(value, array):
    """Return closest index (rounded down) of a value from sorted array."""
    ind = np.abs(array - value).argmin()
    return int(ind)


def deg2rad(theta):
    """
    Convert degrees to radians.

    >>> deg2rad(180)
    3.141592653589793
    """
    return theta * (np.pi / 180)


def greatcircdist(lat1, lon1, lat2, lon2, radius):
    """
    Return great circle distance between two points on a spherical body.
    Uses Haversine formula for great circle distances.

    >>> greatcircdist(36.12, -86.67, 33.94, -118.40, 6372.8)
    2887.259950607111
    """
    if abs(lat1) >= 90 or abs(lat2) >= 90 or not all(map(inbounds, (
     lat1, lon1), (
     lat2, lon2))):
        raise ValueError('Latitude or longitude out of bounds.')
    lat1, lon1, lat2, lon2 = map(deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    theta = 2 * np.arcsin(np.sqrt(a))
    dist = radius * theta
    return dist


def histogram(roi, bins, hmin=None, hmax=None, skew=False, verbose=False, *args, **kwargs):
    """
    Return histogram, bins of histogram computed on ROI. See np.histogram for
    full usage and optional parameters. Set verbose=True to print a summary of
    the statistics.
    """
    roi_notnan = roi[(~np.isnan(roi))]
    roi_valid = roi_notnan[(hmin <= roi_notnan <= hmax)]
    hist, bins = np.histogram(roi, bins=bins, hmin=hmin, hmax=hmax, *args, **kwargs)
    ret = [hist, bins]
    output = ('Histogram with {} pixels total,               {} pixels in [hmin, hmax] inclusive,               {} nan pixels excluded,               {} bins').format(len(roi), len(roi_valid), len(roi_notnan), len(bins))
    if skew:
        skewness = sp.stats.skew(hist)
        ret.append(skewness)
        output += (', {} skewness').format(skewness)
    if verbose:
        print(output)
    return ret


def fit_exp(x, y, PLOT_EXP=False):
    """
    Return an exponential that has been fit to data using scipy.curvefit().
    If plot is True, plot the data and the fit.
    """

    def exp_eval(x, a, b, c):
        """
        Return exponential of x with a,b,c parameters.
        """
        return a * np.exp(-b * x) + c

    def plot_exp(x, y, exp):
        pass

    try:
        p_opt, cov = opt.curve_fit(exp_eval, x, y)
    except:
        RuntimeError
        return

    if PLOT_EXP:
        plot_exp(x, y, exp_eval(x, *p_opt))
    return p_opt


def fit_gauss(data, PLOT_GAUSS=False):
    """
    Return parameters of a Gaussian that has been fit to data using least
    squares fitting. If plot=True, plot the histogram and fit of the data.
    """

    def gauss(x, p):
        """
        Return Gaussian with mean = p[0], standard deviation = p[1].
        """
        return 1.0 / (p[1] * np.sqrt(2 * np.pi)) * np.exp(-(x - p[0]) ** 2 / (2 * p[1] ** 2))

    def errorfn(p, x, y):
        """Compute distance from gaussian to y."""
        gauss(x, p) - y

    def plot_gauss(bins, n, gauss):
        pass

    data = data[(data > 0)]
    n, bins = np.histogram(data, bins='fd', density=True)
    p0 = [0, 1]
    p, success = opt.leastsq(errorfn, p0[:], args=(bins[:-1], n))
    if PLOT_GAUSS:
        plot_gauss(bins, n, gauss(bins, p))
    return p


def fit_pow(xdata, ydata, p0, plot=False, cid=''):
    """
    Return a power law curve fit of y using a least squares fit.
    """

    def residuals(p, x, y):
        return ydata - pow_eval(p, x)

    def pow_eval(p, x):
        return p[0] + p[1] * x ** p[2]

    pfinal, success = opt.leastsq(residuals, p0, args=(xdata, ydata))
    xarr = np.arange(xdata[0], xdata[(-1)], 0.1)
    return (xarr, pow_eval(pfinal, xarr))


def fit_pow_linear(xdata, ydata, p0, plot=False, cid=''):
    """
    Return a power law curve fit of y by converting to linear data using
    logarithms and then performing a linear least squares fit.
    """

    def fit_line(p, x):
        return p[0] + p[1] * x

    def residuals(p, x, y):
        return ydata - fit_line(p, x)

    def pow_eval(x, amp, index):
        return amp * x ** index

    logx = np.log(xdata)
    logy = np.log(ydata)
    pfinal, success = opt.leastsq(residuals, p0, args=(logx, logy))
    return pow_eval(xdata, pfinal[0], pfinal[1])