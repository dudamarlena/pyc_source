# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\virtexp\elphys\clampable.py
# Compiled at: 2013-01-23 10:18:51
"""Virtual voltage clamping."""
from __future__ import division
import logging
from collections import namedtuple
from contextlib import contextmanager
from itertools import chain
import numpy as np
try:
    from cgp.utils.rnumpy import r, RRuntimeError
    have_rnumpy = True
except ImportError:
    have_rnumpy = False
    import warnings
    warnings.warn('rnumpy not installed, some functions will not work.')
    from nose.plugins.skip import SkipTest

    class DummyR(object):
        """Dummy R object to skip nosetests if R is unavailable."""

        def __getattr__(self, name):
            raise SkipTest('rnumpy not installed')


    r = DummyR()

from ...cvodeint.namedcvodeint import Namedcvodeint
from . import paceable
from .ap_stats import apd
from ...utils.ordereddict import OrderedDict
from ...utils.thinrange import thin
from ...utils.splom import r2rec
Pace = namedtuple('Pace', 't y dy a stats')
Trajectory = namedtuple('Trajectory', 't y dy a')
Bond_protocol = namedtuple('Bond_protocol', 'varnames protocol limits url')
keys = 'asctime levelname name lineno process message'
format_ = '%(' + (')s\t%(').join(keys.split()) + ')s'
logging.basicConfig(level=logging.INFO, format=format_)
logger = logging.getLogger('protocols')

@contextmanager
def roptions(**kwargs):
    """
    Temporarily change R options.
    
    Keyword arguments are passed to the options() function in R, restoring the 
    original settings on exiting the with block.
    
    Example: Temporarily use a different character for the decimal point.
    
    >>> with roptions(OutDec="@"):
    ...     r.as_character(1.5)[0]
    '1@5'
    
    Verify that the default has been restored.
    
    >>> r.as_character(1.5)[0]
    '1.5'

    Underscores in keyword names are automatically converted to dots, 
    so the Python statement::
    
        with roptions(show_error_messages=False):
            ...
    
    corresponds to the R statement::
    
        opt <- options(show.error.messages=FALSE)
        ...
        options(opt)
    
    One hack is that *deparse_max_lines* = 0 will suppress R tracebacks 
    altogether,     whereas in R this setting is ignored if it is not a 
    positive integer.
    """
    opt = r.options(**kwargs)
    old_max_lines = RRuntimeError.max_lines
    if kwargs.get('deparse_max_lines') == 0:
        RRuntimeError.max_lines = 0
    try:
        yield
    finally:
        r.options(opt)
        RRuntimeError.max_lines = old_max_lines


def listify(sequence):
    """
    Make a mutable copy of a sequence, recursively converting to list.
    
    Strings are left alone.
    
    This is useful for modifying pacing protocols.
    
    >>> from cgp.virtexp.elphys.examples import Bond
    >>> b = Bond()
    >>> listify(b.bond_protocols(thold=5000)[11])
    [['i_Kr'], [[5000, -80], [1000, [-70, -60, ..., 60]], [1000, -40]], 
    [[0, 2000, 0, 1]], 'http://...']
    
    >>> listify([(1, 2), (3, 4, 5), (6, [7, 8], "abc")])
    [[1, 2], [3, 4, 5], [6, [7, 8], 'abc']]
    """
    if isinstance(sequence, basestring):
        return sequence
    try:
        return [ listify(i) for i in sequence ]
    except TypeError:
        return sequence


def pairbcast(*pairs):
    """
    Broadcasting for pairs of values.
    
    No broadcasting if all pairs have scalar items.
    
    >>> pairbcast((1, 2), (3, 4))
    [[(1, 2), (3, 4)]]
    
    First item of first pair is a 2-tuple.
    
    >>> pairbcast(((1, 2), 3), (4, 5))
    [[(1, 3), (4, 5)], [(2, 3), (4, 5)]]
    
    Second item of second pair is a 2-tuple.
    
    >>> pairbcast((1, 2), (3, (4, 5)))
    [[(1, 2), (3, 4)], [(1, 2), (3, 5)]]
    
    Both items of first pair are tuples.
    
    >>> pairbcast(((1, 2), (3, 4)), (5, 6))
    [[(1, 3), (5, 6)], [(1, 4), (5, 6)], [(2, 3), (5, 6)], [(2, 4), (5, 6)]]
    
    Both items of first pair, and second item of last pair, are tuples.
    
    >>> pairbcast(((1, 2), (3, 4)), (5, 6), (7, (8, 9)))
    [[(1, 3), (5, 6), (7, 8)], [(1, 3), (5, 6), (7, 9)], 
     [(1, 4), (5, 6), (7, 8)], [(1, 4), (5, 6), (7, 9)], 
     [(2, 3), (5, 6), (7, 8)], [(2, 3), (5, 6), (7, 9)], 
     [(2, 4), (5, 6), (7, 8)], [(2, 4), (5, 6), (7, 9)]]
    """
    flat = np.array([ i for p in pairs for i in p ], dtype=object)
    need_bc = np.array([ len(np.atleast_1d(i)) > 1 for i in flat ], dtype=bool)
    if not any(need_bc):
        return [[ tuple(pair) for pair in pairs ]]
    bc = np.broadcast_arrays(*np.ix_(*flat[need_bc]))
    flatbc = zip(*(np.ravel(i) for i in bc))
    result = []
    for bc in flatbc:
        item = np.copy(flat)
        item[need_bc] = bc
        result.append(zip(item[::2], item[1::2]))

    return result


def ndbcast(*tuples):
    """
    Broadcasting for tuples of values.

    No broadcasting if all tuples have scalar items.
    
    >>> ndbcast((1, 2, 3), (4, 5, 6))
    [[(1, 2, 3), (4, 5, 6)]]
    
    First item of first tuple is a 2-tuple.
    
    >>> ndbcast(((1, 2), 3, 4), (5, 6, 7))
    [[(1, 3, 4), (5, 6, 7)], [(2, 3, 4), (5, 6, 7)]]
    
    Second item of second tuple is a 2-tuple.
    
    >>> ndbcast((1, 2, 3), (4, (5, 6), 7))
    [[(1, 2, 3), (4, 5, 7)], [(1, 2, 3), (4, 6, 7)]]
    
    All items of first tuple are tuples.
    
    >>> ndbcast(((1, 2), (3, 4), (5, 6)), (7, 8, 9))
    [[(1, 3, 5), (7, 8, 9)], [(1, 3, 6), (7, 8, 9)], 
     [(1, 4, 5), (7, 8, 9)], [(1, 4, 6), (7, 8, 9)], 
     [(2, 3, 5), (7, 8, 9)], [(2, 3, 6), (7, 8, 9)], 
     [(2, 4, 5), (7, 8, 9)], [(2, 4, 6), (7, 8, 9)]]
    
    :func:`ndbcast` is a generalization of :func:`pairbcast`.
    
    >>> pairs = ((1, 2), (3, 4)), (5, 6), (7, (8, 9))
    >>> ndbcast(*pairs) == pairbcast(*pairs)
    True
    """
    n = len(tuples[0])
    assert all(len(p) == n for p in tuples)
    flat = [ np.atleast_1d(i) for p in tuples for i in p ]
    pb = np.broadcast_arrays(*np.ix_(*flat))
    flatb = zip(*(np.ravel(i) for i in pb))
    return [ zip(*[ i[j::n] for j in range(n) ]) for i in flatb ]


def catrec--- This code section failed: ---

 L. 248         0  LOAD_FAST             1  'kwargs'
                3  LOAD_ATTR             0  'pop'
                6  LOAD_CONST               'globalize_time'
                9  LOAD_GLOBAL           1  'True'
               12  CALL_FUNCTION_2       2  None
               15  STORE_FAST            2  'globalize_time'

 L. 249        18  LOAD_FAST             1  'kwargs'
               21  UNARY_NOT        
               22  POP_JUMP_IF_TRUE     38  'to 38'
               25  LOAD_ASSERT              AssertionError
               28  LOAD_CONST               'Unexpected keyword argument(s): %s'
               31  LOAD_FAST             1  'kwargs'
               34  BINARY_MODULO    
               35  RAISE_VARARGS_2       2  None

 L. 250        38  BUILD_LIST_0          0 
               41  STORE_FAST            3  'C'

 L. 251        44  SETUP_LOOP          207  'to 254'
               47  LOAD_GLOBAL           3  'enumerate'
               50  LOAD_GLOBAL           4  'zip'
               53  LOAD_FAST             0  'args'
               56  CALL_FUNCTION_VAR_0     0  None
               59  CALL_FUNCTION_1       1  None
               62  GET_ITER         
               63  FOR_ITER            187  'to 253'
               66  UNPACK_SEQUENCE_2     2 
               69  STORE_FAST            4  'i'
               72  STORE_FAST            5  'v'

 L. 252        75  SETUP_EXCEPT        140  'to 218'

 L. 253        78  LOAD_FAST             4  'i'
               81  LOAD_CONST               0
               84  COMPARE_OP            2  ==
               87  POP_JUMP_IF_FALSE   123  'to 123'
               90  LOAD_FAST             2  'globalize_time'
             93_0  COME_FROM            87  '87'
               93  POP_JUMP_IF_FALSE   123  'to 123'

 L. 254        96  LOAD_GLOBAL           5  'np'
               99  LOAD_ATTR             6  'concatenate'
              102  LOAD_GLOBAL           7  'paceable'
              105  LOAD_ATTR             8  'globaltime'
              108  LOAD_FAST             5  'v'
              111  CALL_FUNCTION_1       1  None
              114  CALL_FUNCTION_1       1  None
              117  STORE_FAST            6  'c'
              120  JUMP_FORWARD         49  'to 172'

 L. 256       123  LOAD_GLOBAL           5  'np'
              126  LOAD_ATTR             6  'concatenate'
              129  BUILD_LIST_0          0 
              132  LOAD_FAST             5  'v'
              135  GET_ITER         
              136  FOR_ITER             21  'to 160'
              139  STORE_FAST            4  'i'
              142  LOAD_GLOBAL           5  'np'
              145  LOAD_ATTR             9  'atleast_1d'
              148  LOAD_FAST             4  'i'
              151  CALL_FUNCTION_1       1  None
              154  LIST_APPEND           2  None
              157  JUMP_BACK           136  'to 136'
              160  LOAD_CONST               'axis'
              163  LOAD_CONST               0
              166  CALL_FUNCTION_257   257  None
              169  STORE_FAST            6  'c'
            172_0  COME_FROM           120  '120'

 L. 257       172  LOAD_FAST             3  'C'
              175  LOAD_ATTR            10  'append'
              178  LOAD_FAST             6  'c'
              181  LOAD_ATTR            11  'view'
              184  LOAD_FAST             5  'v'
              187  LOAD_CONST               0
              190  BINARY_SUBSCR    
              191  LOAD_ATTR            12  'dtype'
              194  LOAD_GLOBAL          13  'type'
              197  LOAD_FAST             5  'v'
              200  LOAD_CONST               0
              203  BINARY_SUBSCR    
              204  CALL_FUNCTION_1       1  None
              207  CALL_FUNCTION_2       2  None
              210  CALL_FUNCTION_1       1  None
              213  POP_TOP          
              214  POP_BLOCK        
              215  JUMP_BACK            63  'to 63'
            218_0  COME_FROM            75  '75'

 L. 258       218  DUP_TOP          
              219  LOAD_GLOBAL          14  'Exception'
              222  COMPARE_OP           10  exception-match
              225  POP_JUMP_IF_FALSE   249  'to 249'
              228  POP_TOP          
              229  STORE_FAST            7  '_exc'
              232  POP_TOP          

 L. 259       233  LOAD_FAST             3  'C'
              236  LOAD_ATTR            10  'append'
              239  LOAD_FAST             5  'v'
              242  CALL_FUNCTION_1       1  None
              245  POP_TOP          
              246  JUMP_BACK            63  'to 63'
              249  END_FINALLY      
            250_0  COME_FROM           249  '249'
              250  JUMP_BACK            63  'to 63'
              253  POP_BLOCK        
            254_0  COME_FROM            44  '44'

 L. 260       254  LOAD_FAST             3  'C'
              257  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 257


def vclamp2arr(L, nthin=100):
    """
    Record array thinned from results of vectorized voltage-clamp experiment.
    
    :param list L: list of Trajectory namedtuples of (t, y, dy, a)
    :param int nthin: number of time-points to retain
    :return recarray arr: Record array with fields for 
        time, state variables, algebraic variables.
        Fields are 2-d with dimensions (protocol #, time #).
        Shape is set to (1,) rather than () for convenience; 
        record arrays of shape () do not include their dtype in their string 
        representation.
    
    Example, thinning to 3 time-points and rounding results to nearest 1/4 
    for briefer printing:
    
    >>> from cgp.virtexp.elphys.examples import Fitz
    >>> b = Fitz()
    >>> protocol = (1000, -140), (500, np.linspace(-80, 40, 4)), (180, -20)
    >>> L = zip(*[traj for proto, traj in b.vecvclamp(protocol)])
    >>> holding, p1, p2 = [vclamp2arr(i, 3) for i in L]
    >>> f = p1.view(float)
    >>> f[:] = np.round(f * 4) / 4 + 0  # adding zero to avoid -0.0
    
    The resulting record array has four fields (t, V, w, I), each with shape 
    (4, 3) for 4 protocols (P1 voltage of -80, -40, 0, 40) and 3 time-points.
    
    >>> p1
    rec.array([ ([[0.0, 117.5, 500.0], [0.0, 135.5, 500.0], 
                  [0.0, 176.0, 500.0], [0.0, 140.75, 500.0]], 
                 [[-80.0, -80.0, -80.0], [-40.0, -40.0, -40.0], 
                  [0.0, 0.0, 0.0], [40.0, 40.0, 40.0]], 
                 [[-46.75, -30.0, -26.75], [-46.75, -17.75, -13.25], 
                  [-46.75, -3.25, 0.0], [-46.75, 6.0, 13.25]], 
                 [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 
                  [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])], 
    dtype=[('t', '<f8', (4, 3)), ('V', '<f8', (4, 3)), 
           ('w', '<f8', (4, 3)), ('I', '<f8', (4, 3))])
    """
    first = L[0]
    shape = (len(L), nthin)
    dtype = [ (k, float, shape) for k in chain(['t'], first.y.dtype.names, first.a.dtype.names)
            ]
    result = np.zeros((), dtype=dtype).view(np.recarray)
    for i, (t, y, _dy, a) in enumerate(L):
        result['t'][i, :] = np.squeeze(thin(t, nthin))
        for k in y.dtype.names:
            result[k][i, :] = np.squeeze(thin(y[k], nthin))

        for k in a.dtype.names:
            result[k][i, :] = np.squeeze(thin(a[k], nthin))

    return result.reshape(1)


class Clampable(object):
    """
    :wiki:`Mixin` class for in silico experimental protocols for Bondarenko-like models.
    
    Each protocol returns a list of ``(t, y, dy, a)``, concatenated if ``concatenate=True``.
    
    Models are assumed to have parameters *stim_duration* and *stim_amplitude*, and 
    context managers :meth:`~cvodeint.namedcvodeint.Namedcvodeint.clamp` and 
    :meth:`~cellmlmodels.cellmlmodel.Cellmlmodel.dynclamp`.
    
    The 
    :cellml:`Bondarenko 
    <11df840d0150d34c9716cd4cbdd164c8/bondarenko_szigeti_bett_kim_rasmusson_2004_apical>`,
    :doi:`LNCS <10.1152/ajpheart.00219.2010>` and 
    :cellml:`Ten Tusscher 
    <e946a72663bdf17ef6752980a0232351/tentusscher_noble_noble_panfilov_2004_a>` 
    models have a regular stimulus protocol built in, governed by parameters for 
    period, duration and amplitude. Method :meth:`~cgp.virtexp.elphys.paceable.ap` 
    uses this protocol, computing action potential and calcium transient 
    durations, possibly with rootfinding. The current hack is to set 
    ``stim_duration=inf`` when *stim_amplitude* does not depend on time or its 
    time-dependence is handled inside the protocol function.
    """

    def bond_protocols(self, thold=1000, nburnin=10, trest=30000, url='http://ajpheart.physiology.org/content/287/3/H1378.full#F%s'):
        """
        Voltage-clamping protocols from Bondarenko et al. 2004.
        
        Returns an ordered dictionary whose keys are figure numbers
        in :doi:`Bondarenko et al. 2004 <10.1152/ajpheart.00185.2003>`.
        The values are :class:`Bond_protocol` named tuples of 
        ``(varnames, protocol, limits, url)``:
        
        * **varnames**: list of space-delimited strings naming the variables 
          (whether state or algebraic) plotted in each panel
        * **protocol**: input for :meth:`Clampable.pace` or 
          :meth:`Clampable.vecvclamp`. For pacing protocols, 
          stimulus duration and amplitude are taken from the model parameters
        * **limits**: list of original axis limits for time and variable, 
          if applicable. len(limits) == len(varnames)
        * **url**: URL to original figure
        
        :param ms thold: duration at holding potential
        :param nburnin: number of stimuli for pacing protocol
        :param trest: duration of rest before Ca staircase 
            (`figure 19 
            <http://ajpheart.physiology.org/content/287/3/H1378.full#F19>`). 
            Default taken from Bondarenko's ref. 39, Huser et al. 1998, 
            start of Results.
        
        >>> from cgp.virtexp.elphys.examples import Bond
        >>> b = Bond()
        >>> b.bond_protocols(thold=5000)[11]
        Bond_protocol(varnames=['i_Kr'], 
        protocol=[(5000, -80), (1000, array([-70, -60, ...,  60])), (1000, -40)], 
        limits=[[0, 2000, 0, 1]], url='http://...')
        """
        d, a = self.pr.stim_duration, self.pr.stim_amplitude
        return OrderedDict((fignumber, Bond_protocol(varnames, protocol, limits, url % fignumber)) for fignumber, varnames, protocol, limits in [
         (
          3, ['i_Na'],
          [(thold, -140), (500, np.arange(-130, 51, 10)),
           (180, -20)], [[0, 30, -400, 0]]),
         (
          5, ['i_CaL'],
          [(thold, -80), (250, np.arange(-70, 41, 10)),
           (2, -80), (250, 10)], [[0, 500, -8, 0]]),
         (
          6, ['Cai Cass', 'i_CaL Cai'],
          [(thold, -80),
           (
            200, np.arange(-60, 51, 10))], [[0, 200, 0, 40], None]),
         (
          7, ['i_CaL'],
          [(thold, -80), (250, 0),
           (
            np.arange(2, 503, 25), (-90, -80, -70)),
           (100, 0)], [[0, 800, -8, 0]]),
         (
          8, ['i_Kto_f i_Kto_s i_Kr i_Kur i_Kss i_Ks i_K1'],
          [(thold, -80),
           (
            5000, np.arange(-70, 51, 10))], [[0, 5000, 0, 70]]),
         (
          9, ['i_Kto_f'],
          [(thold, -80), (500, np.arange(-100, 51, 10)),
           (500, 50)], [[0, 1000, 0, 60]]),
         (
          10, ['i_Kto_s'], [(thold, -100), (5000, np.arange(-90, 51, 10))],
          [
           [
            0, 2000, 0, 10]]),
         (
          11, ['i_Kr'],
          [
           (
            thold, -80), (1000, np.arange(-70, 61, 10)), (1000, -40)],
          [
           [
            0, 2000, 0, 1]]),
         (
          12, ['i_Kur', 'i_Kss'],
          [
           (
            thold, -100), (5000, np.arange(-90, 51, 10))],
          [
           [
            0, 5000, 0, 15], [0, 5000, 0, 5]]),
         (
          13, ['i_Kur i_Kss'],
          [
           (
            thold, -100), (5000, np.arange(-60, 61, 10))], [None]),
         (
          14, ['i_Ks'], [(thold, -80), (5000, np.arange(-70, 51, 10))],
          [
           [
            0, 5000, 0, 0.6]]),
         (
          15, ['i_K1'], [(thold, -80), (5000, np.arange(-150, -39, 10))],
          [
           None]),
         (
          16,
          ['V', 'i_Kto_f i_Kur i_Kss i_CaL i_Na',
           'i_NaCa i_NaK i_K1 i_Cab i_Nab'],
          [
           (
            nburnin, 1000, d, a)],
          [[0, 50, -90, 40],
           [
            0, 50, -15, 30], [0, 50, -0.5, 1]]),
         (
          17, ['V', 'Cai'], [(nburnin, (150, 250, 500, 1000, 2000), d, a)],
          [
           [
            0, 50, -90, 40], [0, 140, 0, 0.6]]),
         (
          18, ['Cai'], [(nburnin, 1000 / np.arange(500, 7001, 500), d, a)],
          [
           None]),
         (
          19, ['Cai'], [(1, trest, d, a), (12, 1300, d, a)],
          [
           [
            0, 15000, 0.1, 0.7]]),
         (
          20, ['J_rel i_CaL i_NaCa J_up J_leak'], [(11, 1000, d, a)],
          [
           [
            0, 60, -0.4, 0.4], [0, 1000, -40, 40]])])

    def zhou_protocols(self, thold=1000, nburnin=10, trest=30000, url='http://ajpheart.physiology.org/content/287/3/H1378.full#F%s'):
        """
        Voltage-clamping protocols from Zhou et al. 1998.
        
        .. todo:: Definition lists in ReST have (term, descr) on separate lines
        
        Returns an ordered dictionary whose keys are figure numbers in
        `Zhou et al. 1998 <http://circres.ahajournals.org/cgi/content/full/83/8/806>`_.
        The values are :class:`Bond_protocol` named tuples of 
        (varnames, protocol, limits, url):
        
        * **varnames**: list of space-delimited strings naming the variables 
          (whether state or algebraic) plotted in each panel
        * **protocol**: input for :meth:`Clampable.pace` or :meth:`Clampable.vecvclamp`
          For pacing protocols, stimulus duration and amplitude are taken 
          from the model parameters
        * **limits**: list of original axis limits for time and variable, 
          if applicable. Note that len(limits) == len(varnames)
        * **url**: URL to original figure.
        
        :param ms thold: duration at holding potential
        :param nburnin: number of stimuli for pacing protocol
        :param trest: duration of rest before Ca staircase (figure 19).
        
        >>> from cgp.virtexp.elphys.examples import Bond
        >>> b = Bond()
        >>> b.zhou_protocols(thold=5000)[2]
        Bond_protocol(varnames=['i_Kto_s'], 
        protocol=[(5000, -50), (200, 40), (5, -50), 
        (100, array([-40, -30, ...,  50])), (100, -20)], limits=[None], 
        url='http://...')
        """
        return OrderedDict((fignumber, Bond_protocol(varnames, protocol, limits, url % fignumber)) for fignumber, varnames, protocol, limits in [
         (
          2, ['i_Kto_s'],
          [(thold, -50), (200, 40), (5, -50),
           (
            100, np.arange(-40, 51, 10)), (100, -20)], [None])])

    def pace(self, protocol, nthin=None):
        """
        Iterator to yield (t, y, dy, a, stats) from specified pacing of a model.
        
        :param protocol: Sequence of (n, period, duration, amplitude)
        :param nthin: number of time-points for each pace (default: no thinning)
        :return: Yields successive named tuples of class Pace with fields 
            ``(t, y, dy, a, stats)``, where *t* is local time, 
            cf. :func:`~cgp.virtexp.elphys.paceable.globaltime` 
            and :func:`~cgp.virtexp.elphys.paceable.localtime`.
        
        Here is an example pacing twice at 70-ms intervals, then three times 
        at 30-ms intervals. Here we store the output of the :meth:`pace`
        iterator in a list so we can reuse it below without recomputing.
        
        .. plot::
            :include-source:
            :context:
            :nofigs:
            
            >>> from cgp.virtexp.elphys.examples import Bond
            >>> b = Bond(reltol=1e-3)
            >>> protocol = [(2, 70, 0.5, -80), (3, 30, 0.5, -80)]
        
        .. plot::
            :context:
            
            for t, y, dy, a, stats in b.pace(protocol):
                plt.plot(t, y.V)
        
        You may concatenate the output with :func:`catrec`. To reuse results
        of lengthy computations, the output of the :meth:`pace` iterator
        can be stored in a list.
        
        .. plot::
            :context:
            :include-source:
            :nofigs:
            
            >>> from cgp.virtexp.elphys.clampable import catrec
            >>> L = list(b.pace(protocol))
            >>> t, y, dy, a, stats = catrec(*L)
            >>> "%5.2f" % y.V.max()
            '33.02'
        
        .. plot::
            :context:
        
            plt.clf()
            plt.plot(t, y.V, t, 100 * y.Cai)
            plt.show()

        The named tuples that :meth:`pace` yields can be unpacked as usual, 
        or you may refer to named fields.
        
        >>> ["%4.2f" % stats["caistats"]["peak"] for t, y, dy, a, stats in L]
        ['0.64', '0.54', '0.53', '0.49', '0.38']
        >>> [(i.t[0], i.t[-1]) for i in L]
        [(0.0, 70.0), (0.0, 70.0), (0.0, 30.0), (0.0, 30.0), (0.0, 30.0)]
        
        The *nthin* argument can reduce the size of output.
        
        >>> all([len(i.y.Cai) == 3 for i in b.pace(protocol, nthin=3)])
        True
        """
        y0 = np.copy(self.y)
        for n, period, duration, amplitude in protocol:
            with self.autorestore(_y=y0, stim_period=period, stim_duration=duration, stim_amplitude=amplitude):
                for _i in range(n):
                    t, y, stats = self.ap()
                    dy, a = self.rates_and_algebraic(t, y)
                    if nthin:
                        t, y, dy, a = [ thin(arr, nthin) for arr in (t, y, dy, a) ]
                    yield Pace(t, y, dy, a, stats)

            y0 = y[(-1)]

    def vecpace(self, protocol, nthin=None):
        """
        Vectorized :meth:`~Clampable.pace`.
        
        :param protocol: Sequence of (n, period, duration, amplitude).
            If any n, period, duration or amplitude is a sequence of length > 1, 
            multiple protocols are computed by :func:`ndbcast`.
        :param nthin: Number of time-points for each pulse (default: no thinning).
        :return list: Input and output (protocol_i, [list of Pace]) for each 
            call to :meth:`~Clampable.pace`, one for each unique protocol.
        
        >>> from cgp.virtexp.elphys.examples import Bond
        >>> b = Bond()
        >>> protocol = [(3, (150, 250), 0.25, -80)]
        >>> L = b.vecpace(protocol)
        
        An example using named fields of :class:`Pace` objects.
        
        >>> for proto, paces in L:
        ...     print proto,
        ...     for pace in paces:
        ...         print "%8.3f" % pace.y.V.max(),
        [(3, 150, 0.25, -80)]   31.584 -63.698 -63.112
        [(3, 250, 0.25, -80)]   31.584 -63.252 -62.847
        """
        return [ (p, list(self.pace(p, nthin))) for p in ndbcast(*protocol) ]

    @contextmanager
    def dynclamp(self, setpoint, R=0.02, V='V', ion='Ki', scale=None):
        """
        Derived model with state value dynamically clamped to a set point.
        
        Input arguments:
        
        * setpoint : target value for state variable
        * R=0.02 : resistance of clamping current
        * V="V" : name of clamped variable
        * ion="Ki" : name of state variable carrying the clamping current
        * scale=None : "ion" per "V", 
          default :math:`Acap * Cm / (Vmyo * F)`, see below
        
        Clamping is implemented as a dynamically applied current that is 
        proportional to the deviation from the set point::
        
            dV/dt = -(i_K1 + ... + I_app)
            I_app = (V - setpoint) / R
        
        Thus, if V > setpoint, then I_app > 0 and serves to decrease dV/dt.
        To account for the charge added to the system, a current proportional 
        to I_app is added to a specified ion concentration, by default Ki. This 
        needs to be scaled according to conductance and other constants.
        The default is as for the Bondarenko model::
         
            scale = Acap * Cm / (Vmyo * F)
            dKi/dt = -(i_K1 + ... + I_app) * scale
                
        Example with voltage clamping of Bondarenko model. Any pre-existing 
        stimulus amplitude is temporarily set to zero. The parameter array is 
        shared between the original and clamped models, and restored on 
        exiting the 'with' block.
        
        >>> from cgp.virtexp.elphys.examples import Bond
        >>> bond = Bond()
        >>> with bond.dynclamp(-140) as clamped:
        ...     t, y, flag = clamped.integrate(t=[0, 10])
        ...     bond.pr.stim_amplitude
        array([ 0.])
        >>> clamped.pr is bond.pr
        True
        >>> bond.pr.stim_amplitude
        array([-80.])
        
        The clamped model has its own instance of the CVODE integrator and 
        state NVector.
        
        >>> (clamped.cvode_mem is bond.cvode_mem, clamped.y is bond.y)
        (False, False)
        
        However, changes in state are copied to the original on exiting the 
        'with' block.
        
        >>> "%7.2f" % bond.yr.V
        '-139.68'
                
        Unlike .clamp(), .dynclamp() does not allow you to change the setpoint 
        inside the "with" block. Instead, just start a new "with" block.
        (Changes to state variables remain on exit from the with block.)
        
        >>> with bond.dynclamp(-30) as clamped:
        ...     t0, y0, flag0 = clamped.integrate(t=[0, 10])
        >>> with bond.dynclamp(-10) as clamped:
        ...     t1, y1, flag1 = clamped.integrate(t=[10, 20])
        >>> np.concatenate([y0[0], y0[-1], y1[0], y1[-1]])["V"].round(2)
        array([-139.68,  -29.96,  -29.96,  -10.34])
        
        Naive clamping with dV/dt = 0 and unspecified clamping current, 
        like .clamp() does, equals the limit as R -> 0 and scale = 0.
        
        >>> with bond.autorestore(V=0):
        ...     with bond.dynclamp(-140, 1e-10, scale=0) as clamped:
        ...         t, y, flag = clamped.integrate(t=[0, 0.1])
        
        Although V starts at 0, it gets clamped to the setpoint very quickly.
        
        >>> y.V[0]
        array([   0.])
        >>> t[y.V.squeeze() < -139][0]
        4.94...e-10
        """
        if scale is None:
            p = self.pr
            scale = p.Acap * p.Cm / (p.Vmyo * p.F)
        iV = self.dtype.y.names.index(V)
        iion = self.dtype.y.names.index(ion)

        def dynclamped(t, y, ydot, f_data):
            """New RHS that prevents some elements from changing."""
            self.f_ode(t, y, ydot, f_data)
            I_app = (y[iV] - setpoint) / R
            ydot[iV] -= I_app
            ydot[iion] -= I_app * scale
            return 0

        y = np.array(self.y).view(self.dtype.y)
        oldkwargs = dict((k, getattr(self, k)) for k in ('chunksize maxsteps reltol abstol').split())
        pr_old = self.pr.copy()
        args, kwargs = self._init_args
        clamped_model = self.__class__(*args, **kwargs)
        Namedcvodeint.__init__(clamped_model, dynclamped, self.t, y, self.pr, **oldkwargs)
        if 'stim_amplitude' in clamped_model.dtype.p.names:
            clamped_model.pr.stim_amplitude = 0
        try:
            yield clamped_model
        finally:
            self.pr[:] = pr_old
            for k in clamped_model.dtype.y.names:
                if k in self.dtype.y.names:
                    setattr(self.yr, k, getattr(clamped_model.yr, k))

        return

    def vclamp(self, protocol, nthin=None):
        """
        Iterator to yield t, y, dy, a from a voltage clamp experiment.
        
        :param protocol: Sequence of (duration, voltage) for each pulse
        :param nthin: number of time-points for each pulse (default: no thinning)
        :return: Yields successive named tuples of (t, y, dy, a) 
            where t is local time, cf. 
            :func:`~cgp.virtexp.elphys.paceable.globaltime`.
        
        Here is an example of the P1-P2 protocol used in Figure 3 of 
        Bondarenko et al. 2004.
        
        >>> from cgp.virtexp.elphys.examples import Bond
        >>> b = Bond()
        
        Simulate three intervals: holding potential, P1 pulse, P2 pulse.
        
        >>> L = b.vclamp([(1000, -140), (500, -70), (180, -20)])
        
        Peak (most negative) i_Na in the P1 and P2 intervals:
        
        >>> ["%5.2f" % i.a.i_Na.min() for i in L[1:]]
        ['-0.11', '-99.78']
        
        State and parameters are autorestored after the protocol is finished.
        
        >>> all(b.y == b.model.y0)
        True
        
        Verify that the stimulus current is disabled during clamping.
        
        >>> all(L[0].a.i_stim == 0)
        True
        """
        L = []
        with self.autorestore():
            for duration, voltage in protocol:
                with self.clamp(V=voltage) as (clamped):
                    t, y, _flag = clamped.integrate(t=[0, duration])
                    dy, a = self.rates_and_algebraic(t, y)
                if nthin:
                    t, y, dy, a = [ thin(arr, nthin) for arr in (t, y, dy, a) ]
                L.append(Trajectory(t, y, dy, a))

        return L

    def vargap(self, protocol, nthin=None):
        """
        Variable-gap protocol without duplication of effort.
        
        :param protocol: sequence of (duration, voltage) for 
            (holding, p1, gap, p2) where gap duration and voltage may be 
            vectors.
            If any duration or voltage is a sequence of length > 1, 
            multiple protocols are computed by :func:`pairbcast`.
        :param nthin: thinning output as for vclamp
        :return: Trajectories for p1, gap, p2; the latter in lists.
        
        * The holding trajectory is discarded because it is not of interest.
        * The p1 trajectory is common to all variations of the protocol, 
          so only computed once.
        * Gap trajectories are returned only for the longest gap for each 
          unique gap voltage, because the shorter gap dynamics duplicate 
          the longest up to their endpoint.
        * All p2 trajectories are returned because they depend on previous 
          history.
        
        .. todo:: `vargap` gives blatantly wrong result, will fix later. 
           Workaround: Stick with vecvclamp.
        """
        with self.autorestore():
            for duration, voltage in protocol[:2]:
                with self.clamp(V=voltage) as (clamped):
                    t, y, _flag = clamped.integrate(t=[0, duration])

            dy, a = self.rates_and_algebraic(t, y)
            p1 = [Trajectory(t, y, dy, a)]
            p1_duration, _p1_voltage = protocol[1]
            gap_durations, gap_voltages = protocol[2]
            p2_duration, p2_voltage = protocol[3]
            gap = []
            p2 = []
            for gap_voltage in gap_voltages:
                gap_trajectory = []
                with self.autorestore():
                    with self.clamp(V=gap_voltage) as (clamped):
                        tspan = np.ones(2) * p1_duration
                        for gap_duration in gap_durations:
                            tspan = np.array([tspan[(-1)],
                             p1_duration + gap_duration])
                            gap_trajectory.append(clamped.integrate(t=tspan))
                            with clamped.autorestore():
                                with clamped.clamp(V=p2_voltage) as (p2_clamped):
                                    p2tspan = tspan[(-1)] + np.array([0, p2_duration])
                                    t, y, _flag = p2_clamped.integrate(t=p2tspan)
                            dy, a = self.rates_and_algebraic(t, y)
                            p2.append(Trajectory(t, y, dy, a))

                        t, y, _flag = catrec(globalize_time=False, *gap_trajectory)
                        dy, a = self.rates_and_algebraic(t, y)
                        gap.append(Trajectory(t, y, dy, a))

        if nthin:
            p1 = [ Trajectory(*[ thin(arr, nthin) for arr in i ]) for i in p1 ]
            gap = [ Trajectory(*[ thin(arr, nthin) for arr in i ]) for i in gap ]
            p2 = [ Trajectory(*[ thin(arr, nthin) for arr in i ]) for i in p2 ]
        return (
         p1, gap, p2)

    def vecvclamp(self, protocol, nthin=None, log_exceptions=False):
        """
        Vectorized :meth:`~Clampable.vclamp`.
        
        :param protocol: sequence of (duration, voltage)
            If any duration or voltage is a sequence of length > 1, 
            multiple protocols are computed by pairbcast().
        :param nthin: thinning output as for :meth:`~Clampable.vclamp`
        :param bool log_exceptions: handle any exceptions by logging a warning
        :return: List with input and output (protocol_i, trajectories_i) for 
            each call to :meth:`~Clampable.vclamp`, one for each unique protocol.
        
        >>> from cgp.virtexp.elphys.examples import Bond
        >>> b = Bond(reltol=1e-3)
        >>> protocol = (1000, -140), (500, np.linspace(-80, 40, 4)), (180, -20)
        >>> L = b.vecvclamp(protocol)
        
        The first protocol.
        
        >>> L[0][0]
        [(1000, -140), (500, -80.0), (180, -20)]
        
        An example using named fields of :class:`Trajectory` objects.
        
        >>> for proto, traj in L:
        ...     t1, v1 = proto[1]
        ...     print "%3d: %8.3f" % (v1, traj[1].a.i_Na.min())
        -80:   -0.004
        -40: -175...
          0: -300...
         40:    0.000
        
        State and parameters are autorestored after the protocol is finished.
        
        >>> all(b.y == b.model.y0)
        True
        """
        L = []
        for p in pairbcast(*protocol):
            try:
                L.append((p, self.vclamp(p, nthin)))
            except Exception as _exc:
                logger.exception('Error in vclamp(%s)', p)

        return L

    def bondfig3(self, thold=1000, vhold=-140, t1=500, v1=np.arange(-140, 51, 10), t2=180, v2=-20, plot=True):
        """
        P1-P2 protocol from Fig. 3 of Bondarenko et al.
        """
        L = self.vecvclamp([(thold, vhold), (t1, v1), (t2, v2)])
        peak1, peak2 = [ np.array([ traj[i].a.i_Na.min() for _proto, traj in L ]) for i in (1,
                                                                                            2)
                       ]
        peak1 = -peak1 / peak1.min()
        peak2 = peak2 / peak2.min()
        if plot:
            from pylab import figure, subplot, plot, axis
            figure()
            subplot(221)
            _h = [ plot(tr[1].t, tr[1].a.i_Na, label=pr[1][1]) for pr, tr in L ]
            axis(xmax=30)
            subplot(222)
            plot(v1, peak1, '.-')
            subplot(223)
            plot(v1, peak2, '.-')
        return L

    def bondfig5(self, thold=1000, vhold=-80, t1=250, v1=np.arange(-70, 41, 10), t2=2, v2=-80, t3=250, v3=10, plot=True):
        """Fig. 5 of Bondarenko et al."""
        L = self.vecvclamp([(thold, vhold), (t1, v1), (t2, v2), (t3, v3)])
        peak1, peak3 = [ np.array([ traj[i].a.i_CaL.min() for _proto, traj in L ]) for i in (1,
                                                                                             3)
                       ]
        peak1 = -peak1 / peak1.min()
        peak3 = peak3 / peak3.min()
        if plot:
            from pylab import figure, subplot, plot, axis
            figure()
            subplot(221)
            for v1i, (_proto, traj) in zip(v1, L):
                t, _y, _dy, a = catrec(*traj[1:])
                plot(t - t[0], a.i_CaL, label=v1i)

            axis(ymin=-8, xmax=500)
            subplot(222)
            plot(v1, peak1, '.-')
            axis([-60, 60, -1, 0])
            subplot(223)
            plot(v1, peak3, '.-')
            axis([-80, 40, 0, 1])
        return L

    def bondfig6(self, thold=1000, vhold=-80, t1=200, v1=np.arange(-60, 51, 10), plot=True):
        """Fig. 6 of Bondarenko et al."""
        L = self.vecvclamp([(thold, vhold), (t1, v1)])
        peakCai = np.array([ traj[1].y.Cai.max() for _proto, traj in L ])
        peaki_CaL = np.array([ traj[1].a.i_CaL.max() for _proto, traj in L ])
        peakCai = peakCai / peakCai.max()
        peaki_CaL = peaki_CaL / peaki_CaL.max()
        if plot:
            from pylab import figure, subplot, plot, axis
            figure()
            subplot(211)
            for _proto, (_, (t, y, _dy, _a)) in L:
                plot(t, y.Cai, t, y.Cass)

            axis(xmax=500)
            subplot(212)
            plot(v1, peakCai, '.-', v1, peaki_CaL, '.-')
        return L

    def bondfig7(self, protocol=(
 (1000, -80), (250, 0), (np.arange(2, 503, 25), -80), (100, 0)), plot=True):
        L = self.vecvclamp(protocol)
        if plot:
            from pylab import figure, subplot, plot
            figure()
            subplot(211)
            for _proto, traj in L:
                t, _y, _dy, a = catrec(*traj[1:])
                plot(t - t[0], a.i_CaL)

        return L

    def nelsonCa(self, protocol=(
 (1000, -75), (4000, 0)), plot=True):
        (_proto, (_traj0, traj1)), = self.vecvclamp(protocol)
        if plot:
            from pylab import figure, plot, axis
            figure()
            plot(traj1.t, traj1.a.i_CaL)
            axis('tight')
        return traj1


def mmfits--- This code section failed: ---

 L. 983         0  LOAD_CONST               'k must be a single field name of y or a, not %s'
                3  LOAD_GLOBAL           0  'type'
                6  LOAD_FAST             2  'k'
                9  CALL_FUNCTION_1       1  None
               12  BINARY_MODULO    
               13  STORE_FAST            4  'msg'

 L. 984        16  LOAD_GLOBAL           1  'isinstance'
               19  LOAD_FAST             2  'k'
               22  LOAD_GLOBAL           2  'basestring'
               25  CALL_FUNCTION_2       2  None
               28  POP_JUMP_IF_TRUE     40  'to 40'
               31  LOAD_ASSERT              AssertionError
               34  LOAD_FAST             4  'msg'
               37  RAISE_VARARGS_2       2  None

 L. 985        40  BUILD_LIST_0          0 
               43  STORE_FAST            5  'tgap'

 L. 986        46  BUILD_LIST_0          0 
               49  STORE_FAST            6  'peak'

 L. 987        52  SETUP_LOOP          156  'to 211'
               55  LOAD_FAST             0  'L'
               58  GET_ITER         
               59  FOR_ITER            148  'to 210'
               62  UNPACK_SEQUENCE_2     2 
               65  STORE_FAST            7  'proto'
               68  STORE_FAST            8  'traj'

 L. 988        71  LOAD_FAST             7  'proto'
               74  LOAD_FAST             1  'i'
               77  BINARY_SUBSCR    
               78  UNPACK_SEQUENCE_2     2 
               81  STORE_FAST            9  'duration'
               84  STORE_FAST           10  '_voltage'

 L. 989        87  LOAD_FAST             8  'traj'
               90  LOAD_FAST             1  'i'
               93  LOAD_CONST               1
               96  BINARY_ADD       
               97  BINARY_SUBSCR    
               98  UNPACK_SEQUENCE_4     4 
              101  STORE_FAST           11  '_t'
              104  STORE_FAST           12  'y'
              107  STORE_FAST           13  '_dy'
              110  STORE_FAST           14  'a'

 L. 990       113  LOAD_FAST             2  'k'
              116  LOAD_FAST            12  'y'
              119  LOAD_ATTR             4  'dtype'
              122  LOAD_ATTR             5  'names'
              125  COMPARE_OP            6  in
              128  POP_JUMP_IF_FALSE   141  'to 141'
              131  LOAD_FAST            12  'y'
              134  LOAD_FAST             2  'k'
              137  BINARY_SUBSCR    
              138  JUMP_FORWARD          7  'to 148'
              141  LOAD_FAST            14  'a'
              144  LOAD_FAST             2  'k'
              147  BINARY_SUBSCR    
            148_0  COME_FROM           138  '138'
              148  STORE_FAST           15  'curr'

 L. 991       151  LOAD_FAST             3  'abs_'
              154  POP_JUMP_IF_FALSE   175  'to 175'

 L. 992       157  LOAD_GLOBAL           6  'np'
              160  LOAD_ATTR             7  'abs'
              163  LOAD_FAST            15  'curr'
              166  CALL_FUNCTION_1       1  None
              169  STORE_FAST           15  'curr'
              172  JUMP_FORWARD          0  'to 175'
            175_0  COME_FROM           172  '172'

 L. 993       175  LOAD_FAST             5  'tgap'
              178  LOAD_ATTR             8  'append'
              181  LOAD_FAST             9  'duration'
              184  CALL_FUNCTION_1       1  None
              187  POP_TOP          

 L. 994       188  LOAD_FAST             6  'peak'
              191  LOAD_ATTR             8  'append'
              194  LOAD_FAST            15  'curr'
              197  LOAD_ATTR             9  'max'
              200  CALL_FUNCTION_0       0  None
              203  CALL_FUNCTION_1       1  None
              206  POP_TOP          
              207  JUMP_BACK            59  'to 59'
              210  POP_BLOCK        
            211_0  COME_FROM            52  '52'

 L. 995       211  LOAD_GLOBAL          10  'mmfit'
              214  LOAD_FAST             5  'tgap'
              217  LOAD_FAST             6  'peak'
              220  CALL_FUNCTION_2       2  None
              223  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 223


def mmfit(x, y, rse=False):
    """
    Michaelis-Menten fit, y = ymax x / (x + xhalf).
    
    Passing rse=False also returns relative standard errors for each estimate.
    
    :return ymax: asymptotic value of y as x goes to infinity
    :return xhalf: half-saturation value of x
    :return rse_ymax: relative standard error for *ymax* (if ``rse=True``)
    :return rse_xhalf: relative standard errors for *xhalf* (if ``rse=True``)
    
    For use with results from :meth:`Clampable.vecvclamp`, 
    see :func:`mmfits`.
    
    >>> np.random.seed(0)
    >>> x = np.arange(10.0)
    >>> y =  x / (x + 5) + 0.05 * np.random.random(size=x.shape)
    >>> mmfit(x, y)
    (0.99860..., 4.35779...)
    >>> mmfit(x, y, rse=True)
    (0.99860..., 4.35779..., 0.04162..., 0.09433...)
    
    Note that the estimators are somewhat biased.
    
    >>> np.mean([mmfit(x, x / (x + 5) + 0.05 * np.random.randn(*x.shape)) 
    ...     for i in range(100)], axis=0)
    array([ 1.059...,  5.690...])
    
    (Increasing to 10000 samples gives [ 1.035,  5.401].)
    
    Verify fix for excessive output on error (unwanted dump of source code).
    
    >>> from cgp.utils import rnumpy
    >>> rnumpy.RRuntimeError.max_lines = 0
    >>> mmfit(range(5), range(5))
    (nan, nan)
    
    If the estimate of ymax or xhalf is negative, nans are returned.
    A debug message is also logged.
    
    >>> mmfit(x, -y)
    (nan, nan)
    """
    with roptions(show_error_messages=False, deparse_max_lines=0):
        kwargs = dict(formula='y~ymax*x/(x+xhalf)', data=dict(x=x, y=y), start=dict(ymax=max(y), xhalf=np.mean(x)))
        try:
            fit = r.nls(**kwargs)
        except RRuntimeError as exc:
            s = str(exc.exc).split('\n')[1].strip()
            errmsg = "Michaelis-Menten fit failed with message '%s'. " % s
            errmsg += 'Arguments to r.nls() were: %s'
            logger.debug(errmsg, kwargs)
            ymax = xhalf = rse_ymax = rse_xhalf = np.nan
        else:
            coef = r2rec(r.as_data_frame(r.coef(r.summary(fit))))
            ymax, xhalf = coef.Estimate
            rse_ymax, rse_xhalf = coef['Std. Error'] / coef.Estimate
            if ymax < 0 or xhalf < 0:
                errmsg = 'Michalis-Menten fit gave negative estimate(s): ymax=%s, xhalf=%s. Arguments to r.nls() were: %s'
                logger.debug(errmsg, ymax, xhalf, kwargs)
                ymax = xhalf = rse_ymax = rse_xhalf = np.nan
            if rse:
                return (ymax, xhalf, rse_ymax, rse_xhalf)

        return (ymax, xhalf)


def decayfits--- This code section failed: ---

 L.1091         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             2  'k'
                6  LOAD_GLOBAL           1  'basestring'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'k must be a single field name of y or a'
               21  RAISE_VARARGS_2       2  None

 L.1092        24  BUILD_LIST_0          0 
               27  STORE_FAST            4  'vi'

 L.1093        30  BUILD_LIST_0          0 
               33  STORE_FAST            5  'tau'

 L.1094        36  SETUP_LOOP          155  'to 194'
               39  LOAD_FAST             0  'L'
               42  GET_ITER         
               43  FOR_ITER            147  'to 193'
               46  UNPACK_SEQUENCE_2     2 
               49  STORE_FAST            6  'proto'
               52  STORE_FAST            7  'traj'

 L.1095        55  LOAD_FAST             6  'proto'
               58  LOAD_FAST             1  'i'
               61  BINARY_SUBSCR    
               62  UNPACK_SEQUENCE_2     2 
               65  STORE_FAST            8  '_duration'
               68  STORE_FAST            9  'voltage'

 L.1096        71  LOAD_FAST             7  'traj'
               74  LOAD_FAST             1  'i'
               77  BINARY_SUBSCR    
               78  UNPACK_SEQUENCE_4     4 
               81  STORE_FAST           10  't'
               84  STORE_FAST           11  'y'
               87  STORE_FAST           12  '_dy'
               90  STORE_FAST           13  'a'

 L.1097        93  LOAD_FAST             2  'k'
               96  LOAD_FAST            11  'y'
               99  LOAD_ATTR             3  'dtype'
              102  LOAD_ATTR             4  'names'
              105  COMPARE_OP            6  in
              108  POP_JUMP_IF_FALSE   121  'to 121'
              111  LOAD_FAST            11  'y'
              114  LOAD_FAST             2  'k'
              117  BINARY_SUBSCR    
              118  JUMP_FORWARD          7  'to 128'
              121  LOAD_FAST            13  'a'
              124  LOAD_FAST             2  'k'
              127  BINARY_SUBSCR    
            128_0  COME_FROM           118  '118'
              128  STORE_FAST           14  'curr'

 L.1098       131  LOAD_FAST             3  'abs_'
              134  POP_JUMP_IF_FALSE   155  'to 155'

 L.1099       137  LOAD_GLOBAL           5  'np'
              140  LOAD_ATTR             6  'abs'
              143  LOAD_FAST            14  'curr'
              146  CALL_FUNCTION_1       1  None
              149  STORE_FAST           14  'curr'
              152  JUMP_FORWARD          0  'to 155'
            155_0  COME_FROM           152  '152'

 L.1100       155  LOAD_FAST             4  'vi'
              158  LOAD_ATTR             7  'append'
              161  LOAD_FAST             9  'voltage'
              164  CALL_FUNCTION_1       1  None
              167  POP_TOP          

 L.1101       168  LOAD_FAST             5  'tau'
              171  LOAD_ATTR             7  'append'
              174  LOAD_GLOBAL           8  'decayfit'
              177  LOAD_FAST            10  't'
              180  LOAD_FAST            14  'curr'
              183  CALL_FUNCTION_2       2  None
              186  CALL_FUNCTION_1       1  None
              189  POP_TOP          
              190  JUMP_BACK            43  'to 43'
              193  POP_BLOCK        
            194_0  COME_FROM            36  '36'

 L.1102       194  LOAD_FAST             4  'vi'
              197  LOAD_FAST             5  'tau'
              200  BUILD_TUPLE_2         2 
              203  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 203


def decayfit(t, y, p=(
 0.05, 0.9), prepend_zero=False, rse=False, lm=False):
    """
    Fit exponential decay, y(t) = w exp(-t/tau), to latter part of trajectory.
    
    :param t: time
    :param y: variable, e.g. an ion current
    :param p: proportion of return to initial value, 
        as for action potential duration
    :param bool prepend_zero: add a 0 at the start of y (hack for use with 
        ion currents)
    :param bool rse: return relative standard error of slope (not of *tau*!).
    :param bool lm: Return R object for fitted linear model.
    :return tau: -1/slope for estimated slope of log(y) vs t
    
    tau has dimension 'time' and is analogous to half-life: '1/e'-life = 0.37-life.
    
    For use with results from :meth:`Clampable.vecvclamp`, see :func:`decayfits`.
    
    Trivial example.
    
    >>> t = np.arange(10)
    >>> y = np.exp(-t)
    >>> y[0] = 0
    >>> decayfit(t, y)
    1.0
    
    Relative standard error when adding noise.
    
    >>> np.random.seed(0)
    >>> noisy = y + 0.05 * np.random.random(size=y.shape)
    >>> decayfit(t, noisy, rse=True, p=[0.5, 0.99])
    (1.292..., 0.045...)
    """
    assert len(p) == 2
    if prepend_zero:
        t = np.r_[(0, t)]
        y = np.r_[(0, y)]
    stats = apd(t, y, p)
    _ip, i0, i1 = stats['i']
    if i1 <= i0:
        tau = rse_slope = np.nan
        rlm = None
    elif have_rnumpy:
        with roptions(show_error_messages=False, deparse_max_lines=0):
            try:
                rlm = r.lm('log(y)~t', data=dict(t=t[i0:i1], y=y[i0:i1].squeeze()))
                coef = r2rec(r.as_data_frame(r.coef(r.summary(rlm))))
                _intercept, slope = coef.Estimate
                _rse_intercept, rse_slope = coef['Std. Error'] / abs(coef.Estimate)
                tau = -1.0 / slope
            except RRuntimeError:
                tau = rse_slope = np.nan
                rlm = None

    else:
        from scipy.stats.stats import linregress
        try:
            slope, _intercept, _r_value, _p_value, std_err = linregress(t[i0:i1], np.log(y[i0:i1]).squeeze())
            rse_slope = std_err / np.abs(slope)
            tau = -1.0 / slope
        except ZeroDivisionError:
            tau = rse_slope = np.nan
            rlm = None

    result = (
     tau,)
    if rse:
        result += (rse_slope,)
    if lm:
        result += (rlm,)
    if len(result) > 1:
        return result
    else:
        return result[0]


def markovplot(t, y, a=None, names=None, model=None, comp=None, col='bgrcmyk', plotpy=False, plotr=True, newfig=True, **legend_kwargs):
    """
    Plot markov state distribution for ion channel.
    
    :param array_like t: time
    :param recarray y: state
    :param recarray a: algebraics
    :param names: sequence of variable names to include
    :param Cellmlmodel model: Cellmlmodel object
    :param str comp: (partial) name of component
    :param col: sequence of fill colours for stacked area chart
    :param bool plotpy: plot using Python (matplotlib)?
    :param bool plotr: plot using R (ggplot2)?
    :param bool newfig: create a new figure? (if using matplotlib)
    :param ``**legend_kwargs``: passed to matplotlib legend()
    
    If a is None, it will be computed using 
    ``model.rates_and_algebraic(t, y)``.
    If names is ``None``, include all "dimensionless" variables whose 
    component name contains *comp*.
    
    .. ggplot::
       
       from cgp.virtexp.elphys.examples import Bond
       from cgp.virtexp.elphys.clampable import markovplot
       
       bond = Bond()
       t, y, stats = bond.ap()
       p = markovplot(t, y, model=bond, comp="fast_sodium")
    """
    t, i = np.unique(t, return_index=True)
    y = y[i]
    if a is None:
        _dy, a = model.rates_and_algebraic(t, y)
    else:
        a = a[i]
    if names is None:
        names = sorted([ n for i in ('y', 'a') for n, c, u in zip(*model.legend[i]) if comp in c and u == 'dimensionless'
                       ])
        if len(names) < 2:
            return
        o = [ i for i in names if i.startswith('O') ]
        no = [ i for i in names if not i.startswith('O') ]
        names = o + no
    x = np.rec.fromarrays([ y[k] if k in y.dtype.names else a[k] for k in names ], names=names)
    xc = x.view(float).cumsum(axis=1).view(x.dtype).squeeze()
    if plotr:
        from ...utils.rec2dict import rec2dict
        r['df'] = r.cbind({'t': t}, r.as_data_frame(rec2dict(x)))
        for pkg in ('colorspace', 'reshape', 'ggplot2'):
            try:
                r.library(pkg)
            except RRuntimeError:
                r.install_packages(pkg, repos='http://cran.us.r-project.org')
                r.library(pkg)

        r['xm'] = r.melt(r.df, id_var='t')
        cmd = "qplot(t, value, fill=variable, geom='area', position='stack', data=xm) + scale_fill_brewer('State', palette='Set3') + theme_bw()"
        if comp:
            cmd += "+ labs(title='%s')" % comp
        return r(cmd)
    else:
        if plotpy:
            from pylab import figure, fill_between, legend, axis, Rectangle
            if newfig:
                figure()
            prev = 0
            col = [ col[(i % len(col))] for i in range(len(names)) ]
            symbols = []
            labels = []
            for i, k in enumerate(x.dtype.names):
                kwargs = dict(label=k, facecolor=col[i], edgecolor='none')
                fill_between(t, xc[k], prev, **kwargs)
                prev = xc[k]
                symbols.append(Rectangle((0, 0), 1, 1, **kwargs))
                labels.append(k)

            axis('tight')
            legend(reversed(symbols), reversed(labels), labelspacing=0, handlelength=1, handletextpad=0.5, borderaxespad=0, **legend_kwargs)
        return


def markovplots(t, y, a=None, model=None):
    """
    Markov plots for all components.
    
    >>> from cgp.virtexp.elphys.examples import Bond
    >>> bond = Bond()
    >>> t, y, stats = bond.ap()
    >>> from cgp.utils.thinrange import thin
    >>> i = thin(len(t), 100)
    
    (Below, the ... ellipsis makes doctest ignore messages that R may print 
    about packages getting loaded. However, doctest output cannot start with 
    ellipsis, so we need to print something else first. Sigh.)
    
    >>> print "Text output ignored:"; L = markovplots(t[i], y[i], model=bond)
    Text output ignored:...
    >>> from cgp.utils.rnumpy import r
    >>> r.windows(record=True) # doctest: +SKIP
    >>> print L # doctest: +SKIP    
    """
    comps = np.unique([ c for v in model.legend.values() for _n, c, _u in zip(*v) if c
                      ])
    plots = [ markovplot(t, y, model=model, comp=comp) for comp in comps ]
    return [ (c, p) for c, p in zip(comps, plots) if p ]


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)