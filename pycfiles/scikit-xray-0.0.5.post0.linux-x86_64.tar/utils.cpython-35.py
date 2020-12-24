# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/utils.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 38748 bytes
"""
This module is for the 'core' data types.
"""
from __future__ import absolute_import, division, print_function
import six
from six.moves import zip
from six import string_types
import time, sys
from collections import namedtuple, MutableMapping, defaultdict, deque
import numpy as np
from itertools import tee
import logging
logger = logging.getLogger(__name__)
try:
    import src.ctrans as ctrans
except ImportError:
    try:
        import ctrans
    except ImportError:
        ctrans = None

md_value = namedtuple('md_value', ['value', 'units'])
_defaults = {'bins': 100, 
 'nx': 100, 
 'ny': 100, 
 'nz': 100}

class NotInstalledError(ImportError):
    __doc__ = '\n    Custom exception that should be subclassed to handle\n    specific missing libraries\n\n    '


class MD_dict(MutableMapping):
    __doc__ = "\n    A class to make dealing with the meta-data scheme for DataExchange easier\n\n    Examples\n    --------\n    Getting and setting data by path is possible\n\n    >>> tt = MD_dict()\n    >>> tt['name'] = 'test'\n    >>> tt['nested.a'] = 2\n    >>> tt['nested.b'] = (5, 'm')\n    >>> tt['nested.a'].value\n    2\n    >>> tt['nested.a'].units is None\n    True\n    >>> tt['name'].value\n    'test'\n    >>> tt['nested.b'].units\n    'm'\n    "

    def __init__(self, md_dict=None):
        if md_dict is None:
            md_dict = dict()
        self._dict = md_dict
        self._split = '.'

    def __repr__(self):
        return self._dict.__repr__()

    def __setitem__(self, key, val):
        key_split = key.split(self._split)
        tmp = self._dict
        for k in key_split[:-1]:
            try:
                tmp = tmp[k]._dict
            except:
                tmp[k] = type(self)()
                tmp = tmp[k]._dict

            if isinstance(tmp, md_value):
                raise KeyError('trying to use a leaf node as a branch')

        if isinstance(val, md_value):
            tmp[key_split[(-1)]] = val
            return
        if isinstance(val, string_types):
            tmp[key_split[(-1)]] = md_value(val, 'text')
            return
        try:
            if isinstance(val[1], string_types) or val[1] is None:
                print('here')
                tmp[key_split[(-1)]] = md_value(*val)
            else:
                tmp[key_split[(-1)]] = md_value(val, None)
        except TypeError:
            tmp[key_split[(-1)]] = md_value(val, None)

    def __getitem__(self, key):
        key_split = key.split(self._split)
        tmp = self._dict
        for k in key_split[:-1]:
            try:
                tmp = tmp[k]._dict
            except:
                tmp[k] = type(self)()
                tmp = tmp[k]._dict

            if isinstance(tmp, md_value):
                raise KeyError('trying to use a leaf node as a branch')

        return tmp.get(key_split[(-1)], None)

    def __delitem__(self, key):
        key_split = key.split(self._split)
        tmp = self._dict
        for k in key_split[:-1]:
            tmp = tmp[k]._dict

        del tmp[key_split[(-1)]]

    def __len__(self):
        return len(list(iter(self)))

    def __iter__(self):
        return _iter_helper([], self._split, self._dict)


def _iter_helper(path_list, split, md_dict):
    """
    Recursively walk the tree and return the names of the leaves
    """
    for k, v in six.iteritems(md_dict):
        if isinstance(v, md_value):
            yield split.join(path_list + [k])
        else:
            for inner_v in _iter_helper(path_list + [k], split, v._dict):
                yield inner_v


class verbosedict(dict):
    __doc__ = '\n    A sub-class of dict which raises more verbose errors if\n    a key is not found.\n    '

    def __getitem__(self, key):
        try:
            v = dict.__getitem__(self, key)
        except KeyError:
            if len(self) < 25:
                new_msg = "You tried to access the key '{key}' which does not exist.  The extant keys are: {valid_keys}".format(key=key, valid_keys=list(self))
            else:
                new_msg = "You tried to access the key '{key}' which does not exist.  There are {num} extant keys, which is too many to show you".format(key=key, num=len(self))
            six.reraise(KeyError, KeyError(new_msg), sys.exc_info()[2])

        return v


class RCParamDict(MutableMapping):
    __doc__ = "A class to make dealing with storing default values easier.\n\n    RC params is a hold- over from the UNIX days where configuration\n    files are 'rc' files.  See\n    http://en.wikipedia.org/wiki/Configuration_file\n\n    Examples\n    --------\n    Getting and setting data by path is possible\n\n    >>> tt = RCParamDict()\n    >>> tt['name'] = 'test'\n    >>> tt['nested.a'] = 2\n    "
    _delim = '.'

    def __init__(self):
        self._dict = dict()
        self._validators = defaultdict(lambda : lambda x: True)

    def __setitem__(self, key, val):
        splt_key = key.split(self._delim, 1)
        if len(splt_key) > 1:
            try:
                tmp = self._dict[splt_key[0]]
            except KeyError:
                tmp = RCParamDict()
                self._dict[splt_key[0]] = tmp

            if not isinstance(tmp, RCParamDict):
                raise KeyError('name space is borked')
            tmp[splt_key[1]] = val
        else:
            if not self._validators[key]:
                raise ValueError('fails to validate, improve this')
            self._dict[key] = val

    def __getitem__(self, key):
        splt_key = key.split(self._delim, 1)
        if len(splt_key) > 1:
            return self._dict[splt_key[0]][splt_key[1]]
        else:
            return self._dict[key]

    def __delitem__(self, key):
        splt_key = key.split(self._delim, 1)
        if len(splt_key) > 1:
            self._dict[splt_key[0]].__delitem__(splt_key[1])
        else:
            del self._dict[key]

    def __len__(self):
        return len(list(iter(self)))

    def __iter__(self):
        return self._iter_helper([])

    def _iter_helper(self, path_list):
        """
        Recursively walk the tree and return the names of the leaves
        """
        for key, val in six.iteritems(self._dict):
            if isinstance(val, RCParamDict):
                for k in val._iter_helper(path_list + [key]):
                    yield k

            else:
                yield self._delim.join(path_list + [key])

    def __repr__(self):
        str_list = self._repr_helper(0)
        return '\n'.join(str_list)

    def _repr_helper(self, tab_level):
        str_list = []
        elm_list = []
        nested_list = []
        for key, val in six.iteritems(self._dict):
            if isinstance(val, RCParamDict):
                nested_list.append(key)
            else:
                elm_list.append(key)

        elm_list.sort()
        nested_list.sort()
        for elm in elm_list:
            str_list.append('    ' * tab_level + '{key}: {val}'.format(key=elm, val=self._dict[elm]))

        for nested in nested_list:
            str_list.append('    ' * tab_level + '{key}:'.format(key=nested))
            str_list.extend(self._dict[nested]._repr_helper(tab_level + 1))

        return str_list


keys_core = {'pixel_size': {'description': '2 element tuple defining the (x y) dimensions of the pixel', 
                'type': tuple, 
                'units': 'um'}, 
 
 'voxel_size': {'description': '3 element tuple defining the (x y z) dimensions of the voxel', 
                'type': tuple, 
                'units': 'um'}, 
 
 'calibrated_center': {'description': '2 element tuple defining the (x y) center of the detector in pixels', 
                       'type': tuple, 
                       'units': 'pixel'}, 
 
 'detector_size': {'description': '2 element tuple defining no. of pixels(size) in the detector X and Y direction', 
                   'type': tuple, 
                   'units': 'pixel'}, 
 
 'detector_tilt_angles': {'description': 'Detector tilt angle', 
                          'type': tuple, 
                          'units': ' degrees'}, 
 
 'dist_sample': {'description': 'distance from the sample to the detector (mm)', 
                 'type': float, 
                 'units': 'mm'}, 
 
 'wavelength': {'description': 'wavelength of incident radiation (Angstroms)', 
                'type': float, 
                'units': 'angstrom'}, 
 
 'ub_mat': {'description': 'UB matrix(orientation matrix) 3x3 array', 
            'type': 'ndarray'}, 
 
 'energy': {'description': 'scanning energy for data collection', 
            'type': float, 
            'units': 'keV'}, 
 
 'array_dimensions': {'description': 'axial lengths of the array (Pixels)', 
                      'x_dimension': {'description': 'x-axis array length as int', 
                                      'type': int, 
                                      'units': 'pixels'}, 
                      
                      'y_dimension': {'description': 'y-axis array length as int', 
                                      'type': int, 
                                      'units': 'pixels'}, 
                      
                      'z_dimension': {'description': 'z-axis array length as int', 
                                      'type': int, 
                                      'units': 'pixels'}}, 
 
 'bounding_box': {'description': 'physical extents of the array: useful for ' + 'volume alignment, transformation, merge and ' + 'spatial comparison of multiple volumes', 
                  
                  'x_min': {'description': 'minimum spatial coordinate along the x-axis', 
                            'type': float, 
                            'units': 'um'}, 
                  
                  'x_max': {'description': 'maximum spatial coordinate along the x-axis', 
                            'type': float, 
                            'units': 'um'}, 
                  
                  'y_min': {'description': 'minimum spatial coordinate along the y-axis', 
                            'type': float, 
                            'units': 'um'}, 
                  
                  'y_max': {'description': 'maximum spatial coordinate along the y-axis', 
                            'type': float, 
                            'units': 'um'}, 
                  
                  'z_min': {'description': 'minimum spatial coordinate along the z-axis', 
                            'type': float, 
                            'units': 'um'}, 
                  
                  'z_max': {'description': 'maximum spatial coordinate along the z-axis', 
                            'type': float, 
                            'units': 'um'}}}

def subtract_reference_images(imgs, is_reference):
    """
    Function to subtract a series of measured images from
    background/dark current/reference images.  The nearest reference
    image in the reverse temporal direction is subtracted from each
    measured image.

    Parameters
    ----------
    imgs : numpy.ndarray
        Array of 2-D images

    is_reference : 1-D boolean array
        true  : image is reference image
        false : image is measured image

    Returns
    -------
    img_corr : numpy.ndarray
        len(img_corr) == len(img_arr) - len(is_reference_img == true)
        img_corr is the array of measured images minus the reference
        images.

    Raises
    ------
    ValueError
        Possible causes:
            is_reference contains no true values
            Raised when the first image in the array is not a reference image.

    """
    if not is_reference[0]:
        raise ValueError('The first image is not a reference image')
    ref_imge = imgs[0]
    ref_count = np.sum(is_reference)
    corrected_image = deque()
    for imgs, ref in zip(imgs[1:], is_reference[1:]):
        if ref:
            ref_imge = imgs
            continue
            corrected_image.append(imgs - ref_imge)

    return list(corrected_image)


def img_to_relative_xyi(img, cx, cy, pixel_size_x=None, pixel_size_y=None):
    """
    Convert the 2D image to a list of x y I coordinates where
    x == x_img - detector_center[0] and
    y == y_img - detector_center[1]

    Parameters
    ----------
    img: `ndarray`
        2D image
    cx : float
        Image center in the x direction
    cy : float
        Image center in the y direction
    pixel_size_x : float, optional
        Pixel size in x
    pixel_size_y : float, optional
        Pixel size in y
    **kwargs: dict
        Bucket for extra parameters in an unpacked dictionary

    Returns
    -------
    x : `ndarray`
        x-coordinate of pixel. shape (N, )
    y : `ndarray`
        y-coordinate of pixel. shape (N, )
    I : `ndarray`
        intensity of pixel. shape (N, )
    """
    if pixel_size_x is not None and pixel_size_y is not None:
        if pixel_size_x <= 0:
            raise ValueError('Input parameter pixel_size_x must be greater than 0. Your value was ' + six.text_type(pixel_size_x))
        if pixel_size_y <= 0:
            raise ValueError('Input parameter pixel_size_y must be greater than 0. Your value was ' + six.text_type(pixel_size_y))
    else:
        if pixel_size_x is None and pixel_size_y is None:
            pixel_size_x = 1
            pixel_size_y = 1
        else:
            raise ValueError('pixel_size_x and pixel_size_y must both be None or greater than zero. You passed in values for pixel_size_x of {0} and pixel_size_y of {1]'.format(pixel_size_x, pixel_size_y))
    x, y = np.meshgrid(pixel_size_x * (np.arange(img.shape[0]) - cx), pixel_size_y * (np.arange(img.shape[1]) - cy))
    return (
     x.ravel(), y.ravel(), img.ravel())


def bin_1D(x, y, nx=None, min_x=None, max_x=None):
    """
    Bin the values in y based on their x-coordinates

    Parameters
    ----------
    x : array
        position
    y : array
        intensity
    nx : integer, optional
        number of bins to use defaults to default bin value
    min_x : float, optional
        Left edge of first bin defaults to minimum value of x
    max_x : float, optional
        Right edge of last bin defaults to maximum value of x

    Returns
    -------
    edges : array
        edges of bins, length nx + 1

    val : array
        sum of values in each bin, length nx

    count : array
        The number of counts in each bin, length nx
    """
    if min_x is None:
        min_x = np.min(x)
    if max_x is None:
        max_x = np.max(x)
    if nx is None:
        nx = _defaults['bins']
    bins = np.linspace(start=min_x, stop=max_x, num=nx + 1, endpoint=True)
    val, _ = np.histogram(a=x, bins=bins, weights=y)
    count, _ = np.histogram(a=x, bins=bins)
    return (
     bins, val, count)


def radial_grid(center, shape, pixel_size=None):
    """Convert a cartesian grid (x,y) to the radius relative to some center

    Parameters
    ----------
    center : tuple
        point in image where r=0; may be a float giving subpixel precision.
        Order is (rr, cc).
    shape : tuple
        Image shape which is used to determine the maximum extent of output
        pixel coordinates.
        Order is (rr, cc).
    pixel_size : sequence, optional
        The physical size of the pixels.
        len(pixel_size) should be the same as len(shape)
        defaults to (1,1)

    Returns
    -------
    r : array
        The distance of each pixel from `center`
        Shape of the return value is equal to the `shape` input parameter
    """
    if pixel_size is None:
        pixel_size = (1, 1)
    X, Y = np.meshgrid(pixel_size[1] * (np.arange(shape[1]) - center[1]), pixel_size[0] * (np.arange(shape[0]) - center[0]))
    return np.sqrt(X * X + Y * Y)


def angle_grid(center, shape, pixel_size=None):
    r"""
    Make a grid of angular positions.

    Read note for our conventions here -- there be dragons!

    Parameters
    ----------
    center : tuple
        point in image where r=0; may be a float giving subpixel precision.
        Order is (rr, cc).

    shape: tuple
        Image shape which is used to determine the maximum extent of output
        pixel coordinates. Order is (rr, cc).

    Returns
    -------
    agrid : array
        angular position (in radians) of each array element in range [-pi, pi]

    Note
    ----
    :math:`\theta`, the counter-clockwise angle from the positive x axis
    :math:`\theta \el [-\pi, \pi]`.  In array indexing and the conventional
    axes for images (origin in upper left), positive y is downward.
    """
    if pixel_size is None:
        pixel_size = (1, 1)
    x, y = np.meshgrid(pixel_size[1] * (np.arange(shape[1]) - center[1]), pixel_size[0] * (np.arange(shape[0]) - center[0]))
    return np.arctan2(y, x)


def radius_to_twotheta(dist_sample, radius):
    r"""
    Converts radius from the calibrated center to scattering angle
    (2:math:`2\theta`) with known detector to sample distance.

    Parameters
    ----------
    dist_sample : float
        distance from the sample to the detector (mm)

    radius : array
        The L2 norm of the distance of each pixel from the calibrated center.

    Returns
    -------
    two_theta : array
        An array of :math:`2\theta` values
    """
    return np.arctan(radius / dist_sample)


def wedge_integration(src_data, center, theta_start, delta_theta, r_inner, delta_r):
    """
    Implementation of caking.

    Parameters
    ----------
    scr_data : ndarray
        The source-data to be integrated

    center : ndarray
        The center of the ring in pixels

    theta_start : float
        The angle of the start of the wedge from the
        image y-axis in degrees

    delta_theta : float
        The angular width of the wedge in degrees.  Positive
        angles go clockwise, negative go counter-clockwise.

    r_inner : float
        The inner radius in pixel units, Must be non-negative

    delta_r : float
        The length of the wedge in the radial direction
        in pixel units. Must be non-negative

    Returns
    -------
    float
        The integrated intensity under the wedge
    """
    raise NotImplementedError()


def bin_edges(range_min=None, range_max=None, nbins=None, step=None):
    """
    Generate bin edges.  The last value is the returned array is
    the right edge of the last bin, the rest of the values are the
    left edges of each bin.

    If `range_max` is specified all bin edges will be less than or
    equal to it's value.

    If `range_min` is specified all bin edges will be greater than
    or equal to it's value

    If `nbins` is specified then there will be than number of bins and
    the returned array will have length `nbins + 1` (as the right most
    edge is included)

    If `step` is specified then bin width is approximately `step` (It is
    not exact due to the nature of floats). The arrays generated by
    `np.cumsum(np.ones(nbins) * step)` and `np.arange(nbins) * step` are
    not identical.  This function uses the second method in all cases
    where `step` is specified.

    .. warning :: If the set :code:`(range_min, range_max, step)` is
        given there is no guarantee that :code:`range_max - range_min`
        is an integer multiple of :code:`step`.  In this case the left
        most bin edge is :code:`range_min` and the right most bin edge
        is less than :code:`range_max` and the distance between the
        right most edge and :code:`range_max` is not greater than
        :code:`step` (this is the same behavior as the built-in
        :code:`range()`).  It is not recommended to specify bins in this
        manner.

    Parameters
    ----------
    range_min : float, optional
        The minimum value that may be included as a bin edge

    range_max : float, optional
        The maximum value that may be included as a bin edge

    nbins : int, optional
        The number of bins, if specified the length of the returned
        value will be nbins + 1

    step : float, optional
        The step between the bins

    Returns
    -------
    edges : np.array
        An array of floats for the bin edges.  The last value is the
        right edge of the last bin.
    """
    num_valid_args = sum((range_min is not None, range_max is not None,
     step is not None, nbins is not None))
    if num_valid_args != 3:
        raise ValueError('Exactly three of the arguments must be non-None not {}.'.format(num_valid_args))
    if range_min is not None and range_max is not None and range_max <= range_min:
        raise ValueError('The minimum must be less than the maximum')
    if nbins is not None and nbins <= 0:
        raise ValueError('The number of bins must be positive')
    if step is None:
        return np.linspace(range_min, range_max, nbins + 1, endpoint=True)
    if nbins is None:
        if step > range_max - range_min:
            raise ValueError('The step can not be greater than the difference between min and max')
        nbins = int((range_max - range_min) // step)
        ret = range_min + np.arange(nbins + 1) * step
        if ret[(-1)] > range_max:
            return ret[:-1]
        if range_max - ret[(-1)] > 1e-10 * step:
            logger.debug('Inconsistent (range_min, range_max, step) and step does not evenly divide (range_min - range_max). The bins has been truncated.\nmin: %f max: %f step: %f gap: %f', range_min, range_max, step, range_max - ret[(-1)])
        return ret
    if range_max is None:
        return range_min + np.arange(nbins + 1) * step
    if range_min is None:
        return range_max - np.arange(nbins + 1)[::-1] * step


def grid3d(q, img_stack, nx=None, ny=None, nz=None, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None, binary_mask=None):
    """Grid irregularly spaced data points onto a regular grid via histogramming

    This function will process the set of reciprocal space values (q), the
    image stack (img_stack) and grid the image data based on the bounds
    provided, using defaults if none are provided.

    Parameters
    ----------
    q : ndarray
        (Qx, Qy, Qz) - HKL values - Nx3 array
    img_stack : ndarray
        Intensity array of the images
        dimensions are: [num_img][num_rows][num_cols]
    nx : int, optional
        Number of voxels along x
    ny : int, optional
        Number of voxels along y
    nz : int, optional
        Number of voxels along z
    xmin : float, optional
        Minimum value along x. Defaults to smallest x value in q
    ymin : float, optional
        Minimum value along y. Defaults to smallest y value in q
    zmin : float, optional
        Minimum value along z. Defaults to smallest z value in q
    xmax : float, optional
        Maximum value along x. Defaults to largest x value in q
    ymax : float, optional
        Maximum value along y. Defaults to largest y value in q
    zmax : float, optional
        Maximum value along z. Defaults to largest z value in q
    binary_mask : ndarray, optional
        The binary mask provides a mechanism to remove unwanted pixels
        from the images.
        Binary mask can be two different shapes.
        - 1: 2-D with binary_mask.shape == np.asarray(img_stack[0]).shape
        - 2: 3-D with binary_mask.shape == np.asarray(img_stack).shape

    Returns
    -------
    mean : ndarray
        intensity grid.  The values in this grid are the
        mean of the values that fill with in the grid.
    occupancy : ndarray
        The number of data points that fell in the grid.
    std_err : ndarray
        This is the standard error of the value in the
        grid box.
    oob : int
        Out Of Bounds. Number of data points that are outside of
        the gridded region.
    bounds : list
        tuple of (min, max, step) for x, y, z in order: [x_bounds,
        y_bounds, z_bounds]

    """
    img_stack = np.asarray(img_stack)
    if binary_mask is None or binary_mask.shape == img_stack.shape:
        pass
    else:
        if binary_mask.shape == img_stack[0].shape:
            binary_mask = np.tile(np.ravel(binary_mask), img_stack.shape[0])
        else:
            raise ValueError('The binary mask must be the same shape as theimg_stack ({0}) or a single image in the image stack ({1}).  The input binary mask is shaped ({2})'.format(img_stack.shape, img_stack[0].shape, binary_mask.shape))
        q = np.atleast_2d(q)
        if q.ndim != 2:
            raise ValueError('q.ndim must be a 2-D array of shape Nx3 array. You provided an array with {0} dimensions.'.format(q.ndim))
        if q.shape[1] != 3:
            raise ValueError('The shape of q must be an Nx3 array, not {0}X{1} which you provided.'.format(*q.shape))
        qmin = np.min(q, axis=0)
        qmax = np.max(q, axis=0)
        dqn = [_defaults['nx'], _defaults['ny'], _defaults['nz']]
        qmax += np.spacing(qmax)
        for target, input_vals in ((dqn, (nx, ny, nz)),
         (
          qmin, (xmin, ymin, zmin)),
         (
          qmax, (xmax, ymax, zmax))):
            for j, in_val in enumerate(input_vals):
                if in_val is not None:
                    target[j] = in_val

        bounds = np.array([qmin, qmax, dqn]).T
        q = np.insert(q, 3, np.ravel(img_stack), axis=1)
        if binary_mask is not None:
            q = q[np.ravel(binary_mask)]
        t1 = time.time()
        mean, occupancy, std_err, oob = ctrans.grid3d(q, qmin, qmax, dqn, norm=1)
        t2 = time.time()
        logger.info('Done processed in {0} seconds'.format(t2 - t1))
        empt_nb = (occupancy == 0).sum()
        if oob:
            logger.debug('There are %.2e points outside the grid {0}'.format(oob))
        logger.debug('There are %2e bins in the grid {0}'.format(mean.size))
    if empt_nb:
        logger.debug('There are %.2e values zero in the grid {0}'.format(empt_nb))
    return (mean, occupancy, std_err, oob, bounds)


def bin_edges_to_centers(input_edges):
    """
    Helper function for turning a array of bin edges into
    an array of bin centers

    Parameters
    ----------
    input_edges : array-like
        N + 1 values which are the left edges of N bins
        and the right edge of the last bin

    Returns
    -------
    centers : ndarray
        A length N array giving the centers of the bins
    """
    input_edges = np.asarray(input_edges)
    return (input_edges[:-1] + input_edges[1:]) * 0.5


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def q_to_d(q):
    r"""
    Helper function to convert :math:`d` to :math:`q`.  The point
    of this function is to prevent fat-fingered typos.

    By definition the relationship is:

    ..math ::

        q = \frac{2 \pi}{d}

    Parameters
    ----------
    q : array
        An array of q values

    Returns
    -------
    d : array
       An array of d (plane) spacing

    """
    return 2 * np.pi / np.asarray(q)


def d_to_q(d):
    r"""
    Helper function to convert :math:`d` to :math:`q`.
    The point of this function is to prevent fat-fingered typos.

    By definition the relationship is:

    ..math ::

        d = \frac{2 \pi}{q}

    Parameters
    ----------
    d : array
       An array of d (plane) spacing

    Returns
    -------
    q : array
        An array of q values

    """
    return 2 * np.pi / np.asarray(d)


def q_to_twotheta(q, wavelength):
    r"""
    Helper function to convert :math:`q` + :math:`\lambda` to :math:`2\theta`.
    The point of this function is to prevent fat-fingered typos.

    By definition the relationship is:

    ..math ::

        \sin\left(\frac{2\theta}{2}
ight) = \frac{\lambda q}{4 \pi}

    thus

    ..math ::

        2\theta_n = 2 \arcsin\left(\frac{\lambda q}{4 \pi}\right

    Parameters
    ----------
    q : array
        An array of :math:`q` values

    wavelength : float
        Wavelength of the incoming x-rays

    Returns
    -------
    two_theta : array
        An array of :math:`2\theta` values

    """
    q = np.asarray(q)
    wavelength = float(wavelength)
    pre_factor = wavelength / (4 * np.pi)
    return 2 * np.arcsin(q * pre_factor)


def twotheta_to_q(two_theta, wavelength):
    r"""
    Helper function to convert :math:`2\theta` + :math:`\lambda` to :math:`q`.
    The point of this function is to prevent fat-fingered typos.

    By definition the relationship is:

    ..math ::

        \sin\left(\frac{2\theta}{2}
ight) = \frac{\lambda q}{4 \pi}

    thus

    ..math ::

        q = \frac{4 \pi \sin\left(\frac{2\theta}{2}
ight)}{\lambda}

    Parameters
    ----------
    two_theta : array
        An array of :math:`2\theta` values

    wavelength : float
        Wavelength of the incoming x-rays

    Returns
    -------
    q : array
        An array of :math:`q` values
    """
    two_theta = np.asarray(two_theta)
    wavelength = float(wavelength)
    pre_factor = 4 * np.pi / wavelength
    return pre_factor * np.sin(two_theta / 2)


def multi_tau_lags(multitau_levels, multitau_channels):
    """
    Standard multiple-tau algorithm for finding the lag times (delay
    times).

    Parameters
    ----------
    multitau_levels : int
        number of levels of multiple-taus

    multitau_channels : int
        number of channels or number of buffers in auto-correlators
        normalizations (must be even)

    Returns
    -------
    total_channels : int
        total number of channels ( or total number of delay times)

    lag_steps : ndarray
        delay or lag steps for the multiple tau analysis

    Notes
    -----
    The multi-tau correlation scheme was used for finding the lag times
    (delay times).

    References: text [1]_

    .. [1] K. Schätzela, M. Drewela and  S. Stimaca, "Photon correlation
       measurements at large lag times: Improving statistical accuracy,"
       J. Mod. Opt., vol 35, p 711–718, 1988.
    """
    if multitau_channels % 2 != 0:
        raise ValueError('Number of  multiple tau channels(buffers) must be even. You provided {0} '.format(multitau_channels))
    tot_channels = (multitau_levels + 1) * multitau_channels // 2
    lag = []
    lag_steps = np.arange(0, multitau_channels)
    for i in range(2, multitau_levels + 1):
        for j in range(0, multitau_channels // 2):
            lag.append((multitau_channels // 2 + j) * 2 ** (i - 1))

    lag_steps = np.append(lag_steps, np.array(lag))
    return (
     tot_channels, lag_steps)


def geometric_series(common_ratio, number_of_images, first_term=1):
    """
    This will provide the geometric series for the integration.
    Last values of the series has to be less than or equal to number
    of images
    ex: number_of_images = 100, first_term =1
    common_ratio = 2, geometric_series =  1, 2, 4, 8, 16, 32, 64
    common_ratio = 3, geometric_series =  1, 3, 9, 27, 81

    Parameters
    ----------
    common_ratio : float
        common ratio of the series

    number_of_images : int
        number of images

    first_term : float, optional
        first term in the series

    Return
    ------
    geometric_series : list
        time series

    Note
    ----
    :math ::
     a + ar + ar^2 + ar^3 + ar^4 + ...

     a - first term in the series
     r - is the common ratio
    """
    geometric_series = [
     first_term]
    while geometric_series[(-1)] * common_ratio < number_of_images:
        geometric_series.append(geometric_series[(-1)] * common_ratio)

    return geometric_series