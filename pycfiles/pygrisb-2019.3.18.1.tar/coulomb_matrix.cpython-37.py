# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/mbody/coulomb_matrix.py
# Compiled at: 2019-02-26 10:15:40
# Size of source mod 2**32: 12326 bytes
from itertools import product
import numpy as np
import scipy.misc as fact
from pygrisb.math.matrix_util import unitary_transform_coulomb_matrix

def U_matrix(mode, l, radial_integrals=None, U_int=None, J_hund=None, T=None):
    if 'slater' in mode:
        U_matrix = U_matrix_slater(l, radial_integrals, U_int, J_hund)
    else:
        if 'kanamori' in mode:
            U_matrix = U_matrix_kanamori(2 * l + 1, U_int, J_hund)
        else:
            raise NameError(' unsupported mode!')
    u_avg, j_avg = get_average_uj(U_matrix)
    norb = U_matrix.shape[0]
    norb2 = norb * 2
    Ufull_matrix = np.zeros((norb2, norb2, norb2, norb2), dtype=(np.complex))
    if T is not None:
        Ufull_matrix[:norb, :norb, :norb, :norb] = U_matrix
        Ufull_matrix[norb:, norb:, norb:, norb:] = U_matrix
        Ufull_matrix[:norb, :norb, norb:, norb:] = U_matrix
        Ufull_matrix[norb:, norb:, :norb, :norb] = U_matrix
        print(' u-matrix: nnz in compl_sph_harm = {}'.format(np.count_nonzero(np.abs(Ufull_matrix) > 1e-10)))
        Ufull_matrix = unitary_transform_coulomb_matrix(Ufull_matrix, T)
    else:
        Ufull_matrix[::2, ::2, ::2, ::2] = U_matrix
        Ufull_matrix[1::2, 1::2, 1::2, 1::2] = U_matrix
        Ufull_matrix[::2, ::2, 1::2, 1::2] = U_matrix
        Ufull_matrix[1::2, 1::2, ::2, ::2] = U_matrix
    print(' u-matrix: nnz in final basis = {}'.format(np.count_nonzero(np.abs(Ufull_matrix) > 1e-10)))
    return (Ufull_matrix, u_avg, j_avg)


def U_matrix_slater(l, radial_integrals=None, U_int=None, J_hund=None):
    r"""
    Calculate the full four-index U matrix being given either
    radial_integrals or U_int and J_hund.
    The convetion for the U matrix is that used to construct
    the Hamiltonians, namely:

    .. math:: H = \frac{1}{2} \sum_{ijkl,\sigma \sigma'} U_{ikjl}
            a_{i \sigma}^\dagger a_{j \sigma'}^\dagger
            a_{l \sigma'} a_{k \sigma}.

    Parameters
    ----------
    l : integer
        Angular momentum of shell being treated
        (l=2 for d shell, l=3 for f shell).
    radial_integrals : list, optional
                       Slater integrals [F0,F2,F4,..].
                       Must be provided if U_int and J_hund are not given.
                       Preferentially used to compute the U_matrix
                       if provided alongside U_int and J_hund.
    U_int : scalar, optional
            Value of the screened Hubbard interaction.
            Must be provided if radial_integrals are not given.
    J_hund : scalar, optional
             Value of the Hund's coupling.
             Must be provided if radial_integrals are not given.

    Returns
    -------
    U_matrix : float numpy array
               The four-index interaction matrix in the chosen basis.
    """
    if radial_integrals is None:
        if U_int is None:
            if J_hund is None:
                raise ValueError('U_matrix: provide either the radial_integrals or U_int and J_hund.')
    elif radial_integrals is None:
        if U_int is not None:
            if J_hund is not None:
                radial_integrals = U_J_to_radial_integrals(l, U_int, J_hund)
    elif radial_integrals is not None:
        if U_int is not None and J_hund is not None:
            if len(radial_integrals) - 1 != l:
                raise ValueError('U_matrix: inconsistency in l and number of radial_integrals provided.')
            if not np.allclose(radial_integrals, U_J_to_radial_integrals(l, U_int, J_hund)):
                print(' Warning: U_matrix: radial_integrals provided\n do not match U_int and J_hund.\n Using radial_integrals to calculate U_matrix.')
    U_matrix = np.zeros((2 * l + 1, 2 * l + 1, 2 * l + 1, 2 * l + 1), dtype=(np.float))
    m_range = range(-l, l + 1)
    for n, F in enumerate(radial_integrals):
        k = 2 * n
        for m1, m2, m3, m4 in product(m_range, m_range, m_range, m_range):
            U_matrix[(m1 + l, m3 + l, m2 + l, m4 + l)] += F * angular_matrix_element(l, k, m1, m2, m3, m4)

    return U_matrix


def U_matrix_kanamori(n_orb, U_int, J_hund):
    """
    Calculate the Kanamori U and Uprime matrices.

    Parameters
    ----------
    n_orb : integer
            Number of orbitals in basis.
    U_int : scalar
            Value of the screened Hubbard interaction.
    J_hund : scalar
             Value of the Hund's coupling.

    Returns
    -------
    U_matrix : float numpy array
               The four-index interaction matrix in the chosen basis.
    """
    U_matrix = np.zeros((n_orb, n_orb, n_orb, n_orb), dtype=(np.float))
    m_range = range(n_orb)
    for m, mp in product(m_range, m_range):
        if m == mp:
            U_matrix[(m, m, mp, mp)] = U_int
        else:
            U_matrix[(m, m, mp, mp)] = U_int - 2.0 * J_hund
            U_matrix[(m, mp, mp, m)] = J_hund
            U_matrix[(m, mp, m, mp)] = J_hund

    return U_matrix


def U_J_to_radial_integrals4(l, U, J):
    label_to_l = {'s':0, 
     'p':1,  'd':2,  'f':3}
    if isinstance(l, basestring):
        l = label_to_l[l_label]
    f_list = U_J_to_radial_integrals(l, U, J)
    for i in range(len(f_list), 4):
        f_list.append(0.0)

    return f_list


def U_J_to_radial_integrals(l, U_int, J_hund):
    """
    Determine the radial integrals F_k from U_int and J_hund.

    Parameters
    ----------
    l : integer
        Angular momentum of shell being treated
        (l=2 for d shell, l=3 for f shell).
    U_int : scalar
            Value of the screened Hubbard interaction.
    J_hund : scalar
             Value of the Hund's coupling.

    Returns
    -------
    radial_integrals : list
                       Slater integrals [F0,F2,F4,..].
    """
    F = np.zeros((l + 1), dtype=(np.float))
    F[0] = U_int
    if l == 0:
        pass
    elif l == 1:
        F[1] = J_hund * 5.0
    else:
        if l == 2:
            F[1] = J_hund * 14.0 / 1.625
            F[2] = 0.625 * F[1]
        else:
            if l == 3:
                F[1] = 6435.0 * J_hund / 539.76
                F[2] = 0.668 * F[1]
                F[3] = 0.494 * F[1]
            else:
                raise ValueError(' U_J_to_radial_integrals: implemented only for l=0,1,2,3')
    return F


def radial_integrals_to_U_J(l, F):
    """
    Determine U_int and J_hund from the radial integrals.

    Parameters
    ----------
    l : integer
        Angular momentum of shell being treated
        (l=2 for d shell, l=3 for f shell).
    F : list
        Slater integrals [F0,F2,F4,..].

    Returns
    -------
    U_int : scalar
            Value of the screened Hubbard interaction.
    J_hund : scalar
             Value of the Hund's coupling.

    """
    U_int = F[0]
    if l == 0:
        J_Hund = 0.0
    else:
        if l == 1:
            J_hund = F[1] / 5.0
        else:
            if l == 2:
                J_hund = F[1] * 1.625 / 14.0
            else:
                if l == 3:
                    J_hund = F[1] * 539.76 / 6435.0
                else:
                    raise ValueError('radial_integrals_to_U_J: implemented only for l=2,3')
    return (
     U_int, J_hund)


def angular_matrix_element(l, k, m1, m2, m3, m4):
    r"""
    Calculate the angular matrix element

    .. math::
       (2l+1)^2
       \begin{pmatrix}
            l & k & l \\
            0 & 0 & 0
       \end{pmatrix}^2
       \sum_{q=-k}^k (-1)^{m_1+m_2+q}
       \begin{pmatrix}
            l & k & l \\
         -m_1 & q & m_3
       \end{pmatrix}
       \begin{pmatrix}
            l & k  & l \\
         -m_2 & -q & m_4
       \end{pmatrix}.

    Parameters
    ----------
    l : integer
    k : integer
    m1 : integer
    m2 : integer
    m3 : integer
    m4 : integer

    Returns
    -------
    ang_mat_ele : scalar
                  Angular matrix element.

    """
    ang_mat_ele = 0
    for q in range(-k, k + 1):
        ang_mat_ele += three_j_symbol((l, -m1), (k, q), (l, m3)) * three_j_symbol((l, -m2), (k, -q), (l, m4)) * (-1.0 if (m1 + q + m2) % 2 else 1.0)

    ang_mat_ele *= (2 * l + 1) ** 2 * three_j_symbol((l, 0), (k, 0), (l, 0)) ** 2
    return ang_mat_ele


def three_j_symbol--- This code section failed: ---

 L. 300         0  LOAD_FAST                'jm1'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'j1'
                6  STORE_FAST               'm1'

 L. 301         8  LOAD_FAST                'jm2'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'j2'
               14  STORE_FAST               'm2'

 L. 302        16  LOAD_FAST                'jm3'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'j3'
               22  STORE_FAST               'm3'

 L. 304        24  LOAD_FAST                'm1'
               26  LOAD_FAST                'm2'
               28  BINARY_ADD       
               30  LOAD_FAST                'm3'
               32  BINARY_ADD       
               34  LOAD_CONST               0
               36  COMPARE_OP               !=
               38  POP_JUMP_IF_TRUE    122  'to 122'

 L. 305        40  LOAD_FAST                'm1'
               42  LOAD_FAST                'j1'
               44  UNARY_NEGATIVE   
               46  COMPARE_OP               <
               48  POP_JUMP_IF_TRUE    122  'to 122'
               50  LOAD_FAST                'm1'
               52  LOAD_FAST                'j1'
               54  COMPARE_OP               >
               56  POP_JUMP_IF_TRUE    122  'to 122'

 L. 306        58  LOAD_FAST                'm2'
               60  LOAD_FAST                'j2'
               62  UNARY_NEGATIVE   
               64  COMPARE_OP               <
               66  POP_JUMP_IF_TRUE    122  'to 122'
               68  LOAD_FAST                'm2'
               70  LOAD_FAST                'j2'
               72  COMPARE_OP               >
               74  POP_JUMP_IF_TRUE    122  'to 122'

 L. 307        76  LOAD_FAST                'm3'
               78  LOAD_FAST                'j3'
               80  UNARY_NEGATIVE   
               82  COMPARE_OP               <
               84  POP_JUMP_IF_TRUE    122  'to 122'
               86  LOAD_FAST                'm3'
               88  LOAD_FAST                'j3'
               90  COMPARE_OP               >
               92  POP_JUMP_IF_TRUE    122  'to 122'

 L. 308        94  LOAD_FAST                'j3'
               96  LOAD_FAST                'j1'
               98  LOAD_FAST                'j2'
              100  BINARY_ADD       
              102  COMPARE_OP               >
              104  POP_JUMP_IF_TRUE    122  'to 122'

 L. 309       106  LOAD_FAST                'j3'
              108  LOAD_GLOBAL              abs
              110  LOAD_FAST                'j1'
              112  LOAD_FAST                'j2'
              114  BINARY_SUBTRACT  
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  COMPARE_OP               <
              120  POP_JUMP_IF_FALSE   126  'to 126'
            122_0  COME_FROM           104  '104'
            122_1  COME_FROM            92  '92'
            122_2  COME_FROM            84  '84'
            122_3  COME_FROM            74  '74'
            122_4  COME_FROM            66  '66'
            122_5  COME_FROM            56  '56'
            122_6  COME_FROM            48  '48'
            122_7  COME_FROM            38  '38'

 L. 310       122  LOAD_CONST               0.0
              124  RETURN_VALUE     
            126_0  COME_FROM           120  '120'

 L. 312       126  LOAD_FAST                'j1'
              128  LOAD_FAST                'j2'
              130  BINARY_SUBTRACT  
              132  LOAD_FAST                'm3'
              134  BINARY_SUBTRACT  
              136  LOAD_CONST               2
              138  BINARY_MODULO    
              140  POP_JUMP_IF_FALSE   146  'to 146'
              142  LOAD_CONST               -1.0
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           140  '140'
              146  LOAD_CONST               1.0
            148_0  COME_FROM           144  '144'
              148  STORE_FAST               'three_j_sym'

 L. 313       150  LOAD_FAST                'three_j_sym'
              152  LOAD_GLOBAL              np
              154  LOAD_METHOD              sqrt

 L. 314       156  LOAD_GLOBAL              fact
              158  LOAD_FAST                'j1'
              160  LOAD_FAST                'j2'
              162  BINARY_ADD       
              164  LOAD_FAST                'j3'
              166  BINARY_SUBTRACT  
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  LOAD_GLOBAL              fact
              172  LOAD_FAST                'j1'
              174  LOAD_FAST                'j2'
              176  BINARY_SUBTRACT  
              178  LOAD_FAST                'j3'
              180  BINARY_ADD       
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  BINARY_MULTIPLY  
              186  LOAD_GLOBAL              fact
              188  LOAD_FAST                'j1'
              190  UNARY_NEGATIVE   
              192  LOAD_FAST                'j2'
              194  BINARY_ADD       
              196  LOAD_FAST                'j3'
              198  BINARY_ADD       
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  BINARY_MULTIPLY  
              204  LOAD_GLOBAL              fact
              206  LOAD_FAST                'j1'
              208  LOAD_FAST                'j2'
              210  BINARY_ADD       
              212  LOAD_FAST                'j3'
              214  BINARY_ADD       
              216  LOAD_CONST               1
              218  BINARY_ADD       
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  BINARY_TRUE_DIVIDE
              224  CALL_METHOD_1         1  '1 positional argument'
              226  INPLACE_MULTIPLY 
              228  STORE_FAST               'three_j_sym'

 L. 315       230  LOAD_FAST                'three_j_sym'
              232  LOAD_GLOBAL              np
              234  LOAD_METHOD              sqrt

 L. 316       236  LOAD_GLOBAL              fact
              238  LOAD_FAST                'j1'
              240  LOAD_FAST                'm1'
              242  BINARY_SUBTRACT  
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  LOAD_GLOBAL              fact
              248  LOAD_FAST                'j1'
              250  LOAD_FAST                'm1'
              252  BINARY_ADD       
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  BINARY_MULTIPLY  
              258  LOAD_GLOBAL              fact
              260  LOAD_FAST                'j2'
              262  LOAD_FAST                'm2'
              264  BINARY_SUBTRACT  
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  BINARY_MULTIPLY  
              270  LOAD_GLOBAL              fact
              272  LOAD_FAST                'j2'
              274  LOAD_FAST                'm2'
              276  BINARY_ADD       
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  BINARY_MULTIPLY  
              282  LOAD_GLOBAL              fact
              284  LOAD_FAST                'j3'
              286  LOAD_FAST                'm3'
              288  BINARY_SUBTRACT  
              290  CALL_FUNCTION_1       1  '1 positional argument'
              292  BINARY_MULTIPLY  
              294  LOAD_GLOBAL              fact
              296  LOAD_FAST                'j3'
              298  LOAD_FAST                'm3'
              300  BINARY_ADD       
              302  CALL_FUNCTION_1       1  '1 positional argument'
              304  BINARY_MULTIPLY  
              306  CALL_METHOD_1         1  '1 positional argument'
              308  INPLACE_MULTIPLY 
              310  STORE_FAST               'three_j_sym'

 L. 318       312  LOAD_GLOBAL              max
              314  LOAD_FAST                'j2'
              316  LOAD_FAST                'j3'
              318  BINARY_SUBTRACT  
              320  LOAD_FAST                'm1'
              322  BINARY_SUBTRACT  
              324  LOAD_FAST                'j1'
              326  LOAD_FAST                'j3'
              328  BINARY_SUBTRACT  
              330  LOAD_FAST                'm2'
              332  BINARY_ADD       
              334  LOAD_CONST               0
              336  CALL_FUNCTION_3       3  '3 positional arguments'
              338  STORE_FAST               't_min'

 L. 319       340  LOAD_GLOBAL              min
              342  LOAD_FAST                'j1'
              344  LOAD_FAST                'm1'
              346  BINARY_SUBTRACT  
              348  LOAD_FAST                'j2'
              350  LOAD_FAST                'm2'
              352  BINARY_ADD       
              354  LOAD_FAST                'j1'
              356  LOAD_FAST                'j2'
              358  BINARY_ADD       
              360  LOAD_FAST                'j3'
              362  BINARY_SUBTRACT  
              364  CALL_FUNCTION_3       3  '3 positional arguments'
              366  STORE_FAST               't_max'

 L. 321       368  LOAD_CONST               0
              370  STORE_FAST               't_sum'

 L. 322       372  SETUP_LOOP          520  'to 520'
              374  LOAD_GLOBAL              range
              376  LOAD_FAST                't_min'
              378  LOAD_FAST                't_max'
              380  LOAD_CONST               1
              382  BINARY_ADD       
              384  CALL_FUNCTION_2       2  '2 positional arguments'
              386  GET_ITER         
              388  FOR_ITER            518  'to 518'
              390  STORE_FAST               't'

 L. 323       392  LOAD_FAST                't_sum'
              394  LOAD_FAST                't'
              396  LOAD_CONST               2
              398  BINARY_MODULO    
          400_402  POP_JUMP_IF_FALSE   408  'to 408'
              404  LOAD_CONST               -1.0
              406  JUMP_FORWARD        410  'to 410'
            408_0  COME_FROM           400  '400'
              408  LOAD_CONST               1.0
            410_0  COME_FROM           406  '406'

 L. 324       410  LOAD_GLOBAL              fact
              412  LOAD_FAST                't'
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  LOAD_GLOBAL              fact
              418  LOAD_FAST                'j3'
              420  LOAD_FAST                'j2'
              422  BINARY_SUBTRACT  
              424  LOAD_FAST                'm1'
              426  BINARY_ADD       
              428  LOAD_FAST                't'
              430  BINARY_ADD       
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  BINARY_MULTIPLY  
              436  LOAD_GLOBAL              fact
              438  LOAD_FAST                'j3'
              440  LOAD_FAST                'j1'
              442  BINARY_SUBTRACT  
              444  LOAD_FAST                'm2'
              446  BINARY_SUBTRACT  
              448  LOAD_FAST                't'
              450  BINARY_ADD       
              452  CALL_FUNCTION_1       1  '1 positional argument'
              454  BINARY_MULTIPLY  
              456  LOAD_GLOBAL              fact
              458  LOAD_FAST                'j1'
              460  LOAD_FAST                'j2'
              462  BINARY_ADD       
              464  LOAD_FAST                'j3'
              466  BINARY_SUBTRACT  
              468  LOAD_FAST                't'
              470  BINARY_SUBTRACT  
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  BINARY_MULTIPLY  
              476  LOAD_GLOBAL              fact
              478  LOAD_FAST                'j1'
              480  LOAD_FAST                'm1'
              482  BINARY_SUBTRACT  
              484  LOAD_FAST                't'
              486  BINARY_SUBTRACT  
              488  CALL_FUNCTION_1       1  '1 positional argument'
              490  BINARY_MULTIPLY  
              492  LOAD_GLOBAL              fact
              494  LOAD_FAST                'j2'
              496  LOAD_FAST                'm2'
              498  BINARY_ADD       
              500  LOAD_FAST                't'
              502  BINARY_SUBTRACT  
              504  CALL_FUNCTION_1       1  '1 positional argument'
              506  BINARY_MULTIPLY  
              508  BINARY_TRUE_DIVIDE
              510  INPLACE_ADD      
              512  STORE_FAST               't_sum'
          514_516  JUMP_BACK           388  'to 388'
              518  POP_BLOCK        
            520_0  COME_FROM_LOOP      372  '372'

 L. 326       520  LOAD_FAST                'three_j_sym'
              522  LOAD_FAST                't_sum'
              524  INPLACE_MULTIPLY 
              526  STORE_FAST               'three_j_sym'

 L. 327       528  LOAD_FAST                'three_j_sym'
              530  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 530


def get_average_uj(v2e):
    m_range = range(v2e.shape[0])
    u_avg = 0
    j_avg = 0
    isum_u = 0
    isum_j = 0
    for i, j in product(m_range, m_range):
        u_avg += v2e[(i, i, j, j)]
        isum_u += 1
        if i != j:
            j_avg += v2e[(i, i, j, j)] - v2e[(i, j, j, i)]
            isum_j += 1

    u_avg /= isum_u
    if isum_j > 0:
        j_avg = u_avg - j_avg / isum_j
    return (
     u_avg, j_avg)


def get_v2e_list(lhub, l_list, imap_list, utrans_list, u_list=None, j_list=None, f_list=None):
    mode_list = [
     'manual', 'slater-condon', 'kanamori', 'slater-condon']
    if lhub > 0:
        v2e_list = []
        u_avg_list = []
        j_avg_list = []
        for i, imap in enumerate(imap_list):
            if i > imap:
                v2e_list.append(v2e_list[imap])
                u_avg_list.append(u_avg_list[imap])
                j_avg_list.append(j_avg_list[imap])
                continue
            else:
                assert len(l_list[i]) == 1, ' more than one l with lhub>0!'
                l_imp = l_list[i][0]
                utrans = utrans_list[i]
                if lhub in (1, 2):
                    v2e, u_avg, j_avg = U_matrix((mode_list[lhub]), l_imp, U_int=(u_list[i]),
                      J_hund=(j_list[i]),
                      T=utrans)
                else:
                    v2e, u_avg, j_avg = U_matrix((mode_list[lhub]), l_imp, radial_integrals=(f_list[i][:l_imp + 1]),
                      T=utrans)
            v2e_list.append(v2e)
            u_avg_list.append(u_avg)
            j_avg_list.append(j_avg)

    else:
        v2e_list = None
        u_avg_list = None
        j_avg_list = None
    return (v2e_list, u_avg_list, j_avg_list)


if __name__ == '__main__':
    l = 2
    coulomb_matrix = U_matrix('slater', l, U_int=6.7, J_hund=0.67)
    m_range = range(2 * l + 1)
    with open('coulomb_matrixp.txt', 'w') as (f):
        for m1, m2, m3, m4 in product(m_range, m_range, m_range, m_range):
            if np.abs(coulomb_matrix[(m1, m2, m3, m4)]) < 1e-08:
                continue
            f.write('{} {} {} {}  {}\n'.format(m1 + 1, m2 + 1, m3 + 1, m4 + 1, coulomb_matrix[(m1, m2, m3, m4)]))