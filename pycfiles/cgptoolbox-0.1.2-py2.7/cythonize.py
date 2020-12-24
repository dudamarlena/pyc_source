# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\physmod\cythonize.py
# Compiled at: 2013-01-14 06:47:43
"""Cythonize the generated Python code for a CellML model."""
import re
from ..utils import codegen

def cythonize_model(s, modelname=''):
    """
    Cythonize the generated Python code for a CellML model.
    
    :param str s: original Python source code
    :param str modelname: name of model
    :rtype str: Cython source code
    """
    s = s.replace('constants = [0.0] * sizeConstants; states = [0.0] * sizeStates;', 'constants = np.zeros(sizeConstants, dtype=ftype); states = np.zeros(sizeStates, dtype=ftype)')
    for i in ('Algebraic', 'States', 'Constants'):
        s = s.replace('\nsize%s = ' % i, '\ncpdef int size%s = ' % i)

    w = ('equal less greater less_equal greater_equal').split()
    s = s.replace('\nfrom math import *\n', '\n## BEGIN Added by cythonize_model() ##\n\nimport ctypes\ncimport numpy as np\nimport numpy as np\nfrom numpy import *\nfrom pysundials.cvode import NVector\n\nftype = np.float64 # explicit type declaration, can be used with cython\nctypedef np.float64_t dtype_t\n\ncdef extern from "math.h":\n    dtype_t log(dtype_t x)\n    dtype_t exp(dtype_t x)\n    dtype_t floor(dtype_t x)\n    dtype_t fabs(dtype_t x)\n\ncdef extern from "Python.h":\n    ctypedef struct PyObject\n    void* PyLong_AsVoidPtr(PyObject *pylong)\n\n# C pointers to array of dtype_t\ncdef inline dtype_t* bufarr(x):\n    return <dtype_t*>(<np.ndarray>x).data\n\ncdef inline dtype_t* bufnv(v):\n    cdef long lp # 64-bit integers for pointers to buffers\n    lp = ctypes.addressof(v.cdata.contents)\n    return <dtype_t*>lp\n\n# Numpy arrays, can be used from Python\ny0 = np.zeros(sizeStates, dtype=ftype)\nydot = np.zeros(sizeStates, dtype=ftype)\np = np.zeros(sizeConstants, dtype=ftype)\nalgebraic = np.zeros(sizeAlgebraic, dtype=ftype)\n\n# Pointers to array of dtype_t, fast access from Cython\ncdef dtype_t* py0 = bufarr(y0)\ncdef dtype_t* pydot = bufarr(ydot)\ncdef dtype_t* pp = bufarr(p)\ncdef dtype_t* palgebraic = bufarr(algebraic)\n\ncpdef int ode(dtype_t t, y, ydot, f_data):\n    cdef dtype_t *py, *pydot # pointers to buffers\n    cdef str msg = "Use of f_data not implemented; use global array p instead"\n    assert f_data is None, msg\n    # make this work with both numpy.ndarray and pysundials.cvode.NVector\n    if isinstance(y, NVector):\n        py = bufnv(y)\n    else:\n        assert isinstance(y, np.ndarray)\n        py = bufarr(y)\n    if isinstance(ydot, NVector):\n        pydot = bufnv(ydot)\n    else:\n        assert isinstance(ydot, np.ndarray)\n        pydot = bufarr(ydot)\n    # NVector has no .fill method, so do this the hard way\n    cdef int i\n    # ydot.fill(0.0)\n    for i in range(sizeStates):\n        pydot[i] = 0.0\n    # algebraic.fill(0.0)\n    for i in range(sizeAlgebraic):\n        palgebraic[i] = 0.0\n    compute_rates(t, py, pydot, pp, palgebraic)\n    return 0\n\ndef rates_and_algebraic(np.ndarray[dtype_t, ndim=1] t, y):\n    """\n    Compute rates and algebraic variables for a given state trajectory.\n    \n    Unfortunately, the CVODE machinery does not offer a way to return rates and \n    algebraic variables during integration. This function re-computes the rates \n    and algebraics at each time step for the given state.\n    \n    >>> from cgp.physmod.cellmlmodel import Cellmlmodel\n    >>> workspace = "bondarenko_szigeti_bett_kim_rasmusson_2004"\n    >>> bond = Cellmlmodel(workspace, t=[0, 20])\n    >>> with bond.autorestore():\n    ...     bond.yr.V = 100 # simulate stimulus\n    ...     t, y, flag = bond.integrate()\n    >>> ydot, alg = bond.model.rates_and_algebraic(t, y)\n    >>> from pylab import * # doctest: +SKIP\n    >>> plot(t, alg.view(bond.dtype.a)["J_xfer"], \'.-\', t, y.Cai, \'.-\') # doctest: +SKIP\n    \n    Verify that this Cython version is equivalent to the pure Python version.\n    \n    >>> bondp = Cellmlmodel(workspace, t=[0, 20], \n    ...     use_cython=False, purge=True)\n    >>> ydotp, algp = bondp.model.rates_and_algebraic(t, y)\n    >>> np.testing.assert_almost_equal(ydot, ydotp, decimal=5)\n    >>> np.testing.assert_almost_equal(alg, algp, decimal=5)\n    """\n    cdef int imax = len(t)\n    y = y.view(ftype)\n    ydot = np.zeros_like(y)\n    alg = np.zeros((imax, len(algebraic)))\n    cdef double* py\n    cdef double* pydot\n    cdef double * palgebraic\n    cdef int i\n    for i in range(imax):\n        py = bufarr(y[i])\n        pydot = bufarr(ydot[i])\n        palgebraic = bufarr(alg[i])\n        compute_rates(t[i], py, pydot, pp, palgebraic)\n        compute_algebraic(t[i], py, pp, palgebraic)\n    return ydot, alg\n\n\n## END Added by cythonize_model() ##\n')
    s0 = '\ndef computeRates(voi, states, constants):\n    rates = [0.0] * sizeStates; algebraic = [0.0] * sizeAlgebraic\n'
    i0 = s.find(s0)
    s1 = '\n    return(rates)\n'
    i1 = s.find(s1)
    compute_rates_code = s[i0:i1]
    L = [ repcp(line) for line in compute_rates_code.split('\n') ]
    L = [ prepend('cy_', w, line) for line in L ]
    compute_rates_code = ('\n').join(L)
    s += compute_rates_code.replace(s0.strip(), '\n\n## BEGIN Added by cythonize_model() ##\n\ncdef inline bint cy_equal(dtype_t x, dtype_t y):\n    return x == y\n\ncdef inline bint cy_greater(dtype_t x, dtype_t y):\n    return x > y\n\ncdef inline bint cy_less(dtype_t x, dtype_t y):\n    return x < y\n\ncdef inline bint cy_greater_equal(dtype_t x, dtype_t y):\n    return x >= y\n\ncdef inline bint cy_less_equal(dtype_t x, dtype_t y):\n    return x <= y\n\ncimport cython\n@cython.cdivision(True)\ncdef void compute_rates(dtype_t voi, dtype_t* states, dtype_t* rates, dtype_t* constants, dtype_t* algebraic):\n    pass  # in case function body is empty\n') + '\n'
    s0 = '\ndef computeAlgebraic(constants, states, voi):\n    algebraic = array([[0.0] * len(voi)] * sizeAlgebraic)\n    states = array(states)\n    voi = array(voi)\n'
    i0 = s.find(s0)
    s1 = '\n    return algebraic\n'
    i1 = s.find(s1)
    compute_algebraic_code = s[i0:i1]
    L = [ repcp(line) for line in compute_algebraic_code.split('\n') ]
    L = [ prepend('cy_', w, line) for line in L ]
    compute_algebraic_code = ('\n').join(L) + '\n'
    s += compute_algebraic_code.replace(s0, '\n\n@cython.cdivision(True)\ncdef void compute_algebraic(dtype_t voi, dtype_t* states, dtype_t* constants, dtype_t* algebraic):\n    pass # in case there is no function body left after eliminating s0\n') + '\n'
    s += '\ndef bench():\n    """\n    Benchmark ode().\n    \n    To profile execution, prepend this line to the module::\n    \n        # cython: profile=True\n    \n    This can be used with the usual Python or IPython profiler.\n    Unfortunately, Cython does not have line profiling.\n    \n    In IPython::\n    \n        >>> import module_name as m         # doctest: +SKIP\n        >>> prun m.bench()                  # doctest: +SKIP\n        \n        Sample output:\n        1400004 function calls in 9.270 CPU seconds\n        ncalls  tottime  percall  cumtime  percall filename:lineno(function)\n        100000    4.952    0.000    7.322    0.000 BL6WT_200410.pyx:736(compute_rates)\n        100000    1.182    0.000    8.976    0.000 BL6WT_200410.pyx:60(ode)\n        400000    0.946    0.000    0.946    0.000 BL6WT_200410.pyx:731(cy_custom_piecewise)\n    """\n    cdef int i\n    for i in range(10000):\n        ode(0, y0, ydot, None)\n\ny0[:], p[:] = initConsts()\n\n## END Added by cythonize_model() ##\n'
    setup = '\n"""\n%(modelname)s setup file.\nUsage: python setup.py build_ext --inplace\n\nIt may be necessary to remove intermediate files from previous builds:\n\nLinux:\nrm -rf build m.so m.c && python setup.py build_ext --inplace && python -c "import m"\n\nWindows:\ndel /q build m.pyd m.c\npython setup.py build_ext --inplace\npython -c "import m"\n"""\nfrom distutils.core import setup\nfrom distutils.extension import Extension\nfrom Cython.Distutils import build_ext\nimport numpy as np\nimport platform\nimport os\n\nextname = "cy"\nHOME = os.environ["HOME"]\n\nif platform.system() == "Windows":\n    ext_modules = [Extension(extname, [extname + ".pyx"],\n        include_dirs=[\'c:/MinGW/msys/1.0/local/include\', \'c:/msys/1.0/local/include\', np.get_include()],\n        library_dirs=[\'c:/MinGW/msys/1.0/local/lib\', \'c:/msys/1.0/local/lib\'],\n        libraries=[\'sundials_cvode\', \'sundials_nvecserial\'])]\nelif platform.system() == "Linux":\n    if "stallo" in platform.node():\n        ext_modules = [Extension(extname, [extname + ".pyx"],\n            include_dirs=[HOME + \'/usr/include\', np.get_include()],\n            library_dirs=[HOME + \'/usr/lib\'],\n            libraries=[\'sundials_cvode\', \'sundials_nvecserial\'])]\n    else: # Titan\n        ext_modules = [Extension(extname, [extname + ".pyx"],\n            include_dirs=[HOME + \'/usr/include\', \'/site/VERSIONS/sundials-2.3.0/include\', np.get_include()],\n            library_dirs=[HOME + \'/usr/lib\', \'/site/VERSIONS/sundials-2.3.0/lib\'],\n            libraries=[\'sundials_cvode\', \'sundials_nvecserial\'])]\nelif platform.system() == "Darwin":  # Mac OS X\n    ext_modules = [Extension(extname, [extname + ".pyx"],\n        include_dirs=[\'/usr/local/include\', np.get_include()],\n        library_dirs=[\'/usr/local/lib\'],\n        libraries=[\'sundials_cvode\', \'sundials_nvecserial\'])]\n\nsetup(\n    name = extname,\n    cmdclass = {"build_ext": build_ext},\n    ext_modules = ext_modules\n)\n'
    return (s, setup % dict(modelname=modelname))


def rep--- This code section failed: ---

 L. 311         0  LOAD_FAST             1  'old'
                3  LOAD_CONST               '(['
                6  BINARY_ADD       
                7  STORE_FAST            3  'pattern'

 L. 312        10  SETUP_LOOP          206  'to 219'
               13  LOAD_FAST             3  'pattern'
               16  LOAD_FAST             0  's'
               19  COMPARE_OP            6  in
               22  POP_JUMP_IF_FALSE   218  'to 218'

 L. 314        25  LOAD_FAST             0  's'
               28  LOAD_ATTR             0  'partition'
               31  LOAD_FAST             3  'pattern'
               34  CALL_FUNCTION_1       1  None
               37  UNPACK_SEQUENCE_3     3 
               40  STORE_FAST            4  'before'
               43  STORE_FAST            5  '_sep'
               46  STORE_FAST            6  'after'

 L. 316        49  LOAD_CONST               1
               52  STORE_FAST            7  'nesting_level'

 L. 317        55  SETUP_LOOP           92  'to 150'
               58  LOAD_GLOBAL           1  'enumerate'
               61  LOAD_FAST             6  'after'
               64  CALL_FUNCTION_1       1  None
               67  GET_ITER         
               68  FOR_ITER             78  'to 149'
               71  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST            8  'pos'
               77  STORE_FAST            9  'char'

 L. 318        80  LOAD_FAST             9  'char'
               83  LOAD_CONST               '['
               86  COMPARE_OP            2  ==
               89  POP_JUMP_IF_FALSE   105  'to 105'

 L. 319        92  LOAD_FAST             7  'nesting_level'
               95  LOAD_CONST               1
               98  INPLACE_ADD      
               99  STORE_FAST            7  'nesting_level'
              102  JUMP_FORWARD         25  'to 130'

 L. 320       105  LOAD_FAST             9  'char'
              108  LOAD_CONST               ']'
              111  COMPARE_OP            2  ==
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L. 321       117  LOAD_FAST             7  'nesting_level'
              120  LOAD_CONST               1
              123  INPLACE_SUBTRACT 
              124  STORE_FAST            7  'nesting_level'
              127  JUMP_FORWARD          0  'to 130'
            130_0  COME_FROM           127  '127'
            130_1  COME_FROM           102  '102'

 L. 322       130  LOAD_FAST             7  'nesting_level'
              133  LOAD_CONST               0
              136  COMPARE_OP            2  ==
              139  POP_JUMP_IF_FALSE    68  'to 68'

 L. 323       142  BREAK_LOOP       
              143  JUMP_BACK            68  'to 68'
              146  JUMP_BACK            68  'to 68'
              149  POP_BLOCK        
            150_0  COME_FROM            55  '55'

 L. 324       150  LOAD_FAST             7  'nesting_level'
              153  LOAD_CONST               0
              156  COMPARE_OP            2  ==
              159  POP_JUMP_IF_TRUE    175  'to 175'
              162  LOAD_ASSERT              AssertionError
              165  LOAD_CONST               "Matching bracket not found in '%s'"
              168  LOAD_FAST             0  's'
              171  BINARY_MODULO    
              172  RAISE_VARARGS_2       2  None

 L. 326       175  LOAD_FAST             6  'after'
              178  LOAD_FAST             8  'pos'
              181  SLICE+2          
              182  LOAD_FAST             6  'after'
              185  LOAD_FAST             8  'pos'
              188  LOAD_CONST               1
              191  BINARY_ADD       
              192  SLICE+1          
              193  BINARY_ADD       
              194  STORE_FAST            6  'after'

 L. 327       197  LOAD_FAST             4  'before'
              200  LOAD_FAST             2  'new'
              203  BINARY_ADD       
              204  LOAD_CONST               '('
              207  BINARY_ADD       
              208  LOAD_FAST             6  'after'
              211  BINARY_ADD       
              212  STORE_FAST            0  's'
              215  JUMP_BACK            13  'to 13'
              218  POP_BLOCK        
            219_0  COME_FROM            10  '10'

 L. 328       219  LOAD_FAST             0  's'
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 218


def cp2cond(s):
    """
    Make a conditional expression to replace a call to custom_piecewise().
    
    The CellML code generator outputs "ternary if" expressions for C 
    (cond ? val_if_true : val_if_false)
    but not (val_if_true if cond else val_if_false) for Python.
    Instead, it defines a custom_piecewise() function which is about 1000 times 
    slower and barely legible. This function returns equivalent code that uses 
    Python's native conditional expressions, which Cython can convert to 
    efficient C.
    
    The typical case is one condition and 0 otherwise.
    CellML then ends the list with True, 0.
    The final "else 0" mimics the behaviour of custom_piecewise() and 
    np.select() if no conditions match.
    
    >>> cp2cond('custom_piecewise([x<3, "<3", True, 0])')
    "('<3' if (x < 3) else 0 if True else 0)"
    
    Two conditions, so the final "else 0" is not redundant.
    
    >>> cp2cond('custom_piecewise([x<3, "<3", x>5, ">5"])')
    "('<3' if (x < 3) else '>5' if (x > 5) else 0)"
    
    Two conditions and otherwise 0, as CellML might code it.
    
    >>> cp2cond('custom_piecewise([x<3, "<3", x>5, ">5", True, 0])')
    "('<3' if (x < 3) else '>5' if (x > 5) else 0 if True else 0)"
    
    Function call as list item.
    
    >>> cp2cond('custom_piecewise([f(x,1), "<3", x>5, ">5", True, 0])')
    "('<3' if f(x, 1) else '>5' if (x > 5) else 0 if True else 0)"
    """
    p = codegen.parse(s)
    L = [ codegen.to_source(i) for i in p.body[0].value.args[0].elts ]
    cond = L[0::2]
    val = L[1::2]
    ifelse = (' ').join('%s if %s else' % (v, c) for c, v in zip(cond, val))
    return '(%s 0)' % ifelse


def repcp--- This code section failed: ---

 L. 380         0  LOAD_CONST               'custom_piecewise(['
                3  STORE_FAST            1  'pattern'

 L. 381         6  SETUP_LOOP          240  'to 249'
                9  LOAD_FAST             1  'pattern'
               12  LOAD_FAST             0  's'
               15  COMPARE_OP            6  in
               18  POP_JUMP_IF_FALSE   248  'to 248'

 L. 383        21  LOAD_FAST             0  's'
               24  LOAD_ATTR             0  'partition'
               27  LOAD_FAST             1  'pattern'
               30  CALL_FUNCTION_1       1  None
               33  UNPACK_SEQUENCE_3     3 
               36  STORE_FAST            2  '_before'
               39  STORE_FAST            3  'sep'
               42  STORE_FAST            4  'after'

 L. 385        45  LOAD_CONST               1
               48  STORE_FAST            5  'nesting_level'

 L. 386        51  SETUP_LOOP           92  'to 146'
               54  LOAD_GLOBAL           1  'enumerate'
               57  LOAD_FAST             4  'after'
               60  CALL_FUNCTION_1       1  None
               63  GET_ITER         
               64  FOR_ITER             78  'to 145'
               67  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST            6  'pos'
               73  STORE_FAST            7  'char'

 L. 387        76  LOAD_FAST             7  'char'
               79  LOAD_CONST               '['
               82  COMPARE_OP            2  ==
               85  POP_JUMP_IF_FALSE   101  'to 101'

 L. 388        88  LOAD_FAST             5  'nesting_level'
               91  LOAD_CONST               1
               94  INPLACE_ADD      
               95  STORE_FAST            5  'nesting_level'
               98  JUMP_FORWARD         25  'to 126'

 L. 389       101  LOAD_FAST             7  'char'
              104  LOAD_CONST               ']'
              107  COMPARE_OP            2  ==
              110  POP_JUMP_IF_FALSE   126  'to 126'

 L. 390       113  LOAD_FAST             5  'nesting_level'
              116  LOAD_CONST               1
              119  INPLACE_SUBTRACT 
              120  STORE_FAST            5  'nesting_level'
              123  JUMP_FORWARD          0  'to 126'
            126_0  COME_FROM           123  '123'
            126_1  COME_FROM            98  '98'

 L. 391       126  LOAD_FAST             5  'nesting_level'
              129  LOAD_CONST               0
              132  COMPARE_OP            2  ==
              135  POP_JUMP_IF_FALSE    64  'to 64'

 L. 392       138  BREAK_LOOP       
              139  JUMP_BACK            64  'to 64'
              142  JUMP_BACK            64  'to 64'
              145  POP_BLOCK        
            146_0  COME_FROM            51  '51'

 L. 393       146  LOAD_FAST             5  'nesting_level'
              149  LOAD_CONST               0
              152  COMPARE_OP            2  ==
              155  POP_JUMP_IF_TRUE    171  'to 171'
              158  LOAD_ASSERT              AssertionError
              161  LOAD_CONST               "Matching bracket not found in '%s'"
              164  LOAD_FAST             0  's'
              167  BINARY_MODULO    
              168  RAISE_VARARGS_2       2  None

 L. 394       171  LOAD_FAST             0  's'
              174  LOAD_ATTR             3  'index'
              177  LOAD_FAST             1  'pattern'
              180  CALL_FUNCTION_1       1  None
              183  STORE_FAST            8  'ibefore'

 L. 395       186  LOAD_FAST             8  'ibefore'
              189  LOAD_GLOBAL           4  'len'
              192  LOAD_FAST             3  'sep'
              195  CALL_FUNCTION_1       1  None
              198  BINARY_ADD       
              199  LOAD_FAST             6  'pos'
              202  BINARY_ADD       
              203  LOAD_CONST               2
              206  BINARY_ADD       
              207  STORE_FAST            9  'iafter'

 L. 396       210  LOAD_FAST             0  's'
              213  LOAD_FAST             8  'ibefore'
              216  SLICE+2          
              217  LOAD_GLOBAL           5  'cp2cond'
              220  LOAD_FAST             0  's'
              223  LOAD_FAST             8  'ibefore'
              226  LOAD_FAST             9  'iafter'
              229  SLICE+3          
              230  CALL_FUNCTION_1       1  None
              233  BINARY_ADD       
              234  LOAD_FAST             0  's'
              237  LOAD_FAST             9  'iafter'
              240  SLICE+1          
              241  BINARY_ADD       
              242  STORE_FAST            0  's'
              245  JUMP_BACK             9  'to 9'
              248  POP_BLOCK        
            249_0  COME_FROM             6  '6'

 L. 397       249  LOAD_FAST             0  's'
              252  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 248


def prepend(prefix, words, string):
    """
    Prepend prefix to certain words in a string.
    
    >>> prepend("PREFIX", ["is", "test"], "This is a test: test_is")
    'This PREFIXis a PREFIXtest: test_is'
    """
    for w in words:
        string = re.sub('\\b%s\\b' % w, prefix + w, string)

    return string


if __name__ == '__main__':
    import doctest
    doctest.testmod()