# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/tsops.py
# Compiled at: 2011-02-11 14:08:42
"""Do mathematical operations on time series, where
the two operands don't necessarily have the same
sampling times.     It finds a common sampling time
and sampling interval, then interpolates as necessary
to bring the data onto the common time axis.
"""
import math
from gmisclib import Num
from gmisclib import Numeric_gpk as NG
import gpkimgclass

class axis:
    """This class represents a time axis for a time series.
        Indices of the underlying array are assumed to be zero-based.
        """

    def __init__--- This code section failed: ---

 L.  20         0  LOAD_FAST             1  'start'
                3  LOAD_CONST               None
                6  COMPARE_OP            9  is-not
                9  POP_JUMP_IF_FALSE    96  'to 96'
               12  LOAD_FAST             4  'end'
               15  LOAD_CONST               None
               18  COMPARE_OP            9  is-not
               21  POP_JUMP_IF_FALSE    96  'to 96'
               24  LOAD_FAST             3  'n'
               27  LOAD_CONST               None
               30  COMPARE_OP            9  is-not
             33_0  COME_FROM            21  '21'
             33_1  COME_FROM             9  '9'
               33  POP_JUMP_IF_FALSE    96  'to 96'

 L.  21        36  LOAD_FAST             1  'start'
               39  LOAD_FAST             0  'self'
               42  STORE_ATTR            1  'crval'

 L.  22        45  LOAD_GLOBAL           2  'int'
               48  LOAD_GLOBAL           3  'round'
               51  LOAD_FAST             3  'n'
               54  CALL_FUNCTION_1       1  None
               57  CALL_FUNCTION_1       1  None
               60  LOAD_FAST             0  'self'
               63  STORE_ATTR            4  'n'

 L.  23        66  LOAD_FAST             4  'end'
               69  LOAD_FAST             1  'start'
               72  BINARY_SUBTRACT  
               73  LOAD_GLOBAL           5  'float'
               76  LOAD_FAST             3  'n'
               79  LOAD_CONST               1
               82  BINARY_SUBTRACT  
               83  CALL_FUNCTION_1       1  None
               86  BINARY_DIVIDE    
               87  LOAD_FAST             0  'self'
               90  STORE_ATTR            6  'cdelt'
               93  JUMP_FORWARD        199  'to 295'

 L.  24        96  LOAD_FAST             1  'start'
               99  LOAD_CONST               None
              102  COMPARE_OP            9  is-not
              105  POP_JUMP_IF_FALSE   162  'to 162'
              108  LOAD_FAST             3  'n'
              111  LOAD_CONST               None
              114  COMPARE_OP            9  is-not
              117  POP_JUMP_IF_FALSE   162  'to 162'
              120  LOAD_FAST             2  'dt'
              123  LOAD_CONST               None
              126  COMPARE_OP            9  is-not
            129_0  COME_FROM           117  '117'
            129_1  COME_FROM           105  '105'
              129  POP_JUMP_IF_FALSE   162  'to 162'

 L.  25       132  LOAD_FAST             1  'start'
              135  LOAD_FAST             0  'self'
              138  STORE_ATTR            1  'crval'

 L.  26       141  LOAD_FAST             3  'n'
              144  LOAD_FAST             0  'self'
              147  STORE_ATTR            4  'n'

 L.  27       150  LOAD_FAST             2  'dt'
              153  LOAD_FAST             0  'self'
              156  STORE_ATTR            6  'cdelt'
              159  JUMP_FORWARD        133  'to 295'

 L.  28       162  LOAD_FAST             1  'start'
              165  LOAD_CONST               None
              168  COMPARE_OP            9  is-not
              171  POP_JUMP_IF_FALSE   286  'to 286'
              174  LOAD_FAST             2  'dt'
              177  LOAD_CONST               None
              180  COMPARE_OP            9  is-not
              183  POP_JUMP_IF_FALSE   286  'to 286'
              186  LOAD_FAST             4  'end'
              189  LOAD_CONST               None
              192  COMPARE_OP            9  is-not
            195_0  COME_FROM           183  '183'
            195_1  COME_FROM           171  '171'
              195  POP_JUMP_IF_FALSE   286  'to 286'

 L.  29       198  LOAD_FAST             1  'start'
              201  LOAD_FAST             0  'self'
              204  STORE_ATTR            1  'crval'

 L.  30       207  LOAD_CONST               1
              210  LOAD_GLOBAL           7  'abs'
              213  LOAD_GLOBAL           2  'int'
              216  LOAD_GLOBAL           8  'math'
              219  LOAD_ATTR             9  'floor'
              222  LOAD_FAST             4  'end'
              225  LOAD_FAST             1  'start'
              228  BINARY_SUBTRACT  
              229  LOAD_FAST             2  'dt'
              232  BINARY_DIVIDE    
              233  CALL_FUNCTION_1       1  None
              236  CALL_FUNCTION_1       1  None
              239  CALL_FUNCTION_1       1  None
              242  BINARY_ADD       
              243  LOAD_FAST             0  'self'
              246  STORE_ATTR            4  'n'

 L.  32       249  LOAD_FAST             4  'end'
              252  LOAD_FAST             1  'start'
              255  COMPARE_OP            4  >
              258  POP_JUMP_IF_FALSE   273  'to 273'

 L.  33       261  LOAD_FAST             2  'dt'
              264  LOAD_FAST             0  'self'
              267  STORE_ATTR            6  'cdelt'
              270  JUMP_ABSOLUTE       295  'to 295'

 L.  35       273  LOAD_FAST             2  'dt'
              276  UNARY_NEGATIVE   
              277  LOAD_FAST             0  'self'
              280  STORE_ATTR            6  'cdelt'
              283  JUMP_FORWARD          9  'to 295'

 L.  37       286  LOAD_GLOBAL          10  'ValueError'
              289  LOAD_CONST               'Either silly values or not implemented.'
              292  RAISE_VARARGS_2       2  None
            295_0  COME_FROM           283  '283'
            295_1  COME_FROM           159  '159'
            295_2  COME_FROM            93  '93'

 L.  38       295  LOAD_FAST             0  'self'
              298  LOAD_ATTR             4  'n'
              301  LOAD_CONST               0
              304  COMPARE_OP            5  >=
              307  POP_JUMP_IF_TRUE    319  'to 319'
              310  LOAD_ASSERT              AssertionError
              313  LOAD_CONST               'Silly number of data'
              316  RAISE_VARARGS_2       2  None

 L.  39       319  LOAD_FAST             5  'crpix'
              322  LOAD_FAST             0  'self'
              325  STORE_ATTR           12  'crpix'

 L.  41       328  LOAD_GLOBAL           3  'round'
              331  LOAD_FAST             0  'self'
              334  LOAD_ATTR            13  'index'
              337  LOAD_FAST             0  'self'
              340  LOAD_ATTR            14  'start'
              343  CALL_FUNCTION_0       0  None
              346  CALL_FUNCTION_1       1  None
              349  CALL_FUNCTION_1       1  None
              352  LOAD_CONST               0
              355  COMPARE_OP            2  ==
              358  POP_JUMP_IF_TRUE    374  'to 374'
              361  LOAD_ASSERT              AssertionError
              364  LOAD_CONST               'start fail: %s'
              367  LOAD_FAST             0  'self'
              370  BINARY_MODULO    
              371  RAISE_VARARGS_2       2  None

 L.  42       374  LOAD_GLOBAL           3  'round'
              377  LOAD_FAST             0  'self'
              380  LOAD_ATTR            13  'index'
              383  LOAD_FAST             0  'self'
              386  LOAD_ATTR            15  'end'
              389  CALL_FUNCTION_0       0  None
              392  CALL_FUNCTION_1       1  None
              395  CALL_FUNCTION_1       1  None
              398  LOAD_FAST             0  'self'
              401  LOAD_ATTR             4  'n'
              404  LOAD_CONST               1
              407  BINARY_SUBTRACT  
              408  COMPARE_OP            2  ==
              411  POP_JUMP_IF_TRUE    427  'to 427'
              414  LOAD_ASSERT              AssertionError
              417  LOAD_CONST               'end fail: %s'
              420  LOAD_FAST             0  'self'
              423  BINARY_MODULO    
              424  RAISE_VARARGS_2       2  None
              427  LOAD_CONST               None
              430  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 427

    def N(self):
        return self.n

    def coord(self, index):
        """What is the i^th coordinate if the i^th index==index?
                More plainly, this function gives you the coordinate that
                corresponds to the index."""
        assert self.n >= 0
        return self.crval + (index - self.crpix) * self.cdelt

    def coords(self):
        """Generate an array of all the time values."""
        assert self.n >= 0
        index = Num.arrayrange(self.n)
        return index * self.cdelt + (self.crval - self.crpix * self.cdelt)

    def index(self, t, limit=False, error=True):
        assert self.n > 0
        assert self.cdelt != 0
        tmp = self.crpix + (t - self.crval) / self.cdelt
        if limit:
            rtmp = round(tmp)
            if not rtmp >= 0:
                tmp = 0.0
            elif not rtmp < self.n:
                tmp = self.n - 1.0
        elif error and not 0 <= round(tmp) < self.n:
            raise IndexError, 'coordinate out of range: %g->%.1f' % (t, tmp)
        return tmp

    def indices(self, t, limit=False, error=True):
        assert self.n > 0
        assert self.cdelt != 0
        tmp = self.crpix + (t - self.crval) / self.cdelt
        if limit:
            Num.maximum(tmp, 0.0, tmp)
            Num.minimum(tmp, self.n - 1, tmp)
        elif error:
            nbad = Num.sum(Num.less(tmp, -0.5)) + Num.sum(Num.greater(tmp, self.n - 0.5))
            if nbad:
                raise IndexError, '%d coordinates out of range' % nbad
        return tmp

    def dt(self):
        return self.cdelt

    def start(self):
        return self.coord(0)

    def end(self):
        return self.coord(self.n - 1)

    def __str__(self):
        return '<axis start=%g end=%g dt=%g n=%d>' % (self.start(), self.end(),
         self.dt(), self.N())

    __repr__ = __str__


def time(datasets, start=None, end=None):
    dts = 0.0
    dtn = 0
    for x in datasets:
        tdt = x.dt()
        dts += math.log(tdt)
        dtn += 1

    dt = math.exp(dts / dtn)
    _s = [ x.start() for x in datasets ]
    if start is not None:
        _s.append(start)
    _start = max(_s)
    _e = [ x.end() for x in datasets ]
    if end is not None:
        _e.append(end)
    _end = min(_e)
    n = int(math.floor((_end - _start) / dt))
    if n < 0:
        n = 0
    return axis(start=_start, dt=dt, n=n)


def time2(a, b):
    dt = 0.5 * (a.dt() + b.dt())
    start = max(a.start(), b.start())
    end0 = min(a.end(), b.end())
    n = int(math.floor((end0 - start) / dt))
    return axis(start=start, dt=dt, n=n)


def _fill_interp_guts(a, t, fill, interpolator):
    """Returns a Numeric array."""
    assert len(t.shape) == 1
    if a.n[2] == 0:
        return Num.zeros((t.shape[0], a.n[1]), Num.Float) + fill
    noneedfill = Num.greater_equal(t, a.start()) * Num.less_equal(t, a.end())
    assert len(noneedfill.shape) == 1
    nofillidx = Num.nonzero(noneedfill)[0]
    if nofillidx.shape != t.shape:
        ainofill = interpolator(a, Num.take(t, nofillidx, axis=0))
        out = Num.zeros((t.shape[0], a.n[1]), Num.Float) + fill
        Num.put(out, nofillidx, ainofill)
    else:
        out = interpolator(a, t)
    return out


def test_fig():
    print 'TEST_FIG'
    a = axis(start=2.0, dt=1.0, n=10)
    a.n = (0, 1, 10)
    t = Num.arrayrange(20)
    fill = -1
    ifcn = lambda a, b: 100
    q = _fill_interp_guts(a, t, fill, ifcn)
    print q
    print q.shape


def interp_fill(a, t, fill):
    return _fill_interp_guts(a, t, fill, interp)


def interpN_fill(a, t, fill):
    return _fill_interp_guts(a, t, fill, interpN)


def interp(a, t):
    """Interpolate to a specified time axis.
        This does a linear interpolation.
        @param a: data to be interpolated (a time series)
        @type a: gpkimgclass.gpk_img
        @type t: an array of times.
        @rtype: numpy array.
        @return: data interpolated onto the specified time values.
        """
    idx = a.t_index(t)
    return NG.interp(a.d, idx)


def test_interp1():
    x = Num.array([0, 1], Num.Float)
    xx = gpkimgclass.gpk_img({'CDELT2': 1.0, 'CRPIX2': 1, 'CRVAL2': 0}, x)
    t = Num.array([0.0, 0.7, 0.99, 1.0], Num.Float)
    q = interp(xx, t)
    print q.shape, t.shape, x.shape, xx.d.shape
    print q
    assert q.shape[0] == t.shape[0]
    assert len(q.shape) == len(xx.d.shape)
    assert Num.sum(Num.absolute(q - [[0.0], [0.7], [0.99], [1.0]])) < 1e-06
    qq = gpkimgclass.gpk_img({'CDELT2': 1.0, 'CRPIX2': 1, 'CRVAL2': 0}, q)
    print 'qq.n', qq.n, xx.n
    assert qq.n[1] == xx.n[1] and qq.n[2] == t.shape[0]
    qn = interpN(xx, t)
    print 'qn=', qn
    assert Num.sum(Num.absolute(qn - [[0.0], [1.0], [1.0], [1.0]])) < 1e-06


def test_interp2():
    x = Num.array([0, 1, 1.5], Num.Float)
    xx = gpkimgclass.gpk_img({'CDELT2': 1.0, 'CRPIX2': 1, 'CRVAL2': 0}, x)
    t = Num.array([0.0, 0.7, 0.99, 1.0, 1.1, 2.0], Num.Float)
    q = interp(xx, t)
    assert Num.sum(Num.absolute(q - [[0.0], [0.7], [0.99], [1.0], [1.05], [1.5]])) < 1e-06
    qn = interp(xx, t)
    assert Num.sum(Num.absolute(qn - [[0.0], [0.7], [0.99], [1.0], [1.05], [1.5]])) < 1e-06


def test_interp3():
    x = Num.array([[0, 100], [1, 101], [1.5, 101.5]], Num.Float)
    xx = gpkimgclass.gpk_img({'CDELT2': 1.0, 'CRPIX2': 1, 'CRVAL2': 0}, x)
    t = Num.array([0.0, 0.7, 0.99, 1.0, 1.1, 2.0], Num.Float)
    q = interp(xx, t)
    print q
    qq = gpkimgclass.gpk_img({'CDELT2': 1.0, 'CRPIX2': 1, 'CRVAL2': 0}, q)
    print 'qq.n', qq.n, xx.n
    assert qq.n[1] == xx.n[1] and qq.n[2] == t.shape[0]
    assert Num.sum(Num.absolute(q - [[0.0, 100.0], [0.7, 100.7], [0.99, 100.99],
     [
      1.0, 101.0], [1.05, 101.05], [1.5, 101.5]])) < 1e-06
    qn = interp(xx, t)
    assert Num.sum(Num.absolute(qn - [[0.0, 100.0], [0.7, 100.7], [0.99, 100.99],
     [
      1.0, 101.0], [1.05, 101.05], [1.5, 101.5]])) < 1e-06


def interpN(a, t):
    """Interpolate to a specified time axis via
        nearest-neighbor interpolation.
        A is a gpkimgclass, and t is an array of times.
        Returns a Numeric array, not a gpkimgclass.
        """
    idx = a.t_index(t)
    return NG.interpN(a.d, idx)


def common(data_sets, start=None, end=None):
    """Computes a common time axis for several datasets.
        Linearly interpolate as needed.
        The data sets need not be the same width, and need not have the
        same sampling interval or a common starting time.
        @param data_sets: this is a list of the data to be put on a common time axis.
        @type data_sets: L{list}(L{gpkimgclass.gpk_img})
        @param start: this allows you to restrict the output data to a smaller region.
        @param end: this allows you to restrict the output data to a smaller region.
        @type start: L{float} or L{None}
        @type end: L{float} or L{None}
        @rtype: list(numpy.ndarray) where the first ndarray is 1-D and the rest are two dimensional.
        @return: the time_axis (as a 1-D numpy array of time values),
                followed by a 2-D numpy array for each of the input data sets.
        """
    tt = time(data_sets, start=start, end=end)
    t = tt.coords()
    return [
     tt] + [ interp(x, t) for x in data_sets ]


def commonN(data_sets, start=None, end=None):
    """Put several data sets on a common time axis.
        Interpolate by choosing nearest neighbor.
        """
    tt = time(data_sets, start=start, end=end)
    t = tt.coords()
    return [
     t] + [ interpN(x, t) for x in data_sets ]


def mul(a, b, hdr_op=None):
    tt = time((a, b))
    t = tt.coords()
    ai = interp(a, t)
    bi = interp(b, t)
    c = ai * bi
    if hdr_op is None:
        h = {}
    else:
        h = hdr_op(a.hdr, b.hdr)
    h['CDELT2'] = tt.dt()
    h['CRVAL2'] = tt.start()
    h['CRPIX2'] = 1
    return gpkimgclass.gpk_img(h, c)


def copy_interval(a, t0, t1, hdr_op=None, mode='rr'):
    """This copies the part of the time-series in a
        where t0 < t < t1.
        'a' is a gpk_img object.
        """
    if hdr_op is None:
        h = a.hdr.copy()
    else:
        h = hdr_op(a.hdr, t0, t1)
    i0 = a.t_index(t0)
    i1 = a.t_index(t1)
    if mode[0] == 'r':
        i0 = int(round(i0))
    elif mode[0] == 'w':
        i0 = int(math.floor(i0))
    elif mode[0] == 'n':
        i0 = int(math.ceil(i0))
    if mode[1] == 'r':
        i1 = int(round(i1))
    elif mode[1] == 'w':
        i1 = int(math.floor(i1))
    elif mode[1] == 'n':
        i1 = int(math.ceil(i1))
    d = Num.array(a.d[i0:i1, :], Num.Float, copy=True)
    h['CRVAL2'] = a.time(i0)
    h['CRPIX2'] = 1
    return gpkimgclass.gpk_img(h, d)


def apply(fcn, a, hdrfcn=lambda x: x):
    """Apply a function, point-by-point to the data in a."""
    return gpkimgclass.gpk_img(hdrfcn(a.hdr), fcn(a.d))


def resample--- This code section failed: ---

 L. 350         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'samplerate'
                9  STORE_FAST            2  'samplerate'

 L. 351        12  LOAD_FAST             0  'a'
               15  LOAD_ATTR             1  'dt'
               18  CALL_FUNCTION_0       0  None
               21  LOAD_FAST             1  'dt'
               24  BINARY_DIVIDE    
               25  STORE_FAST            3  'ratio'

 L. 352        28  LOAD_FAST             2  'samplerate'
               31  LOAD_ATTR             2  'resample'
               34  LOAD_FAST             0  'a'
               37  LOAD_ATTR             3  'd'
               40  LOAD_FAST             3  'ratio'
               43  CALL_FUNCTION_2       2  None
               46  STORE_FAST            4  'd'

 L. 353        49  LOAD_GLOBAL           4  'len'
               52  LOAD_FAST             4  'd'
               55  LOAD_ATTR             5  'shape'
               58  CALL_FUNCTION_1       1  None
               61  LOAD_GLOBAL           4  'len'
               64  LOAD_FAST             0  'a'
               67  LOAD_ATTR             3  'd'
               70  LOAD_ATTR             5  'shape'
               73  CALL_FUNCTION_1       1  None
               76  COMPARE_OP            2  ==
               79  POP_JUMP_IF_TRUE     88  'to 88'
               82  LOAD_ASSERT              AssertionError
               85  RAISE_VARARGS_1       1  None

 L. 354        88  LOAD_FAST             4  'd'
               91  LOAD_ATTR             5  'shape'
               94  LOAD_CONST               1
               97  BINARY_SUBSCR    
               98  LOAD_FAST             0  'a'
              101  LOAD_ATTR             3  'd'
              104  LOAD_ATTR             5  'shape'
              107  LOAD_CONST               1
              110  BINARY_SUBSCR    
              111  COMPARE_OP            2  ==
              114  POP_JUMP_IF_TRUE    153  'to 153'
              117  LOAD_ASSERT              AssertionError
              120  LOAD_CONST               'd.shape[0]: %d -> %d'
              123  LOAD_FAST             0  'a'
              126  LOAD_ATTR             3  'd'
              129  LOAD_ATTR             5  'shape'
              132  LOAD_CONST               0
              135  BINARY_SUBSCR    
              136  LOAD_FAST             4  'd'
              139  LOAD_ATTR             5  'shape'
              142  LOAD_CONST               0
              145  BINARY_SUBSCR    
              146  BUILD_TUPLE_2         2 
              149  BINARY_MODULO    
              150  RAISE_VARARGS_2       2  None

 L. 355       153  LOAD_GLOBAL           7  'abs'
              156  LOAD_GLOBAL           8  'float'
              159  LOAD_FAST             4  'd'
              162  LOAD_ATTR             5  'shape'
              165  LOAD_CONST               0
              168  BINARY_SUBSCR    
              169  CALL_FUNCTION_1       1  None
              172  LOAD_GLOBAL           8  'float'
              175  LOAD_FAST             0  'a'
              178  LOAD_ATTR             3  'd'
              181  LOAD_ATTR             5  'shape'
              184  LOAD_CONST               0
              187  BINARY_SUBSCR    
              188  CALL_FUNCTION_1       1  None
              191  BINARY_DIVIDE    
              192  LOAD_FAST             3  'ratio'
              195  BINARY_SUBTRACT  
              196  CALL_FUNCTION_1       1  None
              199  LOAD_CONST               0.1
              202  COMPARE_OP            0  <
              205  POP_JUMP_IF_TRUE    214  'to 214'
              208  LOAD_ASSERT              AssertionError
              211  RAISE_VARARGS_1       1  None

 L. 356       214  LOAD_FAST             0  'a'
              217  LOAD_ATTR             9  'hdr'
              220  LOAD_ATTR            10  'copy'
              223  CALL_FUNCTION_0       0  None
              226  STORE_FAST            5  'h'

 L. 357       229  LOAD_FAST             1  'dt'
              232  LOAD_FAST             5  'h'
              235  LOAD_CONST               'CDELT2'
              238  STORE_SUBSCR     

 L. 358       239  LOAD_GLOBAL          11  'gpkimgclass'
              242  LOAD_ATTR            12  'gpk_img'
              245  LOAD_FAST             5  'h'
              248  LOAD_FAST             4  'd'
              251  CALL_FUNCTION_2       2  None
              254  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 254


def test():
    a = gpkimgclass.gpk_img({'CDELT2': 1.0, 'CRPIX2': 1, 'CRVAL2': 0.0}, Num.arrayrange(10))
    b = gpkimgclass.gpk_img({'CDELT2': 0.5, 'CRPIX2': 1, 'CRVAL2': 0.4}, Num.arrayrange(10) * 0.5 + 0.4)
    ab = mul(a, b)
    err = ab.d - Num.transpose([ab.time()]) ** 2
    assert Num.sum(err ** 2) < 1e-05


if __name__ == '__main__':
    test_interp1()
    test_interp2()
    test_interp3()
    test()