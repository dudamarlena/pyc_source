# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/multivariance_mm.py
# Compiled at: 2008-02-16 08:19:02
"""This a helper module for multivariance.py"""
import Num, multivariance_classes as M, random, g_implements

class datum_c:

    def __init__(self, vector, classid):
        self.classid = classid
        self.value = vector


def _multi_mu__init__--- This code section failed: ---

 L.  20         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'dictops'
                9  STORE_FAST            5  'dictops'

 L.  22        12  LOAD_FAST             1  'dataset'
               15  LOAD_CONST               None
               18  COMPARE_OP            9  is-not
               21  POP_JUMP_IF_FALSE   242  'to 242'

 L.  23        24  LOAD_FAST             4  'details'
               27  LOAD_CONST               None
               30  COMPARE_OP            8  is
               33  POP_JUMP_IF_TRUE     42  'to 42'
               36  LOAD_ASSERT              AssertionError
               39  RAISE_VARARGS_1       1  None

 L.  24        42  LOAD_FAST             2  'ndim'
               45  LOAD_CONST               None
               48  COMPARE_OP            8  is
               51  POP_JUMP_IF_FALSE    66  'to 66'
               54  LOAD_FAST             3  'idmap'
               57  LOAD_CONST               None
               60  COMPARE_OP            8  is
             63_0  COME_FROM            51  '51'
               63  POP_JUMP_IF_TRUE     72  'to 72'
               66  LOAD_ASSERT              AssertionError
               69  RAISE_VARARGS_1       1  None

 L.  25        72  LOAD_CONST               -1
               75  LOAD_CONST               None
               78  IMPORT_NAME           3  'nice_hash'
               81  STORE_FAST            6  'nice_hash'

 L.  26        84  LOAD_FAST             2  'ndim'
               87  LOAD_CONST               None
               90  COMPARE_OP            8  is
               93  POP_JUMP_IF_FALSE   108  'to 108'
               96  LOAD_FAST             3  'idmap'
               99  LOAD_CONST               None
              102  COMPARE_OP            8  is
            105_0  COME_FROM            93  '93'
              105  POP_JUMP_IF_TRUE    114  'to 114'
              108  LOAD_ASSERT              AssertionError
              111  RAISE_VARARGS_1       1  None

 L.  27       114  LOAD_FAST             6  'nice_hash'
              117  LOAD_ATTR             3  'nice_hash'
              120  LOAD_LAMBDA              '<code_object <lambda>>'
              123  MAKE_FUNCTION_0       0  None
              126  CALL_FUNCTION_1       1  None
              129  STORE_FAST            7  'h'

 L.  28       132  SETUP_LOOP           73  'to 208'
              135  LOAD_FAST             1  'dataset'
              138  GET_ITER         
              139  FOR_ITER             65  'to 207'
              142  STORE_FAST            8  't'

 L.  29       145  LOAD_GLOBAL           4  'g_implements'
              148  LOAD_ATTR             5  'impl'
              151  LOAD_FAST             8  't'
              154  LOAD_GLOBAL           6  'datum_c'
              157  CALL_FUNCTION_2       2  None
              160  POP_JUMP_IF_TRUE    188  'to 188'
              163  LOAD_ASSERT              AssertionError

 L.  30       166  LOAD_CONST               'Bad input type: %s'
              169  LOAD_GLOBAL           4  'g_implements'
              172  LOAD_ATTR             7  'why'
              175  LOAD_FAST             8  't'
              178  LOAD_GLOBAL           6  'datum_c'
              181  CALL_FUNCTION_2       2  None
              184  BINARY_MODULO    
              185  RAISE_VARARGS_2       2  None

 L.  31       188  LOAD_FAST             7  'h'
              191  LOAD_ATTR             8  'add'
              194  LOAD_FAST             8  't'
              197  LOAD_ATTR             9  'classid'
              200  CALL_FUNCTION_1       1  None
              203  POP_TOP          
              204  JUMP_BACK           139  'to 139'
              207  POP_BLOCK        
            208_0  COME_FROM           132  '132'

 L.  32       208  LOAD_GLOBAL          10  'len'
              211  LOAD_FAST             1  'dataset'
              214  LOAD_CONST               0
              217  BINARY_SUBSCR    
              218  LOAD_ATTR            11  'value'
              221  CALL_FUNCTION_1       1  None
              224  STORE_FAST            2  'ndim'

 L.  33       227  LOAD_FAST             7  'h'
              230  LOAD_ATTR            12  'map'
              233  CALL_FUNCTION_0       0  None
              236  STORE_FAST            3  'idmap'
              239  JUMP_FORWARD         66  'to 308'

 L.  34       242  LOAD_FAST             4  'details'
              245  LOAD_CONST               None
              248  COMPARE_OP            9  is-not
              251  POP_JUMP_IF_FALSE   308  'to 308'

 L.  35       254  LOAD_FAST             2  'ndim'
              257  LOAD_CONST               None
              260  COMPARE_OP            8  is
              263  POP_JUMP_IF_FALSE   278  'to 278'
              266  LOAD_FAST             3  'idmap'
              269  LOAD_CONST               None
              272  COMPARE_OP            8  is
            275_0  COME_FROM           263  '263'
              275  POP_JUMP_IF_TRUE    284  'to 284'
              278  LOAD_ASSERT              AssertionError
              281  RAISE_VARARGS_1       1  None

 L.  36       284  LOAD_FAST             4  'details'
              287  LOAD_ATTR            13  'ndim'
              290  CALL_FUNCTION_0       0  None
              293  STORE_FAST            2  'ndim'

 L.  37       296  LOAD_FAST             4  'details'
              299  LOAD_ATTR            14  'id_to_int'
              302  STORE_FAST            3  'idmap'
              305  JUMP_FORWARD          0  'to 308'
            308_0  COME_FROM           305  '305'
            308_1  COME_FROM           239  '239'

 L.  38       308  LOAD_FAST             2  'ndim'
              311  LOAD_CONST               None
              314  COMPARE_OP            9  is-not
              317  POP_JUMP_IF_FALSE   332  'to 332'
              320  LOAD_FAST             3  'idmap'
              323  LOAD_CONST               None
              326  COMPARE_OP            9  is-not
            329_0  COME_FROM           317  '317'
              329  POP_JUMP_IF_TRUE    338  'to 338'
              332  LOAD_ASSERT              AssertionError
              335  RAISE_VARARGS_1       1  None

 L.  39       338  LOAD_GLOBAL          10  'len'
              341  LOAD_FAST             3  'idmap'
              344  CALL_FUNCTION_1       1  None
              347  LOAD_FAST             0  'self'
              350  STORE_ATTR           15  'Nmu'

 L.  40       353  LOAD_FAST             3  'idmap'
              356  LOAD_ATTR            16  'copy'
              359  CALL_FUNCTION_0       0  None
              362  LOAD_FAST             0  'self'
              365  STORE_ATTR           14  'id_to_int'

 L.  41       368  LOAD_FAST             5  'dictops'
              371  LOAD_ATTR            17  'rev1to1'
              374  LOAD_FAST             3  'idmap'
              377  CALL_FUNCTION_1       1  None
              380  LOAD_FAST             0  'self'
              383  STORE_ATTR           18  'int_to_id'

 L.  44       386  SETUP_LOOP           53  'to 442'
              389  LOAD_GLOBAL          19  'range'
              392  LOAD_GLOBAL          10  'len'
              395  LOAD_FAST             0  'self'
              398  LOAD_ATTR            18  'int_to_id'
              401  CALL_FUNCTION_1       1  None
              404  CALL_FUNCTION_1       1  None
              407  GET_ITER         
              408  FOR_ITER             30  'to 441'
              411  STORE_FAST            9  'i'

 L.  45       414  LOAD_FAST             9  'i'
              417  LOAD_FAST             0  'self'
              420  LOAD_ATTR            18  'int_to_id'
              423  COMPARE_OP            6  in
              426  POP_JUMP_IF_TRUE    408  'to 408'
              429  LOAD_ASSERT              AssertionError
              432  LOAD_CONST               'Not a good mapping to indices.'
              435  RAISE_VARARGS_2       2  None
              438  JUMP_BACK           408  'to 408'
              441  POP_BLOCK        
            442_0  COME_FROM           386  '386'
              442  LOAD_CONST               None
              445  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 207


class multi_mu(M.modeldesc):
    """This describes a quadratic model of a known size,
                        with multiple means
                        (one for each different class of data)."""

    def __init__(self, dataset=None, ndim=None, idmap=None, details=None):
        M.modeldesc.__init__(self, ndim)
        _multi_mu__init__(self, dataset, ndim, idmap, details)

    __init__.__doc__ = _multi_mu__init__.__doc__

    def modeldim(self):
        m = self.ndim()
        return self.Nmu * m + m * (m + 1) / 2

    def unpack(self, prms):
        m = self.ndim()
        assert len(prms) == self.modeldim()
        mu = {}
        for i in range(self.Nmu):
            mu[self.int_to_id[i]] = prms[i * m:(i + 1) * m]

        invsigma = Num.zeros((m, m), Num.Float)
        j = self.Nmu * m
        for i in range(m):
            tmp = prms[j:j + (m - i)]
            invsigma[i, i:] = tmp
            invsigma[i:, i] = tmp
            j += m - i

        return self.new(mu, invsigma)

    def new(self, mu, invsigma, bias=0.0):
        """Mu is a mapping of classids to vectors.  invsigma is a square matrix."""
        assert type(mu) == type({})
        return multi_mu_with_numbers(mu, invsigma, self, bias)

    def start(self, data):
        raise RuntimeError, 'Broken'
        import nice_hash
        h = nice_hash.nice_hash(lambda x: x.classid)
        for datum in data:
            assert g_implements.impl(datum, datum_c)
            h.add(datum)

        if len(data) > 1:
            ivar = M.diag_inv_variance([ datum.value for datum in data ])
        else:
            ivar = Num.identity(self.ndim())
        divar = Num.diagonal(ivar)
        rnd = {}
        var = {}
        for k, v in h.rmap().items():
            rnd[self.int_to_id[k]] = random.choice(v).value
            var[self.int_to_id[k]] = 1.0 / divar

        return (self.new(rnd, ivar),
         self.new(var, Num.outerproduct(divar, divar)))


class multi_mu_with_numbers(M.model_with_numbers):

    def __init__(self, mu, invsigma, details, bias=0.0, offset=None):
        """self.mu, self.invsigma, and self._offset should be considered
                read-only for all users of this class."""
        assert isinstance(details, multi_mu)
        M.model_with_numbers.__init__(self, details, bias)
        self.mu = Num.array(mu, copy=True)
        self.invsigma = Num.array(invsigma)
        self._offset = offset

    def __str__(self):
        return '<multi_mu: mu=%s; invsigma=%s >' % (str(self.mu), str(self.invsigma))

    __repr__ = __str__
    addoff = M._q_addoff

    def pack(self):
        n = self.ndim()
        assert self.invsigma.shape == (n, n)
        assert len(self.mu) == self.desc.Nmu
        tmp = []
        for i in range(self.desc.Nmu):
            tmp.append(self.mu[self.desc.int_to_id[i]])

        for i in range(n):
            tmp.append(self.invsigma[i, i:])

        return Num.concatenate(tmp)

    def logp(self, datum):
        delta = datum.value - self.mu[datum.classid]
        parab = Num.dot(delta, Num.matrixmultiply(self.invsigma, delta))
        if not parab >= 0.0:
            raise M.QuadraticNotNormalizable, 'Not positive-definite'
        return -parab / 2.0 + self.offset() + self.bias


class multi_mu_diag(M.modeldesc):
    """This describes a quadratic model of a known size,
                        with multiple means (one for each different class of data).
                        The covariance matrix is shared and diagonal."""

    def __init__(self, dataset=None, ndim=None, idmap=None, details=None):
        M.modeldesc.__init__(self, ndim)
        _multi_mu__init__(self, dataset, ndim, idmap, details)

    __init__.__doc__ = _multi_mu__init__.__doc__

    def modeldim(self):
        m = self.ndim()
        return self.Nmu * m + m

    def unpack(self, prms):
        m = self.ndim()
        assert len(prms) == self.modeldim()
        mu = {}
        for i in range(self.Nmu):
            mu[self.int_to_id[i]] = prms[i * m:(i + 1) * m]

        j = self.Nmu * m
        invsigma = prms[j:]
        return self.new(mu, invsigma)

    def new(self, mu, invsigma, bias=0.0):
        """Mu is a mapping of classids to vectors.  Invsigma is a vector."""
        assert type(mu) == type({})
        return multi_mu_diag_with_numbers(mu, invsigma, self, bias)

    def start(self, data):
        raise RuntimeError, 'Broken'
        import nice_hash
        h = nice_hash.nice_hash(lambda x: x.classid)
        for datum in data:
            assert g_implements.impl(datum, datum_c)
            h.add(datum)

        if len(data) > 1:
            divar = M.vec_inv_variance([ datum.value for datum in data ])
        else:
            divar = Num.ones((self.ndim(),), Num.Float)
        rnd = {}
        var = {}
        for k, v in h.rmap().items():
            rnd[self.int_to_id[k]] = random.choice(v).value
            var[self.int_to_id[k]] = 1.0 / divar

        return (
         self.new(rnd, divar),
         self.new(var, divar * divar))


class multi_mu_diag_with_numbers(M.model_with_numbers):

    def __init__(self, mu, invsigma, details, bias=0.0, offset=None):
        """self.mu, self.invsigma, and self._offset should be considered
                read-only for all users of this class."""
        assert isinstance(details, multi_mu_diag)
        M.model_with_numbers.__init__(self, details, bias)
        self.mu = Num.array(mu)
        self.invsigma = Num.array(invsigma)
        self._offset = offset

    def __str__(self):
        return '<multi_mu_diag: mu=%s; invsigma=%s >' % (str(self.mu), str(self.invsigma))

    __repr__ = __str__
    addoff = M._d_addoff

    def pack(self):
        n = self.ndim()
        assert self.invsigma.shape == (n,)
        assert len(self.mu) == self.desc.Nmu
        tmp = []
        for i in range(self.desc.Nmu):
            tmp.append(self.mu[self.desc.int_to_id[i]])

        tmp.append(self.invsigma)
        return Num.concatenate(tmp)

    def logp(self, datum):
        delta = datum.value - self.mu[datum.classid]
        parab = Num.sum(self.invsigma * delta ** 2)
        if not parab >= 0.0:
            raise M.QuadraticNotNormalizable, 'Not positive-definite'
        return -parab / 2.0 + self.offset() + self.bias