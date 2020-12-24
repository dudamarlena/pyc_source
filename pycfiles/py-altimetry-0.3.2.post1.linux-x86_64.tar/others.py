# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/tools/others.py
# Compiled at: 2016-03-23 12:35:00
import numpy as np, datetime
from dateutil import tz
from Tkinter import Tk
import inspect, getpass, socket, platform
from warnings import warn
import collections, __main__, os, sys

def get_zero_element(array):
    try:
        array = array.flat.next()
    except StopIteration:
        pass

    return array


def current_time():
    LOCAL = tz.tzlocal()
    GMT = tz.gettz('GMT')
    return datetime.datetime.now().replace(tzinfo=LOCAL).astimezone(GMT)


def bytscl(array, maximum=None, minimum=None, nan=0, top=255):
    """
    see http://star.pst.qub.ac.uk/idl/BYTSCL.html
    note that IDL uses slightly different formulae for bytscaling floats and ints. 
    here we apply only the FLOAT formula...
    """
    if maximum is None:
        maximum = np.nanmax(array)
    if minimum is None:
        minimum = np.nanmin(array)
    return np.maximum(np.minimum(((top + 1.0) * (array - minimum) / (maximum - minimum)).astype(np.int16), top), 0)


def scale_vector(x, bottom, top):
    return (x - bottom) / (top - bottom)


def get_screen_size(units='p'):
    units = '1' + units
    width = Tk().winfo_fpixels(str(Tk().winfo_screenwidth()) + 'p') / Tk().winfo_fpixels(units)
    height = Tk().winfo_fpixels(str(Tk().winfo_screenheight()) + 'p') / Tk().winfo_fpixels(units)
    return np.array([width, height])


def get_screen_dpi(units='1i'):
    return Tk().winfo_fpixels(units)


def where_list(list1, list2):
    index = []
    for i in list1:
        try:
            index.append(list2.index(i))
        except ValueError:
            index.append(-1)

    return index


def argresample(a, **kwargs):
    """
    This function returns the positions needed for resampling a "gappy" vector 
    
    :keyword dt: Force sampling at a given resolution. Otherwise uses main data sampling (computed by getting the median value of the derivative)
    """
    dt = kwargs.get('dt', np.median(deriv(a)))
    h, _ = np.histogram(a, bins=(a.max() - a.min()) / dt + 1, range=[a.min() - dt / 2.0, a.max() + dt / 2.0])
    return h.astype(bool)


def isiterable(item):
    """
    Check if item is iterable ans is not a string (or unicode)
    """
    if isinstance(item, collections.Iterable):
        if not isinstance(item, (str, unicode)):
            return True
        else:
            return False

    else:
        False


def deriv(*args):
    """
    ; Copyright (c) 1984-2009, ITT Visual Information Solutions. All
    ;       rights reserved. Unauthorized reproduction is prohibited.
    ;
    
    ;+
    ; NAME:
    ;    DERIV
    ;
    ; PURPOSE:
    ;    Perform numerical differentiation using 3-point, Lagrangian 
    ;    interpolation.
    ;
    ; CATEGORY:
    ;    Numerical analysis.
    ;
    ; CALLING SEQUENCE:
    ;    Dy = Deriv(Y)         ;Dy(i)/di, point spacing = 1.
    ;    Dy = Deriv(X, Y)    ;Dy/Dx, unequal point spacing.
    ;
    ; INPUTS:
    ;    Y:  Variable to be differentiated.
    ;    X:  Variable to differentiate with respect to.  If omitted, unit 
    ;        spacing for Y (i.e., X(i) = i) is assumed.
    ;
    ; OPTIONAL INPUT PARAMETERS:
    ;    As above.
    ;
    ; OUTPUTS:
    ;    Returns the derivative.
    ;
    ; COMMON BLOCKS:
    ;    None.
    ;
    ; SIDE EFFECTS:
    ;    None.
    ;
    ; RESTRICTIONS:
    ;    None.
    ;
    ; PROCEDURE:
    ;    See Hildebrand, Introduction to Numerical Analysis, Mc Graw
    ;    Hill, 1956.  Page 82.
    ;
    ; MODIFICATION HISTORY:
    ;    Written, DMS, Aug, 1984.
    ;    Corrected formula for points with unequal spacing.  DMS, Nov, 1999.
    ;-
    ;
    ; on_error,2              ;Return to caller if an error occurs
    """
    x = args[0]
    n = x.size
    if n < 3:
        raise Exception('Parameters must have at least 3 points')
    if len(args) == 2:
        y = args[1]
        if n != y.size:
            raise 'Vectors must have same size'
        if isinstance(x, np.ma.masked_array):
            x = x.data
        if not isinstance(x, np.float):
            x.astype(np.float)
        x12 = x - np.roll(x, -1)
        x01 = np.roll(x, 1) - x
        x02 = np.roll(x, 1) - np.roll(x, -1)
        d = np.roll(y, 1) * (x12 / (x01 * x02)) + y * (1.0 / x12 - 1.0 / x01) - np.roll(y, -1) * (x01 / (x02 * x12))
        d[0] = y[0] * (x01[1] + x02[1]) / (x01[1] * x02[1]) - y[1] * x02[1] / (x01[1] * x12[1]) + y[2] * x01[1] / (x02[1] * x12[1])
        n2 = n - 2
        d[n - 1] = -y[(n - 3)] * x12[n2] / (x01[n2] * x02[n2]) + y[(n - 2)] * x02[n2] / (x01[n2] * x12[n2]) - y[(n - 1)] * (x02[n2] + x12[n2]) / (x02[n2] * x12[n2])
    else:
        d = (np.roll(x, -1) - np.roll(x, 1)) / 2.0
        d[0] = (-3.0 * x[0] + 4.0 * x[1] - x[2]) / 2.0
        d[n - 1] = (3.0 * x[(n - 1)] - 4.0 * x[(n - 2)] + x[(n - 3)]) / 2.0
    return d


def mask2NaN(array):
    n = array.size
    if array.mask.size != n:
        array.mask = np.zeros(n, dtype=bool)
    array.data[np.arange(n).compress(array.mask)] = np.NaN
    return array


def histogram_indices(hist, R):
    ind = []
    for k in np.arange(len(hist)):
        ind.append(R[R[k]:R[(k + 1)]]) if hist[k] > 0 else ind.append([])

    return ind


def nanargmin(array, axis=None):
    if axis is None:
        return np.nanargmin()
    else:
        return


def nearest(t, x):
    adiff = np.abs(t - np.float(x))
    i = np.argmin(adiff)
    return i


def cart2polar(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)
    return (r, theta)


def polar2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return (x, y)


def rad2geo(alpha):
    theta = np.rad2deg(alpha) * -1 + 360 + 90
    theta = np.mod(theta, 360)
    return theta


def cart2geo(u, v):
    spd, d = cart2polar(u, v)
    d = rad2geo(d)
    return (spd, d)


def rms(array):
    """
    ;+
    ; RMS : Returns root-mean-squared deviation of an array
    ; 
    ; @param array {in}{required}{type:NUMERIC} 2-dimensionnal array. Time dimension<br />
    ;   should be the last dimension.
    ;   
    ; @returns RMS array (1 value per time serie)
    ; 
    ; @author Renaud DUSSURGET, LEGOS/CTOH
    ;-
    """
    nans = np.where(~np.isnan(array))
    cnt = len(nans)
    if cnt == 0:
        return np.NaN
    nval = np.nansum(~np.isnan(array))
    mn = np.nansum(array) / nval
    return np.sqrt(np.nansum((array - mn) ** 2.0) / nval)


def get_caller(level=2):
    frame = inspect.currentframe()
    for l in np.arange(level):
        frame = frame.f_back

    code = frame.f_code
    return code


def get_main():
    return (' ').join(sys.argv[:])


def username():
    return getpass.getuser()


def hostname(full=False):
    if full:
        return socket.gethostbyaddr(socket.gethostname())[0]
    else:
        return platform.node()


def message(MSG_LEVEL, msg, verbose=1):
    """
     MESSAGE : print function wrapper. Print a message depending on the verbose level
     
     @param MSG_LEVEL {in}{required}{type=int} level of the message to be compared with self.verbose
     
     @example self.message(0,'This message will be shown for any verbose level') 
    """
    caller = get_caller()
    if MSG_LEVEL <= verbose:
        print ('[{0}.{1}()] {2}').format(__name__, caller.co_name, msg)


def warning(MSG_LEVEL, msg, verbose=1):
    """
     WARNING : Wrapper to the warning function. Returns a warning when verbose level is not 0. 
     
     @param MSG_LEVEL {in}{required}{type=int} level of the message to be compared with self.verbose
     
     @example self.waring(1,'Warning being issued) 
    """
    if verbose <= 1:
        warn(msg)