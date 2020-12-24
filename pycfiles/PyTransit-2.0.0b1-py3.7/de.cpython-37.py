# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/utils/de.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 7409 bytes
"""
Implements the differential evolution optimization method by Storn & Price
(Storn, R., Price, K., Journal of Global Optimization 11: 341--359, 1997)

.. moduleauthor:: Hannu Parviainen <hpparvi@gmail.com>
"""
from numba import njit
from numpy import asarray, zeros, zeros_like, tile, array, argmin, mod
from numpy.random import random, randint, rand, seed as rseed, uniform

def wrap(v, vmin, vmax):
    w = vmax - vmin
    return vmin + mod(asarray(v) - vmin, w)


@njit
def evolve_vector--- This code section failed: ---

 L.  36         0  LOAD_FAST                'pop'
                2  LOAD_ATTR                shape
                4  UNPACK_SEQUENCE_2     2 
                6  STORE_FAST               'npop'
                8  STORE_FAST               'ndim'

 L.  39        10  LOAD_FAST                'i'
               12  LOAD_FAST                'i'
               14  LOAD_FAST                'i'
               16  ROT_THREE        
               18  ROT_TWO          
               20  STORE_FAST               'v1'
               22  STORE_FAST               'v2'
               24  STORE_FAST               'v3'

 L.  40        26  SETUP_LOOP           48  'to 48'
               28  LOAD_FAST                'v1'
               30  LOAD_FAST                'i'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L.  41        36  LOAD_GLOBAL              randint
               38  LOAD_FAST                'npop'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  STORE_FAST               'v1'
               44  JUMP_BACK            28  'to 28'
             46_0  COME_FROM            34  '34'
               46  POP_BLOCK        
             48_0  COME_FROM_LOOP       26  '26'

 L.  42        48  SETUP_LOOP           78  'to 78'
               50  LOAD_FAST                'v2'
               52  LOAD_FAST                'i'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_TRUE     66  'to 66'
               58  LOAD_FAST                'v2'
               60  LOAD_FAST                'v1'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    76  'to 76'
             66_0  COME_FROM            56  '56'

 L.  43        66  LOAD_GLOBAL              randint
               68  LOAD_FAST                'npop'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  STORE_FAST               'v2'
               74  JUMP_BACK            50  'to 50'
             76_0  COME_FROM            64  '64'
               76  POP_BLOCK        
             78_0  COME_FROM_LOOP       48  '48'

 L.  44        78  SETUP_LOOP          116  'to 116'
               80  LOAD_FAST                'v3'
               82  LOAD_FAST                'i'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_TRUE    104  'to 104'
               88  LOAD_FAST                'v3'
               90  LOAD_FAST                'v2'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_TRUE    104  'to 104'
               96  LOAD_FAST                'v3'
               98  LOAD_FAST                'v1'
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   114  'to 114'
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            86  '86'

 L.  45       104  LOAD_GLOBAL              randint
              106  LOAD_FAST                'npop'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  STORE_FAST               'v3'
              112  JUMP_BACK            80  'to 80'
            114_0  COME_FROM           102  '102'
              114  POP_BLOCK        
            116_0  COME_FROM_LOOP       78  '78'

 L.  48       116  LOAD_FAST                'pop'
              118  LOAD_FAST                'v1'
              120  BINARY_SUBSCR    
              122  LOAD_FAST                'f'
              124  LOAD_FAST                'pop'
              126  LOAD_FAST                'v2'
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'pop'
              132  LOAD_FAST                'v3'
              134  BINARY_SUBSCR    
              136  BINARY_SUBTRACT  
              138  BINARY_MULTIPLY  
              140  BINARY_ADD       
              142  STORE_FAST               'v'

 L.  51       144  LOAD_GLOBAL              randint
              146  LOAD_FAST                'ndim'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  STORE_FAST               'jf'

 L.  52       152  LOAD_GLOBAL              rand
              154  LOAD_FAST                'ndim'
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  STORE_FAST               'co'

 L.  53       160  SETUP_LOOP          214  'to 214'
              162  LOAD_GLOBAL              range
              164  LOAD_FAST                'ndim'
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  GET_ITER         
            170_0  COME_FROM           192  '192'
            170_1  COME_FROM           184  '184'
              170  FOR_ITER            212  'to 212'
              172  STORE_FAST               'j'

 L.  54       174  LOAD_FAST                'co'
              176  LOAD_FAST                'j'
              178  BINARY_SUBSCR    
              180  LOAD_FAST                'c'
              182  COMPARE_OP               >
              184  POP_JUMP_IF_FALSE   170  'to 170'
              186  LOAD_FAST                'j'
              188  LOAD_FAST                'jf'
              190  COMPARE_OP               !=
              192  POP_JUMP_IF_FALSE   170  'to 170'

 L.  55       194  LOAD_FAST                'pop'
              196  LOAD_FAST                'i'
              198  LOAD_FAST                'j'
              200  BUILD_TUPLE_2         2 
              202  BINARY_SUBSCR    
              204  LOAD_FAST                'v'
              206  LOAD_FAST                'j'
              208  STORE_SUBSCR     
              210  JUMP_BACK           170  'to 170'
              212  POP_BLOCK        
            214_0  COME_FROM_LOOP      160  '160'

 L.  56       214  LOAD_FAST                'v'
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 114


@njit
def evolve_population--- This code section failed: ---

 L.  61         0  LOAD_FAST                'pop'
                2  LOAD_ATTR                shape
                4  UNPACK_SEQUENCE_2     2 
                6  STORE_FAST               'npop'
                8  STORE_FAST               'ndim'

 L.  63        10  SETUP_LOOP          262  'to 262'
               12  LOAD_GLOBAL              range
               14  LOAD_FAST                'npop'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  GET_ITER         
               20  FOR_ITER            260  'to 260'
               22  STORE_FAST               'i'

 L.  66        24  LOAD_FAST                'i'
               26  LOAD_FAST                'i'
               28  LOAD_FAST                'i'
               30  ROT_THREE        
               32  ROT_TWO          
               34  STORE_FAST               'v1'
               36  STORE_FAST               'v2'
               38  STORE_FAST               'v3'

 L.  67        40  SETUP_LOOP           62  'to 62'
               42  LOAD_FAST                'v1'
               44  LOAD_FAST                'i'
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L.  68        50  LOAD_GLOBAL              randint
               52  LOAD_FAST                'npop'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  STORE_FAST               'v1'
               58  JUMP_BACK            42  'to 42'
             60_0  COME_FROM            48  '48'
               60  POP_BLOCK        
             62_0  COME_FROM_LOOP       40  '40'

 L.  69        62  SETUP_LOOP           92  'to 92'
               64  LOAD_FAST                'v2'
               66  LOAD_FAST                'i'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_TRUE     80  'to 80'
               72  LOAD_FAST                'v2'
               74  LOAD_FAST                'v1'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE    90  'to 90'
             80_0  COME_FROM            70  '70'

 L.  70        80  LOAD_GLOBAL              randint
               82  LOAD_FAST                'npop'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  STORE_FAST               'v2'
               88  JUMP_BACK            64  'to 64'
             90_0  COME_FROM            78  '78'
               90  POP_BLOCK        
             92_0  COME_FROM_LOOP       62  '62'

 L.  71        92  SETUP_LOOP          130  'to 130'
               94  LOAD_FAST                'v3'
               96  LOAD_FAST                'i'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    118  'to 118'
              102  LOAD_FAST                'v3'
              104  LOAD_FAST                'v2'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_TRUE    118  'to 118'
              110  LOAD_FAST                'v3'
              112  LOAD_FAST                'v1'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   128  'to 128'
            118_0  COME_FROM           108  '108'
            118_1  COME_FROM           100  '100'

 L.  72       118  LOAD_GLOBAL              randint
              120  LOAD_FAST                'npop'
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  STORE_FAST               'v3'
              126  JUMP_BACK            94  'to 94'
            128_0  COME_FROM           116  '116'
              128  POP_BLOCK        
            130_0  COME_FROM_LOOP       92  '92'

 L.  75       130  LOAD_FAST                'pop'
              132  LOAD_FAST                'v1'
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'f'
              138  LOAD_FAST                'pop'
              140  LOAD_FAST                'v2'
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'pop'
              146  LOAD_FAST                'v3'
              148  BINARY_SUBSCR    
              150  BINARY_SUBTRACT  
              152  BINARY_MULTIPLY  
              154  BINARY_ADD       
              156  STORE_FAST               'v'

 L.  78       158  LOAD_GLOBAL              rand
              160  LOAD_FAST                'ndim'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  STORE_FAST               'co'

 L.  79       166  SETUP_LOOP          234  'to 234'
              168  LOAD_GLOBAL              range
              170  LOAD_FAST                'ndim'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  GET_ITER         
              176  FOR_ITER            232  'to 232'
              178  STORE_FAST               'j'

 L.  80       180  LOAD_FAST                'co'
              182  LOAD_FAST                'j'
              184  BINARY_SUBSCR    
              186  LOAD_FAST                'c'
              188  COMPARE_OP               <=
              190  POP_JUMP_IF_FALSE   210  'to 210'

 L.  81       192  LOAD_FAST                'v'
              194  LOAD_FAST                'j'
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'pop2'
              200  LOAD_FAST                'i'
              202  LOAD_FAST                'j'
              204  BUILD_TUPLE_2         2 
              206  STORE_SUBSCR     
              208  JUMP_BACK           176  'to 176'
            210_0  COME_FROM           190  '190'

 L.  83       210  LOAD_FAST                'pop'
              212  LOAD_FAST                'i'
              214  LOAD_FAST                'j'
              216  BUILD_TUPLE_2         2 
              218  BINARY_SUBSCR    
              220  LOAD_FAST                'pop2'
              222  LOAD_FAST                'i'
              224  LOAD_FAST                'j'
              226  BUILD_TUPLE_2         2 
              228  STORE_SUBSCR     
              230  JUMP_BACK           176  'to 176'
              232  POP_BLOCK        
            234_0  COME_FROM_LOOP      166  '166'

 L.  86       234  LOAD_GLOBAL              randint
              236  LOAD_FAST                'ndim'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  STORE_FAST               'j'

 L.  87       242  LOAD_FAST                'v'
              244  LOAD_FAST                'j'
              246  BINARY_SUBSCR    
              248  LOAD_FAST                'pop2'
              250  LOAD_FAST                'i'
              252  LOAD_FAST                'j'
              254  BUILD_TUPLE_2         2 
              256  STORE_SUBSCR     
              258  JUMP_BACK            20  'to 20'
              260  POP_BLOCK        
            262_0  COME_FROM_LOOP       10  '10'

 L.  89       262  LOAD_FAST                'pop2'
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 128


class DiffEvol(object):
    __doc__ = '\n    Implements the differential evolution optimization method by Storn & Price\n    (Storn, R., Price, K., Journal of Global Optimization 11: 341--359, 1997)\n\n    :param fun:\n       the function to be minimized\n\n    :param bounds:\n        parameter bounds as [npar,2] array\n\n    :param npop:\n        the size of the population (5*D - 10*D)\n\n    :param  f: (optional)\n        the difference amplification factor. Values of 0.5-0.8 are good in most cases.\n\n    :param c: (optional)\n        The cross-over probability. Use 0.9 to test for fast convergence, and smaller\n        values (~0.1) for a more elaborate search.\n\n    :param seed: (optional)\n        Random seed\n\n    :param maximize: (optional)\n        Switch setting whether to maximize or minimize the function. Defaults to minimization.\n    '

    def __init__(self, fun, bounds, npop, f=None, c=None, seed=None, maximize=False, vectorize=False, cbounds=(0.25, 1), fbounds=(0.25, 0.75), pool=None, min_ptp=0.01, args=[], kwargs={}):
        if seed is not None:
            rseed(seed)
        else:
            self.minfun = _function_wrapper(fun, args, kwargs)
            self.bounds = asarray(bounds)
            self.n_pop = npop
            self.n_par = self.bounds.shape[0]
            self.bl = tile(self.bounds[:, 0], [npop, 1])
            self.bw = tile(self.bounds[:, 1] - self.bounds[:, 0], [npop, 1])
            self.m = -1 if maximize else 1
            self.pool = pool
            self.args = args
            if self.pool is not None:
                self.map = self.pool.map
            else:
                self.map = map
            self.periodic = []
            self.min_ptp = min_ptp
            self.cmin = cbounds[0]
            self.cmax = cbounds[1]
            self.cbounds = cbounds
            self.fbounds = fbounds
            self.seed = seed
            self.f = f
            self.c = c
            self._population = asarray(self.bl + random([self.n_pop, self.n_par]) * self.bw)
            self._fitness = zeros(npop)
            self._minidx = None
            self._trial_pop = zeros_like(self._population)
            self._trial_fit = zeros_like(self._fitness)
            if vectorize:
                self._eval = self._eval_vfun
            else:
                self._eval = self._eval_sfun

    @property
    def population(self):
        """The parameter vector population"""
        return self._population

    @property
    def minimum_value(self):
        """The best-fit value of the optimized function"""
        return self._fitness[self._minidx]

    @property
    def minimum_location(self):
        """The best-fit solution"""
        return self._population[self._minidx, :]

    @property
    def minimum_index(self):
        """Index of the best-fit solution"""
        return self._minidx

    def optimize(self, ngen):
        """Run the optimizer for ``ngen`` generations"""
        for res in self(ngen):
            pass

        return res

    def __call__(self, ngen=1):
        return self._eval(ngen)

    def _eval_sfun(self, ngen=1):
        """Run DE for a function that takes a single pv as an input and retuns a single value."""
        popc, fitc = self._population, self._fitness
        popt, fitt = self._trial_pop, self._trial_fit
        for ipop in range(self.n_pop):
            fitc[ipop] = self.m * self.minfun(popc[ipop, :])

        for igen in range(ngen):
            f = self.f or uniform(*self.fbounds)
            c = self.c or uniform(*self.cbounds)
            popt = evolve_population(popc, popt, f, c)
            fitt[:] = self.m * array(list(self.map(self.minfun, popt)))
            msk = fitt < fitc
            popc[msk, :] = popt[msk, :]
            fitc[msk] = fitt[msk]
            self._minidx = argmin(fitc)
            if fitc.ptp() < self.min_ptp:
                break
            yield (
             popc[self._minidx, :], fitc[self._minidx])

    def _eval_vfun(self, ngen=1):
        """Run DE for a function that takes the whole population as an input and retuns a value for each pv."""
        popc, fitc = self._population, self._fitness
        popt, fitt = self._trial_pop, self._trial_fit
        fitc[:] = self.m * self.minfun(self._population)
        for igen in range(ngen):
            f = self.f or uniform(*self.fbounds)
            c = self.c or uniform(*self.cbounds)
            popt = evolve_population(popc, popt, f, c)
            fitt[:] = self.m * self.minfun(popt)
            msk = fitt < fitc
            popc[msk, :] = popt[msk, :]
            fitc[msk] = fitt[msk]
            self._minidx = argmin(fitc)
            if fitc.ptp() < self.min_ptp:
                break
            yield (
             popc[self._minidx, :], fitc[self._minidx])


class _function_wrapper(object):

    def __init__(self, f, args=[], kwargs={}):
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def __call__(self, x):
        return (self.f)(x, *(self.args), **self.kwargs)