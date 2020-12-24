# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\elastic3rd\crystal\deform.py
# Compiled at: 2020-01-13 10:19:02
# Size of source mod 2**32: 5061 bytes
import numpy as np

def deform_mode(strain, flag):
    strain = float(strain)
    if flag == 1:
        STRAIN = np.array([strain, 0, 0, 0, 0, 0])
    else:
        if flag == 2:
            STRAIN = np.array([strain, strain, 0, 0, 0, 0])
        else:
            if flag == 3:
                STRAIN = np.array([strain, strain, strain, 0, 0, 0])
            else:
                if flag == 4:
                    STRAIN = np.array([strain, 0, 0, 2.0 * strain, 0, 0])
                else:
                    if flag == 5:
                        STRAIN = np.array([strain, 0, 0, 0, 0, 2.0 * strain])
                    else:
                        if flag == 6:
                            STRAIN = np.array([0, 0, 0, 2.0 * strain, 2.0 * strain, 2.0 * strain])
                        else:
                            if flag == 7:
                                STRAIN = np.array([0, strain, 0, 0, 0, 0])
                            else:
                                if flag == 8:
                                    STRAIN = np.array([0, 0, strain, 0, 0, 0])
                                else:
                                    if flag == 9:
                                        STRAIN = np.array([0, strain, strain, 0, 0, 0])
                                    else:
                                        if flag == 10:
                                            STRAIN = np.array([0, 0, 0, 2.0 * strain, 0, 0])
                                        else:
                                            if flag == 11:
                                                STRAIN = np.array([0, 0, strain, 0, 0, 2.0 * strain])
                                            else:
                                                if flag == 12:
                                                    STRAIN = np.array([0, strain, 0, 2.0 * strain, 0, 0])
                                                else:
                                                    if flag == 13:
                                                        STRAIN = np.array([0, strain, 0, 0, 2.0 * strain, 0])
                                                    else:
                                                        if flag == 14:
                                                            STRAIN = np.array([0, 0, strain, 0, 2.0 * strain, 0])
                                                        else:
                                                            if flag == 15:
                                                                STRAIN = np.array([strain, 0, strain, 2.0 * strain, 0, 0])
                                                            else:
                                                                if flag == 16:
                                                                    STRAIN = np.array([strain, strain, 0, 0, 2.0 * strain, 0])
                                                                return STRAIN


def vec2matrix(StrainVerctor):
    e1, e2, e3, e4, e5, e6 = StrainVerctor
    e4 = e4 / 2.0
    e5 = e5 / 2.0
    e6 = e6 / 2.0
    StrainMatrix = np.array([[e1, e6, e5], [e6, e2, e4], [e5, e4, e3]])
    return StrainMatrix


def matrix2vec(StrainMatrix):
    if not is_strain_matrix(StrainMatrix):
        StrainVerctor = np.array([0, 0, 0, 0, 0, 0])
        print('Warning: The format of input strain matrix is not correct. And it is set as zeros')
        return StrainVerctor
    e1 = StrainMatrix[0][0]
    e2 = StrainMatrix[1][1]
    e3 = StrainMatrix[2][2]
    e4 = 2.0 * StrainMatrix[1][2]
    e5 = 2.0 * StrainMatrix[0][2]
    e6 = 2.0 * StrainMatrix[0][1]
    StrainVerctor = np.array([e1, e2, e3, e4, e5, e6])
    return StrainVerctor


def is_strain_matrix--- This code section failed: ---

 L.  70         0  LOAD_FAST                'StrainMatrix'
                2  LOAD_ATTR                shape
                4  UNPACK_SEQUENCE_2     2 
                6  STORE_FAST               'm'
                8  STORE_FAST               'n'

 L.  71        10  LOAD_FAST                'm'
               12  LOAD_CONST               3
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    26  'to 26'
               18  LOAD_FAST                'n'
               20  LOAD_CONST               3
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     38  'to 38'
             26_0  COME_FROM            16  '16'

 L.  72        26  LOAD_GLOBAL              print
               28  LOAD_STR                 'Error: The size of input strain matrix is not 3 by 3!'
               30  CALL_FUNCTION_1       1  ''
               32  POP_TOP          

 L.  73        34  LOAD_CONST               False
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'

 L.  75        38  LOAD_GLOBAL              range
               40  LOAD_CONST               1
               42  LOAD_CONST               3
               44  CALL_FUNCTION_2       2  ''
               46  GET_ITER         
               48  FOR_ITER            110  'to 110'
               50  STORE_FAST               'i'

 L.  76        52  LOAD_GLOBAL              range
               54  LOAD_CONST               0
               56  LOAD_FAST                'i'
               58  CALL_FUNCTION_2       2  ''
               60  GET_ITER         
             62_0  COME_FROM            88  '88'
               62  FOR_ITER            108  'to 108'
               64  STORE_FAST               'j'

 L.  77        66  LOAD_FAST                'StrainMatrix'
               68  LOAD_FAST                'i'
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'j'
               74  BINARY_SUBSCR    
               76  LOAD_FAST                'StrainMatrix'
               78  LOAD_FAST                'j'
               80  BINARY_SUBSCR    
               82  LOAD_FAST                'i'
               84  BINARY_SUBSCR    
               86  COMPARE_OP               !=
               88  POP_JUMP_IF_FALSE    62  'to 62'

 L.  78        90  LOAD_GLOBAL              print
               92  LOAD_STR                 'Warning: The input strain matrix is not symmtry!'
               94  CALL_FUNCTION_1       1  ''
               96  POP_TOP          

 L.  79        98  POP_TOP          
              100  POP_TOP          
              102  LOAD_CONST               False
              104  RETURN_VALUE     
              106  JUMP_BACK            62  'to 62'
              108  JUMP_BACK            48  'to 48'

 L.  80       110  LOAD_CONST               True
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 100


def strain2deformgrad(StrainMatrix):
    Y = 2 * StrainMatrix + 1 * np.eye(3)
    D, V = eigv(Y)
    VT = V.T
    DeformGrad = V.dot(np.sqrt(D)).dot(VT)
    return DeformGrad


def strain2deformgrad2(StrMat):
    DeformGrad = np.zeros((3, 3))
    for i in range03:
        for j in range03:
            if i == j:
                deltaij = 1
            else:
                deltaij = 0
            DeformGrad[(i, j)] = deltaij + StrMat[(i, j)]
            for k in range03:
                DeformGrad[(i, j)] = DeformGrad[(i, j)] - 0.5 * StrMat[(k, i)] * StrMat[(k, j)]
                for l in range03:
                    DeformGrad[(i, j)] = DeformGrad[(i, j)] + 0.5 * StrMat[(k, i)] * StrMat[(l, k)] * StrMat[(l, j)]

            else:
                return DeformGrad


def eigv(a):
    D, V = np.linalg.eigh(a)
    Dv = np.zeros((3, 3))
    for i in range03:
        Dv[(i, i)] = D[i]
    else:
        return (
         Dv, V)