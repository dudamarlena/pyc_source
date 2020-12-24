# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/optimize/nelder_mead.py
# Compiled at: 2019-07-07 21:19:40
# Size of source mod 2**32: 14146 bytes
"""
Implements the Nelder-Mead algorithm for maximizing a function with one or more
variables.

"""
import numpy as np
from numba import njit
from collections import namedtuple
results = namedtuple('results', 'x fun success nit final_simplex')

@njit
def nelder_mead(fun, x0, bounds=np.array([[], []]).T, args=(), tol_f=1e-10, tol_x=1e-10, max_iter=1000):
    """
    .. highlight:: none

    Maximize a scalar-valued function with one or more variables using the
    Nelder-Mead method.

    This function is JIT-compiled in `nopython` mode using Numba.

    Parameters
    ----------
    fun : callable
        The objective function to be maximized: `fun(x, *args) -> float`
        where x is an 1-D array with shape (n,) and args is a tuple of the
        fixed parameters needed to completely specify the function. This
        function must be JIT-compiled in `nopython` mode using Numba.

    x0 : ndarray(float, ndim=1)
        Initial guess. Array of real elements of size (n,), where ‘n’ is the
        number of independent variables.

    bounds: ndarray(float, ndim=2), optional
        Bounds for each variable for proposed solution, encoded as a sequence
        of (min, max) pairs for each element in x. The default option is used
        to specify no bounds on x.

    args : tuple, optional
        Extra arguments passed to the objective function.

    tol_f : scalar(float), optional(default=1e-10)
        Tolerance to be used for the function value convergence test.

    tol_x : scalar(float), optional(default=1e-10)
        Tolerance to be used for the function domain convergence test.

    max_iter : scalar(float), optional(default=1000)
        The maximum number of allowed iterations.

    Returns
    ----------
    results : namedtuple
        A namedtuple containing the following items:
        ::

            "x" : Approximate local maximizer
            "fun" : Approximate local maximum value
            "success" : 1 if the algorithm successfully terminated, 0 otherwise
            "nit" : Number of iterations
            "final_simplex" : Vertices of the final simplex

    Examples
    --------
    >>> @njit
    ... def rosenbrock(x):
    ...     return -(100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0])**2)
    ...
    >>> x0 = np.array([-2, 1])
    >>> qe.optimize.nelder_mead(rosenbrock, x0)
    results(x=array([0.99999814, 0.99999756]), fun=-1.6936258239463265e-10,
            success=True, nit=110,
            final_simplex=array([[0.99998652, 0.9999727],
                                 [1.00000218, 1.00000301],
                                 [0.99999814, 0.99999756]]))

    Notes
    --------
    This algorithm has a long history of successful use in applications, but it
    will usually be slower than an algorithm that uses first or second
    derivative information. In practice, it can have poor performance in
    high-dimensional problems and is not robust to minimizing complicated
    functions. Additionally, there currently is no complete theory describing
    when the algorithm will successfully converge to the minimum, or how fast
    it will if it does.

    References
    ----------

    .. [1] J. C. Lagarias, J. A. Reeds, M. H. Wright and P. E. Wright,
           Convergence Properties of the Nelder–Mead Simplex Method in Low
           Dimensions, SIAM. J. Optim. 9, 112–147 (1998).

    .. [2] S. Singer and S. Singer, Efficient implementation of the Nelder–Mead
           search algorithm, Appl. Numer. Anal. Comput. Math., vol. 1, no. 2,
           pp. 524–534, 2004.

    .. [3] J. A. Nelder and R. Mead, A simplex method for function
           minimization, Comput. J. 7, 308–313 (1965).

    .. [4] Gao, F. and Han, L., Implementing the Nelder-Mead simplex algorithm
           with adaptive parameters, Comput Optim Appl (2012) 51: 259.

    .. [5] http://www.scholarpedia.org/article/Nelder-Mead_algorithm

    .. [6] http://www.brnt.eu/phd/node10.html#SECTION00622200000000000000

    .. [7] Chase Coleman's tutorial on Nelder Mead

    .. [8] SciPy's Nelder-Mead implementation

    """
    vertices = _initialize_simplex(x0, bounds)
    results = _nelder_mead_algorithm(fun, vertices, bounds, args=args, tol_f=tol_f,
      tol_x=tol_x,
      max_iter=max_iter)
    return results


@njit
def _nelder_mead_algorithm--- This code section failed: ---

 L. 185         0  LOAD_FAST                'vertices'
                2  LOAD_ATTR                shape
                4  LOAD_CONST               1
                6  BINARY_SUBSCR    
                8  STORE_FAST               'n'

 L. 186        10  LOAD_GLOBAL              _check_params
               12  LOAD_FAST                'ρ'
               14  LOAD_FAST                'χ'
               16  LOAD_FAST                'γ'
               18  LOAD_FAST                'σ'
               20  LOAD_FAST                'bounds'
               22  LOAD_FAST                'n'
               24  CALL_FUNCTION_6       6  '6 positional arguments'
               26  POP_TOP          

 L. 188        28  LOAD_CONST               0
               30  STORE_FAST               'nit'

 L. 190        32  LOAD_FAST                'ρ'
               34  LOAD_FAST                'γ'
               36  BINARY_MULTIPLY  
               38  STORE_FAST               'ργ'

 L. 191        40  LOAD_FAST                'ρ'
               42  LOAD_FAST                'χ'
               44  BINARY_MULTIPLY  
               46  STORE_FAST               'ρχ'

 L. 192        48  LOAD_FAST                'σ'
               50  LOAD_FAST                'n'
               52  BINARY_POWER     
               54  STORE_FAST               'σ_n'

 L. 194        56  LOAD_GLOBAL              np
               58  LOAD_ATTR                empty
               60  LOAD_FAST                'n'
               62  LOAD_CONST               1
               64  BINARY_ADD       
               66  LOAD_GLOBAL              np
               68  LOAD_ATTR                float64
               70  LOAD_CONST               ('dtype',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  STORE_FAST               'f_val'

 L. 195        76  SETUP_LOOP          122  'to 122'
               78  LOAD_GLOBAL              range
               80  LOAD_FAST                'n'
               82  LOAD_CONST               1
               84  BINARY_ADD       
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  GET_ITER         
               90  FOR_ITER            120  'to 120'
               92  STORE_FAST               'i'

 L. 196        94  LOAD_GLOBAL              _neg_bounded_fun
               96  LOAD_FAST                'fun'
               98  LOAD_FAST                'bounds'
              100  LOAD_FAST                'vertices'
              102  LOAD_FAST                'i'
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'args'
              108  LOAD_CONST               ('args',)
              110  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              112  LOAD_FAST                'f_val'
              114  LOAD_FAST                'i'
              116  STORE_SUBSCR     
              118  JUMP_BACK            90  'to 90'
              120  POP_BLOCK        
            122_0  COME_FROM_LOOP       76  '76'

 L. 199       122  LOAD_FAST                'f_val'
              124  LOAD_METHOD              argsort
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  STORE_FAST               'sort_ind'

 L. 200       130  LOAD_CONST               1
              132  STORE_FAST               'LV_ratio'

 L. 203       134  LOAD_FAST                'vertices'
              136  LOAD_FAST                'sort_ind'
              138  LOAD_CONST               None
              140  LOAD_FAST                'n'
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  BINARY_SUBSCR    
              148  LOAD_ATTR                sum
              150  LOAD_CONST               0
              152  LOAD_CONST               ('axis',)
              154  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              156  LOAD_FAST                'n'
              158  BINARY_TRUE_DIVIDE
              160  STORE_FAST               'x_bar'

 L. 205   162_164  SETUP_LOOP          850  'to 850'

 L. 206       166  LOAD_CONST               False
              168  STORE_FAST               'shrink'

 L. 209       170  LOAD_FAST                'nit'
              172  LOAD_FAST                'max_iter'
              174  COMPARE_OP               >=
              176  STORE_FAST               'fail'

 L. 211       178  LOAD_FAST                'sort_ind'
              180  LOAD_CONST               0
              182  BINARY_SUBSCR    
              184  STORE_FAST               'best_val_idx'

 L. 212       186  LOAD_FAST                'sort_ind'
              188  LOAD_FAST                'n'
              190  BINARY_SUBSCR    
              192  STORE_FAST               'worst_val_idx'

 L. 214       194  LOAD_FAST                'f_val'
              196  LOAD_FAST                'worst_val_idx'
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'f_val'
              202  LOAD_FAST                'best_val_idx'
              204  BINARY_SUBSCR    
              206  BINARY_SUBTRACT  
              208  LOAD_FAST                'tol_f'
              210  COMPARE_OP               <
              212  STORE_FAST               'term_f'

 L. 217       214  LOAD_FAST                'LV_ratio'
              216  LOAD_FAST                'tol_x'
              218  COMPARE_OP               <
              220  STORE_FAST               'term_x'

 L. 219       222  LOAD_FAST                'term_x'
              224  POP_JUMP_IF_TRUE    234  'to 234'
              226  LOAD_FAST                'term_f'
              228  POP_JUMP_IF_TRUE    234  'to 234'
              230  LOAD_FAST                'fail'
              232  POP_JUMP_IF_FALSE   236  'to 236'
            234_0  COME_FROM           228  '228'
            234_1  COME_FROM           224  '224'

 L. 220       234  BREAK_LOOP       
            236_0  COME_FROM           232  '232'

 L. 223       236  LOAD_FAST                'x_bar'
              238  LOAD_FAST                'ρ'
              240  LOAD_FAST                'x_bar'
              242  LOAD_FAST                'vertices'
              244  LOAD_FAST                'worst_val_idx'
              246  BINARY_SUBSCR    
              248  BINARY_SUBTRACT  
              250  BINARY_MULTIPLY  
              252  BINARY_ADD       
              254  STORE_FAST               'x_r'

 L. 224       256  LOAD_GLOBAL              _neg_bounded_fun
              258  LOAD_FAST                'fun'
              260  LOAD_FAST                'bounds'
              262  LOAD_FAST                'x_r'
              264  LOAD_FAST                'args'
              266  LOAD_CONST               ('args',)
              268  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              270  STORE_FAST               'f_r'

 L. 226       272  LOAD_FAST                'f_r'
              274  LOAD_FAST                'f_val'
              276  LOAD_FAST                'best_val_idx'
              278  BINARY_SUBSCR    
              280  COMPARE_OP               >=
          282_284  POP_JUMP_IF_FALSE   328  'to 328'
              286  LOAD_FAST                'f_r'
              288  LOAD_FAST                'f_val'
              290  LOAD_FAST                'sort_ind'
              292  LOAD_FAST                'n'
              294  LOAD_CONST               1
              296  BINARY_SUBTRACT  
              298  BINARY_SUBSCR    
              300  BINARY_SUBSCR    
              302  COMPARE_OP               <
          304_306  POP_JUMP_IF_FALSE   328  'to 328'

 L. 228       308  LOAD_FAST                'x_r'
              310  LOAD_FAST                'vertices'
              312  LOAD_FAST                'worst_val_idx'
              314  STORE_SUBSCR     

 L. 229       316  LOAD_FAST                'LV_ratio'
              318  LOAD_FAST                'ρ'
              320  INPLACE_MULTIPLY 
              322  STORE_FAST               'LV_ratio'
          324_326  JUMP_FORWARD        704  'to 704'
            328_0  COME_FROM           304  '304'
            328_1  COME_FROM           282  '282'

 L. 232       328  LOAD_FAST                'f_r'
              330  LOAD_FAST                'f_val'
              332  LOAD_FAST                'best_val_idx'
              334  BINARY_SUBSCR    
              336  COMPARE_OP               <
          338_340  POP_JUMP_IF_FALSE   422  'to 422'

 L. 233       342  LOAD_FAST                'x_bar'
              344  LOAD_FAST                'χ'
              346  LOAD_FAST                'x_r'
              348  LOAD_FAST                'x_bar'
              350  BINARY_SUBTRACT  
              352  BINARY_MULTIPLY  
              354  BINARY_ADD       
              356  STORE_FAST               'x_e'

 L. 234       358  LOAD_GLOBAL              _neg_bounded_fun
              360  LOAD_FAST                'fun'
              362  LOAD_FAST                'bounds'
              364  LOAD_FAST                'x_e'
              366  LOAD_FAST                'args'
              368  LOAD_CONST               ('args',)
              370  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              372  STORE_FAST               'f_e'

 L. 235       374  LOAD_FAST                'f_e'
              376  LOAD_FAST                'f_r'
              378  COMPARE_OP               <
          380_382  POP_JUMP_IF_FALSE   402  'to 402'

 L. 236       384  LOAD_FAST                'x_e'
              386  LOAD_FAST                'vertices'
              388  LOAD_FAST                'worst_val_idx'
              390  STORE_SUBSCR     

 L. 237       392  LOAD_FAST                'LV_ratio'
              394  LOAD_FAST                'ρχ'
              396  INPLACE_MULTIPLY 
              398  STORE_FAST               'LV_ratio'
              400  JUMP_FORWARD        704  'to 704'
            402_0  COME_FROM           380  '380'

 L. 239       402  LOAD_FAST                'x_r'
              404  LOAD_FAST                'vertices'
              406  LOAD_FAST                'worst_val_idx'
              408  STORE_SUBSCR     

 L. 240       410  LOAD_FAST                'LV_ratio'
              412  LOAD_FAST                'ρ'
              414  INPLACE_MULTIPLY 
              416  STORE_FAST               'LV_ratio'
          418_420  JUMP_FORWARD        704  'to 704'
            422_0  COME_FROM           338  '338'

 L. 245       422  LOAD_FAST                'f_r'
              424  LOAD_FAST                'f_val'
              426  LOAD_FAST                'worst_val_idx'
              428  BINARY_SUBSCR    
              430  COMPARE_OP               <
          432_434  POP_JUMP_IF_FALSE   458  'to 458'

 L. 246       436  LOAD_FAST                'x_bar'
              438  LOAD_FAST                'γ'
              440  LOAD_FAST                'x_r'
              442  LOAD_FAST                'x_bar'
              444  BINARY_SUBTRACT  
              446  BINARY_MULTIPLY  
              448  BINARY_ADD       
              450  STORE_FAST               'x_c'

 L. 247       452  LOAD_FAST                'ργ'
              454  STORE_FAST               'LV_ratio_update'
              456  JUMP_FORWARD        478  'to 478'
            458_0  COME_FROM           432  '432'

 L. 249       458  LOAD_FAST                'x_bar'
              460  LOAD_FAST                'γ'
              462  LOAD_FAST                'x_r'
              464  LOAD_FAST                'x_bar'
              466  BINARY_SUBTRACT  
              468  BINARY_MULTIPLY  
              470  BINARY_SUBTRACT  
              472  STORE_FAST               'x_c'

 L. 250       474  LOAD_FAST                'γ'
              476  STORE_FAST               'LV_ratio_update'
            478_0  COME_FROM           456  '456'

 L. 252       478  LOAD_GLOBAL              _neg_bounded_fun
              480  LOAD_FAST                'fun'
              482  LOAD_FAST                'bounds'
              484  LOAD_FAST                'x_c'
              486  LOAD_FAST                'args'
              488  LOAD_CONST               ('args',)
              490  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              492  STORE_FAST               'f_c'

 L. 253       494  LOAD_FAST                'f_c'
              496  LOAD_GLOBAL              min
              498  LOAD_FAST                'f_r'
              500  LOAD_FAST                'f_val'
              502  LOAD_FAST                'worst_val_idx'
              504  BINARY_SUBSCR    
              506  CALL_FUNCTION_2       2  '2 positional arguments'
              508  COMPARE_OP               <
          510_512  POP_JUMP_IF_FALSE   532  'to 532'

 L. 254       514  LOAD_FAST                'x_c'
              516  LOAD_FAST                'vertices'
              518  LOAD_FAST                'worst_val_idx'
              520  STORE_SUBSCR     

 L. 255       522  LOAD_FAST                'LV_ratio'
              524  LOAD_FAST                'LV_ratio_update'
              526  INPLACE_MULTIPLY 
              528  STORE_FAST               'LV_ratio'
              530  JUMP_FORWARD        704  'to 704'
            532_0  COME_FROM           510  '510'

 L. 259       532  LOAD_CONST               True
              534  STORE_FAST               'shrink'

 L. 260       536  SETUP_LOOP          616  'to 616'
              538  LOAD_FAST                'sort_ind'
              540  LOAD_CONST               1
              542  LOAD_CONST               None
              544  BUILD_SLICE_2         2 
              546  BINARY_SUBSCR    
              548  GET_ITER         
              550  FOR_ITER            614  'to 614'
              552  STORE_FAST               'i'

 L. 261       554  LOAD_FAST                'vertices'
              556  LOAD_FAST                'best_val_idx'
              558  BINARY_SUBSCR    
              560  LOAD_FAST                'σ'

 L. 262       562  LOAD_FAST                'vertices'
              564  LOAD_FAST                'i'
              566  BINARY_SUBSCR    
              568  LOAD_FAST                'vertices'
              570  LOAD_FAST                'best_val_idx'
              572  BINARY_SUBSCR    
              574  BINARY_SUBTRACT  
              576  BINARY_MULTIPLY  
              578  BINARY_ADD       
              580  LOAD_FAST                'vertices'
              582  LOAD_FAST                'i'
              584  STORE_SUBSCR     

 L. 263       586  LOAD_GLOBAL              _neg_bounded_fun
              588  LOAD_FAST                'fun'
              590  LOAD_FAST                'bounds'
              592  LOAD_FAST                'vertices'
              594  LOAD_FAST                'i'
              596  BINARY_SUBSCR    

 L. 264       598  LOAD_FAST                'args'
              600  LOAD_CONST               ('args',)
              602  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              604  LOAD_FAST                'f_val'
              606  LOAD_FAST                'i'
              608  STORE_SUBSCR     
          610_612  JUMP_BACK           550  'to 550'
              614  POP_BLOCK        
            616_0  COME_FROM_LOOP      536  '536'

 L. 266       616  LOAD_FAST                'f_val'
              618  LOAD_FAST                'sort_ind'
              620  LOAD_CONST               1
              622  LOAD_CONST               None
              624  BUILD_SLICE_2         2 
              626  BINARY_SUBSCR    
              628  BINARY_SUBSCR    
              630  LOAD_METHOD              argsort
              632  CALL_METHOD_0         0  '0 positional arguments'
              634  LOAD_CONST               1
              636  BINARY_ADD       
              638  LOAD_FAST                'sort_ind'
              640  LOAD_CONST               1
              642  LOAD_CONST               None
              644  BUILD_SLICE_2         2 
              646  STORE_SUBSCR     

 L. 269       648  LOAD_FAST                'vertices'
              650  LOAD_FAST                'best_val_idx'
              652  BINARY_SUBSCR    
              654  LOAD_FAST                'σ'
              656  LOAD_FAST                'x_bar'
              658  LOAD_FAST                'vertices'
              660  LOAD_FAST                'best_val_idx'
              662  BINARY_SUBSCR    
              664  BINARY_SUBTRACT  
              666  BINARY_MULTIPLY  
              668  BINARY_ADD       

 L. 270       670  LOAD_FAST                'vertices'
              672  LOAD_FAST                'worst_val_idx'
              674  BINARY_SUBSCR    
              676  LOAD_FAST                'vertices'
              678  LOAD_FAST                'sort_ind'
              680  LOAD_FAST                'n'
              682  BINARY_SUBSCR    
            684_0  COME_FROM           400  '400'
              684  BINARY_SUBSCR    
              686  BINARY_SUBTRACT  
              688  LOAD_FAST                'n'
              690  BINARY_TRUE_DIVIDE
              692  BINARY_ADD       
              694  STORE_FAST               'x_bar'

 L. 272       696  LOAD_FAST                'LV_ratio'
              698  LOAD_FAST                'σ_n'
              700  INPLACE_MULTIPLY 
              702  STORE_FAST               'LV_ratio'
            704_0  COME_FROM           530  '530'
            704_1  COME_FROM           418  '418'
            704_2  COME_FROM           324  '324'

 L. 274       704  LOAD_FAST                'shrink'
          706_708  POP_JUMP_IF_TRUE    838  'to 838'

 L. 275       710  LOAD_GLOBAL              _neg_bounded_fun
              712  LOAD_FAST                'fun'
              714  LOAD_FAST                'bounds'

 L. 276       716  LOAD_FAST                'vertices'
              718  LOAD_FAST                'worst_val_idx'
              720  BINARY_SUBSCR    

 L. 277       722  LOAD_FAST                'args'
              724  LOAD_CONST               ('args',)
              726  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              728  LOAD_FAST                'f_val'
              730  LOAD_FAST                'worst_val_idx'
              732  STORE_SUBSCR     

 L. 279       734  SETUP_LOOP          810  'to 810'
              736  LOAD_GLOBAL              enumerate
              738  LOAD_FAST                'sort_ind'
              740  CALL_FUNCTION_1       1  '1 positional argument'
              742  GET_ITER         
            744_0  COME_FROM           766  '766'
              744  FOR_ITER            808  'to 808'
              746  UNPACK_SEQUENCE_2     2 
              748  STORE_FAST               'i'
              750  STORE_FAST               'j'

 L. 280       752  LOAD_FAST                'f_val'
              754  LOAD_FAST                'worst_val_idx'
              756  BINARY_SUBSCR    
              758  LOAD_FAST                'f_val'
              760  LOAD_FAST                'j'
              762  BINARY_SUBSCR    
              764  COMPARE_OP               <
          766_768  POP_JUMP_IF_FALSE   744  'to 744'

 L. 281       770  LOAD_FAST                'sort_ind'
              772  LOAD_FAST                'i'
              774  LOAD_CONST               -1
              776  BUILD_SLICE_2         2 
              778  BINARY_SUBSCR    
              780  LOAD_FAST                'sort_ind'
              782  LOAD_FAST                'i'
              784  LOAD_CONST               1
              786  BINARY_ADD       
              788  LOAD_CONST               None
              790  BUILD_SLICE_2         2 
              792  STORE_SUBSCR     

 L. 282       794  LOAD_FAST                'worst_val_idx'
              796  LOAD_FAST                'sort_ind'
              798  LOAD_FAST                'i'
              800  STORE_SUBSCR     

 L. 283       802  BREAK_LOOP       
          804_806  JUMP_BACK           744  'to 744'
              808  POP_BLOCK        
            810_0  COME_FROM_LOOP      734  '734'

 L. 285       810  LOAD_FAST                'x_bar'
              812  LOAD_FAST                'vertices'
              814  LOAD_FAST                'worst_val_idx'
              816  BINARY_SUBSCR    
              818  LOAD_FAST                'vertices'
              820  LOAD_FAST                'sort_ind'
              822  LOAD_FAST                'n'
              824  BINARY_SUBSCR    
              826  BINARY_SUBSCR    
              828  BINARY_SUBTRACT  
              830  LOAD_FAST                'n'
              832  BINARY_TRUE_DIVIDE
              834  INPLACE_ADD      
              836  STORE_FAST               'x_bar'
            838_0  COME_FROM           706  '706'

 L. 287       838  LOAD_FAST                'nit'
              840  LOAD_CONST               1
              842  INPLACE_ADD      
              844  STORE_FAST               'nit'
              846  JUMP_BACK           166  'to 166'
              848  POP_BLOCK        
            850_0  COME_FROM_LOOP      162  '162'

 L. 289       850  LOAD_GLOBAL              results
              852  LOAD_FAST                'vertices'
              854  LOAD_FAST                'sort_ind'
              856  LOAD_CONST               0
              858  BINARY_SUBSCR    
              860  BINARY_SUBSCR    
              862  LOAD_FAST                'f_val'
              864  LOAD_FAST                'sort_ind'
              866  LOAD_CONST               0
              868  BINARY_SUBSCR    
              870  BINARY_SUBSCR    
              872  UNARY_NEGATIVE   
              874  LOAD_FAST                'fail'
              876  UNARY_NOT        
              878  LOAD_FAST                'nit'

 L. 290       880  LOAD_FAST                'vertices'
              882  CALL_FUNCTION_5       5  '5 positional arguments'
              884  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 684_0


@njit
def _initialize_simplex(x0, bounds):
    """
    Generates an initial simplex for the Nelder-Mead method. JIT-compiled in
    `nopython` mode using Numba.

    Parameters
    ----------
    x0 : ndarray(float, ndim=1)
        Initial guess. Array of real elements of size (n,), where ‘n’ is the
        number of independent variables.

    bounds: ndarray(float, ndim=2)
        Sequence of (min, max) pairs for each element in x0.

    Returns
    ----------
    vertices : ndarray(float, ndim=2)
        Initial simplex with shape (n+1, n).

    """
    n = x0.size
    vertices = np.empty((n + 1, n), dtype=(np.float64))
    vertices[:] = x0
    nonzdelt = 0.05
    zdelt = 0.00025
    for i in range(n):
        if vertices[(i + 1, i)] != 0.0:
            vertices[(i + 1, i)] *= 1 + nonzdelt
        else:
            vertices[(i + 1, i)] = zdelt

    return vertices


@njit
def _check_params(ρ, χ, γ, σ, bounds, n):
    """
    Checks whether the parameters for the Nelder-Mead algorithm are valid.
    JIT-compiled in `nopython` mode using Numba.

    Parameters
    ----------
    ρ : scalar(float)
        Reflection parameter. Must be strictly greater than 0.

    χ : scalar(float)
        Expansion parameter. Must be strictly greater than max(1, ρ).

    γ : scalar(float)
        Contraction parameter. Must be stricly between 0 and 1.

    σ : scalar(float)
        Shrinkage parameter. Must be strictly between 0 and 1.

    bounds: ndarray(float, ndim=2)
        Sequence of (min, max) pairs for each element in x.

    n : scalar(int)
        Number of independent variables.

    """
    if ρ < 0:
        raise ValueError('ρ must be strictly greater than 0.')
    elif χ < 1:
        raise ValueError('χ must be strictly greater than 1.')
    else:
        if χ < ρ:
            raise ValueError('χ must be strictly greater than ρ.')
        if γ < 0 or γ > 1:
            raise ValueError('γ must be strictly between 0 and 1.')
        if σ < 0 or σ > 1:
            raise ValueError('σ must be strictly between 0 and 1.')
        assert bounds.shape == (0, 2) or bounds.shape == (n, 2), 'The shape of `bounds` is not valid.'
    if (np.atleast_2d(bounds)[:, 0] > np.atleast_2d(bounds)[:, 1]).any:
        raise ValueError('Lower bounds must be greater than upper bounds.')


@njit
def _check_bounds(x, bounds):
    """
    Checks whether `x` is within `bounds`. JIT-compiled in `nopython` mode
    using Numba.

    Parameters
    ----------
    x : ndarray(float, ndim=1)
        1-D array with shape (n,) of independent variables.

    bounds: ndarray(float, ndim=2)
        Sequence of (min, max) pairs for each element in x.

    Returns
    ----------
    bool
        `True` if `x` is within `bounds`, `False` otherwise.

    """
    if bounds.shape == (0, 2):
        return True
    return (np.atleast_2d(bounds)[:, 0] <= x).all and (x <= np.atleast_2d(bounds)[:, 1]).all


@njit
def _neg_bounded_fun(fun, bounds, x, args=()):
    """
    Wrapper for bounding and taking the negative of `fun` for the
    Nelder-Mead algorithm. JIT-compiled in `nopython` mode using Numba.

    Parameters
    ----------
    fun : callable
        The objective function to be minimized.
            `fun(x, *args) -> float`
        where x is an 1-D array with shape (n,) and args is a tuple of the
        fixed parameters needed to completely specify the function. This
        function must be JIT-compiled in `nopython` mode using Numba.

    bounds: ndarray(float, ndim=2)
        Sequence of (min, max) pairs for each element in x.

    x : ndarray(float, ndim=1)
        1-D array with shape (n,) of independent variables at which `fun` is
        to be evaluated.

    args : tuple, optional
        Extra arguments passed to the objective function.

    Returns
    ----------
    scalar
        `-fun(x, *args)` if x is within `bounds`, `np.inf` otherwise.

    """
    if _check_bounds(x, bounds):
        return -fun(x, *args)
    return np.inf