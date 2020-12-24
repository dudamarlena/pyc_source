# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/lsqfitgp/_GP.py
# Compiled at: 2020-04-26 18:49:26
# Size of source mod 2**32: 35043 bytes
import itertools, sys, builtins, abc, gvar
from autograd import numpy as np
from autograd.scipy import linalg
from autograd.builtins import isinstance
from . import _Kernel
from . import _linalg
from . import _array
from . import _Deriv
__all__ = [
 'GP']

def _concatenate_noop(alist, **kw):
    """
    Like np.concatenate, but does not make a copy when concatenating only one
    array.
    """
    if len(alist) == 1:
        return np.array((alist[0]), copy=False)
    return (np.concatenate)(alist, **kw)


def _triu_indices_and_back(n):
    """
    Return indices to get the upper triangular part of a matrix, and indices to
    convert a flat array of upper triangular elements to a symmetric matrix.
    """
    indices = np.triu_indices(n)
    q = np.empty((n, n), int)
    a = np.arange(len(indices[0]))
    q[indices] = a
    q[tuple(reversed(indices))] = a
    return (indices, q)


def _block_matrix(blocks):
    """
    Like np.block, but is autograd-friendly and avoids a copy when there is
    only one block.
    """
    return _concatenate_noop([_concatenate_noop(row, axis=1) for row in blocks], axis=0)


def _isarraylike_nostructured(x):
    return isinstance(x, (list, np.ndarray))


def _isarraylike(x):
    return _isarraylike_nostructured(x) or isinstance(x, _array.StructuredArray)


def _asarray(x):
    if isinstance(x, _array.StructuredArray):
        return x
    return np.array(x, copy=False)


def _isdictlike(x):
    return isinstance(x, (dict, gvar.BufferDict))


def _compatible_dtypes(d1, d2):
    """
    Function to check x arrays datatypes passed to GP.addx. If the dtype is
    structured, it checks the structure of the fields is the same, but allows
    casting of concrete dtypes (like, in one array a field can be int, in
    another float, as long as the field name and position is the same).
    Currently not used.
    """
    if d1.names != d2.names or d1.shape != d2.shape:
        return False
    if d1.names is not None:
        for name in d1.names:
            if not _compatible_dtypes(d1.fields[name][0], d2.fields[name][0]):
                return False

    else:
        try:
            np.result_type(d1, d2)
        except TypeError:
            return False
        else:
            return True


class _Element(metaclass=abc.ABCMeta):
    __doc__ = '\n    Abstract class for an object holding information associated to a key in a\n    GP object.\n    '

    @property
    @abc.abstractmethod
    def shape(self):
        """Output shape"""
        pass

    @property
    def size(self):
        return np.prod(self.shape)


class _Points(_Element):
    __doc__ = 'Points where the process is evaluated'

    def __init__(self, x, deriv):
        assert _isarraylike(x)
        assert isinstance(deriv, _Deriv.Deriv)
        self.x = x
        self.deriv = deriv

    @property
    def shape(self):
        return self.x.shape


class _Transf(_Element):
    __doc__ = 'Trasformation over other _Element objects'

    def __init__(self, tensors, shape):
        assert isinstance(tensors, dict)
        assert isinstance(shape, tuple)
        self.tensors = tensors
        self._shape = shape

    @property
    def shape(self):
        return self._shape

    @classmethod
    def tensormul(cls, tensor, x):
        if tensor.shape:
            x = np.tensordot(tensor, x, axes=1)
        else:
            if tensor.item != 1:
                x = tensor * x
        return x


class GP:
    __doc__ = '\n    \n    Object that represents a gaussian process over arbitrary input.\n    \n    Methods\n    -------\n    addx :\n        Add points where the gaussian process is evaluated.\n    addtransf :\n        Add a linear transformation of the process.\n    prior :\n        Compute the prior for the process.\n    pred :\n        Compute the posterior for the process.\n    predfromfit, predfromdata :\n        Convenience wrappers for `pred`.\n    marginal_likelihood :\n        Compute the "marginal likelihood", also known as "bayes factor".\n    \n    '

    def __init__(self, covfun, solver='eigcut+', checkpos=True, checksym=True, checkfinite=True, **kw):
        """
        
        Parameters
        ----------
        covfun : Kernel
            An instance of `Kernel` representing the covariance kernel.
        solver : str
            A solver used to invert the covariance matrix. See list below for
            the available solvers. Default is `eigcut+` which is slow but
            robust.
        checkpos : bool
            If True (default), raise a `LinAlgError` if the prior covariance
            matrix turns out non positive within numerical error. The check
            will be done only if you use in some way the `gvar` prior. With
            the Cholesky solvers the check will be done in all cases.
        checksym : bool
            If True (default), check that the prior covariance matrix is
            symmetric. If False, only half of the matrix is computed.
        checkfinite : bool
            If True (default), check that the prior covariance matrix does not
            contain infs or nans.
        
        Solvers
        -------
        eigcut+ :
            Promote small eigenvalues to a minimum value (default). What
            `lsqfit` does by default.
        eigcut- :
            Remove small eigenvalues.
        lowrank :
            Reduce the rank of the matrix. The complexity is O(n^2 r) where
            `n` is the matrix size and `r` the required rank, while other
            algorithms are O(n^3). Slow for small sizes.
        gersh :
            Cholesky decomposition after regularizing the matrix with a
            Gershgorin estimate of the maximum eigenvalue. The fastest of the
            O(n^3) algorithms.
        maxeigv :
            Cholesky decomposition regularizing the matrix with the maximum
            eigenvalue. Slow for small sizes. Use only for large sizes and if
            gersh is giving inaccurate results.
        
        Keyword arguments
        -----------------
        eps : positive float
            For solvers `eigcut+`, `eigcut-`, `gersh` and `maxeigv`. Specifies
            the threshold for considering small the eigenvalues, relative to
            the maximum eigenvalue. The default is matrix size * float epsilon.
        rank : positive integer
            For the `lowrank` solver, the target rank. It should be much
            smaller than the matrix size for the method to be convenient.
        
        """
        if not isinstance(covfun, _Kernel.Kernel):
            raise TypeError('covariance function must be of class Kernel')
        self._covfun = covfun
        self._elements = dict()
        self._canaddx = True
        decomp = {'eigcut+':_linalg.EigCutFullRank, 
         'eigcut-':_linalg.EigCutLowRank, 
         'lowrank':_linalg.ReduceRank, 
         'gersh':_linalg.CholGersh, 
         'maxeigv':_linalg.CholMaxEig}[solver]
        self._decompclass = lambda K, **kwargs: decomp(K, **kwargs, **kw)
        self._checkpositive = bool(checkpos)
        self._checksym = bool(checksym)
        self._checkfinite = bool(checkfinite)

    def addx(self, x, key=None, deriv=0):
        """
        
        Add points where the gaussian process is evaluated. The GP object
        keeps the various x arrays in a dictionary. If `x` is an array, you
        have to specify its dictionary key with the `key` parameter. Otherwise,
        you can directly pass a dictionary for `x`.
        
        To specify that on the given `x` a derivative of the process instead of
        the process itself should be evaluated, use the parameter `deriv`.
        
        `addx` never copies the input arrays if they are numpy arrays, so if
        you change their contents before doing something with the GP, the
        change will be reflected on the result. However, after the GP has
        computed internally its covariance matrix, the x are ignored.
        
        If you use in some way the `gvar` prior, e.g. by calling `prior` or
        `pred` using `gvar`s, you can't call `addx` any more, due to a
        limitation in gvar.
        
        Parameters
        ----------
        x : array or dictionary of arrays
            The points to be added.
        key :
            If `x` is an array, the dictionary key under which `x` is added.
            Can not be specified if `x` is a dictionary.
        deriv :
            Derivative specification. A `Deriv` object or something that can
            be converted to `Deriv` (see Deriv's help).
        
        """
        if not self._canaddx:
            raise RuntimeError('can not add x any more to this process')
        deriv = _Deriv.Deriv(deriv)
        if _isarraylike(x):
            if key is None:
                raise ValueError('x is array but key is None')
            x = {key: x}
        else:
            if _isdictlike(x):
                if key is not None:
                    raise ValueError('can not specify key if x is a dictionary')
                elif None in x:
                    raise ValueError('None key in x not allowed')
                else:
                    raise TypeError('x must be array or dict')
            else:
                for key in x:
                    if key in self._elements:
                        raise RuntimeError('key {!r} already in GP'.format(key))
                    else:
                        gx = x[key]
                        if not _isarraylike(gx):
                            raise TypeError('x[{!r}] is not array or list'.format(key))
                        gx = _asarray(gx)
                        if not gx.size:
                            raise ValueError('x[{!r}] is empty'.format(key))
                        if hasattr(self, '_dtype'):
                            try:
                                self._dtype = np.result_type(self._dtype, gx.dtype)
                            except TypeError:
                                msg = 'x[{!r}].dtype = {!r} not compatible with {!r}'
                                msg = msg.format(key, gx.dtype, self._dtype)
                                raise TypeError(msg)

                        else:
                            self._dtype = gx.dtype
                    if gx.dtype.names is None:
                        if not deriv.implicit:
                            raise ValueError('x has not fields but derivative has')

            for dim in deriv:
                if dim not in gx.dtype.names:
                    raise ValueError('deriv field {!r} not in x'.format(dim))
                else:
                    self._elements[key] = _Points(gx, deriv)

    def addtransf(self, tensors, key):
        """
        
        Apply a linear transformation to already specified process points. The
        result of the transformation is represented by a new key.
        
        Parameters
        ----------
        tensors : dict
            Dictionary mapping keys of the GP to arrays/scalars. Each array is
            matrix-multiplied with the process array represented by its key,
            while scalars are just multiplied. Finally, the keys are summed
            over.
        key :
            A new key under which the transformation is placed.
        
        The multiplication between the tensors and the process is done with
        np.tensordot with 1-axis contraction. For >2d arrays this is different
        from numpy's matrix multiplication.
        
        """
        if key is None:
            raise ValueError('key can not be None')
        if key in self._elements:
            raise RuntimeError('key {!r} already in GP'.format(key))
        for k in tensors:
            if k not in self._elements:
                raise KeyError(k)

        for k, t in tensors.items():
            t = np.array(t, copy=False)
            if not np.issubdtype(t.dtype, np.number):
                msg = 'tensors[{!r}] has non-numeric dtype {!r}'
                raise TypeError(msg.format(k, t.dtype))
            if self._checkfinite:
                if not np.all(np.isfinite(t)):
                    raise ValueError('tensors[{!r}] contains infs/nans'.format(k))
            rshape = self._elements[k].shape
            if t.shape:
                if t.shape[(-1)] != rshape[0]:
                    msg = 'tensors[{!r}].shape = {!r} can not be multiplied with shape {!r}'
                    raise ValueError(msg.format(k, t.shape, rshape))
            tensors[k] = t
        else:
            arrays = tensors.values()
            elements = (self._elements[k] for k in tensors)
            shapes = [t.shape[:-1] + e.shape[1:] if t.shape else e.shape for t, e in zip(arrays, elements)]
            try:
                shape = _array.broadcast_shapes(shapes)
            except ValueError:
                msg = 'can not broadcast tensors with shapes ['
                msg += ', '.join((repr(t.shape) for t in arrays))
                msg += '] contracted with arrays with shapes ['
                msg += ', '.join((repr(e.shape) for e in elements)) + ']'
                raise ValueError(msg)
            else:
                self._elements[key] = _Transf(tensors, shape)

    def _makecovblock_points(self, xkey, ykey):
        x = self._elements[xkey]
        y = self._elements[ykey]
        assert isinstance(x, _Points)
        assert isinstance(y, _Points)
        kernel = self._covfun.diff(x.deriv, y.deriv)
        if x is y:
            indices, back = self._checksym or _triu_indices_and_back(x.size)
            x = x.x.reshape(-1)[indices]
            y = y.x.reshape(-1)[indices]
            halfcov = kernel(x, y)
            cov = halfcov[back]
        else:
            x = x.x.reshape(-1)[:, None]
            y = y.x.reshape(-1)[None, :]
            cov = kernel(x, y)
        return cov

    def _makecovblock_transf_any(self, xkey, ykey):
        x = self._elements[xkey]
        y = self._elements[ykey]
        assert isinstance(x, _Transf)
        covsum = None
        for key, tensor in x.tensors.items():
            elem = self._elements[key]
            cov = self._covblock(key, ykey)
            assert cov.shape == (elem.size, y.size)
            cov = cov.reshape(elem.shape + y.shape)
            cov = type(x).tensormul(tensor, cov)
            if covsum is not None:
                covsum = covsum + cov
            else:
                covsum = cov
        else:
            assert covsum.shape == x.shape + y.shape
            return covsum.reshape(x.size, y.size)

    def _makecovblock(self, xkey, ykey):
        x = self._elements[xkey]
        y = self._elements[ykey]
        if isinstance(x, _Points) and isinstance(y, _Points):
            cov = self._makecovblock_points(xkey, ykey)
        else:
            if isinstance(x, _Transf):
                cov = self._makecovblock_transf_any(xkey, ykey)
            else:
                if isinstance(y, _Transf):
                    cov = self._makecovblock_transf_any(ykey, xkey)
                    cov = cov.T
                elif self._checkfinite and not np.all(np.isfinite(cov)):
                    raise RuntimeError('covariance block {!r} is not finite'.format((xkey, ykey)))
                if self._checksym:
                    if xkey == ykey:
                        if not np.allclose(cov, cov.T):
                            raise RuntimeError('covariance block {!r} is not symmetric'.format((xkey, ykey)))
                return cov

    def _covblock(self, row, col):
        if not hasattr(self, '_covblocks'):
            self._covblocks = dict()
        if (row, col) not in self._covblocks:
            block = self._makecovblock(row, col)
            _linalg.noautograd(block).flags['WRITEABLE'] = False
            if row != col:
                if self._checksym:
                    blockT = self._makecovblock(col, row)
                    if not np.allclose(block.T, blockT):
                        msg = 'covariance block {!r} is not symmetric'
                        raise RuntimeError(msg.format((row, col)))
                self._covblocks[(col, row)] = block.T
            self._covblocks[(row, col)] = block
        return self._covblocks[(row, col)]

    def _assemblecovblocks(self, rowkeys, colkeys=None):
        if colkeys is None:
            colkeys = rowkeys
        blocks = [[self._covblock(row, col) for col in colkeys] for row in rowkeys]
        return _block_matrix(blocks)

    def _solver(self, keys, ycov=0):
        """
        Return a decomposition of the covariance matrix of the keys in `keys`
        plus the matrix ycov.
        """
        Kxx = self._assemblecovblocks(keys)
        return self._decompclass(Kxx + ycov)

    def _checkpos(self, cov):
        eigv = linalg.eigvalsh(_linalg.noautograd(cov))
        mineigv = np.min(eigv)
        if mineigv < 0:
            bound = -len(cov) * np.finfo(float).eps * np.max(eigv)
            if mineigv < bound:
                msg = 'covariance matrix is not positive definite: '
                msg += 'mineigv = {:.4g} < {:.4g}'.format(mineigv, bound)
                raise np.linalg.LinAlgError(msg)

    def _priorpoints--- This code section failed: ---

 L. 513         0  LOAD_GLOBAL              hasattr
                2  LOAD_DEREF               'self'
                4  LOAD_STR                 '_priordict'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE    148  'to 148'

 L. 514        10  LOAD_DEREF               'self'
               12  LOAD_ATTR                _checkpositive
               14  POP_JUMP_IF_FALSE    60  'to 60'

 L. 515        16  LOAD_LISTCOMP            '<code_object <listcomp>>'
               18  LOAD_STR                 'GP._priorpoints.<locals>.<listcomp>'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 516        22  LOAD_DEREF               'self'
               24  LOAD_ATTR                _elements
               26  LOAD_METHOD              items
               28  CALL_METHOD_0         0  ''

 L. 515        30  GET_ITER         
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'keys'

 L. 519        36  LOAD_DEREF               'self'
               38  LOAD_METHOD              _assemblecovblocks
               40  LOAD_GLOBAL              list
               42  LOAD_FAST                'keys'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'fullcov'

 L. 520        50  LOAD_DEREF               'self'
               52  LOAD_METHOD              _checkpos
               54  LOAD_FAST                'fullcov'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
             60_0  COME_FROM            14  '14'

 L. 521        60  LOAD_LISTCOMP            '<code_object <listcomp>>'
               62  LOAD_STR                 'GP._priorpoints.<locals>.<listcomp>'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 522        66  LOAD_DEREF               'self'
               68  LOAD_ATTR                _elements
               70  LOAD_METHOD              items
               72  CALL_METHOD_0         0  ''

 L. 521        74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  STORE_DEREF              'items'

 L. 525        80  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               82  LOAD_STR                 'GP._priorpoints.<locals>.<dictcomp>'
               84  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 527        86  LOAD_DEREF               'items'

 L. 525        88  GET_ITER         
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'mean'

 L. 529        94  LOAD_CLOSURE             'items'
               96  LOAD_CLOSURE             'self'
               98  BUILD_TUPLE_2         2 
              100  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              102  LOAD_STR                 'GP._priorpoints.<locals>.<dictcomp>'
              104  MAKE_FUNCTION_8          'closure'

 L. 531       106  LOAD_DEREF               'items'

 L. 529       108  GET_ITER         
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'cov'

 L. 534       114  LOAD_GLOBAL              gvar
              116  LOAD_METHOD              gvar
              118  LOAD_FAST                'mean'
              120  LOAD_FAST                'cov'
              122  CALL_METHOD_2         2  ''
              124  LOAD_DEREF               'self'
              126  STORE_ATTR               _priordict

 L. 535       128  LOAD_CONST               False
              130  LOAD_DEREF               'self'
              132  LOAD_ATTR                _priordict
              134  LOAD_ATTR                buf
              136  LOAD_ATTR                flags
              138  LOAD_STR                 'WRITEABLE'
              140  STORE_SUBSCR     

 L. 536       142  LOAD_CONST               False
              144  LOAD_DEREF               'self'
              146  STORE_ATTR               _canaddx
            148_0  COME_FROM             8  '8'

 L. 537       148  LOAD_DEREF               'self'
              150  LOAD_ATTR                _priordict
              152  LOAD_FAST                'key'
              154  BINARY_SUBSCR    
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 100

    def _priortransf(self, key):
        x = self._elements[key]
        assert isinstance(x, _Transf)
        out = None
        for k, tensor in x.tensors.items():
            prior = self._prior(k)
            transf = type(x).tensormul(tensor, prior)
            if out is None:
                out = transf
            else:
                out = out + transf
        else:
            return out

    def _prior(self, key):
        prior = getattr(self, '_priordict', {}).get(key, None)
        if prior is None:
            x = self._elements[key]
            if isinstance(x, _Points):
                prior = self._priorpoints(key)
            else:
                if isinstance(x, _Transf):
                    prior = self._priortransf(key)
                    self._priordict[key] = prior
        return prior

    def prior--- This code section failed: ---

 L. 597         0  LOAD_GLOBAL              bool
                2  LOAD_FAST                'raw'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'raw'

 L. 599         8  LOAD_FAST                'key'
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_FALSE    28  'to 28'

 L. 600        16  LOAD_GLOBAL              list
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                _elements
               22  CALL_FUNCTION_1       1  ''
               24  STORE_DEREF              'outkeys'
               26  JUMP_FORWARD         48  'to 48'
             28_0  COME_FROM            14  '14'

 L. 601        28  LOAD_GLOBAL              isinstance
               30  LOAD_FAST                'key'
               32  LOAD_GLOBAL              list
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 602        38  LOAD_FAST                'key'
               40  STORE_DEREF              'outkeys'
               42  JUMP_FORWARD         48  'to 48'
             44_0  COME_FROM            36  '36'

 L. 604        44  LOAD_CONST               None
               46  STORE_DEREF              'outkeys'
             48_0  COME_FROM            42  '42'
             48_1  COME_FROM            26  '26'

 L. 606        48  LOAD_FAST                'raw'
               50  POP_JUMP_IF_FALSE    80  'to 80'
               52  LOAD_DEREF               'outkeys'
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    80  'to 80'

 L. 607        60  LOAD_CLOSURE             'outkeys'
               62  LOAD_CLOSURE             'self'
               64  BUILD_TUPLE_2         2 
               66  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               68  LOAD_STR                 'GP.prior.<locals>.<dictcomp>'
               70  MAKE_FUNCTION_8          'closure'

 L. 610        72  LOAD_DEREF               'outkeys'

 L. 607        74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  RETURN_VALUE     
             80_0  COME_FROM            58  '58'
             80_1  COME_FROM            50  '50'

 L. 613        80  LOAD_FAST                'raw'
               82  POP_JUMP_IF_FALSE    96  'to 96'

 L. 614        84  LOAD_DEREF               'self'
               86  LOAD_METHOD              _covblock
               88  LOAD_FAST                'key'
               90  LOAD_FAST                'key'
               92  CALL_METHOD_2         2  ''
               94  RETURN_VALUE     
             96_0  COME_FROM            82  '82'

 L. 615        96  LOAD_DEREF               'outkeys'
               98  LOAD_CONST               None
              100  COMPARE_OP               is-not
              102  POP_JUMP_IF_FALSE   128  'to 128'

 L. 616       104  LOAD_GLOBAL              gvar
              106  LOAD_METHOD              BufferDict
              108  LOAD_CLOSURE             'self'
              110  BUILD_TUPLE_1         1 
              112  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              114  LOAD_STR                 'GP.prior.<locals>.<dictcomp>'
              116  MAKE_FUNCTION_8          'closure'

 L. 617       118  LOAD_DEREF               'outkeys'

 L. 616       120  GET_ITER         
              122  CALL_FUNCTION_1       1  ''
              124  CALL_METHOD_1         1  ''
              126  RETURN_VALUE     
            128_0  COME_FROM           102  '102'

 L. 620       128  LOAD_DEREF               'self'
              130  LOAD_METHOD              _prior
              132  LOAD_FAST                'key'
              134  CALL_METHOD_1         1  ''
              136  RETURN_VALUE     

Parse error at or near `LOAD_DICTCOMP' instruction at offset 66

    def _flatgiven--- This code section failed: ---

 L. 624         0  LOAD_GLOBAL              _isarraylike_nostructured
                2  LOAD_DEREF               'given'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_FALSE   108  'to 108'

 L. 625         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _elements
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               1
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    98  'to 98'

 L. 626        22  LOAD_CLOSURE             'given'
               24  BUILD_TUPLE_1         1 
               26  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               28  LOAD_STR                 'GP._flatgiven.<locals>.<dictcomp>'
               30  MAKE_FUNCTION_8          'closure'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _elements
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  STORE_DEREF              'given'

 L. 627        42  LOAD_GLOBAL              len
               44  LOAD_DEREF               'given'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_CONST               1
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_TRUE     58  'to 58'
               54  LOAD_ASSERT              AssertionError
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            52  '52'

 L. 628        58  LOAD_DEREF               'givencov'
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not
               64  POP_JUMP_IF_FALSE   106  'to 106'

 L. 629        66  LOAD_GLOBAL              _isarraylike_nostructured
               68  LOAD_DEREF               'givencov'
               70  CALL_FUNCTION_1       1  ''
               72  POP_JUMP_IF_TRUE     78  'to 78'
               74  LOAD_ASSERT              AssertionError
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            72  '72'

 L. 630        78  LOAD_CLOSURE             'givencov'
               80  BUILD_TUPLE_1         1 
               82  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               84  LOAD_STR                 'GP._flatgiven.<locals>.<dictcomp>'
               86  MAKE_FUNCTION_8          'closure'
               88  LOAD_DEREF               'given'
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  STORE_DEREF              'givencov'
               96  JUMP_ABSOLUTE       146  'to 146'
             98_0  COME_FROM            20  '20'

 L. 632        98  LOAD_GLOBAL              ValueError
              100  LOAD_STR                 '`given` is an array but GP has multiple keys, provide a dictionary'
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            64  '64'
              106  JUMP_FORWARD        146  'to 146'
            108_0  COME_FROM             6  '6'

 L. 634       108  LOAD_GLOBAL              _isdictlike
              110  LOAD_DEREF               'given'
              112  CALL_FUNCTION_1       1  ''
              114  POP_JUMP_IF_FALSE   138  'to 138'

 L. 635       116  LOAD_DEREF               'givencov'
              118  LOAD_CONST               None
              120  COMPARE_OP               is-not
              122  POP_JUMP_IF_FALSE   146  'to 146'

 L. 636       124  LOAD_GLOBAL              _isdictlike
              126  LOAD_DEREF               'givencov'
              128  CALL_FUNCTION_1       1  ''
              130  POP_JUMP_IF_TRUE    146  'to 146'
              132  LOAD_ASSERT              AssertionError
              134  RAISE_VARARGS_1       1  'exception instance'
              136  JUMP_FORWARD        146  'to 146'
            138_0  COME_FROM           114  '114'

 L. 639       138  LOAD_GLOBAL              TypeError
              140  LOAD_STR                 '`given` must be array or dict'
              142  CALL_FUNCTION_1       1  ''
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           136  '136'
            146_1  COME_FROM           130  '130'
            146_2  COME_FROM           122  '122'
            146_3  COME_FROM           106  '106'

 L. 641       146  BUILD_LIST_0          0 
              148  STORE_DEREF              'ylist'

 L. 642       150  BUILD_LIST_0          0 
              152  STORE_DEREF              'keylist'

 L. 643       154  LOAD_DEREF               'given'
              156  LOAD_METHOD              items
              158  CALL_METHOD_0         0  ''
              160  GET_ITER         
              162  FOR_ITER            328  'to 328'
              164  UNPACK_SEQUENCE_2     2 
              166  STORE_FAST               'key'
              168  STORE_FAST               'l'

 L. 644       170  LOAD_FAST                'key'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                _elements
              176  COMPARE_OP               not-in
              178  POP_JUMP_IF_FALSE   188  'to 188'

 L. 645       180  LOAD_GLOBAL              KeyError
              182  LOAD_FAST                'key'
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           178  '178'

 L. 647       188  LOAD_GLOBAL              np
              190  LOAD_ATTR                array
              192  LOAD_FAST                'l'
              194  LOAD_CONST               False
              196  LOAD_CONST               ('copy',)
              198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              200  STORE_FAST               'l'

 L. 648       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _elements
              206  LOAD_FAST                'key'
              208  BINARY_SUBSCR    
              210  LOAD_ATTR                shape
              212  STORE_FAST               'shape'

 L. 649       214  LOAD_FAST                'l'
              216  LOAD_ATTR                shape
              218  LOAD_FAST                'shape'
              220  COMPARE_OP               !=
              222  POP_JUMP_IF_FALSE   248  'to 248'

 L. 650       224  LOAD_STR                 'given[{!r}] has shape {!r} different from shape {!r}'
              226  STORE_FAST               'msg'

 L. 651       228  LOAD_GLOBAL              ValueError
              230  LOAD_FAST                'msg'
              232  LOAD_METHOD              format
              234  LOAD_FAST                'key'
              236  LOAD_FAST                'l'
              238  LOAD_ATTR                shape
              240  LOAD_FAST                'shape'
              242  CALL_METHOD_3         3  ''
              244  CALL_FUNCTION_1       1  ''
              246  RAISE_VARARGS_1       1  'exception instance'
            248_0  COME_FROM           222  '222'

 L. 652       248  LOAD_FAST                'l'
              250  LOAD_ATTR                dtype
              252  LOAD_GLOBAL              object
              254  COMPARE_OP               !=
          256_258  POP_JUMP_IF_FALSE   300  'to 300'
              260  LOAD_GLOBAL              np
              262  LOAD_METHOD              issubdtype
              264  LOAD_FAST                'l'
              266  LOAD_ATTR                dtype
              268  LOAD_GLOBAL              np
              270  LOAD_ATTR                number
              272  CALL_METHOD_2         2  ''
          274_276  POP_JUMP_IF_TRUE    300  'to 300'

 L. 653       278  LOAD_STR                 'given[{!r}] has non-numerical dtype {!r}'
              280  STORE_FAST               'msg'

 L. 654       282  LOAD_GLOBAL              ValueError
              284  LOAD_FAST                'msg'
              286  LOAD_METHOD              format
              288  LOAD_FAST                'key'
              290  LOAD_FAST                'l'
              292  LOAD_ATTR                dtype
              294  CALL_METHOD_2         2  ''
              296  CALL_FUNCTION_1       1  ''
              298  RAISE_VARARGS_1       1  'exception instance'
            300_0  COME_FROM           274  '274'
            300_1  COME_FROM           256  '256'

 L. 656       300  LOAD_DEREF               'ylist'
              302  LOAD_METHOD              append
              304  LOAD_FAST                'l'
              306  LOAD_METHOD              reshape
              308  LOAD_CONST               -1
              310  CALL_METHOD_1         1  ''
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          

 L. 657       316  LOAD_DEREF               'keylist'
              318  LOAD_METHOD              append
              320  LOAD_FAST                'key'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          
              326  JUMP_BACK           162  'to 162'

 L. 659       328  LOAD_DEREF               'givencov'
              330  LOAD_CONST               None
              332  COMPARE_OP               is-not
          334_336  POP_JUMP_IF_FALSE   370  'to 370'

 L. 660       338  LOAD_CLOSURE             'givencov'
              340  LOAD_CLOSURE             'keylist'
              342  LOAD_CLOSURE             'ylist'
              344  BUILD_TUPLE_3         3 
              346  LOAD_LISTCOMP            '<code_object <listcomp>>'
              348  LOAD_STR                 'GP._flatgiven.<locals>.<listcomp>'
              350  MAKE_FUNCTION_8          'closure'

 L. 665       352  LOAD_GLOBAL              range
              354  LOAD_GLOBAL              len
              356  LOAD_DEREF               'keylist'
              358  CALL_FUNCTION_1       1  ''
              360  CALL_FUNCTION_1       1  ''

 L. 660       362  GET_ITER         
              364  CALL_FUNCTION_1       1  ''
              366  STORE_FAST               'covblocks'
              368  JUMP_FORWARD        374  'to 374'
            370_0  COME_FROM           334  '334'

 L. 668       370  LOAD_CONST               None
              372  STORE_FAST               'covblocks'
            374_0  COME_FROM           368  '368'

 L. 670       374  LOAD_DEREF               'ylist'
              376  LOAD_DEREF               'keylist'
              378  LOAD_FAST                'covblocks'
              380  BUILD_TUPLE_3         3 
              382  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 26

    def _slices(self, keylist):
        """
        Return list of slices for the positions of flattened arrays
        corresponding to keys in `keylist` into their concatenation.
        """
        sizes = [self._elements[key].size for key in keylist]
        stops = np.concatenate([[0], np.cumsum(sizes)])
        return [slice(stops[(i - 1)], stops[i]) for i in range(1, len(stops))]

    def pred--- This code section failed: ---

 L. 742         0  LOAD_FAST                'fromdata'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 743         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'you must specify if `given` is data or fit result'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 744        16  LOAD_GLOBAL              bool
               18  LOAD_FAST                'fromdata'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'fromdata'

 L. 745        24  LOAD_GLOBAL              bool
               26  LOAD_FAST                'raw'
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'raw'

 L. 746        32  LOAD_FAST                'keepcorr'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 747        40  LOAD_FAST                'raw'
               42  UNARY_NOT        
               44  STORE_FAST               'keepcorr'
             46_0  COME_FROM            38  '38'

 L. 748        46  LOAD_FAST                'keepcorr'
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  LOAD_FAST                'raw'
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 749        54  LOAD_GLOBAL              ValueError
               56  LOAD_STR                 'both keepcorr=True and raw=True'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            48  '48'

 L. 751        62  LOAD_CONST               False
               64  STORE_FAST               'strip'

 L. 752        66  LOAD_FAST                'key'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 753        74  LOAD_GLOBAL              list
               76  LOAD_DEREF               'self'
               78  LOAD_ATTR                _elements
               80  CALL_FUNCTION_1       1  ''
               82  STORE_DEREF              'outkeys'
               84  JUMP_FORWARD        112  'to 112'
             86_0  COME_FROM            72  '72'

 L. 754        86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'key'
               90  LOAD_GLOBAL              list
               92  CALL_FUNCTION_2       2  ''
               94  POP_JUMP_IF_FALSE   102  'to 102'

 L. 755        96  LOAD_FAST                'key'
               98  STORE_DEREF              'outkeys'
              100  JUMP_FORWARD        112  'to 112'
            102_0  COME_FROM            94  '94'

 L. 757       102  LOAD_FAST                'key'
              104  BUILD_LIST_1          1 
              106  STORE_DEREF              'outkeys'

 L. 758       108  LOAD_CONST               True
              110  STORE_FAST               'strip'
            112_0  COME_FROM           100  '100'
            112_1  COME_FROM            84  '84'

 L. 759       112  LOAD_DEREF               'self'
              114  LOAD_METHOD              _slices
              116  LOAD_DEREF               'outkeys'
              118  CALL_METHOD_1         1  ''
              120  STORE_DEREF              'outslices'

 L. 761       122  LOAD_DEREF               'self'
              124  LOAD_METHOD              _flatgiven
              126  LOAD_FAST                'given'
              128  LOAD_FAST                'givencov'
              130  CALL_METHOD_2         2  ''
              132  UNPACK_SEQUENCE_3     3 
              134  STORE_FAST               'ylist'
              136  STORE_FAST               'inkeys'
              138  STORE_FAST               'ycovblocks'

 L. 762       140  LOAD_GLOBAL              _concatenate_noop
              142  LOAD_FAST                'ylist'
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'y'

 L. 766       148  LOAD_DEREF               'self'
              150  LOAD_METHOD              _assemblecovblocks
              152  LOAD_FAST                'inkeys'
              154  LOAD_DEREF               'outkeys'
              156  CALL_METHOD_2         2  ''
              158  STORE_FAST               'Kxxs'

 L. 767       160  LOAD_FAST                'Kxxs'
              162  LOAD_ATTR                T
              164  STORE_FAST               'Kxsx'

 L. 769       166  LOAD_FAST                'ycovblocks'
              168  LOAD_CONST               None
              170  COMPARE_OP               is-not
              172  POP_JUMP_IF_FALSE   184  'to 184'

 L. 770       174  LOAD_GLOBAL              _block_matrix
              176  LOAD_FAST                'ycovblocks'
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'ycov'
              182  JUMP_FORWARD        258  'to 258'
            184_0  COME_FROM           172  '172'

 L. 771       184  LOAD_FAST                'fromdata'
              186  POP_JUMP_IF_TRUE    196  'to 196'
              188  LOAD_FAST                'raw'
              190  POP_JUMP_IF_TRUE    196  'to 196'
              192  LOAD_FAST                'keepcorr'
              194  POP_JUMP_IF_TRUE    254  'to 254'
            196_0  COME_FROM           190  '190'
            196_1  COME_FROM           186  '186'
              196  LOAD_FAST                'y'
              198  LOAD_ATTR                dtype
              200  LOAD_GLOBAL              object
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   254  'to 254'

 L. 772       206  LOAD_GLOBAL              gvar
              208  LOAD_METHOD              evalcov
              210  LOAD_GLOBAL              gvar
              212  LOAD_METHOD              gvar
              214  LOAD_FAST                'y'
              216  CALL_METHOD_1         1  ''
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               'ycov'

 L. 774       222  LOAD_DEREF               'self'
              224  LOAD_ATTR                _checkfinite
              226  POP_JUMP_IF_FALSE   252  'to 252'
              228  LOAD_GLOBAL              np
              230  LOAD_METHOD              all
              232  LOAD_GLOBAL              np
              234  LOAD_METHOD              isfinite
              236  LOAD_FAST                'ycov'
              238  CALL_METHOD_1         1  ''
              240  CALL_METHOD_1         1  ''
              242  POP_JUMP_IF_TRUE    252  'to 252'

 L. 775       244  LOAD_GLOBAL              ValueError
              246  LOAD_STR                 'covariance matrix of `given` is not finite'
              248  CALL_FUNCTION_1       1  ''
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           242  '242'
            252_1  COME_FROM           226  '226'
              252  JUMP_FORWARD        258  'to 258'
            254_0  COME_FROM           204  '204'
            254_1  COME_FROM           194  '194'

 L. 777       254  LOAD_CONST               0
              256  STORE_FAST               'ycov'
            258_0  COME_FROM           252  '252'
            258_1  COME_FROM           182  '182'

 L. 779       258  LOAD_FAST                'raw'
          260_262  POP_JUMP_IF_TRUE    270  'to 270'
              264  LOAD_FAST                'keepcorr'
          266_268  POP_JUMP_IF_TRUE    542  'to 542'
            270_0  COME_FROM           260  '260'

 L. 781       270  LOAD_DEREF               'self'
              272  LOAD_METHOD              _assemblecovblocks
              274  LOAD_DEREF               'outkeys'
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'Kxsxs'

 L. 783       280  LOAD_GLOBAL              gvar
              282  LOAD_METHOD              mean
              284  LOAD_FAST                'y'
              286  CALL_METHOD_1         1  ''
              288  STORE_FAST               'ymean'

 L. 784       290  LOAD_DEREF               'self'
              292  LOAD_ATTR                _checkfinite
          294_296  POP_JUMP_IF_FALSE   324  'to 324'
              298  LOAD_GLOBAL              np
              300  LOAD_METHOD              all
              302  LOAD_GLOBAL              np
              304  LOAD_METHOD              isfinite
              306  LOAD_FAST                'ymean'
              308  CALL_METHOD_1         1  ''
              310  CALL_METHOD_1         1  ''
          312_314  POP_JUMP_IF_TRUE    324  'to 324'

 L. 785       316  LOAD_GLOBAL              ValueError
              318  LOAD_STR                 'mean of `given` is not finite'
              320  CALL_FUNCTION_1       1  ''
              322  RAISE_VARARGS_1       1  'exception instance'
            324_0  COME_FROM           312  '312'
            324_1  COME_FROM           294  '294'

 L. 787       324  LOAD_FAST                'fromdata'
          326_328  POP_JUMP_IF_FALSE   374  'to 374'

 L. 788       330  LOAD_DEREF               'self'
              332  LOAD_METHOD              _solver
              334  LOAD_FAST                'inkeys'
              336  LOAD_FAST                'ycov'
              338  CALL_METHOD_2         2  ''
              340  STORE_FAST               'solver'

 L. 789       342  LOAD_FAST                'Kxsxs'
              344  LOAD_FAST                'solver'
              346  LOAD_METHOD              quad
              348  LOAD_FAST                'Kxxs'
              350  CALL_METHOD_1         1  ''
              352  BINARY_SUBTRACT  
              354  STORE_DEREF              'cov'

 L. 790       356  LOAD_FAST                'solver'
              358  LOAD_METHOD              solve
              360  LOAD_FAST                'Kxxs'
              362  CALL_METHOD_1         1  ''
              364  LOAD_ATTR                T
              366  LOAD_FAST                'ymean'
              368  BINARY_MATRIX_MULTIPLY
              370  STORE_DEREF              'mean'
              372  JUMP_FORWARD        540  'to 540'
            374_0  COME_FROM           326  '326'

 L. 792       374  LOAD_DEREF               'self'
              376  LOAD_METHOD              _solver
              378  LOAD_FAST                'inkeys'
              380  CALL_METHOD_1         1  ''
              382  STORE_FAST               'solver'

 L. 793       384  LOAD_FAST                'solver'
              386  LOAD_METHOD              solve
              388  LOAD_FAST                'Kxxs'
              390  CALL_METHOD_1         1  ''
              392  LOAD_ATTR                T
              394  STORE_FAST               'A'

 L. 794       396  LOAD_GLOBAL              np
              398  LOAD_METHOD              isscalar
              400  LOAD_FAST                'ycov'
              402  CALL_METHOD_1         1  ''
          404_406  POP_JUMP_IF_FALSE   434  'to 434'
              408  LOAD_FAST                'ycov'
              410  LOAD_CONST               0
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   434  'to 434'

 L. 795       418  LOAD_FAST                'Kxsxs'
              420  LOAD_FAST                'solver'
              422  LOAD_METHOD              quad
              424  LOAD_FAST                'Kxxs'
              426  CALL_METHOD_1         1  ''
              428  BINARY_SUBTRACT  
              430  STORE_DEREF              'cov'
              432  JUMP_FORWARD        532  'to 532'
            434_0  COME_FROM           414  '414'
            434_1  COME_FROM           404  '404'

 L. 796       434  LOAD_GLOBAL              np
              436  LOAD_METHOD              isscalar
              438  LOAD_FAST                'ycov'
              440  CALL_METHOD_1         1  ''
          442_444  POP_JUMP_IF_TRUE    462  'to 462'
              446  LOAD_GLOBAL              len
              448  LOAD_FAST                'ycov'
              450  LOAD_ATTR                shape
              452  CALL_FUNCTION_1       1  ''
              454  LOAD_CONST               1
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_FALSE   504  'to 504'
            462_0  COME_FROM           442  '442'

 L. 797       462  LOAD_GLOBAL              np
              464  LOAD_METHOD              reshape
              466  LOAD_FAST                'ycov'
              468  LOAD_CONST               (1, -1)
              470  CALL_METHOD_2         2  ''
              472  STORE_FAST               'ycov_mat'

 L. 798       474  LOAD_FAST                'Kxsxs'
              476  LOAD_FAST                'A'
              478  LOAD_FAST                'ycov_mat'
              480  BINARY_MULTIPLY  
              482  LOAD_FAST                'A'
              484  LOAD_ATTR                T
              486  BINARY_MATRIX_MULTIPLY
              488  BINARY_ADD       
              490  LOAD_FAST                'solver'
              492  LOAD_METHOD              quad
              494  LOAD_FAST                'Kxxs'
              496  CALL_METHOD_1         1  ''
              498  BINARY_SUBTRACT  
              500  STORE_DEREF              'cov'
              502  JUMP_FORWARD        532  'to 532'
            504_0  COME_FROM           458  '458'

 L. 800       504  LOAD_FAST                'Kxsxs'
              506  LOAD_FAST                'A'
              508  LOAD_FAST                'ycov'
              510  BINARY_MATRIX_MULTIPLY
              512  LOAD_FAST                'A'
              514  LOAD_ATTR                T
              516  BINARY_MATRIX_MULTIPLY
              518  BINARY_ADD       
              520  LOAD_FAST                'solver'
              522  LOAD_METHOD              quad
              524  LOAD_FAST                'Kxxs'
              526  CALL_METHOD_1         1  ''
              528  BINARY_SUBTRACT  
              530  STORE_DEREF              'cov'
            532_0  COME_FROM           502  '502'
            532_1  COME_FROM           432  '432'

 L. 803       532  LOAD_FAST                'A'
              534  LOAD_FAST                'ymean'
              536  BINARY_MATRIX_MULTIPLY
              538  STORE_DEREF              'mean'
            540_0  COME_FROM           372  '372'
              540  JUMP_FORWARD        638  'to 638'
            542_0  COME_FROM           266  '266'

 L. 806       542  LOAD_CLOSURE             'self'
              544  BUILD_TUPLE_1         1 
              546  LOAD_LISTCOMP            '<code_object <listcomp>>'
              548  LOAD_STR                 'GP.pred.<locals>.<listcomp>'
              550  MAKE_FUNCTION_8          'closure'
              552  LOAD_FAST                'inkeys'
              554  GET_ITER         
              556  CALL_FUNCTION_1       1  ''
              558  STORE_FAST               'yplist'

 L. 807       560  LOAD_CLOSURE             'self'
              562  BUILD_TUPLE_1         1 
              564  LOAD_LISTCOMP            '<code_object <listcomp>>'
              566  LOAD_STR                 'GP.pred.<locals>.<listcomp>'
              568  MAKE_FUNCTION_8          'closure'
              570  LOAD_DEREF               'outkeys'
              572  GET_ITER         
              574  CALL_FUNCTION_1       1  ''
              576  STORE_FAST               'ysplist'

 L. 808       578  LOAD_GLOBAL              _concatenate_noop
              580  LOAD_FAST                'yplist'
              582  CALL_FUNCTION_1       1  ''
              584  STORE_FAST               'yp'

 L. 809       586  LOAD_GLOBAL              _concatenate_noop
              588  LOAD_FAST                'ysplist'
              590  CALL_FUNCTION_1       1  ''
              592  STORE_FAST               'ysp'

 L. 811       594  LOAD_FAST                'fromdata'
          596_598  POP_JUMP_IF_FALSE   604  'to 604'
              600  LOAD_FAST                'ycov'
              602  JUMP_FORWARD        606  'to 606'
            604_0  COME_FROM           596  '596'
              604  LOAD_CONST               0
            606_0  COME_FROM           602  '602'
              606  STORE_FAST               'mat'

 L. 812       608  LOAD_FAST                'Kxsx'
              610  LOAD_DEREF               'self'
              612  LOAD_METHOD              _solver
              614  LOAD_FAST                'inkeys'
              616  LOAD_FAST                'mat'
              618  CALL_METHOD_2         2  ''
              620  LOAD_METHOD              usolve
              622  LOAD_FAST                'y'
              624  LOAD_FAST                'yp'
              626  BINARY_SUBTRACT  
              628  CALL_METHOD_1         1  ''
              630  BINARY_MATRIX_MULTIPLY
              632  LOAD_FAST                'ysp'
              634  BINARY_ADD       
              636  STORE_DEREF              'flatout'
            638_0  COME_FROM           540  '540'

 L. 814       638  LOAD_FAST                'raw'
          640_642  POP_JUMP_IF_FALSE   714  'to 714'
              644  LOAD_FAST                'strip'
          646_648  POP_JUMP_IF_TRUE    714  'to 714'

 L. 815       650  LOAD_CLOSURE             'mean'
              652  LOAD_CLOSURE             'self'
              654  BUILD_TUPLE_2         2 
              656  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              658  LOAD_STR                 'GP.pred.<locals>.<dictcomp>'
              660  MAKE_FUNCTION_8          'closure'

 L. 817       662  LOAD_GLOBAL              zip
              664  LOAD_DEREF               'outkeys'
              666  LOAD_DEREF               'outslices'
              668  CALL_FUNCTION_2       2  ''

 L. 815       670  GET_ITER         
              672  CALL_FUNCTION_1       1  ''
              674  STORE_FAST               'meandict'

 L. 820       676  LOAD_CLOSURE             'cov'
              678  LOAD_CLOSURE             'outkeys'
              680  LOAD_CLOSURE             'outslices'
              682  LOAD_CLOSURE             'self'
              684  BUILD_TUPLE_4         4 
              686  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              688  LOAD_STR                 'GP.pred.<locals>.<dictcomp>'
              690  MAKE_FUNCTION_8          'closure'

 L. 823       692  LOAD_GLOBAL              zip
              694  LOAD_DEREF               'outkeys'
              696  LOAD_DEREF               'outslices'
              698  CALL_FUNCTION_2       2  ''

 L. 820       700  GET_ITER         
              702  CALL_FUNCTION_1       1  ''
              704  STORE_FAST               'covdict'

 L. 827       706  LOAD_FAST                'meandict'
              708  LOAD_FAST                'covdict'
              710  BUILD_TUPLE_2         2 
              712  RETURN_VALUE     
            714_0  COME_FROM           646  '646'
            714_1  COME_FROM           640  '640'

 L. 829       714  LOAD_FAST                'raw'
          716_718  POP_JUMP_IF_FALSE   794  'to 794'

 L. 830       720  LOAD_GLOBAL              len
              722  LOAD_DEREF               'outkeys'
              724  CALL_FUNCTION_1       1  ''
              726  LOAD_CONST               1
              728  COMPARE_OP               ==
          730_732  POP_JUMP_IF_TRUE    738  'to 738'
              734  LOAD_ASSERT              AssertionError
              736  RAISE_VARARGS_1       1  'exception instance'
            738_0  COME_FROM           730  '730'

 L. 831       738  LOAD_DEREF               'mean'
              740  LOAD_METHOD              reshape
              742  LOAD_DEREF               'self'
              744  LOAD_ATTR                _elements
              746  LOAD_DEREF               'outkeys'
              748  LOAD_CONST               0
              750  BINARY_SUBSCR    
              752  BINARY_SUBSCR    
              754  LOAD_ATTR                shape
              756  CALL_METHOD_1         1  ''
              758  STORE_DEREF              'mean'

 L. 832       760  LOAD_DEREF               'cov'
              762  LOAD_METHOD              reshape
              764  LOAD_CONST               2
              766  LOAD_DEREF               'self'
              768  LOAD_ATTR                _elements
              770  LOAD_DEREF               'outkeys'
              772  LOAD_CONST               0
              774  BINARY_SUBSCR    
              776  BINARY_SUBSCR    
              778  LOAD_ATTR                shape
              780  BINARY_MULTIPLY  
              782  CALL_METHOD_1         1  ''
              784  STORE_DEREF              'cov'

 L. 833       786  LOAD_DEREF               'mean'
              788  LOAD_DEREF               'cov'
              790  BUILD_TUPLE_2         2 
              792  RETURN_VALUE     
            794_0  COME_FROM           716  '716'

 L. 835       794  LOAD_FAST                'keepcorr'
          796_798  POP_JUMP_IF_TRUE    812  'to 812'

 L. 836       800  LOAD_GLOBAL              gvar
              802  LOAD_METHOD              gvar
              804  LOAD_DEREF               'mean'
              806  LOAD_DEREF               'cov'
              808  CALL_METHOD_2         2  ''
              810  STORE_DEREF              'flatout'
            812_0  COME_FROM           796  '796'

 L. 838       812  LOAD_FAST                'strip'
          814_816  POP_JUMP_IF_TRUE    850  'to 850'

 L. 839       818  LOAD_GLOBAL              gvar
              820  LOAD_METHOD              BufferDict
              822  LOAD_CLOSURE             'flatout'
              824  LOAD_CLOSURE             'self'
              826  BUILD_TUPLE_2         2 
              828  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              830  LOAD_STR                 'GP.pred.<locals>.<dictcomp>'
              832  MAKE_FUNCTION_8          'closure'

 L. 841       834  LOAD_GLOBAL              zip
              836  LOAD_DEREF               'outkeys'
              838  LOAD_DEREF               'outslices'
              840  CALL_FUNCTION_2       2  ''

 L. 839       842  GET_ITER         
              844  CALL_FUNCTION_1       1  ''
              846  CALL_METHOD_1         1  ''
              848  RETURN_VALUE     
            850_0  COME_FROM           814  '814'

 L. 844       850  LOAD_GLOBAL              len
              852  LOAD_DEREF               'outkeys'
              854  CALL_FUNCTION_1       1  ''
              856  LOAD_CONST               1
              858  COMPARE_OP               ==
          860_862  POP_JUMP_IF_TRUE    868  'to 868'
              864  LOAD_ASSERT              AssertionError
              866  RAISE_VARARGS_1       1  'exception instance'
            868_0  COME_FROM           860  '860'

 L. 845       868  LOAD_DEREF               'flatout'
              870  LOAD_METHOD              reshape
              872  LOAD_DEREF               'self'
              874  LOAD_ATTR                _elements
              876  LOAD_DEREF               'outkeys'
              878  LOAD_CONST               0
              880  BINARY_SUBSCR    
              882  BINARY_SUBSCR    
              884  LOAD_ATTR                shape
              886  CALL_METHOD_1         1  ''
              888  RETURN_VALUE     

Parse error at or near `LOAD_DICTCOMP' instruction at offset 656

    def predfromfit(self, *args, **kw):
        """
        Like `pred` with `fromdata=False`.
        """
        return (self.pred)(args, fromdata=False, **kw)

    def predfromdata(self, *args, **kw):
        """
        Like `pred` with `fromdata=True`.
        """
        return (self.pred)(args, fromdata=True, **kw)

    def marginal_likelihood(self, given, givencov=None):
        """
        
        Compute (the logarithm of) the marginal likelihood given data, i.e. the
        probability of the data conditioned on the gaussian process prior and
        data error.
        
        Unlike `pred()`, you can't compute this with a fit result instead of
        data. If you used the gaussian process as latent variable in a fit,
        use the whole fit to compute the marginal likelihood. E.g. `lsqfit`
        always computes the logGBF (it's the same thing).
        
        The input is an array or dictionary of arrays, `given`. You can pass an
        array only if the GP has only one key. The contents of `given`
        represent the input data.
                
        Parameters
        ----------
        given : array or dictionary of arrays
            The data for some/all of the points in the GP. The arrays can
            contain either `gvar`s or normal numbers, the latter being
            equivalent to zero-uncertainty `gvar`s.
        givencov : array or dictionary of arrays
            Covariance matrix of `given`. If not specified, the covariance
            is extracted from `given` with `gvar.evalcov(given)`.
        
        Returns
        -------
        logGBF : scalar
            The logarithm of the marginal likelihood.
            
        """
        ylist, inkeys, ycovblocks = self._flatgiven(given, givencov)
        y = _concatenate_noop(ylist)
        if ycovblocks is not None:
            ycov = _block_matrix(ycovblocks)
            ymean = gvar.mean(y)
        else:
            if y.dtype == object:
                gvary = gvar.gvar(y)
                ycov = gvar.evalcov(gvary)
                ymean = gvar.mean(gvary)
            else:
                ycov = 0
                ymean = y
        if self._checkfinite:
            if not np.all(np.isfinite(ymean)):
                raise ValueError('mean of `given` is not finite')
        if self._checkfinite:
            if not np.all(np.isfinite(ycov)):
                raise ValueError('covariance matrix of `given` is not finite')
        decomp = self._solver(inkeys, ycov)
        return -0.5 * (decomp.quad(ymean) + decomp.logdet() + len(y) * np.log(2 * np.pi))