# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/ mad/CASC4DE/CODES/EUFTICR-NB/spike/NPKData.py
# Compiled at: 2020-04-15 08:30:57
# Size of source mod 2**32: 120923 bytes
"""
NPKData.py

Implement the basic mechanisms for spectral data-sets

First version created by Marc-André and Marie-Aude on 2010-03-17.
"""
from __future__ import print_function, division
import os, numpy as np
import numpy.fft as npfft
import copy, itertools as it, unittest, math, re, time, warnings, inspect
from . import version
from .NPKError import NPKError
from util.signal_tools import findnoiselevel_2D
import sys
if sys.version_info[0] < 3:
    pass
else:
    xrange = range

def hypercomplex_modulus(arr, size1, size2):
    """
    Calculates the modulus of an array of hypercomplex numbers.
    input:
        arr : hypercomplex array
        size1 : size counting horizontally each half quadrant.
        size2 : siez counting vertically each half quadrant.

    eg:
        arr = np.array([[1, 4],[3, 7],[1, 9],[5, 7]])
        is an hypercomplex with size1 = 2 and size2 = 2
    """
    b = np.zeros((size1 // 2, size2 // 2))
    brr = arr[::2, ::2]
    bri = arr[::2, 1::2]
    bir = arr[1::2, ::2]
    bii = arr[1::2, 1::2]
    b = np.sqrt(brr ** 2 + bri ** 2 + bir ** 2 + bii ** 2)
    return b


def as_cpx(arr):
    """
    interpret arr as a complex array
    useful to move between complex and real arrays (see as_float)
    
    >>> print as_cpx(np.arange(4.0))
    [ 0.+1.j  2.+3.j]
    
    """
    return arr.view(dtype='complex')


def as_float(arr):
    """
    interpret arr as a float array
    useful to move between complex and real arrays (see as_float)

    >>> print as_float(np.arange(4)*(1+1j))
    [ 0.  0.  1.  1.  2.  2.  3.  3.]
    """
    return arr.view(dtype='float')


def conj_ip(a):
    """
    computes conjugate() in-place

    >>> conj_ip(np.arange(4)*(1+1j))
    [ 0.-0.j  1.-1.j  2.-2.j  3.-3.j]
    """
    if a.dtype == np.complex:
        b = as_float(a)[1::2]
        np.multiply(b, -1.0, b)
    return a


def _conj_ip_from_float(a):
    return np.conjugate(a.view(dtype='complex'))


def _conj_ip_to_float(a):
    return np.conjugate(a).view(dtype='float')


def _base_fft(a):
    """
    should not be used for regular use - called by wrapper routines
    
    computes the complex Fourier transform, the NMR way
    built as the conjugate of the fft found in numpy 
    
    WARNING - destroy the buffer given as parameter
    
    test : 
    >> print _base_fft(np.arange(4.0))
    [ 2.  4. -2. -2.]
    
    """
    return _conj_ip_to_float(npfft.fft(_conj_ip_from_float(a)))


def _base_ifft(a):
    """
    should not be used for regular use - called by wrapper routines

    computes the inverse complex Fourier transform, the NMR way
    built as the conjugate of the ifft found in numpy 

    WARNING - destroy the buffer given as parameter

    test : 
    >> print _base_ifft(np.arange(4.0))
    array([ 1.,  2., -1., -1.])

    """
    v = npfft.ifft(conj_ip(as_cpx(a)))
    return as_float(conj_ip(v))


def _base_rfft(a):
    """
    should not be used for regular use - called by wrapper routines
    
    imaginary parts of first and last freq is zero ( [1] and [-1]) so they are dropped and rfft is inplace.
    This works only if self.size2 is even !!!

    test : 
    >> print _base_rfft(np.arange(4.0))
    [ 3.  1. -2. -2.]
    """
    v = as_float(npfft.rfft(as_float(a)))
    v[1] = 0.5 * v[(-2)]
    v[0] *= 0.5
    return as_float(conj_ip(as_cpx(v[:-2])))


def _base_irfft(a):
    """
    should not be used for regular use - called by wrapper routines
    
    inverse of _base_rfft
    This works only if self.size2 is even !!!

    test : 
    >> print _base_irfft(np.arange(4.0))
    [ 0.5,  2. , -1.5, -1. ]
    """
    v = np.zeros(len(a) + 2)
    v[:-2] = as_float(conj_ip(as_cpx(a[:])))
    v[0] = 2 * v[0]
    v[-2] = 2 * v[1]
    v[1] = 0.0
    return npfft.irfft(as_cpx(v))


def _base_fftr(a):
    """
    should not be used for regular use - called by wrapper routines

    complex to real direct FT
    This works only if self.size2 is even !!!

    test : 
    >> print _base_fftr(np.arange(4.0))
    [ 2.0, -3.0, -2.0, 3.0 ]
    >> print _base_fftr(np.arange(8.0)+1.0)
    [16.0, -16.31, 0.0, 1.34, -4.0, 6.313, -8.0, 12.65]

    """
    v = np.zeros(len(a) + 2)
    v[:-2] = a[:]
    v[0] = 2 * v[0]
    v[-2] = 2 * v[1]
    v[-2] = 0.0
    v = npfft.irfft(as_cpx(v))
    return v * (len(v) / 2)


def _base_ifftr(a):
    """
    should not be used for regular use - called by wrapper routines

    inverse of fftr

    test : 
    >> print _base_ifftr(np.arange(4.0))
    [ 1.5,  0.5, -1.0, -1.0 ]
    >> print _base_ifftr(np.arange(8.0)+1.0)
    [4.5, 0.5, -1.0, 2.41, -1.0, 1.0, -1.0, 0.414]
    """
    v = as_float(npfft.rfft(as_float(a)))
    v[1] = 0.5 * v[(-2)]
    v[0] *= 0.5
    return v[:-2] * (2.0 / (len(v) - 2))


def flatten(*arg):
    """
    flatten recursively a list of lists

    >>>print flatten( ( (1,2), 3, (4, (5,), (6,7) ) ) )
    [1, 2, 3, 4, 5, 6, 7]
    """
    import collections
    r = []
    for i in arg:
        if isinstance(i, collections.Sequence):
            for j in i:
                r += flatten(j)

        else:
            r += [i]

    return r


def warning(msg):
    """issue a warning message to the user"""
    print('WARNING')
    print(msg)


def ident(v):
    """a identity function used by default converter"""
    return v


class Unit(object):
    __doc__ = '\n    a small class to hold parameters for units\n    name: the name of the "unit"\n    converter: a function converting from points to "unit"\n    bconverter: a function converting from "unit" to points\n    reverse: direction in which axis are displayed (True means right to left)\n    scale: scale along this axis, possible values are \'linear\' or \'log\'\n    \n    '

    def __init__(self, name='points', converter=ident, bconverter=ident, reverse=False, scale='linear'):
        """creates an 'points' methods - to be extended"""
        self.name = name
        self.converter = converter
        self.bconverter = bconverter
        self.reverse = reverse
        self.scale = scale


class Axis(object):
    __doc__ = '\n    hold information for one spectral axis\n    used internally - a template for other axis types\n    '

    def __init__(self, size=64, itype=0, currentunit='points'):
        """
        size        number of points along axis
        itype       0 == real, 1 == complex
        currentunit       string which hold the unit name (defaut is "points", also called index)
                                    
        """
        self.size = size
        self.itype = itype
        self.units = {'points': Unit()}
        self.currentunit = currentunit
        self.sampling = None
        self.sampling_info = {}
        self.kind = 'generic'
        self.attributes = ['kind', 'itype', 'sampling']

    @property
    def borders(self):
        """the (min, max) available windows, used typically for display"""
        return (
         0, self.size - 1)

    @property
    def cpxsize(self):
        """returns size of complex entries
        this is different from size, 
        size == cpxsize if axis is real
        size == 2*cpxsize if axis is complex
        """
        return self.size // (self.itype + 1)

    def report(self):
        if self.sampling:
            return 'size : %d   sampled from %d   itype %d   unit %s' % (self.size, max(self.sampling), self.itype, self.currentunit)
        return 'size : %d   itype %d   currentunit %s' % (self.size, self.itype, self.currentunit)

    def _report(self):
        """low level full-report"""
        st = [
         'Stored attributes:\n'] + ['  %s: %s\n' % (att, getattr(self, att)) for att in self.attributes]
        st += ['other attributes:\n'] + ['  %s: %s\n' % (att, getattr(self, att)) for att in self.__dict__ if att not in self.attributes + ['attributes', 'units']]
        st += ['  units: '] + [' %s' % k for k in self.units.keys()]
        return ''.join(st)

    def typestr(self):
        """ returns its type (real or complex) as a string"""
        if self.itype == 1:
            tt = 'complex'
        else:
            tt = 'real'
        return tt

    def copy(self):
        return copy.deepcopy(self)

    def getslice(self, zoom):
        """
        given a zoom window (or any slice), given as (low,high) in CURRENT UNIT,
        
        returns the value pair in index, as (star,end)                
        which insures that
        -  low<high and within axis size
        -  that it starts on a real index if itype is complex
        -  that it fits in the data-set
        raise error if not possible
        """
        if len(zoom) != 2:
            raise NPKError("slice should be defined as coordinate pair (left,right) in axis' current unit %s" % self.currentunit)
        a = int(round(float(self.ctoi(zoom[0]))))
        b = int(round(float(self.ctoi(zoom[1]))))
        if self.itype == 1:
            a = 2 * (a // 2)
            b = 2 * (b // 2)
        left, right = min(a, b), max(a, b) + 1
        if self.itype == 1:
            right += 1
        l = max(0, left)
        l = min(self.size - 5, l)
        r = max(4, left)
        r = min(self.size - 1, right)
        return (
         l, r)

    def check_zoom(self, zoom):
        """
        check whether a zoom window (or any slice), given as (low,high) is valid
        - check low<high and within axis size
        - check that it starts on a real index if itype is complex
        return a boolean
        """
        test = zoom[0] >= 0 and zoom[0] <= self.size
        test = test and zoom[1] >= 0 and zoom[1] <= self.size
        test = test and zoom[0] <= zoom[1]
        if self.itype == 1:
            test = test and zoom[0] % 2 == 0 and zoom[1] % 2 == 1
        return test

    def extract(self, zoom):
        """
        redefines the axis parameters so that the new axis is extracted for the points [start:end] 
        
        zoom is given in current unit - does not modify the Data, only the axis definition
        
        This definition should be overloaded for each new axis, as the calibration system, associated to unit should be updated.
        
        """
        start, end = self.getslice(zoom)
        return (
         start, end)

    def load_sampling(self, filename):
        """
        loads the sampling scheme contained in an external file
        file should contain index values, one per line, comment lines start with a #
        complex axes should be sampled by complex pairs, and indices go up to self.size1/2
        
        sampling is loaded into self.sampling  and self.sampling_info is a dictionnary with information
        """
        from .Algo import CS_transformations as cstr
        S = cstr.sampling_load(filename)
        self.sampling = S[0]
        self.sampling_info = S[1]

    def get_sampling(self):
        """returns the sampling scheme contained in current axis"""
        return self.sampling

    def set_sampling(self, sampling):
        """sets the sampling scheme contained in current axis"""
        self.sampling = sampling
        return self.sampling

    @property
    def sampled(self):
        """true is sampled axis"""
        return self.sampling is not None

    def _gcurunits(self):
        """get the current unit for this axis, to be chosen in axis.units.keys()"""
        return self._currentunit

    def _scurunits(self, currentunit):
        """set the current unit for this axis, to be chosen in axis.units.keys()"""
        if currentunit not in self.units.keys():
            raise NPKError('Wrong unit type: %s - valid units are : %s' % (currentunit, str(self.units.keys())))
        self._currentunit = currentunit

    currentunit = property(_gcurunits, _scurunits)

    def points_axis(self):
        """return axis in points currentunit, actually 0..size-1"""
        return np.arange(self.size)

    def unit_axis(self):
        """returns an axis in the unit defined in self.currentunit"""
        return self.itoc(self.points_axis())

    def itoc(self, val):
        """
        converts point value (i) to currentunit (c)
        """
        f = self.units[self.currentunit].converter
        return f(val)

    def ctoi(self, val):
        """
        converts into point value (i) from currentunit (c)
        """
        f = self.units[self.currentunit].bconverter
        return f(val)


class TimeAxis(Axis):
    __doc__ = '\n    Not implmented yet\n    hold information for one sampled time axis (such as chromato of T2 relax)\n    time values should be given as a list of values \n    '

    def __init__(self, size=32, tabval=None, importunit='sec', currentunit='sec', scale='linear'):
        """
        tabval is a list of time values, values should be in seconds
              can be set latter on directly or using TimeAxis.load_tabval()
        importunit is the unit in the tabval series
        currentunit is for display
        unit are chosen in ('msec', sec', 'min', 'hours')
        scale is either 'linear' or 'log'
        """
        super(TimeAxis, self).__init__(size=size, itype=0)
        self.Time = 'Time'
        self.kind = 'Time'
        self.fval = lambda x: 1.0
        self.fm1val = lambda x: 1.0
        if tabval is not None:
            self.tabval = np.array(tabval)
        else:
            self.tabval = np.arange(size)
        if importunit != 'sec':
            if importunit == 'msec':
                self.tabval = self.mstos(self.tabval)
            else:
                if importunit == 'min':
                    self.tabval = self.mtos(self.tabval)
                else:
                    if importunit == 'hours':
                        self.tabval = self.htos(self.tabval)
                    else:
                        raise ValueError
        self.comp_interpolate()
        self.units['msec'] = Unit(name='millisec', converter=(self.itoms), bconverter=(self.mstoi), scale='linear')
        self.units['sec'] = Unit(name='second', converter=(self.itos), bconverter=(self.stoi), scale='linear')
        self.units['min'] = Unit(name='minutes', converter=(self.itom), bconverter=(self.mtoi), scale='linear')
        self.units['hours'] = Unit(name='hours', converter=(self.itoh), bconverter=(self.htoi), scale='linear')
        for i in ('Time', 'tabval'):
            self.attributes.append(i)

        self.currentunit = currentunit
        if scale == 'log':
            self.set_logdisplay()

    @property
    def Tmin(self):
        """smaller tabulated time value"""
        return self.tabval.min()

    @property
    def Tmax(self):
        """larger tabulated time value"""
        return self.tabval.max()

    def set_logdisplay(self):
        """set display in log spacing"""
        for unit in self.units.keys():
            self.units[unit].scale = 'log'

    def set_lindisplay(self):
        """set display in linear spacing"""
        for unit in self.units.keys():
            self.units[unit].scale = 'linear'

    def itos(self, value):
        """
        returns time from point value (i) - interpolated if possible
        """
        d = self.fval(value)
        return d

    def stoi(self, value):
        """
        returns point value (i) from time - interpolated if possible
        """
        d = self.fm1val(value)
        return d

    def mstoi(self, value):
        """millisec to index"""
        return self.stoi(value / 1000.0)

    def mtoi(self, value):
        """minutes to index"""
        return self.stoi(value * 60.0)

    def htoi(self, value):
        """hours to index"""
        return self.stoi(value * 3600.0)

    def itoms(self, value):
        """index to millisec"""
        return self.itos(value) * 1000.0

    def itom(self, value):
        """index to minutes"""
        return self.itos(value) / 60.0

    def itoh(self, value):
        """index to hours"""
        return self.itos(value) / 3600.0

    def stoms(self, value):
        return value * 1000.0

    def stom(self, value):
        return value / 60.0

    def stoh(self, value):
        return value / 3600.0

    def mstos(self, value):
        return value / 1000.0

    def mtos(self, value):
        return value * 60.0

    def htos(self, value):
        return value * 3600.0

    def report(self):
        """hight level report"""
        return 'Time sampled axis of %d points,  from %f sec to %f sec ' % (
         self.size, self.Tmin, self.Tmax)

    def load_tabval(self, fname, importunit='sec'):
        """
        load tabulated time values form a file - plain text, one entry per line

        importunit is the unit in the tabval series
        unit is chosen in ('msec', sec', 'min', 'hours')
        """
        from scipy.interpolate import interp1d
        with open(fname, 'r') as (F):
            self.tabval = np.array([float(l) for l in F.readlines() if not l.startswith('#')])
        self.comp_interpolate()
        if importunit != 'sec':
            if importunit == 'msec':
                self.tabval = self.mstos(self.tabval)
            else:
                if importunit == 'min':
                    self.tabval = self.mtos(self.tabval)
                else:
                    if importunit == 'hours':
                        self.tabval = self.htos(self.tabval)
                    else:
                        raise ValueError
        return self.tabval

    def comp_interpolate(self):
        """computes an interpolater if possible"""
        from scipy.interpolate import interp1d
        if self.tabval is not None:
            is_sorted = np.diff(self.tabval).all() >= 0.0
            self.fval = interp1d((np.arange(len(self.tabval))), (self.tabval), kind='quadratic',
              assume_sorted=is_sorted,
              fill_value='extrapolate')
            self.fm1val = interp1d((self.tabval), (np.arange(len(self.tabval))), kind='quadratic',
              assume_sorted=is_sorted,
              fill_value='extrapolate')
        return self.fval


class LaplaceAxis(Axis):
    __doc__ = '\n    hold information for one Laplace axis (such as DOSY)\n    used internally\n    '

    def __init__(self, size=64, dmin=1.0, dmax=10.0, dfactor=1.0, currentunit='damping'):
        super(LaplaceAxis, self).__init__(size=size, itype=0)
        self.dmin = dmin
        self.dmax = dmax
        self.dfactor = dfactor
        self.Laplace = 'Laplace'
        self.kind = 'Laplace'
        self.units['damping'] = Unit(name='damping', converter=(self.itod), bconverter=(self.dtoi), scale='log')
        self.units['Diff'] = self.units['damping']
        for i in ('dmin', 'dmax', 'dfactor', 'Laplace'):
            self.attributes.append(i)

        self.currentunit = currentunit
        self.qvalues = None

    def itod(self, value):
        """
        returns damping value (d) from point value (i)
        """
        cst = (math.log(self.dmax) - math.log(self.dmin)) / (float(self.size) - 1)
        d = self.dmin * np.exp(cst * value)
        return d

    def dtoi(self, value):
        """
        returns point value (i) from damping value (d)
        """
        cst = (math.log(self.dmax) - math.log(self.dmin)) / (float(self.size) - 1)
        i = np.log(value / self.dmin) / cst
        return i

    def D_axis(self):
        """return axis containing Diffusion values, can be used for display"""
        return self.itod(self.points_axis())

    def report(self):
        """hight level report"""
        return 'Laplace axis of %d points,  from %f to %f  using a scaling factor of %f' % (
         self.size, self.itod(0.0), self.itod(self.size - 1), self.dfactor)

    def load_qvalues(self, fname):
        """
        doc
        """
        with open(fname, 'r') as (F):
            self.qvalues = np.array([float(l) for l in F.readlines() if not l.startswith('#')])
        return self.qvalues


def copyaxes(inp, out):
    """
    copy axes values from NPKDAta in to out.
   
    internal use
    """
    for ii in range(inp.dim):
        i = ii + 1
        setattr(out, 'axis%1d' % i, inp.axes(i).copy())


def parsezoom(npkd, zoom):
    """
    takes zoom (in currentunit) for NPKData npkd, and return either
    in 1D : zlo, zup    
    in 2D : z1lo, z1up, z2lo, z2up
    if zoom is None, it returns the full zone
    """
    if npkd.dim == 1:
        if zoom is not None:
            z1lo, z1up = npkd.axis1.getslice(zoom)
        else:
            z1lo, z1up = npkd.axis1.borders
        return (
         z1lo, z1up)
    if npkd.dim == 2:
        if zoom is not None:
            zz = flatten(zoom)
            z1lo, z1up = npkd.axis1.getslice((zz[0], zz[1]))
            z2lo, z2up = npkd.axis2.getslice((zz[2], zz[3]))
        else:
            z1lo, z1up = npkd.axis1.borders
            z2lo, z2up = npkd.axis2.borders
        return (z1lo, z1up, z2lo, z2up)
    raise Exception('this code is not done yet')


def NPKData_plugin(name, method, verbose=False):
    """
    This function allows to register a new method inside the NPKData class.
    
    for instance - define myfunc() anywhere in your code :

    def myfunc(npkdata, args):
        "myfunc doc"
        ...do whatever, assuming npkdata is a NPKData
        return npkdata     # THIS is important, that is the standard NPKData mechanism
    
    then elsewhere do :
    NPKData_plugin("mymeth", myfunc)
    
    then all NPKData created will have the method .mymeth()
    
    look at .plugins/__init__.py for details
    """
    from . import plugins
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 1)
    callerfile = calframe[1][1]
    pluginfile = os.path.splitext(os.path.basename(callerfile))[0]
    if not callable(method):
        raise Exception('method should be callable')
    if not isinstance(name, str):
        raise Exception('method name should be a string')
    setattr(_NPKData, name, method)
    if verbose:
        print('   - successfully added .%s() method to NPKData' % name)
    plugins.codes[pluginfile].append(name)


def NPKData(*arg, **kw):
    """trick to insure compatibility for modified code"""
    from . import NMR
    print('******************************************************************************', file=(sys.stderr))
    print('* Calling directly NPKData.NPKData() to create a new NMR dataset is obsolete *', file=(sys.stderr))
    print('* Please use NMR.NMRData() instead                                           *', file=(sys.stderr))
    print('******************************************************************************', file=(sys.stderr))
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe)[1]
    print(('in %s - %s line %s\n' % (calframe[1], calframe[3], calframe[2])), file=(sys.stderr))


class _NPKData(object):
    __doc__ = '\n    a working data used by the NPK package\n    \n    The data is a numpy array, found in self.buffer     can also be accessed directly d[i], d[i,j], ...\n    \n    1D 2D and 3D are handled, 3 axes are defined : axis1 axis2 axis3\n    axes are defined as in NMR\n    in 1D, every is in axis1\n    in 2D, the fastest varying dimension is in axis2, the slowest in axis1\n    in 3D, the fastest varying dimension is in axis3, the slowest in axis1\n    see axis_index\n    typical properties and methods are :\n    utilities:\n        .display() \n        .check()\n    properties\n        .itype\n        .dim .size1, .size2, .size3 ...\n    moving data :\n        .row(i) .col(i) .set_row(i)  .set_col(i)\n        .copy()\n        .load() .save()\n    processing :\n        .fft() .rfft() .modulus() .apod_xxx()  sg()  transpose() ...\n    arithmetics :\n        .fill() .mult .add()\n        also direct arithmetics : f = 2*d+e\n    all methods return self, so computation can be piped\n    etc...\n    '

    def __init__(self, dim=1, shape=None, buffer=None, debug=0):
        """
        data initialisation,
        four alternative posibilities :
        - name : file-name is given, the file is read and loaded
        - buffer : numpy buffer is given - used as is, not copied !
        - shape eg : (si1,si2) is given 
        - dim is given (default is dim=1)
        
        the first found takes over the others which are not used
        """
        self.debug = debug
        if shape is not None:
            dim = len(shape)
        elif buffer is not None:
            shape = buffer.shape
            dim = len(shape)
        elif dim == 1:
            if shape is None:
                shape = (64, )
            self.axis1 = Axis()
        else:
            if dim == 2:
                if shape is None:
                    shape = (64, 64)
                self.axis1 = Axis()
                self.axis2 = Axis()
            else:
                if dim == 3:
                    if shape is None:
                        shape = (64, 64, 64)
                    self.axis1 = Axis()
                    self.axis2 = Axis()
                    self.axis3 = Axis()
                else:
                    raise NPKError('invalid dimension')
        if buffer is None:
            buffer = np.zeros(shape)
        if self.debug:
            print('dim %d, shape %s, buffer %s' % (dim, shape, buffer.shape))
        self.buffer = buffer
        self.set_buffer(buffer)
        self.adapt_size()
        self.check()
        self._absmax = 0.0
        self.noise = 0.0
        self.name = 'no data'
        self.level = []

    def get_buffer(self, copy=False):
        """
        returns a view or a copy of the numpy buffer containing the NPKData values
        dtype is either real or complex if axis is complex.
        remarks :
         - default is a view, if you want a copy, simply do d.get_buffer(copy=True)
         - if you use a view, do not modify the size, nor the dtype
         - see set_buffer()
        WARNING
        - In nD with n>1 and if NPKData is hypercomplex, only the fastest (n) axis is considered, all other imaginary parts are left as real.
        """
        if self.axes(self.dim).itype == 1:
            buf = as_cpx(self.buffer)
        else:
            buf = self.buffer
        if copy:
            return buf.copy()
        return buf

    def set_buffer(self, buff):
        """
        modify the internal buffer of the NPKData.
        allows real or complex arrays to be used
        remarks
         - see get_buffer()
        """
        t = buff.shape
        if len(t) != self.dim:
            raise NPKError('set_buffer() cannot change the data dimension', data=self)
        else:
            try:
                dt = buff.dtype
            except:
                dt = np.float

            if dt == np.complex:
                buff = as_float(buff)
                self.axes(self.dim).itype = 1
            else:
                if dt == 'float':
                    self.axes(self.dim).itype = 0
        self.buffer = buff
        self._absmax = 0.0
        self.adapt_size()
        self.check()
        return self

    def axes(self, axis):
        """
        returns the required axis : 1, 2 or 3
        """
        return getattr(self, 'axis%1d' % axis)

    @property
    def dim(self):
        """returns the dimension of data : 1 2 or 3 (for 1D 2D or 3D)"""
        return len(self.buffer.shape)

    @property
    def cpxsize1(self):
        """
        returns the size of the F1 spectral axis in 1D 2D and 3D (number of entries, real or complex)
        i.e. the unique axis in 1D, the slowest axis in 2D and 3D
        """
        return self.axis1.cpxsize

    @property
    def cpxsize2(self):
        """
        returns the size of the F2 spectral axis in 2D and 3D  (number of entries, real or complex)
        i.e. the slowest axis in 2D and the intermediate in 3D
        """
        return self.axis2.cpxsize

    @property
    def cpxsize3(self):
        """
        returns the size of the F3 spectral axis in 3D  (number of entries, real or complex)
        i.e. the slowest axis in 3D
        """
        return self.axis3.cpxsize

    @property
    def size1(self):
        """
        returns the size of the F1 spectral axis in 1D 2D and 3D
        i.e. the unique axis in 1D, the slowest axis in 2D and 3D
        warning, if data along axis is complex, the size is twice the number of complex pairs
            i.e. this is the size of the underlying array
        """
        return self.axis1.size

    @property
    def size2(self):
        """
        returns the size of the F2 spectral axis in 2D and 3D
        i.e. the slowest axis in 2D and the intermediate in 3D
        warning, if data along axis is complex, the size is twice the number of complex pairs
            i.e. this is the size of the underlying array
        """
        return self.axis2.size

    @property
    def size3(self):
        """
        returns the size of the F3 spectral axis in 3D
        i.e. the slowest axis in 3D
        warning, if data along axis is complex, the size is twice the number of complex pairs
            i.e. this is the size of the underlying array
        """
        return self.axis3.size

    @property
    def itype(self):
        """returns complex type of each axes coded as single number, using NPKv1 code"""
        if self.dim == 1:
            t = self.axis1.itype
        else:
            if self.dim == 2:
                t = self.axis2.itype + 2 * self.axis1.itype
            else:
                if self.dim == 3:
                    t = self.axis3.itype + 2 * self.axis2.itype + 4 * self.axis1.itype
        return t

    def __getitem__(self, key):
        """
        allows d[i] where d is an NPKData
        will always return as if data is real, independently of itype
        """
        return self.buffer.__getitem__(key)

    def __setitem__(self, key, value):
        """
        allows d[i] where d is an NPKData
        will always set as if data is real, independently of itype
        """
        return self.buffer.__setitem__(key, value)

    def _gunits(self):
        """copy currentunit to all the axes"""
        return [self.axes(i + 1).currentunit for i in range(self.dim)]

    def _sunits(self, currentunit):
        for i in range(self.dim):
            ax = self.axes(i + 1)
            ax.currentunit = currentunit

    unit = property(_gunits, _sunits)

    def set_unit(self, currentunit):
        """
        a method equivalent to the unit property
        can be used in processing pipelines
        if currentunit is a list/tuple, each entries are applied to the different axes
        """
        if type(currentunit) not in (tuple, list):
            self._sunits(currentunit)
        else:
            if self.dim != len(currentunit):
                raise NPKError('dimension do not match')
            for i, u in zip(range(self.dim), currentunit):
                ax = self.axes(i + 1)
                ax.currentunit = u

        return self

    def check(self, warn=False):
        """
        check basic internal validity
        raises exceptions unless warn is set to True - in which case, only warnings are issued
        can be used in pipes as it returns self if everything is ok
        """

        def check_msg(string):
            if warn:
                warning('WARNING in NPKData.check() : ' + string)
            else:
                print(self.report())
                raise Exception(string)

        try:
            if not self.buffer.flags['OWNDATA']:
                if self.debug > 0:
                    warning('WARNING in NPKData.check() : NPKData does not own its buffer')
        except:
            pass

        try:
            if not self.buffer.flags['C_CONTIGUOUS']:
                if self.debug > 0:
                    warning('WARNING in NPKData.check() : NPKData does not own its buffer')
        except:
            pass

        try:
            dt = self.buffer.dtype
        except:
            dt = np.float

        if dt != np.float:
            check_msg('wrong buffer type : %s' % str(dt))
        else:
            if len(self.buffer.shape) != self.dim:
                check_msg('wrong dim value : %d while buffer is %d' % (self.dim, len(self.buffer.shape)))
            if self.dim == 1:
                if self.buffer.shape[0] != self.axis1.size:
                    check_msg('wrong size value : %d while buffer is %d' % (self.axis1.size, self.buffer.size))
            elif not self.dim == 2 or self.buffer.shape[0] != self.axis1.size or self.buffer.shape[1] != self.axis2.size:
                check_msg('wrong size value : %d x %d while buffer is %d x %d' % (
                 self.axis1.size, self.axis2.size, self.buffer.shape[0], self.buffer.shape[1]))
            else:
                pass
        if self.dim == 3:
            if self.buffer.shape[0] != self.axis1.size or self.buffer.shape[1] != self.axis2.size or self.buffer.shape[2] != self.axis3.size:
                check_msg('wrong size value : %d x %d x %d while buffer is %d x %d x %d' % (
                 self.axis1.size, self.axis2.size, self.axis3.size, self.buffer.shape[0], self.buffer.shape[1], self.buffer.shape[2]))
        for i in range(self.dim):
            if self.axes(i + 1).itype == 1 and self.axes(i + 1).size % 2 == 1:
                check_msg('axis %d as size and type mismatch : %d - %d' % (i, self.axes(i + 1).itype, self.axes(i + 1).size))

        return self

    def checknD(self, n):
        if self.dim != n:
            raise NPKError(('The dataset is not a %1dD experiment, as required' % n), data=self)
        else:
            return True

    def check1D(self):
        """true for a 1D"""
        self.checknD(1)

    def check2D(self):
        """true for a 2D"""
        self.checknD(2)

    def check3D(self):
        """true for a 3D"""
        self.checknD(3)

    def copy(self):
        """return a copy of itself"""
        Data = type(self)
        c = Data(buffer=(self.buffer.copy()))
        copyaxes(self, c)
        c.debug = self.debug
        c._absmax = self._absmax
        c.noise = self.noise
        c.name = self.name
        c.level = self.level
        try:
            c.params = copy.deepcopy(self.params)
        except AttributeError:
            pass

        return c

    def adapt_size(self):
        """
        adapt the sizes held in the axis objects to the size of the buffer
        TO BE CALLED each time the buffer size is modified
        otherwise strange things will happen
        """
        sizes = self.buffer.shape
        for i in range(self.dim):
            self.axes(i + 1).size = sizes[i]

        self.check()

    def _chsize1d(self, sz1=-1):
        """
        Change size of data, zero-fill or truncate.
        Only designed for time domain data.
        DO NOT change the value of spectroscopic units, so EXTRACT should 
        always be preferred on spectra (unless you know exactly what your are doing).
        """
        self.check1D()
        if sz1 == -1:
            sz1 = self.axis1.size
        elif sz1 <= self.size1:
            self.buffer = self.buffer[:sz1]
        else:
            b = np.zeros(sz1)
            b[:self.size1] = self.buffer
            self.buffer = b
        self.adapt_size()
        return self

    def _chsize2d(self, sz1=-1, sz2=-1):
        """
        Change size of data, zero-fill or truncate. 
        DO NOT change the value of OFFSET and SPECW, so EXTRACT should 
        always be preferred on spectra (unless you know exactly what your are doing).
        """
        self.check2D()
        if sz1 == -1:
            sz1 = self.axis1.size
        if sz2 == -1:
            sz2 = self.axis2.size
        b = np.zeros((sz1, sz2))
        s1 = min(sz1, self.size1)
        s2 = min(sz2, self.size2)
        b[:s1, :s2] = self.buffer[:s1, :s2]
        self.buffer = b
        self.adapt_size()
        return self

    def _chsize3d(self, sz1=-1, sz2=-1, sz3=-1):
        """
        Change size of data, zero-fill or truncate. 
        DO NOT change the value of OFFSET and SPECW, so EXTRACT should 
        always be preferred on spectra (unless you know exactly what your are doing).
        """
        self.check3D()
        if sz1 == -1:
            sz1 = self.axis1.size
        if sz2 == -1:
            sz2 = self.axis2.size
        if sz3 == -1:
            sz3 = self.axis3.size
        b = np.zeros((sz1, sz2, sz3))
        s1 = min(sz1, self.size1)
        s2 = min(sz2, self.size2)
        s3 = min(sz3, self.size3)
        b[:s1, :s2, :s3] = self.buffer[:s1, :s2, :s3]
        self.buffer = b
        self.adapt_size()
        return self

    def chsize(self, sz1=-1, sz2=-1, sz3=-1):
        """
        Change size of data, zero-fill or truncate. 
        DO NOT change the value of OFFSET and SPECW, so EXTRACT should 
        always be preferred on spectra (unless you know exactly what your are doing).
        """
        if self.dim == 1:
            self._chsize1d(sz1)
        else:
            if self.dim == 2:
                self._chsize2d(sz1, sz2)
            else:
                self._chsize3d(sz1, sz2, sz3)
        self._absmax = 0.0
        return self

    def zf(self, zf1=None, zf2=None, zf3=None):
        """
        Zerofill data by adding zeros.
        for a dataset of length size, will add zeros up to zf*size

        do nothing by default unless axis is sampled,
        in which case, missing unsampled points are replaced by 0.0
        """
        if self.dim == 1:
            if self.axis1.sampled:
                if self.axis1.itype == 0:
                    data = np.zeros(max(self.axis1.sampling) + 1)
                    data[self.axis1.sampling] = self.buffer
                    self.buffer = data
                else:
                    data = np.zeros(max(self.axis1.sampling) + 1) * complex(0.0, 1.0)
                    data[self.axis1.sampling] = as_cpx(self.buffer)
                    self.buffer = as_float(data)
                self.axis1.sampling = None
                self.adapt_size()
            if zf1:
                self._chsize1d(self.size1 * zf1)
        else:
            if self.dim == 2:
                if self.axis2.sampled:
                    raise 'This is to be done'
                if self.axis1.sampled:
                    if self.axis1.itype == 0:
                        data = np.zeros((max(self.axis1.sampling) + 1, self.size2))
                        data[self.axis1.sampling, :] = self.buffer[:, :]
                        self.buffer = data
                    else:
                        data = np.zeros((2 * max(self.axis1.sampling) + 2, self.size2))
                        data[2 * self.axis1.sampling, :] = self.buffer[::2, :]
                        data[2 * self.axis1.sampling + 1, :] = self.buffer[1::2, :]
                        self.buffer = data
                    self.axis1.sampling = None
                    self.adapt_size()
                if zf2:
                    self._chsize2d(self.size1, self.size2 * zf2)
                if zf1:
                    self._chsize2d(self.size1 * zf1, self.size2)
            else:
                if self.axis3.sampled:
                    raise 'This is to be done'
                if zf3:
                    self._chsize3d(self.size1, self.size2, self.size3 * zf3)
                if zf2:
                    self._chsize3d(self.size1, self.size2 * zf2, self.size3)
                if zf1:
                    self._chsize3d(self.size1 * zf1, self.size2, self.size3)
            self._absmax = 0.0
            return self

    def load_sampling(self, filename, axis=1):
        """equivalent to the axis.load_sampling() method - can be pipelined"""
        todo = self.test_axis(axis)
        self.axes(todo).load_sampling(filename)
        return self

    def extract(self, *args):
        """
        extract([[x1, y1]])
        extract([x1, y1], [x2, y2]) or extract([x1, y1, x2, y2])
        etc...

        Permits to extract a portion of the data.
        Data can then be processed as a regular data-set.
        EXTRACT changes the value of OFFSET and SPECW accordingly.

            * extract(x1,y1) for 1D datasets.
            * extract(x1, y1, x2, y2) for 2D datasets.
        
        coordinates are given in axis current unit

        see also : chsize
        """
        limits = flatten(args)
        if len(limits) != 2 * self.dim:
            raise NPKError(("slice should be defined as coordinate pair (left,right) in axis' current unit : " + ' - '.join(self.unit)), data=self)
        elif self.dim == 1:
            self._extract1d(limits)
        else:
            if self.dim == 2:
                self._extract2d(limits)
            else:
                if self.dim == 3:
                    self._extract3d(limits)
        self._absmax = 0.0
        return self

    def _extract1d(self, zoom):
        """performs the extract in 1D,
        """
        self.check1D()
        x1, y1 = self.axis1.extract(zoom)
        self.buffer = self.buffer[x1:y1]
        self.adapt_size()
        return self

    def _extract2d(self, zoom):
        self.check2D()
        zoom = flatten(zoom)
        x1, y1 = self.axis1.extract(zoom[0:2])
        x2, y2 = self.axis2.extract(zoom[2:4])
        self.buffer = self.buffer[x1:y1, x2:y2]
        self.adapt_size()
        return self

    def _extract3d(self, zoom):
        self.check3D()
        zoom = flatten(zoom)
        x1, y1 = self.axis1.extract((zoom[0], zoom[1]))
        x2, y2 = self.axis2.extract((zoom[2], zoom[3]))
        x3, y3 = self.axis3.extract((zoom[4], zoom[5]))
        self.buffer = self.buffer[x1:y1, x2:y2, x3:y3]
        self.adapt_size()
        return self

    def zeroing(self, threshold):
        """
        Sets to zero points below threshold (in absolute value)
        Can be used for compression
        see also :  eroding, plus, minus
        """
        self.buffer[abs(self.buffer) < threshold] = 0.0
        return self

    def eroding(self):
        """
        Sets to zeros values isolated between to zeros values
        Can be used for further compression after zeroing
        see also :  zeroing
        """
        b = self.get_buffer()
        b[1:-1] = np.where(np.logical_and(b[2:] == 0, b[:-2] == 0), 0.0, b[1:-1])
        if b[1] == 0:
            b[0] = 0
        if b[(-2)] == 0:
            b[-1] = 0
        self.set_buffer(b)
        return self

    def dilating(self):
        """
        Extends values neighbourg to zeros values
        see also :  eroding
        """
        b = self.get_buffer()
        b[1:-1] = np.where(np.logical_and(b[1:-1] == 0, b[:-2] + b[2:] != 0), 0.5 * (b[:-2] + b[2:]), b[1:-1])
        if b[0] == 0:
            b[0] = 0.5 * b[1]
        if b[(-1)] == 0:
            b[-1] = 0.5 * b[(-2)]
        self.set_buffer(b)
        return self

    def plus(self):
        """
        Sets to zero the negative part of the data set
        see also :  minus, zeroing
        """
        self.buffer[self.buffer < 0] = 0.0
        self._absmax = 0.0
        return self

    def minus(self):
        """
        Sets to zero the positive part of the data set
        see also :  minus, zeroing
        """
        self.buffer[self.buffer > 0] = 0.0
        return self

    def diag(self, direc='F12'):
        """
        In 2D, extracts the diagonal of the 2D and put into the 1D buffer.

        In 3D, extracts one diagonal plane of the 3D cube, chosen with the direc parameter 
        and put it into the 2D buffer
        direct values are :

        "F12" is the F1=F2 diagonal
        "F23" is the F2=F3 diagonal
        "F13" is the F1=F3 diagonal

        """
        if self.itype != 0:
            raise NPKError('Data should be real')
        else:
            if self.dim == 1:
                raise NPKError('Can not extract diagonal from a 1D buffer')
            else:
                if self.dim == 2:
                    c = self.diag2D()
                else:
                    if self.dim == 3:
                        c = self.diag3D(direc)
            return c

    def diag2D(self):
        self.check2D()
        Data = type(self)
        if self.size1 > self.size2:
            c = Data(shape=(self.size1,))
            z = float(self.size1) / self.size1
            for i in range(1, self.size2):
                for j in range(0, int(z)):
                    c.buffer[(i - 1) * z + j] = self.buffer[i][(float(i) / z)]

            c.axis1 = self.axis1.copy()
        else:
            z = float(self.size2) / self.size1
            c = Data(shape=(self.size2,))
            for i in range(1, self.size1):
                for j in range(0, int(z)):
                    c.buffer[(i - 1) * z + j] = self.buffer[(i - 1)][((i - 1) * z + j)]

            c.axis1 = self.axis2.copy()
        return c

    def diag3D(self, direc):
        raise NPKError('Not implemented yet')

    def col(self, i):
        """returns a 1D extracted from the current 2D at position 0<=i<=size2-1 """
        self.check2D()
        Data = type(self)
        c = Data(buffer=(self.buffer[:, i].copy()))
        c.axis1 = self.axis1.copy()
        try:
            c.params = copy.deepcopy(self.params)
        except AttributeError:
            pass

        return c

    def set_col(self, i, d1D):
        """set into the current 2D the given 1D, as the column at position 0<=i<=size2-1 """
        self.check2D()
        d1D.check1D()
        if d1D.axis1.itype != self.axis1.itype:
            warnings.warn('column and 2D types do not match', UserWarning)
        self.buffer[:, i] = d1D.buffer
        return self

    def xcol(self, start=0, stop=None, step=1):
        """
        an iterator over columns of a 2D
        so 
        for c in matrix.xcol():
            do something with c...

        is equivalent to
        for i in range(matrix.size2):     # i.e. all cols
            c = matrix.col(i)
            do something with c...

        you can limit the range by giving start, stop and step arguments - using the same syntax as xrange()
        
        on hypercomplex data
        matrix.xcol( step=matrix.axis2.itype+1 )
        will step only on cols associated to the real point 
        """
        if not stop:
            stop = self.size2
        for index in xrange(start, stop, step):
            yield self.col(index)

    def row(self, i):
        """returns a 1D extracted from the current 2D at position 0<=i<=size1-1 """
        self.check2D()
        Data = type(self)
        r = Data(buffer=(self.buffer[i, :].copy()))
        r.axis1 = self.axis2.copy()
        try:
            r.params = copy.deepcopy(self.params)
        except AttributeError:
            pass

        return r

    def set_row(self, i, d1D):
        """set into the current 2D the given 1D, as the row at position 0<=i<=size1-1 """
        self.check2D()
        d1D.check1D()
        if d1D.axis1.itype != self.axis2.itype:
            warnings.warn('row and 2D types do not match', UserWarning)
        self.buffer[i, :] = d1D.buffer[:]
        return self

    def xrow(self, start=0, stop=None, step=1):
        """
        an iterator over rows of a 2D
        so 
        for r in matrix.xrow():
            do something with r...

        is equivalent to
        for i in range(matrix.size1):     # i.e. all rows 
            r = matrix.row(i)
            do something with r...

        you can limit the range by giving start, stop and step arguments - using the same syntax as xrange()
        
        on hypercomplex data
        matrix.xrow( step=matrix.axis1.itype+1 )
        will step only on rows associated to the real point 
        """
        if not stop:
            stop = self.size1
        for index in xrange(start, stop, step):
            yield self.row(index)

    def plane(self, axis, i):
        """returns a 2D extracted from the current 3D at position 0<=i<=size1-1 """
        todo = self.test_axis(axis)
        self.check3D()
        Data = type(self)
        if todo == 1:
            r = Data(buffer=(self.buffer[i, :, :].copy()))
            r.axis1 = self.axis2.copy()
            r.axis2 = self.axis3.copy()
            return r
        if todo == 2:
            r = Data(buffer=(self.buffer[:, i, :].copy()))
            r.axis1 = self.axis1.copy()
            r.axis2 = self.axis3.copy()
            return r
        if todo == 3:
            r = Data(buffer=(self.buffer[:, :, i].copy()))
            r.axis1 = self.axis1.copy()
            r.axis2 = self.axis2.copy()
            return r
        raise NPKError('problem with plane')

    def set_plane(self, axis, i, d2D):
        """set into the current 3D the given 2D, as a plane at position i """
        todo = self.test_axis(axis)
        self.check3D()
        d2D.check2D()
        if todo == 1:
            self.buffer[i, :, :] = d2D.buffer[:, :]
        else:
            if todo == 2:
                self.buffer[:, i, :] = d2D.buffer[:, :]
            else:
                if todo == 3:
                    self.buffer[:, :, i] = d2D.buffer[:, :]
                else:
                    raise NPKError('problem with plane axis selection')
        return self

    def xplane(self, axis, start=0, stop=None, step=1):
        """
        an iterator over planes of a 3D along axis (1, 2 or 3)
        (see test_axis() for documentation on axis selection)

        so 
        for p in matrix.xplane("F1"):
            do something with p...
        will scan through all  F1 planes

        you can limit the range by giving start, stop and step arguments - using the same syntax as xrange()

        on hypercomplex axis
        matrix.xplane("F2, step=matrix.axis2.itype+1 )
        will step only on planes associated to the real point 
        """
        todo = self.test_axis(axis)
        self.check3D()
        if not stop:
            stop = self.axes(todo).size
        for index in xrange(start, stop, step):
            yield self.plane(todo, index)

    def check_zoom(self, zoom):
        """
        check whether a zoom window, given as (low,high) or ((low1,high1),(low2,high2))  is valid
        - check low<high and within axis size
        - check that it starts on a real index in itype is complex
        return a boolean
        """
        if not zoom:
            return True
        else:
            z = flatten(zoom)
            if self.dim == 1:
                test = self.axis1.check_zoom(z)
            else:
                if self.dim == 2:
                    test = self.axis1.check_zoom(z[0:1]) and self.axis2.check_zoom(z[2:3])
        return test

    def display(self, scale=1.0, autoscalethresh=3.0, absmax=None, show=False, label=None, new_fig=True, axis=None, zoom=None, xlabel='_def_', ylabel='_def_', title=None, figure=None, linewidth=1, color=None, mpldic={}, mode3D=False, NbMaxVect=None):
        """
        not so quick and dirty display using matplotlib or mlab - still a first try
        
        scale   allows to increase the vertical scale of display,
                in 2D if "auto" will compute a scale so the first level is located at at autoscalethresh sigma
        autoscalethresh used for scale="auto"
        absmax  overwrite the value for the largest point, which will not be computed 
            display is scaled so that the largest point is first computed (and stored in _absmax),
            and then the value at _bsmax/scale is set full screen 
        show    will call plot.show() at the end, allowing every declared display to be shown on-screen
                useless in ipython
        label   add a label text to plot
        xlabel, ylabel : axes label (default is self.currentunit - use None to remove)
        axis    used as axis if present, axis length should match experiment length
                in 2D, should be a pair (xaxis,yaxis)
        new_fig will create a new window if set to True (default) (active only is figure==None)
                if new_fig is a dict, it will be passed as is to plt.figure()
        mode3D  obsolete
        zoom    is a tuple defining the zoom window (left,right) or   ((F1_limits),(F2_limits))
                defined in the current axis unit (points, ppm, m/z etc ....)
        figure  if not None, will be used directly to display instead of using its own
        linewidth: linewidth for the plots (useful for example when using seaborn)
        mpldic: a dictionnary passed as is to the plot command 
        NbMaxVect: if set to a number, will limit the number of displayed vectors to that number by decimating the data (in 1D only so far)

        can actually be called without harm, even if no graphic is available, it will just do nothing.
        
        """
        if figure is None:
            from .Display import testplot
            plot = testplot.plot()
            if new_fig:
                if isinstance(new_fig, dict):
                    (plot.figure)(**new_fig)
                else:
                    plot.figure()
            fig = plot.subplot(111)
        else:
            fig = figure
        self.mplfigure = fig
        if self.dim == 1:
            if absmax is None:
                absmax = self.absmax
            else:
                mmin = -absmax / scale
                mmax = absmax / scale
                step = self.axis1.itype + 1
                if scale == 'auto':
                    scale = 1.0
                z1, z2 = parsezoom(self, zoom)
                if axis is None:
                    ax = self.axis1.unit_axis()
                else:
                    ax = axis
            fig.set_xscale(self.axis1.units[self.axis1.currentunit].scale)
            if self.axis1.units[self.axis1.currentunit].reverse:
                fig.set_xlim(ax[z1], ax[z2])
            if NbMaxVect is not None:
                while abs(z2 - z1 + 1) / step > NbMaxVect:
                    step += self.axis1.itype + 1

            (fig.plot)(ax[z1:z2:step], self.buffer[z1:z2:step].clip(mmin, mmax), label=label, linewidth=linewidth, color=color, **mpldic)
            if xlabel == '_def_':
                xlabel = self.axis1.currentunit
            if ylabel == '_def_':
                ylabel = 'a.u.'
            if self.dim == 2:
                step2 = self.axis2.itype + 1
                step1 = self.axis1.itype + 1
                z1lo, z1up, z2lo, z2up = parsezoom(self, zoom)
                if not absmax:
                    absmax = self.absmax
                if mode3D:
                    print('3D not implemented')
        elif self.level:
            level = self.level
        else:
            if scale == 'auto':
                noise = findnoiselevel_2D(self.buffer)
                m = autoscalethresh * noise / 0.05
                print('computed scale: %.2f' % (absmax / m,))
            else:
                m = absmax / scale
            level = sorted([m * 0.05, m * 0.1, m * 0.25, m * 0.5])
            if xlabel == '':
                if ylabel == '':
                    fig.set_xticklabels('')
                    fig.set_yticklabels('')
            if axis is None:
                axis = (
                 self.axis1.unit_axis(), self.axis2.unit_axis())
            fig.set_yscale(self.axis1.units[self.axis1.currentunit].scale)
            if self.axis1.units[self.axis1.currentunit].reverse:
                fig.set_ylim(axis[0][z1lo], axis[0][z1up])
            fig.set_xscale(self.axis2.units[self.axis2.currentunit].scale)
            if self.axis2.units[self.axis2.currentunit].reverse:
                fig.set_xlim(axis[1][z2lo], axis[1][z2up])
            (fig.contour)(axis[1][z2lo:z2up:step2], axis[0][z1lo:z1up:step1],
 self.buffer[z1lo:z1up:step1, z2lo:z2up:step2],
 level, colors=color, **mpldic)
        if xlabel == '_def_':
            xlabel = self.axis2.currentunit
        if ylabel == '_def_':
            ylabel = self.axis1.currentunit
        if xlabel is not None:
            fig.set_xlabel(xlabel)
        if ylabel is not None:
            fig.set_ylabel(ylabel)
        if title:
            fig.set_title(title)
        if label:
            fig.legend()
        if show:
            if figure is None:
                plot.show()
        return self

    def f(self, x, y):
        """used by 3D display"""
        return self.buffer[(x, y)] / self.absmax * 100

    @property
    def absmax(self):
        if self._absmax == 0:
            self._absmax = np.nanmax(np.abs(self.buffer))
        return self._absmax

    def load(self, name):
        """load data from a file"""
        import File.GifaFile as GifaFile
        Go = GifaFile(name, 'r')
        Go.load()
        Go.close()
        B = Go.get_data()
        del Go
        self.buffer = B.buffer
        copyaxes(B, self)
        self.name = name
        del B
        return self

    def save(self, name):
        """save data to a file"""
        import File.GifaFile as GifaFile
        Go = GifaFile(name, 'w')
        Go.set_data(self)
        Go.save()
        Go.close()
        del Go
        self.name = name
        return self

    def save_txt(self, name):
        """save 1D data in texte, single column, no unit - with attributes as pseudo comments """
        from .File import csv
        if self.dim > 1:
            raise NPKError('text file format only possible on 1D', data=self)
        csv.save(self, name)
        return self

    def load_txt(self, name):
        """load 1D data in texte, single column, no unit - with attributes as pseudo comments """
        from .File import csv
        buf, att = csv.load(name)
        self.buffer = buf
        for k, v in att.items():
            if k in self.axis1.attributes:
                setattr(self.axis1, k, v)
            else:
                warning(' - wrong attributes : %s %s' % (k, v))

        self.adapt_size()
        return self

    def save_csv(self, name, fmt='%.9g'):
        """save 1D data in csv,
        in 2 columns : 
        x, y   x values are conditions by the .currentunit attribute
        data attributes are stored as pseudo comments
        
        data can be read back with File.csv.Import_1D()
        """
        from .File import csv
        if self.dim > 1:
            raise NPKError('csv only possible on 1D', data=self)
        csv.save_unit(self, name, fmt=fmt)
        return self

    def _report(self):
        """low level report"""
        s = '%dD data-set\n' % self.dim
        s += ''.join(['  %s: %s\n' % (att, getattr(self, att)) for att in self.__dict__ if att not in ('buffer',
                                                                                                       'axis1',
                                                                                                       'axis2',
                                                                                                       'axis3')])
        s = s + '\nAxis F1:\n' + self.axis1._report()
        if self.dim > 1:
            s = s + '\nAxis F2:\n' + self.axis2._report()
        if self.dim > 2:
            s = s + '\nAxis F3:\n' + self.axis3._report()
        return s

    def report(self):
        """reports itself"""
        self.check(warn=True)
        isum = 0
        iprod = 1
        s = '%dD data-set' % self.dim
        s = s + '\nAxis F1 :' + self.axis1.report()
        if self.dim > 1:
            s = s + '\nAxis F2: ' + self.axis2.report()
        if self.dim > 2:
            s = s + '\nAxis F3: ' + self.axis3.report()
        s = s + '\n' + self.typestr()
        return s

    def typestr(self):
        """ returns its type (real, complex or hypercomplex) as a string"""
        isum = sum([self.axes(i + 1).itype for i in range(self.dim)])
        if isum == 0:
            s = 'data-set is real'
        else:
            if isum == 1:
                if self.dim == 1:
                    s = 'data-set is complex'
                elif self.axis1.itype == 1:
                    s = 'data-set is complex in F1'
                elif self.axis2.itype == 1:
                    s = 'data-set is complex in F2'
            else:
                s = 'data-set is hypercomplex (order %d)' % (isum,)
        return s

    def __str__(self, *args, **kw):
        """
        express itself as a string,
        add checking here, as this is used during interactive use in ipython
        """
        self.check(warn=True)
        return (self.report)(*args, **kw)

    def __repr__(self, *args, **kw):
        """
        express itself as a string,
        add checking here, as this is used during interactive use in ipython
        """
        self.check(warn=True)
        return (self.report)(*args, **kw)

    def fill(self, value):
        """fills the dataset with a single numerical value"""
        self.buffer.fill(value)
        self._absmax = value
        return self

    def mult(self, multiplier):
        """
        Multiply data-set by a scalar
        eg : d.mult(alpha) multiplies d buffer by alpha
        """
        import numbers
        if not isinstance(multiplier, numbers.Number):
            raise NotImplementedError
        elif multiplier.imag == 0:
            self.buffer *= multiplier
            self._absmax *= multiplier
        else:
            if self.itype == 1:
                bb = as_cpx(self.buffer)
                bb *= multiplier
                self.buffer = as_float(bb)
                self._absmax *= multiplier
            else:
                raise NPKError('Multiplication of a real buffer by a complex scalar is not implemented yet', data=self)
        return self

    def __mul__(self, multiplier):
        return self.copy().mult(multiplier)

    def __rmul__(self, multiplier):
        return self.copy().mult(multiplier)

    def __imul__(self, multiplier):
        return self.mult(multiplier)

    def __neg__(self):
        return self.copy().mult(-1)

    def __pos__(self):
        return self.copy()

    def add(self, otherdata):
        """
        add the provided data : otherdata to the current one
        eg : data.add(otherdata) add content of otherdata to data buffer
        
        can add NPKData and numbers
        """
        import numbers, warnings
        if isinstance(otherdata, _NPKData):
            if self.itype != otherdata.itype:
                raise NPKError('addition of dataset with different complex states is not implemented yet', data=self)
            self.buffer += otherdata.buffer
            self._absmax = 0.0
        else:
            if isinstance(otherdata, numbers.Number):
                if self.itype == 0:
                    if isinstance(otherdata, complex):
                        raise NPKError('cannot add a complex value to this data-set', data=self)
                    else:
                        self.buffer += otherdata
                        self._absmax += otherdata
                else:
                    self.buffer = as_float(as_cpx(self.buffer) + otherdata * complex(1.0, 0.0))
                    self._absmax += otherdata.real
            else:
                raise ValueError
        return self

    def __iadd__(self, otherdata):
        return self.add(otherdata)

    def __add__(self, otherdata):
        import numbers
        if isinstance(otherdata, _NPKData):
            return self.copy().add(otherdata)
        if isinstance(otherdata, numbers.Number):
            return self.copy().add(otherdata)
        raise NotImplementedError

    def __radd__(self, otherdata):
        import numbers
        if isinstance(otherdata, _NPKData):
            return self.copy().add(otherdata)
        if isinstance(otherdata, numbers.Number):
            return self.copy().add(otherdata)
        raise NotImplementedError

    def __sub__(self, otherdata):
        import numbers
        if isinstance(otherdata, _NPKData):
            return self.copy().add(otherdata.copy().mult(-1))
        if isinstance(otherdata, numbers.Number):
            return self.copy().add(-otherdata)
        raise NotImplementedError

    def __isub__(self, otherdata):
        import numbers
        if isinstance(otherdata, _NPKData):
            return self.add(otherdata.copy().mult(-1))
        if isinstance(otherdata, numbers.Number):
            return self.add(-otherdata)
        raise NotImplementedError

    def addbase(self, constant):
        """
        add a constant to the data
        """
        import numbers
        if isinstance(constant, complex):
            raise NotImplementedError
        else:
            if isinstance(constant, numbers.Number):
                self.buffer += constant
                self._absmax += constant
            else:
                raise NotImplementedError
        return self

    def addnoise(self, noise, seed=None):
        """
        add to the current data-set (1D, 2D, 3D) a white-gaussian, 
        characterized by its level noise, and the random generator seed.
        """
        if seed is not None:
            np.random.seed(seed)
        self._absmax = 0.0
        self.buffer += noise * np.random.standard_normal(self.buffer.shape)
        return self

    def addfreq(self, freq, amp=1.0):
        """
        add to the current data-set (1D) a single frequency sinusoid
        characterized by its frequency (from axis.specwidth) and amplitude
        """
        if self.dim == 1:
            if self.axis1.itype == 0:
                t = np.arange(self.size1) * freq / self.axis1.specwidth
                self.buffer += amp * np.cos(np.pi * t)
            else:
                t = np.arange(self.size1 // 2) * freq / self.axis1.specwidth
                self.buffer += as_float(amp * np.exp(complex(0.0, 1.0) * np.pi * t))
        else:
            raise NotImplementedError
        self._absmax += amp
        return self

    def mean(self, zone=None):
        """
        computes mean value  in the designed spectral zone
        (NEW!) returns a complex if data is complex along fastest axis
        """
        if self.dim == 1:
            if zone is None:
                ll = 0
                ur = self.size1
            else:
                ll = int(zone[0])
                ur = int(zone[1])
            shift = self.get_buffer()[ll:ur].mean()
        else:
            if self.dim == 2:
                if zone is None:
                    ll = 0
                    lr = self.size2
                    ul = 1
                    ur = self.size1
                else:
                    ll = int(zone[0][0])
                    lr = int(zone[0][1])
                    ul = int(zone[1][0])
                    ur = int(zone[1][1])
                shift = self.get_buffer()[ul:ur, ll:lr].mean()
        return shift

    def center(self, zone=None):
        """
        center the data, so that the sum of points is zero (usefull for FIDs) 

        """
        self.check1D()
        self -= self.mean()
        return self

    def std(self, zone=None):
        """
        computes standard deviation in the designed spectral zone
        Computes value on the real part only
        """
        if self.dim == 1:
            if zone is None:
                ll = 0
                ur = self.size1
            else:
                ll = int(zone[0])
                ur = int(zone[1])
            noise = self.buffer[ll:ur:self.axis1.itype + 1].std()
        else:
            if self.dim == 2:
                if zone is None:
                    ll = 0
                    lr = self.size2
                    ul = 1
                    ur = self.size1
                else:
                    ll = int(zone[0][0])
                    lr = int(zone[0][1])
                    ul = int(zone[1][0])
                    ur = int(zone[1][1])
                noise = self.buffer[ll:lr:self.axis1.itype + 1, ul:ur:self.axis2.itype + 1].std()
        return noise

    def robust_stats(self, tresh=3.0, iterations=5):
        """
        returns (mean, std) for current dataset, while excluding most outliers
        defined as larger than (tresh*std+mean)
        """
        b = self.copy().get_buffer().real.ravel()
        for i in range(iterations):
            b = b[(b - b.mean() < tresh * b.std())]

        return (
         b.mean(), b.std())

    def test_axis(self, axis=0):
        """
        tests on axis

         in 1D,  axis is not used
                 axis has to be 1 or "F1"
         in 2D,  axis is either 2 for horizontal / faster incremented dimension  == "F2"
                 or 1 for the other dimension == "F1"
                 defaut is 2
         in 3D, axis is 3, 2 or 1 with 3 the faster incremented and 1 the slower == F3 F2 F1
                 defaut is 3
         alternativaly, you may use the strings "F1", "F2" or "F3"
         BUT not F12 F23 as 
         0 is set to default

        """
        if self.dim == 1:
            if axis in (0, 1, 'F1', 'f1'):
                r = 1
            else:
                raise NPKError('Wrong axis parameter : %s in %dD' % (str(axis), self.dim))
        elif self.dim == 2:
            if axis in (0, 2, 'F2', 'f2'):
                r = 2
            elif axis in (1, 'F1', 'f1'):
                r = 1
            else:
                raise NPKError('Wrong axis parameter : %s in %dD' % (str(axis), self.dim))
        elif self.dim == 3:
            if axis in (0, 3, 'F3', 'f3'):
                r = 3
            elif axis in (2, 'F2', 'f2'):
                r = 2
            elif axis in (1, 'F1', 'f1'):
                r = 1
            else:
                raise NPKError('Wrong axis parameter : %s in %dD' % (str(axis), self.dim))
        else:
            raise NPKError('Wrong axis parameter : %s in %dD' % (str(axis), self.dim))
        return r

    def abs(self):
        """
        This command takes the absolute value of the current the data set 
        """
        self.buffer[:] = abs(self.buffer[:])
        return self

    def real(self, axis=0):
        """
        This command extract the real part of the current the data set 
        considered as complex.
        
        axis is not needed in 1D, 

        can be F1, or F2  in 2D - default is F2
        
        does nothing if not needed
        """
        axtodo = self.test_axis(axis)
        it = self.axes(axtodo).itype
        if it == 0:
            return self
        elif self.dim == 1:
            self.buffer = self.buffer[::2]
        else:
            if self.dim == 2:
                if axtodo == 1:
                    self.buffer = self.buffer[::2, :]
                elif axtodo == 2:
                    self.buffer = self.buffer[:, ::2]
                else:
                    print('this should never happen')
            else:
                print(' real() not implemented in 3D yet')
        self.axes(axtodo).itype = 0
        self.adapt_size()
        return self

    def swap--- This code section failed: ---

 L.2044         0  LOAD_FAST                'self'
                2  LOAD_METHOD              test_axis
                4  LOAD_FAST                'axis'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'todo'

 L.2045        10  LOAD_FAST                'self'
               12  LOAD_METHOD              axes
               14  LOAD_FAST                'todo'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  LOAD_ATTR                itype
               20  STORE_FAST               'it'

 L.2046        22  LOAD_FAST                'it'
               24  LOAD_CONST               1
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L.2047        30  LOAD_GLOBAL              NPKError
               32  LOAD_STR                 'Dataset should be real along given axis'
               34  LOAD_FAST                'self'
               36  LOAD_CONST               ('data',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            28  '28'

 L.2048        42  LOAD_FAST                'self'
               44  LOAD_ATTR                dim
               46  LOAD_CONST               1
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE   108  'to 108'

 L.2049        52  LOAD_GLOBAL              as_float
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                buffer
               58  LOAD_CONST               None
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                size1
               64  LOAD_CONST               2
               66  BINARY_FLOOR_DIVIDE
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  LOAD_CONST               1j
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                buffer
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                size1
               82  LOAD_CONST               2
               84  BINARY_FLOOR_DIVIDE
               86  LOAD_CONST               None
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  BINARY_MULTIPLY  
               94  BINARY_ADD       
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  LOAD_METHOD              copy
              100  CALL_METHOD_0         0  '0 positional arguments'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               buffer
              106  JUMP_FORWARD        318  'to 318'
            108_0  COME_FROM            50  '50'

 L.2050       108  LOAD_FAST                'self'
              110  LOAD_ATTR                dim
              112  LOAD_CONST               2
              114  COMPARE_OP               ==
          116_118  POP_JUMP_IF_FALSE   294  'to 294'

 L.2051       120  LOAD_FAST                'todo'
              122  LOAD_CONST               1
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   206  'to 206'

 L.2052       128  SETUP_LOOP          292  'to 292'
              130  LOAD_GLOBAL              xrange
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                size2
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  GET_ITER         
              140  FOR_ITER            202  'to 202'
              142  STORE_FAST               'i'

 L.2053       144  LOAD_FAST                'self'
              146  LOAD_METHOD              col
              148  LOAD_FAST                'i'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  LOAD_METHOD              swap
              154  CALL_METHOD_0         0  '0 positional arguments'
              156  STORE_FAST               'r'

 L.2054       158  LOAD_GLOBAL              warnings
              160  LOAD_METHOD              catch_warnings
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  SETUP_WITH          194  'to 194'
              166  POP_TOP          

 L.2055       168  LOAD_GLOBAL              warnings
              170  LOAD_METHOD              simplefilter
              172  LOAD_STR                 'ignore'
              174  CALL_METHOD_1         1  '1 positional argument'
              176  POP_TOP          

 L.2056       178  LOAD_FAST                'self'
              180  LOAD_METHOD              set_col
              182  LOAD_FAST                'i'
              184  LOAD_FAST                'r'
              186  CALL_METHOD_2         2  '2 positional arguments'
              188  POP_TOP          
              190  POP_BLOCK        
              192  LOAD_CONST               None
            194_0  COME_FROM_WITH      164  '164'
              194  WITH_CLEANUP_START
              196  WITH_CLEANUP_FINISH
              198  END_FINALLY      
              200  JUMP_BACK           140  'to 140'
              202  POP_BLOCK        
              204  JUMP_FORWARD        292  'to 292'
            206_0  COME_FROM           126  '126'

 L.2057       206  LOAD_FAST                'todo'
              208  LOAD_CONST               2
              210  COMPARE_OP               ==
          212_214  POP_JUMP_IF_FALSE   318  'to 318'

 L.2058       216  SETUP_LOOP          318  'to 318'
              218  LOAD_GLOBAL              xrange
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                size1
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  GET_ITER         
              228  FOR_ITER            290  'to 290'
              230  STORE_FAST               'i'

 L.2059       232  LOAD_FAST                'self'
              234  LOAD_METHOD              row
              236  LOAD_FAST                'i'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  LOAD_METHOD              swap
              242  CALL_METHOD_0         0  '0 positional arguments'
              244  STORE_FAST               'r'

 L.2060       246  LOAD_GLOBAL              warnings
              248  LOAD_METHOD              catch_warnings
              250  CALL_METHOD_0         0  '0 positional arguments'
              252  SETUP_WITH          282  'to 282'
              254  POP_TOP          

 L.2061       256  LOAD_GLOBAL              warnings
              258  LOAD_METHOD              simplefilter
              260  LOAD_STR                 'ignore'
              262  CALL_METHOD_1         1  '1 positional argument'
              264  POP_TOP          

 L.2062       266  LOAD_FAST                'self'
              268  LOAD_METHOD              set_row
              270  LOAD_FAST                'i'
              272  LOAD_FAST                'r'
              274  CALL_METHOD_2         2  '2 positional arguments'
              276  POP_TOP          
              278  POP_BLOCK        
              280  LOAD_CONST               None
            282_0  COME_FROM_WITH      252  '252'
              282  WITH_CLEANUP_START
              284  WITH_CLEANUP_FINISH
              286  END_FINALLY      
              288  JUMP_BACK           228  'to 228'
              290  POP_BLOCK        
            292_0  COME_FROM_LOOP      216  '216'
            292_1  COME_FROM           204  '204'
            292_2  COME_FROM_LOOP      128  '128'
              292  JUMP_FORWARD        318  'to 318'
            294_0  COME_FROM           116  '116'

 L.2063       294  LOAD_FAST                'self'
              296  LOAD_ATTR                dim
              298  LOAD_CONST               3
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   318  'to 318'

 L.2064       306  LOAD_GLOBAL              NPKError
              308  LOAD_STR                 'reste a faire'
              310  LOAD_FAST                'self'
              312  LOAD_CONST               ('data',)
              314  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              316  RAISE_VARARGS_1       1  'exception instance'
            318_0  COME_FROM           302  '302'
            318_1  COME_FROM           292  '292'
            318_2  COME_FROM           212  '212'
            318_3  COME_FROM           106  '106'

 L.2065       318  LOAD_CONST               1
              320  LOAD_FAST                'self'
              322  LOAD_METHOD              axes
              324  LOAD_FAST                'todo'
              326  CALL_METHOD_1         1  '1 positional argument'
              328  STORE_ATTR               itype

 L.2066       330  LOAD_FAST                'self'
              332  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 292_2

    def unswap--- This code section failed: ---

 L.2078         0  LOAD_FAST                'self'
                2  LOAD_METHOD              test_axis
                4  LOAD_FAST                'axis'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'todo'

 L.2079        10  LOAD_FAST                'self'
               12  LOAD_METHOD              axes
               14  LOAD_FAST                'todo'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  LOAD_ATTR                itype
               20  STORE_FAST               'it'

 L.2080        22  LOAD_FAST                'it'
               24  LOAD_CONST               0
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L.2081        30  LOAD_GLOBAL              NPKError
               32  LOAD_STR                 'Dataset should be complex along given axis'
               34  LOAD_FAST                'self'
               36  LOAD_CONST               ('data',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            28  '28'

 L.2082        42  LOAD_FAST                'self'
               44  LOAD_ATTR                dim
               46  LOAD_CONST               1
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE   112  'to 112'

 L.2083        52  LOAD_GLOBAL              as_cpx
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                buffer
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  LOAD_METHOD              copy
               62  CALL_METHOD_0         0  '0 positional arguments'
               64  STORE_FAST               'cop'

 L.2084        66  LOAD_FAST                'cop'
               68  LOAD_ATTR                real
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                buffer
               74  LOAD_CONST               None
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                size1
               80  LOAD_CONST               2
               82  BINARY_FLOOR_DIVIDE
               84  BUILD_SLICE_2         2 
               86  STORE_SUBSCR     

 L.2085        88  LOAD_FAST                'cop'
               90  LOAD_ATTR                imag
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                buffer
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                size1
              100  LOAD_CONST               2
              102  BINARY_FLOOR_DIVIDE
              104  LOAD_CONST               None
              106  BUILD_SLICE_2         2 
              108  STORE_SUBSCR     
              110  JUMP_FORWARD        318  'to 318'
            112_0  COME_FROM            50  '50'

 L.2086       112  LOAD_FAST                'self'
              114  LOAD_ATTR                dim
              116  LOAD_CONST               2
              118  COMPARE_OP               ==
          120_122  POP_JUMP_IF_FALSE   298  'to 298'

 L.2087       124  LOAD_FAST                'todo'
              126  LOAD_CONST               1
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   210  'to 210'

 L.2088       132  SETUP_LOOP          296  'to 296'
              134  LOAD_GLOBAL              xrange
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                size2
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  GET_ITER         
              144  FOR_ITER            206  'to 206'
              146  STORE_FAST               'i'

 L.2089       148  LOAD_FAST                'self'
              150  LOAD_METHOD              col
              152  LOAD_FAST                'i'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  LOAD_METHOD              unswap
              158  CALL_METHOD_0         0  '0 positional arguments'
              160  STORE_FAST               'r'

 L.2090       162  LOAD_GLOBAL              warnings
              164  LOAD_METHOD              catch_warnings
              166  CALL_METHOD_0         0  '0 positional arguments'
              168  SETUP_WITH          198  'to 198'
              170  POP_TOP          

 L.2091       172  LOAD_GLOBAL              warnings
              174  LOAD_METHOD              simplefilter
              176  LOAD_STR                 'ignore'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_TOP          

 L.2092       182  LOAD_FAST                'self'
              184  LOAD_METHOD              set_col
              186  LOAD_FAST                'i'
              188  LOAD_FAST                'r'
              190  CALL_METHOD_2         2  '2 positional arguments'
              192  POP_TOP          
              194  POP_BLOCK        
              196  LOAD_CONST               None
            198_0  COME_FROM_WITH      168  '168'
              198  WITH_CLEANUP_START
              200  WITH_CLEANUP_FINISH
              202  END_FINALLY      
              204  JUMP_BACK           144  'to 144'
              206  POP_BLOCK        
              208  JUMP_FORWARD        296  'to 296'
            210_0  COME_FROM           130  '130'

 L.2093       210  LOAD_FAST                'todo'
              212  LOAD_CONST               2
              214  COMPARE_OP               ==
          216_218  POP_JUMP_IF_FALSE   318  'to 318'

 L.2094       220  SETUP_LOOP          318  'to 318'
              222  LOAD_GLOBAL              xrange
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                size1
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  GET_ITER         
              232  FOR_ITER            294  'to 294'
              234  STORE_FAST               'i'

 L.2095       236  LOAD_FAST                'self'
              238  LOAD_METHOD              row
              240  LOAD_FAST                'i'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  LOAD_METHOD              unswap
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  STORE_FAST               'r'

 L.2096       250  LOAD_GLOBAL              warnings
              252  LOAD_METHOD              catch_warnings
              254  CALL_METHOD_0         0  '0 positional arguments'
              256  SETUP_WITH          286  'to 286'
              258  POP_TOP          

 L.2097       260  LOAD_GLOBAL              warnings
              262  LOAD_METHOD              simplefilter
              264  LOAD_STR                 'ignore'
              266  CALL_METHOD_1         1  '1 positional argument'
              268  POP_TOP          

 L.2098       270  LOAD_FAST                'self'
              272  LOAD_METHOD              set_row
              274  LOAD_FAST                'i'
              276  LOAD_FAST                'r'
              278  CALL_METHOD_2         2  '2 positional arguments'
              280  POP_TOP          
              282  POP_BLOCK        
              284  LOAD_CONST               None
            286_0  COME_FROM_WITH      256  '256'
              286  WITH_CLEANUP_START
              288  WITH_CLEANUP_FINISH
              290  END_FINALLY      
              292  JUMP_BACK           232  'to 232'
              294  POP_BLOCK        
            296_0  COME_FROM_LOOP      220  '220'
            296_1  COME_FROM           208  '208'
            296_2  COME_FROM_LOOP      132  '132'
              296  JUMP_FORWARD        318  'to 318'
            298_0  COME_FROM           120  '120'

 L.2099       298  LOAD_FAST                'self'
              300  LOAD_ATTR                dim
              302  LOAD_CONST               3
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   318  'to 318'

 L.2100       310  LOAD_GLOBAL              NPKError
              312  LOAD_STR                 'reste a faire'
              314  CALL_FUNCTION_1       1  '1 positional argument'
              316  RAISE_VARARGS_1       1  'exception instance'
            318_0  COME_FROM           306  '306'
            318_1  COME_FROM           296  '296'
            318_2  COME_FROM           216  '216'
            318_3  COME_FROM           110  '110'

 L.2101       318  LOAD_CONST               0
              320  LOAD_FAST                'self'
              322  LOAD_METHOD              axes
              324  LOAD_FAST                'todo'
              326  CALL_METHOD_1         1  '1 positional argument'
              328  STORE_ATTR               itype

 L.2102       330  LOAD_FAST                'self'
              332  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 296_2

    def flip(self):
        """
        on a 2D with axis2.itype==1 and axis1.itype==0
        copies the imaginary from on axis to the other
        after this, we have
            axis2.itype==0 and axis1.itype==1
            size1 is doubled
            size2 is halved
        Useful for complex FT
        this is the opposite of flop()
        
        >>>bb=NPKData(buffer=array([[  0.,   1.,   2.,   3.],[  4.,   5.,   6.,   7.],[  8.,   9.,  10.,  11.],[ 12.,  13.,  14.,  15.]]))
        >>>print bb.buffer
        array([[  0.,   1.,   2.,   3.],
               [  4.,   5.,   6.,   7.],
               [  8.,   9.,  10.,  11.],
               [ 12.,  13.,  14.,  15.]])
        >>>bb.axis2.itype=1
        >>>print bb.typestr()
        data-set is complex in F2
        >>>bb.flip()
        >>>print bb.typestr()
        data-set is complex in F1
        >>>print bb.buffer
        array([[  0.,   2.],
               [  1.,   3.],
               [  4.,   6.],
               [  5.,   7.],
               [  8.,  10.],
               [  9.,  11.],
               [ 12.,  14.],
               [ 13.,  15.]])
        """
        if self.dim == 1:
            raise NPKError('Only in 2D or higher', data=self)
        else:
            if self.dim == 2:
                if not (self.axis2.itype == 1 and self.axis1.itype == 0):
                    raise NPKError('wrong axis itype', data=self)
                self.unswap(axis=2)
                self.buffer.resize((2 * self.size1, self.size2 // 2))
                self.axis2.itype = 0
                self.axis1.itype = 1
            else:
                if self.dim == 3:
                    raise NPKError('reste a faire')
        self.adapt_size()
        return self

    def flop(self):
        """
        on a 2D with axis2.itype==0 and axis1.itype==1
        copies the imaginary from on axis to the other
        after this, we have
            axis2.itype==1 and axis1.itype==0
            size1 is halved
            size2 is doubled
        Useful for complex FT
        this is the opposite of flip()
        """
        if self.dim == 1:
            raise NPKError('Only in 2D or higher', data=self)
        else:
            if self.dim == 2:
                if not (self.axis2.itype == 0 and self.axis1.itype == 1):
                    raise NPKError('wrong axis itype', data=self)
                self.buffer.resize((self.size1 // 2, self.size2 * 2))
                self.adapt_size()
                self.swap(axis=2)
                self.axis2.itype = 1
                self.axis1.itype = 0
            else:
                if self.dim == 3:
                    raise NPKError('reste a faire')
        return self

    def proj(self, axis=0, projtype='s'):
        """
        returns a projection of the dataset on the given axis
        projtype determines the algorithm :
            "s" is for skyline projection (the highest point is retained)
            "m" is for mean,
        """
        ptype = projtype.lower()
        todo = self.test_axis(axis)
        Data = type(self)
        if self.dim == 2:
            if todo == 1:
                if ptype == 's':
                    c = Data(buffer=(self.buffer.max(1)))
                else:
                    if ptype == 'm':
                        c = Data(buffer=self.buffer.mean(axis=1))
                c.axis1 = self.axis1.copy()
            elif todo == 2:
                if ptype == 's':
                    c = Data(buffer=(self.buffer.max(0)))
                else:
                    if ptype == 'm':
                        c = Data(buffer=self.buffer.mean(axis=0))
                c.axis1 = self.axis2.copy()
        elif self.dim == 3:
            print('3D')
        else:
            print('Dim should be at least 2')
        c.adapt_size()
        return c

    def phase(self, ph0, ph1, axis=0):
        """
        apply a phase correction along given axis
        phase corrections are in degree
        for a N complex spectrum, correction on ith point is 
             ph = ph0 +ph1*(i/N - 0.5)
             so central point is unchanged
        """
        import math as m
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        if it == 0:
            raise NPKError(msg='no phase correction on real data-set', data=self)
        else:
            size = self.axes(todo).size // 2
            if ph1 == 0:
                e = np.exp(complex(0.0, 1.0) * m.radians(float(ph0))) * np.ones(size, dtype=complex)
            else:
                le = m.radians(float(ph0)) + m.radians(float(ph1)) * np.linspace(-0.5, 0.5, size)
            e = np.cos(le) + complex(0.0, 1.0) * np.sin(le)
        self.axes(todo).P0 = ph0
        self.axes(todo).P1 = ph1
        return self.mult_by_vector(axis, e, mode='complex')

    def _phase_old(self, ph0, ph1, axis=0):
        """
        OBSOLETE - 10 to 20 time slower than above !
        apply a phase correction along given axis
        phase corrections are in degree
        for a N complex spectrum, correction on ith point is 
             ph = ph0 +ph1*(i/N - 0.5)
             so central point is unchanged
        """
        import math as m
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        if it == 0:
            raise NPKError(msg='no phase correction on real data-set', data=self)
        else:
            size = self.axes(todo).size // 2
            if ph1 == 0:
                e = np.exp(complex(0.0, 1.0) * m.radians(float(ph0))) * np.ones(size, dtype=complex)
            else:
                e = np.empty(size, dtype=complex)
                p0 = float(ph0) - 0.5 * ph1
                p1 = float(ph1) / (size - 1)
                for i in range(size):
                    z = m.radians(p0 + i * p1)
                    e[i] = m.cos(z) + complex(0.0, 1.0) * m.sin(z)

        self.axes(todo).P0 = ph0
        self.axes(todo).P1 = ph1
        return self.mult_by_vector(axis, e, mode='complex')

    def f1demodu(self, shift, axis=1):
        """
        'demodulate' a given 2D with FID along F1 by multiplying it with the complex serie exp(j 2 pi shift)
        this has the effect of shifting the frequency by 'shift' expressed in Hz
        
        Only for 2D.
        it is assumed to have complex pairs in even and odd columns
        faked by calling flipphase()
        """
        self.flipphase(0.0, 180.0 * shift)
        self.axis1.P1 = 0.0
        return self

    def flipphase(self, ph0, ph1, axis=1):
        """
        equivalent to   flip(); phase();flop()   but much faster
        apply a phase correction along F1 axis of a 2D.
        on 2D where axis1.itype = 0   and   axis2.itype = 1
        using pairs of columns as real and imaginary pair
        phase corrections are in degree
        """
        import math as m
        todo = self.test_axis(axis)
        if todo != 1 or self.dim != 2:
            raise NPKError(msg='works only along F1 axis of 2D', data=self)
        it = self.axis2.itype
        if it == 0:
            raise NPKError(msg='no phase correction on real data-set', data=self)
        else:
            size = self.axis1.size
            if ph1 == 0:
                e = np.exp(complex(0.0, 1.0) * m.radians(float(ph0))) * np.ones(size, dtype=complex)
            else:
                e = np.empty(size, dtype=complex)
                p0 = float(ph0) - 0.5 * ph1
                p1 = float(ph1) / (size - 1)
                for i in range(size):
                    z = m.radians(p0 + i * p1)
                    e[i] = m.cos(z) + complex(0.0, 1.0) * m.sin(z)

        for i in xrange(self.axis2.size // 2):
            c = e * (self.buffer[:, 2 * i] + complex(0.0, 1.0) * self.buffer[:, 2 * i + 1])
            self.buffer[:, 2 * i] = c.real
            self.buffer[:, 2 * i + 1] = c.imag

        self.axis1.P0 = ph0
        self.axis1.P1 = ph1
        return self

    def bruker_corr(self):
        """
        applies a correction on the spectrum for the time offset in the FID.
        time offset is stored in the axis property zerotime
        """
        delay = self.axes(self.dim).zerotime
        self.phase(0, (-360.0 * delay), axis=0)
        self.axes(self.dim).P1 = 0.0
        return self

    def conv_n_p(self):
        """
        realises the n+p to SH conversion
        """
        self.check2D()
        for i in xrange(0, self.size1, 2):
            a = self.row(i)
            b = self.row(i + 1)
            self.set_row(i, a.copy().add(b))
            a.buffer -= b.buffer
            a.buffer = as_float(complex(0.0, 1.0) * as_cpx(a.buffer))
            self.set_row(i + 1, a)

        self.axis1.itype = 1
        return self

    def fft(self, axis=0):
        """
        computes the complex Fourier transform,
        
        takes complex time domain data and returns complex frequency domain data

        see test_axis for information on axis
        """
        self._fft_nD(_base_fft, axis, 1, 1)
        return self

    def fftr(self, axis=0):
        """
        computes the alternate Fourier transform,

        takes complex time domain data and returns real frequency domain data

        see test_axis for information on axis
        """
        self._fft_nD(_base_fftr, axis, 1, 0)
        return self

    def rfft(self, axis=0):
        """
        computes the real Fourier transform,
        takes real time domain data and returns complex frequency domain data

        see test_axis for information on axis
        """
        self._fft_nD(_base_rfft, axis, 0, 1)
        return self

    def ifft(self, axis=0):
        """
        computes the inverse of fft(),
        takes complex frequency domain data and returns complex time domain data

        see test_axis for information on axis
        """
        self._fft_nD(_base_ifft, axis, 1, 1)
        return self

    def irfft(self, axis=0):
        """
        computes the inverse of rfft(),
        takes complex frequency domain data and returns real time domain data

        see test_axis for information on axis
        """
        self._fft_nD(_base_irfft, axis, 1, 0)
        return self

    def ifftr(self, axis=0):
        """
        computes the inverse of fftr,
        takes real frequency domain data and returns complex time domain data

        see test_axis for information on axis
        """
        self._fft_nD(_base_ifftr, axis, 0, 1)
        return self

    def _fft_nD--- This code section failed: ---

 L.2428         0  LOAD_CONST               0
                2  LOAD_CONST               ('time',)
                4  IMPORT_NAME              time
                6  IMPORT_FROM              time
                8  STORE_FAST               'time'
               10  POP_TOP          

 L.2429        12  LOAD_FAST                'time'
               14  CALL_FUNCTION_0       0  '0 positional arguments'
               16  STORE_FAST               't0'

 L.2430        18  LOAD_FAST                'self'
               20  LOAD_METHOD              test_axis
               22  LOAD_FAST                'axis'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  STORE_FAST               'todo'

 L.2431        28  LOAD_FAST                'self'
               30  LOAD_METHOD              axes
               32  LOAD_FAST                'todo'
               34  CALL_METHOD_1         1  '1 positional argument'
               36  LOAD_ATTR                itype
               38  LOAD_FAST                'it_before'
               40  COMPARE_OP               !=
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L.2432        44  LOAD_GLOBAL              NPKError
               46  LOAD_STR                 'wrong itype'
               48  LOAD_FAST                'self'
               50  LOAD_CONST               ('data',)
               52  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            42  '42'

 L.2433        56  LOAD_FAST                'self'
               58  LOAD_ATTR                dim
               60  LOAD_CONST               1
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    82  'to 82'

 L.2434        66  LOAD_FAST                'fft_base'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                buffer
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  LOAD_FAST                'self'
               76  STORE_ATTR               buffer
            78_80  JUMP_FORWARD        556  'to 556'
             82_0  COME_FROM            64  '64'

 L.2435        82  LOAD_FAST                'self'
               84  LOAD_ATTR                dim
               86  LOAD_CONST               2
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   250  'to 250'

 L.2436        92  LOAD_FAST                'todo'
               94  LOAD_CONST               2
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   158  'to 158'

 L.2437       100  SETUP_LOOP          246  'to 246'
              102  LOAD_GLOBAL              xrange
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                size1
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  GET_ITER         
              112  FOR_ITER            154  'to 154'
              114  STORE_FAST               'i'

 L.2439       116  LOAD_FAST                'fft_base'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                buffer
              122  LOAD_FAST                'i'
              124  LOAD_CONST               None
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  BUILD_TUPLE_2         2 
              132  BINARY_SUBSCR    
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  LOAD_FAST                'self'
              138  LOAD_ATTR                buffer
              140  LOAD_FAST                'i'
              142  LOAD_CONST               None
              144  LOAD_CONST               None
              146  BUILD_SLICE_2         2 
              148  BUILD_TUPLE_2         2 
              150  STORE_SUBSCR     
              152  JUMP_BACK           112  'to 112'
              154  POP_BLOCK        
              156  JUMP_FORWARD        556  'to 556'
            158_0  COME_FROM            98  '98'

 L.2440       158  LOAD_FAST                'todo'
              160  LOAD_CONST               1
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   246  'to 246'

 L.2441       166  LOAD_GLOBAL              np
              168  LOAD_METHOD              zeros
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                size1
              174  CALL_METHOD_1         1  '1 positional argument'
              176  STORE_FAST               'a'

 L.2442       178  SETUP_LOOP          246  'to 246'
              180  LOAD_GLOBAL              xrange
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                size2
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  GET_ITER         
              190  FOR_ITER            244  'to 244'
              192  STORE_FAST               'i'

 L.2445       194  LOAD_FAST                'self'
              196  LOAD_ATTR                buffer
              198  LOAD_CONST               None
              200  LOAD_CONST               None
              202  BUILD_SLICE_2         2 
              204  LOAD_FAST                'i'
              206  BUILD_TUPLE_2         2 
              208  BINARY_SUBSCR    
              210  LOAD_FAST                'a'
              212  LOAD_CONST               None
              214  LOAD_CONST               None
              216  BUILD_SLICE_2         2 
              218  STORE_SUBSCR     

 L.2446       220  LOAD_FAST                'fft_base'
              222  LOAD_FAST                'a'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                buffer
              230  LOAD_CONST               None
              232  LOAD_CONST               None
              234  BUILD_SLICE_2         2 
              236  LOAD_FAST                'i'
              238  BUILD_TUPLE_2         2 
              240  STORE_SUBSCR     
              242  JUMP_BACK           190  'to 190'
              244  POP_BLOCK        
            246_0  COME_FROM_LOOP      178  '178'
            246_1  COME_FROM           164  '164'
            246_2  COME_FROM_LOOP      100  '100'
          246_248  JUMP_FORWARD        556  'to 556'
            250_0  COME_FROM            90  '90'

 L.2447       250  LOAD_FAST                'self'
              252  LOAD_ATTR                dim
              254  LOAD_CONST               3
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   556  'to 556'

 L.2448       262  LOAD_GLOBAL              print
              264  LOAD_STR                 'A TESTER'
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  POP_TOP          

 L.2449       270  LOAD_FAST                'todo'
              272  LOAD_CONST               3
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   366  'to 366'

 L.2450       280  SETUP_LOOP          364  'to 364'
              282  LOAD_GLOBAL              xrange
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                size1
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  GET_ITER         
              292  FOR_ITER            362  'to 362'
              294  STORE_FAST               'i'

 L.2451       296  SETUP_LOOP          358  'to 358'
              298  LOAD_GLOBAL              xrange
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                size2
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  GET_ITER         
              308  FOR_ITER            356  'to 356'
              310  STORE_FAST               'j'

 L.2452       312  LOAD_FAST                'fft_base'
              314  LOAD_FAST                'self'
              316  LOAD_ATTR                buffer
              318  LOAD_FAST                'i'
              320  LOAD_FAST                'j'
              322  LOAD_CONST               None
              324  LOAD_CONST               None
              326  BUILD_SLICE_2         2 
              328  BUILD_TUPLE_3         3 
              330  BINARY_SUBSCR    
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  LOAD_FAST                'self'
              336  LOAD_ATTR                buffer
              338  LOAD_FAST                'i'
              340  LOAD_FAST                'j'
              342  LOAD_CONST               None
              344  LOAD_CONST               None
              346  BUILD_SLICE_2         2 
              348  BUILD_TUPLE_3         3 
              350  STORE_SUBSCR     
          352_354  JUMP_BACK           308  'to 308'
              356  POP_BLOCK        
            358_0  COME_FROM_LOOP      296  '296'
          358_360  JUMP_BACK           292  'to 292'
              362  POP_BLOCK        
            364_0  COME_FROM_LOOP      280  '280'
              364  JUMP_FORWARD        556  'to 556'
            366_0  COME_FROM           276  '276'

 L.2453       366  LOAD_FAST                'todo'
              368  LOAD_CONST               2
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   462  'to 462'

 L.2454       376  SETUP_LOOP          556  'to 556'
              378  LOAD_GLOBAL              xrange
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                size1
              384  CALL_FUNCTION_1       1  '1 positional argument'
              386  GET_ITER         
              388  FOR_ITER            458  'to 458'
              390  STORE_FAST               'i'

 L.2455       392  SETUP_LOOP          454  'to 454'
              394  LOAD_GLOBAL              xrange
              396  LOAD_FAST                'self'
              398  LOAD_ATTR                size3
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  GET_ITER         
              404  FOR_ITER            452  'to 452'
              406  STORE_FAST               'j'

 L.2456       408  LOAD_FAST                'fft_base'
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                buffer
              414  LOAD_FAST                'i'
              416  LOAD_CONST               None
              418  LOAD_CONST               None
              420  BUILD_SLICE_2         2 
              422  LOAD_FAST                'j'
              424  BUILD_TUPLE_3         3 
              426  BINARY_SUBSCR    
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                buffer
              434  LOAD_FAST                'i'
              436  LOAD_CONST               None
              438  LOAD_CONST               None
              440  BUILD_SLICE_2         2 
              442  LOAD_FAST                'j'
              444  BUILD_TUPLE_3         3 
              446  STORE_SUBSCR     
          448_450  JUMP_BACK           404  'to 404'
              452  POP_BLOCK        
            454_0  COME_FROM_LOOP      392  '392'
          454_456  JUMP_BACK           388  'to 388'
              458  POP_BLOCK        
              460  JUMP_FORWARD        556  'to 556'
            462_0  COME_FROM           372  '372'

 L.2457       462  LOAD_FAST                'todo'
            464_0  COME_FROM           156  '156'
              464  LOAD_CONST               1
              466  COMPARE_OP               ==
          468_470  POP_JUMP_IF_FALSE   556  'to 556'

 L.2458       472  SETUP_LOOP          556  'to 556'
              474  LOAD_GLOBAL              xrange
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                size2
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  GET_ITER         
              484  FOR_ITER            554  'to 554'
              486  STORE_FAST               'i'

 L.2459       488  SETUP_LOOP          550  'to 550'
              490  LOAD_GLOBAL              xrange
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                size3
              496  CALL_FUNCTION_1       1  '1 positional argument'
              498  GET_ITER         
              500  FOR_ITER            548  'to 548'
              502  STORE_FAST               'j'

 L.2460       504  LOAD_FAST                'fft_base'
              506  LOAD_FAST                'self'
              508  LOAD_ATTR                buffer
              510  LOAD_CONST               None
              512  LOAD_CONST               None
              514  BUILD_SLICE_2         2 
              516  LOAD_FAST                'i'
              518  LOAD_FAST                'j'
              520  BUILD_TUPLE_3         3 
              522  BINARY_SUBSCR    
              524  CALL_FUNCTION_1       1  '1 positional argument'
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                buffer
              530  LOAD_CONST               None
              532  LOAD_CONST               None
              534  BUILD_SLICE_2         2 
              536  LOAD_FAST                'i'
              538  LOAD_FAST                'j'
              540  BUILD_TUPLE_3         3 
              542  STORE_SUBSCR     
          544_546  JUMP_BACK           500  'to 500'
              548  POP_BLOCK        
            550_0  COME_FROM_LOOP      488  '488'
          550_552  JUMP_BACK           484  'to 484'
              554  POP_BLOCK        
            556_0  COME_FROM_LOOP      472  '472'
            556_1  COME_FROM           468  '468'
            556_2  COME_FROM           460  '460'
            556_3  COME_FROM_LOOP      376  '376'
            556_4  COME_FROM           364  '364'
            556_5  COME_FROM           258  '258'
            556_6  COME_FROM           246  '246'
            556_7  COME_FROM            78  '78'

 L.2461       556  LOAD_FAST                'it_after'
              558  LOAD_FAST                'self'
              560  LOAD_METHOD              axes
              562  LOAD_FAST                'todo'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  STORE_ATTR               itype

 L.2462       568  LOAD_CONST               0.0
              570  LOAD_FAST                'self'
              572  STORE_ATTR               _absmax

Parse error at or near `LOAD_CONST' instruction at offset 464

    def apply_process--- This code section failed: ---

 L.2478         0  LOAD_CODE                <code_object _do_it>
                2  LOAD_STR                 '_NPKData.apply_process.<locals>._do_it'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               '_do_it'

 L.2482         8  LOAD_FAST                'self'
               10  LOAD_METHOD              test_axis
               12  LOAD_FAST                'axis'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  STORE_FAST               'todo'

 L.2483        18  LOAD_GLOBAL              it
               20  LOAD_METHOD              imap
               22  LOAD_FAST                '_do_it'
               24  LOAD_GLOBAL              it
               26  LOAD_METHOD              izip
               28  LOAD_FAST                'axis_it'
               30  LOAD_GLOBAL              it
               32  LOAD_METHOD              repeat
               34  LOAD_FAST                'process'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  CALL_METHOD_2         2  '2 positional arguments'
               40  CALL_METHOD_2         2  '2 positional arguments'
               42  STORE_FAST               'results'

 L.2484        44  LOAD_FAST                'results'
               46  LOAD_METHOD              next
               48  CALL_METHOD_0         0  '0 positional arguments'
               50  STORE_FAST               'r0'

 L.2485        52  LOAD_FAST                'r0'
               54  LOAD_ATTR                dim
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                dim
               60  COMPARE_OP               <=
               62  POP_JUMP_IF_FALSE    76  'to 76'

 L.2486        64  LOAD_GLOBAL              NPKError
               66  LOAD_STR                 'wrong dimension'
               68  LOAD_FAST                'self'
               70  LOAD_CONST               ('data',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            62  '62'

 L.2487        76  LOAD_FAST                'self'
               78  LOAD_ATTR                dim
               80  LOAD_CONST               1
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   158  'to 158'

 L.2488        86  LOAD_FAST                'r0'
               88  LOAD_ATTR                buffer
               90  LOAD_CONST               None
               92  LOAD_CONST               None
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                buffer
              102  LOAD_CONST               None
              104  LOAD_CONST               None
              106  BUILD_SLICE_2         2 
              108  STORE_SUBSCR     

 L.2489       110  SETUP_LOOP          156  'to 156'
              112  LOAD_FAST                'results'
              114  GET_ITER         
              116  FOR_ITER            154  'to 154'
              118  STORE_FAST               'r'

 L.2490       120  LOAD_FAST                'self'
              122  LOAD_ATTR                buffer
              124  LOAD_CONST               None
              126  LOAD_CONST               None
              128  BUILD_SLICE_2         2 
              130  DUP_TOP_TWO      
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'r'
              136  LOAD_ATTR                buffer
              138  LOAD_CONST               None
              140  LOAD_CONST               None
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  INPLACE_ADD      
              148  ROT_THREE        
              150  STORE_SUBSCR     
              152  JUMP_BACK           116  'to 116'
              154  POP_BLOCK        
            156_0  COME_FROM_LOOP      110  '110'
              156  JUMP_FORWARD        380  'to 380'
            158_0  COME_FROM            84  '84'

 L.2491       158  LOAD_FAST                'self'
              160  LOAD_ATTR                dim
              162  LOAD_CONST               2
              164  COMPARE_OP               ==
          166_168  POP_JUMP_IF_FALSE   360  'to 360'

 L.2492       170  LOAD_FAST                'todo'
              172  LOAD_CONST               2
              174  COMPARE_OP               ==
          176_178  POP_JUMP_IF_FALSE   264  'to 264'

 L.2493       180  LOAD_FAST                'r0'
              182  LOAD_ATTR                buffer
              184  LOAD_CONST               None
              186  LOAD_CONST               None
              188  BUILD_SLICE_2         2 
              190  BINARY_SUBSCR    
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                buffer
              196  LOAD_CONST               0
              198  LOAD_CONST               None
              200  LOAD_CONST               None
              202  BUILD_SLICE_2         2 
              204  BUILD_TUPLE_2         2 
              206  STORE_SUBSCR     

 L.2494       208  LOAD_CONST               0
              210  STORE_FAST               'i'

 L.2495       212  SETUP_LOOP          358  'to 358'
              214  LOAD_FAST                'results'
              216  GET_ITER         
              218  FOR_ITER            260  'to 260'
              220  STORE_FAST               'r'

 L.2496       222  LOAD_FAST                'i'
              224  LOAD_CONST               1
              226  INPLACE_ADD      
              228  STORE_FAST               'i'

 L.2497       230  LOAD_FAST                'r'
              232  LOAD_ATTR                buffer
              234  LOAD_CONST               None
              236  LOAD_CONST               None
              238  BUILD_SLICE_2         2 
              240  BINARY_SUBSCR    
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                buffer
              246  LOAD_FAST                'i'
              248  LOAD_CONST               None
              250  LOAD_CONST               None
              252  BUILD_SLICE_2         2 
              254  BUILD_TUPLE_2         2 
              256  STORE_SUBSCR     
              258  JUMP_BACK           218  'to 218'
              260  POP_BLOCK        
              262  JUMP_FORWARD        358  'to 358'
            264_0  COME_FROM           176  '176'

 L.2498       264  LOAD_FAST                'todo'
              266  LOAD_CONST               1
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   380  'to 380'

 L.2499       274  LOAD_FAST                'r0'
              276  LOAD_ATTR                buffer
              278  LOAD_CONST               None
              280  LOAD_CONST               None
              282  BUILD_SLICE_2         2 
              284  BINARY_SUBSCR    
              286  LOAD_FAST                'self'
              288  LOAD_ATTR                buffer
              290  LOAD_CONST               None
              292  LOAD_CONST               None
              294  BUILD_SLICE_2         2 
              296  LOAD_CONST               0
              298  BUILD_TUPLE_2         2 
              300  STORE_SUBSCR     

 L.2500       302  LOAD_CONST               0
              304  STORE_FAST               'i'

 L.2501       306  SETUP_LOOP          380  'to 380'
              308  LOAD_FAST                'results'
              310  GET_ITER         
              312  FOR_ITER            356  'to 356'
              314  STORE_FAST               'r'

 L.2502       316  LOAD_FAST                'i'
              318  LOAD_CONST               1
              320  INPLACE_ADD      
              322  STORE_FAST               'i'

 L.2503       324  LOAD_FAST                'r'
              326  LOAD_ATTR                buffer
              328  LOAD_CONST               None
              330  LOAD_CONST               None
              332  BUILD_SLICE_2         2 
              334  BINARY_SUBSCR    
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                buffer
              340  LOAD_CONST               None
              342  LOAD_CONST               None
              344  BUILD_SLICE_2         2 
              346  LOAD_FAST                'i'
              348  BUILD_TUPLE_2         2 
              350  STORE_SUBSCR     
          352_354  JUMP_BACK           312  'to 312'
              356  POP_BLOCK        
            358_0  COME_FROM_LOOP      306  '306'
            358_1  COME_FROM           262  '262'
            358_2  COME_FROM_LOOP      212  '212'
              358  JUMP_FORWARD        380  'to 380'
            360_0  COME_FROM           166  '166'

 L.2504       360  LOAD_FAST                'self'
              362  LOAD_ATTR                dim
              364  LOAD_CONST               3
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   380  'to 380'

 L.2505       372  LOAD_GLOBAL              print
              374  LOAD_STR                 'A FAIRE'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  POP_TOP          
            380_0  COME_FROM           368  '368'
            380_1  COME_FROM           358  '358'
            380_2  COME_FROM           270  '270'
            380_3  COME_FROM           156  '156'

 L.2506       380  LOAD_FAST                'self'
              382  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 358_2

    def transpose(self, axis=0):
        """
        Transposes the 2D matrix or planes of the 3D cube. The sizes of 
        the matrix must be a power of two for this command to be used. After 
        transposition, the two dimensions are completely permuted
        
        axis is used in 3D to tell which submatrices should be transposed
        
        
        see also : sym chsize modifysize
        """
        todo = self.test_axis(axis)
        if self.dim == 2:
            self.set_buffer(self.get_buffer().T)
            self.axis1, self.axis2 = self.axis2, self.axis1
            self.adapt_size()
        else:
            raise NPKError('Operation not available', self)
        return self

    def reverse--- This code section failed: ---

 L.2535         0  LOAD_FAST                'self'
                2  LOAD_METHOD              test_axis
                4  LOAD_FAST                'axis'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'todo'

 L.2536        10  LOAD_FAST                'self'
               12  LOAD_METHOD              axes
               14  LOAD_FAST                'todo'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  LOAD_ATTR                itype
               20  STORE_FAST               'it'

 L.2537        22  LOAD_FAST                'self'
               24  LOAD_ATTR                dim
               26  LOAD_CONST               1
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE   158  'to 158'

 L.2538        32  LOAD_FAST                'it'
               34  LOAD_CONST               0
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    64  'to 64'

 L.2539        40  LOAD_FAST                'self'
               42  LOAD_ATTR                buffer
               44  LOAD_CONST               None
               46  LOAD_CONST               None
               48  LOAD_CONST               -1
               50  BUILD_SLICE_3         3 
               52  BINARY_SUBSCR    
               54  LOAD_METHOD              copy
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               buffer
               62  JUMP_FORWARD       1036  'to 1036'
             64_0  COME_FROM            38  '38'

 L.2540        64  LOAD_FAST                'it'
               66  LOAD_CONST               1
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   146  'to 146'

 L.2541        72  LOAD_FAST                'self'
               74  LOAD_ATTR                buffer
               76  LOAD_CONST               None
               78  LOAD_CONST               None
               80  LOAD_CONST               -1
               82  BUILD_SLICE_3         3 
               84  BINARY_SUBSCR    
               86  LOAD_METHOD              copy
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  STORE_FAST               'v'

 L.2542        92  LOAD_FAST                'v'
               94  LOAD_CONST               1
               96  LOAD_CONST               None
               98  LOAD_CONST               2
              100  BUILD_SLICE_3         3 
              102  BINARY_SUBSCR    
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                buffer
              108  LOAD_CONST               None
              110  LOAD_CONST               None
              112  LOAD_CONST               2
              114  BUILD_SLICE_3         3 
              116  STORE_SUBSCR     

 L.2543       118  LOAD_FAST                'v'
              120  LOAD_CONST               None
              122  LOAD_CONST               None
              124  LOAD_CONST               2
              126  BUILD_SLICE_3         3 
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                buffer
              134  LOAD_CONST               1
              136  LOAD_CONST               None
              138  LOAD_CONST               2
              140  BUILD_SLICE_3         3 
              142  STORE_SUBSCR     
              144  JUMP_FORWARD       1036  'to 1036'
            146_0  COME_FROM            70  '70'

 L.2545       146  LOAD_GLOBAL              NPKError
              148  LOAD_STR                 'internal error'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  RAISE_VARARGS_1       1  'exception instance'
          154_156  JUMP_FORWARD       1036  'to 1036'
            158_0  COME_FROM            30  '30'

 L.2546       158  LOAD_FAST                'self'
              160  LOAD_ATTR                dim
              162  LOAD_CONST               2
              164  COMPARE_OP               ==
          166_168  POP_JUMP_IF_FALSE   484  'to 484'

 L.2547       170  LOAD_FAST                'todo'
              172  LOAD_CONST               1
              174  COMPARE_OP               ==
          176_178  POP_JUMP_IF_FALSE   296  'to 296'

 L.2548       180  LOAD_FAST                'it'
              182  LOAD_CONST               0
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   212  'to 212'

 L.2549       188  LOAD_FAST                'self'
              190  LOAD_ATTR                buffer
              192  LOAD_CONST               None
              194  LOAD_CONST               None
              196  LOAD_CONST               -1
              198  BUILD_SLICE_3         3 
              200  BINARY_SUBSCR    
              202  LOAD_METHOD              copy
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  LOAD_FAST                'self'
              208  STORE_ATTR               buffer
              210  JUMP_FORWARD        294  'to 294'
            212_0  COME_FROM           186  '186'

 L.2550       212  LOAD_FAST                'it'
              214  LOAD_CONST               1
              216  COMPARE_OP               ==
          218_220  POP_JUMP_IF_FALSE   480  'to 480'

 L.2551       222  LOAD_FAST                'self'
              224  LOAD_ATTR                buffer
              226  LOAD_CONST               None
              228  LOAD_CONST               None
              230  LOAD_CONST               -1
              232  BUILD_SLICE_3         3 
              234  BINARY_SUBSCR    
              236  LOAD_METHOD              copy
              238  CALL_METHOD_0         0  '0 positional arguments'
              240  STORE_FAST               'v'

 L.2552       242  LOAD_FAST                'v'
              244  LOAD_CONST               1
              246  LOAD_CONST               None
              248  LOAD_CONST               2
              250  BUILD_SLICE_3         3 
              252  BINARY_SUBSCR    
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                buffer
              258  LOAD_CONST               None
              260  LOAD_CONST               None
              262  LOAD_CONST               2
              264  BUILD_SLICE_3         3 
              266  STORE_SUBSCR     

 L.2553       268  LOAD_FAST                'v'
              270  LOAD_CONST               None
              272  LOAD_CONST               None
              274  LOAD_CONST               2
              276  BUILD_SLICE_3         3 
              278  BINARY_SUBSCR    
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                buffer
              284  LOAD_CONST               1
              286  LOAD_CONST               None
              288  LOAD_CONST               2
              290  BUILD_SLICE_3         3 
              292  STORE_SUBSCR     
            294_0  COME_FROM           210  '210'
              294  JUMP_FORWARD       1036  'to 1036'
            296_0  COME_FROM           176  '176'

 L.2554       296  LOAD_FAST                'todo'
              298  LOAD_CONST               2
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE  1036  'to 1036'

 L.2555       306  LOAD_FAST                'it'
              308  LOAD_CONST               0
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   348  'to 348'

 L.2556       316  LOAD_FAST                'self'
              318  LOAD_ATTR                buffer
              320  LOAD_CONST               None
              322  LOAD_CONST               None
              324  BUILD_SLICE_2         2 
              326  LOAD_CONST               None
              328  LOAD_CONST               None
              330  LOAD_CONST               -1
              332  BUILD_SLICE_3         3 
              334  BUILD_TUPLE_2         2 
              336  BINARY_SUBSCR    
              338  LOAD_METHOD              copy
              340  CALL_METHOD_0         0  '0 positional arguments'
              342  LOAD_FAST                'self'
              344  STORE_ATTR               buffer
              346  JUMP_FORWARD       1036  'to 1036'
            348_0  COME_FROM           312  '312'

 L.2557       348  LOAD_FAST                'it'
              350  LOAD_CONST               1
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   472  'to 472'

 L.2558       358  LOAD_FAST                'self'
              360  LOAD_ATTR                buffer
              362  LOAD_CONST               None
              364  LOAD_CONST               None
              366  BUILD_SLICE_2         2 
              368  LOAD_CONST               None
              370  LOAD_CONST               None
              372  LOAD_CONST               -1
              374  BUILD_SLICE_3         3 
              376  BUILD_TUPLE_2         2 
              378  BINARY_SUBSCR    
              380  LOAD_METHOD              copy
              382  CALL_METHOD_0         0  '0 positional arguments'
              384  STORE_FAST               'v'

 L.2559       386  LOAD_FAST                'v'
              388  LOAD_CONST               None
              390  LOAD_CONST               None
              392  BUILD_SLICE_2         2 
              394  LOAD_CONST               1
              396  LOAD_CONST               None
              398  LOAD_CONST               2
              400  BUILD_SLICE_3         3 
              402  BUILD_TUPLE_2         2 
              404  BINARY_SUBSCR    
              406  LOAD_FAST                'self'
              408  LOAD_ATTR                buffer
              410  LOAD_CONST               None
              412  LOAD_CONST               None
              414  BUILD_SLICE_2         2 
              416  LOAD_CONST               None
              418  LOAD_CONST               None
              420  LOAD_CONST               2
              422  BUILD_SLICE_3         3 
              424  BUILD_TUPLE_2         2 
              426  STORE_SUBSCR     

 L.2560       428  LOAD_FAST                'v'
              430  LOAD_CONST               None
              432  LOAD_CONST               None
              434  BUILD_SLICE_2         2 
              436  LOAD_CONST               None
              438  LOAD_CONST               None
              440  LOAD_CONST               2
              442  BUILD_SLICE_3         3 
              444  BUILD_TUPLE_2         2 
              446  BINARY_SUBSCR    
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                buffer
              452  LOAD_CONST               None
              454  LOAD_CONST               None
              456  BUILD_SLICE_2         2 
              458  LOAD_CONST               1
              460  LOAD_CONST               None
              462  LOAD_CONST               2
              464  BUILD_SLICE_3         3 
              466  BUILD_TUPLE_2         2 
              468  STORE_SUBSCR     
              470  JUMP_FORWARD       1036  'to 1036'
            472_0  COME_FROM           354  '354'

 L.2562       472  LOAD_GLOBAL              NPKError
              474  LOAD_STR                 'internal error'
              476  CALL_FUNCTION_1       1  '1 positional argument'
              478  RAISE_VARARGS_1       1  'exception instance'
            480_0  COME_FROM           218  '218'
          480_482  JUMP_FORWARD       1036  'to 1036'
            484_0  COME_FROM           166  '166'

 L.2563       484  LOAD_FAST                'self'
              486  LOAD_ATTR                dim
              488  LOAD_CONST               3
              490  COMPARE_OP               ==
          492_494  POP_JUMP_IF_FALSE  1024  'to 1024'

 L.2564       496  LOAD_FAST                'todo'
              498  LOAD_CONST               1
              500  COMPARE_OP               ==
          502_504  POP_JUMP_IF_FALSE   674  'to 674'

 L.2565       506  LOAD_FAST                'it'
              508  LOAD_CONST               0
              510  COMPARE_OP               ==
          512_514  POP_JUMP_IF_FALSE   548  'to 548'

 L.2566       516  LOAD_FAST                'self'
              518  LOAD_ATTR                buffer
              520  LOAD_CONST               None
              522  LOAD_CONST               None
              524  BUILD_SLICE_2         2 
              526  LOAD_CONST               None
              528  LOAD_CONST               None
              530  LOAD_CONST               -1
              532  BUILD_SLICE_3         3 
              534  BUILD_TUPLE_2         2 
              536  BINARY_SUBSCR    
              538  LOAD_METHOD              copy
              540  CALL_METHOD_0         0  '0 positional arguments'
              542  LOAD_FAST                'self'
              544  STORE_ATTR               buffer
              546  JUMP_ABSOLUTE      1036  'to 1036'
            548_0  COME_FROM           512  '512'

 L.2567       548  LOAD_FAST                'it'
              550  LOAD_CONST               1
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_FALSE  1022  'to 1022'

 L.2568       558  LOAD_FAST                'self'
              560  LOAD_ATTR                buffer
              562  LOAD_CONST               None
              564  LOAD_CONST               None
              566  BUILD_SLICE_2         2 
              568  LOAD_CONST               None
              570  LOAD_CONST               None
              572  LOAD_CONST               -1
              574  BUILD_SLICE_3         3 
              576  BUILD_TUPLE_2         2 
              578  BINARY_SUBSCR    
              580  LOAD_METHOD              copy
              582  CALL_METHOD_0         0  '0 positional arguments'
              584  STORE_FAST               'v'

 L.2569       586  LOAD_FAST                'v'
              588  LOAD_CONST               None
              590  LOAD_CONST               None
              592  BUILD_SLICE_2         2 
              594  LOAD_CONST               1
              596  LOAD_CONST               None
              598  LOAD_CONST               2
              600  BUILD_SLICE_3         3 
              602  BUILD_TUPLE_2         2 
              604  BINARY_SUBSCR    
              606  LOAD_FAST                'self'
              608  LOAD_ATTR                buffer
              610  LOAD_CONST               None
              612  LOAD_CONST               None
              614  BUILD_SLICE_2         2 
              616  LOAD_CONST               None
              618  LOAD_CONST               None
              620  LOAD_CONST               2
              622  BUILD_SLICE_3         3 
              624  BUILD_TUPLE_2         2 
              626  STORE_SUBSCR     

 L.2570       628  LOAD_FAST                'v'
              630  LOAD_CONST               None
              632  LOAD_CONST               None
              634  BUILD_SLICE_2         2 
              636  LOAD_CONST               None
              638  LOAD_CONST               None
              640  LOAD_CONST               2
              642  BUILD_SLICE_3         3 
              644  BUILD_TUPLE_2         2 
              646  BINARY_SUBSCR    
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                buffer
              652  LOAD_CONST               None
              654  LOAD_CONST               None
              656  BUILD_SLICE_2         2 
              658  LOAD_CONST               1
              660  LOAD_CONST               None
              662  LOAD_CONST               2
              664  BUILD_SLICE_3         3 
              666  BUILD_TUPLE_2         2 
              668  STORE_SUBSCR     
          670_672  JUMP_ABSOLUTE      1036  'to 1036'
            674_0  COME_FROM           502  '502'

 L.2571       674  LOAD_FAST                'todo'
              676  LOAD_CONST               2
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_FALSE   802  'to 802'

 L.2572       684  LOAD_FAST                'it'
              686  LOAD_CONST               0
              688  COMPARE_OP               ==
          690_692  POP_JUMP_IF_FALSE   718  'to 718'

 L.2573       694  LOAD_FAST                'self'
              696  LOAD_ATTR                buffer
              698  LOAD_CONST               None
              700  LOAD_CONST               None
              702  LOAD_CONST               -1
              704  BUILD_SLICE_3         3 
              706  BINARY_SUBSCR    
              708  LOAD_METHOD              copy
              710  CALL_METHOD_0         0  '0 positional arguments'
              712  LOAD_FAST                'self'
              714  STORE_ATTR               buffer
              716  JUMP_FORWARD        800  'to 800'
            718_0  COME_FROM           690  '690'

 L.2574       718  LOAD_FAST                'it'
              720  LOAD_CONST               1
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE  1022  'to 1022'

 L.2575       728  LOAD_FAST                'self'
              730  LOAD_ATTR                buffer
              732  LOAD_CONST               None
              734  LOAD_CONST               None
              736  LOAD_CONST               -1
              738  BUILD_SLICE_3         3 
              740  BINARY_SUBSCR    
              742  LOAD_METHOD              copy
              744  CALL_METHOD_0         0  '0 positional arguments'
              746  STORE_FAST               'v'

 L.2576       748  LOAD_FAST                'v'
              750  LOAD_CONST               1
              752  LOAD_CONST               None
              754  LOAD_CONST               2
              756  BUILD_SLICE_3         3 
              758  BINARY_SUBSCR    
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                buffer
              764  LOAD_CONST               None
              766  LOAD_CONST               None
              768  LOAD_CONST               2
              770  BUILD_SLICE_3         3 
              772  STORE_SUBSCR     

 L.2577       774  LOAD_FAST                'v'
              776  LOAD_CONST               None
              778  LOAD_CONST               None
              780  LOAD_CONST               2
              782  BUILD_SLICE_3         3 
              784  BINARY_SUBSCR    
              786  LOAD_FAST                'self'
              788  LOAD_ATTR                buffer
              790  LOAD_CONST               1
              792  LOAD_CONST               None
              794  LOAD_CONST               2
              796  BUILD_SLICE_3         3 
              798  STORE_SUBSCR     
            800_0  COME_FROM           716  '716'
              800  JUMP_FORWARD       1022  'to 1022'
            802_0  COME_FROM           680  '680'

 L.2578       802  LOAD_FAST                'todo'
              804  LOAD_CONST               3
              806  COMPARE_OP               ==
          808_810  POP_JUMP_IF_FALSE  1036  'to 1036'

 L.2579       812  LOAD_FAST                'it'
              814  LOAD_CONST               0
              816  COMPARE_OP               ==
          818_820  POP_JUMP_IF_FALSE   860  'to 860'

 L.2580       822  LOAD_FAST                'self'
              824  LOAD_ATTR                buffer
              826  LOAD_CONST               None
              828  LOAD_CONST               None
              830  BUILD_SLICE_2         2 
              832  LOAD_CONST               None
              834  LOAD_CONST               None
              836  BUILD_SLICE_2         2 
              838  LOAD_CONST               None
              840  LOAD_CONST               None
              842  LOAD_CONST               -1
              844  BUILD_SLICE_3         3 
              846  BUILD_TUPLE_3         3 
            848_0  COME_FROM           294  '294'
              848  BINARY_SUBSCR    
              850  LOAD_METHOD              copy
              852  CALL_METHOD_0         0  '0 positional arguments'
              854  LOAD_FAST                'self'
              856  STORE_ATTR               buffer
              858  JUMP_FORWARD       1022  'to 1022'
            860_0  COME_FROM           818  '818'

 L.2581       860  LOAD_FAST                'it'
              862  LOAD_CONST               1
              864  COMPARE_OP               ==
          866_868  POP_JUMP_IF_FALSE  1014  'to 1014'

 L.2582       870  LOAD_FAST                'self'
              872  LOAD_ATTR                buffer
              874  LOAD_CONST               None
              876  LOAD_CONST               None
              878  BUILD_SLICE_2         2 
              880  LOAD_CONST               None
              882  LOAD_CONST               None
              884  BUILD_SLICE_2         2 
              886  LOAD_CONST               None
              888  LOAD_CONST               None
              890  LOAD_CONST               -1
              892  BUILD_SLICE_3         3 
              894  BUILD_TUPLE_3         3 
              896  BINARY_SUBSCR    
              898  LOAD_METHOD              copy
            900_0  COME_FROM           346  '346'
              900  CALL_METHOD_0         0  '0 positional arguments'
              902  STORE_FAST               'v'

 L.2583       904  LOAD_FAST                'v'
              906  LOAD_CONST               None
              908  LOAD_CONST               None
              910  BUILD_SLICE_2         2 
              912  LOAD_CONST               None
              914  LOAD_CONST               None
              916  BUILD_SLICE_2         2 
              918  LOAD_CONST               1
              920  LOAD_CONST               None
              922  LOAD_CONST               2
              924  BUILD_SLICE_3         3 
              926  BUILD_TUPLE_3         3 
              928  BINARY_SUBSCR    
              930  LOAD_FAST                'self'
              932  LOAD_ATTR                buffer
              934  LOAD_CONST               None
              936  LOAD_CONST               None
              938  BUILD_SLICE_2         2 
              940  LOAD_CONST               None
            942_0  COME_FROM            62  '62'
              942  LOAD_CONST               None
              944  BUILD_SLICE_2         2 
              946  LOAD_CONST               None
              948  LOAD_CONST               None
              950  LOAD_CONST               2
              952  BUILD_SLICE_3         3 
              954  BUILD_TUPLE_3         3 
              956  STORE_SUBSCR     

 L.2584       958  LOAD_FAST                'v'
              960  LOAD_CONST               None
              962  LOAD_CONST               None
              964  BUILD_SLICE_2         2 
              966  LOAD_CONST               None
              968  LOAD_CONST               None
              970  BUILD_SLICE_2         2 
              972  LOAD_CONST               None
              974  LOAD_CONST               None
              976  LOAD_CONST               2
              978  BUILD_SLICE_3         3 
              980  BUILD_TUPLE_3         3 
              982  BINARY_SUBSCR    
              984  LOAD_FAST                'self'
              986  LOAD_ATTR                buffer
              988  LOAD_CONST               None
              990  LOAD_CONST               None
              992  BUILD_SLICE_2         2 
              994  LOAD_CONST               None
              996  LOAD_CONST               None
              998  BUILD_SLICE_2         2 
             1000  LOAD_CONST               1
             1002  LOAD_CONST               None
             1004  LOAD_CONST               2
             1006  BUILD_SLICE_3         3 
             1008  BUILD_TUPLE_3         3 
             1010  STORE_SUBSCR     
             1012  JUMP_FORWARD       1022  'to 1022'
           1014_0  COME_FROM           866  '866'

 L.2586      1014  LOAD_GLOBAL              NPKError
             1016  LOAD_STR                 'internal error'
             1018  CALL_FUNCTION_1       1  '1 positional argument'
             1020  RAISE_VARARGS_1       1  'exception instance'
           1022_0  COME_FROM          1012  '1012'
           1022_1  COME_FROM           858  '858'
           1022_2  COME_FROM           800  '800'
           1022_3  COME_FROM           724  '724'
           1022_4  COME_FROM           554  '554'
             1022  JUMP_FORWARD       1036  'to 1036'
           1024_0  COME_FROM           492  '492'
           1024_1  COME_FROM           470  '470'
           1024_2  COME_FROM           144  '144'

 L.2588      1024  LOAD_GLOBAL              print
             1026  LOAD_STR                 'This should never happen '
             1028  LOAD_FAST                'self'
             1030  LOAD_ATTR                dim
             1032  CALL_FUNCTION_2       2  '2 positional arguments'
             1034  POP_TOP          
           1036_0  COME_FROM          1022  '1022'
           1036_1  COME_FROM           808  '808'
           1036_2  COME_FROM           480  '480'
           1036_3  COME_FROM           302  '302'
           1036_4  COME_FROM           154  '154'

 L.2589      1036  LOAD_FAST                'self'
             1038  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 848_0

    def conjg--- This code section failed: ---

 L.2595         0  LOAD_FAST                'self'
                2  LOAD_METHOD              test_axis
                4  LOAD_FAST                'axis'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'todo'

 L.2596        10  LOAD_FAST                'self'
               12  LOAD_METHOD              axes
               14  LOAD_FAST                'todo'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  LOAD_ATTR                itype
               20  LOAD_CONST               1
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L.2597        26  LOAD_GLOBAL              NPKError
               28  LOAD_STR                 'wrong itype'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L.2598        34  LOAD_FAST                'self'
               36  LOAD_ATTR                dim
               38  LOAD_CONST               1
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    70  'to 70'

 L.2599        44  LOAD_FAST                'self'
               46  LOAD_ATTR                buffer
               48  LOAD_CONST               1
               50  LOAD_CONST               None
               52  LOAD_CONST               2
               54  BUILD_SLICE_3         3 
               56  DUP_TOP_TWO      
               58  BINARY_SUBSCR    
               60  LOAD_CONST               -1
               62  INPLACE_MULTIPLY 
               64  ROT_THREE        
               66  STORE_SUBSCR     
               68  JUMP_FORWARD        206  'to 206'
             70_0  COME_FROM            42  '42'

 L.2600        70  LOAD_FAST                'self'
               72  LOAD_ATTR                dim
               74  LOAD_CONST               2
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   198  'to 198'

 L.2601        80  LOAD_FAST                'todo'
               82  LOAD_CONST               2
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   138  'to 138'

 L.2602        88  SETUP_LOOP          196  'to 196'
               90  LOAD_GLOBAL              xrange
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                size1
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  GET_ITER         
              100  FOR_ITER            134  'to 134'
              102  STORE_FAST               'i'

 L.2603       104  LOAD_FAST                'self'
              106  LOAD_ATTR                buffer
              108  LOAD_FAST                'i'
              110  LOAD_CONST               1
              112  LOAD_CONST               None
              114  LOAD_CONST               2
              116  BUILD_SLICE_3         3 
              118  BUILD_TUPLE_2         2 
              120  DUP_TOP_TWO      
              122  BINARY_SUBSCR    
              124  LOAD_CONST               -1
              126  INPLACE_MULTIPLY 
              128  ROT_THREE        
              130  STORE_SUBSCR     
              132  JUMP_BACK           100  'to 100'
              134  POP_BLOCK        
              136  JUMP_ABSOLUTE       206  'to 206'
            138_0  COME_FROM            86  '86'

 L.2604       138  LOAD_FAST                'todo'
              140  LOAD_CONST               1
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   206  'to 206'

 L.2605       146  SETUP_LOOP          206  'to 206'
              148  LOAD_GLOBAL              xrange
              150  LOAD_CONST               1
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                size1
              156  LOAD_CONST               2
              158  CALL_FUNCTION_3       3  '3 positional arguments'
              160  GET_ITER         
              162  FOR_ITER            194  'to 194'
              164  STORE_FAST               'i'

 L.2606       166  LOAD_FAST                'self'
              168  LOAD_ATTR                buffer
              170  LOAD_FAST                'i'
              172  LOAD_CONST               None
              174  LOAD_CONST               None
              176  BUILD_SLICE_2         2 
              178  BUILD_TUPLE_2         2 
              180  DUP_TOP_TWO      
              182  BINARY_SUBSCR    
              184  LOAD_CONST               -1
              186  INPLACE_MULTIPLY 
              188  ROT_THREE        
              190  STORE_SUBSCR     
              192  JUMP_BACK           162  'to 162'
              194  POP_BLOCK        
            196_0  COME_FROM_LOOP      146  '146'
            196_1  COME_FROM_LOOP       88  '88'
              196  JUMP_FORWARD        206  'to 206'
            198_0  COME_FROM            78  '78'

 L.2608       198  LOAD_GLOBAL              NPKError
              200  LOAD_STR                 'a faire'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           196  '196'
            206_1  COME_FROM           144  '144'
            206_2  COME_FROM            68  '68'

 L.2609       206  LOAD_FAST                'self'
              208  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 196_1

    def revf--- This code section failed: ---

 L.2619         0  LOAD_FAST                'self'
                2  LOAD_METHOD              test_axis
                4  LOAD_FAST                'axis'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'todo'

 L.2620        10  LOAD_FAST                'self'
               12  LOAD_ATTR                dim
               14  LOAD_CONST               1
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    70  'to 70'

 L.2621        20  LOAD_FAST                'self'
               22  LOAD_ATTR                buffer
               24  LOAD_CONST               2
               26  LOAD_CONST               None
               28  LOAD_CONST               4
               30  BUILD_SLICE_3         3 
               32  DUP_TOP_TWO      
               34  BINARY_SUBSCR    
               36  LOAD_CONST               -1
               38  INPLACE_MULTIPLY 
               40  ROT_THREE        
               42  STORE_SUBSCR     

 L.2622        44  LOAD_FAST                'self'
               46  LOAD_ATTR                buffer
               48  LOAD_CONST               3
               50  LOAD_CONST               None
               52  LOAD_CONST               4
               54  BUILD_SLICE_3         3 
               56  DUP_TOP_TWO      
               58  BINARY_SUBSCR    
               60  LOAD_CONST               -1
               62  INPLACE_MULTIPLY 
               64  ROT_THREE        
               66  STORE_SUBSCR     
               68  JUMP_FORWARD        268  'to 268'
             70_0  COME_FROM            18  '18'

 L.2623        70  LOAD_FAST                'self'
               72  LOAD_ATTR                dim
               74  LOAD_CONST               2
               76  COMPARE_OP               ==
            78_80  POP_JUMP_IF_FALSE   260  'to 260'

 L.2624        82  LOAD_FAST                'todo'
               84  LOAD_CONST               2
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   168  'to 168'

 L.2625        90  SETUP_LOOP          258  'to 258'
               92  LOAD_GLOBAL              xrange
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                size1
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  GET_ITER         
              102  FOR_ITER            164  'to 164'
              104  STORE_FAST               'i'

 L.2626       106  LOAD_FAST                'self'
              108  LOAD_ATTR                buffer
              110  LOAD_FAST                'i'
              112  LOAD_CONST               2
              114  LOAD_CONST               None
              116  LOAD_CONST               4
              118  BUILD_SLICE_3         3 
              120  BUILD_TUPLE_2         2 
              122  DUP_TOP_TWO      
              124  BINARY_SUBSCR    
              126  LOAD_CONST               -1
              128  INPLACE_MULTIPLY 
              130  ROT_THREE        
              132  STORE_SUBSCR     

 L.2627       134  LOAD_FAST                'self'
              136  LOAD_ATTR                buffer
              138  LOAD_FAST                'i'
              140  LOAD_CONST               3
              142  LOAD_CONST               None
              144  LOAD_CONST               4
              146  BUILD_SLICE_3         3 
              148  BUILD_TUPLE_2         2 
              150  DUP_TOP_TWO      
              152  BINARY_SUBSCR    
              154  LOAD_CONST               -1
              156  INPLACE_MULTIPLY 
              158  ROT_THREE        
              160  STORE_SUBSCR     
              162  JUMP_BACK           102  'to 102'
              164  POP_BLOCK        
              166  JUMP_FORWARD        258  'to 258'
            168_0  COME_FROM            88  '88'

 L.2628       168  LOAD_FAST                'todo'
              170  LOAD_CONST               1
              172  COMPARE_OP               ==
          174_176  POP_JUMP_IF_FALSE   268  'to 268'

 L.2629       178  SETUP_LOOP          268  'to 268'
              180  LOAD_GLOBAL              xrange
              182  LOAD_CONST               2
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                size1
              188  LOAD_CONST               4
              190  CALL_FUNCTION_3       3  '3 positional arguments'
              192  GET_ITER         
              194  FOR_ITER            256  'to 256'
              196  STORE_FAST               'i'

 L.2630       198  LOAD_FAST                'self'
              200  LOAD_ATTR                buffer
              202  LOAD_FAST                'i'
              204  LOAD_CONST               None
              206  LOAD_CONST               None
              208  BUILD_SLICE_2         2 
              210  BUILD_TUPLE_2         2 
              212  DUP_TOP_TWO      
              214  BINARY_SUBSCR    
              216  LOAD_CONST               -1
              218  INPLACE_MULTIPLY 
              220  ROT_THREE        
              222  STORE_SUBSCR     

 L.2631       224  LOAD_FAST                'self'
              226  LOAD_ATTR                buffer
              228  LOAD_FAST                'i'
              230  LOAD_CONST               1
              232  BINARY_ADD       
              234  LOAD_CONST               None
              236  LOAD_CONST               None
              238  BUILD_SLICE_2         2 
              240  BUILD_TUPLE_2         2 
              242  DUP_TOP_TWO      
              244  BINARY_SUBSCR    
              246  LOAD_CONST               -1
              248  INPLACE_MULTIPLY 
              250  ROT_THREE        
              252  STORE_SUBSCR     
              254  JUMP_BACK           194  'to 194'
              256  POP_BLOCK        
            258_0  COME_FROM_LOOP      178  '178'
            258_1  COME_FROM           166  '166'
            258_2  COME_FROM_LOOP       90  '90'
              258  JUMP_FORWARD        268  'to 268'
            260_0  COME_FROM            78  '78'

 L.2633       260  LOAD_GLOBAL              NPKError
              262  LOAD_STR                 'a faire'
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  RAISE_VARARGS_1       1  'exception instance'
            268_0  COME_FROM           258  '258'
            268_1  COME_FROM           174  '174'
            268_2  COME_FROM            68  '68'

 L.2634       268  LOAD_FAST                'self'
              270  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 258_2

    def kaiser(self, beta, axis=0):
        """
        apply a Kaiser apodisation
        beta is a positive number

            beta    Window shape
            ----    ------------
            0       Rectangular
            5       Similar to a Hamming
            6       Similar to a Hanning
            8.6     Similar to a Blackman
        """
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        size = self.axes(todo).size
        if it == 1:
            size = size // 2
        e = np.kaiser(size, beta)
        if it == 1:
            e = as_float(complex(1.0, 1.0) * e)
        return self.apod_apply(axis, e)

    def hamming(self, axis=0):
        """
        apply a Hamming apodisation
        """
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        sw = self.axes(todo).specwidth
        size = self.axes(todo).size
        if it == 1:
            size = size // 2
        e = np.hamming(size)
        if it == 1:
            e = as_float(complex(1.0, 1.0) * e)
        return self.apod_apply(axis, e)

    def hanning(self, axis=0):
        """
        apply a Hanning apodisation
        """
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        sw = self.axes(todo).specwidth
        size = self.axes(todo).size
        if it == 1:
            size = size // 2
        e = np.hanning(size)
        if it == 1:
            e = as_float(complex(1.0, 1.0) * e)
        return self.apod_apply(axis, e)

    def apod_gm(self, gb, axis=0):
        """
        apply an gaussian apodisation, gb is in Hz
        WARNING : different from common definition of apodisation
        """
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        sw = self.axes(todo).specwidth
        size = self.axes(todo).size
        if it == 1:
            size = size // 2
        e = np.exp(-(gb * np.arange(size) / sw) ** 2)
        if it == 1:
            e = as_float(complex(1.0, 1.0) * e)
        return self.apod_apply(axis, e)

    def apod_tm(self, tm1, tm2, axis=0):
        """
        apply a trapezoide apodisation, lb is in Hz
        WARNING : different from common definition of apodisation
        This commands applies a trapezoid filter function to the data-
        set. The function raises from 0.0 to 1.0 from the first point to 
        point n1. The function then stays to 1.0 until point n2, from which 
        it goes down to 0.0 at the last point.
        If in 2D or 3D then Fx tells on which axis to apply the filter.
        """
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        size = self.axes(todo).size
        if it == 1:
            tm1 = min(size, 2 * (tm1 // 2) + 1)
            tm2 = 2 * (tm2 // 2) + 1
        ftm1 = tm1
        ftm2 = size - tm2 + 1
        e = np.zeros(size)
        if it == 0:
            for i in range(1, ftm1):
                e[i] = float(i) / ftm1 + 1

            for i in range(ftm1, tm2):
                e[i] = 1.0

            for i in range(tm2, size):
                e[i] = float(i) / size

            print('****** ', e[0])
        else:
            if it == 1:
                for i in range(1, ftm1, 2):
                    e[i] = float(i) / ftm1
                    e[i + 1] = float(i) / ftm1

                for i in range(ftm1, tm2, 2):
                    e[i] = 1.0
                    e[i + 1] = 1.0

                for i in range(tm2, size - 1, 2):
                    e[i] = float(size - i + 1) / ftm2
                    e[i + 1] = float(size - i + 1) / ftm2

            print('APOD_TM still to be doublechecked', e)

    def apod_em(self, lb, axis=0):
        """
        apply an exponential apodisation, lb is in Hz
        WARNING : different from common definition of apodisation
        """
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        sw = self.axes(todo).specwidth
        size = self.axes(todo).size
        if it == 1:
            size = size // 2
        e = np.exp(-lb * np.arange(size) / sw)
        if it == 1:
            e = as_float(complex(1.0, 1.0) * e)
        return self.apod_apply(axis, e)

    def apod_sq_sin(self, maxi=0.0, axis=0):
        """
        apply a squared sinebell apodisation
        maxi ranges from 0 to 0.5
        """
        import math as m
        if maxi < 0.0 or maxi > 0.5:
            raise ValueError
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        size = self.axes(todo).size
        if it == 1:
            size = size // 2
        s = 2 * (1 - maxi)
        zz = m.pi / ((size - 1) * s)
        yy = m.pi * (s - 1) / s
        e = np.sin(zz * np.arange(size) + yy) ** 2
        if it == 1:
            e = as_float(complex(1.0, 1.0) * e)
        return self.apod_apply(axis, e)

    def apod_sin(self, maxi=0.0, axis=0):
        """
        apply a sinebell apodisation
        maxi ranges from 0 to 0.5
        """
        import math as m
        if maxi < 0.0 or maxi > 0.5:
            raise ValueError
        todo = self.test_axis(axis)
        it = self.axes(todo).itype
        size = self.axes(todo).size
        if it == 1:
            size = size // 2
        s = 2 * (1 - maxi)
        zz = m.pi / ((size - 1) * s)
        yy = m.pi * (s - 1) / s
        e = np.sin(zz * np.arange(size) + yy)
        if it == 1:
            e = as_float(complex(1.0, 1.0) * e)
        return self.apod_apply(axis, e)

    def apod_apply(self, axis, apod_buf):
        """
        apply an apodisation, held into the buffer apod_buf
        """
        todo = self.test_axis(axis)
        if self.dim == 1:
            self.buffer = self.buffer * apod_buf
        if self.dim == 2:
            if todo == 2:
                self.buffer = self.buffer * apod_buf
            if todo == 1:
                for i in xrange(self.size2):
                    self.buffer[:, i] = self.buffer[:, i] * apod_buf

        if self.dim == 3:
            if todo == 3:
                self.buffer = self.buffer * apod_buf
            if todo == 2:
                for i in xrange(self.size1):
                    for j in xrange(self.size3):
                        self.buffer[i, :, j] = self.buffer[i, :, j] * apod_buf

            if todo == 1:
                for i in xrange(self.size2):
                    for j in xrange(self.size3):
                        self.buffer[:, i, j] = self.buffer[:, i, j] * apod_buf

        return self

    def mult_by_vector(self, axis, vector, mode='real'):
        """
        multiply the data-set by a vector, along a given axis
        if mode == "real", does it point by point regardles of itype
        if mode == "complex" uses axis.itype to determine how handle complex values
            in all cases vector can be real or complex
        """
        todo = self.test_axis(axis)
        if mode == 'complex':
            if self.axes(todo).itype == 1:
                tf = as_cpx
            else:
                tf = as_float
        elif mode == 'real':
            raise NPKError('reste a faire')
        else:
            raise NPKError('error with mode', data=self)
        if self.dim == 1:
            self.buffer = as_float(tf(self.buffer) * vector)
        if self.dim == 2:
            if todo == 2:
                self.buffer = as_float(tf(self.buffer) * vector)
            if todo == 1:
                for i in xrange(self.size2):
                    self.buffer[:, i] = as_float(tf(self.buffer[:, i].copy()) * vector)

        if self.dim == 3:
            print('A VERIFIER')
            if todo == 3:
                self.buffer = as_float(tf(self.buffer) * vector)
            if todo == 2:
                for i in xrange(self.size1):
                    for j in xrange(self.size3):
                        self.buffer[i, :, j] = as_float(tf(self.buffer[i, :, j].copy()) * vector)

            if todo == 1:
                for i in xrange(self.size2):
                    for j in xrange(self.size3):
                        self.buffer[:, i, j] = as_float(tf(self.buffer[:, i, j].copy()) * vector)

        self._absmax = 0.0
        return self

    def median(self):
        """
        Executes a median filter on the data-set (1D or 2D).a window of x 
        points (or y by x in 2D) is moved along the data set, the point are 
        ordered, and the indexth point is taken as the new point for the 
        data set.
        """
        pass

    def modulus(self):
        """
        takes the modulus of the dataset
        depends on the value f axis(i).itype
        """
        if self.dim == 1:
            if self.axis1.itype != 1:
                raise NPKError('wrong itype', data=self)
            d = as_cpx(self.buffer)
            self.buffer = np.real(np.sqrt(d * d.conj()))
            self.axis1.itype = 0
        else:
            if self.dim == 2:
                if self.axis1.itype == 0:
                    if self.axis2.itype == 0:
                        print('real data, nothing to do')
                    elif self.axis1.itype == 1 and self.axis2.itype == 0:
                        b = np.zeros((self.size1 // 2, self.size2))
                        for i in xrange(0, self.size1, 2):
                            dr = self.buffer[i, :]
                            di = self.buffer[i + 1, :]
                            b[i // 2, :] = np.sqrt(dr ** 2 + di ** 2)

                        self.axis1.itype = 0
                elif self.axis1.itype == 0 and self.axis2.itype == 1:
                    b = np.zeros((self.size1, self.size2 // 2))
                    for i in xrange(self.size1):
                        d = as_cpx(self.buffer[i, :])
                        b[i, :] = np.sqrt(np.real(d * d.conj()))

                    self.axis2.itype = 0
                else:
                    if self.axis1.itype == 1:
                        if self.axis2.itype == 1:
                            self.axis1.itype = 0
                            self.axis2.itype = 0
                            b = hypercomplex_modulus(self.get_buffer(), self.size1, self.size2)
                self.buffer = b
            else:
                if self.dim == 3:
                    raise NPKError('reste a faire')
                self._absmax = 0.0
                self.adapt_size()
                return self


class NPKDataTests(unittest.TestCase):
    __doc__ = ' - Testing NPKData basic behaviour - '

    def test_fft(self):
        """ - Testing FFT methods - """
        x = np.arange(1024.0)
        E = _NPKData(buffer=x)
        E.axis1.itype = 0
        E.ifftr()
        sim = np.exp(-x * complex(0.1, 1.0))
        D = _NPKData(buffer=sim)
        p = 0
        D1 = D.copy().phase(p, 0).chsize(2 * D.size1).fft().real()
        D2 = D.copy().phase(p, 0).fftr()
        D3 = D2.ifftr()
        D.phase(p, 0).add(D3.mult(-1))
        print('ecart max :', np.max(D.get_buffer()))
        print('ecart moyen :', np.mean(D.get_buffer()))
        self.assertTrue(np.max(D.get_buffer()) < 1e-14)
        self.assertTrue(np.mean(D.get_buffer()) < 1e-14)

    def test_math(self):
        """ - Testing dataset arithmetics - """
        M = np.zeros((20, 20))
        d = _NPKData(buffer=M)
        d[(5, 7)] = 10
        d[(10, 12)] = 20
        d += 1
        self.assertAlmostEqual(d[(10, 12)], 21)
        e = d + 2
        self.assertAlmostEqual(e[(10, 12)], 23)
        e = d - 2
        self.assertAlmostEqual(e[(10, 12)], 19)
        f = 2 * d + e
        self.assertAlmostEqual(f[(10, 12)], 61)
        f += d
        self.assertAlmostEqual(f[(10, 12)], 82)
        f *= 3.0
        self.assertAlmostEqual(f[(10, 12)], 246)
        f = 2 * d - e
        self.assertAlmostEqual(f[(10, 12)], 23)
        re = e.row(10)
        re.axis1.itype = 1
        re *= complex(0.0, 2.0)
        self.assertAlmostEqual(re[13], 38.0)

    def test_flatten(self):
        """ test the flatten utility """
        self.assertEqual([1, 2, 3, 4, 5, 6, 7], flatten(((1, 2), 3, (4, (5,), (6, 7)))))

    def test_zf(self):
        for ty in range(2):
            d1 = _NPKData(buffer=(np.arange(6.0)))
            d2 = _NPKData(buffer=(np.zeros((6, 8))))
            for i in range(d2.size2):
                d2.set_col(i, _NPKData(buffer=(0.1 * i + np.arange(d2.size1))))

            d1.axis1.itype = ty
            d2.axis1.itype = ty
            d2.axis2.itype = 1
            if ty == 0:
                samp = np.array([0, 3, 6, 8, 10, 11])
            else:
                samp = np.array([0, 3, 5])
            d1.axis1.set_sampling(samp)
            d2.axis1.set_sampling(samp)
            self.assertTrue(d1.axis1.sampled)
            self.assertTrue(d2.axis1.sampled)
            d1.zf()
            d2.zf()
            if ty == 0:
                self.assertAlmostEqual(d1[6], 2.0)
                self.assertAlmostEqual(d1[7], 0.0)
                self.assertAlmostEqual(d2[(6, 4)], 2.4)
                self.assertAlmostEqual(d2[(7, 4)], 0.0)
            else:
                self.assertAlmostEqual(d1[6], 2.0)
                self.assertAlmostEqual(d1[7], 3.0)
                self.assertAlmostEqual(d2[(6, 4)], 2.4)
                self.assertAlmostEqual(d2[(7, 4)], 3.4)

    def test_hypercomplex_modulus(self):
        """
        Test of hypercomplex modulus
        """
        arr = np.array([[1, 4], [3, 7], [1, 9], [5, 7]])
        modulus = hypercomplex_modulus(arr, 2, 2)
        np.testing.assert_almost_equal(modulus, np.array([[np.sqrt(75)], [np.sqrt(156)]]))

    def test_dampingunit(self):
        """test itod and dtoi"""
        print(self.test_dampingunit.__doc__)
        LA = LaplaceAxis(dmin=10.0, dmax=10000.0, dfactor=35534.34765625)
        damping = LA.itod(50)
        point = LA.dtoi(damping)
        self.assertAlmostEqual(damping, 2404.099183509974)
        self.assertEqual(point, 50)

    def test_TimeAxis(self):
        """test TimeAxis"""
        print(self.test_TimeAxis.__doc__)
        N = 20
        tabval = list(np.logspace(np.log10(0.001), np.log10(3), N))
        d = _NPKData(buffer=(np.ones((N, 1000))))
        d.axis1.specwidth = 2000 * np.pi
        d.apod_sin(axis=2)
        d.apod_em(lb=1000, axis=1)
        d.axis1 = TimeAxis(size=(d.size1), tabval=tabval, scale='log')
        d.axis1.currentunit = 'msec'
        print(d.report())
        d.col(0).display(show=True, title='Testing time series')
        self.assertTrue(d.axis1.fval(12.1) > tabval[12])
        self.assertTrue(d.axis1.fval(12.9) < tabval[13])
        self.assertEqual(d.axis1.Tmin, 0.001)

    def test_plugin(self):
        """Test of plugin mechanism"""

        def toto(dd, title):
            """fake method"""
            dd.test_title = title
            return dd

        NPKData_plugin('test_pi', toto)
        d1 = _NPKData(buffer=(np.arange(6.0)))
        d1.test_pi('this is a title').rfft()
        self.assertTrue(d1.test_title == 'this is a title')


if __name__ == '__main__':
    unittest.main()