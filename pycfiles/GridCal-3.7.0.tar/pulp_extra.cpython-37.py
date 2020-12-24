# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/pulp_extra.py
# Compiled at: 2019-07-27 05:38:24
# Size of source mod 2**32: 9419 bytes
"""
This file includes extensions to the PuLP library
"""
import numpy as np
from .pulp import LpProblem, LpVariable
from itertools import product
from scipy.sparse import csc_matrix

def lpDot(mat, arr):
    """
    CSC matrix-vector or CSC matrix-matrix dot product (A x b)
    :param mat: CSC sparse matrix (A)
    :param arr: dense vector or matrix of object type (b)
    :return: vector or matrix result of the product
    """
    n_rows, n_cols = mat.shape
    if not n_cols == arr.shape[0]:
        raise AssertionError
    elif mat.format == 'csc':
        mat_2 = mat
    else:
        mat_2 = csc_matrix(mat)
    if len(arr.shape) == 1:
        res = np.zeros(n_rows, dtype=(arr.dtype))
        for i in range(n_cols):
            for ii in range(mat_2.indptr[i], mat_2.indptr[(i + 1)]):
                j = mat_2.indices[ii]
                res[j] += mat_2.data[ii] * arr[i]

    else:
        cols_vec = arr.shape[1]
        res = np.zeros((n_rows, cols_vec), dtype=(arr.dtype))
        for k in range(cols_vec):
            for i in range(n_cols):
                for ii in range(mat_2.indptr[i], mat_2.indptr[(i + 1)]):
                    j = mat_2.indices[ii]
                    res[(j, k)] += mat_2.data[ii] * arr[(i, k)]

    return res


def lpAddRestrictions--- This code section failed: ---

 L.  77         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'arr'
                4  LOAD_ATTR                shape
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  LOAD_CONST               1
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    66  'to 66'

 L.  79        14  SETUP_LOOP          172  'to 172'
               16  LOAD_GLOBAL              enumerate
               18  LOAD_FAST                'arr'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  GET_ITER         
               24  FOR_ITER             62  'to 62'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'i'
               30  STORE_FAST               'elm'

 L.  80        32  LOAD_FAST                'problem'
               34  LOAD_METHOD              add
               36  LOAD_FAST                'elm'
               38  LOAD_FAST                'name'
               40  LOAD_STR                 '_'
               42  BINARY_ADD       
               44  LOAD_GLOBAL              str
               46  LOAD_FAST                'i'
               48  LOAD_CONST               1
               50  BINARY_ADD       
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  BINARY_ADD       
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  POP_TOP          
               60  JUMP_BACK            24  'to 24'
               62  POP_BLOCK        
               64  JUMP_FORWARD        172  'to 172'
             66_0  COME_FROM            12  '12'

 L.  82        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'arr'
               70  LOAD_ATTR                shape
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  LOAD_CONST               2
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   172  'to 172'

 L.  84        80  SETUP_LOOP          172  'to 172'
               82  LOAD_GLOBAL              product
               84  LOAD_GLOBAL              range
               86  LOAD_FAST                'arr'
               88  LOAD_ATTR                shape
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_GLOBAL              range
               98  LOAD_FAST                'arr'
              100  LOAD_ATTR                shape
              102  LOAD_CONST               1
              104  BINARY_SUBSCR    
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  CALL_FUNCTION_2       2  '2 positional arguments'
              110  GET_ITER         
              112  FOR_ITER            170  'to 170'
              114  UNPACK_SEQUENCE_2     2 
              116  STORE_FAST               'i'
              118  STORE_FAST               'j'

 L.  85       120  LOAD_FAST                'problem'
              122  LOAD_METHOD              add
              124  LOAD_FAST                'arr'
              126  LOAD_FAST                'i'
              128  LOAD_FAST                'j'
              130  BUILD_TUPLE_2         2 
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'name'
              136  LOAD_STR                 '_'
              138  BINARY_ADD       
              140  LOAD_GLOBAL              str
              142  LOAD_FAST                'i'
              144  LOAD_CONST               1
              146  BINARY_ADD       
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  BINARY_ADD       
              152  LOAD_STR                 '_'
              154  BINARY_ADD       
              156  LOAD_GLOBAL              str
              158  LOAD_FAST                'j'
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  BINARY_ADD       
              164  CALL_METHOD_2         2  '2 positional arguments'
              166  POP_TOP          
              168  JUMP_BACK           112  'to 112'
              170  POP_BLOCK        
            172_0  COME_FROM_LOOP       80  '80'
            172_1  COME_FROM            78  '78'
            172_2  COME_FROM            64  '64'
            172_3  COME_FROM_LOOP       14  '14'

Parse error at or near `COME_FROM' instruction at offset 172_2


def lpAddRestrictions2(problem: LpProblem, lhs, rhs, name, op='='):
    """
    Add vector or matrix of restrictions to the problem
    :param problem: instance of LpProblem
    :param lhs: 1D array (left hand side)
    :param rhs: 1D or 2D array (right hand side)
    :param name: name of the restriction    
    :param op: type of restriction (=, <=, >=)
    """
    assert lhs.shape == rhs.shape
    arr = np.empty((lhs.shape), dtype=object)
    if len(lhs.shape) == 1:
        for i in range(lhs.shape[0]):
            if op == '=':
                arr[i] = lhs[i] == rhs[i]
            else:
                if op == '<=':
                    arr[i] = lhs[i] <= rhs[i]

    else:
        if len(lhs.shape) == 2:
            for i, j in product(range(lhs.shape[0]), range(lhs.shape[1])):
                if op == '=':
                    arr[(i, j)] = lhs[(i, j)] == rhs[(i, j)]
                else:
                    if op == '<=':
                        arr[(i, j)] = lhs[(i, j)] <= rhs[(i, j)]

        lpAddRestrictions(problem=problem, arr=arr, name=name)
        return arr


def lpMakeVars--- This code section failed: ---

 L. 141         0  LOAD_GLOBAL              np
                2  LOAD_ATTR                empty
                4  LOAD_FAST                'shape'
                6  LOAD_GLOBAL              object
                8  LOAD_CONST               ('dtype',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  STORE_FAST               'var'

 L. 143        14  LOAD_GLOBAL              type
               16  LOAD_FAST                'shape'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_GLOBAL              int
               22  COMPARE_OP               ==
            24_26  POP_JUMP_IF_FALSE   616  'to 616'

 L. 145        28  LOAD_FAST                'lower'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE   100  'to 100'
               36  LOAD_FAST                'upper'
               38  LOAD_CONST               None
               40  COMPARE_OP               is-not
               42  POP_JUMP_IF_FALSE   100  'to 100'

 L. 147        44  SETUP_LOOP           96  'to 96'
               46  LOAD_GLOBAL              range
               48  LOAD_FAST                'shape'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  GET_ITER         
               54  FOR_ITER             94  'to 94'
               56  STORE_FAST               'i'

 L. 148        58  LOAD_GLOBAL              LpVariable
               60  LOAD_FAST                'name'
               62  LOAD_STR                 '_'
               64  BINARY_ADD       
               66  LOAD_GLOBAL              str
               68  LOAD_FAST                'i'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  BINARY_ADD       
               74  LOAD_CONST               None
               76  LOAD_FAST                'upper'
               78  LOAD_FAST                'i'
               80  BINARY_SUBSCR    
               82  LOAD_CONST               ('lowBound', 'upBound')
               84  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               86  LOAD_FAST                'var'
               88  LOAD_FAST                'i'
               90  STORE_SUBSCR     
               92  JUMP_BACK            54  'to 54'
               94  POP_BLOCK        
             96_0  COME_FROM_LOOP       44  '44'
            96_98  JUMP_ABSOLUTE      1986  'to 1986'
            100_0  COME_FROM            42  '42'
            100_1  COME_FROM            34  '34'

 L. 150       100  LOAD_FAST                'lower'
              102  LOAD_CONST               None
              104  COMPARE_OP               is-not
              106  POP_JUMP_IF_FALSE   234  'to 234'
              108  LOAD_FAST                'upper'
              110  LOAD_CONST               None
              112  COMPARE_OP               is
              114  POP_JUMP_IF_FALSE   234  'to 234'

 L. 152       116  LOAD_GLOBAL              type
              118  LOAD_FAST                'lower'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  LOAD_GLOBAL              int
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   178  'to 178'

 L. 153       128  SETUP_LOOP          230  'to 230'
              130  LOAD_GLOBAL              range
              132  LOAD_FAST                'shape'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  GET_ITER         
              138  FOR_ITER            174  'to 174'
              140  STORE_FAST               'i'

 L. 154       142  LOAD_GLOBAL              LpVariable
              144  LOAD_FAST                'name'
              146  LOAD_STR                 '_'
              148  BINARY_ADD       
              150  LOAD_GLOBAL              str
              152  LOAD_FAST                'i'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  BINARY_ADD       
              158  LOAD_FAST                'lower'
              160  LOAD_CONST               None
              162  LOAD_CONST               ('lowBound', 'upBound')
              164  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              166  LOAD_FAST                'var'
              168  LOAD_FAST                'i'
              170  STORE_SUBSCR     
              172  JUMP_BACK           138  'to 138'
              174  POP_BLOCK        
              176  JUMP_ABSOLUTE      1986  'to 1986'
            178_0  COME_FROM           126  '126'

 L. 156       178  SETUP_LOOP          230  'to 230'
              180  LOAD_GLOBAL              range
              182  LOAD_FAST                'shape'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  GET_ITER         
              188  FOR_ITER            228  'to 228'
              190  STORE_FAST               'i'

 L. 157       192  LOAD_GLOBAL              LpVariable
              194  LOAD_FAST                'name'
              196  LOAD_STR                 '_'
              198  BINARY_ADD       
              200  LOAD_GLOBAL              str
              202  LOAD_FAST                'i'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  BINARY_ADD       
              208  LOAD_FAST                'lower'
              210  LOAD_FAST                'i'
              212  BINARY_SUBSCR    
              214  LOAD_CONST               None
              216  LOAD_CONST               ('lowBound', 'upBound')
              218  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              220  LOAD_FAST                'var'
              222  LOAD_FAST                'i'
              224  STORE_SUBSCR     
              226  JUMP_BACK           188  'to 188'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP      178  '178'
            230_1  COME_FROM_LOOP      128  '128'
          230_232  JUMP_ABSOLUTE      1986  'to 1986'
            234_0  COME_FROM           114  '114'
            234_1  COME_FROM           106  '106'

 L. 161       234  LOAD_GLOBAL              type
              236  LOAD_FAST                'lower'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  LOAD_GLOBAL              float
              242  LOAD_GLOBAL              int
              244  BUILD_TUPLE_2         2 
              246  COMPARE_OP               in
          248_250  POP_JUMP_IF_FALSE   324  'to 324'
              252  LOAD_GLOBAL              type
              254  LOAD_FAST                'upper'
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  LOAD_GLOBAL              float
              260  LOAD_GLOBAL              int
              262  BUILD_TUPLE_2         2 
              264  COMPARE_OP               in
          266_268  POP_JUMP_IF_FALSE   324  'to 324'

 L. 162       270  SETUP_LOOP          320  'to 320'
              272  LOAD_GLOBAL              range
              274  LOAD_FAST                'shape'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  GET_ITER         
              280  FOR_ITER            318  'to 318'
              282  STORE_FAST               'i'

 L. 163       284  LOAD_GLOBAL              LpVariable
              286  LOAD_FAST                'name'
              288  LOAD_STR                 '_'
              290  BINARY_ADD       
              292  LOAD_GLOBAL              str
              294  LOAD_FAST                'i'
              296  CALL_FUNCTION_1       1  '1 positional argument'
              298  BINARY_ADD       
              300  LOAD_FAST                'lower'
              302  LOAD_FAST                'upper'
              304  LOAD_CONST               ('lowBound', 'upBound')
              306  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              308  LOAD_FAST                'var'
              310  LOAD_FAST                'i'
              312  STORE_SUBSCR     
          314_316  JUMP_BACK           280  'to 280'
              318  POP_BLOCK        
            320_0  COME_FROM_LOOP      270  '270'
          320_322  JUMP_ABSOLUTE      1986  'to 1986'
            324_0  COME_FROM           266  '266'
            324_1  COME_FROM           248  '248'

 L. 165       324  LOAD_GLOBAL              type
              326  LOAD_FAST                'lower'
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  LOAD_GLOBAL              float
              332  LOAD_GLOBAL              int
              334  BUILD_TUPLE_2         2 
              336  COMPARE_OP               not-in
          338_340  POP_JUMP_IF_FALSE   416  'to 416'
              342  LOAD_GLOBAL              type
              344  LOAD_FAST                'upper'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  LOAD_GLOBAL              float
              350  LOAD_GLOBAL              int
              352  BUILD_TUPLE_2         2 
              354  COMPARE_OP               in
          356_358  POP_JUMP_IF_FALSE   416  'to 416'

 L. 166       360  SETUP_LOOP          612  'to 612'
              362  LOAD_GLOBAL              range
              364  LOAD_FAST                'shape'
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  GET_ITER         
              370  FOR_ITER            412  'to 412'
              372  STORE_FAST               'i'

 L. 167       374  LOAD_GLOBAL              LpVariable
              376  LOAD_FAST                'name'
              378  LOAD_STR                 '_'
              380  BINARY_ADD       
              382  LOAD_GLOBAL              str
              384  LOAD_FAST                'i'
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  BINARY_ADD       
              390  LOAD_FAST                'lower'
              392  LOAD_FAST                'i'
              394  BINARY_SUBSCR    
              396  LOAD_FAST                'upper'
              398  LOAD_CONST               ('lowBound', 'upBound')
              400  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              402  LOAD_FAST                'var'
              404  LOAD_FAST                'i'
              406  STORE_SUBSCR     
          408_410  JUMP_BACK           370  'to 370'
              412  POP_BLOCK        
              414  JUMP_FORWARD       1986  'to 1986'
            416_0  COME_FROM           356  '356'
            416_1  COME_FROM           338  '338'

 L. 169       416  LOAD_GLOBAL              type
              418  LOAD_FAST                'lower'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  LOAD_GLOBAL              float
              424  LOAD_GLOBAL              int
              426  BUILD_TUPLE_2         2 
              428  COMPARE_OP               in
          430_432  POP_JUMP_IF_FALSE   508  'to 508'
              434  LOAD_GLOBAL              type
              436  LOAD_FAST                'upper'
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  LOAD_GLOBAL              float
              442  LOAD_GLOBAL              int
              444  BUILD_TUPLE_2         2 
              446  COMPARE_OP               not-in
          448_450  POP_JUMP_IF_FALSE   508  'to 508'

 L. 170       452  SETUP_LOOP          612  'to 612'
              454  LOAD_GLOBAL              range
              456  LOAD_FAST                'shape'
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  GET_ITER         
              462  FOR_ITER            504  'to 504'
              464  STORE_FAST               'i'

 L. 171       466  LOAD_GLOBAL              LpVariable
              468  LOAD_FAST                'name'
              470  LOAD_STR                 '_'
              472  BINARY_ADD       
              474  LOAD_GLOBAL              str
              476  LOAD_FAST                'i'
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  BINARY_ADD       
              482  LOAD_FAST                'lower'
              484  LOAD_FAST                'upper'
              486  LOAD_FAST                'i'
              488  BINARY_SUBSCR    
              490  LOAD_CONST               ('lowBound', 'upBound')
              492  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              494  LOAD_FAST                'var'
              496  LOAD_FAST                'i'
              498  STORE_SUBSCR     
          500_502  JUMP_BACK           462  'to 462'
              504  POP_BLOCK        
              506  JUMP_FORWARD       1986  'to 1986'
            508_0  COME_FROM           448  '448'
            508_1  COME_FROM           430  '430'

 L. 173       508  LOAD_GLOBAL              type
              510  LOAD_FAST                'lower'
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  LOAD_GLOBAL              float
              516  LOAD_GLOBAL              int
              518  BUILD_TUPLE_2         2 
              520  COMPARE_OP               not-in
          522_524  POP_JUMP_IF_FALSE   604  'to 604'
              526  LOAD_GLOBAL              type
              528  LOAD_FAST                'upper'
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  LOAD_GLOBAL              float
              534  LOAD_GLOBAL              int
              536  BUILD_TUPLE_2         2 
              538  COMPARE_OP               not-in
          540_542  POP_JUMP_IF_FALSE   604  'to 604'

 L. 174       544  SETUP_LOOP          612  'to 612'
              546  LOAD_GLOBAL              range
              548  LOAD_FAST                'shape'
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  GET_ITER         
              554  FOR_ITER            600  'to 600'
              556  STORE_FAST               'i'

 L. 175       558  LOAD_GLOBAL              LpVariable
              560  LOAD_FAST                'name'
              562  LOAD_STR                 '_'
              564  BINARY_ADD       
              566  LOAD_GLOBAL              str
              568  LOAD_FAST                'i'
              570  CALL_FUNCTION_1       1  '1 positional argument'
              572  BINARY_ADD       
              574  LOAD_FAST                'lower'
              576  LOAD_FAST                'i'
              578  BINARY_SUBSCR    
              580  LOAD_FAST                'upper'
              582  LOAD_FAST                'i'
              584  BINARY_SUBSCR    
              586  LOAD_CONST               ('lowBound', 'upBound')
              588  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              590  LOAD_FAST                'var'
              592  LOAD_FAST                'i'
              594  STORE_SUBSCR     
          596_598  JUMP_BACK           554  'to 554'
              600  POP_BLOCK        
              602  JUMP_FORWARD       1986  'to 1986'
            604_0  COME_FROM           540  '540'
            604_1  COME_FROM           522  '522'

 L. 178       604  LOAD_GLOBAL              Exception
              606  LOAD_STR                 'Cannot handle the indices...'
              608  CALL_FUNCTION_1       1  '1 positional argument'
              610  RAISE_VARARGS_1       1  'exception instance'
            612_0  COME_FROM_LOOP      544  '544'
            612_1  COME_FROM_LOOP      452  '452'
            612_2  COME_FROM_LOOP      360  '360'
          612_614  JUMP_FORWARD       1986  'to 1986'
            616_0  COME_FROM            24  '24'

 L. 182       616  LOAD_GLOBAL              len
              618  LOAD_FAST                'shape'
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  LOAD_CONST               1
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_FALSE   856  'to 856'

 L. 183       630  LOAD_FAST                'lower'
              632  LOAD_CONST               None
              634  COMPARE_OP               is
          636_638  POP_JUMP_IF_FALSE   710  'to 710'
              640  LOAD_FAST                'upper'
              642  LOAD_CONST               None
              644  COMPARE_OP               is-not
          646_648  POP_JUMP_IF_FALSE   710  'to 710'

 L. 185       650  SETUP_LOOP          852  'to 852'
              652  LOAD_GLOBAL              range
              654  LOAD_FAST                'shape'
              656  LOAD_CONST               0
              658  BINARY_SUBSCR    
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  GET_ITER         
              664  FOR_ITER            706  'to 706'
              666  STORE_FAST               'i'

 L. 186       668  LOAD_GLOBAL              LpVariable
              670  LOAD_FAST                'name'
              672  LOAD_STR                 '_'
              674  BINARY_ADD       
              676  LOAD_GLOBAL              str
              678  LOAD_FAST                'i'
              680  CALL_FUNCTION_1       1  '1 positional argument'
              682  BINARY_ADD       
              684  LOAD_CONST               None
              686  LOAD_FAST                'upper'
              688  LOAD_FAST                'i'
              690  BINARY_SUBSCR    
              692  LOAD_CONST               ('lowBound', 'upBound')
              694  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              696  LOAD_FAST                'var'
              698  LOAD_FAST                'i'
              700  STORE_SUBSCR     
          702_704  JUMP_BACK           664  'to 664'
              706  POP_BLOCK        
              708  JUMP_FORWARD       1986  'to 1986'
            710_0  COME_FROM           646  '646'
            710_1  COME_FROM           636  '636'

 L. 188       710  LOAD_FAST                'lower'
              712  LOAD_CONST               None
              714  COMPARE_OP               is-not
          716_718  POP_JUMP_IF_FALSE   790  'to 790'
              720  LOAD_FAST                'upper'
              722  LOAD_CONST               None
              724  COMPARE_OP               is
          726_728  POP_JUMP_IF_FALSE   790  'to 790'

 L. 190       730  SETUP_LOOP          852  'to 852'
              732  LOAD_GLOBAL              range
              734  LOAD_FAST                'shape'
              736  LOAD_CONST               0
              738  BINARY_SUBSCR    
              740  CALL_FUNCTION_1       1  '1 positional argument'
              742  GET_ITER         
              744  FOR_ITER            786  'to 786'
              746  STORE_FAST               'i'

 L. 191       748  LOAD_GLOBAL              LpVariable
              750  LOAD_FAST                'name'
              752  LOAD_STR                 '_'
              754  BINARY_ADD       
              756  LOAD_GLOBAL              str
              758  LOAD_FAST                'i'
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  BINARY_ADD       
              764  LOAD_FAST                'lower'
              766  LOAD_FAST                'i'
              768  BINARY_SUBSCR    
              770  LOAD_CONST               None
              772  LOAD_CONST               ('lowBound', 'upBound')
              774  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              776  LOAD_FAST                'var'
              778  LOAD_FAST                'i'
              780  STORE_SUBSCR     
          782_784  JUMP_BACK           744  'to 744'
              786  POP_BLOCK        
              788  JUMP_FORWARD       1986  'to 1986'
            790_0  COME_FROM           726  '726'
            790_1  COME_FROM           716  '716'

 L. 195       790  SETUP_LOOP          852  'to 852'
              792  LOAD_GLOBAL              range
              794  LOAD_FAST                'shape'
              796  LOAD_CONST               0
              798  BINARY_SUBSCR    
              800  CALL_FUNCTION_1       1  '1 positional argument'
              802  GET_ITER         
              804  FOR_ITER            850  'to 850'
              806  STORE_FAST               'i'

 L. 196       808  LOAD_GLOBAL              LpVariable
              810  LOAD_FAST                'name'
              812  LOAD_STR                 '_'
              814  BINARY_ADD       
              816  LOAD_GLOBAL              str
              818  LOAD_FAST                'i'
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  BINARY_ADD       
              824  LOAD_FAST                'lower'
              826  LOAD_FAST                'i'
              828  BINARY_SUBSCR    
              830  LOAD_FAST                'upper'
              832  LOAD_FAST                'i'
              834  BINARY_SUBSCR    
              836  LOAD_CONST               ('lowBound', 'upBound')
              838  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              840  LOAD_FAST                'var'
              842  LOAD_FAST                'i'
              844  STORE_SUBSCR     
          846_848  JUMP_BACK           804  'to 804'
              850  POP_BLOCK        
            852_0  COME_FROM_LOOP      790  '790'
            852_1  COME_FROM_LOOP      730  '730'
            852_2  COME_FROM_LOOP      650  '650'
          852_854  JUMP_FORWARD       1986  'to 1986'
            856_0  COME_FROM           626  '626'

 L. 198       856  LOAD_GLOBAL              len
              858  LOAD_FAST                'shape'
              860  CALL_FUNCTION_1       1  '1 positional argument'
              862  LOAD_CONST               2
              864  COMPARE_OP               ==
          866_868  POP_JUMP_IF_FALSE  1986  'to 1986'

 L. 200       870  LOAD_FAST                'lower'
              872  LOAD_CONST               None
              874  COMPARE_OP               is
          876_878  POP_JUMP_IF_FALSE  1094  'to 1094'
              880  LOAD_FAST                'upper'
              882  LOAD_CONST               None
              884  COMPARE_OP               is-not
          886_888  POP_JUMP_IF_FALSE  1094  'to 1094'

 L. 202       890  LOAD_GLOBAL              type
              892  LOAD_FAST                'upper'
              894  CALL_FUNCTION_1       1  '1 positional argument'
              896  LOAD_GLOBAL              float
              898  LOAD_GLOBAL              int
              900  BUILD_LIST_2          2 
              902  COMPARE_OP               in
          904_906  POP_JUMP_IF_FALSE   998  'to 998'

 L. 203       908  SETUP_LOOP         1090  'to 1090'
              910  LOAD_GLOBAL              product
              912  LOAD_GLOBAL              range
              914  LOAD_FAST                'shape'
              916  LOAD_CONST               0
              918  BINARY_SUBSCR    
              920  CALL_FUNCTION_1       1  '1 positional argument'
              922  LOAD_GLOBAL              range
              924  LOAD_FAST                'shape'
              926  LOAD_CONST               1
              928  BINARY_SUBSCR    
              930  CALL_FUNCTION_1       1  '1 positional argument'
              932  CALL_FUNCTION_2       2  '2 positional arguments'
              934  GET_ITER         
              936  FOR_ITER            994  'to 994'
              938  UNPACK_SEQUENCE_2     2 
              940  STORE_FAST               'i'
              942  STORE_FAST               'j'

 L. 204       944  LOAD_GLOBAL              LpVariable
              946  LOAD_FAST                'name'
              948  LOAD_STR                 '_'
              950  BINARY_ADD       
              952  LOAD_GLOBAL              str
              954  LOAD_FAST                'i'
              956  CALL_FUNCTION_1       1  '1 positional argument'
              958  BINARY_ADD       
              960  LOAD_STR                 '_'
              962  BINARY_ADD       
              964  LOAD_GLOBAL              str
              966  LOAD_FAST                'j'
              968  CALL_FUNCTION_1       1  '1 positional argument'
              970  BINARY_ADD       
              972  LOAD_CONST               None
              974  LOAD_FAST                'upper'
              976  LOAD_CONST               ('lowBound', 'upBound')
              978  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              980  LOAD_FAST                'var'
              982  LOAD_FAST                'i'
              984  LOAD_FAST                'j'
              986  BUILD_TUPLE_2         2 
              988  STORE_SUBSCR     
          990_992  JUMP_BACK           936  'to 936'
              994  POP_BLOCK        
              996  JUMP_ABSOLUTE      1986  'to 1986'
            998_0  COME_FROM           904  '904'

 L. 206       998  SETUP_LOOP         1090  'to 1090'
             1000  LOAD_GLOBAL              product
             1002  LOAD_GLOBAL              range
             1004  LOAD_FAST                'shape'
             1006  LOAD_CONST               0
             1008  BINARY_SUBSCR    
             1010  CALL_FUNCTION_1       1  '1 positional argument'
             1012  LOAD_GLOBAL              range
             1014  LOAD_FAST                'shape'
             1016  LOAD_CONST               1
             1018  BINARY_SUBSCR    
             1020  CALL_FUNCTION_1       1  '1 positional argument'
             1022  CALL_FUNCTION_2       2  '2 positional arguments'
             1024  GET_ITER         
             1026  FOR_ITER           1088  'to 1088'
             1028  UNPACK_SEQUENCE_2     2 
             1030  STORE_FAST               'i'
             1032  STORE_FAST               'j'

 L. 207      1034  LOAD_GLOBAL              LpVariable
             1036  LOAD_FAST                'name'
             1038  LOAD_STR                 '_'
             1040  BINARY_ADD       
             1042  LOAD_GLOBAL              str
             1044  LOAD_FAST                'i'
             1046  CALL_FUNCTION_1       1  '1 positional argument'
             1048  BINARY_ADD       
             1050  LOAD_STR                 '_'
             1052  BINARY_ADD       
             1054  LOAD_GLOBAL              str
             1056  LOAD_FAST                'j'
             1058  CALL_FUNCTION_1       1  '1 positional argument'
             1060  BINARY_ADD       
             1062  LOAD_CONST               None
             1064  LOAD_FAST                'upper'
             1066  LOAD_FAST                'i'
             1068  BINARY_SUBSCR    
             1070  LOAD_CONST               ('lowBound', 'upBound')
             1072  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1074  LOAD_FAST                'var'
             1076  LOAD_FAST                'i'
             1078  LOAD_FAST                'j'
             1080  BUILD_TUPLE_2         2 
             1082  STORE_SUBSCR     
         1084_1086  JUMP_BACK          1026  'to 1026'
             1088  POP_BLOCK        
           1090_0  COME_FROM_LOOP      998  '998'
           1090_1  COME_FROM_LOOP      908  '908'
         1090_1092  JUMP_ABSOLUTE      1986  'to 1986'
           1094_0  COME_FROM           886  '886'
           1094_1  COME_FROM           876  '876'

 L. 209      1094  LOAD_FAST                'lower'
             1096  LOAD_CONST               None
             1098  COMPARE_OP               is-not
         1100_1102  POP_JUMP_IF_FALSE  1318  'to 1318'
             1104  LOAD_FAST                'upper'
             1106  LOAD_CONST               None
             1108  COMPARE_OP               is
         1110_1112  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 211      1114  LOAD_GLOBAL              type
             1116  LOAD_FAST                'lower'
             1118  CALL_FUNCTION_1       1  '1 positional argument'
             1120  LOAD_GLOBAL              float
             1122  LOAD_GLOBAL              int
             1124  BUILD_LIST_2          2 
             1126  COMPARE_OP               in
         1128_1130  POP_JUMP_IF_FALSE  1222  'to 1222'

 L. 212      1132  SETUP_LOOP         1314  'to 1314'
             1134  LOAD_GLOBAL              product
             1136  LOAD_GLOBAL              range
             1138  LOAD_FAST                'shape'
             1140  LOAD_CONST               0
             1142  BINARY_SUBSCR    
             1144  CALL_FUNCTION_1       1  '1 positional argument'
             1146  LOAD_GLOBAL              range
             1148  LOAD_FAST                'shape'
             1150  LOAD_CONST               1
             1152  BINARY_SUBSCR    
             1154  CALL_FUNCTION_1       1  '1 positional argument'
             1156  CALL_FUNCTION_2       2  '2 positional arguments'
             1158  GET_ITER         
             1160  FOR_ITER           1218  'to 1218'
             1162  UNPACK_SEQUENCE_2     2 
             1164  STORE_FAST               'i'
             1166  STORE_FAST               'j'

 L. 213      1168  LOAD_GLOBAL              LpVariable
             1170  LOAD_FAST                'name'
             1172  LOAD_STR                 '_'
             1174  BINARY_ADD       
             1176  LOAD_GLOBAL              str
             1178  LOAD_FAST                'i'
             1180  CALL_FUNCTION_1       1  '1 positional argument'
             1182  BINARY_ADD       
             1184  LOAD_STR                 '_'
             1186  BINARY_ADD       
             1188  LOAD_GLOBAL              str
             1190  LOAD_FAST                'j'
             1192  CALL_FUNCTION_1       1  '1 positional argument'
             1194  BINARY_ADD       
             1196  LOAD_FAST                'lower'
             1198  LOAD_CONST               None
             1200  LOAD_CONST               ('lowBound', 'upBound')
             1202  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1204  LOAD_FAST                'var'
             1206  LOAD_FAST                'i'
             1208  LOAD_FAST                'j'
             1210  BUILD_TUPLE_2         2 
             1212  STORE_SUBSCR     
         1214_1216  JUMP_BACK          1160  'to 1160'
             1218  POP_BLOCK        
             1220  JUMP_ABSOLUTE      1986  'to 1986'
           1222_0  COME_FROM          1128  '1128'

 L. 215      1222  SETUP_LOOP         1314  'to 1314'
             1224  LOAD_GLOBAL              product
             1226  LOAD_GLOBAL              range
             1228  LOAD_FAST                'shape'
             1230  LOAD_CONST               0
             1232  BINARY_SUBSCR    
             1234  CALL_FUNCTION_1       1  '1 positional argument'
             1236  LOAD_GLOBAL              range
             1238  LOAD_FAST                'shape'
             1240  LOAD_CONST               1
             1242  BINARY_SUBSCR    
             1244  CALL_FUNCTION_1       1  '1 positional argument'
             1246  CALL_FUNCTION_2       2  '2 positional arguments'
             1248  GET_ITER         
             1250  FOR_ITER           1312  'to 1312'
             1252  UNPACK_SEQUENCE_2     2 
             1254  STORE_FAST               'i'
             1256  STORE_FAST               'j'

 L. 216      1258  LOAD_GLOBAL              LpVariable
             1260  LOAD_FAST                'name'
             1262  LOAD_STR                 '_'
             1264  BINARY_ADD       
             1266  LOAD_GLOBAL              str
             1268  LOAD_FAST                'i'
             1270  CALL_FUNCTION_1       1  '1 positional argument'
             1272  BINARY_ADD       
             1274  LOAD_STR                 '_'
             1276  BINARY_ADD       
             1278  LOAD_GLOBAL              str
             1280  LOAD_FAST                'j'
             1282  CALL_FUNCTION_1       1  '1 positional argument'
             1284  BINARY_ADD       
             1286  LOAD_FAST                'lower'
             1288  LOAD_FAST                'i'
             1290  BINARY_SUBSCR    
             1292  LOAD_CONST               None
             1294  LOAD_CONST               ('lowBound', 'upBound')
             1296  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1298  LOAD_FAST                'var'
             1300  LOAD_FAST                'i'
             1302  LOAD_FAST                'j'
             1304  BUILD_TUPLE_2         2 
             1306  STORE_SUBSCR     
         1308_1310  JUMP_BACK          1250  'to 1250'
             1312  POP_BLOCK        
           1314_0  COME_FROM_LOOP     1222  '1222'
           1314_1  COME_FROM_LOOP     1132  '1132'
         1314_1316  JUMP_ABSOLUTE      1986  'to 1986'
           1318_0  COME_FROM          1110  '1110'
           1318_1  COME_FROM          1100  '1100'

 L. 220      1318  LOAD_GLOBAL              type
             1320  LOAD_FAST                'lower'
             1322  CALL_FUNCTION_1       1  '1 positional argument'
             1324  LOAD_GLOBAL              float
             1326  LOAD_GLOBAL              int
             1328  BUILD_LIST_2          2 
             1330  COMPARE_OP               in
         1332_1334  POP_JUMP_IF_FALSE  1446  'to 1446'
             1336  LOAD_GLOBAL              type
             1338  LOAD_FAST                'upper'
             1340  CALL_FUNCTION_1       1  '1 positional argument'
             1342  LOAD_GLOBAL              float
             1344  LOAD_GLOBAL              int
             1346  BUILD_LIST_2          2 
             1348  COMPARE_OP               in
         1350_1352  POP_JUMP_IF_FALSE  1446  'to 1446'

 L. 221      1354  SETUP_LOOP         1442  'to 1442'
             1356  LOAD_GLOBAL              product
             1358  LOAD_GLOBAL              range
             1360  LOAD_FAST                'shape'
             1362  LOAD_CONST               0
             1364  BINARY_SUBSCR    
             1366  CALL_FUNCTION_1       1  '1 positional argument'
             1368  LOAD_GLOBAL              range
             1370  LOAD_FAST                'shape'
             1372  LOAD_CONST               1
             1374  BINARY_SUBSCR    
             1376  CALL_FUNCTION_1       1  '1 positional argument'
             1378  CALL_FUNCTION_2       2  '2 positional arguments'
             1380  GET_ITER         
             1382  FOR_ITER           1440  'to 1440'
             1384  UNPACK_SEQUENCE_2     2 
             1386  STORE_FAST               'i'
             1388  STORE_FAST               'j'

 L. 222      1390  LOAD_GLOBAL              LpVariable
             1392  LOAD_FAST                'name'
             1394  LOAD_STR                 '_'
             1396  BINARY_ADD       
             1398  LOAD_GLOBAL              str
             1400  LOAD_FAST                'i'
             1402  CALL_FUNCTION_1       1  '1 positional argument'
             1404  BINARY_ADD       
             1406  LOAD_STR                 '_'
             1408  BINARY_ADD       
             1410  LOAD_GLOBAL              str
             1412  LOAD_FAST                'j'
             1414  CALL_FUNCTION_1       1  '1 positional argument'
             1416  BINARY_ADD       
             1418  LOAD_FAST                'lower'
             1420  LOAD_FAST                'upper'
             1422  LOAD_CONST               ('lowBound', 'upBound')
             1424  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1426  LOAD_FAST                'var'
             1428  LOAD_FAST                'i'
             1430  LOAD_FAST                'j'
             1432  BUILD_TUPLE_2         2 
             1434  STORE_SUBSCR     
         1436_1438  JUMP_BACK          1382  'to 1382'
             1440  POP_BLOCK        
           1442_0  COME_FROM_LOOP     1354  '1354'
         1442_1444  JUMP_ABSOLUTE      1986  'to 1986'
           1446_0  COME_FROM          1350  '1350'
           1446_1  COME_FROM          1332  '1332'

 L. 224      1446  LOAD_GLOBAL              len
             1448  LOAD_FAST                'lower'
             1450  LOAD_ATTR                shape
             1452  CALL_FUNCTION_1       1  '1 positional argument'
             1454  LOAD_CONST               2
             1456  COMPARE_OP               ==
         1458_1460  POP_JUMP_IF_FALSE  1586  'to 1586'
             1462  LOAD_GLOBAL              len
             1464  LOAD_FAST                'lower'
             1466  LOAD_ATTR                shape
             1468  CALL_FUNCTION_1       1  '1 positional argument'
             1470  LOAD_CONST               2
             1472  COMPARE_OP               ==
         1474_1476  POP_JUMP_IF_FALSE  1586  'to 1586'

 L. 225      1478  SETUP_LOOP         1582  'to 1582'
             1480  LOAD_GLOBAL              product
             1482  LOAD_GLOBAL              range
             1484  LOAD_FAST                'shape'
             1486  LOAD_CONST               0
             1488  BINARY_SUBSCR    
             1490  CALL_FUNCTION_1       1  '1 positional argument'
             1492  LOAD_GLOBAL              range
             1494  LOAD_FAST                'shape'
             1496  LOAD_CONST               1
             1498  BINARY_SUBSCR    
             1500  CALL_FUNCTION_1       1  '1 positional argument'
             1502  CALL_FUNCTION_2       2  '2 positional arguments'
             1504  GET_ITER         
             1506  FOR_ITER           1580  'to 1580'
             1508  UNPACK_SEQUENCE_2     2 
             1510  STORE_FAST               'i'
             1512  STORE_FAST               'j'

 L. 226      1514  LOAD_GLOBAL              LpVariable
             1516  LOAD_FAST                'name'
             1518  LOAD_STR                 '_'
             1520  BINARY_ADD       
             1522  LOAD_GLOBAL              str
             1524  LOAD_FAST                'i'
             1526  CALL_FUNCTION_1       1  '1 positional argument'
             1528  BINARY_ADD       
             1530  LOAD_STR                 '_'
             1532  BINARY_ADD       
             1534  LOAD_GLOBAL              str
             1536  LOAD_FAST                'j'
             1538  CALL_FUNCTION_1       1  '1 positional argument'
             1540  BINARY_ADD       
             1542  LOAD_FAST                'lower'
             1544  LOAD_FAST                'i'
             1546  LOAD_FAST                'j'
             1548  BUILD_TUPLE_2         2 
             1550  BINARY_SUBSCR    
             1552  LOAD_FAST                'upper'
             1554  LOAD_FAST                'i'
             1556  LOAD_FAST                'j'
             1558  BUILD_TUPLE_2         2 
             1560  BINARY_SUBSCR    
             1562  LOAD_CONST               ('lowBound', 'upBound')
             1564  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1566  LOAD_FAST                'var'
             1568  LOAD_FAST                'i'
             1570  LOAD_FAST                'j'
             1572  BUILD_TUPLE_2         2 
             1574  STORE_SUBSCR     
         1576_1578  JUMP_BACK          1506  'to 1506'
             1580  POP_BLOCK        
           1582_0  COME_FROM_LOOP     1478  '1478'
         1582_1584  JUMP_ABSOLUTE      1986  'to 1986'
           1586_0  COME_FROM          1474  '1474'
           1586_1  COME_FROM          1458  '1458'

 L. 228      1586  LOAD_GLOBAL              len
             1588  LOAD_FAST                'lower'
             1590  LOAD_ATTR                shape
             1592  CALL_FUNCTION_1       1  '1 positional argument'
             1594  LOAD_CONST               1
             1596  COMPARE_OP               ==
         1598_1600  POP_JUMP_IF_FALSE  1722  'to 1722'
             1602  LOAD_GLOBAL              len
             1604  LOAD_FAST                'lower'
             1606  LOAD_ATTR                shape
             1608  CALL_FUNCTION_1       1  '1 positional argument'
             1610  LOAD_CONST               2
             1612  COMPARE_OP               ==
         1614_1616  POP_JUMP_IF_FALSE  1722  'to 1722'

 L. 229      1618  SETUP_LOOP         1718  'to 1718'
             1620  LOAD_GLOBAL              product
             1622  LOAD_GLOBAL              range
             1624  LOAD_FAST                'shape'
             1626  LOAD_CONST               0
             1628  BINARY_SUBSCR    
             1630  CALL_FUNCTION_1       1  '1 positional argument'
             1632  LOAD_GLOBAL              range
             1634  LOAD_FAST                'shape'
             1636  LOAD_CONST               1
             1638  BINARY_SUBSCR    
             1640  CALL_FUNCTION_1       1  '1 positional argument'
             1642  CALL_FUNCTION_2       2  '2 positional arguments'
             1644  GET_ITER         
             1646  FOR_ITER           1716  'to 1716'
             1648  UNPACK_SEQUENCE_2     2 
             1650  STORE_FAST               'i'
             1652  STORE_FAST               'j'

 L. 230      1654  LOAD_GLOBAL              LpVariable
             1656  LOAD_FAST                'name'
             1658  LOAD_STR                 '_'
             1660  BINARY_ADD       
             1662  LOAD_GLOBAL              str
             1664  LOAD_FAST                'i'
             1666  CALL_FUNCTION_1       1  '1 positional argument'
             1668  BINARY_ADD       
             1670  LOAD_STR                 '_'
             1672  BINARY_ADD       
             1674  LOAD_GLOBAL              str
             1676  LOAD_FAST                'j'
             1678  CALL_FUNCTION_1       1  '1 positional argument'
             1680  BINARY_ADD       
             1682  LOAD_FAST                'lower'
             1684  LOAD_FAST                'i'
             1686  BINARY_SUBSCR    
             1688  LOAD_FAST                'upper'
             1690  LOAD_FAST                'i'
             1692  LOAD_FAST                'j'
             1694  BUILD_TUPLE_2         2 
             1696  BINARY_SUBSCR    
             1698  LOAD_CONST               ('lowBound', 'upBound')
             1700  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1702  LOAD_FAST                'var'
             1704  LOAD_FAST                'i'
             1706  LOAD_FAST                'j'
             1708  BUILD_TUPLE_2         2 
             1710  STORE_SUBSCR     
         1712_1714  JUMP_BACK          1646  'to 1646'
             1716  POP_BLOCK        
           1718_0  COME_FROM_LOOP     1618  '1618'
         1718_1720  JUMP_ABSOLUTE      1986  'to 1986'
           1722_0  COME_FROM          1614  '1614'
           1722_1  COME_FROM          1598  '1598'

 L. 232      1722  LOAD_GLOBAL              len
             1724  LOAD_FAST                'lower'
             1726  LOAD_ATTR                shape
             1728  CALL_FUNCTION_1       1  '1 positional argument'
             1730  LOAD_CONST               2
             1732  COMPARE_OP               ==
         1734_1736  POP_JUMP_IF_FALSE  1856  'to 1856'
             1738  LOAD_GLOBAL              len
             1740  LOAD_FAST                'lower'
             1742  LOAD_ATTR                shape
             1744  CALL_FUNCTION_1       1  '1 positional argument'
             1746  LOAD_CONST               1
             1748  COMPARE_OP               ==
         1750_1752  POP_JUMP_IF_FALSE  1856  'to 1856'

 L. 233      1754  SETUP_LOOP         1984  'to 1984'
             1756  LOAD_GLOBAL              product
             1758  LOAD_GLOBAL              range
             1760  LOAD_FAST                'shape'
             1762  LOAD_CONST               0
             1764  BINARY_SUBSCR    
             1766  CALL_FUNCTION_1       1  '1 positional argument'
             1768  LOAD_GLOBAL              range
             1770  LOAD_FAST                'shape'
             1772  LOAD_CONST               1
             1774  BINARY_SUBSCR    
             1776  CALL_FUNCTION_1       1  '1 positional argument'
             1778  CALL_FUNCTION_2       2  '2 positional arguments'
             1780  GET_ITER         
             1782  FOR_ITER           1852  'to 1852'
             1784  UNPACK_SEQUENCE_2     2 
           1786_0  COME_FROM           414  '414'
             1786  STORE_FAST               'i'
             1788  STORE_FAST               'j'

 L. 234      1790  LOAD_GLOBAL              LpVariable
             1792  LOAD_FAST                'name'
             1794  LOAD_STR                 '_'
             1796  BINARY_ADD       
             1798  LOAD_GLOBAL              str
             1800  LOAD_FAST                'i'
             1802  CALL_FUNCTION_1       1  '1 positional argument'
             1804  BINARY_ADD       
             1806  LOAD_STR                 '_'
             1808  BINARY_ADD       
             1810  LOAD_GLOBAL              str
             1812  LOAD_FAST                'j'
             1814  CALL_FUNCTION_1       1  '1 positional argument'
             1816  BINARY_ADD       
             1818  LOAD_FAST                'lower'
             1820  LOAD_FAST                'i'
             1822  LOAD_FAST                'j'
             1824  BUILD_TUPLE_2         2 
             1826  BINARY_SUBSCR    
             1828  LOAD_FAST                'upper'
             1830  LOAD_FAST                'i'
             1832  BINARY_SUBSCR    
             1834  LOAD_CONST               ('lowBound', 'upBound')
             1836  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1838  LOAD_FAST                'var'
           1840_0  COME_FROM           708  '708'
             1840  LOAD_FAST                'i'
             1842  LOAD_FAST                'j'
             1844  BUILD_TUPLE_2         2 
             1846  STORE_SUBSCR     
         1848_1850  JUMP_BACK          1782  'to 1782'
             1852  POP_BLOCK        
             1854  JUMP_FORWARD       1984  'to 1984'
           1856_0  COME_FROM          1750  '1750'
           1856_1  COME_FROM          1734  '1734'

 L. 236      1856  LOAD_GLOBAL              len
             1858  LOAD_FAST                'lower'
             1860  LOAD_ATTR                shape
             1862  CALL_FUNCTION_1       1  '1 positional argument'
             1864  LOAD_CONST               1
             1866  COMPARE_OP               ==
         1868_1870  POP_JUMP_IF_FALSE  1986  'to 1986'
             1872  LOAD_GLOBAL              len
             1874  LOAD_FAST                'lower'
             1876  LOAD_ATTR                shape
           1878_0  COME_FROM           506  '506'
             1878  CALL_FUNCTION_1       1  '1 positional argument'
             1880  LOAD_CONST               1
             1882  COMPARE_OP               ==
         1884_1886  POP_JUMP_IF_FALSE  1986  'to 1986'

 L. 237      1888  SETUP_LOOP         1986  'to 1986'
             1890  LOAD_GLOBAL              product
             1892  LOAD_GLOBAL              range
             1894  LOAD_FAST                'shape'
             1896  LOAD_CONST               0
             1898  BINARY_SUBSCR    
             1900  CALL_FUNCTION_1       1  '1 positional argument'
             1902  LOAD_GLOBAL              range
             1904  LOAD_FAST                'shape'
             1906  LOAD_CONST               1
             1908  BINARY_SUBSCR    
             1910  CALL_FUNCTION_1       1  '1 positional argument'
             1912  CALL_FUNCTION_2       2  '2 positional arguments'
             1914  GET_ITER         
             1916  FOR_ITER           1982  'to 1982'
             1918  UNPACK_SEQUENCE_2     2 
           1920_0  COME_FROM           788  '788'
             1920  STORE_FAST               'i'
             1922  STORE_FAST               'j'

 L. 238      1924  LOAD_GLOBAL              LpVariable
             1926  LOAD_FAST                'name'
             1928  LOAD_STR                 '_'
             1930  BINARY_ADD       
             1932  LOAD_GLOBAL              str
             1934  LOAD_FAST                'i'
             1936  CALL_FUNCTION_1       1  '1 positional argument'
             1938  BINARY_ADD       
             1940  LOAD_STR                 '_'
             1942  BINARY_ADD       
             1944  LOAD_GLOBAL              str
             1946  LOAD_FAST                'j'
             1948  CALL_FUNCTION_1       1  '1 positional argument'
             1950  BINARY_ADD       
             1952  LOAD_FAST                'lower'
             1954  LOAD_FAST                'i'
             1956  BINARY_SUBSCR    
             1958  LOAD_FAST                'upper'
             1960  LOAD_FAST                'i'
             1962  BINARY_SUBSCR    
             1964  LOAD_CONST               ('lowBound', 'upBound')
             1966  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1968  LOAD_FAST                'var'
             1970  LOAD_FAST                'i'
             1972  LOAD_FAST                'j'
           1974_0  COME_FROM           602  '602'
             1974  BUILD_TUPLE_2         2 
             1976  STORE_SUBSCR     
         1978_1980  JUMP_BACK          1916  'to 1916'
             1982  POP_BLOCK        
           1984_0  COME_FROM_LOOP     1888  '1888'
           1984_1  COME_FROM          1854  '1854'
           1984_2  COME_FROM_LOOP     1754  '1754'
             1984  JUMP_FORWARD       1986  'to 1986'
           1986_0  COME_FROM          1984  '1984'
           1986_1  COME_FROM          1884  '1884'
           1986_2  COME_FROM          1868  '1868'
           1986_3  COME_FROM           866  '866'
           1986_4  COME_FROM           852  '852'
           1986_5  COME_FROM           612  '612'

 L. 242      1986  LOAD_FAST                'var'
             1988  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 230_1


def lpGet2D(arr, make_abs=False):
    """
    Extract values fro the 2D array of LP variables
    :param arr: 2D array of LP variables
    :param make_abs: substitute the result by its abs value
    :return: 2D numpy array
    """
    val = np.zeros(arr.shape)
    for i, j in product(range(val.shape[0]), range(val.shape[1])):
        val[(i, j)] = arr[(i, j)].value()

    if make_abs:
        val = np.abs(val)
    return val