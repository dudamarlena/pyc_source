# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/multivariance_classes.py
# Compiled at: 2008-03-29 07:06:44
"""Support module for multivariance.py"""
from gmisclib import gpkmisc
from gmisclib import Num
from gmisclib import die
BAYES_PRIOR_SPACE = 0
HUGE = 1e+30

class QuadraticNotNormalizable(ValueError):

    def __init__(self, s=''):
        ValueError.__init__(self, s)


def vec_inv_variance(start):
    vv = gpkmisc.vec_variance(start)
    assert Num.alltrue(Num.greater(vv, 0.0))
    return 1.0 / vv


def diag_inv_variance(start):
    return gpkmisc.make_diag(vec_inv_variance(start))


class modeldesc:
    """Virtual base class for a description of a model
                        of a particular size."""
    LF = (1.0 / 3.0) ** 2

    def __init__(self, ndim):
        assert ndim > 0
        self.dim = ndim

    def ndim(self):
        """This returns the dimensionality of the data."""
        return self.dim

    def modeldim(self):
        """This gives the dimensionality of the model,
                i.e. the number of parameters required to specify
                the means and covariance matrix(ces)."""
        raise RuntimeError, 'Virtual method'

    def unpack(self, prms):
        """This returns some subclass of model."""
        raise RuntimeError, 'Virtual method'

    def new(self, mu, invsigma):
        """Creates a model that contains data."""
        raise RuntimeError, 'Virtual method'

    def start(self, dataset):
        """Selects a random starting point from the dataset."""
        raise RuntimeError, 'Virtual method'


class model_with_numbers:
    """Virtual base class for adding in the functions
                you need when you create a model with known parameters
                (like mu and sigma)."""

    def __init__(self, details, bias):
        """Bias is an overall shift of the log probability up or
                down.  In a classifier, it is used to bias things toward
                one class or another."""
        self.desc = details
        self._offset = None
        self.bias = bias
        return

    def logp(self, datum):
        raise RuntimeError, 'Virtual method'

    def pack(self):
        """Returns a vector of parameters."""
        raise RuntimeError, 'Virtual method'

    def ndim(self):
        return self.desc.ndim()

    def unpack(self, prms):
        return self.desc.unpack(prms)

    def new(self, mu, invsigma):
        return self.desc.new(mu, invsigma)

    def start(self, dataset):
        return self.desc.start(dataset)

    def offset(self):
        if self._offset is None:
            self.addoff()
        return self._offset

    def addoff(self):
        raise RuntimeError, 'Virtual Function'


def _q_addoff--- This code section failed: ---

 L. 110         0  LOAD_GLOBAL           0  'BAYES_PRIOR_SPACE'
                3  LOAD_CONST               1
                6  BINARY_ADD       
                7  STORE_FAST            1  'phasespacefac'

 L. 111        10  LOAD_CONST               1
               13  LOAD_FAST             1  'phasespacefac'
               16  BINARY_SUBTRACT  
               17  STORE_FAST            2  'determinantfac'

 L. 112        20  LOAD_GLOBAL           1  'Num'
               23  LOAD_ATTR             2  'sum'
               26  LOAD_GLOBAL           1  'Num'
               29  LOAD_ATTR             3  'diagonal'
               32  LOAD_FAST             0  'self'
               35  LOAD_ATTR             4  'invsigma'
               38  CALL_FUNCTION_1       1  None
               41  CALL_FUNCTION_1       1  None
               44  STORE_FAST            3  'trace'

 L. 113        47  LOAD_FAST             3  'trace'
               50  LOAD_CONST               0.0
               53  COMPARE_OP            1  <=
               56  POP_JUMP_IF_FALSE    71  'to 71'

 L. 114        59  LOAD_GLOBAL           5  'QuadraticNotNormalizable'
               62  LOAD_CONST               'Input trace is nonpositive.'
               65  RAISE_VARARGS_2       2  None
               68  JUMP_FORWARD          0  'to 71'
             71_0  COME_FROM            68  '68'

 L. 115        71  SETUP_EXCEPT         28  'to 102'

 L. 116        74  LOAD_GLOBAL           1  'Num'
               77  LOAD_ATTR             6  'LA'
               80  LOAD_ATTR             7  'Heigenvalues'
               83  LOAD_FAST             0  'self'
               86  LOAD_ATTR             4  'invsigma'
               89  CALL_FUNCTION_1       1  None
               92  LOAD_FAST             0  'self'
               95  STORE_ATTR            8  'ev'
               98  POP_BLOCK        
               99  JUMP_FORWARD         57  'to 159'
            102_0  COME_FROM            71  '71'

 L. 117       102  DUP_TOP          
              103  LOAD_GLOBAL           1  'Num'
              106  LOAD_ATTR             6  'LA'
              109  LOAD_ATTR             9  'LinAlgError'
              112  COMPARE_OP           10  exception-match
              115  POP_JUMP_IF_FALSE   158  'to 158'
              118  POP_TOP          
              119  STORE_FAST            4  'x'
              122  POP_TOP          

 L. 118       123  LOAD_GLOBAL          10  'die'
              126  LOAD_ATTR            11  'warn'
              129  LOAD_CONST               'While computing the volume of the probability distribution: %s'
              132  LOAD_GLOBAL          12  'str'
              135  LOAD_FAST             4  'x'
              138  CALL_FUNCTION_1       1  None
              141  BINARY_MODULO    
              142  CALL_FUNCTION_1       1  None
              145  POP_TOP          

 L. 119       146  LOAD_GLOBAL           5  'QuadraticNotNormalizable'
              149  LOAD_FAST             4  'x'
              152  RAISE_VARARGS_2       2  None
              155  JUMP_FORWARD          1  'to 159'
              158  END_FINALLY      
            159_0  COME_FROM           158  '158'
            159_1  COME_FROM            99  '99'

 L. 120       159  LOAD_GLOBAL           1  'Num'
              162  LOAD_ATTR            13  'alltrue'
              165  LOAD_FAST             0  'self'
              168  LOAD_ATTR             8  'ev'
              171  LOAD_CONST               0.0
              174  COMPARE_OP            4  >
              177  CALL_FUNCTION_1       1  None
              180  POP_JUMP_IF_TRUE    195  'to 195'

 L. 121       183  LOAD_GLOBAL           5  'QuadraticNotNormalizable'
              186  LOAD_CONST               'Some eigenvalues are zero or negative.'
              189  RAISE_VARARGS_2       2  None
              192  JUMP_FORWARD          0  'to 195'
            195_0  COME_FROM           192  '192'

 L. 122       195  LOAD_GLOBAL          14  'abs'
              198  LOAD_GLOBAL           1  'Num'
              201  LOAD_ATTR             2  'sum'
              204  LOAD_FAST             0  'self'
              207  LOAD_ATTR             8  'ev'
              210  CALL_FUNCTION_1       1  None
              213  LOAD_FAST             3  'trace'
              216  BINARY_SUBTRACT  
              217  CALL_FUNCTION_1       1  None
              220  LOAD_CONST               1e-10
              223  LOAD_CONST               1e-06
              226  LOAD_FAST             3  'trace'
              229  BINARY_MULTIPLY  
              230  BINARY_ADD       
              231  COMPARE_OP            0  <
              234  POP_JUMP_IF_TRUE    268  'to 268'
              237  LOAD_ASSERT              AssertionError
              240  LOAD_CONST               'Bad Eigenvalues run: trace not matched: %g to %g'
              243  LOAD_FAST             3  'trace'
              246  LOAD_GLOBAL           1  'Num'
              249  LOAD_ATTR             2  'sum'
              252  LOAD_FAST             0  'self'
              255  LOAD_ATTR             8  'ev'
              258  CALL_FUNCTION_1       1  None
              261  BUILD_TUPLE_2         2 
              264  BINARY_MODULO    
              265  RAISE_VARARGS_2       2  None

 L. 123       268  LOAD_GLOBAL           1  'Num'
              271  LOAD_ATTR             2  'sum'
              274  LOAD_FAST             0  'self'
              277  LOAD_ATTR             8  'ev'
              280  CALL_FUNCTION_1       1  None
              283  LOAD_CONST               0.0
              286  COMPARE_OP            4  >
              289  POP_JUMP_IF_TRUE    301  'to 301'
              292  LOAD_ASSERT              AssertionError
              295  LOAD_CONST               'Input trace is nonpositive.'
              298  RAISE_VARARGS_2       2  None

 L. 124       301  LOAD_GLOBAL           1  'Num'
              304  LOAD_ATTR             2  'sum'
              307  LOAD_GLOBAL           1  'Num'
              310  LOAD_ATTR            16  'log'
              313  LOAD_FAST             0  'self'
              316  LOAD_ATTR             8  'ev'
              319  CALL_FUNCTION_1       1  None
              322  CALL_FUNCTION_1       1  None
              325  LOAD_FAST             2  'determinantfac'
              328  BINARY_MULTIPLY  
              329  LOAD_FAST             0  'self'
              332  STORE_ATTR           17  '_offset'

Parse error at or near `LOAD_FAST' instruction at offset 329


def _d_addoff(self):
    phasespacefac = BAYES_PRIOR_SPACE + 1
    determinantfac = 1 - phasespacefac
    self.ev = Num.array(self.invsigma, copy=True)
    if not Num.alltrue(self.ev > 0.0):
        raise QuadraticNotNormalizable, 'Some eigenvalues are zero or negative.'
    self._offset = Num.sum(Num.log(self.ev)) * determinantfac