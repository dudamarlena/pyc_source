# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/functions.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 86126 bytes
__doc__ = '\nfunctions.py -  Miscellaneous functions with no other home\nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n'
from __future__ import division
from .python2_3 import asUnicode
from .Qt import QtGui, QtCore, USE_PYSIDE
Colors = {'b':QtGui.QColor(0, 0, 255, 255), 
 'g':QtGui.QColor(0, 255, 0, 255), 
 'r':QtGui.QColor(255, 0, 0, 255), 
 'c':QtGui.QColor(0, 255, 255, 255), 
 'm':QtGui.QColor(255, 0, 255, 255), 
 'y':QtGui.QColor(255, 255, 0, 255), 
 'k':QtGui.QColor(0, 0, 0, 255), 
 'w':QtGui.QColor(255, 255, 255, 255), 
 'd':QtGui.QColor(150, 150, 150, 255), 
 'l':QtGui.QColor(200, 200, 200, 255), 
 's':QtGui.QColor(100, 100, 150, 255)}
SI_PREFIXES = asUnicode('yzafpnµm kMGTPEZY')
SI_PREFIXES_ASCII = 'yzafpnum kMGTPEZY'
from .Qt import QtGui, QtCore, USE_PYSIDE
from . import getConfigOption, setConfigOptions
import numpy as np, decimal, re, ctypes, sys, struct
from . import debug

def siScale(x, minVal=1e-25, allowUnicode=True):
    """
    Return the recommended scale factor and SI prefix string for x.
    
    Example::
    
        siScale(0.0001)   # returns (1e6, 'μ')
        # This indicates that the number 0.0001 is best represented as 0.0001 * 1e6 = 100 μUnits
    """
    if isinstance(x, decimal.Decimal):
        x = float(x)
    else:
        try:
            if np.isnan(x) or np.isinf(x):
                return (1, '')
        except:
            print(x, type(x))
            raise

        if abs(x) < minVal:
            m = 0
            x = 0
        else:
            m = int(np.clip(np.floor(np.log(abs(x)) / np.log(1000)), -9.0, 9.0))
        if m == 0:
            pref = ''
        elif m < -8 or m > 8:
            pref = 'e%d' % (m * 3)
        elif allowUnicode:
            pref = SI_PREFIXES[(m + 8)]
        else:
            pref = SI_PREFIXES_ASCII[(m + 8)]
    p = 0.001 ** m
    return (
     p, pref)


def siFormat(x, precision=3, suffix='', space=True, error=None, minVal=1e-25, allowUnicode=True):
    """
    Return the number x formatted in engineering notation with SI prefix.
    
    Example::
        siFormat(0.0001, suffix='V')  # returns "100 μV"
    """
    if space is True:
        space = ' '
    else:
        if space is False:
            space = ''
        p, pref = siScale(x, minVal, allowUnicode)
        if len(pref) > 0:
            if not pref[0] == 'e':
                pref = space + pref
            if error is None:
                fmt = '%.' + str(precision) + 'g%s%s'
                return fmt % (x * p, pref, suffix)
            if allowUnicode:
                plusminus = space + asUnicode('±') + space
        else:
            plusminus = ' +/- '
    fmt = '%.' + str(precision) + 'g%s%s%s%s'
    return fmt % (x * p, pref, suffix, plusminus, siFormat(error, precision=precision, suffix=suffix, space=space, minVal=minVal))


def siEval(s):
    """
    Convert a value written in SI notation to its equivalent prefixless value
    
    Example::
    
        siEval("100 μV")  # returns 0.0001
    """
    s = asUnicode(s)
    m = re.match('(-?((\\d+(\\.\\d*)?)|(\\.\\d+))([eE]-?\\d+)?)\\s*([u' + SI_PREFIXES + ']?).*$', s)
    if m is None:
        raise Exception("Can't convert string '%s' to number." % s)
    else:
        v = float(m.groups()[0])
        p = m.groups()[6]
        if p == '':
            n = 0
        elif p == 'u':
            n = -2
        else:
            n = SI_PREFIXES.index(p) - 8
    return v * 1000 ** n


class Color(QtGui.QColor):

    def __init__(self, *args):
        QtGui.QColor.__init__(self, mkColor(*args))

    def glColor(self):
        """Return (r,g,b,a) normalized for use in opengl"""
        return (
         self.red() / 255.0, self.green() / 255.0, self.blue() / 255.0, self.alpha() / 255.0)

    def __getitem__(self, ind):
        return (
         self.red, self.green, self.blue, self.alpha)[ind]()


def mkColor(*args):
    """
    Convenience function for constructing QColor from a variety of argument types. Accepted arguments are:
    
    ================ ================================================
     'c'             one of: r, g, b, c, m, y, k, w                      
     R, G, B, [A]    integers 0-255
     (R, G, B, [A])  tuple of integers 0-255
     float           greyscale, 0.0-1.0
     int             see :func:`intColor() <pyqtgraph.intColor>`
     (int, hues)     see :func:`intColor() <pyqtgraph.intColor>`
     "RGB"           hexadecimal strings; may begin with '#'
     "RGBA"          
     "RRGGBB"       
     "RRGGBBAA"     
     QColor          QColor instance; makes a copy.
    ================ ================================================
    """
    err = 'Not sure how to make a color from "%s"' % str(args)
    if len(args) == 1:
        if isinstance(args[0], basestring):
            c = args[0]
            if c[0] == '#':
                c = c[1:]
            if len(c) == 1:
                try:
                    return Colors[c]
                except KeyError:
                    raise Exception('No color named "%s"' % c)

                if len(c) == 3:
                    r = int(c[0] * 2, 16)
                    g = int(c[1] * 2, 16)
                    b = int(c[2] * 2, 16)
                    a = 255
            elif len(c) == 4:
                r = int(c[0] * 2, 16)
                g = int(c[1] * 2, 16)
                b = int(c[2] * 2, 16)
                a = int(c[3] * 2, 16)
            elif len(c) == 6:
                r = int(c[0:2], 16)
                g = int(c[2:4], 16)
                b = int(c[4:6], 16)
                a = 255
            elif len(c) == 8:
                r = int(c[0:2], 16)
                g = int(c[2:4], 16)
                b = int(c[4:6], 16)
                a = int(c[6:8], 16)
        else:
            if isinstance(args[0], QtGui.QColor):
                return QtGui.QColor(args[0])
            if isinstance(args[0], float):
                r = g = b = int(args[0] * 255)
                a = 255
            elif hasattr(args[0], '__len__'):
                if len(args[0]) == 3:
                    r, g, b = args[0]
                    a = 255
                elif len(args[0]) == 4:
                    r, g, b, a = args[0]
                else:
                    if len(args[0]) == 2:
                        return intColor(*args[0])
                    raise Exception(err)
            else:
                if type(args[0]) == int:
                    return intColor(args[0])
                raise Exception(err)
    elif len(args) == 3:
        r, g, b = args
        a = 255
    elif len(args) == 4:
        r, g, b, a = args
    else:
        raise Exception(err)
    args = [r, g, b, a]
    args = [0 if (np.isnan(a) or np.isinf(a)) else a for a in args]
    args = list(map(int, args))
    return (QtGui.QColor)(*args)


def mkBrush(*args, **kwds):
    """
    | Convenience function for constructing Brush.
    | This function always constructs a solid brush and accepts the same arguments as :func:`mkColor() <pyqtgraph.mkColor>`
    | Calling mkBrush(None) returns an invisible brush.
    """
    if 'color' in kwds:
        color = kwds['color']
    elif len(args) == 1:
        arg = args[0]
        if arg is None:
            return QtGui.QBrush(QtCore.Qt.NoBrush)
        if isinstance(arg, QtGui.QBrush):
            return QtGui.QBrush(arg)
        color = arg
    elif len(args) > 1:
        color = args
    return QtGui.QBrush(mkColor(color))


def mkPen(*args, **kargs):
    """
    Convenience function for constructing QPen. 
    
    Examples::
    
        mkPen(color)
        mkPen(color, width=2)
        mkPen(cosmetic=False, width=4.5, color='r')
        mkPen({'color': "FF0", width: 2})
        mkPen(None)   # (no pen)
    
    In these examples, *color* may be replaced with any arguments accepted by :func:`mkColor() <pyqtgraph.mkColor>`    """
    color = kargs.get('color', None)
    width = kargs.get('width', 1)
    style = kargs.get('style', None)
    dash = kargs.get('dash', None)
    cosmetic = kargs.get('cosmetic', True)
    hsv = kargs.get('hsv', None)
    if len(args) == 1:
        arg = args[0]
        if isinstance(arg, dict):
            return mkPen(**arg)
        elif isinstance(arg, QtGui.QPen):
            return QtGui.QPen(arg)
            if arg is None:
                style = QtCore.Qt.NoPen
        else:
            color = arg
    else:
        if len(args) > 1:
            color = args
        if color is None:
            color = mkColor('l')
        if hsv is not None:
            color = hsvColor(*hsv)
        else:
            color = mkColor(color)
    pen = QtGui.QPen(QtGui.QBrush(color), width)
    pen.setCosmetic(cosmetic)
    if style is not None:
        pen.setStyle(style)
    if dash is not None:
        pen.setDashPattern(dash)
    return pen


def hsvColor(hue, sat=1.0, val=1.0, alpha=1.0):
    """Generate a QColor from HSVa values. (all arguments are float 0.0-1.0)"""
    c = QtGui.QColor()
    c.setHsvF(hue, sat, val, alpha)
    return c


def colorTuple(c):
    """Return a tuple (R,G,B,A) from a QColor"""
    return (
     c.red(), c.green(), c.blue(), c.alpha())


def colorStr(c):
    """Generate a hex string code from a QColor"""
    return '%02x%02x%02x%02x' % colorTuple(c)


def intColor(index, hues=9, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=255, **kargs):
    """
    Creates a QColor from a single index. Useful for stepping through a predefined list of colors.
    
    The argument *index* determines which color from the set will be returned. All other arguments determine what the set of predefined colors will be
     
    Colors are chosen by cycling across hues while varying the value (brightness). 
    By default, this selects from a list of 9 hues."""
    hues = int(hues)
    values = int(values)
    ind = int(index) % (hues * values)
    indh = ind % hues
    indv = ind / hues
    if values > 1:
        v = minValue + indv * ((maxValue - minValue) / (values - 1))
    else:
        v = maxValue
    h = minHue + indh * (maxHue - minHue) / hues
    c = QtGui.QColor()
    c.setHsv(h, sat, v)
    c.setAlpha(alpha)
    return c


def glColor(*args, **kargs):
    """
    Convert a color to OpenGL color format (r,g,b,a) floats 0.0-1.0
    Accepts same arguments as :func:`mkColor <pyqtgraph.mkColor>`.
    """
    c = mkColor(*args, **kargs)
    return (
     c.red() / 255.0, c.green() / 255.0, c.blue() / 255.0, c.alpha() / 255.0)


def makeArrowPath(headLen=20, tipAngle=20, tailLen=20, tailWidth=3, baseAngle=0):
    """
    Construct a path outlining an arrow with the given dimensions.
    The arrow points in the -x direction with tip positioned at 0,0.
    If *tipAngle* is supplied (in degrees), it overrides *headWidth*.
    If *tailLen* is None, no tail will be drawn.
    """
    headWidth = headLen * np.tan(tipAngle * 0.5 * np.pi / 180.0)
    path = QtGui.QPainterPath()
    path.moveTo(0, 0)
    path.lineTo(headLen, -headWidth)
    if tailLen is None:
        innerY = headLen - headWidth * np.tan(baseAngle * np.pi / 180.0)
        path.lineTo(innerY, 0)
    else:
        tailWidth *= 0.5
        innerY = headLen - (headWidth - tailWidth) * np.tan(baseAngle * np.pi / 180.0)
        path.lineTo(innerY, -tailWidth)
        path.lineTo(headLen + tailLen, -tailWidth)
        path.lineTo(headLen + tailLen, tailWidth)
        path.lineTo(innerY, tailWidth)
    path.lineTo(headLen, headWidth)
    path.lineTo(0, 0)
    return path


def affineSlice(data, shape, origin, vectors, axes, order=1, returnCoords=False, **kargs):
    """
    Take a slice of any orientation through an array. This is useful for extracting sections of multi-dimensional arrays such as MRI images for viewing as 1D or 2D data.
    
    The slicing axes are aribtrary; they do not need to be orthogonal to the original data or even to each other. It is possible to use this function to extract arbitrary linear, rectangular, or parallelepiped shapes from within larger datasets. The original data is interpolated onto a new array of coordinates using scipy.ndimage.map_coordinates if it is available (see the scipy documentation for more information about this). If scipy is not available, then a slower implementation of map_coordinates is used.
    
    For a graphical interface to this function, see :func:`ROI.getArrayRegion <pyqtgraph.ROI.getArrayRegion>`
    
    ==============  ====================================================================================================
    **Arguments:**
    *data*          (ndarray) the original dataset
    *shape*         the shape of the slice to take (Note the return value may have more dimensions than len(shape))
    *origin*        the location in the original dataset that will become the origin of the sliced data.
    *vectors*       list of unit vectors which point in the direction of the slice axes. Each vector must have the same 
                    length as *axes*. If the vectors are not unit length, the result will be scaled relative to the 
                    original data. If the vectors are not orthogonal, the result will be sheared relative to the 
                    original data.
    *axes*          The axes in the original dataset which correspond to the slice *vectors*
    *order*         The order of spline interpolation. Default is 1 (linear). See scipy.ndimage.map_coordinates
                    for more information.
    *returnCoords*  If True, return a tuple (result, coords) where coords is the array of coordinates used to select
                    values from the original dataset.
    *All extra keyword arguments are passed to scipy.ndimage.map_coordinates.*
    --------------------------------------------------------------------------------------------------------------------
    ==============  ====================================================================================================
    
    Note the following must be true: 
        
        | len(shape) == len(vectors) 
        | len(origin) == len(axes) == len(vectors[i])
        
    Example: start with a 4D fMRI data set, take a diagonal-planar slice out of the last 3 axes
        
        * data = array with dims (time, x, y, z) = (100, 40, 40, 40)
        * The plane to pull out is perpendicular to the vector (x,y,z) = (1,1,1) 
        * The origin of the slice will be at (x,y,z) = (40, 0, 0)
        * We will slice a 20x20 plane from each timepoint, giving a final shape (100, 20, 20)
        
    The call for this example would look like::
        
        affineSlice(data, shape=(20,20), origin=(40,0,0), vectors=((-1, 1, 0), (-1, 0, 1)), axes=(1,2,3))
    
    """
    try:
        import scipy.ndimage
        have_scipy = True
    except ImportError:
        have_scipy = False

    have_scipy = False
    if len(shape) != len(vectors):
        raise Exception('shape and vectors must have same length.')
    if len(origin) != len(axes):
        raise Exception('origin and axes must have same length.')
    for v in vectors:
        if len(v) != len(axes):
            raise Exception('each vector must be same length as axes.')

    shape = list(map(np.ceil, shape))
    trAx = list(range(data.ndim))
    for x in axes:
        trAx.remove(x)

    tr1 = tuple(axes) + tuple(trAx)
    data = data.transpose(tr1)
    if not isinstance(vectors, np.ndarray):
        vectors = np.array(vectors)
    if not isinstance(origin, np.ndarray):
        origin = np.array(origin)
    origin.shape = (
     len(axes),) + (1, ) * len(shape)
    grid = np.mgrid[tuple([slice(0, x) for x in shape])]
    x = (grid[(np.newaxis, ...)] * vectors.transpose()[((Ellipsis,) + (np.newaxis,) * len(shape))]).sum(axis=1)
    x += origin
    if have_scipy:
        extraShape = data.shape[len(axes):]
        output = np.empty((tuple(shape) + extraShape), dtype=(data.dtype))
        for inds in (np.ndindex)(*extraShape):
            ind = (
             Ellipsis,) + inds
            output[ind] = (scipy.ndimage.map_coordinates)(data[ind], x, order=order, **kargs)

    else:
        tr = tuple(range(1, x.ndim)) + (0, )
        output = interpolateArray(data, x.transpose(tr))
    tr = list(range(output.ndim))
    trb = []
    for i in range(min(axes)):
        ind = tr1.index(i) + (len(shape) - len(axes))
        tr.remove(ind)
        trb.append(ind)

    tr2 = tuple(trb + tr)
    output = output.transpose(tr2)
    if returnCoords:
        return (output, x)
    return output


def interpolateArray(data, x, default=0.0):
    """
    N-dimensional interpolation similar to scipy.ndimage.map_coordinates.
    
    This function returns linearly-interpolated values sampled from a regular
    grid of data. 
    
    *data* is an array of any shape containing the values to be interpolated.
    *x* is an array with (shape[-1] <= data.ndim) containing the locations
        within *data* to interpolate. 
    
    Returns array of shape (x.shape[:-1] + data.shape[x.shape[-1]:])
    
    For example, assume we have the following 2D image data::
    
        >>> data = np.array([[1,   2,   4  ],
                             [10,  20,  40 ],
                             [100, 200, 400]])
        
    To compute a single interpolated point from this data::
        
        >>> x = np.array([(0.5, 0.5)])
        >>> interpolateArray(data, x)
        array([ 8.25])
        
    To compute a 1D list of interpolated locations:: 
        
        >>> x = np.array([(0.5, 0.5),
                          (1.0, 1.0),
                          (1.0, 2.0),
                          (1.5, 0.0)])
        >>> interpolateArray(data, x)
        array([  8.25,  20.  ,  40.  ,  55.  ])
        
    To compute a 2D array of interpolated locations::
    
        >>> x = np.array([[(0.5, 0.5), (1.0, 2.0)],
                          [(1.0, 1.0), (1.5, 0.0)]])
        >>> interpolateArray(data, x)
        array([[  8.25,  40.  ],
               [ 20.  ,  55.  ]])
               
    ..and so on. The *x* argument may have any shape as long as 
    ```x.shape[-1] <= data.ndim```. In the case that 
    ```x.shape[-1] < data.ndim```, then the remaining axes are simply 
    broadcasted as usual. For example, we can interpolate one location
    from an entire row of the data::
    
        >>> x = np.array([[0.5]])
        >>> interpolateArray(data, x)
        array([[  5.5,  11. ,  22. ]])

    This is useful for interpolating from arrays of colors, vertexes, etc.
    """
    prof = debug.Profiler()
    nd = data.ndim
    md = x.shape[(-1)]
    if md > nd:
        raise TypeError('x.shape[-1] must be less than or equal to data.ndim')
    else:
        fields = np.mgrid[((slice(0, 2),) * md)]
        xmin = np.floor(x).astype(int)
        xmax = xmin + 1
        indexes = np.concatenate([xmin[(np.newaxis, ...)], xmax[(np.newaxis, ...)]])
        fieldInds = []
        totalMask = np.ones((x.shape[:-1]), dtype=bool)
        for ax in range(md):
            mask = (xmin[(..., ax)] >= 0) & (x[(..., ax)] <= data.shape[ax] - 1)
            totalMask &= mask
            mask &= xmax[(..., ax)] < data.shape[ax]
            axisIndex = indexes[(..., ax)][fields[ax]]
            axisIndex[axisIndex < 0] = 0
            axisIndex[axisIndex >= data.shape[ax]] = 0
            fieldInds.append(axisIndex)

        prof()
        fieldData = data[tuple(fieldInds)]
        prof()
        s = np.empty(((md,) + fieldData.shape), dtype=float)
        dx = x - xmin
        for ax in range(md):
            f1 = fields[ax].reshape(fields[ax].shape + (1, ) * (dx.ndim - 1))
            sax = f1 * dx[(..., ax)] + (1 - f1) * (1 - dx[(..., ax)])
            sax = sax.reshape(sax.shape + (1, ) * (s.ndim - 1 - sax.ndim))
            s[ax] = sax

        s = np.product(s, axis=0)
        result = fieldData * s
        for i in range(md):
            result = result.sum(axis=0)

        prof()
        if totalMask.ndim > 0:
            result[~totalMask] = default
        elif totalMask is False:
            result[:] = default
    prof()
    return result


def subArray(data, offset, shape, stride):
    """
    Unpack a sub-array from *data* using the specified offset, shape, and stride.
    
    Note that *stride* is specified in array elements, not bytes.
    For example, we have a 2x3 array packed in a 1D array as follows::
    
        data = [_, _, 00, 01, 02, _, 10, 11, 12, _]
        
    Then we can unpack the sub-array with this call::
    
        subArray(data, offset=2, shape=(2, 3), stride=(4, 1))
        
    ..which returns::
    
        [[00, 01, 02],
         [10, 11, 12]]
         
    This function operates only on the first axis of *data*. So changing 
    the input in the example above to have shape (10, 7) would cause the
    output to have shape (2, 3, 7).
    """
    data = data[offset:]
    shape = tuple(shape)
    stride = tuple(stride)
    extraShape = data.shape[1:]
    for i in range(len(shape)):
        mask = (slice(None),) * i + (slice(None, shape[i] * stride[i]),)
        newShape = shape[:i + 1]
        if i < len(shape) - 1:
            newShape += (stride[i],)
        newShape += extraShape
        data = data[mask]
        data = data.reshape(newShape)

    return data


def transformToArray(tr):
    """
    Given a QTransform, return a 3x3 numpy array.
    Given a QMatrix4x4, return a 4x4 numpy array.
    
    Example: map an array of x,y coordinates through a transform::
    
        ## coordinates to map are (1,5), (2,6), (3,7), and (4,8)
        coords = np.array([[1,2,3,4], [5,6,7,8], [1,1,1,1]])  # the extra '1' coordinate is needed for translation to work
        
        ## Make an example transform
        tr = QtGui.QTransform()
        tr.translate(3,4)
        tr.scale(2, 0.1)
        
        ## convert to array
        m = pg.transformToArray()[:2]  # ignore the perspective portion of the transformation
        
        ## map coordinates through transform
        mapped = np.dot(m, coords)
    """
    if isinstance(tr, QtGui.QTransform):
        return np.array([[tr.m11(), tr.m21(), tr.m31()], [tr.m12(), tr.m22(), tr.m32()], [tr.m13(), tr.m23(), tr.m33()]])
    if isinstance(tr, QtGui.QMatrix4x4):
        return np.array(tr.copyDataTo()).reshape(4, 4)
    raise Exception('Transform argument must be either QTransform or QMatrix4x4.')


def transformCoordinates(tr, coords, transpose=False):
    """
    Map a set of 2D or 3D coordinates through a QTransform or QMatrix4x4.
    The shape of coords must be (2,...) or (3,...)
    The mapping will _ignore_ any perspective transformations.
    
    For coordinate arrays with ndim=2, this is basically equivalent to matrix multiplication.
    Most arrays, however, prefer to put the coordinate axis at the end (eg. shape=(...,3)). To 
    allow this, use transpose=True.
    
    """
    if transpose:
        coords = coords.transpose((coords.ndim - 1,) + tuple(range(0, coords.ndim - 1)))
    else:
        nd = coords.shape[0]
        if isinstance(tr, np.ndarray):
            m = tr
        else:
            m = transformToArray(tr)
            m = m[:m.shape[0] - 1]
        if m.shape == (2, 3):
            if nd == 3:
                m2 = np.zeros((3, 4))
                m2[:2, :2] = m[:2, :2]
                m2[:2, 3] = m[:2, 2]
                m2[(2, 2)] = 1
                m = m2
        if m.shape == (3, 4) and nd == 2:
            m2 = np.empty((2, 3))
            m2[:, :2] = m[:2, :2]
            m2[:, 2] = m[:2, 3]
            m = m2
    m = m.reshape(m.shape + (1, ) * (coords.ndim - 1))
    coords = coords[(np.newaxis, ...)]
    translate = m[:, -1]
    m = m[:, :-1]
    mapped = (m * coords).sum(axis=1)
    mapped += translate
    if transpose:
        mapped = mapped.transpose(tuple(range(1, mapped.ndim)) + (0, ))
    return mapped


def solve3DTransform(points1, points2):
    """
    Find a 3D transformation matrix that maps points1 onto points2.
    Points must be specified as either lists of 4 Vectors or 
    (4, 3) arrays.
    """
    import numpy.linalg
    pts = []
    for inp in (points1, points2):
        if isinstance(inp, np.ndarray):
            A = np.empty((4, 4), dtype=float)
            A[:, :3] = inp[:, :3]
            A[:, 3] = 1.0
        else:
            A = np.array([[inp[i].x(), inp[i].y(), inp[i].z(), 1] for i in range(4)])
        pts.append(A)

    matrix = np.zeros((4, 4))
    for i in range(3):
        matrix[i] = numpy.linalg.solve(pts[0], pts[1][:, i])

    return matrix


def solveBilinearTransform(points1, points2):
    """
    Find a bilinear transformation matrix (2x4) that maps points1 onto points2.
    Points must be specified as a list of 4 Vector, Point, QPointF, etc.
    
    To use this matrix to map a point [x,y]::
    
        mapped = np.dot(matrix, [x*y, x, y, 1])
    """
    import numpy.linalg
    A = np.array([[points1[i].x() * points1[i].y(), points1[i].x(), points1[i].y(), 1] for i in range(4)])
    B = np.array([[points2[i].x(), points2[i].y()] for i in range(4)])
    matrix = np.zeros((2, 4))
    for i in range(2):
        matrix[i] = numpy.linalg.solve(A, B[:, i])

    return matrix


def rescaleData(data, scale, offset, dtype=None):
    """Return data rescaled and optionally cast to a new dtype::
    
        data => (data-offset) * scale
        
    Uses scipy.weave (if available) to improve performance.
    """
    if dtype is None:
        dtype = data.dtype
    else:
        dtype = np.dtype(dtype)
    try:
        if not getConfigOption('useWeave'):
            raise Exception('Weave is disabled; falling back to slower version.')
        else:
            try:
                import scipy.weave
            except ImportError:
                raise Exception('scipy.weave is not importable; falling back to slower version.')

            if not data.dtype.isnative:
                data = data.astype(data.dtype.newbyteorder('='))
            if not dtype.isnative:
                weaveDtype = dtype.newbyteorder('=')
            else:
                weaveDtype = dtype
        newData = np.empty((data.size,), dtype=weaveDtype)
        flat = np.ascontiguousarray(data).reshape(data.size)
        size = data.size
        code = '\n        double sc = (double)scale;\n        double off = (double)offset;\n        for( int i=0; i<size; i++ ) {\n            newData[i] = ((double)flat[i] - off) * sc;\n        }\n        '
        scipy.weave.inline(code, ['flat', 'newData', 'size', 'offset', 'scale'], compiler='gcc')
        if dtype != weaveDtype:
            newData = newData.astype(dtype)
        data = newData.reshape(data.shape)
    except:
        if getConfigOption('useWeave'):
            if getConfigOption('weaveDebug'):
                debug.printExc('Error; disabling weave.')
            setConfigOptions(useWeave=False)
        d2 = data - offset
        d2 *= scale
        data = d2.astype(dtype)

    return data


def applyLookupTable(data, lut):
    """
    Uses values in *data* as indexes to select values from *lut*.
    The returned data has shape data.shape + lut.shape[1:]
    
    Note: color gradient lookup tables can be generated using GradientWidget.
    """
    if data.dtype.kind not in ('i', 'u'):
        data = data.astype(int)
    return np.take(lut, data, axis=0, mode='clip')


def makeRGBA(*args, **kwds):
    """Equivalent to makeARGB(..., useRGBA=True)"""
    kwds['useRGBA'] = True
    return makeARGB(*args, **kwds)


def makeARGB(data, lut=None, levels=None, scale=None, useRGBA=False):
    """ 
    Convert an array of values into an ARGB array suitable for building QImages, OpenGL textures, etc.
    
    Returns the ARGB array (values 0-255) and a boolean indicating whether there is alpha channel data.
    This is a two stage process:
    
        1) Rescale the data based on the values in the *levels* argument (min, max).
        2) Determine the final output by passing the rescaled values through a lookup table.
   
    Both stages are optional.
    
    ============== ==================================================================================
    **Arguments:**
    data           numpy array of int/float types. If 
    levels         List [min, max]; optionally rescale data before converting through the
                   lookup table. The data is rescaled such that min->0 and max->*scale*::
                   
                      rescaled = (clip(data, min, max) - min) * (*scale* / (max - min))
                   
                   It is also possible to use a 2D (N,2) array of values for levels. In this case,
                   it is assumed that each pair of min,max values in the levels array should be 
                   applied to a different subset of the input data (for example, the input data may 
                   already have RGB values and the levels are used to independently scale each 
                   channel). The use of this feature requires that levels.shape[0] == data.shape[-1].
    scale          The maximum value to which data will be rescaled before being passed through the 
                   lookup table (or returned if there is no lookup table). By default this will
                   be set to the length of the lookup table, or 256 is no lookup table is provided.
                   For OpenGL color specifications (as in GLColor4f) use scale=1.0
    lut            Optional lookup table (array with dtype=ubyte).
                   Values in data will be converted to color by indexing directly from lut.
                   The output data shape will be input.shape + lut.shape[1:].
                   
                   Note: the output of makeARGB will have the same dtype as the lookup table, so
                   for conversion to QImage, the dtype must be ubyte.
                   
                   Lookup tables can be built using GradientWidget.
    useRGBA        If True, the data is returned in RGBA order (useful for building OpenGL textures). 
                   The default is False, which returns in ARGB order for use with QImage 
                   (Note that 'ARGB' is a term used by the Qt documentation; the _actual_ order 
                   is BGRA).
    ============== ==================================================================================
    """
    profile = debug.Profiler()
    if lut is not None:
        if not isinstance(lut, np.ndarray):
            lut = np.array(lut)
    if levels is not None:
        if not isinstance(levels, np.ndarray):
            levels = np.array(levels)
    elif levels is not None:
        if levels.ndim == 1:
            if len(levels) != 2:
                raise Exception('levels argument must have length 2')
        elif levels.ndim == 2:
            if lut is not None:
                if lut.ndim > 1:
                    raise Exception('Cannot make ARGB data when bot levels and lut have ndim > 2')
            if levels.shape != (data.shape[(-1)], 2):
                raise Exception('levels must have shape (data.shape[-1], 2)')
        else:
            print(levels)
            raise Exception('levels argument must be 1D or 2D.')
    profile()
    if scale is None:
        if lut is not None:
            scale = lut.shape[0]
        else:
            scale = 255.0
    elif levels is not None:
        if isinstance(levels, np.ndarray):
            if levels.ndim == 2:
                if levels.shape[0] != data.shape[(-1)]:
                    raise Exception('When rescaling multi-channel data, there must be the same number of levels as channels (data.shape[-1] == levels.shape[0])')
                newData = np.empty((data.shape), dtype=int)
                for i in range(data.shape[(-1)]):
                    minVal, maxVal = levels[i]
                    if minVal == maxVal:
                        maxVal += 1e-16
                    newData[(..., i)] = rescaleData((data[(..., i)]), (scale / (maxVal - minVal)), minVal, dtype=int)

                data = newData
            else:
                minVal, maxVal = levels
                if minVal == maxVal:
                    maxVal += 1e-16
                elif maxVal == minVal:
                    data = rescaleData(data, 1, minVal, dtype=int)
                else:
                    data = rescaleData(data, (scale / (maxVal - minVal)), minVal, dtype=int)
        else:
            profile()
            if lut is not None:
                data = applyLookupTable(data, lut)
            elif data.dtype is not np.ubyte:
                data = np.clip(data, 0, 255).astype(np.ubyte)
            profile()
            imgData = np.empty((data.shape[:2] + (4, )), dtype=(np.ubyte))
            profile()
            if useRGBA:
                order = [
                 0, 1, 2, 3]
            else:
                order = [
                 2, 1, 0, 3]
        if data.ndim == 2:
            for i in range(3):
                imgData[(..., i)] = data

        elif data.shape[2] == 1:
            for i in range(3):
                imgData[(..., i)] = data[(Ellipsis, 0)]

        else:
            for i in range(0, data.shape[2]):
                imgData[(..., i)] = data[(..., order[i])]

        profile()
        if data.ndim == 2 or data.shape[2] == 3:
            alpha = False
            imgData[(Ellipsis, 3)] = 255
    else:
        alpha = True
    profile()
    return (
     imgData, alpha)


def makeQImage(imgData, alpha=None, copy=True, transpose=True):
    """
    Turn an ARGB array into QImage.
    By default, the data is copied; changes to the array will not
    be reflected in the image. The image will be given a 'data' attribute
    pointing to the array which shares its data to prevent python
    freeing that memory while the image is in use.
    
    ============== ===================================================================
    **Arguments:**
    imgData        Array of data to convert. Must have shape (width, height, 3 or 4) 
                   and dtype=ubyte. The order of values in the 3rd axis must be 
                   (b, g, r, a).
    alpha          If True, the QImage returned will have format ARGB32. If False,
                   the format will be RGB32. By default, _alpha_ is True if
                   array.shape[2] == 4.
    copy           If True, the data is copied before converting to QImage.
                   If False, the new QImage points directly to the data in the array.
                   Note that the array must be contiguous for this to work
                   (see numpy.ascontiguousarray).
    transpose      If True (the default), the array x/y axes are transposed before 
                   creating the image. Note that Qt expects the axes to be in 
                   (height, width) order whereas pyqtgraph usually prefers the 
                   opposite.
    ============== ===================================================================    
    """
    profile = debug.Profiler()
    if alpha is None:
        alpha = imgData.shape[2] == 4
    else:
        copied = False
        if imgData.shape[2] == 3:
            if copy is True:
                d2 = np.empty((imgData.shape[:2] + (4, )), dtype=(imgData.dtype))
                d2[:, :, :3] = imgData
                d2[:, :, 3] = 255
                imgData = d2
                copied = True
            else:
                raise Exception('Array has only 3 channels; cannot make QImage without copying.')
        if alpha:
            imgFormat = QtGui.QImage.Format_ARGB32
        else:
            imgFormat = QtGui.QImage.Format_RGB32
    if transpose:
        imgData = imgData.transpose((1, 0, 2))
    profile()
    if not imgData.flags['C_CONTIGUOUS']:
        if copy is False:
            extra = ' (try setting transpose=False)' if transpose else ''
            raise Exception('Array is not contiguous; cannot make QImage without copying.' + extra)
        imgData = np.ascontiguousarray(imgData)
        copied = True
    elif copy is True:
        if copied is False:
            imgData = imgData.copy()
        if USE_PYSIDE:
            ch = ctypes.c_char.from_buffer(imgData, 0)
            img = QtGui.QImage(ch, imgData.shape[1], imgData.shape[0], imgFormat)
    else:
        try:
            img = QtGui.QImage(imgData.ctypes.data, imgData.shape[1], imgData.shape[0], imgFormat)
        except:
            if copy:
                img = QtGui.QImage(buffer(imgData), imgData.shape[1], imgData.shape[0], imgFormat)
            else:
                img = QtGui.QImage(memoryview(imgData), imgData.shape[1], imgData.shape[0], imgFormat)

    img.data = imgData
    return img


def imageToArray(img, copy=False, transpose=True):
    """
    Convert a QImage into numpy array. The image must have format RGB32, ARGB32, or ARGB32_Premultiplied.
    By default, the image is not copied; changes made to the array will appear in the QImage as well (beware: if 
    the QImage is collected before the array, there may be trouble).
    The array will have shape (width, height, (b,g,r,a)).
    """
    fmt = img.format()
    ptr = img.bits()
    if USE_PYSIDE:
        arr = np.frombuffer(ptr, dtype=(np.ubyte))
    else:
        ptr.setsize(img.byteCount())
        arr = np.asarray(ptr)
        if img.byteCount() != arr.size * arr.itemsize:
            arr = np.frombuffer(ptr, np.ubyte, img.byteCount())
    if fmt == img.Format_RGB32:
        arr = arr.reshape(img.height(), img.width(), 3)
    elif fmt == img.Format_ARGB32 or fmt == img.Format_ARGB32_Premultiplied:
        arr = arr.reshape(img.height(), img.width(), 4)
    if copy:
        arr = arr.copy()
    if transpose:
        return arr.transpose((1, 0, 2))
    return arr


def colorToAlpha(data, color):
    """
    Given an RGBA image in *data*, convert *color* to be transparent. 
    *data* must be an array (w, h, 3 or 4) of ubyte values and *color* must be 
    an array (3) of ubyte values.
    This is particularly useful for use with images that have a black or white background.
    
    Algorithm is taken from Gimp's color-to-alpha function in plug-ins/common/colortoalpha.c
    Credit:
        /*
        * Color To Alpha plug-in v1.0 by Seth Burgess, sjburges@gimp.org 1999/05/14
        *  with algorithm by clahey
        */
    
    """
    data = data.astype(float)
    if data.shape[(-1)] == 3:
        d2 = np.empty((data.shape[:2] + (4, )), dtype=(data.dtype))
        d2[..., :3] = data
        d2[(Ellipsis, 3)] = 255
        data = d2
    color = color.astype(float)
    alpha = np.zeros((data.shape[:2] + (3, )), dtype=float)
    output = data.copy()
    for i in (0, 1, 2):
        d = data[(..., i)]
        c = color[i]
        mask = d > c
        alpha[(..., i)][mask] = (d[mask] - c) / (255.0 - c)
        imask = d < c
        alpha[(..., i)][imask] = (c - d[imask]) / c

    output[(Ellipsis, 3)] = alpha.max(axis=2) * 255.0
    mask = output[(Ellipsis, 3)] >= 1.0
    correction = 255.0 / output[(Ellipsis, 3)][mask]
    for i in (0, 1, 2):
        output[(..., i)][mask] = (output[(..., i)][mask] - color[i]) * correction + color[i]
        output[(Ellipsis, 3)][mask] *= data[(Ellipsis, 3)][mask] / 255.0

    return np.clip(output, 0, 255).astype(np.ubyte)


def gaussianFilter(data, sigma):
    """
    Drop-in replacement for scipy.ndimage.gaussian_filter.
    
    (note: results are only approximately equal to the output of
     gaussian_filter)
    """
    if np.isscalar(sigma):
        sigma = (
         sigma,) * data.ndim
    baseline = data.mean()
    filtered = data - baseline
    for ax in range(data.ndim):
        s = sigma[ax]
        if s == 0:
            continue
        ksize = int(s * 6)
        x = np.arange(-ksize, ksize)
        kernel = np.exp(-x ** 2 / (2 * s ** 2))
        kshape = [1] * data.ndim
        kshape[ax] = len(kernel)
        kernel = kernel.reshape(kshape)
        shape = data.shape[ax] + ksize
        scale = 1.0 / (abs(s) * (2 * np.pi) ** 0.5)
        filtered = scale * np.fft.irfft((np.fft.rfft(filtered, shape, axis=ax) * np.fft.rfft(kernel, shape, axis=ax)),
          axis=ax)
        sl = [
         slice(None)] * data.ndim
        sl[ax] = slice(filtered.shape[ax] - data.shape[ax], None, None)
        filtered = filtered[sl]

    return filtered + baseline


def downsample(data, n, axis=0, xvals='subsample'):
    """Downsample by averaging points together across axis.
    If multiple axes are specified, runs once per axis.
    If a metaArray is given, then the axis values can be either subsampled
    or downsampled to match.
    """
    ma = None
    if hasattr(data, 'implements'):
        if data.implements('MetaArray'):
            ma = data
            data = data.view(np.ndarray)
    if hasattr(axis, '__len__'):
        if not hasattr(n, '__len__'):
            n = [
             n] * len(axis)
        for i in range(len(axis)):
            data = downsample(data, n[i], axis[i])

        return data
    if n <= 1:
        return data
    nPts = int(data.shape[axis] / n)
    s = list(data.shape)
    s[axis] = nPts
    s.insert(axis + 1, n)
    sl = [slice(None)] * data.ndim
    sl[axis] = slice(0, nPts * n)
    d1 = data[tuple(sl)]
    d1.shape = tuple(s)
    d2 = d1.mean(axis + 1)
    if ma is None:
        return d2
    info = ma.infoCopy()
    if 'values' in info[axis]:
        if xvals == 'subsample':
            info[axis]['values'] = info[axis]['values'][::n][:nPts]
        elif xvals == 'downsample':
            info[axis]['values'] = downsample(info[axis]['values'], n)
    return MetaArray(d2, info=info)


def arrayToQPath(x, y, connect='all'):
    """Convert an array of x,y coordinats to QPainterPath as efficiently as possible.
    The *connect* argument may be 'all', indicating that each point should be
    connected to the next; 'pairs', indicating that each pair of points
    should be connected, or an array of int32 values (0 or 1) indicating
    connections.
    """
    path = QtGui.QPainterPath()
    n = x.shape[0]
    arr = np.empty((n + 2), dtype=[('x', '>f8'), ('y', '>f8'), ('c', '>i4')])
    byteview = arr.view(dtype=(np.ubyte))
    byteview[:12] = 0
    byteview.data[12:20] = struct.pack('>ii', n, 0)
    arr[1:-1]['x'] = x
    arr[1:-1]['y'] = y
    if connect == 'pairs':
        connect = np.empty((n / 2, 2), dtype=(np.int32))
        if connect.size != n:
            raise Exception("x,y array lengths must be multiple of 2 to use connect='pairs'")
        connect[:, 0] = 1
        connect[:, 1] = 0
        connect = connect.flatten()
    elif connect == 'finite':
        connect = np.isfinite(x) & np.isfinite(y)
        arr[1:-1]['c'] = connect
    elif connect == 'all':
        arr[1:-1]['c'] = 1
    elif isinstance(connect, np.ndarray):
        arr[1:-1]['c'] = connect
    else:
        raise Exception('connect argument must be "all", "pairs", or array')
    lastInd = 20 * (n + 1)
    byteview.data[lastInd:lastInd + 4] = struct.pack('>i', 0)
    path.strn = byteview.data[12:lastInd + 4]
    try:
        buf = QtCore.QByteArray.fromRawData(path.strn)
    except TypeError:
        buf = QtCore.QByteArray(bytes(path.strn))

    ds = QtCore.QDataStream(buf)
    ds >> path
    return path


def isocurve(data, level, connected=False, extendToEdge=False, path=False):
    """
    Generate isocurve from 2D data using marching squares algorithm.
    
    ============== =========================================================
    **Arguments:**
    data           2D numpy array of scalar values
    level          The level at which to generate an isosurface
    connected      If False, return a single long list of point pairs
                   If True, return multiple long lists of connected point 
                   locations. (This is slower but better for drawing 
                   continuous lines)
    extendToEdge   If True, extend the curves to reach the exact edges of 
                   the data. 
    path           if True, return a QPainterPath rather than a list of 
                   vertex coordinates. This forces connected=True.
    ============== =========================================================
    
    This function is SLOW; plenty of room for optimization here.
    """
    if path is True:
        connected = True
    else:
        if extendToEdge:
            d2 = np.empty((data.shape[0] + 2, data.shape[1] + 2), dtype=(data.dtype))
            d2[1:-1, 1:-1] = data
            d2[0, 1:-1] = data[0]
            d2[-1, 1:-1] = data[(-1)]
            d2[1:-1, 0] = data[:, 0]
            d2[1:-1, -1] = data[:, -1]
            d2[(0, 0)] = d2[(0, 1)]
            d2[(0, -1)] = d2[(1, -1)]
            d2[(-1, 0)] = d2[(-1, 1)]
            d2[(-1, -1)] = d2[(-1, -2)]
            data = d2
        else:
            sideTable = [[], [0, 1],
             [
              1, 2],
             [
              0, 2],
             [
              0, 3],
             [
              1, 3],
             [
              0, 1, 2, 3],
             [
              2, 3],
             [
              2, 3],
             [
              0, 1, 2, 3],
             [
              1, 3],
             [
              0, 3],
             [
              0, 2],
             [
              1, 2],
             [
              0, 1], []]
            edgeKey = [
             [
              (0, 1), (0, 0)],
             [
              (0, 0), (1, 0)],
             [
              (1, 0), (1, 1)],
             [
              (1, 1), (0, 1)]]
            lines = []
            mask = data < level
            index = np.zeros([x - 1 for x in data.shape], dtype=(np.ubyte))
            fields = np.empty((2, 2), dtype=object)
            slices = [slice(0, -1), slice(1, None)]
            for i in (0, 1):
                for j in (0, 1):
                    fields[(i, j)] = mask[(slices[i], slices[j])]
                    vertIndex = i + 2 * j
                    index += fields[(i, j)] * 2 ** vertIndex

            for i in range(index.shape[0]):
                for j in range(index.shape[1]):
                    sides = sideTable[index[(i, j)]]
                    for l in range(0, len(sides), 2):
                        edges = sides[l:l + 2]
                        pts = []
                        for m in (0, 1):
                            p1 = edgeKey[edges[m]][0]
                            p2 = edgeKey[edges[m]][1]
                            v1 = data[(i + p1[0], j + p1[1])]
                            v2 = data[(i + p2[0], j + p2[1])]
                            f = (level - v1) / (v2 - v1)
                            fi = 1.0 - f
                            p = (
                             p1[0] * fi + p2[0] * f + i + 0.5,
                             p1[1] * fi + p2[1] * f + j + 0.5)
                            if extendToEdge:
                                p = (
                                 min(data.shape[0] - 2, max(0, p[0] - 1)),
                                 min(data.shape[1] - 2, max(0, p[1] - 1)))
                            if connected:
                                gridKey = (
                                 i + (1 if edges[m] == 2 else 0), j + (1 if edges[m] == 3 else 0), edges[m] % 2)
                                pts.append((p, gridKey))
                            else:
                                pts.append(p)

                        lines.append(pts)

            return connected or lines
        points = {}
        for a, b in lines:
            if a[1] not in points:
                points[a[1]] = []
            points[a[1]].append([a, b])
            if b[1] not in points:
                points[b[1]] = []
            points[b[1]].append([b, a])

        for k in list(points.keys()):
            try:
                chains = points[k]
            except KeyError:
                continue

            for chain in chains:
                x = None
                while True:
                    if x == chain[(-1)][1]:
                        break
                    x = chain[(-1)][1]
                    if x == k:
                        break
                    y = chain[(-2)][1]
                    connects = points[x]
                    for conn in connects[:]:
                        if conn[1][1] != y:
                            chain.extend(conn[1:])

                    del points[x]

                if chain[0][1] == chain[(-1)][1]:
                    chains.pop()
                    break

        lines = []
        for chain in points.values():
            if len(chain) == 2:
                chain = chain[1][1:][::-1] + chain[0]
            else:
                chain = chain[0]
            lines.append([p[0] for p in chain])

        return path or lines
    path = QtGui.QPainterPath()
    for line in lines:
        (path.moveTo)(*line[0])
        for p in line[1:]:
            (path.lineTo)(*p)

    return path


def traceImage(image, values, smooth=0.5):
    """
    Convert an image to a set of QPainterPath curves.
    One curve will be generated for each item in *values*; each curve outlines the area
    of the image that is closer to its value than to any others.
    
    If image is RGB or RGBA, then the shape of values should be (nvals, 3/4)
    The parameter *smooth* is expressed in pixels.
    """
    try:
        import scipy.ndimage as ndi
    except ImportError:
        raise Exception('traceImage() requires the package scipy.ndimage, but it is not importable.')

    if values.ndim == 2:
        values = values.T
    values = values[(np.newaxis, np.newaxis, ...)].astype(float)
    image = image[(..., np.newaxis)].astype(float)
    diff = np.abs(image - values)
    if values.ndim == 4:
        diff = diff.sum(axis=2)
    labels = np.argmin(diff, axis=2)
    paths = []
    for i in range(diff.shape[(-1)]):
        d = (labels == i).astype(float)
        d = gaussianFilter(d, (smooth, smooth))
        lines = isocurve(d, 0.5, connected=True, extendToEdge=True)
        path = QtGui.QPainterPath()
        for line in lines:
            (path.moveTo)(*line[0])
            for p in line[1:]:
                (path.lineTo)(*p)

        paths.append(path)

    return paths


IsosurfaceDataCache = None

def isosurface(data, level):
    """
    Generate isosurface from volumetric data using marching cubes algorithm.
    See Paul Bourke, "Polygonising a Scalar Field"  
    (http://paulbourke.net/geometry/polygonise/)
    
    *data*   3D numpy array of scalar values
    *level*  The level at which to generate an isosurface
    
    Returns an array of vertex coordinates (Nv, 3) and an array of 
    per-face vertex indexes (Nf, 3)    
    """
    global IsosurfaceDataCache
    if IsosurfaceDataCache is None:
        edgeTable = np.array([
         0, 265, 515, 778, 1030, 1295, 1541, 1804,
         2060, 2309, 2575, 2822, 3082, 3331, 3593, 3840,
         400, 153, 915, 666, 1430, 1183, 1941, 1692,
         2460, 2197, 2975, 2710, 3482, 3219, 3993, 3728,
         560, 825, 51, 314, 1590, 1855, 1077, 1340,
         2620, 2869, 2111, 2358, 3642, 3891, 3129, 3376,
         928, 681, 419, 170, 1958, 1711, 1445, 1196,
         2988, 2725, 2479, 2214, 4010, 3747, 3497, 3232,
         1120, 1385, 1635, 1898, 102, 367, 613, 876,
         3180, 3429, 3695, 3942, 2154, 2403, 2665, 2912,
         1520, 1273, 2035, 1786, 502, 255, 1013, 764,
         3580, 3317, 4095, 3830, 2554, 2291, 3065, 2800,
         1616, 1881, 1107, 1370, 598, 863, 85, 348,
         3676, 3925, 3167, 3414, 2650, 2899, 2137, 2384,
         1984, 1737, 1475, 1226, 966, 719, 453, 204,
         4044, 3781, 3535, 3270, 3018, 2755, 2505, 2240,
         2240, 2505, 2755, 3018, 3270, 3535, 3781, 4044,
         204, 453, 719, 966, 1226, 1475, 1737, 1984,
         2384, 2137, 2899, 2650, 3414, 3167, 3925, 3676,
         348, 85, 863, 598, 1370, 1107, 1881, 1616,
         2800, 3065, 2291, 2554, 3830, 4095, 3317, 3580,
         764, 1013, 255, 502, 1786, 2035, 1273, 1520,
         2912, 2665, 2403, 2154, 3942, 3695, 3429, 3180,
         876, 613, 367, 102, 1898, 1635, 1385, 1120,
         3232, 3497, 3747, 4010, 2214, 2479, 2725, 2988,
         1196, 1445, 1711, 1958, 170, 419, 681, 928,
         3376, 3129, 3891, 3642, 2358, 2111, 2869, 2620,
         1340, 1077, 1855, 1590, 314, 51, 825, 560,
         3728, 3993, 3219, 3482, 2710, 2975, 2197, 2460,
         1692, 1941, 1183, 1430, 666, 915, 153, 400,
         3840, 3593, 3331, 3082, 2822, 2575, 2309, 2060,
         1804, 1541, 1295, 1030, 778, 515, 265, 0],
          dtype=(np.uint16))
        triTable = [[],
         [
          0, 8, 3],
         [
          0, 1, 9],
         [
          1, 8, 3, 9, 8, 1],
         [
          1, 2, 10],
         [
          0, 8, 3, 1, 2, 10],
         [
          9, 2, 10, 0, 2, 9],
         [
          2, 8, 3, 2, 10, 8, 10, 9, 8],
         [
          3, 11, 2],
         [
          0, 11, 2, 8, 11, 0],
         [
          1, 9, 0, 2, 3, 11],
         [
          1, 11, 2, 1, 9, 11, 9, 8, 11],
         [
          3, 10, 1, 11, 10, 3],
         [
          0, 10, 1, 0, 8, 10, 8, 11, 10],
         [
          3, 9, 0, 3, 11, 9, 11, 10, 9],
         [
          9, 8, 10, 10, 8, 11],
         [
          4, 7, 8],
         [
          4, 3, 0, 7, 3, 4],
         [
          0, 1, 9, 8, 4, 7],
         [
          4, 1, 9, 4, 7, 1, 7, 3, 1],
         [
          1, 2, 10, 8, 4, 7],
         [
          3, 4, 7, 3, 0, 4, 1, 2, 10],
         [
          9, 2, 10, 9, 0, 2, 8, 4, 7],
         [
          2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4],
         [
          8, 4, 7, 3, 11, 2],
         [
          11, 4, 7, 11, 2, 4, 2, 0, 4],
         [
          9, 0, 1, 8, 4, 7, 2, 3, 11],
         [
          4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1],
         [
          3, 10, 1, 3, 11, 10, 7, 8, 4],
         [
          1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4],
         [
          4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3],
         [
          4, 7, 11, 4, 11, 9, 9, 11, 10],
         [
          9, 5, 4],
         [
          9, 5, 4, 0, 8, 3],
         [
          0, 5, 4, 1, 5, 0],
         [
          8, 5, 4, 8, 3, 5, 3, 1, 5],
         [
          1, 2, 10, 9, 5, 4],
         [
          3, 0, 8, 1, 2, 10, 4, 9, 5],
         [
          5, 2, 10, 5, 4, 2, 4, 0, 2],
         [
          2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8],
         [
          9, 5, 4, 2, 3, 11],
         [
          0, 11, 2, 0, 8, 11, 4, 9, 5],
         [
          0, 5, 4, 0, 1, 5, 2, 3, 11],
         [
          2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5],
         [
          10, 3, 11, 10, 1, 3, 9, 5, 4],
         [
          4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10],
         [
          5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3],
         [
          5, 4, 8, 5, 8, 10, 10, 8, 11],
         [
          9, 7, 8, 5, 7, 9],
         [
          9, 3, 0, 9, 5, 3, 5, 7, 3],
         [
          0, 7, 8, 0, 1, 7, 1, 5, 7],
         [
          1, 5, 3, 3, 5, 7],
         [
          9, 7, 8, 9, 5, 7, 10, 1, 2],
         [
          10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3],
         [
          8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2],
         [
          2, 10, 5, 2, 5, 3, 3, 5, 7],
         [
          7, 9, 5, 7, 8, 9, 3, 11, 2],
         [
          9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11],
         [
          2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7],
         [
          11, 2, 1, 11, 1, 7, 7, 1, 5],
         [
          9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11],
         [
          5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0],
         [
          11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0],
         [
          11, 10, 5, 7, 11, 5],
         [
          10, 6, 5],
         [
          0, 8, 3, 5, 10, 6],
         [
          9, 0, 1, 5, 10, 6],
         [
          1, 8, 3, 1, 9, 8, 5, 10, 6],
         [
          1, 6, 5, 2, 6, 1],
         [
          1, 6, 5, 1, 2, 6, 3, 0, 8],
         [
          9, 6, 5, 9, 0, 6, 0, 2, 6],
         [
          5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8],
         [
          2, 3, 11, 10, 6, 5],
         [
          11, 0, 8, 11, 2, 0, 10, 6, 5],
         [
          0, 1, 9, 2, 3, 11, 5, 10, 6],
         [
          5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11],
         [
          6, 3, 11, 6, 5, 3, 5, 1, 3],
         [
          0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6],
         [
          3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9],
         [
          6, 5, 9, 6, 9, 11, 11, 9, 8],
         [
          5, 10, 6, 4, 7, 8],
         [
          4, 3, 0, 4, 7, 3, 6, 5, 10],
         [
          1, 9, 0, 5, 10, 6, 8, 4, 7],
         [
          10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4],
         [
          6, 1, 2, 6, 5, 1, 4, 7, 8],
         [
          1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7],
         [
          8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6],
         [
          7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9],
         [
          3, 11, 2, 7, 8, 4, 10, 6, 5],
         [
          5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11],
         [
          0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6],
         [
          9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6],
         [
          8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6],
         [
          5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11],
         [
          0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7],
         [
          6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9],
         [
          10, 4, 9, 6, 4, 10],
         [
          4, 10, 6, 4, 9, 10, 0, 8, 3],
         [
          10, 0, 1, 10, 6, 0, 6, 4, 0],
         [
          8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10],
         [
          1, 4, 9, 1, 2, 4, 2, 6, 4],
         [
          3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4],
         [
          0, 2, 4, 4, 2, 6],
         [
          8, 3, 2, 8, 2, 4, 4, 2, 6],
         [
          10, 4, 9, 10, 6, 4, 11, 2, 3],
         [
          0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6],
         [
          3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10],
         [
          6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1],
         [
          9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3],
         [
          8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1],
         [
          3, 11, 6, 3, 6, 0, 0, 6, 4],
         [
          6, 4, 8, 11, 6, 8],
         [
          7, 10, 6, 7, 8, 10, 8, 9, 10],
         [
          0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10],
         [
          10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0],
         [
          10, 6, 7, 10, 7, 1, 1, 7, 3],
         [
          1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7],
         [
          2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9],
         [
          7, 8, 0, 7, 0, 6, 6, 0, 2],
         [
          7, 3, 2, 6, 7, 2],
         [
          2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7],
         [
          2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7],
         [
          1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11],
         [
          11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1],
         [
          8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6],
         [
          0, 9, 1, 11, 6, 7],
         [
          7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0],
         [
          7, 11, 6],
         [
          7, 6, 11],
         [
          3, 0, 8, 11, 7, 6],
         [
          0, 1, 9, 11, 7, 6],
         [
          8, 1, 9, 8, 3, 1, 11, 7, 6],
         [
          10, 1, 2, 6, 11, 7],
         [
          1, 2, 10, 3, 0, 8, 6, 11, 7],
         [
          2, 9, 0, 2, 10, 9, 6, 11, 7],
         [
          6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8],
         [
          7, 2, 3, 6, 2, 7],
         [
          7, 0, 8, 7, 6, 0, 6, 2, 0],
         [
          2, 7, 6, 2, 3, 7, 0, 1, 9],
         [
          1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6],
         [
          10, 7, 6, 10, 1, 7, 1, 3, 7],
         [
          10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8],
         [
          0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7],
         [
          7, 6, 10, 7, 10, 8, 8, 10, 9],
         [
          6, 8, 4, 11, 8, 6],
         [
          3, 6, 11, 3, 0, 6, 0, 4, 6],
         [
          8, 6, 11, 8, 4, 6, 9, 0, 1],
         [
          9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6],
         [
          6, 8, 4, 6, 11, 8, 2, 10, 1],
         [
          1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6],
         [
          4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9],
         [
          10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3],
         [
          8, 2, 3, 8, 4, 2, 4, 6, 2],
         [
          0, 4, 2, 4, 6, 2],
         [
          1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8],
         [
          1, 9, 4, 1, 4, 2, 2, 4, 6],
         [
          8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1],
         [
          10, 1, 0, 10, 0, 6, 6, 0, 4],
         [
          4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3],
         [
          10, 9, 4, 6, 10, 4],
         [
          4, 9, 5, 7, 6, 11],
         [
          0, 8, 3, 4, 9, 5, 11, 7, 6],
         [
          5, 0, 1, 5, 4, 0, 7, 6, 11],
         [
          11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5],
         [
          9, 5, 4, 10, 1, 2, 7, 6, 11],
         [
          6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5],
         [
          7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2],
         [
          3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6],
         [
          7, 2, 3, 7, 6, 2, 5, 4, 9],
         [
          9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7],
         [
          3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0],
         [
          6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8],
         [
          9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7],
         [
          1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4],
         [
          4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10],
         [
          7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10],
         [
          6, 9, 5, 6, 11, 9, 11, 8, 9],
         [
          3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5],
         [
          0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11],
         [
          6, 11, 3, 6, 3, 5, 5, 3, 1],
         [
          1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6],
         [
          0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10],
         [
          11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5],
         [
          6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3],
         [
          5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2],
         [
          9, 5, 6, 9, 6, 0, 0, 6, 2],
         [
          1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8],
         [
          1, 5, 6, 2, 1, 6],
         [
          1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6],
         [
          10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0],
         [
          0, 3, 8, 5, 6, 10],
         [
          10, 5, 6],
         [
          11, 5, 10, 7, 5, 11],
         [
          11, 5, 10, 11, 7, 5, 8, 3, 0],
         [
          5, 11, 7, 5, 10, 11, 1, 9, 0],
         [
          10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1],
         [
          11, 1, 2, 11, 7, 1, 7, 5, 1],
         [
          0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11],
         [
          9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7],
         [
          7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2],
         [
          2, 5, 10, 2, 3, 5, 3, 7, 5],
         [
          8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5],
         [
          9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2],
         [
          9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2],
         [
          1, 3, 5, 3, 7, 5],
         [
          0, 8, 7, 0, 7, 1, 1, 7, 5],
         [
          9, 0, 3, 9, 3, 5, 5, 3, 7],
         [
          9, 8, 7, 5, 9, 7],
         [
          5, 8, 4, 5, 10, 8, 10, 11, 8],
         [
          5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0],
         [
          0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5],
         [
          10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4],
         [
          2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8],
         [
          0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11],
         [
          0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5],
         [
          9, 4, 5, 2, 11, 3],
         [
          2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4],
         [
          5, 10, 2, 5, 2, 4, 4, 2, 0],
         [
          3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9],
         [
          5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2],
         [
          8, 4, 5, 8, 5, 3, 3, 5, 1],
         [
          0, 4, 5, 1, 0, 5],
         [
          8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5],
         [
          9, 4, 5],
         [
          4, 11, 7, 4, 9, 11, 9, 10, 11],
         [
          0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11],
         [
          1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11],
         [
          3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4],
         [
          4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2],
         [
          9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3],
         [
          11, 7, 4, 11, 4, 2, 2, 4, 0],
         [
          11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4],
         [
          2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9],
         [
          9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7],
         [
          3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10],
         [
          1, 10, 2, 8, 7, 4],
         [
          4, 9, 1, 4, 1, 7, 7, 1, 3],
         [
          4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1],
         [
          4, 0, 3, 7, 4, 3],
         [
          4, 8, 7],
         [
          9, 10, 8, 10, 11, 8],
         [
          3, 0, 9, 3, 9, 11, 11, 9, 10],
         [
          0, 1, 10, 0, 10, 8, 8, 10, 11],
         [
          3, 1, 10, 11, 3, 10],
         [
          1, 2, 11, 1, 11, 9, 9, 11, 8],
         [
          3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9],
         [
          0, 2, 11, 8, 0, 11],
         [
          3, 2, 11],
         [
          2, 3, 8, 2, 8, 10, 10, 8, 9],
         [
          9, 10, 2, 0, 9, 2],
         [
          2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8],
         [
          1, 10, 2],
         [
          1, 3, 8, 9, 1, 8],
         [
          0, 9, 1],
         [
          0, 3, 8], []]
        edgeShifts = np.array([
         [
          0, 0, 0, 0],
         [
          1, 0, 0, 1],
         [
          0, 1, 0, 0],
         [
          0, 0, 0, 1],
         [
          0, 0, 1, 0],
         [
          1, 0, 1, 1],
         [
          0, 1, 1, 0],
         [
          0, 0, 1, 1],
         [
          0, 0, 0, 2],
         [
          1, 0, 0, 2],
         [
          1, 1, 0, 2],
         [
          0, 1, 0, 2]],
          dtype=(np.uint16))
        nTableFaces = np.array([len(f) / 3 for f in triTable], dtype=(np.ubyte))
        faceShiftTables = [None]
        for i in range(1, 6):
            faceTableI = np.zeros((len(triTable), i * 3), dtype=(np.ubyte))
            faceTableInds = np.argwhere(nTableFaces == i)
            faceTableI[faceTableInds[:, 0]] = np.array([triTable[j] for j in faceTableInds])
            faceTableI = faceTableI.reshape((len(triTable), i, 3))
            faceShiftTables.append(edgeShifts[faceTableI])

        IsosurfaceDataCache = (
         faceShiftTables, edgeShifts, edgeTable, nTableFaces)
    else:
        faceShiftTables, edgeShifts, edgeTable, nTableFaces = IsosurfaceDataCache
    mask = data < level
    index = np.zeros([x - 1 for x in data.shape], dtype=(np.ubyte))
    fields = np.empty((2, 2, 2), dtype=object)
    slices = [slice(0, -1), slice(1, None)]
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                fields[(i, j, k)] = mask[(slices[i], slices[j], slices[k])]
                vertIndex = i - 2 * j * i + 3 * j + 4 * k
                index += fields[(i, j, k)] * 2 ** vertIndex

    cutEdges = np.zeros(([x + 1 for x in index.shape] + [3]), dtype=(np.uint32))
    edges = edgeTable[index]
    for i, shift in enumerate(edgeShifts[:12]):
        slices = [slice(shift[j], cutEdges.shape[j] + (shift[j] - 1)) for j in range(3)]
        cutEdges[(slices[0], slices[1], slices[2], shift[3])] += edges & 2 ** i

    m = cutEdges > 0
    vertexInds = np.argwhere(m)
    vertexes = vertexInds[:, :3].astype(np.float32)
    dataFlat = data.reshape(data.shape[0] * data.shape[1] * data.shape[2])
    cutEdges[(vertexInds[:, 0], vertexInds[:, 1], vertexInds[:, 2], vertexInds[:, 3])] = np.arange(vertexInds.shape[0])
    for i in (0, 1, 2):
        vim = vertexInds[:, 3] == i
        vi = vertexInds[vim, :3]
        viFlat = (vi * (np.array(data.strides[:3]) // data.itemsize)[np.newaxis, :]).sum(axis=1)
        v1 = dataFlat[viFlat]
        v2 = dataFlat[(viFlat + data.strides[i] // data.itemsize)]
        vertexes[(vim, i)] += (level - v1) / (v2 - v1)

    nFaces = nTableFaces[index]
    totFaces = nFaces.sum()
    faces = np.empty((totFaces, 3), dtype=(np.uint32))
    ptr = 0
    cs = np.array(cutEdges.strides) // cutEdges.itemsize
    cutEdges = cutEdges.flatten()
    for i in range(1, 6):
        cells = np.argwhere(nFaces == i)
        if cells.shape[0] == 0:
            continue
        cellInds = index[(cells[:, 0], cells[:, 1], cells[:, 2])]
        verts = faceShiftTables[i][cellInds]
        verts[..., :3] += cells[:, np.newaxis, np.newaxis, :]
        verts = verts.reshape((verts.shape[0] * i,) + verts.shape[2:])
        verts = (verts * cs[np.newaxis, np.newaxis, :]).sum(axis=2)
        vertInds = cutEdges[verts]
        nv = vertInds.shape[0]
        faces[ptr:ptr + nv] = vertInds
        ptr += nv

    return (
     vertexes, faces)


def invertQTransform(tr):
    """Return a QTransform that is the inverse of *tr*.
    Rasises an exception if tr is not invertible.
    
    Note that this function is preferred over QTransform.inverted() due to
    bugs in that method. (specifically, Qt has floating-point precision issues
    when determining whether a matrix is invertible)
    """
    try:
        import numpy.linalg
        arr = np.array([[tr.m11(), tr.m12(), tr.m13()], [tr.m21(), tr.m22(), tr.m23()], [tr.m31(), tr.m32(), tr.m33()]])
        inv = numpy.linalg.inv(arr)
        return QtGui.QTransform(inv[(0, 0)], inv[(0, 1)], inv[(0, 2)], inv[(1, 0)], inv[(1,
                                                                                         1)], inv[(1,
                                                                                                   2)], inv[(2,
                                                                                                             0)], inv[(2,
                                                                                                                       1)])
    except ImportError:
        inv = tr.inverted()
        if inv[1] is False:
            raise Exception('Transform is not invertible.')
        return inv[0]


def pseudoScatter(data, spacing=None, shuffle=True, bidir=False):
    """
    Used for examining the distribution of values in a set. Produces scattering as in beeswarm or column scatter plots.
    
    Given a list of x-values, construct a set of y-values such that an x,y scatter-plot
    will not have overlapping points (it will look similar to a histogram).
    """
    inds = np.arange(len(data))
    if shuffle:
        np.random.shuffle(inds)
    data = data[inds]
    if spacing is None:
        spacing = 2.0 * np.std(data) / len(data) ** 0.5
    s2 = spacing ** 2
    yvals = np.empty(len(data))
    if len(data) == 0:
        return yvals
    yvals[0] = 0
    for i in range(1, len(data)):
        x = data[i]
        x0 = data[:i]
        y0 = yvals[:i]
        y = 0
        dx = (x0 - x) ** 2
        xmask = dx < s2
        if xmask.sum() > 0:
            if bidir:
                dirs = [
                 -1, 1]
            else:
                dirs = [
                 1]
            yopts = []
            for direction in dirs:
                y = 0
                dx2 = dx[xmask]
                dy = (s2 - dx2) ** 0.5
                limits = np.empty((2, len(dy)))
                limits[0] = y0[xmask] - dy
                limits[1] = y0[xmask] + dy
                while True:
                    if direction > 0:
                        mask = limits[1] >= y
                    else:
                        mask = limits[0] <= y
                    limits2 = limits[:, mask]
                    mask = (limits2[0] < y) & (limits2[1] > y)
                    if mask.sum() == 0:
                        break
                    if direction > 0:
                        y = limits2[:, mask].max()
                    else:
                        y = limits2[:, mask].min()

                yopts.append(y)

            if bidir:
                y = yopts[0] if -yopts[0] < yopts[1] else yopts[1]
            else:
                y = yopts[0]
        yvals[i] = y

    return yvals[np.argsort(inds)]


def toposort(deps, nodes=None, seen=None, stack=None, depth=0):
    """Topological sort. Arguments are:
      deps    dictionary describing dependencies where a:[b,c] means "a depends on b and c"
      nodes   optional, specifies list of starting nodes (these should be the nodes 
              which are not depended on by any other nodes). Other candidate starting
              nodes will be ignored.
              
    Example::

        # Sort the following graph:
        # 
        #   B ──┬─────> C <── D
        #       │       │       
        #   E <─┴─> A <─┘
        #     
        deps = {'a': ['b', 'c'], 'c': ['b', 'd'], 'e': ['b']}
        toposort(deps)
         => ['b', 'd', 'c', 'a', 'e']
    """
    deps = deps.copy()
    for k, v in list(deps.items()):
        for k in v:
            if k not in deps:
                deps[k] = []

    if nodes is None:
        rem = set()
        for dep in deps.values():
            rem |= set(dep)

        nodes = set(deps.keys()) - rem
    if seen is None:
        seen = set()
        stack = []
    sorted = []
    for n in nodes:
        if n in stack:
            raise Exception('Cyclic dependency detected', stack + [n])
        if n in seen:
            continue
        seen.add(n)
        sorted.extend(toposort(deps, (deps[n]), seen, (stack + [n]), depth=(depth + 1)))
        sorted.append(n)

    return sorted