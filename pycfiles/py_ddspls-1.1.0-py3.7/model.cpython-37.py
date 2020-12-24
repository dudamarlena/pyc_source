# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_ddspls\model.py
# Compiled at: 2019-02-21 10:15:11
# Size of source mod 2**32: 27395 bytes
"""
        The model module
        ================

"""

def f(x):
    return x * x


import numpy as np
from pandas import get_dummies
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
import importlib
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import preprocessing
import random as rd
from itertools import product as itertools_product

def getResult(dic):
    Xs = dic['Xs']
    Y = dic['Y']
    q = dic['q']
    mode = dic['mode']
    maxIter_imput = dic['maxIter_imput']
    errMin_imput = dic['errMin_imput']
    paras = dic['paras']
    decoupe = dic['decoupe']
    pos_decoupe = dic['pos_decoupe']
    fold = dic['fold']
    K = len(Xs)
    paras_here_pos = np.where(np.array(decoupe) == pos_decoupe)[0]
    l_p_h = len(paras_here_pos)
    if mode == 'reg':
        errors = np.zeros((l_p_h, q))
        select_y = np.zeros((l_p_h, q))
    else:
        errors = []
        select_y = None
    for i in range(l_p_h):
        R = paras[0][paras_here_pos[i]]
        lambd = paras[1][paras_here_pos[i]]
        i_fold = paras[2][paras_here_pos[i]]
        pos_test = np.where(np.array(fold) == i_fold)[0]
        pos_train = np.where(np.array(fold) != i_fold)[0]
        X_train = {}
        X_test = {}
        for k in range(K):
            X_train[k] = Xs[k][pos_train, :]
            X_test[k] = Xs[k][pos_test, :]

        if mode == 'reg':
            Y_train = Y[pos_train, :]
            Y_test = Y[pos_test, :]
        else:
            Y_train = Y[pos_train]
            Y_test = Y[pos_test]
        mod_0 = ddspls(Xs=X_train, Y=Y_train, lambd=lambd, R=R, mode=mode, errMin_imput=errMin_imput,
          maxIter_imput=maxIter_imput)
        Y_est = mod_0.predict(X_test)
        if mode == 'reg':
            error_here = Y_est - Y_test
            errors[i, :] = np.sqrt(np.sum((error_here * error_here), axis=0) / len(pos_test))
            v_no_null = np.where(np.sum((abs(mod_0.model.v)), axis=0) > 1e-10)
            select_y[(i, v_no_null)] < -1
        else:
            numer = float(len([ii for ii, v in enumerate(Y_test) if Y_est[ii] == v]))
            denom = float(len(Y_test))
            errors.append(1.0 - numer / denom)

    if mode == 'reg':
        out = {'RMSE':errors, 
         'v_no_null':v_no_null,  'select_y':select_y}
    else:
        out = errors
    return out


def reshape_dict(Xs_top):
    test_matrix = type(Xs_top) == np.ndarray
    if test_matrix:
        if len(Xs_top.shape) != 0:
            Xs_w_resh = {}
            Xs_w_resh[0] = Xs_top
        else:
            Xs_w_resh = Xs_top
    else:
        Xs_w_resh = Xs_top
    K = len(Xs_w_resh)
    how_much_dim = []
    min_dim = []
    for k in range(K):
        dim_k = Xs_w_resh[k].shape
        if len(dim_k) == 0:
            dim_k_0 = 1
            dim_k = dim_k_0
            min_dim.append(dim_k)
            how_much_dim.append(1)
        else:
            how_much_dim.append(2)
            min_dim.append(min(dim_k))

    if max(how_much_dim) == 1:
        for k in range(K):
            Xs_here = np.zeros((1, min_dim[k]))
            Xs_here[0, :] = Xs_w_resh[k]
            Xs_w_resh[k] = Xs_here

    else:
        for k in range(K):
            if how_much_dim[k] == 1:
                Xs_here = np.zeros((Xs_w_resh[k].shape[0], 1))
                Xs_here[:, 0] = Xs_w_resh[k]
                Xs_w_resh[k] = Xs_here

    return Xs_w_resh


def MddsPLS_core--- This code section failed: ---

 L. 117         0  LOAD_GLOBAL              reshape_dict
                2  LOAD_FAST                'Xs'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'Xs_w'

 L. 118         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'Xs_w'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  STORE_FAST               'K'

 L. 119        16  LOAD_FAST                'Xs_w'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_ATTR                shape
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  STORE_FAST               'n'

 L. 121        30  BUILD_MAP_0           0 
               32  STORE_FAST               'mu_x_s'

 L. 122        34  BUILD_MAP_0           0 
               36  STORE_FAST               'sd_x_s'

 L. 123        38  BUILD_MAP_0           0 
               40  STORE_FAST               'pos_nas'

 L. 124        42  LOAD_GLOBAL              np
               44  LOAD_METHOD              repeat
               46  LOAD_CONST               0
               48  LOAD_FAST                'K'
               50  CALL_METHOD_2         2  '2 positional arguments'
               52  STORE_FAST               'p_s'

 L. 125     54_56  SETUP_LOOP          488  'to 488'
               58  LOAD_GLOBAL              range
               60  LOAD_FAST                'K'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  GET_ITER         
             66_0  COME_FROM           300  '300'
            66_68  FOR_ITER            486  'to 486'
               70  STORE_FAST               'i'

 L. 126        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'Xs_w'
               76  LOAD_FAST                'i'
               78  BINARY_SUBSCR    
               80  LOAD_ATTR                shape
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  LOAD_CONST               2
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L. 127        90  LOAD_FAST                'Xs_w'
               92  LOAD_FAST                'i'
               94  BINARY_SUBSCR    
               96  LOAD_METHOD              to_frame
               98  CALL_METHOD_0         0  '0 positional arguments'
              100  LOAD_FAST                'Xs_w'
              102  LOAD_FAST                'i'
              104  STORE_SUBSCR     
            106_0  COME_FROM            88  '88'

 L. 128       106  LOAD_FAST                'Xs_w'
              108  LOAD_FAST                'i'
              110  BINARY_SUBSCR    
              112  LOAD_ATTR                shape
              114  LOAD_CONST               1
              116  BINARY_SUBSCR    
              118  STORE_FAST               'p_i'

 L. 129       120  LOAD_FAST                'p_i'
              122  LOAD_FAST                'p_s'
              124  LOAD_FAST                'i'
              126  STORE_SUBSCR     

 L. 130       128  LOAD_FAST                'Xs_w'
              130  LOAD_FAST                'i'
              132  BINARY_SUBSCR    
              134  LOAD_METHOD              mean
              136  LOAD_CONST               0
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_FAST                'mu_x_s'
              142  LOAD_FAST                'i'
              144  STORE_SUBSCR     

 L. 131       146  LOAD_FAST                'Xs_w'
              148  LOAD_FAST                'i'
              150  BINARY_SUBSCR    
              152  LOAD_METHOD              std
              154  LOAD_CONST               0
              156  CALL_METHOD_1         1  '1 positional argument'
              158  LOAD_FAST                'sd_x_s'
              160  LOAD_FAST                'i'
              162  STORE_SUBSCR     

 L. 132       164  LOAD_GLOBAL              np
              166  LOAD_METHOD              where
              168  LOAD_GLOBAL              np
              170  LOAD_METHOD              isnan
              172  LOAD_FAST                'Xs_w'
              174  LOAD_FAST                'i'
              176  BINARY_SUBSCR    
              178  LOAD_CONST               None
              180  LOAD_CONST               None
              182  BUILD_SLICE_2         2 
              184  LOAD_CONST               0
              186  BUILD_TUPLE_2         2 
              188  BINARY_SUBSCR    
              190  CALL_METHOD_1         1  '1 positional argument'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'pos_nas'
              200  LOAD_FAST                'i'
              202  STORE_SUBSCR     

 L. 133       204  LOAD_GLOBAL              np
              206  LOAD_METHOD              where
              208  LOAD_GLOBAL              np
              210  LOAD_METHOD              isnan
              212  LOAD_FAST                'Xs_w'
              214  LOAD_FAST                'i'
              216  BINARY_SUBSCR    
              218  LOAD_CONST               None
              220  LOAD_CONST               None
              222  BUILD_SLICE_2         2 
              224  LOAD_CONST               0
              226  BUILD_TUPLE_2         2 
              228  BINARY_SUBSCR    
              230  CALL_METHOD_1         1  '1 positional argument'
              232  LOAD_CONST               False
              234  COMPARE_OP               ==
              236  CALL_METHOD_1         1  '1 positional argument'
              238  LOAD_CONST               0
              240  BINARY_SUBSCR    
              242  STORE_FAST               'pos_no_na'

 L. 134       244  LOAD_GLOBAL              preprocessing
              246  LOAD_METHOD              scale
              248  LOAD_FAST                'Xs_w'
              250  LOAD_FAST                'i'
              252  BINARY_SUBSCR    
              254  LOAD_FAST                'pos_no_na'
              256  LOAD_CONST               None
              258  LOAD_CONST               None
              260  BUILD_SLICE_2         2 
              262  BUILD_TUPLE_2         2 
              264  BINARY_SUBSCR    
              266  CALL_METHOD_1         1  '1 positional argument'
              268  LOAD_FAST                'Xs_w'
              270  LOAD_FAST                'i'
              272  BINARY_SUBSCR    
              274  LOAD_FAST                'pos_no_na'
              276  LOAD_CONST               None
              278  LOAD_CONST               None
              280  BUILD_SLICE_2         2 
              282  BUILD_TUPLE_2         2 
              284  STORE_SUBSCR     

 L. 135       286  LOAD_GLOBAL              len
              288  LOAD_FAST                'pos_nas'
              290  LOAD_FAST                'i'
              292  BINARY_SUBSCR    
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  LOAD_CONST               0
              298  COMPARE_OP               !=
              300  POP_JUMP_IF_FALSE    66  'to 66'

 L. 139       302  LOAD_GLOBAL              np
              304  LOAD_METHOD              delete
              306  LOAD_FAST                'Xs_w'
              308  LOAD_FAST                'i'
              310  BINARY_SUBSCR    
              312  LOAD_FAST                'pos_nas'
              314  LOAD_FAST                'i'
              316  BINARY_SUBSCR    
              318  LOAD_CONST               0
              320  CALL_METHOD_3         3  '3 positional arguments'
              322  STORE_FAST               'y_i_train'

 L. 140       324  LOAD_FAST                'mode'
              326  LOAD_STR                 'reg'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   376  'to 376'

 L. 141       334  LOAD_CONST               0
              336  LOAD_GLOBAL              np
              338  LOAD_METHOD              delete
              340  LOAD_FAST                'Y'
              342  LOAD_FAST                'pos_nas'
              344  LOAD_FAST                'i'
              346  BINARY_SUBSCR    
              348  LOAD_CONST               0
              350  CALL_METHOD_3         3  '3 positional arguments'
              352  BUILD_MAP_1           1 
              354  STORE_FAST               'x_train'

 L. 142       356  LOAD_CONST               0
              358  LOAD_GLOBAL              np
              360  LOAD_METHOD              delete
              362  LOAD_FAST                'Y'
              364  LOAD_FAST                'pos_no_na'
              366  LOAD_CONST               0
              368  CALL_METHOD_3         3  '3 positional arguments'
              370  BUILD_MAP_1           1 
              372  STORE_FAST               'x_test'
              374  JUMP_FORWARD        434  'to 434'
            376_0  COME_FROM           330  '330'

 L. 144       376  LOAD_GLOBAL              preprocessing
              378  LOAD_METHOD              scale
              380  LOAD_GLOBAL              get_dummies
              382  LOAD_FAST                'Y'
              384  CALL_FUNCTION_1       1  '1 positional argument'
              386  LOAD_CONST               1.0
              388  BINARY_MULTIPLY  
              390  CALL_METHOD_1         1  '1 positional argument'
              392  STORE_FAST               'Y_w'

 L. 145       394  LOAD_CONST               0
              396  LOAD_GLOBAL              np
              398  LOAD_METHOD              delete
              400  LOAD_FAST                'Y_w'
              402  LOAD_FAST                'pos_nas'
              404  LOAD_FAST                'i'
              406  BINARY_SUBSCR    
              408  LOAD_CONST               0
              410  CALL_METHOD_3         3  '3 positional arguments'
              412  BUILD_MAP_1           1 
              414  STORE_FAST               'x_train'

 L. 146       416  LOAD_CONST               0
              418  LOAD_GLOBAL              np
              420  LOAD_METHOD              delete
              422  LOAD_FAST                'Y_w'
              424  LOAD_FAST                'pos_no_na'
              426  LOAD_CONST               0
              428  CALL_METHOD_3         3  '3 positional arguments'
              430  BUILD_MAP_1           1 
              432  STORE_FAST               'x_test'
            434_0  COME_FROM           374  '374'

 L. 147       434  LOAD_GLOBAL              ddspls
              436  LOAD_FAST                'x_train'
              438  LOAD_FAST                'y_i_train'
              440  LOAD_FAST                'R'
              442  LOAD_FAST                'lambd'
              444  LOAD_CONST               ('R', 'lambd')
              446  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              448  STORE_FAST               'model_init'

 L. 148       450  LOAD_FAST                'model_init'
              452  LOAD_METHOD              predict
              454  LOAD_FAST                'x_test'
              456  CALL_METHOD_1         1  '1 positional argument'
              458  STORE_FAST               'y_test'

 L. 149       460  LOAD_FAST                'y_test'
              462  LOAD_FAST                'Xs_w'
              464  LOAD_FAST                'i'
              466  BINARY_SUBSCR    
              468  LOAD_FAST                'pos_nas'
              470  LOAD_FAST                'i'
              472  BINARY_SUBSCR    
              474  LOAD_CONST               None
              476  LOAD_CONST               None
              478  BUILD_SLICE_2         2 
              480  BUILD_TUPLE_2         2 
              482  STORE_SUBSCR     
              484  JUMP_BACK            66  'to 66'
              486  POP_BLOCK        
            488_0  COME_FROM_LOOP       54  '54'

 L. 151       488  LOAD_FAST                'mode'
              490  LOAD_STR                 'reg'
              492  COMPARE_OP               !=
          494_496  POP_JUMP_IF_FALSE   508  'to 508'

 L. 152       498  LOAD_GLOBAL              get_dummies
              500  LOAD_FAST                'Y'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  STORE_FAST               'Y_w'
              506  JUMP_FORWARD        520  'to 520'
            508_0  COME_FROM           494  '494'

 L. 154       508  LOAD_GLOBAL              reshape_dict
              510  LOAD_FAST                'Y'
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  LOAD_CONST               0
              516  BINARY_SUBSCR    
              518  STORE_FAST               'Y_w'
            520_0  COME_FROM           506  '506'

 L. 155       520  LOAD_FAST                'Y_w'
              522  LOAD_ATTR                shape
              524  LOAD_CONST               1
              526  BINARY_SUBSCR    
              528  STORE_FAST               'q'

 L. 156       530  LOAD_FAST                'Y_w'
              532  LOAD_METHOD              mean
              534  LOAD_CONST               0
              536  CALL_METHOD_1         1  '1 positional argument'
              538  STORE_FAST               'mu_y'

 L. 157       540  LOAD_FAST                'Y_w'
              542  LOAD_METHOD              std
              544  LOAD_CONST               0
              546  CALL_METHOD_1         1  '1 positional argument'
              548  STORE_FAST               'sd_y'

 L. 158       550  LOAD_GLOBAL              preprocessing
              552  LOAD_METHOD              scale
              554  LOAD_FAST                'Y_w'
              556  LOAD_CONST               1.0
              558  BINARY_MULTIPLY  
              560  CALL_METHOD_1         1  '1 positional argument'
              562  STORE_FAST               'Y_w'

 L. 160       564  BUILD_MAP_0           0 
              566  STORE_FAST               'Ms'

 L. 161       568  SETUP_LOOP          722  'to 722'
              570  LOAD_GLOBAL              range
              572  LOAD_FAST                'K'
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  GET_ITER         
              578  FOR_ITER            720  'to 720'
              580  STORE_FAST               'i'

 L. 162       582  LOAD_FAST                'Y_w'
              584  LOAD_ATTR                T
              586  LOAD_METHOD              dot
              588  LOAD_FAST                'Xs_w'
              590  LOAD_FAST                'i'
              592  BINARY_SUBSCR    
              594  CALL_METHOD_1         1  '1 positional argument'
              596  LOAD_FAST                'n'
              598  LOAD_CONST               1
              600  BINARY_SUBTRACT  
              602  BINARY_TRUE_DIVIDE
              604  STORE_FAST               'M0'

 L. 163       606  LOAD_GLOBAL              abs
              608  LOAD_FAST                'M0'
              610  CALL_FUNCTION_1       1  '1 positional argument'
              612  LOAD_FAST                'lambd'
              614  BINARY_SUBTRACT  
              616  STORE_FAST               'M'

 L. 164       618  LOAD_GLOBAL              np
              620  LOAD_METHOD              where
              622  LOAD_GLOBAL              np
              624  LOAD_METHOD              sign
              626  LOAD_FAST                'M'
              628  CALL_METHOD_1         1  '1 positional argument'
              630  LOAD_CONST               -1
              632  COMPARE_OP               ==
              634  CALL_METHOD_1         1  '1 positional argument'
              636  STORE_FAST               'pos_soft'

 L. 165       638  SETUP_LOOP          694  'to 694'
              640  LOAD_GLOBAL              range
              642  LOAD_GLOBAL              len
              644  LOAD_FAST                'pos_soft'
              646  LOAD_CONST               0
              648  BINARY_SUBSCR    
              650  CALL_FUNCTION_1       1  '1 positional argument'
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  GET_ITER         
              656  FOR_ITER            692  'to 692'
              658  STORE_FAST               'j'

 L. 166       660  LOAD_CONST               0
              662  LOAD_FAST                'M'
              664  LOAD_FAST                'pos_soft'
              666  LOAD_CONST               0
              668  BINARY_SUBSCR    
              670  LOAD_FAST                'j'
              672  BINARY_SUBSCR    
              674  LOAD_FAST                'pos_soft'
              676  LOAD_CONST               1
              678  BINARY_SUBSCR    
              680  LOAD_FAST                'j'
              682  BINARY_SUBSCR    
              684  BUILD_TUPLE_2         2 
              686  STORE_SUBSCR     
          688_690  JUMP_BACK           656  'to 656'
              692  POP_BLOCK        
            694_0  COME_FROM_LOOP      638  '638'

 L. 167       694  LOAD_GLOBAL              np
              696  LOAD_METHOD              multiply
              698  LOAD_GLOBAL              np
              700  LOAD_METHOD              sign
              702  LOAD_FAST                'M0'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  LOAD_FAST                'M'
              708  CALL_METHOD_2         2  '2 positional arguments'
              710  LOAD_FAST                'Ms'
              712  LOAD_FAST                'i'
              714  STORE_SUBSCR     
          716_718  JUMP_BACK           578  'to 578'
              720  POP_BLOCK        
            722_0  COME_FROM_LOOP      568  '568'

 L. 168       722  BUILD_MAP_0           0 
              724  STORE_FAST               'u_t_r'

 L. 169       726  BUILD_MAP_0           0 
              728  STORE_FAST               'u_t_r_0'

 L. 170       730  BUILD_MAP_0           0 
              732  STORE_FAST               't_r'

 L. 171       734  BUILD_MAP_0           0 
              736  STORE_FAST               'z_r'

 L. 172   738_740  SETUP_LOOP         1738  'to 1738'
              742  LOAD_GLOBAL              range
              744  LOAD_FAST                'K'
              746  CALL_FUNCTION_1       1  '1 positional argument'
              748  GET_ITER         
          750_752  FOR_ITER           1736  'to 1736'
              754  STORE_FAST               'k'

 L. 173       756  LOAD_GLOBAL              sum
              758  LOAD_GLOBAL              sum
              760  LOAD_GLOBAL              abs
              762  LOAD_FAST                'Ms'
              764  LOAD_FAST                'k'
              766  BINARY_SUBSCR    
              768  CALL_FUNCTION_1       1  '1 positional argument'
              770  CALL_FUNCTION_1       1  '1 positional argument'
              772  CALL_FUNCTION_1       1  '1 positional argument'
              774  LOAD_CONST               0
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   814  'to 814'

 L. 174       782  LOAD_STR                 'v'
              784  LOAD_GLOBAL              np
              786  LOAD_METHOD              zeros
              788  LOAD_FAST                'Ms'
              790  LOAD_FAST                'k'
              792  BINARY_SUBSCR    
              794  LOAD_ATTR                shape
              796  LOAD_CONST               1
              798  BINARY_SUBSCR    
              800  LOAD_FAST                'R'
              802  BUILD_TUPLE_2         2 
              804  CALL_METHOD_1         1  '1 positional argument'
              806  BUILD_MAP_1           1 
              808  STORE_FAST               'svd_k'
          810_812  JUMP_FORWARD       1378  'to 1378'
            814_0  COME_FROM           778  '778'

 L. 176       814  LOAD_GLOBAL              np
              816  LOAD_ATTR                linalg
              818  LOAD_ATTR                svd
              820  LOAD_FAST                'Ms'
              822  LOAD_FAST                'k'
              824  BINARY_SUBSCR    
              826  LOAD_CONST               False
              828  LOAD_CONST               ('full_matrices',)
              830  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              832  STORE_FAST               'svd_k_res'

 L. 177       834  LOAD_FAST                'svd_k_res'
              836  LOAD_CONST               1
              838  BINARY_SUBSCR    
              840  LOAD_ATTR                size
              842  STORE_FAST               'len_eig'

 L. 178       844  LOAD_FAST                'len_eig'
              846  LOAD_FAST                'R'
              848  COMPARE_OP               <
          850_852  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 179       854  LOAD_GLOBAL              np
              856  LOAD_METHOD              zeros
              858  LOAD_FAST                'R'
              860  CALL_METHOD_1         1  '1 positional argument'
              862  STORE_FAST               'eigs'

 L. 180       864  LOAD_FAST                'len_eig'
              866  LOAD_CONST               1
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   888  'to 888'

 L. 181       874  LOAD_FAST                'svd_k_res'
              876  LOAD_CONST               1
              878  BINARY_SUBSCR    
              880  LOAD_FAST                'eigs'
              882  LOAD_CONST               0
              884  STORE_SUBSCR     
              886  JUMP_FORWARD        908  'to 908'
            888_0  COME_FROM           870  '870'

 L. 183       888  LOAD_FAST                'svd_k_res'
              890  LOAD_CONST               1
              892  BINARY_SUBSCR    
              894  LOAD_FAST                'eigs'
              896  LOAD_GLOBAL              range
              898  LOAD_FAST                'len_eig'
              900  LOAD_CONST               1
              902  BINARY_SUBTRACT  
              904  CALL_FUNCTION_1       1  '1 positional argument'
              906  STORE_SUBSCR     
            908_0  COME_FROM           886  '886'

 L. 184       908  LOAD_FAST                'svd_k_res'
              910  LOAD_CONST               2
              912  BINARY_SUBSCR    
              914  LOAD_ATTR                T
              916  LOAD_ATTR                shape
              918  LOAD_CONST               1
              920  BINARY_SUBSCR    
              922  LOAD_FAST                'R'
              924  COMPARE_OP               <
          926_928  POP_JUMP_IF_FALSE   998  'to 998'

 L. 185       930  LOAD_GLOBAL              np
              932  LOAD_METHOD              zeros
              934  LOAD_FAST                'svd_k_res'
              936  LOAD_CONST               2
              938  BINARY_SUBSCR    
              940  LOAD_ATTR                T
              942  LOAD_ATTR                shape
              944  LOAD_CONST               0
              946  BINARY_SUBSCR    
              948  LOAD_FAST                'R'
              950  LOAD_FAST                'svd_k_res'
              952  LOAD_CONST               2
              954  BINARY_SUBSCR    
              956  LOAD_ATTR                T
              958  LOAD_ATTR                shape
              960  LOAD_CONST               1
              962  BINARY_SUBSCR    
              964  BINARY_SUBTRACT  
              966  BUILD_TUPLE_2         2 
              968  CALL_METHOD_1         1  '1 positional argument'
              970  STORE_FAST               'additionnal'

 L. 186       972  LOAD_GLOBAL              np
              974  LOAD_ATTR                concatenate
              976  LOAD_FAST                'svd_k_res'
              978  LOAD_CONST               2
              980  BINARY_SUBSCR    
              982  LOAD_ATTR                T
              984  LOAD_FAST                'additionnal'
              986  BUILD_TUPLE_2         2 
              988  LOAD_CONST               1
              990  LOAD_CONST               ('axis',)
              992  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              994  STORE_FAST               'v_k'
              996  JUMP_FORWARD       1272  'to 1272'
            998_0  COME_FROM           926  '926'

 L. 188       998  LOAD_FAST                'svd_k_res'
             1000  LOAD_CONST               2
             1002  BINARY_SUBSCR    
             1004  LOAD_ATTR                T
             1006  STORE_FAST               'v_k'
         1008_1010  JUMP_FORWARD       1272  'to 1272'
           1012_0  COME_FROM           850  '850'

 L. 189      1012  LOAD_FAST                'len_eig'
             1014  LOAD_FAST                'R'
             1016  COMPARE_OP               >
         1018_1020  POP_JUMP_IF_FALSE  1254  'to 1254'

 L. 190      1022  LOAD_FAST                'Y_w'
             1024  LOAD_ATTR                T
             1026  LOAD_METHOD              dot
             1028  LOAD_FAST                'Xs_w'
             1030  LOAD_FAST                'k'
             1032  BINARY_SUBSCR    
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  LOAD_METHOD              dot
             1038  LOAD_FAST                'svd_k_res'
             1040  LOAD_CONST               2
             1042  BINARY_SUBSCR    
             1044  LOAD_ATTR                T
             1046  CALL_METHOD_1         1  '1 positional argument'
             1048  STORE_FAST               'proj_not_thresh'

 L. 191      1050  LOAD_GLOBAL              np
             1052  LOAD_METHOD              zeros
             1054  LOAD_FAST                'len_eig'
             1056  CALL_METHOD_1         1  '1 positional argument'
             1058  STORE_FAST               'eigs_not_thresh'

 L. 192      1060  SETUP_LOOP         1110  'to 1110'
             1062  LOAD_GLOBAL              range
             1064  LOAD_FAST                'len_eig'
             1066  CALL_FUNCTION_1       1  '1 positional argument'
             1068  GET_ITER         
             1070  FOR_ITER           1108  'to 1108'
             1072  STORE_FAST               'oo'

 L. 193      1074  LOAD_GLOBAL              np
             1076  LOAD_METHOD              sum
             1078  LOAD_FAST                'proj_not_thresh'
             1080  LOAD_CONST               None
             1082  LOAD_CONST               None
             1084  BUILD_SLICE_2         2 
             1086  LOAD_FAST                'oo'
             1088  BUILD_TUPLE_2         2 
             1090  BINARY_SUBSCR    
             1092  LOAD_CONST               2
             1094  BINARY_POWER     
             1096  CALL_METHOD_1         1  '1 positional argument'
             1098  LOAD_FAST                'eigs_not_thresh'
             1100  LOAD_FAST                'oo'
             1102  STORE_SUBSCR     
         1104_1106  JUMP_BACK          1070  'to 1070'
             1108  POP_BLOCK        
           1110_0  COME_FROM_LOOP     1060  '1060'

 L. 194      1110  LOAD_GLOBAL              np
             1112  LOAD_METHOD              argsort
             1114  LOAD_FAST                'eigs_not_thresh'
             1116  UNARY_NEGATIVE   
             1118  CALL_METHOD_1         1  '1 positional argument'
             1120  STORE_FAST               'order_good'

 L. 195      1122  LOAD_FAST                'R'
             1124  LOAD_CONST               1
             1126  COMPARE_OP               ==
         1128_1130  POP_JUMP_IF_FALSE  1202  'to 1202'

 L. 196      1132  LOAD_FAST                'svd_k_res'
             1134  LOAD_CONST               1
             1136  BINARY_SUBSCR    
             1138  LOAD_FAST                'order_good'
             1140  LOAD_CONST               0
             1142  BINARY_SUBSCR    
             1144  BINARY_SUBSCR    
             1146  LOAD_METHOD              reshape
             1148  LOAD_FAST                'R'
             1150  CALL_METHOD_1         1  '1 positional argument'
             1152  STORE_FAST               'eigs'

 L. 197      1154  LOAD_FAST                'svd_k_res'
             1156  LOAD_CONST               2
             1158  BINARY_SUBSCR    
             1160  LOAD_ATTR                T
             1162  LOAD_CONST               None
             1164  LOAD_CONST               None
             1166  BUILD_SLICE_2         2 
             1168  LOAD_FAST                'order_good'
             1170  LOAD_CONST               0
             1172  BINARY_SUBSCR    
             1174  BUILD_TUPLE_2         2 
             1176  BINARY_SUBSCR    
             1178  LOAD_METHOD              reshape
             1180  LOAD_FAST                'Ms'
             1182  LOAD_FAST                'k'
             1184  BINARY_SUBSCR    
             1186  LOAD_ATTR                shape
             1188  LOAD_CONST               1
             1190  BINARY_SUBSCR    
             1192  LOAD_FAST                'R'
             1194  BUILD_TUPLE_2         2 
             1196  CALL_METHOD_1         1  '1 positional argument'
             1198  STORE_FAST               'v_k'
             1200  JUMP_FORWARD       1252  'to 1252'
           1202_0  COME_FROM          1128  '1128'

 L. 199      1202  LOAD_FAST                'svd_k_res'
             1204  LOAD_CONST               1
             1206  BINARY_SUBSCR    
             1208  LOAD_FAST                'order_good'
             1210  LOAD_GLOBAL              range
             1212  LOAD_FAST                'R'
             1214  CALL_FUNCTION_1       1  '1 positional argument'
             1216  BINARY_SUBSCR    
             1218  BINARY_SUBSCR    
             1220  STORE_FAST               'eigs'

 L. 200      1222  LOAD_FAST                'svd_k_res'
             1224  LOAD_CONST               2
             1226  BINARY_SUBSCR    
             1228  LOAD_ATTR                T
             1230  LOAD_CONST               None
             1232  LOAD_CONST               None
             1234  BUILD_SLICE_2         2 
             1236  LOAD_FAST                'order_good'
             1238  LOAD_GLOBAL              range
             1240  LOAD_FAST                'R'
             1242  CALL_FUNCTION_1       1  '1 positional argument'
             1244  BINARY_SUBSCR    
             1246  BUILD_TUPLE_2         2 
             1248  BINARY_SUBSCR    
             1250  STORE_FAST               'v_k'
           1252_0  COME_FROM          1200  '1200'
             1252  JUMP_FORWARD       1272  'to 1272'
           1254_0  COME_FROM          1018  '1018'

 L. 202      1254  LOAD_FAST                'svd_k_res'
             1256  LOAD_CONST               1
           1258_0  COME_FROM           996  '996'
             1258  BINARY_SUBSCR    
             1260  STORE_FAST               'eigs'

 L. 203      1262  LOAD_FAST                'svd_k_res'
             1264  LOAD_CONST               2
             1266  BINARY_SUBSCR    
             1268  LOAD_ATTR                T
             1270  STORE_FAST               'v_k'
           1272_0  COME_FROM          1252  '1252'
           1272_1  COME_FROM          1008  '1008'

 L. 204      1272  LOAD_FAST                'R'
             1274  LOAD_CONST               1
             1276  COMPARE_OP               !=
         1278_1280  POP_JUMP_IF_FALSE  1334  'to 1334'

 L. 205      1282  SETUP_LOOP         1360  'to 1360'
             1284  LOAD_GLOBAL              range
             1286  LOAD_FAST                'R'
             1288  CALL_FUNCTION_1       1  '1 positional argument'
             1290  GET_ITER         
           1292_0  COME_FROM          1306  '1306'
             1292  FOR_ITER           1330  'to 1330'
             1294  STORE_FAST               'r_i'

 L. 206      1296  LOAD_FAST                'eigs'
             1298  LOAD_FAST                'r_i'
             1300  BINARY_SUBSCR    
             1302  LOAD_CONST               0
             1304  COMPARE_OP               ==
         1306_1308  POP_JUMP_IF_FALSE  1292  'to 1292'

 L. 207      1310  LOAD_CONST               0
             1312  LOAD_FAST                'v_k'
             1314  LOAD_CONST               None
             1316  LOAD_CONST               None
             1318  BUILD_SLICE_2         2 
             1320  LOAD_FAST                'r_i'
             1322  BUILD_TUPLE_2         2 
             1324  STORE_SUBSCR     
         1326_1328  JUMP_BACK          1292  'to 1292'
             1330  POP_BLOCK        
             1332  JUMP_FORWARD       1360  'to 1360'
           1334_0  COME_FROM          1278  '1278'

 L. 209      1334  LOAD_FAST                'eigs'
             1336  LOAD_CONST               0
             1338  COMPARE_OP               ==
         1340_1342  POP_JUMP_IF_FALSE  1360  'to 1360'

 L. 210      1344  LOAD_CONST               0
             1346  LOAD_FAST                'v_k'
             1348  LOAD_CONST               None
             1350  LOAD_CONST               None
             1352  BUILD_SLICE_2         2 
             1354  LOAD_CONST               0
             1356  BUILD_TUPLE_2         2 
             1358  STORE_SUBSCR     
           1360_0  COME_FROM          1340  '1340'
           1360_1  COME_FROM          1332  '1332'
           1360_2  COME_FROM_LOOP     1282  '1282'

 L. 211      1360  LOAD_FAST                'svd_k_res'
             1362  LOAD_CONST               2
             1364  BINARY_SUBSCR    
             1366  LOAD_ATTR                T
             1368  STORE_FAST               'v_k_res'

 L. 212      1370  LOAD_STR                 'v'
             1372  LOAD_FAST                'v_k'
             1374  BUILD_MAP_1           1 
             1376  STORE_FAST               'svd_k'
           1378_0  COME_FROM           810  '810'

 L. 213      1378  LOAD_FAST                'svd_k'
             1380  LOAD_STR                 'v'
             1382  BINARY_SUBSCR    
             1384  LOAD_FAST                'u_t_r'
             1386  LOAD_FAST                'k'
             1388  STORE_SUBSCR     

 L. 214      1390  LOAD_FAST                'svd_k'
             1392  LOAD_STR                 'v'
             1394  BINARY_SUBSCR    
             1396  LOAD_FAST                'u_t_r_0'
             1398  LOAD_FAST                'k'
             1400  STORE_SUBSCR     

 L. 215      1402  LOAD_FAST                'k'
             1404  LOAD_CONST               0
             1406  COMPARE_OP               ==
         1408_1410  POP_JUMP_IF_FALSE  1468  'to 1468'

 L. 216      1412  SETUP_LOOP         1468  'to 1468'
             1414  LOAD_GLOBAL              range
             1416  LOAD_FAST                'R'
             1418  CALL_FUNCTION_1       1  '1 positional argument'
             1420  GET_ITER         
             1422  FOR_ITER           1466  'to 1466'
             1424  STORE_FAST               'r'

 L. 217      1426  LOAD_GLOBAL              np
             1428  LOAD_METHOD              zeros
             1430  LOAD_FAST                'n'
             1432  LOAD_FAST                'K'
             1434  BUILD_TUPLE_2         2 
             1436  CALL_METHOD_1         1  '1 positional argument'
             1438  LOAD_FAST                't_r'
             1440  LOAD_FAST                'r'
             1442  STORE_SUBSCR     

 L. 218      1444  LOAD_GLOBAL              np
             1446  LOAD_METHOD              zeros
             1448  LOAD_FAST                'q'
             1450  LOAD_FAST                'K'
             1452  BUILD_TUPLE_2         2 
             1454  CALL_METHOD_1         1  '1 positional argument'
             1456  LOAD_FAST                'z_r'
             1458  LOAD_FAST                'r'
             1460  STORE_SUBSCR     
         1462_1464  JUMP_BACK          1422  'to 1422'
             1466  POP_BLOCK        
           1468_0  COME_FROM_LOOP     1412  '1412'
           1468_1  COME_FROM          1408  '1408'

 L. 219      1468  LOAD_FAST                'R'
             1470  LOAD_CONST               1
             1472  COMPARE_OP               !=
         1474_1476  POP_JUMP_IF_FALSE  1596  'to 1596'

 L. 220      1478  SETUP_LOOP         1732  'to 1732'
             1480  LOAD_GLOBAL              range
             1482  LOAD_FAST                'R'
             1484  CALL_FUNCTION_1       1  '1 positional argument'
             1486  GET_ITER         
             1488  FOR_ITER           1592  'to 1592'
             1490  STORE_FAST               'r'

 L. 221      1492  LOAD_GLOBAL              np
             1494  LOAD_METHOD              dot
             1496  LOAD_FAST                'Xs_w'
             1498  LOAD_FAST                'k'
             1500  BINARY_SUBSCR    
             1502  LOAD_FAST                'u_t_r'
             1504  LOAD_FAST                'k'
             1506  BINARY_SUBSCR    
             1508  LOAD_CONST               None
             1510  LOAD_CONST               None
             1512  BUILD_SLICE_2         2 
             1514  LOAD_FAST                'r'
             1516  BUILD_TUPLE_2         2 
             1518  BINARY_SUBSCR    
             1520  CALL_METHOD_2         2  '2 positional arguments'
             1522  LOAD_FAST                't_r'
             1524  LOAD_FAST                'r'
             1526  BINARY_SUBSCR    
             1528  LOAD_CONST               None
             1530  LOAD_CONST               None
             1532  BUILD_SLICE_2         2 
             1534  LOAD_FAST                'k'
             1536  BUILD_TUPLE_2         2 
             1538  STORE_SUBSCR     

 L. 222      1540  LOAD_GLOBAL              np
             1542  LOAD_METHOD              dot
             1544  LOAD_FAST                'Ms'
             1546  LOAD_FAST                'k'
             1548  BINARY_SUBSCR    
             1550  LOAD_FAST                'u_t_r'
             1552  LOAD_FAST                'k'
             1554  BINARY_SUBSCR    
             1556  LOAD_CONST               None
             1558  LOAD_CONST               None
             1560  BUILD_SLICE_2         2 
             1562  LOAD_FAST                'r'
             1564  BUILD_TUPLE_2         2 
             1566  BINARY_SUBSCR    
             1568  CALL_METHOD_2         2  '2 positional arguments'
             1570  LOAD_FAST                'z_r'
             1572  LOAD_FAST                'r'
             1574  BINARY_SUBSCR    
             1576  LOAD_CONST               None
             1578  LOAD_CONST               None
             1580  BUILD_SLICE_2         2 
             1582  LOAD_FAST                'k'
             1584  BUILD_TUPLE_2         2 
             1586  STORE_SUBSCR     
         1588_1590  JUMP_BACK          1488  'to 1488'
             1592  POP_BLOCK        
             1594  JUMP_BACK           750  'to 750'
           1596_0  COME_FROM          1474  '1474'

 L. 224      1596  LOAD_FAST                'K'
             1598  LOAD_CONST               1
             1600  COMPARE_OP               ==
         1602_1604  POP_JUMP_IF_FALSE  1656  'to 1656'

 L. 225      1606  LOAD_GLOBAL              np
             1608  LOAD_METHOD              dot
             1610  LOAD_FAST                'Xs_w'
             1612  LOAD_FAST                'k'
             1614  BINARY_SUBSCR    
             1616  LOAD_FAST                'u_t_r'
             1618  LOAD_FAST                'k'
             1620  BINARY_SUBSCR    
             1622  CALL_METHOD_2         2  '2 positional arguments'
             1624  LOAD_FAST                't_r'
             1626  LOAD_CONST               0
             1628  STORE_SUBSCR     

 L. 226      1630  LOAD_GLOBAL              np
             1632  LOAD_METHOD              dot
             1634  LOAD_FAST                'Ms'
             1636  LOAD_FAST                'k'
             1638  BINARY_SUBSCR    
             1640  LOAD_FAST                'u_t_r'
             1642  LOAD_FAST                'k'
             1644  BINARY_SUBSCR    
             1646  CALL_METHOD_2         2  '2 positional arguments'
             1648  LOAD_FAST                'z_r'
             1650  LOAD_CONST               0
             1652  STORE_SUBSCR     
             1654  JUMP_BACK           750  'to 750'
           1656_0  COME_FROM          1602  '1602'

 L. 228      1656  LOAD_GLOBAL              np
             1658  LOAD_METHOD              dot
             1660  LOAD_FAST                'Xs_w'
             1662  LOAD_FAST                'k'
             1664  BINARY_SUBSCR    
             1666  LOAD_FAST                'u_t_r'
             1668  LOAD_FAST                'k'
             1670  BINARY_SUBSCR    
             1672  CALL_METHOD_2         2  '2 positional arguments'
             1674  LOAD_ATTR                T
             1676  LOAD_FAST                't_r'
             1678  LOAD_CONST               0
             1680  BINARY_SUBSCR    
             1682  LOAD_CONST               None
             1684  LOAD_CONST               None
             1686  BUILD_SLICE_2         2 
             1688  LOAD_FAST                'k'
             1690  BUILD_TUPLE_2         2 
             1692  STORE_SUBSCR     

 L. 229      1694  LOAD_GLOBAL              np
             1696  LOAD_METHOD              dot
             1698  LOAD_FAST                'Ms'
             1700  LOAD_FAST                'k'
             1702  BINARY_SUBSCR    
             1704  LOAD_FAST                'u_t_r'
             1706  LOAD_FAST                'k'
             1708  BINARY_SUBSCR    
             1710  CALL_METHOD_2         2  '2 positional arguments'
             1712  LOAD_ATTR                T
             1714  LOAD_FAST                'z_r'
             1716  LOAD_CONST               0
             1718  BINARY_SUBSCR    
             1720  LOAD_CONST               None
             1722  LOAD_CONST               None
             1724  BUILD_SLICE_2         2 
             1726  LOAD_FAST                'k'
             1728  BUILD_TUPLE_2         2 
             1730  STORE_SUBSCR     
           1732_0  COME_FROM_LOOP     1478  '1478'
         1732_1734  JUMP_BACK           750  'to 750'
             1736  POP_BLOCK        
           1738_0  COME_FROM_LOOP      738  '738'

 L. 230      1738  LOAD_GLOBAL              np
             1740  LOAD_METHOD              zeros
             1742  LOAD_FAST                'n'
             1744  LOAD_FAST                'R'
             1746  BUILD_TUPLE_2         2 
             1748  CALL_METHOD_1         1  '1 positional argument'
             1750  STORE_FAST               't'

 L. 231      1752  LOAD_GLOBAL              np
             1754  LOAD_METHOD              zeros
             1756  LOAD_FAST                'q'
             1758  LOAD_FAST                'R'
             1760  BUILD_TUPLE_2         2 
             1762  CALL_METHOD_1         1  '1 positional argument'
             1764  STORE_FAST               'v'

 L. 232      1766  LOAD_GLOBAL              np
             1768  LOAD_METHOD              zeros
             1770  LOAD_FAST                'n'
             1772  LOAD_FAST                'R'
             1774  LOAD_FAST                'K'
             1776  BINARY_MULTIPLY  
             1778  BUILD_TUPLE_2         2 
             1780  CALL_METHOD_1         1  '1 positional argument'
             1782  STORE_FAST               't_all'

 L. 233      1784  LOAD_GLOBAL              np
             1786  LOAD_METHOD              zeros
             1788  LOAD_FAST                'q'
             1790  LOAD_FAST                'R'
             1792  LOAD_FAST                'K'
             1794  BINARY_MULTIPLY  
             1796  BUILD_TUPLE_2         2 
             1798  CALL_METHOD_1         1  '1 positional argument'
             1800  STORE_FAST               'z_all'

 L. 234      1802  SETUP_LOOP         1914  'to 1914'
             1804  LOAD_GLOBAL              range
             1806  LOAD_FAST                'R'
             1808  CALL_FUNCTION_1       1  '1 positional argument'
             1810  GET_ITER         
             1812  FOR_ITER           1912  'to 1912'
             1814  STORE_FAST               'r'

 L. 235      1816  LOAD_GLOBAL              np
             1818  LOAD_METHOD              array
             1820  LOAD_FAST                'z_r'
             1822  LOAD_FAST                'r'
             1824  BINARY_SUBSCR    
             1826  CALL_METHOD_1         1  '1 positional argument'
             1828  LOAD_FAST                'z_all'
             1830  LOAD_CONST               None
             1832  LOAD_CONST               None
             1834  BUILD_SLICE_2         2 
             1836  LOAD_GLOBAL              np
             1838  LOAD_METHOD              repeat
             1840  LOAD_FAST                'r'
             1842  LOAD_FAST                'K'
             1844  BINARY_MULTIPLY  
             1846  LOAD_FAST                'K'
             1848  CALL_METHOD_2         2  '2 positional arguments'
             1850  LOAD_GLOBAL              range
             1852  LOAD_FAST                'K'
             1854  CALL_FUNCTION_1       1  '1 positional argument'
             1856  BINARY_ADD       
             1858  BUILD_TUPLE_2         2 
             1860  STORE_SUBSCR     

 L. 236      1862  LOAD_GLOBAL              np
             1864  LOAD_METHOD              array
             1866  LOAD_FAST                't_r'
             1868  LOAD_FAST                'r'
             1870  BINARY_SUBSCR    
             1872  CALL_METHOD_1         1  '1 positional argument'
             1874  LOAD_FAST                't_all'
             1876  LOAD_CONST               None
             1878  LOAD_CONST               None
             1880  BUILD_SLICE_2         2 
             1882  LOAD_GLOBAL              np
             1884  LOAD_METHOD              repeat
             1886  LOAD_FAST                'r'
             1888  LOAD_FAST                'K'
             1890  BINARY_MULTIPLY  
             1892  LOAD_FAST                'K'
             1894  CALL_METHOD_2         2  '2 positional arguments'
             1896  LOAD_GLOBAL              range
             1898  LOAD_FAST                'K'
             1900  CALL_FUNCTION_1       1  '1 positional argument'
             1902  BINARY_ADD       
             1904  BUILD_TUPLE_2         2 
             1906  STORE_SUBSCR     
         1908_1910  JUMP_BACK          1812  'to 1812'
             1912  POP_BLOCK        
           1914_0  COME_FROM_LOOP     1802  '1802'

 L. 237      1914  LOAD_GLOBAL              np
             1916  LOAD_ATTR                linalg
             1918  LOAD_ATTR                svd
             1920  LOAD_FAST                'z_all'
             1922  LOAD_CONST               False
             1924  LOAD_CONST               ('full_matrices',)
             1926  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1928  STORE_FAST               'svd_all_python'

 L. 238      1930  LOAD_FAST                'svd_all_python'
             1932  LOAD_CONST               1
             1934  BINARY_SUBSCR    
             1936  LOAD_ATTR                size
             1938  LOAD_FAST                'R'
             1940  COMPARE_OP               <
         1942_1944  POP_JUMP_IF_FALSE  2204  'to 2204'

 L. 239      1946  LOAD_GLOBAL              np
             1948  LOAD_METHOD              zeros
             1950  LOAD_FAST                'R'
             1952  CALL_METHOD_1         1  '1 positional argument'
             1954  STORE_FAST               'eigs'

 L. 240      1956  LOAD_FAST                'svd_all_python'
             1958  LOAD_CONST               1
             1960  BINARY_SUBSCR    
             1962  LOAD_ATTR                size
             1964  LOAD_CONST               1
             1966  COMPARE_OP               ==
         1968_1970  POP_JUMP_IF_FALSE  1986  'to 1986'

 L. 241      1972  LOAD_FAST                'svd_all_python'
             1974  LOAD_CONST               1
             1976  BINARY_SUBSCR    
             1978  LOAD_FAST                'eigs'
             1980  LOAD_CONST               0
             1982  STORE_SUBSCR     
             1984  JUMP_FORWARD       2012  'to 2012'
           1986_0  COME_FROM          1968  '1968'

 L. 243      1986  LOAD_FAST                'svd_all_python'
             1988  LOAD_CONST               1
             1990  BINARY_SUBSCR    
             1992  LOAD_FAST                'eigs'
             1994  LOAD_GLOBAL              range
             1996  LOAD_FAST                'svd_all_python'
             1998  LOAD_CONST               1
             2000  BINARY_SUBSCR    
             2002  LOAD_ATTR                size
             2004  LOAD_CONST               1
             2006  BINARY_SUBTRACT  
             2008  CALL_FUNCTION_1       1  '1 positional argument'
             2010  STORE_SUBSCR     
           2012_0  COME_FROM          1984  '1984'

 L. 244      2012  LOAD_FAST                'svd_all_python'
             2014  LOAD_CONST               2
             2016  BINARY_SUBSCR    
             2018  LOAD_ATTR                T
             2020  LOAD_ATTR                shape
             2022  LOAD_CONST               1
             2024  BINARY_SUBSCR    
             2026  LOAD_FAST                'R'
             2028  COMPARE_OP               <
         2030_2032  POP_JUMP_IF_FALSE  2102  'to 2102'

 L. 245      2034  LOAD_GLOBAL              np
             2036  LOAD_METHOD              zeros
             2038  LOAD_FAST                'svd_all_python'
             2040  LOAD_CONST               2
             2042  BINARY_SUBSCR    
             2044  LOAD_ATTR                T
             2046  LOAD_ATTR                shape
             2048  LOAD_CONST               0
             2050  BINARY_SUBSCR    
             2052  LOAD_FAST                'R'
             2054  LOAD_FAST                'svd_all_python'
             2056  LOAD_CONST               2
             2058  BINARY_SUBSCR    
             2060  LOAD_ATTR                T
             2062  LOAD_ATTR                shape
             2064  LOAD_CONST               1
             2066  BINARY_SUBSCR    
             2068  BINARY_SUBTRACT  
             2070  BUILD_TUPLE_2         2 
             2072  CALL_METHOD_1         1  '1 positional argument'
             2074  STORE_FAST               'additionnal'

 L. 246      2076  LOAD_GLOBAL              np
             2078  LOAD_ATTR                concatenate
             2080  LOAD_FAST                'svd_all_python'
             2082  LOAD_CONST               2
             2084  BINARY_SUBSCR    
             2086  LOAD_ATTR                T
             2088  LOAD_FAST                'additionnal'
             2090  BUILD_TUPLE_2         2 
             2092  LOAD_CONST               1
             2094  LOAD_CONST               ('axis',)
             2096  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2098  STORE_FAST               'u'
             2100  JUMP_FORWARD       2112  'to 2112'
           2102_0  COME_FROM          2030  '2030'

 L. 248      2102  LOAD_FAST                'svd_all_python'
             2104  LOAD_CONST               2
             2106  BINARY_SUBSCR    
             2108  LOAD_ATTR                T
             2110  STORE_FAST               'u'
           2112_0  COME_FROM          2100  '2100'

 L. 249      2112  LOAD_FAST                'svd_all_python'
             2114  LOAD_CONST               0
             2116  BINARY_SUBSCR    
             2118  LOAD_ATTR                shape
             2120  LOAD_CONST               1
             2122  BINARY_SUBSCR    
             2124  LOAD_FAST                'R'
             2126  COMPARE_OP               <
         2128_2130  POP_JUMP_IF_FALSE  2194  'to 2194'

 L. 250      2132  LOAD_GLOBAL              np
             2134  LOAD_METHOD              zeros
             2136  LOAD_FAST                'svd_all_python'
             2138  LOAD_CONST               0
             2140  BINARY_SUBSCR    
             2142  LOAD_ATTR                shape
             2144  LOAD_CONST               0
             2146  BINARY_SUBSCR    
             2148  LOAD_FAST                'R'
             2150  LOAD_FAST                'svd_all_python'
             2152  LOAD_CONST               0
             2154  BINARY_SUBSCR    
             2156  LOAD_ATTR                shape
             2158  LOAD_CONST               1
             2160  BINARY_SUBSCR    
             2162  BINARY_SUBTRACT  
             2164  BUILD_TUPLE_2         2 
             2166  CALL_METHOD_1         1  '1 positional argument'
             2168  STORE_FAST               'additionnal'

 L. 251      2170  LOAD_GLOBAL              np
             2172  LOAD_ATTR                concatenate
             2174  LOAD_FAST                'svd_all_python'
             2176  LOAD_CONST               0
             2178  BINARY_SUBSCR    
             2180  LOAD_FAST                'additionnal'
             2182  BUILD_TUPLE_2         2 
             2184  LOAD_CONST               1
             2186  LOAD_CONST               ('axis',)
             2188  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2190  STORE_FAST               'v0'
             2192  JUMP_FORWARD       2202  'to 2202'
           2194_0  COME_FROM          2128  '2128'

 L. 253      2194  LOAD_FAST                'svd_all_python'
             2196  LOAD_CONST               0
             2198  BINARY_SUBSCR    
             2200  STORE_FAST               'v0'
           2202_0  COME_FROM          2192  '2192'
             2202  JUMP_FORWARD       2222  'to 2222'
           2204_0  COME_FROM          1942  '1942'

 L. 255      2204  LOAD_FAST                'svd_all_python'
             2206  LOAD_CONST               2
             2208  BINARY_SUBSCR    
             2210  LOAD_ATTR                T
             2212  STORE_FAST               'u'

 L. 256      2214  LOAD_FAST                'svd_all_python'
             2216  LOAD_CONST               0
             2218  BINARY_SUBSCR    
             2220  STORE_FAST               'v0'
           2222_0  COME_FROM          2202  '2202'

 L. 257      2222  LOAD_FAST                'v0'
             2224  STORE_FAST               'v'

 L. 258      2226  LOAD_GLOBAL              np
             2228  LOAD_METHOD              dot
             2230  LOAD_FAST                'Y_w'
             2232  LOAD_FAST                'v0'
             2234  CALL_METHOD_2         2  '2 positional arguments'
             2236  STORE_FAST               's'

 L. 259      2238  LOAD_GLOBAL              np
             2240  LOAD_METHOD              dot
             2242  LOAD_FAST                't_all'
             2244  LOAD_FAST                'u'
             2246  CALL_METHOD_2         2  '2 positional arguments'
             2248  STORE_FAST               't'

 L. 260      2250  LOAD_GLOBAL              np
             2252  LOAD_ATTR                linalg
             2254  LOAD_ATTR                svd
             2256  LOAD_GLOBAL              np
             2258  LOAD_METHOD              dot
             2260  LOAD_FAST                't'
             2262  LOAD_ATTR                T
             2264  LOAD_FAST                's'
             2266  CALL_METHOD_2         2  '2 positional arguments'
             2268  LOAD_CONST               False
             2270  LOAD_CONST               ('full_matrices',)
             2272  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2274  STORE_FAST               'svd_all_frak_python'

 L. 261      2276  LOAD_FAST                'svd_all_frak_python'
             2278  LOAD_CONST               0
             2280  BINARY_SUBSCR    
             2282  STORE_FAST               'u_frak'

 L. 262      2284  LOAD_FAST                'svd_all_frak_python'
             2286  LOAD_CONST               2
             2288  BINARY_SUBSCR    
             2290  LOAD_ATTR                T
             2292  STORE_FAST               'v_frak'

 L. 263      2294  LOAD_GLOBAL              np
             2296  LOAD_METHOD              dot
             2298  LOAD_FAST                't'
             2300  LOAD_FAST                'u_frak'
             2302  CALL_METHOD_2         2  '2 positional arguments'
             2304  STORE_FAST               't_frak'

 L. 264      2306  LOAD_GLOBAL              np
             2308  LOAD_METHOD              dot
             2310  LOAD_FAST                's'
             2312  LOAD_FAST                'v_frak'
             2314  CALL_METHOD_2         2  '2 positional arguments'
             2316  STORE_FAST               's_frak'

 L. 266      2318  BUILD_LIST_0          0 
             2320  STORE_FAST               'alphas'

 L. 267      2322  SETUP_LOOP         2454  'to 2454'
             2324  LOAD_GLOBAL              range
             2326  LOAD_FAST                'R'
             2328  CALL_FUNCTION_1       1  '1 positional argument'
             2330  GET_ITER         
             2332  FOR_ITER           2452  'to 2452'
             2334  STORE_FAST               'r'

 L. 268      2336  LOAD_GLOBAL              np
             2338  LOAD_METHOD              dot
             2340  LOAD_FAST                't_frak'
             2342  LOAD_CONST               None
             2344  LOAD_CONST               None
             2346  BUILD_SLICE_2         2 
             2348  LOAD_FAST                'r'
             2350  BUILD_TUPLE_2         2 
             2352  BINARY_SUBSCR    
             2354  LOAD_ATTR                T
             2356  LOAD_FAST                't_frak'
             2358  LOAD_CONST               None
             2360  LOAD_CONST               None
             2362  BUILD_SLICE_2         2 
             2364  LOAD_FAST                'r'
             2366  BUILD_TUPLE_2         2 
             2368  BINARY_SUBSCR    
             2370  CALL_METHOD_2         2  '2 positional arguments'
             2372  STORE_FAST               'n_t_2'

 L. 269      2374  LOAD_FAST                'n_t_2'
             2376  LOAD_CONST               0
             2378  COMPARE_OP               !=
         2380_2382  POP_JUMP_IF_FALSE  2438  'to 2438'

 L. 270      2384  LOAD_GLOBAL              np
             2386  LOAD_METHOD              dot
             2388  LOAD_FAST                's_frak'
             2390  LOAD_CONST               None
             2392  LOAD_CONST               None
             2394  BUILD_SLICE_2         2 
             2396  LOAD_FAST                'r'
             2398  BUILD_TUPLE_2         2 
             2400  BINARY_SUBSCR    
             2402  LOAD_ATTR                T
             2404  LOAD_FAST                't_frak'
             2406  LOAD_CONST               None
             2408  LOAD_CONST               None
             2410  BUILD_SLICE_2         2 
             2412  LOAD_FAST                'r'
             2414  BUILD_TUPLE_2         2 
             2416  BINARY_SUBSCR    
             2418  CALL_METHOD_2         2  '2 positional arguments'
             2420  LOAD_FAST                'n_t_2'
             2422  BINARY_TRUE_DIVIDE
             2424  STORE_FAST               'val'

 L. 271      2426  LOAD_FAST                'alphas'
             2428  LOAD_METHOD              append
             2430  LOAD_FAST                'val'
             2432  CALL_METHOD_1         1  '1 positional argument'
             2434  POP_TOP          
             2436  JUMP_BACK          2332  'to 2332'
           2438_0  COME_FROM          2380  '2380'

 L. 273      2438  LOAD_FAST                'alphas'
             2440  LOAD_METHOD              append
             2442  LOAD_CONST               0
             2444  CALL_METHOD_1         1  '1 positional argument'
             2446  POP_TOP          
         2448_2450  JUMP_BACK          2332  'to 2332'
             2452  POP_BLOCK        
           2454_0  COME_FROM_LOOP     2322  '2322'

 L. 274      2454  LOAD_FAST                'mode'
             2456  LOAD_STR                 'reg'
             2458  COMPARE_OP               ==
         2460_2462  POP_JUMP_IF_FALSE  2670  'to 2670'

 L. 275      2464  BUILD_MAP_0           0 
             2466  STORE_FAST               'B'

 L. 276      2468  SETUP_LOOP         2668  'to 2668'
             2470  LOAD_GLOBAL              range
             2472  LOAD_FAST                'K'
             2474  CALL_FUNCTION_1       1  '1 positional argument'
             2476  GET_ITER         
             2478  FOR_ITER           2666  'to 2666'
             2480  STORE_FAST               'k'

 L. 277      2482  LOAD_FAST                'u'
             2484  LOAD_GLOBAL              np
             2486  LOAD_METHOD              repeat
             2488  LOAD_FAST                'k'
             2490  LOAD_FAST                'R'
             2492  BINARY_MULTIPLY  
             2494  LOAD_FAST                'R'
             2496  CALL_METHOD_2         2  '2 positional arguments'
             2498  LOAD_GLOBAL              range
             2500  LOAD_FAST                'R'
             2502  CALL_FUNCTION_1       1  '1 positional argument'
             2504  BINARY_ADD       
             2506  LOAD_CONST               None
             2508  LOAD_CONST               None
             2510  BUILD_SLICE_2         2 
             2512  BUILD_TUPLE_2         2 
             2514  BINARY_SUBSCR    
             2516  STORE_FAST               'beta_k'

 L. 278      2518  LOAD_GLOBAL              np
             2520  LOAD_METHOD              dot
             2522  LOAD_FAST                'beta_k'
             2524  LOAD_FAST                'u_frak'
             2526  CALL_METHOD_2         2  '2 positional arguments'
             2528  STORE_FAST               'a1'

 L. 279      2530  LOAD_FAST                'u_t_r'
             2532  LOAD_FAST                'k'
             2534  BINARY_SUBSCR    
             2536  STORE_FAST               'a2'

 L. 280      2538  LOAD_GLOBAL              np
             2540  LOAD_METHOD              dot
             2542  LOAD_FAST                'u_t_r'
             2544  LOAD_FAST                'k'
             2546  BINARY_SUBSCR    
             2548  LOAD_GLOBAL              np
             2550  LOAD_METHOD              dot
             2552  LOAD_FAST                'beta_k'
             2554  LOAD_FAST                'u_frak'
             2556  CALL_METHOD_2         2  '2 positional arguments'
             2558  CALL_METHOD_2         2  '2 positional arguments'
             2560  LOAD_FAST                'B'
             2562  LOAD_FAST                'k'
             2564  STORE_SUBSCR     

 L. 281      2566  SETUP_LOOP         2630  'to 2630'
             2568  LOAD_GLOBAL              range
             2570  LOAD_FAST                'R'
             2572  CALL_FUNCTION_1       1  '1 positional argument'
             2574  GET_ITER         
             2576  FOR_ITER           2628  'to 2628'
             2578  STORE_FAST               'r'

 L. 282      2580  LOAD_FAST                'B'
             2582  LOAD_FAST                'k'
             2584  BINARY_SUBSCR    
             2586  LOAD_CONST               None
             2588  LOAD_CONST               None
             2590  BUILD_SLICE_2         2 
             2592  LOAD_FAST                'r'
             2594  BUILD_TUPLE_2         2 
             2596  BINARY_SUBSCR    
             2598  LOAD_FAST                'alphas'
             2600  LOAD_FAST                'r'
             2602  BINARY_SUBSCR    
             2604  BINARY_MULTIPLY  
             2606  LOAD_FAST                'B'
             2608  LOAD_FAST                'k'
             2610  BINARY_SUBSCR    
             2612  LOAD_CONST               None
             2614  LOAD_CONST               None
             2616  BUILD_SLICE_2         2 
             2618  LOAD_FAST                'r'
             2620  BUILD_TUPLE_2         2 
             2622  STORE_SUBSCR     
         2624_2626  JUMP_BACK          2576  'to 2576'
             2628  POP_BLOCK        
           2630_0  COME_FROM_LOOP     2566  '2566'

 L. 283      2630  LOAD_GLOBAL              np
             2632  LOAD_METHOD              dot
             2634  LOAD_FAST                'B'
             2636  LOAD_FAST                'k'
             2638  BINARY_SUBSCR    
             2640  LOAD_GLOBAL              np
             2642  LOAD_METHOD              dot
             2644  LOAD_FAST                'v_frak'
             2646  LOAD_ATTR                T
             2648  LOAD_FAST                'v'
             2650  LOAD_ATTR                T
             2652  CALL_METHOD_2         2  '2 positional arguments'
             2654  CALL_METHOD_2         2  '2 positional arguments'
             2656  LOAD_FAST                'B'
             2658  LOAD_FAST                'k'
             2660  STORE_SUBSCR     
         2662_2664  JUMP_BACK          2478  'to 2478'
             2666  POP_BLOCK        
           2668_0  COME_FROM_LOOP     2468  '2468'
             2668  JUMP_FORWARD       2740  'to 2740'
           2670_0  COME_FROM          2460  '2460'

 L. 285      2670  LOAD_GLOBAL              np
             2672  LOAD_METHOD              sum
             2674  LOAD_FAST                't_frak'
             2676  LOAD_FAST                't_frak'
             2678  BINARY_MULTIPLY  
             2680  CALL_METHOD_1         1  '1 positional argument'
             2682  LOAD_CONST               0
             2684  COMPARE_OP               !=
         2686_2688  POP_JUMP_IF_FALSE  2736  'to 2736'

 L. 286      2690  LOAD_GLOBAL              min
             2692  LOAD_FAST                'R'
             2694  LOAD_GLOBAL              len
             2696  LOAD_GLOBAL              set
             2698  LOAD_FAST                'Y'
             2700  CALL_FUNCTION_1       1  '1 positional argument'
             2702  CALL_FUNCTION_1       1  '1 positional argument'
             2704  LOAD_CONST               1
             2706  BINARY_SUBTRACT  
             2708  CALL_FUNCTION_2       2  '2 positional arguments'
             2710  STORE_FAST               'n_components'

 L. 287      2712  LOAD_GLOBAL              LinearDiscriminantAnalysis
             2714  LOAD_FAST                'n_components'
             2716  LOAD_CONST               ('n_components',)
             2718  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2720  STORE_FAST               'B'

 L. 288      2722  LOAD_FAST                'B'
             2724  LOAD_METHOD              fit
             2726  LOAD_FAST                't'
             2728  LOAD_FAST                'Y'
             2730  CALL_METHOD_2         2  '2 positional arguments'
             2732  POP_TOP          
             2734  JUMP_FORWARD       2740  'to 2740'
           2736_0  COME_FROM          2686  '2686'

 L. 290      2736  LOAD_CONST               None
             2738  STORE_FAST               'B'
           2740_0  COME_FROM          2734  '2734'
           2740_1  COME_FROM          2668  '2668'

 L. 291      2740  LOAD_FAST                'u_t_r'
             2742  LOAD_FAST                'v'
             2744  LOAD_FAST                't_r'
             2746  LOAD_FAST                'u'
             2748  LOAD_FAST                't'
             2750  LOAD_FAST                's'

 L. 292      2752  LOAD_FAST                't_frak'
             2754  LOAD_FAST                's_frak'
             2756  LOAD_FAST                'B'
             2758  LOAD_FAST                'mu_x_s'

 L. 293      2760  LOAD_FAST                'sd_x_s'
             2762  LOAD_FAST                'mu_y'
             2764  LOAD_FAST                'sd_y'
             2766  LOAD_FAST                'R'
             2768  LOAD_FAST                'q'

 L. 294      2770  LOAD_FAST                'Ms'
             2772  LOAD_FAST                'lambd'
             2774  LOAD_CONST               ('u', 'v', 'ts', 'beta_comb', 't', 's', 't_frak', 's_frak', 'B', 'mu_x_s', 'sd_x_s', 'mu_y', 'sd_y', 'R', 'q', 'Ms', 'lambd')
             2776  BUILD_CONST_KEY_MAP_17    17 
             2778  STORE_FAST               'out'

 L. 295      2780  LOAD_FAST                'out'
             2782  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1258_0


class model_class:
    __doc__ = 'Class permitting to access the ddspls model computation results.\n\t*K* is the number of blocks in the *X* part.\n\t*p_k* is, for each block *k*, the number of variables in block *k*.\n\t*q* is the number of variables in matrix *Y*.\n\t*R* is the number of dimensions requested by the user.\n\n\tAttributes\n\t----------\n\tu : dict\n\t\ta dictionnary of length *K*. Each element is a *p_k*X*R* matrix : the weights\n\t\tper block per axis\n\tv : numpy matrix\n\t\tA *q*X*R* matrix : the weights for the *Y* part.\n\tts : dict\n\t\tlength *R*. Each element is a *n*X*K* matrix : the scores per axis per block\n\tbeta_comb : int\n\t\tthe number of components to be built, between 1 and the minimum of the\n\t\tnumber of columns of Y and the total number of co-variables among the\n\t\tall blocks (default is 1)\n\tt : \n\tmode : str\n\t\tequals to "reg" in the regression context (and default). Any other\n\t\tchoice would produce "classification" analysis.\n\terrMin_imput : float\n\t\tminimal error in the Tribe Stage of the Koh-Lanta algorithm (default\n\t\tis 1e-9)\n\tmaxIter_imput : int\n\t\tMaximal number of iterations in the Tribe Stage of the Koh-Lanta\n\t\talgorithm. If equals to 0, mean imputation is  considered (default is\n\t\t5)\n\tverbose : bool\n\t\tif TRUE, print specificities of the object (default is false)\n\tmodel : ddspls\n\t\tthe built model according to previous parameters\n\n\t'

    def __init__(self, u, v, ts, beta_comb, t, s, t_frak, s_frak, B, mu_x_s, sd_x_s, mu_y, sd_y, R, q, Ms, lambd):
        self.u = u
        self.v = v
        self.ts = ts
        self.beta_comb = beta_comb
        self.t = t
        self.s = s
        self.t_frak = t_frak
        self.s_frak = s_frak
        self.B = B
        self.mu_x_s = mu_x_s
        self.sd_x_s = sd_x_s
        self.mu_y = mu_y
        self.sd_y = sd_y
        self.R = R
        self.q = q
        self.Ms = Ms
        self.lambd = lambd


class ddspls:
    __doc__ = 'Main class of the package. Filled with propoerties of any built\n\tddsPLS model.\n\n\tAttributes\n\t----------\n\tXs : dict\n\t\ta dictionnary of the different co-factor numpy matrices of the problem\n\tY :  numpy matrix\n\t\teither a multi-variate numpy matrix defining the regression case\n\t\tresponse matrix. Or a single-column numpy matrix in case of \n\t\tclassification\n\tlambd : float\n\t\tthe regularization coefficient, between 0 and 1 (default is 0)\n\tR : int\n\t\tthe number of components to be built, between 1 and the minimum of the\n\t\tnumber of columns of Y and the total number of co-variables among the\n\t\tall blocks (default is 1)\n\tmode : str\n\t\tequals to "reg" in the regression context (and default). Any other\n\t\tchoice would produce "classification" analysis.\n\terrMin_imput : float\n\t\tminimal error in the Tribe Stage of the Koh-Lanta algorithm (default\n\t\tis 1e-9)\n\tmaxIter_imput : int\n\t\tMaximal number of iterations in the Tribe Stage of the Koh-Lanta\n\t\talgorithm. If equals to 0, mean imputation is  considered (default is\n\t\t5)\n\tverbose : bool\n\t\tif TRUE, print specificities of the object (default is false)\n\tmodel : model_class\n\t\tthe built model according to previous parameters\n\n\tMethods\n\t-------\n\tgetModel(model)\n\t\tPermits to build the Python ddsPLS model according to the chosen\n\t\tparameters.\n\tfill_X_test(X_test_0)\n\t\tInternal method which permits to estimate missing values in the\n\t\tco-variable part.\n\t'

    def __init__(self, Xs, Y, lambd=0, R=1, mode='reg', errMin_imput=1e-09, maxIter_imput=50, verbose=False, model=None):
        self.Xs = Xs
        self.Y = Y
        self.lambd = lambd
        self.R = R
        self.mode = mode
        self.errMin_imput = errMin_imput
        self.maxIter_imput = maxIter_imput
        self.verbose = verbose
        n = Xs[0].shape[0]
        if n != 1:
            self.getModel(model)
        else:
            self.model = {}

    def getModel(self, model):
        """Permits to build the Python ddsPLS model according to the chosen
                parameters. Internal method.

                Parameters
                ----------
                model : ddspls, optional
                        The model default value given to the method. Most o times this
                         method is not used.
                """
        if model == None:
            Xs = self.Xs
            Y = self.Y
            lambd = self.lambd
            R = self.R
            mode = self.mode
            errMin_imput = self.errMin_imput
            maxIter_imput = self.maxIter_imput
            verbose = self.verbose
            Xs_w = reshape_dict(Xs)
            has_converged = maxIter_imput
            id_na = {}
            K = len(Xs_w)
            na_lengths = 0
            for k in range(K):
                id_na[k] = np.where(np.isnan(Xs_w[k][:, 0]))[0]
                na_lengths = na_lengths + len(id_na[k])

            if na_lengths != 0:
                for k in range(K):
                    if len(id_na[k]) != 0:
                        mu_k = Xs_w[k].mean(0)
                        for k_ik in id_na[k]:
                            Xs_w[k][k_ik, :] = mu_k

            mod = MddsPLS_core(Xs_w, Y, lambd=lambd, R=R, mode=mode, verbose=verbose)
            if K > 1:
                mod_0 = MddsPLS_core(Xs_w, Y, lambd=lambd, R=R, mode=mode, verbose=verbose)
                if sum(sum(abs(mod_0['t']))) != 0:
                    err = 2
                    iterat = 0
                    while (iterat < maxIter_imput) & (err > errMin_imput):
                        iterat = iterat + 1
                        for k in range(K):
                            if len(id_na[k]) > 0:
                                no_k = np.arange(K)
                                np.deleteno_kk
                                i_k = id_na[k]
                                Xs_i = mod_0['s']
                                Xs_i = np.delete(Xs_i, i_k, axis=0)
                                newX_i = mod_0['s'][i_k, :]
                                u_k = mod_0['u'][k].T[0]
                                Var_selected_k = np.where(abs(u_k) != 0)[0]
                                if len(Var_selected_k) > 0:
                                    Y_i_k = Xs_w[k][:, Var_selected_k]
                                    Y_i_k = np.delete(Y_i_k, i_k, axis=0)
                                    model_here_0 = MddsPLS_core(Xs_i, Y_i_k, lambd=lambd)
                                    model_here = model_class(u=(model_here_0['u']), v=(model_here_0['v']),
                                      ts=(model_here_0['ts']),
                                      beta_comb=(model_here_0['beta_comb']),
                                      t=(model_here_0['t']),
                                      s=(model_here_0['s']),
                                      t_frak=(model_here_0['t_frak']),
                                      s_frak=(model_here_0['s_frak']),
                                      B=(model_here_0['B']),
                                      mu_x_s=(model_here_0['mu_x_s']),
                                      sd_x_s=(model_here_0['sd_x_s']),
                                      mu_y=(model_here_0['mu_y']),
                                      sd_y=(model_here_0['sd_y']),
                                      R=(model_here_0['R']),
                                      q=(model_here_0['q']),
                                      Ms=(model_here_0['Ms']),
                                      lambd=(model_here_0['lambd']))
                                    mod_i_k = ddspls(Xs=Xs_i, Y=Y_i_k, lambd=lambd, R=R, model=model_here,
                                      maxIter_imput=maxIter_imput,
                                      mode='reg')
                                    out = mod_i_k.predict(newX_i)
                                    for i_var in range(len(Var_selected_k)):
                                        var = Var_selected_k[i_var]
                                        Xs_w[k][(i_k, var)] = out[:, i_var].T

                        mod = MddsPLS_core(Xs_w, Y, lambd=lambd, R=R, mode=mode)
                        if sum(sum(abs(mod['t']))) != 0:
                            err = 0
                            for r in range(R):
                                n_new = np.sqrt(sum(np.square(mod['t_frak'][:, r])))
                                n_0 = np.sqrt(sum(np.square(mod_0['t_frak'][:, r])))
                                if n_new * n_0 != 0:
                                    err_r = 1 - abs(np.dotmod['t_frak'][:, r].Tmod_0['t_frak'][:, r]) / (n_new * n_0)
                                    err = err + err_r

                        else:
                            err = 0
                        if iterat >= maxIter_imput:
                            has_converged = 0
                        if err < errMin_imput:
                            has_converged = iterat
                        mod_0 = mod

            self.model = model_class(u=(mod['u']), v=(mod['v']), ts=(mod['ts']), beta_comb=(mod['beta_comb']),
              t=(mod['t']),
              s=(mod['s']),
              t_frak=(mod['t_frak']),
              s_frak=(mod['s_frak']),
              B=(mod['B']),
              mu_x_s=(mod['mu_x_s']),
              sd_x_s=(mod['sd_x_s']),
              mu_y=(mod['mu_y']),
              sd_y=(mod['sd_y']),
              R=(mod['R']),
              q=(mod['q']),
              Ms=(mod['Ms']),
              lambd=(mod['lambd']))
            self.has_converged = has_converged
        else:
            self.model = model

    def fill_X_test(self, X_test_0):
        """Internal method which permits to estimate missing values in the
                co-variable part. Internal method.

                Parameters
                ----------
                X_test_0 : dict
                        a dictionnary of the different co-factor numpy matrices of the
                        problem
                """
        X_test = reshape_dict(X_test_0)
        lambd, R, mod = self.lambd, self.R, self.model
        K = len(X_test)
        n = mod.t_frak.shape[0]
        id_na_test = []
        na_test_lengths = 0
        X_test_w = X_test
        pos_vars_Y_here, t_X_here, number_coeff_no_ok = {}, {}, 0
        for k in range(K):
            id_na_test.append(np.isnan(X_test[k][:, 0])[0] * 1)
            na_test_lengths = na_test_lengths + id_na_test[k]

        if na_test_lengths != 0:
            pos_ok = np.where(np.array(id_na_test) == 0)[0]
            len_pos_ok = len(pos_ok)
            t_X_here = np.zeros((n, len_pos_ok * R))
            for r in range(R):
                for id_ok_r in range(len_pos_ok):
                    t_X_here[:, r * len_pos_ok + id_ok_r] = mod.ts[r][:, pos_ok[id_ok_r]]

            u_X_here, mu_x_here, sd_x_0 = {}, {}, {}
            for id_ok_r in range(len_pos_ok):
                u_X_here[id_ok_r] = mod.u[pos_ok[id_ok_r]]
                mu_x_here[id_ok_r] = mod.mu_x_s[pos_ok[id_ok_r]]
                sd_x_0[id_ok_r] = mod.sd_x_s[pos_ok[id_ok_r]]

            pos_no_ok = range(K)
            pos_no_ok = [x for x in pos_no_ok if x not in pos_ok]
            len_pos_no_ok = len(pos_no_ok)
            for pp in range(len_pos_no_ok):
                u_pos_no_ok_pp = mod.u[pos_no_ok[pp]]
                pos_vars_Y_here[pp] = np.where(np.sum((abs(u_pos_no_ok_pp)), axis=1) != 0)[0]
                number_coeff_no_ok = number_coeff_no_ok + len(pos_vars_Y_here[pp])

            if number_coeff_no_ok != 0:
                vars_Y_here = np.zeros((n, number_coeff_no_ok))
                C_pos = 0
                for k_id in range(len_pos_no_ok):
                    vars_k_id = pos_vars_Y_here[k_id]
                    len_vars_k_id = len(vars_k_id)
                    if len_vars_k_id != 0:
                        for j in range(len_vars_k_id):
                            vars_Y_here[:, C_pos + j] = self.Xs[pos_no_ok[k_id]][:, j]

                        C_pos = C_pos + len_vars_k_id

            else:
                vars_Y_here = np.zeros((n, 1))
            model_impute_test = ddspls(Xs=t_X_here, Y=vars_Y_here, lambd=lambd,
              R=R,
              maxIter_imput=(self.maxIter_imput))
            n_test = 1
            t_X_test = np.zeros((n_test, t_X_here.shape[1]))
            K_h = len(np.where(id_na_test == False)[0])
            for r_j in range(R):
                for k_j in range(K_h):
                    kk = pos_ok[k_j]
                    xx = X_test[kk]
                    for id_xx in range(n_test):
                        variab_sd_no_0 = np.where(sd_x_0[k_j] != 0)
                        for v_sd_no_0 in variab_sd_no_0:
                            xx[(id_xx, v_sd_no_0)] = (xx[(id_xx, v_sd_no_0)] - mu_x_here[k_j][v_sd_no_0]) / sd_x_0[k_j][v_sd_no_0]

                    t_X_test[:, r_j * K_h + k_j] = np.dotxxu_X_here[k_j][:, r_j]

            res = model_impute_test.predict(t_X_test)
            C_pos = 0
            for k_id in range(len_pos_no_ok):
                vars_k_id = pos_vars_Y_here[k_id]
                len_v_k_id = len(vars_k_id)
                pos_n_k_h = pos_no_ok[k_id]
                X_test_w[pos_n_k_h][0, :] = mod.mu_x_s[pos_n_k_h]
                if len_v_k_id != 0:
                    for vv in range(len_v_k_id):
                        X_test_w[pos_n_k_h][(0, vars_k_id[vv])] = res[(0, C_pos + vv)]

                    C_pos = C_pos + len_v_k_id

        return X_test_w

    def predict(self, newX):
        """Estimate Y values for new individuals according to previously a
                built model.

                Parameters
                ----------
                newX : dict
                        The dictionnary of matrices corresponding to the test data set.
                """
        newX_w = reshape_dict(newX)
        K = len(newX_w)
        n_new = newX_w[0].shape[0]
        mod = self.model
        R = mod.R
        q = mod.q
        if n_new == 1:
            id_na_test, na_test_lengths = [], 0
            na_test_lengths = 0
            for k in range(K):
                id_na_test.append(np.isnan(newX_w[k][(0, 0)]) * 1)
                na_test_lengths = na_test_lengths + id_na_test[k]

            if na_test_lengths != 0:
                if (K > 1) & (self.maxIter_imput > 0):
                    newX_w = self.fill_X_test(newX)
                else:
                    for k in range(K):
                        if id_na_test[k] != 0:
                            newX_w[k][0, :] = mod.mu_x_s[k]

            for k in range(K):
                variab_sd_no_0 = np.where(mod.sd_x_s[k] != 0)[0]
                for v_sd_no_0 in variab_sd_no_0:
                    newX_w[k][(0, v_sd_no_0)] = (newX_w[k][(0, v_sd_no_0)] - mod.mu_x_s[k][v_sd_no_0]) / mod.sd_x_s[k][v_sd_no_0]

            if self.mode == 'reg':
                newY = np.zeros((1, q))
                for k in range(K):
                    newY = newY + np.dotnewX_w[k]mod.B[k]

                for q_i in range(q):
                    newY[(0, q_i)] = newY[(0, q_i)] * mod.sd_y[q_i] + mod.mu_y[q_i]

            else:
                if mod.B != None:
                    t_r_all = np.zeros((1, K * R))
                    for k in range(K):
                        for r in range(R):
                            t_r_all[(0, np.repeat(K * r)K + range(K))] = np.dotnewX_w[k]mod.u[k][:, r]

                    df_new = np.dott_r_allmod.beta_comb
                    newY = mod.B.predict(df_new)
                else:
                    newY = rd.sampleset(self.Y)1
        else:
            if self.mode == 'reg':
                newY = np.zeros((n_new, q))
            else:
                newY = []
            for i_new in range(n_new):
                t_i_new = {}
                for k in range(K):
                    t_i_new[k] = newX_w[k][i_new:i_new + 1, :]

                if self.mode == 'reg':
                    newY[i_new, :] = self.predict(t_i_new)
                else:
                    newY.append(self.predict(t_i_new)[0])

        return newY


def perf_ddspls(Xs, Y, lambd_min=0, lambd_max=None, n_lambd=1, lambds=None, R=1, kfolds='loo', mode='reg', fold_fixed=None, errMin_imput=1e-09, maxIter_imput=5, NCORES=1):
    """Permits to start cross-validation processes. A parallelized procedure
        is accessible thanks to parameter NCORES, when >1.

        Parameters
        ----------
        Xs : dict
                a dictionnary of the different co-factor numpy matrices of the problem
        Y :  numpy matrix
                either a multi-variate numpy matrix defining the regression case
                response matrix. Or a single-column numpy matrix in case of
                classification
        lambd_min : float
                minimal value of lambd to be tested (default is *0*)
        lambd_max : float
                maximal value of lambd to be tested (default is *None*). If *None*, the
                highest value which permits to not get an empty model is chosen
        n_lambda : int
                number of lambd to be testes, regularly sampled between lambd_min and
                lambd_max (default is 1)
        lambds : sdarray
                if the user want to test specific values of lambd, else put to *None*
        R : int
                the number of components to be built, between 1 and the minimum of the
                number of columns of Y and the total number of co-variables among the
                all blocks (default is 1)
        kfolds : int or str
                the number of folds in the cross-validation process. In case equal to
                *loo*, then leave-one-out cross-validation is perfomed (default value).
                If equal to *fixed* then *fold_fixed* argument is considered
        mode : str
                equals to "reg" in the regression context (and default). Any other
                choice would produce "classification" analysis
        fold_fixed : sdarray
                if the user wants samples to be removed in the same time in the cross-
                validation process. This is a sdarray of length the total number of
                individuals where each is an integer defining the index of the fold.
                Default is *None* which corresponds to classical f-folds cross-
                validation. Only taken into account if *kfolds==fixed* (default is 
                *None*)
        errMin_imput : float
                minimal error in the Tribe Stage of the Koh-Lanta algorithm (default
                is 1e-9)
        maxIter_imput : int
                Maximal number of iterations in the Tribe Stage of the Koh-Lanta
                algorithm. If equals to 0, mean imputation is  considered (default is
                5)
        NCORES : int
                The number of cores to be used in the parallelized process. If equal to
                1 then no parallel structure is deployed (default is 1)
                
        """

    def expandgrid(*itrs):
        product = list(itertools_product(*itrs))
        return {i:[x[i] for x in product] for i in range(len(itrs))}

    Xs_w = reshape_dict(Xs)
    K = len(Xs_w)
    n = Xs_w[0].shape[0]
    p_s = np.repeat0K
    for i in range(K):
        p_s[i] = Xs_w[i].shape[1]

    if mode == 'reg':
        Y_w = reshape_dict(Y)[0]
        q = Y_w.shape[1]
    else:
        q = 1
        Y_w = Y
    if kfolds == 'loo':
        kfolds_w = n
        fold = range(n)
    else:
        if kfolds == 'fixed':
            fold = fold_fixed
        else:
            fold = []
            rapport = int(np.ceil(float(n) / float(kfolds)))
            val_to_sample = range(kfolds)
            for iterat in range(rapport):
                oo = rd.sampleval_to_samplekfolds
                for popo in val_to_sample:
                    pos = iterat * kfolds + popo
                    if pos < n:
                        fold.append(oo[popo])

    if lambds == None:
        if lambd_max == None:
            MMss0 = ddspls(Xs, Y, lambd=0, R=1, mode=mode,
              maxIter_imput=0).model.Ms
            K = len(MMss0)
            lambd_max_w = 0
            for k in range(K):
                lambd_max_w = max([lambd_max_w, np.max(abs(MMss0[k]))])

        else:
            lambd_max_w = lambd_max
        lambds_w = np.linspacelambd_minlambd_max_wn_lambd
    else:
        lambds_w = lambds
    try:
        iter(R)
    except TypeError:
        R = [
         R]

    try:
        iter(lambds_w)
    except TypeError:
        lambds_w = [
         lambds_w]

    paras = expandgrid(R, lambds_w, range(max(fold) + 1))
    if NCORES > len(paras[0]):
        decoupe = range(len(paras[0]))
    else:
        decoupe = []
        rapport = int(np.ceil(len(paras[0]) / float(NCORES)))
        val_to_sample = range(NCORES)
        for iterat in range(rapport):
            oo = rd.sampleval_to_sampleNCORES
            for popo in val_to_sample:
                pos = iterat * NCORES + popo
                if pos < len(paras[0]):
                    decoupe.append(oo[popo])

    paral_list = []
    for pos_decoupe in range(max(decoupe) + 1):
        dicoco = {'Xs':Xs_w, 
         'Y':Y_w,  'q':q,  'mode':mode,  'maxIter_imput':maxIter_imput, 
         'errMin_imput':errMin_imput,  'paras':paras, 
         'decoupe':decoupe,  'pos_decoupe':pos_decoupe,  'fold':fold}
        paral_list.append(dicoco)

    NCORES_w = int(min(NCORES, len(paras[0])))
    if NCORES_w > 1:
        from multiprocessing import Pool
        p = Pool(processes=NCORES_w)
        ERRORS = p.mapgetResultparal_list
        p.terminate()
    else:
        ERRORS = getResult(paral_list[0])
    paras_out = expandgrid(R, lambds_w)
    if mode == 'reg':
        ERRORS_OUT = np.zeros((len(paras_out[0]), q))
        DF_OUT = np.zeros((len(paras_out[0]), 2 + q))
    else:
        ERRORS_OUT = []
        DF_OUT = np.zeros((len(paras_out[0]), 3))
    for i in range(len(paras_out[0])):
        R_yo = paras_out[0][i]
        lambd_yo = paras_out[1][i]
        DF_OUT[(i, range(2))] = (R_yo, lambd_yo)
        errs = []
        for koko in range(len(paral_list)):
            pos_decoupe = paral_list[koko]['pos_decoupe']
            pos_pos_decoupe = np.where(np.array(decoupe) == pos_decoupe)[0]
            R_koko = [paras[0][i_loc] for i_loc in pos_pos_decoupe]
            lambd_koko = [paras[1][i_loc] for i_loc in pos_pos_decoupe]
            for ll in range(len(R_koko)):
                if (R_koko[ll] == R_yo) & (lambd_koko[ll] == lambd_yo):
                    if mode == 'reg':
                        if len(paral_list) != 1:
                            errs.append(ERRORS[koko]['RMSE'][(ll,)])
                        else:
                            errs.append(ERRORS['RMSE'][(ll,)])
                    elif len(paral_list) != 1:
                        errs.append(ERRORS[koko][ll])
                    else:
                        errs.append(ERRORS[ll])

        DIM = len(errs)
        DIM_2 = 1
        if type(errs[0]) != float:
            DIM_2 = len(errs[0])
        elif mode == 'reg':
            ERRS_KOKO = np.zeros((DIM, DIM_2))
        else:
            ERRS_KOKO = []
        for koko in range(DIM):
            if mode == 'reg':
                ERRS_KOKO[koko, :] = errs[koko]
            else:
                ERRS_KOKO.append(errs[koko])

        if mode == 'reg':
            aaa = np.sqrt(np.sum((ERRS_KOKO * ERRS_KOKO), axis=0) / DIM)
            for ppp in range(len(aaa)):
                DF_OUT[(i, 2 + ppp)] = aaa[ppp]

        else:
            ERRORS_OUT.append(np.sum(ERRS_KOKO) / DIM)

    if mode != 'reg':
        for iii in range(len(ERRORS_OUT)):
            DF_OUT[iii, 2:DF_OUT.shape[1]] = ERRORS_OUT[iii]

    return DF_OUT