# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/models/numba/ma_quadratic_nb.py
# Compiled at: 2020-03-22 18:42:45
# Size of source mod 2**32: 27023 bytes
from typing import Tuple
from numpy import pi, sqrt, arccos, abs, log, ones_like, zeros, zeros_like, linspace, array, atleast_2d, floor, full, inf, isnan, cos, sign, sin, atleast_1d, ndarray, nan
from numba import njit, prange
from orbits.orbits_py import z_ip_s
HALF_PI = 0.5 * pi
FOUR_PI = 4.0 * pi
INV_PI = 1 / pi

@njit(cache=False)
def ellpicb(n, k):
    """The complete elliptical integral of the third kind

    Bulirsch 1965, Numerische Mathematik, 7, 78
    Bulirsch 1965, Numerische Mathematik, 7, 353

    Adapted from L. Kreidbergs C version in BATMAN
    (Kreidberg, L. 2015, PASP 957, 127)
    (https://github.com/lkreidberg/batman)
    which is translated from J. Eastman's IDL routine
    in EXOFAST (Eastman et al. 2013, PASP 125, 83)"""
    kc = sqrt(1.0 - k * k)
    e = kc
    p = sqrt(n + 1.0)
    ip = 1.0 / p
    m0 = 1.0
    c = 1.0
    d = 1.0 / p
    for nit in range(1000):
        f = c
        c = d / p + c
        g = e / p
        d = 2.0 * (f * g + d)
        p = g + p
        g = m0
        m0 = kc + m0
        if abs(1.0 - kc / g) > 1e-08:
            kc = 2.0 * sqrt(e)
            e = kc * m0
        else:
            return HALF_PI * (c * m0 + d) / (m0 * (m0 + p))

    return 0.0


@njit(cache=False)
def ellec(k):
    a1 = 0.44325141463
    a2 = 0.0626060122
    a3 = 0.04757383546
    a4 = 0.01736506451
    b1 = 0.2499836831
    b2 = 0.09200180037
    b3 = 0.04069697526
    b4 = 0.00526449639
    m1 = 1.0 - k * k
    ee1 = 1.0 + m1 * (a1 + m1 * (a2 + m1 * (a3 + m1 * a4)))
    ee2 = m1 * (b1 + m1 * (b2 + m1 * (b3 + m1 * b4))) * log(1.0 / m1)
    return ee1 + ee2


@njit(cache=False)
def ellk(k):
    a0 = 1.38629436112
    a1 = 0.09666344259
    a2 = 0.03590092383
    a3 = 0.03742563713
    a4 = 0.01451196212
    b0 = 0.5
    b1 = 0.12498593597
    b2 = 0.06880248576
    b3 = 0.03328355346
    b4 = 0.00441787012
    m1 = 1.0 - k * k
    ek1 = a0 + m1 * (a1 + m1 * (a2 + m1 * (a3 + m1 * a4)))
    ek2 = (b0 + m1 * (b1 + m1 * (b2 + m1 * (b3 + m1 * b4)))) * log(m1)
    return ek1 - ek2


def calculate_interpolation_tables(kmin: float=0.05, kmax: float=0.2, nk: int=512, nz: int=512) -> Tuple:
    zs = linspace(0, 1 + 1.001 * kmax, nz)
    ks = linspace(kmin, kmax, nk)
    ld = zeros((nk, nz))
    le = zeros((nk, nz))
    ed = zeros((nk, nz))
    for ik, k in enumerate(ks):
        _, ld[ik, :], le[ik, :], ed[ik, :] = eval_quad_z_v(zs, k, array([[0.0, 0.0]]))

    return (ed, le, ld, ks, zs)


@njit(cache=False, parallel=False)
def eval_quad_z_v(zs, k, u: ndarray):
    """Evaluates the transit model for an array of normalized distances.

    Parameters
    ----------
    z: 1D array
        Normalized distances
    k: float
        Planet-star radius ratio
    u: 1D array
        Limb darkening coefficients

    Returns
    -------
    Transit model evaluated at `z`.

    """
    if abs(k - 0.5) < 0.0001:
        k = 0.5
    npt = len(zs)
    npb = u.shape[0]
    k2 = k ** 2
    omega = zeros(npb)
    flux = zeros((npt, npb))
    le = zeros(npt)
    ld = zeros(npt)
    ed = zeros(npt)
    for i in range(npb):
        omega[i] = 1.0 - u[(i, 0)] / 3.0 - u[(i, 1)] / 6.0

    for i in prange(npt):
        z = zs[i]
        if abs(z - k) < 1e-06:
            z += 1e-06
        if z > 1.0 + k or z < 0.0:
            flux[i, :] = 1.0
            le[i] = 0.0
            ld[i] = 0.0
            ed[i] = 0.0
            continue
        else:
            if k >= 1.0:
                if z <= k - 1.0:
                    flux[i, :] = 0.0
                    le[i] = 1.0
                    ld[i] = 1.0
                    ed[i] = 1.0
                    continue
                z2 = z ** 2
                x1 = (k - z) ** 2
                x2 = (k + z) ** 2
                x3 = k ** 2 - z ** 2
                if z >= abs(1.0 - k):
                    if z <= 1.0 + k:
                        kap1 = arccos(min((1.0 - k2 + z2) / (2.0 * z), 1.0))
                        kap0 = arccos(min((k2 + z2 - 1.0) / (2.0 * k * z), 1.0))
                        le[i] = k2 * kap0 + kap1
                        le[i] = (le[i] - 0.5 * sqrt(max(4.0 * z2 - (1.0 + z2 - k2) ** 2, 0.0))) * INV_PI
                if z <= 1.0 - k:
                    le[i] = k2
                if abs(z - k) < 0.0001 * (z + k):
                    if k == 0.5:
                        ld[i] = 0.3333333333333333 - 4.0 * INV_PI / 9.0
                        ed[i] = 0.09375
            elif z > 0.5:
                q = 0.5 / k
                Kk = ellk(q)
                Ek = ellec(q)
                ld[i] = 0.3333333333333333 + 16.0 * k / 9.0 * INV_PI * (2.0 * k2 - 1.0) * Ek - (32.0 * k ** 4 - 20.0 * k2 + 3.0) / 9.0 * INV_PI / k * Kk
                ed[i] = 0.5 * INV_PI * (kap1 + k2 * (k2 + 2.0 * z2) * kap0 - (1.0 + 5.0 * k2 + z2) / 4.0 * sqrt((1.0 - x1) * (x2 - 1.0)))
            else:
                if z < 0.5:
                    q = 2.0 * k
                    Kk = ellk(q)
                    Ek = ellec(q)
                    ld[i] = 0.3333333333333333 + 0.2222222222222222 * INV_PI * (4.0 * (2.0 * k2 - 1.0) * Ek + (1.0 - 4.0 * k2) * Kk)
                    ed[i] = k2 / 2.0 * (k2 + 2.0 * z2)
                elif z > 0.5 + abs(k - 0.5) and z < 1.0 + k or k > 0.5 and z > abs(1.0 - k):
                    if z < k:
                        q = sqrt((1.0 - (k - z) ** 2) / 4.0 / z / k)
                        Kk = ellk(q)
                        Ek = ellec(q)
                        n = 1.0 / x1 - 1.0
                        Pk = ellpicb(n, q)
                        ld[i] = 0.1111111111111111 * INV_PI / sqrt(k * z) * (((1.0 - x2) * (2.0 * x2 + x1 - 3.0) - 3.0 * x3 * (x2 - 2.0)) * Kk + 4.0 * k * z * (z2 + 7.0 * k2 - 4.0) * Ek - 3.0 * x3 / x1 * Pk)
                        if z < k:
                            ld[i] = ld[i] + 0.6666666666666666
                        ed[i] = 0.5 * INV_PI * (kap1 + k2 * (k2 + 2.0 * z2) * kap0 - (1.0 + 5.0 * k2 + z2) / 4.0 * sqrt((1.0 - x1) * (x2 - 1.0)))
                if k <= 1.0 and z <= 1.0 - k:
                    q = sqrt((x2 - x1) / (1.0 - x1))
                    Kk = ellk(q)
                    Ek = ellec(q)
                    n = x2 / x1 - 1.0
                    Pk = ellpicb(n, q)
                    ld[i] = 0.2222222222222222 * INV_PI / sqrt(1.0 - x1) * ((1.0 - 5.0 * z2 + k2 + x3 * x3) * Kk + (1.0 - x1) * (z2 + 7.0 * k2 - 4.0) * Ek - 3.0 * x3 / x1 * Pk)
                    if z < k:
                        ld[i] = ld[i] + 0.6666666666666666
                    if abs(k + z - 1.0) < 0.0001:
                        ld[i] = 0.6666666666666666 * INV_PI * arccos(1.0 - 2.0 * k) - 0.4444444444444444 * INV_PI * sqrt(k * (1.0 - k)) * (3.0 + 2.0 * k - 8.0 * k2)
                    ed[i] = k2 / 2.0 * (k2 + 2.0 * z2)
            for j in range(npb):
                flux[(i, j)] = 1.0 - ((1.0 - u[(j, 0)] - 2.0 * u[(j, 1)]) * le[i] + (u[(j, 0)] + 2.0 * u[(j, 1)]) * ld[i] + u[(j, 1)] * ed[i]) / omega[j]

    return (
     flux, ld, le, ed)


@njit(cache=False, parallel=False, fastmath=True)
def eval_quad_z_s--- This code section failed: ---

 L. 295         0  LOAD_GLOBAL              abs
                2  LOAD_FAST                'k'
                4  LOAD_CONST               0.5
                6  BINARY_SUBTRACT  
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  LOAD_CONST               0.0001
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 296        16  LOAD_CONST               0.5
               18  STORE_FAST               'k'
             20_0  COME_FROM            14  '14'

 L. 298        20  LOAD_FAST                'k'
               22  LOAD_CONST               2
               24  BINARY_POWER     
               26  STORE_FAST               'k2'

 L. 299        28  LOAD_CONST               1.0
               30  LOAD_FAST                'u'
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  LOAD_CONST               3.0
               38  BINARY_TRUE_DIVIDE
               40  BINARY_SUBTRACT  
               42  LOAD_FAST                'u'
               44  LOAD_CONST               1
               46  BINARY_SUBSCR    
               48  LOAD_CONST               6.0
               50  BINARY_TRUE_DIVIDE
               52  BINARY_SUBTRACT  
               54  STORE_FAST               'omega'

 L. 301        56  LOAD_GLOBAL              abs
               58  LOAD_FAST                'z'
               60  LOAD_FAST                'k'
               62  BINARY_SUBTRACT  
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  LOAD_CONST               1e-06
               68  COMPARE_OP               <
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 302        72  LOAD_FAST                'z'
               74  LOAD_CONST               1e-06
               76  INPLACE_ADD      
               78  STORE_FAST               'z'
             80_0  COME_FROM            70  '70'

 L. 305        80  LOAD_FAST                'z'
               82  LOAD_CONST               1.0
               84  LOAD_FAST                'k'
               86  BINARY_ADD       
               88  COMPARE_OP               >
               90  POP_JUMP_IF_TRUE    100  'to 100'
               92  LOAD_FAST                'z'
               94  LOAD_CONST               0.0
               96  COMPARE_OP               <
               98  POP_JUMP_IF_FALSE   104  'to 104'
            100_0  COME_FROM            90  '90'

 L. 306       100  LOAD_CONST               1.0
              102  RETURN_VALUE     
            104_0  COME_FROM            98  '98'

 L. 309       104  LOAD_FAST                'k'
              106  LOAD_CONST               1.0
              108  COMPARE_OP               >=
              110  POP_JUMP_IF_FALSE   128  'to 128'
              112  LOAD_FAST                'z'
              114  LOAD_FAST                'k'
              116  LOAD_CONST               1.0
              118  BINARY_SUBTRACT  
              120  COMPARE_OP               <=
              122  POP_JUMP_IF_FALSE   128  'to 128'

 L. 310       124  LOAD_CONST               0.0
              126  RETURN_VALUE     
            128_0  COME_FROM           122  '122'
            128_1  COME_FROM           110  '110'

 L. 312       128  LOAD_FAST                'z'
              130  LOAD_CONST               2
              132  BINARY_POWER     
              134  STORE_FAST               'z2'

 L. 313       136  LOAD_FAST                'k'
              138  LOAD_FAST                'z'
              140  BINARY_SUBTRACT  
              142  LOAD_CONST               2
              144  BINARY_POWER     
              146  STORE_FAST               'x1'

 L. 314       148  LOAD_FAST                'k'
              150  LOAD_FAST                'z'
              152  BINARY_ADD       
              154  LOAD_CONST               2
              156  BINARY_POWER     
              158  STORE_FAST               'x2'

 L. 315       160  LOAD_FAST                'k'
              162  LOAD_CONST               2
              164  BINARY_POWER     
              166  LOAD_FAST                'z'
              168  LOAD_CONST               2
              170  BINARY_POWER     
              172  BINARY_SUBTRACT  
              174  STORE_FAST               'x3'

 L. 320       176  LOAD_FAST                'z'
              178  LOAD_CONST               1.0
              180  LOAD_FAST                'k'
              182  BINARY_SUBTRACT  
              184  COMPARE_OP               <=
              186  POP_JUMP_IF_FALSE   194  'to 194'

 L. 321       188  LOAD_FAST                'k2'
              190  STORE_FAST               'le'
              192  JUMP_FORWARD        348  'to 348'
            194_0  COME_FROM           186  '186'

 L. 324       194  LOAD_FAST                'z'
              196  LOAD_GLOBAL              abs
              198  LOAD_CONST               1.0
              200  LOAD_FAST                'k'
              202  BINARY_SUBTRACT  
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  COMPARE_OP               >=
          208_210  POP_JUMP_IF_FALSE   348  'to 348'
              212  LOAD_FAST                'z'
              214  LOAD_CONST               1.0
              216  LOAD_FAST                'k'
              218  BINARY_ADD       
              220  COMPARE_OP               <=
          222_224  POP_JUMP_IF_FALSE   348  'to 348'

 L. 325       226  LOAD_GLOBAL              arccos
              228  LOAD_GLOBAL              min
              230  LOAD_CONST               1.0
              232  LOAD_FAST                'k2'
              234  BINARY_SUBTRACT  
              236  LOAD_FAST                'z2'
              238  BINARY_ADD       
              240  LOAD_CONST               2.0
              242  LOAD_FAST                'z'
              244  BINARY_MULTIPLY  
              246  BINARY_TRUE_DIVIDE
              248  LOAD_CONST               1.0
              250  CALL_FUNCTION_2       2  '2 positional arguments'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  STORE_FAST               'kap1'

 L. 326       256  LOAD_GLOBAL              arccos
              258  LOAD_GLOBAL              min
              260  LOAD_FAST                'k2'
              262  LOAD_FAST                'z2'
              264  BINARY_ADD       
              266  LOAD_CONST               1.0
              268  BINARY_SUBTRACT  
              270  LOAD_CONST               2.0
              272  LOAD_FAST                'k'
              274  BINARY_MULTIPLY  
              276  LOAD_FAST                'z'
              278  BINARY_MULTIPLY  
              280  BINARY_TRUE_DIVIDE
              282  LOAD_CONST               1.0
              284  CALL_FUNCTION_2       2  '2 positional arguments'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  STORE_FAST               'kap0'

 L. 327       290  LOAD_FAST                'k2'
              292  LOAD_FAST                'kap0'
              294  BINARY_MULTIPLY  
              296  LOAD_FAST                'kap1'
              298  BINARY_ADD       
              300  STORE_FAST               'le'

 L. 328       302  LOAD_FAST                'le'
              304  LOAD_CONST               0.5
              306  LOAD_GLOBAL              sqrt
              308  LOAD_GLOBAL              max
              310  LOAD_CONST               4.0
              312  LOAD_FAST                'z2'
              314  BINARY_MULTIPLY  
              316  LOAD_CONST               1.0
              318  LOAD_FAST                'z2'
              320  BINARY_ADD       
              322  LOAD_FAST                'k2'
              324  BINARY_SUBTRACT  
              326  LOAD_CONST               2
              328  BINARY_POWER     
              330  BINARY_SUBTRACT  
              332  LOAD_CONST               0.0
              334  CALL_FUNCTION_2       2  '2 positional arguments'
              336  CALL_FUNCTION_1       1  '1 positional argument'
              338  BINARY_MULTIPLY  
              340  BINARY_SUBTRACT  
              342  LOAD_GLOBAL              INV_PI
              344  BINARY_MULTIPLY  
              346  STORE_FAST               'le'
            348_0  COME_FROM           222  '222'
            348_1  COME_FROM           208  '208'
            348_2  COME_FROM           192  '192'

 L. 332       348  LOAD_GLOBAL              abs
              350  LOAD_FAST                'z'
              352  LOAD_FAST                'k'
              354  BINARY_SUBTRACT  
              356  CALL_FUNCTION_1       1  '1 positional argument'
              358  LOAD_CONST               0.0001
              360  LOAD_FAST                'z'
              362  LOAD_FAST                'k'
              364  BINARY_ADD       
              366  BINARY_MULTIPLY  
              368  COMPARE_OP               <
              370  STORE_FAST               'is_edge_at_origin'

 L. 333       372  LOAD_FAST                'k'
              374  LOAD_CONST               1.0
              376  COMPARE_OP               <=
          378_380  JUMP_IF_FALSE_OR_POP   392  'to 392'
              382  LOAD_FAST                'z'
              384  LOAD_CONST               1.0
              386  LOAD_FAST                'k'
              388  BINARY_SUBTRACT  
              390  COMPARE_OP               <=
            392_0  COME_FROM           378  '378'
              392  STORE_FAST               'is_full_transit'

 L. 336       394  LOAD_FAST                'is_edge_at_origin'
          396_398  POP_JUMP_IF_FALSE   724  'to 724'

 L. 337       400  LOAD_FAST                'k'
              402  LOAD_CONST               0.5
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   434  'to 434'

 L. 338       410  LOAD_CONST               0.3333333333333333
              412  LOAD_CONST               4.0
              414  LOAD_GLOBAL              INV_PI
              416  BINARY_MULTIPLY  
              418  LOAD_CONST               9.0
              420  BINARY_TRUE_DIVIDE
              422  BINARY_SUBTRACT  
              424  STORE_FAST               'ld'

 L. 339       426  LOAD_CONST               0.09375
              428  STORE_FAST               'ed'
          430_432  JUMP_ABSOLUTE      1284  'to 1284'
            434_0  COME_FROM           406  '406'

 L. 341       434  LOAD_FAST                'z'
              436  LOAD_CONST               0.5
              438  COMPARE_OP               >
          440_442  POP_JUMP_IF_FALSE   618  'to 618'

 L. 342       444  LOAD_CONST               0.5
              446  LOAD_FAST                'k'
              448  BINARY_TRUE_DIVIDE
              450  STORE_FAST               'q'

 L. 343       452  LOAD_GLOBAL              ellk
              454  LOAD_FAST                'q'
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  STORE_FAST               'Kk'

 L. 344       460  LOAD_GLOBAL              ellec
              462  LOAD_FAST                'q'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  STORE_FAST               'Ek'

 L. 345       468  LOAD_CONST               0.3333333333333333
              470  LOAD_CONST               16.0
              472  LOAD_FAST                'k'
              474  BINARY_MULTIPLY  
              476  LOAD_CONST               9.0
              478  BINARY_TRUE_DIVIDE
              480  LOAD_GLOBAL              INV_PI
              482  BINARY_MULTIPLY  
              484  LOAD_CONST               2.0
              486  LOAD_FAST                'k2'
              488  BINARY_MULTIPLY  
              490  LOAD_CONST               1.0
              492  BINARY_SUBTRACT  
              494  BINARY_MULTIPLY  
              496  LOAD_FAST                'Ek'
              498  BINARY_MULTIPLY  
              500  BINARY_ADD       

 L. 346       502  LOAD_CONST               32.0
              504  LOAD_FAST                'k'
              506  LOAD_CONST               4
              508  BINARY_POWER     
              510  BINARY_MULTIPLY  
              512  LOAD_CONST               20.0
              514  LOAD_FAST                'k2'
              516  BINARY_MULTIPLY  
              518  BINARY_SUBTRACT  
              520  LOAD_CONST               3.0
              522  BINARY_ADD       
              524  LOAD_CONST               9.0
              526  BINARY_TRUE_DIVIDE
              528  LOAD_GLOBAL              INV_PI
              530  BINARY_MULTIPLY  
              532  LOAD_FAST                'k'
              534  BINARY_TRUE_DIVIDE
              536  LOAD_FAST                'Kk'
              538  BINARY_MULTIPLY  
              540  BINARY_SUBTRACT  
              542  STORE_FAST               'ld'

 L. 347       544  LOAD_CONST               0.5
              546  LOAD_GLOBAL              INV_PI
              548  BINARY_MULTIPLY  
              550  LOAD_FAST                'kap1'
              552  LOAD_FAST                'k2'
              554  LOAD_FAST                'k2'
              556  LOAD_CONST               2.0
              558  LOAD_FAST                'z2'
              560  BINARY_MULTIPLY  
              562  BINARY_ADD       
              564  BINARY_MULTIPLY  
              566  LOAD_FAST                'kap0'
              568  BINARY_MULTIPLY  
              570  BINARY_ADD       
              572  LOAD_CONST               1.0
              574  LOAD_CONST               5.0
              576  LOAD_FAST                'k2'
              578  BINARY_MULTIPLY  
              580  BINARY_ADD       
              582  LOAD_FAST                'z2'
              584  BINARY_ADD       
              586  LOAD_CONST               4.0
              588  BINARY_TRUE_DIVIDE
              590  LOAD_GLOBAL              sqrt

 L. 348       592  LOAD_CONST               1.0
              594  LOAD_FAST                'x1'
              596  BINARY_SUBTRACT  
              598  LOAD_FAST                'x2'
              600  LOAD_CONST               1.0
              602  BINARY_SUBTRACT  
              604  BINARY_MULTIPLY  
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  BINARY_MULTIPLY  
              610  BINARY_SUBTRACT  
              612  BINARY_MULTIPLY  
              614  STORE_FAST               'ed'
              616  JUMP_FORWARD       1284  'to 1284'
            618_0  COME_FROM           440  '440'

 L. 350       618  LOAD_FAST                'z'
              620  LOAD_CONST               0.5
              622  COMPARE_OP               <
          624_626  POP_JUMP_IF_FALSE  1284  'to 1284'

 L. 351       628  LOAD_CONST               2.0
              630  LOAD_FAST                'k'
              632  BINARY_MULTIPLY  
              634  STORE_FAST               'q'

 L. 352       636  LOAD_GLOBAL              ellk
              638  LOAD_FAST                'q'
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  STORE_FAST               'Kk'

 L. 353       644  LOAD_GLOBAL              ellec
              646  LOAD_FAST                'q'
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  STORE_FAST               'Ek'

 L. 354       652  LOAD_CONST               0.3333333333333333
              654  LOAD_CONST               0.2222222222222222
              656  LOAD_GLOBAL              INV_PI
              658  BINARY_MULTIPLY  
              660  LOAD_CONST               4.0
              662  LOAD_CONST               2.0
              664  LOAD_FAST                'k2'
              666  BINARY_MULTIPLY  
              668  LOAD_CONST               1.0
              670  BINARY_SUBTRACT  
              672  BINARY_MULTIPLY  
              674  LOAD_FAST                'Ek'
              676  BINARY_MULTIPLY  
              678  LOAD_CONST               1.0
              680  LOAD_CONST               4.0
              682  LOAD_FAST                'k2'
              684  BINARY_MULTIPLY  
              686  BINARY_SUBTRACT  
              688  LOAD_FAST                'Kk'
              690  BINARY_MULTIPLY  
              692  BINARY_ADD       
              694  BINARY_MULTIPLY  
              696  BINARY_ADD       
              698  STORE_FAST               'ld'

 L. 355       700  LOAD_FAST                'k2'
              702  LOAD_CONST               2.0
              704  BINARY_TRUE_DIVIDE
              706  LOAD_FAST                'k2'
              708  LOAD_CONST               2.0
              710  LOAD_FAST                'z2'
              712  BINARY_MULTIPLY  
              714  BINARY_ADD       
              716  BINARY_MULTIPLY  
              718  STORE_FAST               'ed'
          720_722  JUMP_FORWARD       1284  'to 1284'
            724_0  COME_FROM           396  '396'

 L. 358       724  LOAD_FAST                'is_full_transit'
          726_728  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 359       730  LOAD_GLOBAL              sqrt
              732  LOAD_FAST                'x2'
              734  LOAD_FAST                'x1'
              736  BINARY_SUBTRACT  
              738  LOAD_CONST               1.0
              740  LOAD_FAST                'x1'
              742  BINARY_SUBTRACT  
              744  BINARY_TRUE_DIVIDE
              746  CALL_FUNCTION_1       1  '1 positional argument'
              748  STORE_FAST               'q'

 L. 360       750  LOAD_GLOBAL              ellk
              752  LOAD_FAST                'q'
              754  CALL_FUNCTION_1       1  '1 positional argument'
              756  STORE_FAST               'Kk'

 L. 361       758  LOAD_GLOBAL              ellec
              760  LOAD_FAST                'q'
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  STORE_FAST               'Ek'

 L. 362       766  LOAD_FAST                'x2'
              768  LOAD_FAST                'x1'
              770  BINARY_TRUE_DIVIDE
              772  LOAD_CONST               1.0
              774  BINARY_SUBTRACT  
              776  STORE_FAST               'n'

 L. 363       778  LOAD_GLOBAL              ellpicb
              780  LOAD_FAST                'n'
              782  LOAD_FAST                'q'
              784  CALL_FUNCTION_2       2  '2 positional arguments'
              786  STORE_FAST               'Pk'

 L. 364       788  LOAD_CONST               0.2222222222222222
              790  LOAD_GLOBAL              INV_PI
              792  BINARY_MULTIPLY  
              794  LOAD_GLOBAL              sqrt
              796  LOAD_CONST               1.0
              798  LOAD_FAST                'x1'
              800  BINARY_SUBTRACT  
              802  CALL_FUNCTION_1       1  '1 positional argument'
              804  BINARY_TRUE_DIVIDE

 L. 365       806  LOAD_CONST               1.0
              808  LOAD_CONST               5.0
              810  LOAD_FAST                'z2'
              812  BINARY_MULTIPLY  
              814  BINARY_SUBTRACT  
              816  LOAD_FAST                'k2'
              818  BINARY_ADD       
              820  LOAD_FAST                'x3'
              822  LOAD_FAST                'x3'
              824  BINARY_MULTIPLY  
              826  BINARY_ADD       
              828  LOAD_FAST                'Kk'
              830  BINARY_MULTIPLY  
              832  LOAD_CONST               1.0
              834  LOAD_FAST                'x1'
              836  BINARY_SUBTRACT  
              838  LOAD_FAST                'z2'
              840  LOAD_CONST               7.0
              842  LOAD_FAST                'k2'
              844  BINARY_MULTIPLY  
              846  BINARY_ADD       
              848  LOAD_CONST               4.0
              850  BINARY_SUBTRACT  
              852  BINARY_MULTIPLY  
              854  LOAD_FAST                'Ek'
              856  BINARY_MULTIPLY  
              858  BINARY_ADD       
              860  LOAD_CONST               3.0
              862  LOAD_FAST                'x3'
              864  BINARY_MULTIPLY  
              866  LOAD_FAST                'x1'
              868  BINARY_TRUE_DIVIDE
              870  LOAD_FAST                'Pk'
              872  BINARY_MULTIPLY  
              874  BINARY_SUBTRACT  
              876  BINARY_MULTIPLY  
              878  STORE_FAST               'ld'

 L. 366       880  LOAD_FAST                'z'
              882  LOAD_FAST                'k'
              884  COMPARE_OP               <
          886_888  POP_JUMP_IF_FALSE   898  'to 898'

 L. 367       890  LOAD_FAST                'ld'
              892  LOAD_CONST               0.6666666666666666
              894  BINARY_ADD       
              896  STORE_FAST               'ld'
            898_0  COME_FROM           886  '886'

 L. 368       898  LOAD_GLOBAL              abs
              900  LOAD_FAST                'k'
              902  LOAD_FAST                'z'
              904  BINARY_ADD       
              906  LOAD_CONST               1.0
              908  BINARY_SUBTRACT  
              910  CALL_FUNCTION_1       1  '1 positional argument'
              912  LOAD_CONST               0.0001
              914  COMPARE_OP               <
          916_918  POP_JUMP_IF_FALSE   988  'to 988'

 L. 369       920  LOAD_CONST               0.6666666666666666
              922  LOAD_GLOBAL              INV_PI
              924  BINARY_MULTIPLY  
              926  LOAD_GLOBAL              arccos
              928  LOAD_CONST               1.0
              930  LOAD_CONST               2.0
              932  LOAD_FAST                'k'
              934  BINARY_MULTIPLY  
              936  BINARY_SUBTRACT  
              938  CALL_FUNCTION_1       1  '1 positional argument'
              940  BINARY_MULTIPLY  
              942  LOAD_CONST               0.4444444444444444
              944  LOAD_GLOBAL              INV_PI
              946  BINARY_MULTIPLY  
              948  LOAD_GLOBAL              sqrt
              950  LOAD_FAST                'k'
              952  LOAD_CONST               1.0
              954  LOAD_FAST                'k'
              956  BINARY_SUBTRACT  
              958  BINARY_MULTIPLY  
              960  CALL_FUNCTION_1       1  '1 positional argument'
              962  BINARY_MULTIPLY  

 L. 370       964  LOAD_CONST               3.0
              966  LOAD_CONST               2.0
              968  LOAD_FAST                'k'
              970  BINARY_MULTIPLY  
              972  BINARY_ADD       
              974  LOAD_CONST               8.0
              976  LOAD_FAST                'k2'
              978  BINARY_MULTIPLY  
              980  BINARY_SUBTRACT  
              982  BINARY_MULTIPLY  
              984  BINARY_SUBTRACT  
              986  STORE_FAST               'ld'
            988_0  COME_FROM           916  '916'

 L. 371       988  LOAD_FAST                'k2'
              990  LOAD_CONST               2.0
              992  BINARY_TRUE_DIVIDE
              994  LOAD_FAST                'k2'
              996  LOAD_CONST               2.0
              998  LOAD_FAST                'z2'
             1000  BINARY_MULTIPLY  
             1002  BINARY_ADD       
             1004  BINARY_MULTIPLY  
             1006  STORE_FAST               'ed'
         1008_1010  JUMP_FORWARD       1284  'to 1284'
           1012_0  COME_FROM           726  '726'

 L. 375      1012  LOAD_GLOBAL              sqrt
             1014  LOAD_CONST               1.0
             1016  LOAD_FAST                'k'
             1018  LOAD_FAST                'z'
             1020  BINARY_SUBTRACT  
             1022  LOAD_CONST               2
             1024  BINARY_POWER     
             1026  BINARY_SUBTRACT  
             1028  LOAD_CONST               4.0
             1030  BINARY_TRUE_DIVIDE
             1032  LOAD_FAST                'z'
             1034  BINARY_TRUE_DIVIDE
             1036  LOAD_FAST                'k'
             1038  BINARY_TRUE_DIVIDE
             1040  CALL_FUNCTION_1       1  '1 positional argument'
             1042  STORE_FAST               'q'

 L. 376      1044  LOAD_GLOBAL              ellk
             1046  LOAD_FAST                'q'
             1048  CALL_FUNCTION_1       1  '1 positional argument'
             1050  STORE_FAST               'Kk'

 L. 377      1052  LOAD_GLOBAL              ellec
             1054  LOAD_FAST                'q'
             1056  CALL_FUNCTION_1       1  '1 positional argument'
             1058  STORE_FAST               'Ek'

 L. 378      1060  LOAD_CONST               1.0
             1062  LOAD_FAST                'x1'
             1064  BINARY_TRUE_DIVIDE
             1066  LOAD_CONST               1.0
             1068  BINARY_SUBTRACT  
             1070  STORE_FAST               'n'

 L. 379      1072  LOAD_GLOBAL              ellpicb
             1074  LOAD_FAST                'n'
             1076  LOAD_FAST                'q'
             1078  CALL_FUNCTION_2       2  '2 positional arguments'
             1080  STORE_FAST               'Pk'

 L. 380      1082  LOAD_CONST               0.1111111111111111
             1084  LOAD_GLOBAL              INV_PI
             1086  BINARY_MULTIPLY  
             1088  LOAD_GLOBAL              sqrt
             1090  LOAD_FAST                'k'
             1092  LOAD_FAST                'z'
             1094  BINARY_MULTIPLY  
             1096  CALL_FUNCTION_1       1  '1 positional argument'
             1098  BINARY_TRUE_DIVIDE

 L. 382      1100  LOAD_CONST               1.0
             1102  LOAD_FAST                'x2'
             1104  BINARY_SUBTRACT  
             1106  LOAD_CONST               2.0
             1108  LOAD_FAST                'x2'
             1110  BINARY_MULTIPLY  
             1112  LOAD_FAST                'x1'
             1114  BINARY_ADD       
             1116  LOAD_CONST               3.0
             1118  BINARY_SUBTRACT  
             1120  BINARY_MULTIPLY  
             1122  LOAD_CONST               3.0
             1124  LOAD_FAST                'x3'
             1126  BINARY_MULTIPLY  
             1128  LOAD_FAST                'x2'
             1130  LOAD_CONST               2.0
             1132  BINARY_SUBTRACT  
             1134  BINARY_MULTIPLY  
             1136  BINARY_SUBTRACT  
             1138  LOAD_FAST                'Kk'
             1140  BINARY_MULTIPLY  
             1142  LOAD_CONST               4.0
             1144  LOAD_FAST                'k'
             1146  BINARY_MULTIPLY  
             1148  LOAD_FAST                'z'
             1150  BINARY_MULTIPLY  
             1152  LOAD_FAST                'z2'
             1154  LOAD_CONST               7.0
             1156  LOAD_FAST                'k2'
             1158  BINARY_MULTIPLY  
             1160  BINARY_ADD       
             1162  LOAD_CONST               4.0
             1164  BINARY_SUBTRACT  
             1166  BINARY_MULTIPLY  
             1168  LOAD_FAST                'Ek'
             1170  BINARY_MULTIPLY  
             1172  BINARY_ADD       
             1174  LOAD_CONST               3.0
             1176  LOAD_FAST                'x3'
           1178_0  COME_FROM           616  '616'
             1178  BINARY_MULTIPLY  
             1180  LOAD_FAST                'x1'
             1182  BINARY_TRUE_DIVIDE
             1184  LOAD_FAST                'Pk'
             1186  BINARY_MULTIPLY  
             1188  BINARY_SUBTRACT  
             1190  BINARY_MULTIPLY  
             1192  STORE_FAST               'ld'

 L. 383      1194  LOAD_FAST                'z'
             1196  LOAD_FAST                'k'
             1198  COMPARE_OP               <
         1200_1202  POP_JUMP_IF_FALSE  1212  'to 1212'

 L. 384      1204  LOAD_FAST                'ld'
             1206  LOAD_CONST               0.6666666666666666
             1208  BINARY_ADD       
             1210  STORE_FAST               'ld'
           1212_0  COME_FROM          1200  '1200'

 L. 385      1212  LOAD_CONST               0.5
             1214  LOAD_GLOBAL              INV_PI
             1216  BINARY_MULTIPLY  
             1218  LOAD_FAST                'kap1'
             1220  LOAD_FAST                'k2'
             1222  LOAD_FAST                'k2'
             1224  LOAD_CONST               2.0
             1226  LOAD_FAST                'z2'
             1228  BINARY_MULTIPLY  
             1230  BINARY_ADD       
             1232  BINARY_MULTIPLY  
             1234  LOAD_FAST                'kap0'
             1236  BINARY_MULTIPLY  
             1238  BINARY_ADD       
             1240  LOAD_CONST               1.0
             1242  LOAD_CONST               5.0
             1244  LOAD_FAST                'k2'
             1246  BINARY_MULTIPLY  
             1248  BINARY_ADD       
             1250  LOAD_FAST                'z2'
             1252  BINARY_ADD       
             1254  LOAD_CONST               4.0
             1256  BINARY_TRUE_DIVIDE
             1258  LOAD_GLOBAL              sqrt

 L. 386      1260  LOAD_CONST               1.0
             1262  LOAD_FAST                'x1'
             1264  BINARY_SUBTRACT  
             1266  LOAD_FAST                'x2'
             1268  LOAD_CONST               1.0
             1270  BINARY_SUBTRACT  
             1272  BINARY_MULTIPLY  
             1274  CALL_FUNCTION_1       1  '1 positional argument'
             1276  BINARY_MULTIPLY  
             1278  BINARY_SUBTRACT  
             1280  BINARY_MULTIPLY  
             1282  STORE_FAST               'ed'
           1284_0  COME_FROM          1008  '1008'
           1284_1  COME_FROM           720  '720'
           1284_2  COME_FROM           624  '624'

 L. 388      1284  LOAD_CONST               1.0
             1286  LOAD_CONST               1.0
             1288  LOAD_FAST                'u'
             1290  LOAD_CONST               0
             1292  BINARY_SUBSCR    
             1294  BINARY_SUBTRACT  
             1296  LOAD_CONST               2.0
             1298  LOAD_FAST                'u'
             1300  LOAD_CONST               1
             1302  BINARY_SUBSCR    
             1304  BINARY_MULTIPLY  
             1306  BINARY_SUBTRACT  
             1308  LOAD_FAST                'le'
             1310  BINARY_MULTIPLY  
             1312  LOAD_FAST                'u'
             1314  LOAD_CONST               0
             1316  BINARY_SUBSCR    
             1318  LOAD_CONST               2.0
             1320  LOAD_FAST                'u'
             1322  LOAD_CONST               1
             1324  BINARY_SUBSCR    
             1326  BINARY_MULTIPLY  
             1328  BINARY_ADD       
             1330  LOAD_FAST                'ld'
             1332  BINARY_MULTIPLY  
             1334  BINARY_ADD       
             1336  LOAD_FAST                'u'
             1338  LOAD_CONST               1
             1340  BINARY_SUBSCR    
             1342  LOAD_FAST                'ed'
             1344  BINARY_MULTIPLY  
             1346  BINARY_ADD       
             1348  LOAD_FAST                'omega'
             1350  BINARY_TRUE_DIVIDE
             1352  BINARY_SUBTRACT  
             1354  STORE_FAST               'flux'

 L. 389      1356  LOAD_FAST                'flux'
             1358  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1178_0


@njit(cache=False, parallel=False, fastmath=True)
def eval_quad_ip(zs, k, u, c, edt, ldt, let, kt, zt):
    npb = u.shape[0]
    flux = zeros((len(zs), npb))
    omega = zeros(npb)
    dk = kt[1] - kt[0]
    dz = zt[1] - zt[0]
    for i in range(npb):
        omega[i] = 1.0 - u[(i, 0)] / 3.0 - u[(i, 1)] / 6.0

    ik = int(floor((k - kt[0]) / dk))
    ak1 = (k - kt[ik]) / dk
    ak2 = 1.0 - ak1
    ed2 = edt[ik:ik + 2, :]
    ld2 = ldt[ik:ik + 2, :]
    le2 = let[ik:ik + 2, :]
    for i in prange(len(zs)):
        z = zs[i]
        if z >= 1.0 + k or z < 0.0:
            flux[i, :] = 1.0
        else:
            iz = int(floor((z - zt[0]) / dz))
            az1 = (z - zt[iz]) / dz
            az2 = 1.0 - az1
            ed = ed2[(0, iz)] * ak2 * az2 + ed2[(1, iz)] * ak1 * az2 + ed2[(0, iz + 1)] * ak2 * az1 + ed2[(1, iz + 1)] * ak1 * az1
            ld = ld2[(0, iz)] * ak2 * az2 + ld2[(1, iz)] * ak1 * az2 + ld2[(0, iz + 1)] * ak2 * az1 + ld2[(1, iz + 1)] * ak1 * az1
            le = le2[(0, iz)] * ak2 * az2 + le2[(1, iz)] * ak1 * az2 + le2[(0, iz + 1)] * ak2 * az1 + le2[(1, iz + 1)] * ak1 * az1
            for j in range(npb):
                flux[(i, j)] = 1.0 - ((1.0 - u[(j, 0)] - 2.0 * u[(j, 1)]) * le + (u[(j, 0)] + 2.0 * u[(j, 1)]) * ld + u[(j, 1)] * ed) / omega[j]
                flux[(i, j)] = c[j] + (1.0 - c[j]) * flux[(i, j)]

    return flux


@njit(cache=False, parallel=False, fastmath=True)
def eval_quad_ip(zs, k, u, edt, ldt, let, kt, zt):
    npb = u.shape[0]
    flux = zeros((len(zs), npb))
    omega = zeros(npb)
    dk = kt[1] - kt[0]
    dz = zt[1] - zt[0]
    for i in range(npb):
        omega[i] = 1.0 - u[(i, 0)] / 3.0 - u[(i, 1)] / 6.0

    ik = int(floor((k - kt[0]) / dk))
    ak1 = (k - kt[ik]) / dk
    ak2 = 1.0 - ak1
    ed2 = edt[ik:ik + 2, :]
    ld2 = ldt[ik:ik + 2, :]
    le2 = let[ik:ik + 2, :]
    for i in prange(len(zs)):
        z = zs[i]
        if z >= 1.0 + k or z < 0.0:
            flux[i, :] = 1.0
        else:
            iz = int(floor((z - zt[0]) / dz))
            az1 = (z - zt[iz]) / dz
            az2 = 1.0 - az1
            ed = ed2[(0, iz)] * ak2 * az2 + ed2[(1, iz)] * ak1 * az2 + ed2[(0, iz + 1)] * ak2 * az1 + ed2[(1, iz + 1)] * ak1 * az1
            ld = ld2[(0, iz)] * ak2 * az2 + ld2[(1, iz)] * ak1 * az2 + ld2[(0, iz + 1)] * ak2 * az1 + ld2[(1, iz + 1)] * ak1 * az1
            le = le2[(0, iz)] * ak2 * az2 + le2[(1, iz)] * ak1 * az2 + le2[(0, iz + 1)] * ak2 * az1 + le2[(1, iz + 1)] * ak1 * az1
            for j in range(npb):
                flux[(i, j)] = 1.0 - ((1.0 - u[(j, 0)] - 2.0 * u[(j, 1)]) * le + (u[(j, 0)] + 2.0 * u[(j, 1)]) * ld + u[(j, 1)] * ed) / omega[j]

    return flux


@njit(cache=False, parallel=False, fastmath=True)
def eval_quad_ip_mp(zs, pbi, ks, u, edt, ldt, let, kt, zt):
    npb = u.shape[0]
    flux = zeros(zs.size)
    omega = zeros(npb)
    dk = kt[1] - kt[0]
    dz = zt[1] - zt[0]
    for i in range(npb):
        omega[i] = 1.0 - u[(i, 0)] / 3.0 - u[(i, 1)] / 6.0

    j = -1
    for i in prange(zs.size):
        k = ks[pbi[i]]
        z = zs[i]
        if pbi[i] != j:
            ik = int(floor((k - kt[0]) / dk))
            ak1 = (k - kt[ik]) / dk
            ak2 = 1.0 - ak1
            ed2 = edt[ik:ik + 2, :]
            ld2 = ldt[ik:ik + 2, :]
            le2 = let[ik:ik + 2, :]
        j = pbi[i]
        if z >= 1.0 + k or z < 0.0:
            flux[i] = 1.0
        else:
            iz = int(floor((z - zt[0]) / dz))
            az1 = (z - zt[iz]) / dz
            az2 = 1.0 - az1
            ed = ed2[(0, iz)] * ak2 * az2 + ed2[(1, iz)] * ak1 * az2 + ed2[(0, iz + 1)] * ak2 * az1 + ed2[(1, iz + 1)] * ak1 * az1
            ld = ld2[(0, iz)] * ak2 * az2 + ld2[(1, iz)] * ak1 * az2 + ld2[(0, iz + 1)] * ak2 * az1 + ld2[(1, iz + 1)] * ak1 * az1
            le = le2[(0, iz)] * ak2 * az2 + le2[(1, iz)] * ak1 * az2 + le2[(0, iz + 1)] * ak2 * az1 + le2[(1, iz + 1)] * ak1 * az1
            flux[i] = 1.0 - ((1.0 - u[(j, 0)] - 2.0 * u[(j, 1)]) * le + (u[(j, 0)] + 2.0 * u[(j, 1)]) * ld + u[(j, 1)] * ed) / omega[j]

    return flux


@njit(cache=False, fastmath=False)
def quadratic_interpolated_z_s(z, k, u, edt, ldt, let, kt, zt):
    dk = kt[1] - kt[0]
    dz = zt[1] - zt[0]
    omega = 1.0 - u[0] / 3.0 - u[1] / 6.0
    ik = int(floor((k - kt[0]) / dk))
    ak1 = (k - kt[ik]) / dk
    ak2 = 1.0 - ak1
    if z >= 1.0 + k or z < 0.0:
        flux = 1.0
    else:
        iz = int(floor((z - zt[0]) / dz))
        az1 = (z - zt[iz]) / dz
        az2 = 1.0 - az1
        ed = edt[(ik, iz)] * ak2 * az2 + edt[(ik + 1, iz)] * ak1 * az2 + edt[(ik, iz + 1)] * ak2 * az1 + edt[(ik + 1, iz + 1)] * ak1 * az1
        ld = ldt[(ik, iz)] * ak2 * az2 + ldt[(ik + 1, iz)] * ak1 * az2 + ldt[(ik, iz + 1)] * ak2 * az1 + ldt[(ik + 1, iz + 1)] * ak1 * az1
        le = let[(ik, iz)] * ak2 * az2 + let[(ik + 1, iz)] * ak1 * az2 + let[(ik, iz + 1)] * ak2 * az1 + let[(ik + 1, iz + 1)] * ak1 * az1
        flux = 1.0 - ((1.0 - u[0] - 2.0 * u[1]) * le + (u[0] + 2.0 * u[1]) * ld + u[1] * ed) / omega
    return flux


@njit(parallel=True, fastmath=False)
def quadratic_model_direct_v(t, k, t0, p, a, i, e, w, ldc, lcids, pbids, nsamples, exptimes, npb, es, ms, tae):
    ldc = atleast_2d(ldc)
    if ldc.shape[1] != 2 * npb:
        raise ValueError('The quadratic model needs two limb darkening coefficients per passband')
    t0, p, a, i = (atleast_1d(t0), atleast_1d(p), atleast_1d(a), atleast_1d(i))
    npv = k.shape[0]
    npt = t.size
    flux = zeros((npv, npt))
    for j in prange(npt):
        for ipv in range(npv):
            ilc = lcids[j]
            ipb = pbids[ilc]
            if k.shape[1] == 1:
                _k = k[(ipv, 0)]
            else:
                _k = k[(ipv, ipb)]
            if isnan(_k) or isnan(a[ipv]) or isnan(i[ipv]):
                flux[(ipv, j)] = inf
            else:
                for isample in range(1, nsamples[ilc] + 1):
                    time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                    z = z_ip_s(t[j] + time_offset, t0[ipv], p[ipv], a[ipv], i[ipv], e[ipv], w[ipv], es, ms, tae)
                    if z > 1.0 + _k:
                        flux[(ipv, j)] += 1.0
                    else:
                        flux[(ipv, j)] += eval_quad_z_s(z, _k, ldc[ipv, 2 * ipb:2 * (ipb + 1)])

                flux[(ipv, j)] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=True)
def quadratic_model_direct_s(t, k, t0, p, a, i, e, w, ldc, lcids, pbids, nsamples, exptimes, npb, es, ms, tae):
    ldc = atleast_1d(ldc)
    k = atleast_1d(k)
    if ldc.size != 2 * npb:
        raise ValueError('The quadratic model needs two limb darkening coefficients per passband')
    npt = t.size
    flux = zeros(npt)
    for j in prange(npt):
        ilc = lcids[j]
        ipb = pbids[ilc]
        if k.size == 1:
            _k = k[0]
        else:
            _k = k[ipb]
        if isnan(_k) or isnan(a) or isnan(i):
            flux[j] = inf
        else:
            for isample in range(1, nsamples[ilc] + 1):
                time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                z = z_ip_s(t[j] + time_offset, t0, p, a, i, e, w, es, ms, tae)
                if z > 1.0 + _k:
                    flux[j] += 1.0
                else:
                    flux[j] += eval_quad_z_s(z, _k, ldc[2 * ipb:2 * (ipb + 1)])

            flux[j] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=False)
def quadratic_model_direct_pv(t, pvp, ldc, lcids, pbids, nsamples, exptimes, npb, es, ms, tae):
    pvp = atleast_2d(pvp)
    ldc = atleast_2d(ldc)
    if ldc.shape[1] != 2 * npb:
        raise ValueError('The quadratic model needs two limb darkening coefficients per passband')
    if ldc.shape[0] != pvp.shape[0]:
        raise ValueError('The parameter array and the limb darkening coefficient array have mismatching shapes. The first dimension must match.')
    npv = pvp.shape[0]
    nk = pvp.shape[1] - 6
    npt = t.size
    flux = zeros((npv, npt))
    for j in prange(npt):
        ilc = lcids[j]
        ipb = pbids[ilc]
        for ipv in range(npv):
            t0, p, a, i, e, w = pvp[ipv, nk:]
            if nk == 1:
                k = pvp[(ipv, 0)]
            else:
                if ipb < nk:
                    k = pvp[(ipv, ipb)]
                else:
                    k = nan
            if not isnan(k):
                if isnan(a) or isnan(i):
                    flux[(ipv, j)] = inf
                    continue
                for isample in range(1, nsamples[ilc] + 1):
                    time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                    z = z_ip_s(t[j] + time_offset, t0, p, a, i, e, w, es, ms, tae)
                    if z > 1.0 + k:
                        flux[(ipv, j)] += 1.0
                    else:
                        flux[(ipv, j)] += eval_quad_z_s(z, k, ldc[ipv, 2 * ipb:2 * (ipb + 1)])

                flux[(ipv, j)] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=True)
def quadratic_model_interpolated_v(t, k, t0, p, a, i, e, w, ldc, lcids, pbids, nsamples, exptimes, npb, es, ms, tae, edt, ldt, let, kt, zt):
    t0, p, a, i, e, w = (
     atleast_1d(t0), atleast_1d(p), atleast_1d(a), atleast_1d(i), atleast_1d(e), atleast_1d(w))
    ldc = atleast_2d(ldc)
    if ldc.shape[1] != 2 * npb:
        raise ValueError('The quadratic model needs two limb darkening coefficients per passband')
    npv = k.shape[0]
    npt = t.size
    flux = zeros((npv, npt))
    for j in prange(npt):
        for ipv in range(npv):
            ilc = lcids[j]
            ipb = pbids[ilc]
            if k.shape[1] == 1:
                _k = k[(ipv, 0)]
            else:
                _k = k[(ipv, ipb)]
            if _k < kt[0] or _k > kt[(-1)] or isnan(_k) or isnan(a[ipv]) or isnan(i[ipv]):
                flux[(ipv, j)] = inf
            else:
                for isample in range(1, nsamples[ilc] + 1):
                    time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                    z = z_ip_s(t[j] + time_offset, t0[ipv], p[ipv], a[ipv], i[ipv], e[ipv], w[ipv], es, ms, tae)
                    if z > 1.0 + _k:
                        flux[(ipv, j)] += 1.0
                    else:
                        flux[(ipv, j)] += quadratic_interpolated_z_s(z, _k, ldc[ipv, 2 * ipb:2 * (ipb + 1)], edt, ldt, let, kt, zt)

                flux[(ipv, j)] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=True)
def quadratic_model_interpolated_s(t, k, t0, p, a, i, e, w, ldc, lcids, pbids, nsamples, exptimes, npb, es, ms, tae, edt, ldt, let, kt, zt):
    ldc = atleast_1d(ldc)
    k = atleast_1d(k)
    if ldc.size != 2 * npb:
        raise ValueError('The quadratic model needs two limb darkening coefficients per passband')
    npt = t.size
    flux = zeros(npt)
    for j in prange(npt):
        ilc = lcids[j]
        ipb = pbids[ilc]
        if k.size == 1:
            _k = k[0]
        else:
            _k = k[ipb]
        if _k < kt[0] or _k > kt[(-1)] or isnan(_k) or isnan(a) or isnan(i):
            flux[j] = inf
        else:
            for isample in range(1, nsamples[ilc] + 1):
                time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                z = z_ip_s(t[j] + time_offset, t0, p, a, i, e, w, es, ms, tae)
                if z > 1.0 + _k:
                    flux[j] += 1.0
                else:
                    flux[j] += quadratic_interpolated_z_s(z, _k, ldc[2 * ipb:2 * (ipb + 1)], edt, ldt, let, kt, zt)

            flux[j] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=False)
def quadratic_model_interpolated_pv--- This code section failed: ---

 L. 771         0  LOAD_GLOBAL              atleast_2d
                2  LOAD_FAST                'pvp'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'pvp'

 L. 772         8  LOAD_GLOBAL              atleast_2d
               10  LOAD_FAST                'ldc'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  STORE_FAST               'ldc'

 L. 774        16  LOAD_FAST                'ldc'
               18  LOAD_ATTR                shape
               20  LOAD_CONST               1
               22  BINARY_SUBSCR    
               24  LOAD_CONST               2
               26  LOAD_FAST                'npb'
               28  BINARY_MULTIPLY  
               30  COMPARE_OP               !=
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L. 775        34  LOAD_GLOBAL              ValueError
               36  LOAD_STR                 'The quadratic model needs two limb darkening coefficients per passband'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'

 L. 776        42  LOAD_FAST                'ldc'
               44  LOAD_ATTR                shape
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'pvp'
               52  LOAD_ATTR                shape
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L. 777        62  LOAD_GLOBAL              ValueError

 L. 778        64  LOAD_STR                 'The parameter array and the limb darkening coefficient array have mismatching shapes. The first dimension must match.'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L. 780        70  LOAD_FAST                'pvp'
               72  LOAD_ATTR                shape
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  STORE_FAST               'npv'

 L. 781        80  LOAD_FAST                'pvp'
               82  LOAD_ATTR                shape
               84  LOAD_CONST               1
               86  BINARY_SUBSCR    
               88  LOAD_CONST               6
               90  BINARY_SUBTRACT  
               92  STORE_FAST               'nk'

 L. 782        94  LOAD_FAST                't'
               96  LOAD_ATTR                size
               98  STORE_FAST               'npt'

 L. 783       100  LOAD_GLOBAL              zeros
              102  LOAD_FAST                'npv'
              104  LOAD_FAST                'npt'
              106  BUILD_TUPLE_2         2 
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  STORE_FAST               'flux'

 L. 785   112_114  SETUP_LOOP          534  'to 534'
              116  LOAD_GLOBAL              prange
              118  LOAD_FAST                'npt'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  GET_ITER         
          124_126  FOR_ITER            532  'to 532'
              128  STORE_FAST               'j'

 L. 786       130  LOAD_FAST                'lcids'
              132  LOAD_FAST                'j'
              134  BINARY_SUBSCR    
              136  STORE_FAST               'ilc'

 L. 787       138  LOAD_FAST                'pbids'
              140  LOAD_FAST                'ilc'
              142  BINARY_SUBSCR    
              144  STORE_FAST               'ipb'

 L. 789   146_148  SETUP_LOOP          530  'to 530'
              150  LOAD_GLOBAL              range
              152  LOAD_FAST                'npv'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  GET_ITER         
          158_160  FOR_ITER            528  'to 528'
              162  STORE_FAST               'ipv'

 L. 790       164  LOAD_FAST                'pvp'
              166  LOAD_FAST                'ipv'
              168  LOAD_FAST                'nk'
              170  LOAD_CONST               None
              172  BUILD_SLICE_2         2 
              174  BUILD_TUPLE_2         2 
              176  BINARY_SUBSCR    
              178  UNPACK_SEQUENCE_6     6 
              180  STORE_FAST               't0'
              182  STORE_FAST               'p'
              184  STORE_FAST               'a'
              186  STORE_FAST               'i'
              188  STORE_FAST               'e'
              190  STORE_FAST               'w'

 L. 792       192  LOAD_FAST                'nk'
              194  LOAD_CONST               1
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   214  'to 214'

 L. 793       200  LOAD_FAST                'pvp'
              202  LOAD_FAST                'ipv'
              204  LOAD_CONST               0
              206  BUILD_TUPLE_2         2 
              208  BINARY_SUBSCR    
              210  STORE_FAST               'k'
              212  JUMP_FORWARD        240  'to 240'
            214_0  COME_FROM           198  '198'

 L. 795       214  LOAD_FAST                'ipb'
              216  LOAD_FAST                'nk'
              218  COMPARE_OP               <
              220  POP_JUMP_IF_FALSE   236  'to 236'

 L. 796       222  LOAD_FAST                'pvp'
              224  LOAD_FAST                'ipv'
              226  LOAD_FAST                'ipb'
              228  BUILD_TUPLE_2         2 
              230  BINARY_SUBSCR    
              232  STORE_FAST               'k'
              234  JUMP_FORWARD        240  'to 240'
            236_0  COME_FROM           220  '220'

 L. 798       236  LOAD_GLOBAL              nan
              238  STORE_FAST               'k'
            240_0  COME_FROM           234  '234'
            240_1  COME_FROM           212  '212'

 L. 800       240  LOAD_FAST                'k'
              242  LOAD_FAST                'kt'
              244  LOAD_CONST               0
              246  BINARY_SUBSCR    
              248  COMPARE_OP               <
          250_252  POP_JUMP_IF_TRUE    298  'to 298'
              254  LOAD_FAST                'k'
              256  LOAD_FAST                'kt'
              258  LOAD_CONST               -1
              260  BINARY_SUBSCR    
              262  COMPARE_OP               >
          264_266  POP_JUMP_IF_TRUE    298  'to 298'
              268  LOAD_GLOBAL              isnan
              270  LOAD_FAST                'k'
              272  CALL_FUNCTION_1       1  '1 positional argument'
          274_276  POP_JUMP_IF_TRUE    298  'to 298'
              278  LOAD_GLOBAL              isnan
              280  LOAD_FAST                'a'
              282  CALL_FUNCTION_1       1  '1 positional argument'
          284_286  POP_JUMP_IF_TRUE    298  'to 298'
              288  LOAD_GLOBAL              isnan
              290  LOAD_FAST                'i'
              292  CALL_FUNCTION_1       1  '1 positional argument'
          294_296  POP_JUMP_IF_FALSE   312  'to 312'
            298_0  COME_FROM           284  '284'
            298_1  COME_FROM           274  '274'
            298_2  COME_FROM           264  '264'
            298_3  COME_FROM           250  '250'

 L. 801       298  LOAD_GLOBAL              inf
              300  LOAD_FAST                'flux'
              302  LOAD_FAST                'ipv'
              304  LOAD_FAST                'j'
              306  BUILD_TUPLE_2         2 
              308  STORE_SUBSCR     

 L. 802       310  CONTINUE            158  'to 158'
            312_0  COME_FROM           294  '294'

 L. 804       312  SETUP_LOOP          502  'to 502'
              314  LOAD_GLOBAL              range
              316  LOAD_CONST               1
              318  LOAD_FAST                'nsamples'
              320  LOAD_FAST                'ilc'
              322  BINARY_SUBSCR    
              324  LOAD_CONST               1
              326  BINARY_ADD       
              328  CALL_FUNCTION_2       2  '2 positional arguments'
              330  GET_ITER         
              332  FOR_ITER            500  'to 500'
              334  STORE_FAST               'isample'

 L. 805       336  LOAD_FAST                'exptimes'
              338  LOAD_FAST                'ilc'
              340  BINARY_SUBSCR    
              342  LOAD_FAST                'isample'
              344  LOAD_CONST               0.5
              346  BINARY_SUBTRACT  
              348  LOAD_FAST                'nsamples'
              350  LOAD_FAST                'ilc'
              352  BINARY_SUBSCR    
              354  BINARY_TRUE_DIVIDE
              356  LOAD_CONST               0.5
              358  BINARY_SUBTRACT  
              360  BINARY_MULTIPLY  
              362  STORE_FAST               'time_offset'

 L. 806       364  LOAD_GLOBAL              z_ip_s
              366  LOAD_FAST                't'
              368  LOAD_FAST                'j'
              370  BINARY_SUBSCR    
              372  LOAD_FAST                'time_offset'
              374  BINARY_ADD       
              376  LOAD_FAST                't0'
              378  LOAD_FAST                'p'
              380  LOAD_FAST                'a'
              382  LOAD_FAST                'i'
              384  LOAD_FAST                'e'
              386  LOAD_FAST                'w'
              388  LOAD_FAST                'es'
              390  LOAD_FAST                'ms'
              392  LOAD_FAST                'tae'
              394  CALL_FUNCTION_10     10  '10 positional arguments'
              396  STORE_FAST               'z'

 L. 807       398  LOAD_FAST                'z'
              400  LOAD_CONST               1.0
              402  LOAD_FAST                'k'
              404  BINARY_ADD       
              406  COMPARE_OP               >
          408_410  POP_JUMP_IF_FALSE   434  'to 434'

 L. 808       412  LOAD_FAST                'flux'
              414  LOAD_FAST                'ipv'
              416  LOAD_FAST                'j'
              418  BUILD_TUPLE_2         2 
              420  DUP_TOP_TWO      
              422  BINARY_SUBSCR    
              424  LOAD_CONST               1.0
              426  INPLACE_ADD      
              428  ROT_THREE        
              430  STORE_SUBSCR     
              432  JUMP_BACK           332  'to 332'
            434_0  COME_FROM           408  '408'

 L. 810       434  LOAD_FAST                'flux'
              436  LOAD_FAST                'ipv'
              438  LOAD_FAST                'j'
              440  BUILD_TUPLE_2         2 
              442  DUP_TOP_TWO      
              444  BINARY_SUBSCR    
              446  LOAD_GLOBAL              quadratic_interpolated_z_s
              448  LOAD_FAST                'z'
              450  LOAD_FAST                'k'
              452  LOAD_FAST                'ldc'
              454  LOAD_FAST                'ipv'
              456  LOAD_CONST               2
              458  LOAD_FAST                'ipb'
              460  BINARY_MULTIPLY  
              462  LOAD_CONST               2
              464  LOAD_FAST                'ipb'
              466  LOAD_CONST               1
              468  BINARY_ADD       
              470  BINARY_MULTIPLY  
              472  BUILD_SLICE_2         2 
              474  BUILD_TUPLE_2         2 
              476  BINARY_SUBSCR    
              478  LOAD_FAST                'edt'
              480  LOAD_FAST                'ldt'
              482  LOAD_FAST                'let'
              484  LOAD_FAST                'kt'
              486  LOAD_FAST                'zt'
              488  CALL_FUNCTION_8       8  '8 positional arguments'
              490  INPLACE_ADD      
              492  ROT_THREE        
              494  STORE_SUBSCR     
          496_498  JUMP_BACK           332  'to 332'
              500  POP_BLOCK        
            502_0  COME_FROM_LOOP      312  '312'

 L. 811       502  LOAD_FAST                'flux'
              504  LOAD_FAST                'ipv'
              506  LOAD_FAST                'j'
              508  BUILD_TUPLE_2         2 
              510  DUP_TOP_TWO      
              512  BINARY_SUBSCR    
              514  LOAD_FAST                'nsamples'
              516  LOAD_FAST                'ilc'
              518  BINARY_SUBSCR    
              520  INPLACE_TRUE_DIVIDE
              522  ROT_THREE        
              524  STORE_SUBSCR     
              526  JUMP_BACK           158  'to 158'
              528  POP_BLOCK        
            530_0  COME_FROM_LOOP      146  '146'
              530  JUMP_BACK           124  'to 124'
              532  POP_BLOCK        
            534_0  COME_FROM_LOOP      112  '112'

 L. 812       534  LOAD_FAST                'flux'
              536  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 312_0