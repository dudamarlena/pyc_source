# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/datalib/datalib.py
# Compiled at: 2019-08-20 10:23:08
# Size of source mod 2**32: 16308 bytes
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
q = 1.60217662e-19
c = 299792458
h = 6.626e-34
k = 1.38064852e-23
supported_materials = [
 'Air', 'Al', 'Al2O3', 'AlN', 'Ag', 'Au', 'HfO2', 'Re', 'Rh', 'Ru', 'Pd', 'Pt', 'Si', 'SiO2', 'TiO2', 'TiN']
path_and_file = os.path.realpath(__file__)
path = path_and_file[:-10]

def Material_RI--- This code section failed: ---

 L.  23         0  LOAD_FAST                'lam'
                2  LOAD_CONST               1000000000.0
                4  BINARY_MULTIPLY  
                6  STORE_FAST               'l_nm'

 L.  24         8  LOAD_FAST                'lam'
               10  LOAD_CONST               1000000.0
               12  BINARY_MULTIPLY  
               14  STORE_FAST               'lmic'

 L.  25        16  LOAD_FAST                'arg'
               18  LOAD_STR                 'HfO2'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    88  'to 88'

 L.  26        24  LOAD_CONST               187178
               26  STORE_FAST               'A'

 L.  27        28  LOAD_CONST               9993.46
               30  STORE_FAST               'B'

 L.  28        32  LOAD_CONST               0.0173801
               34  STORE_FAST               'C'

 L.  29        36  LOAD_CONST               1.939999
               38  STORE_FAST               'D'

 L.  30        40  LOAD_FAST                'A'
               42  LOAD_FAST                'l_nm'
               44  LOAD_CONST               4
               46  BINARY_POWER     
               48  BINARY_TRUE_DIVIDE
               50  LOAD_FAST                'B'
               52  LOAD_FAST                'l_nm'
               54  LOAD_CONST               2
               56  BINARY_POWER     
               58  BINARY_TRUE_DIVIDE
               60  BINARY_ADD       
               62  LOAD_FAST                'C'
               64  LOAD_FAST                'l_nm'
               66  BINARY_TRUE_DIVIDE
               68  BINARY_ADD       
               70  LOAD_FAST                'D'
               72  BINARY_ADD       
               74  LOAD_CONST               0j
               76  LOAD_FAST                'l_nm'
               78  BINARY_TRUE_DIVIDE
               80  BINARY_ADD       
               82  STORE_FAST               'n'
            84_86  JUMP_FORWARD        582  'to 582'
             88_0  COME_FROM            22  '22'

 L.  31        88  LOAD_FAST                'arg'
               90  LOAD_STR                 'Al2O3'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   160  'to 160'

 L.  32        96  LOAD_CONST               187178
               98  STORE_FAST               'A'

 L.  33       100  LOAD_CONST               9993.46
              102  STORE_FAST               'B'

 L.  34       104  LOAD_CONST               0.0173801
              106  STORE_FAST               'C'

 L.  35       108  LOAD_CONST               1.69999
              110  STORE_FAST               'D'

 L.  36       112  LOAD_FAST                'A'
              114  LOAD_FAST                'l_nm'
              116  LOAD_CONST               4
              118  BINARY_POWER     
              120  BINARY_TRUE_DIVIDE
              122  LOAD_FAST                'B'
              124  LOAD_FAST                'l_nm'
              126  LOAD_CONST               2
              128  BINARY_POWER     
              130  BINARY_TRUE_DIVIDE
              132  BINARY_ADD       
              134  LOAD_FAST                'C'
              136  LOAD_FAST                'l_nm'
              138  BINARY_TRUE_DIVIDE
              140  BINARY_ADD       
              142  LOAD_FAST                'D'
              144  BINARY_ADD       
              146  LOAD_CONST               0j
              148  LOAD_FAST                'l_nm'
              150  BINARY_TRUE_DIVIDE
              152  BINARY_ADD       
              154  STORE_FAST               'n'
          156_158  JUMP_FORWARD        582  'to 582'
            160_0  COME_FROM            94  '94'

 L.  38       160  LOAD_FAST                'arg'
              162  LOAD_STR                 'SiO2'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   252  'to 252'
              168  LOAD_FAST                'lam'
              170  LOAD_GLOBAL              len
              172  LOAD_FAST                'lam'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  LOAD_CONST               1
              178  BINARY_SUBTRACT  
              180  BINARY_SUBSCR    
              182  LOAD_CONST               5e-06
              184  COMPARE_OP               <
              186  POP_JUMP_IF_FALSE   252  'to 252'

 L.  39       188  LOAD_CONST               187178
              190  STORE_FAST               'A'

 L.  40       192  LOAD_CONST               9993.46
              194  STORE_FAST               'B'

 L.  41       196  LOAD_CONST               0.0173801
              198  STORE_FAST               'C'

 L.  42       200  LOAD_CONST               1.45
              202  STORE_FAST               'D'

 L.  43       204  LOAD_FAST                'A'
              206  LOAD_FAST                'l_nm'
              208  LOAD_CONST               4
              210  BINARY_POWER     
              212  BINARY_TRUE_DIVIDE
              214  LOAD_FAST                'B'
              216  LOAD_FAST                'l_nm'
              218  LOAD_CONST               2
              220  BINARY_POWER     
              222  BINARY_TRUE_DIVIDE
              224  BINARY_ADD       
              226  LOAD_FAST                'C'
              228  LOAD_FAST                'l_nm'
              230  BINARY_TRUE_DIVIDE
              232  BINARY_ADD       
              234  LOAD_FAST                'D'
              236  BINARY_ADD       
              238  LOAD_CONST               0j
              240  LOAD_FAST                'l_nm'
              242  BINARY_TRUE_DIVIDE
              244  BINARY_ADD       
              246  STORE_FAST               'n'
          248_250  JUMP_FORWARD        582  'to 582'
            252_0  COME_FROM           186  '186'
            252_1  COME_FROM           166  '166'

 L.  50       252  LOAD_FAST                'arg'
              254  LOAD_STR                 'AlN'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   320  'to 320'
              262  LOAD_FAST                'lam'
              264  LOAD_GLOBAL              len
              266  LOAD_FAST                'lam'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  LOAD_CONST               1
              272  BINARY_SUBTRACT  
              274  BINARY_SUBSCR    
              276  LOAD_CONST               1e-05
              278  COMPARE_OP               <
          280_282  POP_JUMP_IF_FALSE   320  'to 320'

 L.  51       284  LOAD_CONST               1.859
              286  STORE_FAST               'A'

 L.  52       288  LOAD_CONST               0.3401
              290  STORE_FAST               'B'

 L.  53       292  LOAD_FAST                'A'
              294  LOAD_FAST                'B'
              296  LOAD_FAST                'lmic'
              298  LOAD_FAST                'lmic'
              300  BINARY_MULTIPLY  
              302  BINARY_TRUE_DIVIDE
              304  BINARY_ADD       
              306  LOAD_CONST               0j
              308  LOAD_FAST                'lmic'
              310  BINARY_TRUE_DIVIDE
              312  BINARY_ADD       
              314  STORE_FAST               'n'
          316_318  JUMP_FORWARD        582  'to 582'
            320_0  COME_FROM           280  '280'
            320_1  COME_FROM           258  '258'

 L.  54       320  LOAD_FAST                'arg'
              322  LOAD_STR                 'Air'
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   356  'to 356'

 L.  55       330  LOAD_CONST               0.0
              332  STORE_FAST               'A'

 L.  56       334  LOAD_FAST                'A'
              336  LOAD_FAST                'lam'
              338  BINARY_TRUE_DIVIDE
              340  LOAD_CONST               0j
              342  LOAD_FAST                'lam'
              344  BINARY_TRUE_DIVIDE
              346  BINARY_ADD       
              348  LOAD_CONST               1
              350  BINARY_ADD       
              352  STORE_FAST               'n'
              354  JUMP_FORWARD        582  'to 582'
            356_0  COME_FROM           326  '326'

 L.  57       356  LOAD_FAST                'arg'
              358  LOAD_STR                 'TiN'
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   376  'to 376'

 L.  58       366  LOAD_GLOBAL              TiN_Drude_Lorentz
              368  LOAD_FAST                'lam'
              370  CALL_FUNCTION_1       1  '1 positional argument'
              372  STORE_FAST               'n'
              374  JUMP_FORWARD        582  'to 582'
            376_0  COME_FROM           362  '362'

 L.  59       376  LOAD_FAST                'arg'
              378  LOAD_STR                 'W'
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_TRUE    416  'to 416'
              386  LOAD_FAST                'arg'
              388  LOAD_STR                 'Re'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_TRUE    416  'to 416'
              396  LOAD_FAST                'arg'
              398  LOAD_STR                 'Rh'
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_TRUE    416  'to 416'
              406  LOAD_FAST                'arg'
              408  LOAD_STR                 'Ru'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   428  'to 428'
            416_0  COME_FROM           402  '402'
            416_1  COME_FROM           392  '392'
            416_2  COME_FROM           382  '382'

 L.  60       416  LOAD_GLOBAL              Read_RI_from_File
              418  LOAD_FAST                'lam'
              420  LOAD_FAST                'arg'
              422  CALL_FUNCTION_2       2  '2 positional arguments'
              424  STORE_FAST               'n'
              426  JUMP_FORWARD        582  'to 582'
            428_0  COME_FROM           412  '412'

 L.  61       428  LOAD_FAST                'arg'
              430  LOAD_STR                 'Ag'
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_TRUE    478  'to 478'
              438  LOAD_FAST                'arg'
              440  LOAD_STR                 'Au'
              442  COMPARE_OP               ==
          444_446  POP_JUMP_IF_TRUE    478  'to 478'
              448  LOAD_FAST                'arg'
              450  LOAD_STR                 'Pd'
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_TRUE    478  'to 478'
              458  LOAD_FAST                'arg'
              460  LOAD_STR                 'Pt'
              462  COMPARE_OP               ==
          464_466  POP_JUMP_IF_TRUE    478  'to 478'
              468  LOAD_FAST                'arg'
              470  LOAD_STR                 'SiO2'
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   490  'to 490'
            478_0  COME_FROM           464  '464'
            478_1  COME_FROM           454  '454'
            478_2  COME_FROM           444  '444'
            478_3  COME_FROM           434  '434'

 L.  62       478  LOAD_GLOBAL              Read_RI_from_File
              480  LOAD_FAST                'lam'
              482  LOAD_FAST                'arg'
              484  CALL_FUNCTION_2       2  '2 positional arguments'
              486  STORE_FAST               'n'
              488  JUMP_FORWARD        582  'to 582'
            490_0  COME_FROM           474  '474'

 L.  63       490  LOAD_FAST                'arg'
              492  LOAD_STR                 'AlN'
              494  COMPARE_OP               ==
          496_498  POP_JUMP_IF_TRUE    520  'to 520'
              500  LOAD_FAST                'arg'
              502  LOAD_STR                 'Si'
              504  COMPARE_OP               ==
          506_508  POP_JUMP_IF_TRUE    520  'to 520'
              510  LOAD_FAST                'arg'
              512  LOAD_STR                 'TiO2'
              514  COMPARE_OP               ==
          516_518  POP_JUMP_IF_FALSE   532  'to 532'
            520_0  COME_FROM           506  '506'
            520_1  COME_FROM           496  '496'

 L.  64       520  LOAD_GLOBAL              Read_RI_from_File
              522  LOAD_FAST                'lam'
              524  LOAD_FAST                'arg'
              526  CALL_FUNCTION_2       2  '2 positional arguments'
              528  STORE_FAST               'n'
              530  JUMP_FORWARD        582  'to 582'
            532_0  COME_FROM           516  '516'

 L.  65       532  LOAD_FAST                'arg'
              534  LOAD_STR                 'J-Agg'
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   552  'to 552'

 L.  66       542  LOAD_GLOBAL              TDBC
              544  LOAD_FAST                'lam'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  STORE_FAST               'n'
              550  JUMP_FORWARD        582  'to 582'
            552_0  COME_FROM           538  '538'

 L.  69       552  LOAD_GLOBAL              print
              554  LOAD_STR                 '  INVALID MATERIAL OPTION!  THE FOLLOWING MATERIAL KEYWORDS ARE CURRENTLY SUPPORTED: '
              556  CALL_FUNCTION_1       1  '1 positional argument'
              558  POP_TOP          

 L.  70       560  LOAD_GLOBAL              print
              562  LOAD_GLOBAL              supported_materials
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  POP_TOP          

 L.  71       568  LOAD_GLOBAL              print
              570  LOAD_STR                 '  PLEASE CHECK YOUR Material_List AND RE-RUN '
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  POP_TOP          

 L.  72       576  LOAD_GLOBAL              exit
              578  CALL_FUNCTION_0       0  '0 positional arguments'
              580  POP_TOP          
            582_0  COME_FROM           550  '550'
            582_1  COME_FROM           530  '530'
            582_2  COME_FROM           488  '488'
            582_3  COME_FROM           426  '426'
            582_4  COME_FROM           374  '374'
            582_5  COME_FROM           354  '354'
            582_6  COME_FROM           316  '316'
            582_7  COME_FROM           248  '248'
            582_8  COME_FROM           156  '156'
            582_9  COME_FROM            84  '84'

 L.  73       582  LOAD_FAST                'n'
              584  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 426


def read_validation_data(arg):
    if arg == 1:
        file_path = path + '50nm_Au_wl_scan.txt'
        a = np.loadtxt(file_path)
        vlam = np.zeros(len(a))
        vR = np.zeros(len(a))
        vT = np.zeros(len(a))
        vE = np.zeros(len(a))
        for i in range0len(a):
            vlam[i] = a[i][0]
            vR[i] = a[i][1]
            vT[i] = a[i][2]
            vE[i] = a[i][3]

        Valid = {'V_LAM':vlam, 
         'V_REF':vR, 
         'V_TRANS':vT, 
         'V_EMISS':vE}
    else:
        if arg == 2:
            file_path = path + '50nm_Au_theta_scan.txt'
            a = np.loadtxt(file_path)
            vtheta = np.zeros(len(a))
            vR = np.zeros(len(a))
            vT = np.zeros(len(a))
            vE = np.zeros(len(a))
            for i in range0len(a):
                vtheta[i] = a[i][0]
                vR[i] = a[i][1]
                vT[i] = a[i][2]
                vE[i] = a[i][3]

            Valid = {'V_THETA':vtheta, 
             'V_REF_V_THETA':vR, 
             'V_TRANS_V_THETA':vT, 
             'V_EMISS_V_THETA':vE}
        else:
            if arg == 3:
                file_path = path + 'AEM_Fig3.txt'
                a = np.loadtxt(file_path)
                vlam = np.zeros(len(a))
                vR = np.zeros(len(a))
                vT = np.zeros(len(a))
                vE = np.zeros(len(a))
                for i in range0len(a):
                    vlam[i] = a[i][0]
                    vR[i] = a[i][1]
                    vT[i] = a[i][2]
                    vE[i] = a[i][3]

                Valid = {'V_LAM':vlam, 
                 'V_REF':vR, 
                 'V_TRANS':vT, 
                 'V_EMISS':vE}
            return Valid


def TiN_Drude_Lorentz(lam):
    ci = complex(0.0, 1.0)
    epsinf = 3.59
    rho = 1.09e-06
    eps0 = 8.854e-12
    hbar = 6.582e-16
    tau = 7.82e-16
    amp = 4.658129
    br = 4.3827
    en = 5.778
    l_nm = lam * 1000000000.0
    E = 1240.0 / l_nm
    eps = epsinf - hbar * hbar / (eps0 * rho * (tau * E * E + ci * hbar * E))
    eps = eps + amp * br * en / (en * en - E * E - ci * E * br)
    return np.sqrt(eps)


def Read_RI_from_File(lam, matname):
    if matname == 'W':
        file_path = path + 'W_Palik_RI_f.txt'
        a = np.loadtxt(file_path)
    else:
        if matname == 'TiO2':
            file_path = path + 'TiO2_Siefke.txt'
            a = np.loadtxt(file_path)
        else:
            if matname == 'Re':
                file_path = path + 'Re_Palik_RI_f.txt'
                a = np.loadtxt(file_path)
            else:
                if matname == 'Ru':
                    file_path = path + 'Ru_Palik_RI_f.txt'
                    a = np.loadtxt(file_path)
                else:
                    if matname == 'Rh':
                        file_path = path + 'Rh_Palik_RI_f.txt'
                        a = np.loadtxt(file_path)
                    else:
                        if matname == 'Ag' and lam[(len(lam) - 1)] <= 1e-06:
                            file_path = path + 'Ag_JC_RI_f.txt'
                            a = np.loadtxt(file_path)
                        else:
                            if matname == 'Ag' and lam[(len(lam) - 1)] > 1e-06:
                                file_path = path + 'Ag_Yang.txt'
                                a = np.loadtxt(file_path)
                            else:
                                if matname == 'Au' and lam[(len(lam) - 1)] <= 1e-06:
                                    file_path = path + 'Au_JC_RI_f.txt'
                                    a = np.loadtxt(file_path)
                                else:
                                    if matname == 'Au' and lam[(len(lam) - 1)] > 1e-06:
                                        file_path = path + 'Au_IR.txt'
                                        a = np.loadtxt(file_path)
                                    else:
                                        if matname == 'Pd':
                                            file_path = path + 'Pd_Palik_RI_f.txt'
                                            a = np.loadtxt(file_path)
                                        else:
                                            if matname == 'Pt':
                                                file_path = path + 'Pt_Palik_RI_f.txt'
                                                a = np.loadtxt(file_path)
                                            else:
                                                if matname == 'SiO2':
                                                    file_path = path + 'SiO2_IR.txt'
                                                    a = np.loadtxt(file_path)
                                                else:
                                                    if matname == 'AlN':
                                                        file_path = path + 'AlN_IR.txt'
                                                        a = np.loadtxt(file_path)
                                                    else:
                                                        if matname == 'Si':
                                                            file_path = path + 'Si_Schinke.txt'
                                                            a = np.loadtxt(file_path)
                                                        else:
                                                            if matname == 'W_Al2O3_Alloy':
                                                                file_path = path + 'W_Al23_Alloy.txt'
                                                                a = np.loadtxt(file_path)
                                                            else:
                                                                if matname == 'Al':
                                                                    file_path = path + 'Al_Rakic.txt'
                                                                    a = np.loadtxt(file_path)
                                                                else:
                                                                    file_path = path + 'W_Palik_RI_f.txt'
                                                                    a = np.loadtxt(file_path)
    datlam = np.zeros(len(a))
    datn = np.zeros(len(a))
    datk = np.zeros(len(a))
    for i in range0len(a):
        datlam[i] = a[i][0]
        datn[i] = a[i][1]
        datk[i] = a[i][2]

    order = 1
    sn = InterpolatedUnivariateSpline(datlam, datn, k=order)
    sk = InterpolatedUnivariateSpline(datlam, datk, k=order)
    yn = sn(lam)
    yk = sk(lam)
    n = yn + complex(0.0, 1.0) * yk
    return n


def SR_Si(lam):
    datlam = np.linspace(2.6e-07, 1.31e-06, 22)
    dateqe = 0.01 * np.array([0.0, 0.0, 11.5, 23.0, 33.0, 37.0, 41.0, 45.0, 49.0, 52.0, 56.0, 60.0, 64.0, 62.5, 51.0, 35.0, 27.5, 20.0, 12.5, 7.5, 0.0, 0.0])
    order = 1
    s = InterpolatedUnivariateSpline(datlam, dateqe, k=order)
    y = s(lam)
    return y


def Abs_Pyromark(lam):
    file_path = path + 'Pyromark.txt'
    a = np.loadtxt(file_path)
    x = np.zeros(len(a))
    y = np.zeros(len(a))
    for i in range0len(a):
        x[i] = a[i][0]
        y[i] = a[i][1]

    datlam = x
    dateqe = y
    order = 1
    s = InterpolatedUnivariateSpline(datlam, dateqe, k=order)
    z = s(lam)
    return z


def EQE_InGaAsSb(lam):
    datlam = np.linspace(1e-06, 3e-06, 21)
    dateqe = 0.01 * np.array([48.0, 50.0, 52.5, 54.0, 58.0, 59.0, 60.0, 62.0, 61.0, 62.0, 61.5, 59.0, 54.0, 22.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    order = 1
    s = InterpolatedUnivariateSpline(datlam, dateqe, k=order)
    y = s(lam)
    return y


def SR_InGaAsSb(lam):
    datlam = 1e-09 * np.array([200, 320, 1000, 1100, 1200, 1300, 1400, 1500,
     1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400,
     2500, 2600, 2700, 2800, 2900, 3000])
    dateqe = 0.01 * np.array([0.0, 0.0, 48.0, 50.0, 52.5, 54.0, 58.0, 59.0, 60.0, 62.0, 61.0, 62.0, 61.5, 59.0, 54.0, 22.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    datsr = q * dateqe * datlam / (h * c)
    order = 1
    s = InterpolatedUnivariateSpline(datlam, datsr, k=order)
    y = s(lam)
    return y


def SR_GaSb(lam):
    datlam = np.linspace(4e-07, 2e-06, 17)
    datsr = 0.01 * np.array([0.0, 0.0, 17.0, 34.0, 49.0, 58.0, 61.0, 68.0, 73.0, 80.0, 85.0, 88.0, 87.0, 70.0, 2.0, 0.0, 0.0])
    order = 1
    s = InterpolatedUnivariateSpline(datlam, datsr, k=order)
    y = s(lam)
    return y


def BB(lam, T):
    c = 299792458
    h = 6.62607004e-34
    kb = 1.38064852e-23
    rho = np.zeros_like(lam)
    for i in range0len(rho):
        rho[i] = 2 * h * c * c / lam[i] ** 5 * 1.0 / (np.exp(h * c / (lam[i] * kb * T)) - 1)

    return rho


def AM(lam):
    file_path = path + 'scaled_AM_1_5.txt'
    a = np.loadtxt(file_path)
    x = np.zeros(len(a))
    y = np.zeros(len(a))
    for i in range0len(a):
        x[i] = a[i][0]
        y[i] = a[i][1]

    datlam = x
    dateqe = y
    order = 1
    s = InterpolatedUnivariateSpline(datlam, dateqe, k=order)
    z = s(lam)
    return z


def ATData(lam):
    file_path = path + 'ATrans.txt'
    a = np.loadtxt(file_path)
    x = np.zeros(len(a))
    y = np.zeros(len(a))
    for i in range0len(a):
        x[i] = a[i][0] * 1e-06
        y[i] = a[i][1]

    datlam = x
    dateqe = y
    order = 1
    s = InterpolatedUnivariateSpline(datlam, dateqe, k=order)
    z = s(lam)
    return z


def PhLum(lam):
    a = 1.02433
    b = 259462000000000.0
    c = 5.60186e-07
    z = a * np.exp(-b * (lam - c) ** 2)
    return z


def CIE(lam):
    file_path = path + 'cie-cmf.txt'
    a = np.loadtxt(file_path)
    l = np.zeros(len(a))
    x = np.zeros(len(a))
    y = np.zeros(len(a))
    z = np.zeros(len(a))
    for i in range0len(a):
        l[i] = a[i][0] * 1e-09
        x[i] = a[i][1]
        y[i] = a[i][2]
        z[i] = a[i][3]

    order = 1
    xint = InterpolatedUnivariateSpline(l, x, k=order)
    xbar = xint(lam)
    yint = InterpolatedUnivariateSpline(l, y, k=order)
    ybar = yint(lam)
    zint = InterpolatedUnivariateSpline(l, z, k=order)
    zbar = zint(lam)
    cie = {'xbar':xbar, 
     'ybar':ybar, 
     'zbar':zbar}
    return cie


def TDBC(lam):
    datlamk = 1e-09 * np.array([380, 390, 400, 425, 450, 475, 500, 525, 550, 575, 582, 600, 625, 650, 675, 700, 710, 720])
    datk = np.array([0, 0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.01, 0.02, 0.08, 0.11, 0.09, 0.02, 0.01, 0.008, 0.004, 0, 0])
    order = 1
    sk = InterpolatedUnivariateSpline(datlamk, datk, k=order)
    yk = sk(lam)
    datlamn = 1e-09 * np.array([380, 390, 400, 425, 450, 475, 500, 525, 550, 566, 575, 600, 625, 650, 675, 700, 710, 720])
    datn = np.array([1.55, 1.55, 1.545, 1.54, 1.535, 1.527, 1.52, 1.51, 1.49, 1.475, 1.48, 1.595, 1.58, 1.565, 1.555, 1.55, 1.55,
     1.55])
    sn = InterpolatedUnivariateSpline(datlamn, datn, k=order)
    yn = sn(lam)
    ci = complex(0.0, 1.0)
    return yn + ci * yk