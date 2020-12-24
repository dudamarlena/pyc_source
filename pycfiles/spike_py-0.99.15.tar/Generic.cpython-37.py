# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/v2/Generic.py
# Compiled at: 2020-01-11 16:20:08
# Size of source mod 2**32: 107065 bytes
"""
 The library of NMR processing functions to be used with the NPK program.

This library implement the standard functions needed for NMR processing.
Most of theese functions require that the NPK mathematical kernel is loaded.

"""
from __future__ import print_function
__author__ = 'Marc A. Delsuc <delsuc@igbmc.fr> and Vincent Catherinot <v.catherinot@nmrtec.com>'
__date__ = 'Oct 2009'
import math, time, re, os, sys
from . import Nucleus
from . import Param
from .Kore import *
import unittest
try:
    import ConfigParser
except:
    import configparser as ConfigParser

def get_npk_path():
    return os.path.join(os.getcwd(), 'v1')


def dict_load(fname):
    """
    load a property list file as a dictionary
    
    one entry per line with the following syntax :
    entry=value

    keys are set to lowercase
    """
    dico = {}
    print(fname)
    try:
        fin = open(fname)
        f = fin.read()
        ls = f.split('\n')
        for line in ls:
            if not line == '':
                if line[0] == '#':
                    continue
                l = re.split('(?<!\\\\)=', line, 1)
                dkey = re.sub('\\\\=', '=', l[0])
                fval = re.sub('\\\\=', '=', l[1])
                try:
                    val = dico[dkey]
                except:
                    pass

                dico[dkey] = fval

        fin.close
    except:
        print('File ' + fname + ' not found.')
        print('Creating empty parameter list\n')

    return dico


def dict_out(dict, title=''):
    """
    dump the content of a dictionary as a property list file
    
    one entry per line with the following syntax :
    entry=value
    """
    from sys import stdout
    sys.stdout.write('\n#Property listing (START)' + title + '\n')
    for i in dict.keys():
        lk = re.sub('=', '\\\\=', i)
        try:
            lv = re.sub('=', '\\\\=', str(dict[i]))
        except:
            lv = 'UNDEFINED'

        sys.stdout.write(lk + '=' + lv + '\n')

    sys.stdout.write('#Property listing (END)' + title + '\n\n')


def dict_dump(dict, fname):
    """
    dump the content of a dictionary as a property list file
    
    one entry per line with the following syntax :
    entry=value
    """
    fout = open(fname, 'w')
    fout.write('#Property list file, created :' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime()) + '\n')
    for i in dict.keys():
        lk = re.sub('=', '\\\\=', i)
        lv = re.sub('=', '\\\\=', str(dict[i]))
        fout.write(lk + '=' + lv + '\n')

    fout.close()


def build_dict(default_list, p_in_arg={}):
    """ build the default parameter dictionary
    
    used in standard actions,
    returns a dictionary built from the default parmaters (see do_default.py and Param/*)
    and the additional parameters defined in the optionnal p_in_arg overwrite the default values
    
    wrapper around the NPKParam class
    """
    p = Param.NPKParam()
    p.build_default(default_list)
    for i in p_in_arg.keys():
        try:
            p[i] = p_in_arg.raw(i)
        except:
            p[i] = p_in_arg[i]

    return p


def change_key_dict(patternOut, patternIn, p_in_arg):
    """
    goes though the given dictionnay (which remains unchanged)
    and changes in keys the pattern "patternIn" to "patternOut"
    and returns the modified dictionnary

    typically used in 3D processing :

    change_key_dict('f2', 'f3',  change_key_dict('f1', 'f2', p_in))     # in THAT order !

        substitutes F2 (of the 3D) by F1 (of the 2D plane)
        substitutes F3 (of the 3D) by F2 (of the 2D plane)
    
    """
    verbose = 0
    if verbose:
        print('change_key_dict\n', patternIn, patternOut, p_in_arg)
    p = Param.NPKParam()
    if len(p_in_arg) > 0:
        for i in p_in_arg.keys():
            j = re.sub(patternIn, patternOut, i)
            try:
                p[j] = p_in_arg.raw(i)
            except:
                p[j] = p_in_arg[i]

    if verbose:
        print(p)
        raise Exception('stop')
    return p


def key_is_true(dict, key):
    """ used to check keys in processing parameter files
    
    will return true if dict[key] exists and is true
    will return false otherwise (does not exist or is false)
    """
    try:
        keytest = dict[key]
    except:
        keytest = 1 == 0

    return keytest


def key_is_not_false(dict, key):
    """ used to check keys in processing parameter files
    
    will return true if dict[key] exists and is true or doest not exist
    will return false if dict[key] is defined false
    """
    try:
        keytest = dict[key]
    except:
        keytest = 1 == 1

    return keytest


def NPKtempfile(ext='.npktmp'):
    """
    Standard tempfile module is VERY buggy in jython, the secure mkstemp is missing, and the basic system call needed to implement it are lacking.
    This is an attempt to make a "slightly" better tempfile than the jython built-in one.

    This seems to be enough to change it from really annoying to bearly noticiable... 
    """
    import tempfile, random
    r = '%d' % int(1000000 * random.random())
    tpf = tempfile.mktemp(r + ext)
    F = open(tpf, 'w')
    F.close()
    return tpf


def save_state(dd):
    """ save current working data-buffer
    
    kind of wrapper over put("data")
    save on temp file if necessary
    *** NOT FINISHED yet, do no use ***
    """
    global saved_state
    global tempdata
    mem_max = 16777216
    tempdata = 'empty'
    where = 'mem'
    d = get_dim()
    if dd == 1:
        if get_si1_1d() > mem_max:
            where = 'disk'
    if dd == 2:
        if get_si1_2d() * get_si2_2d() > mem_max:
            where = 'disk'
    if dd == 3:
        if get_si1_3d() * get_si2_3d() * get_si3_3d() > mem_max:
            where = 'disk'
    dim(dd)
    if where == 'mem':
        put('data')
    else:
        tempdata = NPKtempfile('.npktemp')
        writec(tempdata)
    dim(d)
    saved_state = (dd, where)
    print(repr(saved_state), tempdata)


def get_saved_state(dd):
    """ recover saved current working data-buffer
    """
    sdim, where = saved_state
    d = get_dim()
    if where == 'mem':
        dim(dd)
        get('data')
    else:
        read(tempdata)
    dim(d)


def get_itype(dim=0):
    """ analyze the complex state of the data buffer
        dim is either 0 (current dim); 1 2 or 3
        returns either (t) (t1,t2) (t1,t2,t3)
        where tx is 0 if real and 1 if complex
    """
    if dim == 0:
        dim = get_dim()
    if dim == 1:
        return get_itype_1d()
    if dim == 2:
        t1 = get_itype_2d() / 2
        t2 = get_itype_2d() % 2
        return (t1, t2)
    if dim == 3:
        t1 = get_itype_3d() / 4
        t3 = get_itype_3d() % 2
        t2 = (get_itype_3d() - 4 * t1) / 2
        return (t1, t2, t3)
    raise Exception('wrong value for dim')


def set_itype(type):
    """ set the complex state of the data buffer
        dim is either 1 2 or 3
        type is either (t) (t1,t2) (t1,t2,t3)
        where tx is 0 if real and 1 if complex
    """
    dim = get_dim()
    if dim == 1:
        t1 = type
        if t1 < 0 or t1 > 1:
            raise Exception('wrong value for type value')
        itype(t1)
    else:
        if dim == 2:
            t1, t2 = type
            if t1 < 0 or t1 > 1:
                raise Exception('wrong value for F1 type value')
            if t2 < 0 or t2 > 1:
                raise Exception('wrong value for F2 type value')
            itype(2 * t1 + t2)
        else:
            if dim == 3:
                t1, t2, t3 = type
                if t1 < 0 or t1 > 1:
                    raise Exception('wrong value for F1 type value')
                if t2 < 0 or t2 > 1:
                    raise Exception('wrong value for F2 type value')
                if t3 < 0 or t3 > 1:
                    raise Exception('wrong value for F3 type value')
                itype(4 * t1 + 2 * t2 + t3)
            else:
                raise Exception('wrong value for dim')


def apsl_cp(pki, sz):
    """computes the phase of the peak centered on i, using +/-sz points
    the phase of the peak is returned between -180 and 180
    i  has to be odd !
    used  by  apsl to compute an automatic phase correction of a 1D spectrum
    
    see also : apsl()
    
    MAD-VC, july 2005"""
    a = b = 0
    pi = 4.0 * math.atan(1.0)
    for j in range(2, 2 * sz + 2, 2):
        dr = val1d(pki + j) - val1d(pki - j)
        di = val1d(pki + j + 1) - val1d(pki - j + 1)
        a = a + dr * di
        b = b + di * di - dr * dr

    phi = 0.5 * math.atan(2.0 * a / b)
    px = 0
    for j in range(0, 4):
        pj = phi + float(j) * 0.5 * pi
        x = math.cos(pj) * val1d(pki) - math.sin(pj) * val1d(pki + 1)
        if x > px:
            phx = pj
            px = x

    while phx <= -pi:
        phx = phx + 2 * pi

    while phx > pi:
        phx = phx - 2 * pi

    return 180.0 * phx / pi


def apsl():
    """    APSL method
        A.Heuer J.Magn.Reson. 91 p241 (1991)

    uses the data buffer

        you may want to adapt :
            s_wdth : ration of line width to spectral width used for computing phases
            p_wdth : ration of line width to spectral width used for broadening for peak picking
            npk :  minimum number of peaks needed for phasing
            nfrst : the number of peaks used for first approx

    see also : apsl2d() apsl_cp()

    MAD-VC, july 2005
    """
    s_wdth = 400
    p_wdth = 1000
    npk = 8
    nfrst = 4
    dim = get_dim()
    if dim != 1:
        raise Exception('On 1D only')
    if get_itype_1d() != 1:
        raise Exception('On complex data only')
    if get_si1_1d() < 500:
        raise Exception('size too small for operation')
    com_put('data')
    ift()
    chsize(get_si1_1d() / 2)
    sqsin(0.5)
    chsize(get_si1_1d() * 4)
    ft()
    modulus()
    com_max()
    npeaks = 0
    pk = {}
    amp = {}
    for loop in range(1, 3):
        if loop == 1:
            zoom(1, 0.01 * get_si1_1d(), 0.48 * get_si1_1d())
        else:
            zoom(1, 0.52 * get_si1_1d(), 0.99 * get_si1_1d())
        sc = 0.5
        while True:
            minimax(geta_max(1) * sc, geta_max(1) + 1)
            peak()
            if get_npk1d() < npk / 2:
                sc = sc / 1.3
                continue
            if get_npk1d() > 2 * npk:
                sc = sc * 1.09
                continue
            break

        for i in range(get_npk1d(), 0, -1):
            pp = geta_pk1d_f(i)
            npeaks = npeaks + 1
            pk[npeaks] = 2 * int((pp - 1) / 2) + 1
            amp[npeaks] = geta_pk1d_a(i)

    zoom(0)
    nfrst = min(nfrst, npeaks)
    com_get('data')
    pk[0] = 1
    pk[npeaks + 1] = get_si1_1d()
    phi = {}
    for i in range(1, nfrst + 1):
        phi[i] = apsl_cp(pk[i], get_si1_1d() / s_wdth)
        if get_debug():
            print(repr(i) + 'th peak at index ' + repr(pk[i]) + ' phase : ' + repr(phi[i]))

    phase0 = 0
    aaa = 0
    for i in range(1, nfrst + 1):
        phase0 = phase0 + amp[i] * phi[i]
        aaa = aaa + amp[i]

    phase0 = phase0 / aaa
    slope = 0.0
    if get_debug():
        print('1rst guess on ' + repr(nfrst) + ' peaks : ' + repr(phase0) + ' ' + repr(slope))
    phase(phase0, slope)
    for i in range(1, nfrst + 1):
        phi[i] = phi[i] - phase0

    for i in range(nfrst + 1, npeaks + 1):
        phi[i] = apsl_cp(pk[i], get_si1_1d() / s_wdth)
        if get_debug():
            print(repr(i) + 'th peak at index ' + repr(pk[i]) + ' phase : ' + repr(phi[i]))

    x = 0
    y = 0
    z = 0
    q = 0
    w = 0
    for i in range(1, npeaks + 1):
        wi = amp[i]
        w = w + wi
        x = x + wi * (pk[i] - get_si1_1d() / 2)
        y = y + wi * phi[i]
        q = q + wi * (pk[i] - get_si1_1d() / 2) * (pk[i] - get_si1_1d() / 2)
        z = z + wi * phi[i] * (pk[i] - get_si1_1d() / 2)

    slope2 = (y * x - z * w) / (x * x - q * w)
    ph02 = (y - slope2 * x) / w
    slope2 = slope2 * get_si1_1d()
    get('data')
    zoom(0)
    pkclear()
    phase(phase0 + ph02, slope + slope2)
    if get_debug():
        print('final correction : ' + repr(phase0 + ph02) + ' ' + repr(slope) + ' ' + repr(slope2))


def apsl2d(axis='F2'):
    """a 2D version of apsl()

    axis is : F1, F2 or F12
    will peak pick the 2D, and apply apsl on sums of rows and columns

    see also : apsl()

    MAD-VC july 2005
    """
    return ap2d(apsl, axis)


def apmin2d(axis='F2'):
    """a 2D version of apmin()

    axis is : F1, F2 or F12
    will peak pick the 2D, and apply apmin on sums of rows and columns

    see also : apsl()

    MAD-VC july 2005
    """
    return ap2d(apmin, axis)


def ap2d(apfunc, axis='F2'):
    """a 2D automatic phaser

    axis is : F1, F2 or F12
    will peak pick the 2D, and apply the chose algo on sums of rows and columns

    MAD nov 2006
    """
    verbose = 0
    if verbose:
        print('ap2d started')
    npk = 8
    ret = ''
    if get_dim() != 2:
        raise Exception('On 2D only')
    if get_itype_2d() != 3:
        raise Exception('On hypercomplex data only')
    if get_si1_2d() < 250 or get_si2_2d() < 500:
        raise Exception('Size too small for operation')
    evaln(get_si1_2d() * 0.06, get_si2_2d() * 0.01, get_si1_2d() * 0.8, get_si2_2d() * 0.2)
    save_state(2)
    s1 = get_si1_2d()
    s2 = get_si2_2d()
    chsize(2 * power2(get_si1_2d() - 2), 2 * power2(get_si2_2d() - 2))
    ift('F12')
    chsize(get_si1_2d() / 2, get_si2_2d() / 2)
    sqsin(0.35, 'F1')
    sqsin(0.35, 'F2')
    chsize(get_si1_2d() * 2, get_si2_2d() * 2)
    ft('F12')
    modulus()
    chsize(s1 / 2, s2 / 2)
    com_max()
    npeaks = 0
    pk1 = {}
    pk2 = {}
    amp = {}
    if verbose:
        print('ap2d end prep')
    for loop in range(1, 5):
        if loop == 1:
            zoom(1, get_si1_2d() * 0.01, get_si2_2d() * 0.01, get_si1_2d() * 0.48, get_si2_2d() * 0.48)
        else:
            if loop == 2:
                zoom(1, get_si1_2d() * 0.01, get_si2_2d() * 0.52, get_si1_2d() * 0.48, get_si2_2d() * 0.99)
            else:
                if loop == 3:
                    zoom(1, get_si1_2d() * 0.52, get_si2_2d() * 0.01, get_si1_2d() * 0.99, get_si2_2d() * 0.48)
                else:
                    if loop == 4:
                        zoom(1, get_si1_2d() * 0.52, get_si2_2d() * 0.52, get_si1_2d() * 0.99, get_si2_2d() * 0.99)
                    sc = 0.5
                    if verbose:
                        print('ap2d end 2')
                    for isc in range(1, 100):
                        minimax(geta_max(1) * sc, geta_max(1) + 1)
                        if verbose:
                            print('ap2d minimax', isc)
                        peak(0)
                        if verbose:
                            print('ap2d')
                        if verbose:
                            print('ap2d', get_npk2d())
                        if get_npk2d() < npk / 2:
                            sc = sc / 1.31
                            continue
                        if get_npk2d() > 2 * npk:
                            sc = sc * 1.09
                            continue
                        if verbose:
                            print('ap2d bf break')
                        break

                    if verbose:
                        print('ap2d end 3')
                    for i in range(1, get_npk2d() + 1):
                        if geta_pk2d_a(i) > 3.0 * get_noise():
                            pp1 = geta_pk2d_f1f(i)
                            pp2 = geta_pk2d_f2f(i)
                            npeaks = npeaks + 1
                            pk1[npeaks] = 2 * pp1 + 1
                            pk2[npeaks] = 2 * pp2 + 1
                            amp[npeaks] = geta_pk2d_a(i)

    get_saved_state(2)
    pf20 = pf21 = 0
    pf10 = pf11 = 0
    if axis == 'F12':
        dim(2)
        row(1)
        dim(1)
        zero()
        put('data')
        for i in range(1, npeaks + 1):
            dim(2)
            row(pk1[i])
            dim(1)
            adddata()
            put('data')

        apfunc()
        dim(2)
        phase(get_ph0(), get_ph1(), 'F2')
        pf20 = get_ph0()
        pf21 = get_ph1()
        dim(2)
        col(1)
        dim(1)
        zero()
        put('data')
        for i in range(1, npeaks + 1):
            dim(2)
            col(pk2[i])
            dim(1)
            adddata()
            put('data')

        apfunc()
        dim(2)
        phase(get_ph0(), get_ph1(), 'F1')
        pf10 = get_ph0()
        pf11 = get_ph1()
    if axis == 'F2' or axis == 'F12':
        dim(2)
        row(1)
        dim(1)
        zero()
        put('data')
        for i in range(1, npeaks + 1):
            dim(2)
            row(pk1[i])
            dim(1)
            adddata()
            put('data')

        apfunc()
        dim(2)
        phase(get_ph0(), get_ph1(), 'F2')
        pf20 = pf20 + get_ph0()
        pf21 = pf21 + get_ph1()
    if axis == 'F1' or axis == 'F12':
        dim(2)
        col(1)
        dim(1)
        zero()
        put('data')
        for i in range(1, npeaks + 1):
            dim(2)
            col(pk2[i])
            dim(1)
            adddata()
            put('data')

        apfunc()
        dim(2)
        phase(get_ph0(), get_ph1(), 'F1')
        pf10 = pf10 + get_ph0()
        pf11 = pf11 + get_ph1()
    return (pf10, pf11, pf20, pf21)


def phase_pivot(p0, p1, pivot=0.5):
    """ three parameter phasing routine
        pivot = 0 is on left side
        pivot = 1 is on right side
        all intermidoate values are possible
        returns actual (P0, P1)
    """
    phase(p0 + (0.5 - pivot) * p1, p1)
    return (p0 + (0.5 - pivot) * p1, p1)


def neg_wing():
    """ measure negative wing power"""
    dim(1)
    real()
    bcorr(1, int(0.01 * get_si1_1d()), (int(0.05 * get_si1_1d()), int(0.95 * get_si1_1d())))
    minus()
    evaln(int(0.05 * get_si1_1d()), int(0.95 * get_si1_1d()))
    return get_noise()


def apmin_original():
    """automatic 1D phase correction
    phase by minimizing the negative wing of the spectrum

    MAD, oct 2006

    apmin moved to Kore
    """
    dim = get_dim()
    if dim != 1:
        raise Exception('On 1D only')
    else:
        if get_itype_1d() != 1:
            raise Exception('On complex data only')
        put('data')
        min = neg_wing()
        P0min = 0
        P1min = 0
        P0minnext = 0
        P1minnext = 0
        neval = 0
        get('data')
        modulus()
        com_max()
        npeaks = 0
        pk = {}
        zoom(1, 0.05 * get_si1_1d(), 0.95 * get_si1_1d())
        minimax(geta_max(1) * 0.1, geta_max(1) + 1)
        peak()
        pm = 0
        im = 0
        for i in range(get_npk1d()):
            if geta_pk1d_a(i + 1) > pm:
                pm = geta_pk1d_a(i + 1)
                im = geta_pk1d_f(i + 1)

        if im == 0:
            raise Exception('error in getting largest point')
        else:
            pivot = im / get_si1_1d()
    P0step = 10.0
    P1step = 20.0
    while P0step >= 1.0 or P0step <= -1.0:
        moved = 1
        while moved:
            moved = 0
            for dP0, dP1 in ((P0step, 0), (-P0step, 0), (0, P1step), (0, -P1step)):
                get('data')
                phase_pivot(P0min + dP0, P1min + dP1, pivot)
                neval = neval + 1
                pw = neg_wing()
                if pw < min:
                    moved = 1
                    min = pw
                    P0minnext = P0min + dP0
                    P1minnext = P1min + dP1
                    if P0step * dP0 < 0:
                        P0step = -P0step
                    if P1step * dP1 < 0:
                        P1step = -P1step
                    break

            P0min = P0minnext
            P1min = P1minnext

        P0step = P0step / 4.0
        P1step = P1step / 4.0

    get('data')
    PP0, PP1 = phase_pivot(P0min, P1min, pivot)


def spec_noise(n=10):
    """estimate of noise in the data-set

    estimates the noise in the data set by choping into n parts, and keeping the smallest one
    in the same time evaluates the offset on the dataset on the same part used for noise determination

    sets the value in get_noise and get_shift"""
    if get_dim() == 1:
        if get_itype_1d() != 0:
            put('data')
            real()
            getdata = 1
        else:
            getdata = 0
        if get_si1_1d() < 200:
            n = round(get_si1_1d() / 10)
        else:
            if n < 3:
                n = 10
            else:
                if get_si1_1d() / n < 20:
                    n = round(get_si1_1d() / 20)
        evaln(10, min(100, get_si1_1d()))
        so_far = get_noise()
        so_f_sh = 0
        for i in range(1, int(n) + 1):
            evaln(get_si1_1d() * (i - 1) / n + 1, get_si1_1d() * i / n)
            if get_noise() < so_far:
                so_far = get_noise()
                so_f_sh = get_shift()

        if getdata:
            get('data')
    else:
        if get_dim() == 2:
            if get_itype_2d() != 0:
                put('data')
                if get_itype_2d() == 3:
                    real('F12')
                else:
                    if get_itype_2d() == 1:
                        real('F2')
                    else:
                        if get_itype_2d() == 2:
                            real('F1')
                        getdata = 1
            else:
                getdata = 0
        elif get_si1_2d() * get_si2_2d() < 500:
            n = 10
        else:
            if n < 3:
                n = 10
            else:
                evaln(1, 1, min(100, get_si1_2d()), min(100, get_si2_2d()))
                so_far = get_noise()
                so_f_sh = get_shift()
                sn = round(math.sqrt(n))
                for j in range(1, int(n) + 1):
                    for i in range(1, int(n) + 1):
                        evaln(get_si1_2d() * (i - 1) / n + 1, get_si2_2d() * (j - 1) / n + 1, get_si1_2d() * i / n, get_si2_2d() * j / n)
                        if get_noise() < so_far:
                            so_far = get_noise()
                            so_f_sh = get_shift()

                if getdata:
                    get('data')
                else:
                    raise Exception('reste a faire en 3D')
    if so_far != 0:
        noise(so_far)
        shift(so_f_sh)


def signal_noise(left=1, right=1, n=10):
    """estimate the signal to noise of a given 1D data-set
    
    It does this by find the most intense peak and dividing it by the noise level

    left , right define the zone in which the signal/noise is to be computed
    both value default to 1, right=1 means the right most point.
    n is the number of pieces on which the noise is computed.
    
    """
    if right == 1:
        right = get_si1_1d()
    else:
        if left >= right:
            raise Exception('wrong argument to signal_noise()')
        if get_itype_1d() != 0:
            put('data')
            real()
            r = 1
        else:
            r = 0
    v = 0.0
    for i in range(left, right + 1):
        v = max(v, val1d(i))

    if r == 1:
        get('data')
    return v / get_noise()


def left_shift(shift_size, axis='F1'):
    """shifts the FID to the left by dropping data points
    MAD-VC January 2007"""
    if get_dim() == 1:
        reverse()
        chsize(get_si1_1d() - shift_size)
        reverse()
    else:
        if get_dim() == 2:
            reverse(axis)
            if axis.upper() == 'F1':
                chsize(get_si1_2d() - shift_size, get_si2_2d())
            else:
                if axis.upper() == 'F2':
                    chsize(get_si1_2d(), get_si2_2d() - shift_size)
            reverse(axis)
        else:
            if get_dim() == 3:
                raise Exception('not done yet')


def right_shift(shift_size, axis='F1'):
    """shifts the FID to the right by adding null data points at the begining of the FID
    MAD-VC January 2007"""
    if get_dim() == 1:
        reverse()
        chsize(get_si1_1d() + shift_size)
        reverse()
    else:
        if get_dim() == 2:
            reverse(axis)
            if axis.upper() == 'F1':
                chsize(get_si1_2d() + shift_size, get_si2_2d())
            else:
                if axis.upper() == 'F2':
                    chsize(get_si1_2d(), get_si2_2d() + shift_size)
            reverse(axis)
        else:
            if get_dim() == 3:
                raise Exception('not done yet')


def ft_sim():
    """performs the fourier transform of a data-set acquired on a Bruker in
    simultaneous mode
    Processing is performed only along the F2 (F3) axis if in 2D (3D)

    (Bruker QSIM mode)

    see also : ft_seq() ft_sh() ft_tppi() ft_sh_tppi() ft_phase_modu() ft_n_p() 

    MAD-VC July 2005"""
    if get_dim() == 1:
        itype(1)
        revf()
        ft()
    else:
        if get_dim() == 2 and not get_itype_2d() == 2:
            if get_itype_2d() == 0:
                print('Forcing Complex form in F2')
                itype(get_itype_2d() + 1)
            revf('f2')
            ft('f2')
        else:
            if get_dim() == 3:
                if get_itype_3d() % 2 == 0:
                    print('Forcing Complex form in F3')
                    itype(get_itype_3d() + 1)
                revf('f3')
                ft('f3')


def ft_seq():
    """performs the fourier transform of a data-set acquired on a Bruker in
    simultaneous mode
    Processing is performed only along the F2 (F3) axis if in 2D (3D)

    (Bruker QSIM mode)

    see also : ft_seq() ft_sh() ft_tppi() ft_sh_tppi() ft_phase_modu() ft_n_p() 

    MAD-VC July 2005"""
    if get_dim() == 1:
        itype(0)
        revf()
        rft()
    else:
        if get_dim() == 2 and not get_itype_2d() == 1:
            if get_itype_2d() == 3:
                print('Forcing Real form in F2')
                itype(get_itype_2d() - 1)
            revf('f2')
            rft('f2')
        else:
            if get_dim() == 3:
                if get_itype_3d() % 2 == 1:
                    print('Forcing Real form in F3')
                    itype(get_itype_3d() - 1)
                revf('f3')
                rft('f3')


def ft_tppi(axis='F1'):
    """TPPI F1 Fourier transform"""
    if get_dim() == 2 and not get_itype_2d() == 2:
        if get_itype_2d() == 3:
            itype(get_itype_2d() - 2)
            print('Forcing Real form in F1')
        rft('f1')
    else:
        if get_dim() == 3:
            axis = axis.upper()
            if axis == 'F1':
                if get_itype_3d() > 3:
                    itype(get_itype_3d() - 4)
                    print('Forcing Real form in F1')
            elif axis == 'F2':
                if get_itype3d() % 4 > 1:
                    itype(get_itype_3d() - 2)
                    print('Forcing Real form in F2')
            else:
                raise Exception('wrong axis')
            rft(axis)
        else:
            raise Exception('Not implemented in 1D, use ft_seq instead')


def ft_n_p(axis='F1'):
    """F1-Fourier transform for N+P (echo/antiecho) 2D"""
    if get_dim() == 2:
        conv_n_p()
        ft_sh()
    else:
        raise Exception('in 2D only')


def ft_sh(axis='F1'):
    """ States-Haberkorn F1 Fourier transform"""
    if get_dim() == 2 and not get_itype_2d() == 0:
        if get_itype_2d() == 1:
            itype(get_itype_2d() + 2)
            print('Forcing Complex form in F1')
        revf('f1')
        ft('f1')
    else:
        if get_dim() == 3:
            axis = axis.upper()
            if axis == 'F1':
                if get_itype_3d() < 4:
                    print('Forcing Complex form in F1')
                    itype(get_itype_3d() + 4)
            elif axis == 'F2':
                if get_itype_3d() % 4 < 2:
                    itype(get_itype_3d() + 2)
                    print('Forcing Complex form in F2')
            revf(axis)
            ft(axis)
        else:
            raise Exception('not implemented in 1D, use ft_sim instead')


def ft_sh_tppi(axis='F1'):
    """States-Haberkorn / TPPI F1 Fourier Transform """
    if get_dim() == 2 and not get_itype_2d() == 0:
        if get_itype_2d() == 1:
            itype(get_itype_2d() + 2)
            print('Forcing Complex form in F1')
        ft('F1')
    else:
        if get_dim() == 3:
            axis = axis.upper()
            if axis == 'F1':
                if get_itype_3d() < 4:
                    itype(get_itype_3d() + 4)
                    print('Forcing Complex form in F1')
            elif axis == 'F2':
                if get_itype_3d() % 4 < 2:
                    itype(get_itype_3d() + 2)
                    print('Forcing Complex form in F2')
            else:
                raise Exception('Wrong axis')
            ft(axis)
        else:
            raise Exception('Not implemeted in 1D')


def ft_phase_modu(axis='F1'):
    """F1-Fourier transform for phase-modulated 2D"""
    if get_dim() != 2:
        raise Exception('implemented only in 2D')
    else:
        itype(1)
        flip()
        revf('F1')
        ft('F1')
        flop()
        reverse('F1')


def expbroad(lb, axis='F1'):
    """apply a lb exponential broadening along given axis"""
    if get_dim() == 1:
        em(lb)
    else:
        axis = axis.upper()
    if get_dim() == 2:
        if axis == 'F1':
            em(lb, 0)
        else:
            if axis == 'F2':
                em(0, lb)
            else:
                if axis == 'F12' or axis == 'F21':
                    em(lb, lb)
                else:
                    raise Exception('Wrong axis')
    else:
        if get_dim() == 3:
            if axis == 'F1':
                em(lb, 0, 0)
            else:
                if axis == 'F2':
                    em(0, lb, 0)
                else:
                    if axis == 'F3':
                        em(0, 0, lb)
                    else:
                        if axis == 'F12' or axis == 'F21':
                            em(lb, lb, 0)
                        else:
                            if axis == 'F23' or axis == 'F32':
                                em(0, lb, lb)
                            else:
                                if axis == 'F31' or axis == 'F13':
                                    em(lb, 0, lb)
                                else:
                                    if axis == 'F123':
                                        em(lb, lb, lb)
                                    else:
                                        raise Exception('Wrong dimension')


def gaussbroad(lb, axis='F1'):
    """apply a lb gaussian broadening along given axis"""
    if get_dim() == 1:
        gm(lb)
    else:
        axis = axis.upper()
    if get_dim() == 2:
        if axis == 'F1':
            gm(lb, 0)
        else:
            if axis == 'F2':
                gm(0, lb)
            else:
                if axis == 'F12' or axis == 'F21':
                    gm(lb, lb)
                else:
                    raise Exception('Wrong axis')
    else:
        if get_dim() == 3:
            if axis == 'F1':
                gm(lb, 0, 0)
            else:
                if axis == 'F2':
                    gm(0, lb, 0)
                else:
                    if axis == 'F3':
                        gm(0, 0, lb)
                    else:
                        if axis == 'F12' or axis == 'F21':
                            gm(lb, lb, 0)
                        else:
                            if axis == 'F23' or axis == 'F32':
                                gm(0, lb, lb)
                            else:
                                if axis == 'F31' or axis == 'F13':
                                    gm(lb, 0, lb)
                                else:
                                    if axis == 'F123':
                                        gm(lb, lb, lb)
                                    else:
                                        raise Exception('Wrong dimension')


def gaussenh--- This code section failed: ---

 L.1155         0  LOAD_GLOBAL              get_dim
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  LOAD_CONST               1
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    36  'to 36'

 L.1156        10  LOAD_GLOBAL              gm
               12  LOAD_FAST                'gg'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  POP_TOP          

 L.1157        18  LOAD_GLOBAL              em
               20  LOAD_FAST                'll'
               22  UNARY_NEGATIVE   
               24  LOAD_FAST                'gg'
               26  BINARY_MULTIPLY  
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  POP_TOP          
            32_34  JUMP_FORWARD        564  'to 564'
             36_0  COME_FROM             8  '8'

 L.1159        36  LOAD_FAST                'axis'
               38  LOAD_METHOD              upper
               40  CALL_METHOD_0         0  '0 positional arguments'
               42  STORE_FAST               'axis'

 L.1160        44  LOAD_GLOBAL              get_dim
               46  CALL_FUNCTION_0       0  '0 positional arguments'
               48  LOAD_CONST               2
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE   188  'to 188'

 L.1161        54  LOAD_FAST                'axis'
               56  LOAD_STR                 'F1'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    90  'to 90'

 L.1162        62  LOAD_GLOBAL              gm
               64  LOAD_FAST                'gg'
               66  LOAD_CONST               0
               68  CALL_FUNCTION_2       2  '2 positional arguments'
               70  POP_TOP          

 L.1163        72  LOAD_GLOBAL              em
               74  LOAD_FAST                'll'
               76  UNARY_NEGATIVE   
               78  LOAD_FAST                'gg'
               80  BINARY_MULTIPLY  
               82  LOAD_CONST               0
               84  CALL_FUNCTION_2       2  '2 positional arguments'
               86  POP_TOP          
               88  JUMP_FORWARD        564  'to 564'
             90_0  COME_FROM            60  '60'

 L.1164        90  LOAD_FAST                'axis'
               92  LOAD_STR                 'F2'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   126  'to 126'

 L.1165        98  LOAD_GLOBAL              gm
              100  LOAD_CONST               0
              102  LOAD_FAST                'gg'
              104  CALL_FUNCTION_2       2  '2 positional arguments'
              106  POP_TOP          

 L.1166       108  LOAD_GLOBAL              em
              110  LOAD_CONST               0
              112  LOAD_FAST                'll'
              114  UNARY_NEGATIVE   
              116  LOAD_FAST                'gg'
              118  BINARY_MULTIPLY  
              120  CALL_FUNCTION_2       2  '2 positional arguments'
              122  POP_TOP          
              124  JUMP_FORWARD        564  'to 564'
            126_0  COME_FROM            96  '96'

 L.1167       126  LOAD_FAST                'axis'
              128  LOAD_STR                 'F12'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_TRUE    142  'to 142'
              134  LOAD_FAST                'axis'
              136  LOAD_STR                 'F21'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   176  'to 176'
            142_0  COME_FROM           132  '132'

 L.1168       142  LOAD_GLOBAL              gm
              144  LOAD_FAST                'gg'
              146  LOAD_FAST                'gg'
              148  CALL_FUNCTION_2       2  '2 positional arguments'
              150  POP_TOP          

 L.1169       152  LOAD_GLOBAL              em
              154  LOAD_FAST                'll'
              156  UNARY_NEGATIVE   
              158  LOAD_FAST                'gg'
              160  BINARY_MULTIPLY  
              162  LOAD_FAST                'll'
              164  UNARY_NEGATIVE   
              166  LOAD_FAST                'gg'
              168  BINARY_MULTIPLY  
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  POP_TOP          
              174  JUMP_FORWARD        564  'to 564'
            176_0  COME_FROM           140  '140'

 L.1171       176  LOAD_GLOBAL              Exception
              178  LOAD_STR                 'wrong axis'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  RAISE_VARARGS_1       1  'exception instance'
          184_186  JUMP_FORWARD        564  'to 564'
            188_0  COME_FROM            52  '52'

 L.1172       188  LOAD_GLOBAL              get_dim
              190  CALL_FUNCTION_0       0  '0 positional arguments'
              192  LOAD_CONST               3
              194  COMPARE_OP               ==
          196_198  POP_JUMP_IF_FALSE   564  'to 564'

 L.1173       200  LOAD_FAST                'axis'
              202  LOAD_STR                 'F1'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   242  'to 242'

 L.1174       208  LOAD_GLOBAL              gm
              210  LOAD_FAST                'gg'
              212  LOAD_CONST               0
              214  LOAD_CONST               0
              216  CALL_FUNCTION_3       3  '3 positional arguments'
              218  POP_TOP          

 L.1175       220  LOAD_GLOBAL              em
              222  LOAD_FAST                'll'
              224  UNARY_NEGATIVE   
              226  LOAD_FAST                'gg'
              228  BINARY_MULTIPLY  
              230  LOAD_CONST               0
              232  LOAD_CONST               0
              234  CALL_FUNCTION_3       3  '3 positional arguments'
              236  POP_TOP          
          238_240  JUMP_FORWARD        564  'to 564'
            242_0  COME_FROM           206  '206'

 L.1176       242  LOAD_FAST                'axis'
              244  LOAD_STR                 'F2'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   286  'to 286'

 L.1177       252  LOAD_GLOBAL              gm
              254  LOAD_CONST               0
              256  LOAD_FAST                'gg'
              258  LOAD_CONST               0
              260  CALL_FUNCTION_3       3  '3 positional arguments'
              262  POP_TOP          

 L.1178       264  LOAD_GLOBAL              em
              266  LOAD_CONST               0
              268  LOAD_FAST                'll'
              270  UNARY_NEGATIVE   
              272  LOAD_FAST                'gg'
              274  BINARY_MULTIPLY  
              276  LOAD_CONST               0
              278  CALL_FUNCTION_3       3  '3 positional arguments'
              280  POP_TOP          
          282_284  JUMP_FORWARD        564  'to 564'
            286_0  COME_FROM           248  '248'

 L.1179       286  LOAD_FAST                'axis'
              288  LOAD_STR                 'F3'
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   328  'to 328'

 L.1180       296  LOAD_GLOBAL              gm
              298  LOAD_CONST               0
              300  LOAD_CONST               0
              302  LOAD_FAST                'gg'
              304  CALL_FUNCTION_3       3  '3 positional arguments'
              306  POP_TOP          

 L.1181       308  LOAD_GLOBAL              em
              310  LOAD_CONST               0
              312  LOAD_CONST               0
              314  LOAD_FAST                'll'
              316  UNARY_NEGATIVE   
              318  LOAD_FAST                'gg'
              320  BINARY_MULTIPLY  
              322  CALL_FUNCTION_3       3  '3 positional arguments'
              324  POP_TOP          
              326  JUMP_FORWARD        564  'to 564'
            328_0  COME_FROM           292  '292'

 L.1182       328  LOAD_FAST                'axis'
              330  LOAD_STR                 'F12'
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_TRUE    348  'to 348'
              338  LOAD_FAST                'axis'
              340  LOAD_STR                 'F21'
              342  COMPARE_OP               ==
          344_346  POP_JUMP_IF_FALSE   386  'to 386'
            348_0  COME_FROM           334  '334'

 L.1183       348  LOAD_GLOBAL              gm
              350  LOAD_FAST                'gg'
              352  LOAD_FAST                'gg'
              354  LOAD_CONST               0
              356  CALL_FUNCTION_3       3  '3 positional arguments'
              358  POP_TOP          

 L.1184       360  LOAD_GLOBAL              em
              362  LOAD_FAST                'll'
              364  UNARY_NEGATIVE   
              366  LOAD_FAST                'gg'
              368  BINARY_MULTIPLY  
              370  LOAD_FAST                'll'
              372  UNARY_NEGATIVE   
              374  LOAD_FAST                'gg'
              376  BINARY_MULTIPLY  
              378  LOAD_CONST               0
              380  CALL_FUNCTION_3       3  '3 positional arguments'
              382  POP_TOP          
              384  JUMP_FORWARD        564  'to 564'
            386_0  COME_FROM           344  '344'

 L.1185       386  LOAD_FAST                'axis'
              388  LOAD_STR                 'F23'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_TRUE    406  'to 406'
              396  LOAD_FAST                'axis'
              398  LOAD_STR                 'F32'
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   444  'to 444'
            406_0  COME_FROM           392  '392'

 L.1186       406  LOAD_GLOBAL              gm
              408  LOAD_CONST               0
              410  LOAD_FAST                'gg'
              412  LOAD_FAST                'gg'
              414  CALL_FUNCTION_3       3  '3 positional arguments'
              416  POP_TOP          

 L.1187       418  LOAD_GLOBAL              em
              420  LOAD_CONST               0
              422  LOAD_FAST                'll'
              424  UNARY_NEGATIVE   
              426  LOAD_FAST                'gg'
              428  BINARY_MULTIPLY  
              430  LOAD_FAST                'll'
              432  UNARY_NEGATIVE   
              434  LOAD_FAST                'gg'
              436  BINARY_MULTIPLY  
              438  CALL_FUNCTION_3       3  '3 positional arguments'
              440  POP_TOP          
              442  JUMP_FORWARD        564  'to 564'
            444_0  COME_FROM           402  '402'

 L.1188       444  LOAD_FAST                'axis'
              446  LOAD_STR                 'F13'
              448  COMPARE_OP               ==
          450_452  POP_JUMP_IF_TRUE    464  'to 464'
              454  LOAD_FAST                'axis'
              456  LOAD_STR                 'F31'
              458  COMPARE_OP               ==
          460_462  POP_JUMP_IF_FALSE   502  'to 502'
            464_0  COME_FROM           450  '450'

 L.1189       464  LOAD_GLOBAL              gm
            466_0  COME_FROM            88  '88'
              466  LOAD_FAST                'gg'
              468  LOAD_CONST               0
              470  LOAD_FAST                'gg'
              472  CALL_FUNCTION_3       3  '3 positional arguments'
              474  POP_TOP          

 L.1190       476  LOAD_GLOBAL              em
              478  LOAD_FAST                'll'
              480  UNARY_NEGATIVE   
              482  LOAD_FAST                'gg'
              484  BINARY_MULTIPLY  
              486  LOAD_CONST               0
              488  LOAD_FAST                'll'
              490  UNARY_NEGATIVE   
              492  LOAD_FAST                'gg'
              494  BINARY_MULTIPLY  
              496  CALL_FUNCTION_3       3  '3 positional arguments'
              498  POP_TOP          
              500  JUMP_FORWARD        564  'to 564'
            502_0  COME_FROM           460  '460'
            502_1  COME_FROM           124  '124'

 L.1191       502  LOAD_FAST                'axis'
              504  LOAD_STR                 'F123'
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   556  'to 556'

 L.1192       512  LOAD_GLOBAL              gm
              514  LOAD_FAST                'gg'
              516  LOAD_FAST                'gg'
              518  LOAD_FAST                'gg'
              520  CALL_FUNCTION_3       3  '3 positional arguments'
              522  POP_TOP          

 L.1193       524  LOAD_GLOBAL              em
              526  LOAD_FAST                'll'
              528  UNARY_NEGATIVE   
              530  LOAD_FAST                'gg'
              532  BINARY_MULTIPLY  
              534  LOAD_FAST                'll'
              536  UNARY_NEGATIVE   
              538  LOAD_FAST                'gg'
              540  BINARY_MULTIPLY  
              542  LOAD_FAST                'll'
              544  UNARY_NEGATIVE   
              546  LOAD_FAST                'gg'
              548  BINARY_MULTIPLY  
              550  CALL_FUNCTION_3       3  '3 positional arguments'
            552_0  COME_FROM           174  '174'
              552  POP_TOP          
              554  JUMP_FORWARD        564  'to 564'
            556_0  COME_FROM           508  '508'

 L.1195       556  LOAD_GLOBAL              Exception
              558  LOAD_STR                 'wrong axis'
              560  CALL_FUNCTION_1       1  '1 positional argument'
              562  RAISE_VARARGS_1       1  'exception instance'
            564_0  COME_FROM           554  '554'
            564_1  COME_FROM           500  '500'
            564_2  COME_FROM           442  '442'
            564_3  COME_FROM           384  '384'
            564_4  COME_FROM           326  '326'
            564_5  COME_FROM           282  '282'
            564_6  COME_FROM           238  '238'
            564_7  COME_FROM           196  '196'
            564_8  COME_FROM           184  '184'
            564_9  COME_FROM            32  '32'

Parse error at or near `COME_FROM' instruction at offset 466_0


def apodise--- This code section failed: ---

 L.1209         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              types
                6  STORE_FAST               'types'

 L.1210         8  LOAD_CONST               0
               10  STORE_FAST               'debug'

 L.1211        12  LOAD_GLOBAL              type
               14  LOAD_FAST                'apod'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  LOAD_GLOBAL              str
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    46  'to 46'

 L.1212        24  LOAD_GLOBAL              print
               26  LOAD_FAST                'apod'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  POP_TOP          

 L.1213        32  LOAD_GLOBAL              Exception
               34  LOAD_STR                 'argument should be an NPK executable string\n\n'
               36  LOAD_GLOBAL              apodise
               38  LOAD_ATTR                __doc__
               40  BINARY_ADD       
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            22  '22'

 L.1214        46  LOAD_GLOBAL              get_dim
               48  CALL_FUNCTION_0       0  '0 positional arguments'
               50  LOAD_CONST               1
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    84  'to 84'

 L.1215        56  LOAD_FAST                'debug'
               58  POP_JUMP_IF_FALSE    72  'to 72'

 L.1215        60  LOAD_GLOBAL              print
               62  LOAD_STR                 'apod 1D '
               64  LOAD_FAST                'apod'
               66  BINARY_ADD       
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  POP_TOP          
             72_0  COME_FROM            58  '58'

 L.1216        72  LOAD_GLOBAL              exec
               74  LOAD_FAST                'apod'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  POP_TOP          
            80_82  JUMP_FORWARD        862  'to 862'
             84_0  COME_FROM            54  '54'

 L.1217        84  LOAD_GLOBAL              get_dim
               86  CALL_FUNCTION_0       0  '0 positional arguments'
               88  LOAD_CONST               2
               90  COMPARE_OP               ==
            92_94  POP_JUMP_IF_FALSE   406  'to 406'

 L.1218        96  LOAD_FAST                'axis'
               98  LOAD_METHOD              upper
              100  CALL_METHOD_0         0  '0 positional arguments'
              102  STORE_FAST               'axis'

 L.1219       104  LOAD_FAST                'axis'
              106  LOAD_STR                 'F2'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   252  'to 252'

 L.1220       112  LOAD_FAST                'debug'
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L.1220       116  LOAD_GLOBAL              print
              118  LOAD_STR                 'apod F2 '
              120  LOAD_FAST                'apod'
              122  BINARY_ADD       
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  POP_TOP          
            128_0  COME_FROM           114  '114'

 L.1221       128  LOAD_FAST                'debug'
              130  POP_JUMP_IF_FALSE   140  'to 140'

 L.1221       132  LOAD_GLOBAL              writec
              134  LOAD_STR                 'TTT1.gs2'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  POP_TOP          
            140_0  COME_FROM           130  '130'

 L.1222       140  LOAD_GLOBAL              row
              142  LOAD_CONST               1
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  POP_TOP          

 L.1223       148  LOAD_GLOBAL              dim
              150  LOAD_CONST               1
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  POP_TOP          

 L.1224       156  LOAD_GLOBAL              get_itype_1d
              158  CALL_FUNCTION_0       0  '0 positional arguments'
              160  LOAD_CONST               0
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   174  'to 174'

 L.1225       166  LOAD_GLOBAL              one
              168  CALL_FUNCTION_0       0  '0 positional arguments'
              170  POP_TOP          
              172  JUMP_FORWARD        196  'to 196'
            174_0  COME_FROM           164  '164'

 L.1227       174  LOAD_GLOBAL              itype
              176  LOAD_CONST               0
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  POP_TOP          

 L.1227       182  LOAD_GLOBAL              one
              184  CALL_FUNCTION_0       0  '0 positional arguments'
              186  POP_TOP          

 L.1227       188  LOAD_GLOBAL              itype
              190  LOAD_CONST               1
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  POP_TOP          
            196_0  COME_FROM           172  '172'

 L.1228       196  SETUP_EXCEPT        210  'to 210'

 L.1229       198  LOAD_GLOBAL              exec
              200  LOAD_FAST                'apod'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  POP_TOP          
              206  POP_BLOCK        
              208  JUMP_FORWARD        234  'to 234'
            210_0  COME_FROM_EXCEPT    196  '196'

 L.1230       210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L.1231       216  LOAD_GLOBAL              print
              218  LOAD_STR                 'error in apodise(), wrong function : '
              220  LOAD_FAST                'apod'
              222  BINARY_ADD       
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  POP_TOP          
              228  POP_EXCEPT       
              230  JUMP_FORWARD        234  'to 234'
              232  END_FINALLY      
            234_0  COME_FROM           230  '230'
            234_1  COME_FROM           208  '208'

 L.1232       234  LOAD_GLOBAL              dim
              236  LOAD_CONST               2
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  POP_TOP          

 L.1233       242  LOAD_GLOBAL              mult1d
              244  LOAD_STR                 'F2'
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  POP_TOP          
              250  JUMP_FORWARD        862  'to 862'
            252_0  COME_FROM           110  '110'

 L.1234       252  LOAD_FAST                'axis'
              254  LOAD_STR                 'F1'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   394  'to 394'

 L.1235       262  LOAD_FAST                'debug'
          264_266  POP_JUMP_IF_FALSE   280  'to 280'

 L.1235       268  LOAD_GLOBAL              print
              270  LOAD_STR                 'apod F1 '
              272  LOAD_FAST                'apod'
              274  BINARY_ADD       
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  POP_TOP          
            280_0  COME_FROM           264  '264'

 L.1236       280  LOAD_GLOBAL              col
              282  LOAD_CONST               1
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  POP_TOP          

 L.1237       288  LOAD_GLOBAL              dim
              290  LOAD_CONST               1
              292  CALL_FUNCTION_1       1  '1 positional argument'
              294  POP_TOP          

 L.1238       296  LOAD_GLOBAL              get_itype_1d
              298  CALL_FUNCTION_0       0  '0 positional arguments'
              300  LOAD_CONST               0
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   316  'to 316'

 L.1239       308  LOAD_GLOBAL              one
              310  CALL_FUNCTION_0       0  '0 positional arguments'
              312  POP_TOP          
              314  JUMP_FORWARD        338  'to 338'
            316_0  COME_FROM           304  '304'

 L.1241       316  LOAD_GLOBAL              itype
              318  LOAD_CONST               0
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  POP_TOP          

 L.1241       324  LOAD_GLOBAL              one
              326  CALL_FUNCTION_0       0  '0 positional arguments'
              328  POP_TOP          

 L.1241       330  LOAD_GLOBAL              itype
              332  LOAD_CONST               1
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  POP_TOP          
            338_0  COME_FROM           314  '314'

 L.1242       338  SETUP_EXCEPT        352  'to 352'

 L.1243       340  LOAD_GLOBAL              exec
              342  LOAD_FAST                'apod'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  POP_TOP          
              348  POP_BLOCK        
              350  JUMP_FORWARD        376  'to 376'
            352_0  COME_FROM_EXCEPT    338  '338'

 L.1244       352  POP_TOP          
              354  POP_TOP          
              356  POP_TOP          

 L.1245       358  LOAD_GLOBAL              print
              360  LOAD_STR                 'error in apodise(), wrong function : '
              362  LOAD_FAST                'apod'
              364  BINARY_ADD       
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  POP_TOP          
              370  POP_EXCEPT       
              372  JUMP_FORWARD        376  'to 376'
              374  END_FINALLY      
            376_0  COME_FROM           372  '372'
            376_1  COME_FROM           350  '350'

 L.1246       376  LOAD_GLOBAL              dim
              378  LOAD_CONST               2
              380  CALL_FUNCTION_1       1  '1 positional argument'
              382  POP_TOP          

 L.1247       384  LOAD_GLOBAL              mult1d
              386  LOAD_STR                 'F1'
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  POP_TOP          
              392  JUMP_FORWARD        862  'to 862'
            394_0  COME_FROM           258  '258'

 L.1249       394  LOAD_GLOBAL              Exception
              396  LOAD_STR                 'wrong axis'
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  RAISE_VARARGS_1       1  'exception instance'
          402_404  JUMP_FORWARD        862  'to 862'
            406_0  COME_FROM            92  '92'

 L.1250       406  LOAD_GLOBAL              get_dim
              408  CALL_FUNCTION_0       0  '0 positional arguments'
              410  LOAD_CONST               3
              412  COMPARE_OP               ==
          414_416  POP_JUMP_IF_FALSE   862  'to 862'

 L.1251       418  LOAD_FAST                'axis'
              420  LOAD_METHOD              upper
              422  CALL_METHOD_0         0  '0 positional arguments'
              424  STORE_FAST               'axis'

 L.1252       426  LOAD_FAST                'axis'
              428  LOAD_STR                 'F3'
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   570  'to 570'

 L.1253       436  LOAD_GLOBAL              plane
              438  LOAD_STR                 'f1'
              440  LOAD_CONST               1
              442  CALL_FUNCTION_2       2  '2 positional arguments'
              444  POP_TOP          

 L.1254       446  LOAD_GLOBAL              dim
              448  LOAD_CONST               2
              450  CALL_FUNCTION_1       1  '1 positional argument'
              452  POP_TOP          

 L.1254       454  LOAD_GLOBAL              row
              456  LOAD_CONST               1
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  POP_TOP          

 L.1255       462  LOAD_GLOBAL              dim
              464  LOAD_CONST               1
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  POP_TOP          

 L.1256       470  LOAD_GLOBAL              get_itype_1d
              472  CALL_FUNCTION_0       0  '0 positional arguments'
              474  LOAD_CONST               0
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   490  'to 490'

 L.1257       482  LOAD_GLOBAL              one
              484  CALL_FUNCTION_0       0  '0 positional arguments'
              486  POP_TOP          
              488  JUMP_FORWARD        512  'to 512'
            490_0  COME_FROM           478  '478'

 L.1259       490  LOAD_GLOBAL              itype
              492  LOAD_CONST               0
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  POP_TOP          

 L.1259       498  LOAD_GLOBAL              one
              500  CALL_FUNCTION_0       0  '0 positional arguments'
              502  POP_TOP          

 L.1259       504  LOAD_GLOBAL              itype
              506  LOAD_CONST               1
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  POP_TOP          
            512_0  COME_FROM           488  '488'

 L.1260       512  SETUP_EXCEPT        526  'to 526'

 L.1261       514  LOAD_GLOBAL              exec
              516  LOAD_FAST                'apod'
              518  CALL_FUNCTION_1       1  '1 positional argument'
              520  POP_TOP          
              522  POP_BLOCK        
              524  JUMP_FORWARD        550  'to 550'
            526_0  COME_FROM_EXCEPT    512  '512'

 L.1262       526  POP_TOP          
              528  POP_TOP          
              530  POP_TOP          

 L.1263       532  LOAD_GLOBAL              print
              534  LOAD_STR                 'error in apodise(), wrong function : '
              536  LOAD_FAST                'apod'
              538  BINARY_ADD       
              540  CALL_FUNCTION_1       1  '1 positional argument'
              542  POP_TOP          
              544  POP_EXCEPT       
              546  JUMP_FORWARD        550  'to 550'
              548  END_FINALLY      
            550_0  COME_FROM           546  '546'
            550_1  COME_FROM           524  '524'

 L.1264       550  LOAD_GLOBAL              dim
              552  LOAD_CONST               3
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  POP_TOP          

 L.1265       558  LOAD_GLOBAL              mult1d
              560  LOAD_STR                 'F3'
              562  CALL_FUNCTION_1       1  '1 positional argument'
              564  POP_TOP          
          566_568  JUMP_FORWARD        862  'to 862'
            570_0  COME_FROM           432  '432'

 L.1266       570  LOAD_FAST                'axis'
              572  LOAD_STR                 'F2'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   712  'to 712'

 L.1267       580  LOAD_GLOBAL              plane
              582  LOAD_STR                 'f1'
              584  LOAD_CONST               1
              586  CALL_FUNCTION_2       2  '2 positional arguments'
              588  POP_TOP          

 L.1268       590  LOAD_GLOBAL              dim
              592  LOAD_CONST               2
              594  CALL_FUNCTION_1       1  '1 positional argument'
              596  POP_TOP          

 L.1268       598  LOAD_GLOBAL              col
              600  LOAD_CONST               1
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  POP_TOP          

 L.1269       606  LOAD_GLOBAL              dim
              608  LOAD_CONST               1
              610  CALL_FUNCTION_1       1  '1 positional argument'
              612  POP_TOP          

 L.1270       614  LOAD_GLOBAL              get_itype_1d
              616  CALL_FUNCTION_0       0  '0 positional arguments'
              618  LOAD_CONST               0
              620  COMPARE_OP               ==
          622_624  POP_JUMP_IF_FALSE   634  'to 634'

 L.1271       626  LOAD_GLOBAL              one
              628  CALL_FUNCTION_0       0  '0 positional arguments'
              630  POP_TOP          
              632  JUMP_FORWARD        656  'to 656'
            634_0  COME_FROM           622  '622'

 L.1273       634  LOAD_GLOBAL              itype
              636  LOAD_CONST               0
              638  CALL_FUNCTION_1       1  '1 positional argument'
              640  POP_TOP          

 L.1273       642  LOAD_GLOBAL              one
              644  CALL_FUNCTION_0       0  '0 positional arguments'
              646  POP_TOP          

 L.1273       648  LOAD_GLOBAL              itype
              650  LOAD_CONST               1
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  POP_TOP          
            656_0  COME_FROM           632  '632'

 L.1274       656  SETUP_EXCEPT        670  'to 670'

 L.1275       658  LOAD_GLOBAL              exec
              660  LOAD_FAST                'apod'
              662  CALL_FUNCTION_1       1  '1 positional argument'
              664  POP_TOP          
              666  POP_BLOCK        
              668  JUMP_FORWARD        694  'to 694'
            670_0  COME_FROM_EXCEPT    656  '656'

 L.1276       670  POP_TOP          
              672  POP_TOP          
              674  POP_TOP          

 L.1277       676  LOAD_GLOBAL              print
              678  LOAD_STR                 'error in apodise(), wrong function : '
              680  LOAD_FAST                'apod'
              682  BINARY_ADD       
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  POP_TOP          
              688  POP_EXCEPT       
              690  JUMP_FORWARD        694  'to 694'
              692  END_FINALLY      
            694_0  COME_FROM           690  '690'
            694_1  COME_FROM           668  '668'

 L.1278       694  LOAD_GLOBAL              dim
              696  LOAD_CONST               2
              698  CALL_FUNCTION_1       1  '1 positional argument'
              700  POP_TOP          

 L.1279       702  LOAD_GLOBAL              mult1d
              704  LOAD_STR                 'F2'
              706  CALL_FUNCTION_1       1  '1 positional argument'
            708_0  COME_FROM           250  '250'
              708  POP_TOP          
              710  JUMP_FORWARD        862  'to 862'
            712_0  COME_FROM           576  '576'

 L.1280       712  LOAD_FAST                'axis'
              714  LOAD_STR                 'F1'
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE   854  'to 854'

 L.1281       722  LOAD_GLOBAL              plane
              724  LOAD_STR                 'f2'
              726  LOAD_CONST               1
              728  CALL_FUNCTION_2       2  '2 positional arguments'
              730  POP_TOP          

 L.1282       732  LOAD_GLOBAL              dim
              734  LOAD_CONST               2
              736  CALL_FUNCTION_1       1  '1 positional argument'
              738  POP_TOP          

 L.1282       740  LOAD_GLOBAL              col
              742  LOAD_CONST               1
              744  CALL_FUNCTION_1       1  '1 positional argument'
              746  POP_TOP          

 L.1283       748  LOAD_GLOBAL              dim
              750  LOAD_CONST               1
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  POP_TOP          

 L.1284       756  LOAD_GLOBAL              get_itype_1d
              758  CALL_FUNCTION_0       0  '0 positional arguments'
              760  LOAD_CONST               0
              762  COMPARE_OP               ==
          764_766  POP_JUMP_IF_FALSE   776  'to 776'

 L.1285       768  LOAD_GLOBAL              one
              770  CALL_FUNCTION_0       0  '0 positional arguments'
              772  POP_TOP          
              774  JUMP_FORWARD        798  'to 798'
            776_0  COME_FROM           764  '764'

 L.1287       776  LOAD_GLOBAL              itype
              778  LOAD_CONST               0
              780  CALL_FUNCTION_1       1  '1 positional argument'
              782  POP_TOP          

 L.1287       784  LOAD_GLOBAL              one
              786  CALL_FUNCTION_0       0  '0 positional arguments'
              788  POP_TOP          

 L.1287       790  LOAD_GLOBAL              itype
              792  LOAD_CONST               1
              794  CALL_FUNCTION_1       1  '1 positional argument'
              796  POP_TOP          
            798_0  COME_FROM           774  '774'

 L.1288       798  SETUP_EXCEPT        812  'to 812'

 L.1289       800  LOAD_GLOBAL              exec
              802  LOAD_FAST                'apod'
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  POP_TOP          
              808  POP_BLOCK        
              810  JUMP_FORWARD        836  'to 836'
            812_0  COME_FROM_EXCEPT    798  '798'

 L.1290       812  POP_TOP          
              814  POP_TOP          
              816  POP_TOP          

 L.1291       818  LOAD_GLOBAL              print
              820  LOAD_STR                 'error in apodise(), wrong function : '
              822  LOAD_FAST                'apod'
              824  BINARY_ADD       
              826  CALL_FUNCTION_1       1  '1 positional argument'
              828  POP_TOP          
              830  POP_EXCEPT       
              832  JUMP_FORWARD        836  'to 836'
              834  END_FINALLY      
            836_0  COME_FROM           832  '832'
            836_1  COME_FROM           810  '810'

 L.1292       836  LOAD_GLOBAL              dim
              838  LOAD_CONST               2
              840  CALL_FUNCTION_1       1  '1 positional argument'
              842  POP_TOP          

 L.1293       844  LOAD_GLOBAL              mult1d
              846  LOAD_STR                 'F1'
              848  CALL_FUNCTION_1       1  '1 positional argument'
            850_0  COME_FROM           392  '392'
              850  POP_TOP          
              852  JUMP_FORWARD        862  'to 862'
            854_0  COME_FROM           718  '718'

 L.1295       854  LOAD_GLOBAL              Exception
              856  LOAD_STR                 'wrong axis'
              858  CALL_FUNCTION_1       1  '1 positional argument'
              860  RAISE_VARARGS_1       1  'exception instance'
            862_0  COME_FROM           852  '852'
            862_1  COME_FROM           710  '710'
            862_2  COME_FROM           566  '566'
            862_3  COME_FROM           414  '414'
            862_4  COME_FROM           402  '402'
            862_5  COME_FROM            80  '80'

Parse error at or near `COME_FROM' instruction at offset 708_0


def apodise_f(apod, axis='F1'):
    """ apod is the function to be applied,
    it is a python callable sequence which realise the apodisation
    e.g.   "sin(0)"   "expbroad(10)"  "sqsin(0),expbroad(3)"  etc...
    (note the , to separate several simple  apodisations)
    
    M-A D. march 2006
    """
    if get_dim() == 1:
        eval(apod)
    else:
        if get_dim() == 2:
            axis = axis.upper()
            if axis == 'F2':
                row(1)
                dim(1)
                chsize(get_si2_2d())
                one()
                try:
                    exec(apod)
                except:
                    print('error in apodise(), wrong function : ' + apod)

                chsize(get_si1_2d() + get_si2_2d())
                put('data')
                chsize(get_si1_2d())
                one()
                chsize(get_si1_2d() + get_si2_2d())
                reverse()
                adddata()
                put('window')
                dim(2)
                apply('window')
            else:
                if axis == 'F1':
                    col(1)
                    dim(1)
                    chsize(get_si1_2d())
                    one()
                    try:
                        exec(apod)
                    except:
                        print('error in apodise(), wrong function : ' + apod)

                    reverse()
                    chsize(get_si1_2d() + get_si2_2d())
                    reverse()
                    put('data')
                    chsize(get_si2_2d())
                    one()
                    chsize(get_si1_2d() + get_si2_2d())
                    adddata()
                    put('window')
                    dim(2)
                    apply('window')
                else:
                    raise Exception('error with axis')
        else:
            raise Exception('not implemented yet !')


def apodise_p(apod, axis='F1'):
    if get_dim() == 1:
        lst = apod.split()
        leng = len(lst)
        i = 0
        while i < leng:
            apod = lst[i]
            print('parsing ' + apod)
            if apod == 'sin':
                i = i + 1
                arg = float(lst[i])
                sin(arg)
            else:
                if apod == 'sqsin':
                    i = i + 1
                    arg = float(lst[i])
                    sqsin(arg)
                else:
                    if apod == 'expbroad' or apod == 'em':
                        i = i + 1
                        arg = float(lst[i])
                        expbroad(arg)
                    else:
                        if apod == 'gaussbroad':
                            i = i + 1
                            arg = float(lst[i])
                            gaussbroad(arg)
                        else:
                            if apod == 'gaussenh':
                                i = i + 1
                                arg = float(lst[i])
                                i = i + 1
                                arg2 = float(lst[i])
                                gaussenh(arg, arg2)
                            else:
                                if apod == 'tm':
                                    i = i + 1
                                    arg = int(float(lst[i]))
                                    i = i + 1
                                    arg2 = int(float(lst[i]))
                                    tm(arg, arg2)
                                else:
                                    if apod == 'DO_NOTHING':
                                        pass
                                    else:
                                        raise Exception('Internal error in Apodisation -> ' + apod)
                                    i = i + 1

    else:
        if get_dim() == 2 or get_dim() == 3:
            axis = axis.upper()
            lst = apod.split()
            leng = len(lst)
            i = 0
            while i < leng:
                apod = lst[i]
                if apod == 'sin':
                    i = i + 1
                    arg = float(lst[i])
                    sin(arg, axis)
                else:
                    if apod == 'sqsin':
                        i = i + 1
                        arg = float(lst[i])
                        sqsin(arg, axis)
                    else:
                        if apod == 'em':
                            i = i + 1
                            arg = float(lst[i])
                            expbroad(arg, axis)
                        else:
                            if apod == 'expbroad':
                                i = i + 1
                                arg = float(lst[i])
                                expbroad(arg, axis)
                            else:
                                if apod == 'gaussbroad':
                                    i = i + 1
                                    arg = float(lst[i])
                                    gaussbroad(arg, axis)
                                else:
                                    if apod == 'gaussenh':
                                        i = i + 1
                                        arg = float(lst[i])
                                        i = i + 1
                                        arg2 = float(lst[i])
                                        gaussenh(arg, arg2, axis)
                                    else:
                                        if apod == 'tm':
                                            i = i + 1
                                            arg = int(lst[i])
                                            i = i + 1
                                            arg2 = int(lst[i])
                                            tm(arg, arg2, axis)
                                        else:
                                            if apod == 'DO_NOTHING':
                                                pass
                                            else:
                                                raise Exception('Internal error in Apodisation -> ' + apod)
                                            i = i + 1


def hanning(axis='F1'):
    """hanning apodisation"""
    if get_dim() == 1:
        sin(0.5)
    else:
        axis = axis.upper()
        if get_dim() == 2:
            sin(0.5, axis)
        else:
            if get_dim() == 3:
                sin(0.5, axis)


def bucket(start=0.5, end=9.5, bsize=0.04, file='bucket.cvs'):
    """
 This tool permits to realize a bucket integration from the current 1D data-set.
 You will have to determine  (all spectral values are in ppm)
   - start, end : the starting and ending points of the integration zone in the spectrum
   - bsize : the size of the bucket
   - file :the filename to which the result is written

 the "set to current window" button defines the starting and ending points of the integration zone from the current zoom window
 the "record" button permits to memorize the current parameters, which will be reused for the bucket integration.
 the "details" button displays the number and the size of the buckets currently defined.
 a non-integer size means that the integration will be performed on a varying number of data points 
   in order to insure a constant integration width in ppm.
   However, the integration intensity is not modified by the integration width.

 For a better bucket integration, you should be careful that :
   - the bucket size is not too small, size is better than number !
   - the baseline correction has been carefully done
   - the spectral window is correctly determined to encompass the meaningfull spectral zone.

 %programer%

  see also : int1d integrate.g

 %author% MA Delsuc
 %version% 5.2005
    """
    if get_dim() != 1:
        raise Exception('Available on 1D data only')
    com_max()
    if geta_max(1) == 0.0:
        raise Exception('Empty data-set !')
    if bsize < 0:
        raise Exception('Negative bucket size not allowed')
    if start - bsize / 2 < itop(get_si1_1d(), 1, 1):
        raise Exception('Starting point outside spectrum')
    if end + bsize / 2 > itop(1, 1, 1):
        raise Exception('Ending point outside spectrum')
    if (end - start) / bsize < 10:
        raise Exception('Integration zone too small or Bucket too large')
    put('data')
    if bsize < get_specw_1d / get_freq_1d / get_si1_1d:
        get('data')
        raise Exception('Bucket size smaller than digital resolution !')
    mkreal()
    int1d()
    fout = open(file)
    s = '# %i buckets with a mean size of %.2f data points' % (round((end - start + bsize) / bsize), get_si1_1d() * bsize * get_freq_1d() / get_specw_1d())
    print(s)
    fout.writelines(s)
    fout.writelines('center, bucket, bucket_size')
    here = min(start, end)
    here2 = here - bsize / 2
    there = max(start, end)
    while here2 < there:
        ih = round(ptoi(here2, 1, 1))
        next = here2 + bsize
        inext = round(ptoi(next, 1, 1))
        fout.writeline('%f, %f, %d' % (here, (val1d(ih) - val1d(inext)) / ((ih - inext) * bsize), ih - inext))
        here2 = next
        here = here + bsize

    get('data')
    close(fout)


def auditinitial(auditfilename='audit_trail.html', title='NPK Processing', append=1):
    """ initialize the audit trail file
    
    auditfilename is the name of the audit file
    if the file does not exist it is created and initialized,
    if append ==1 and if the file exists, content will be added to it, this is the default behaviour
    """
    from ..v1 import NPK_version
    NPK_version = NPK_version
    if auditfilename == 'mute':
        return 'mute'
    if os.path.exists(auditfilename) and append == 1:
        auditfile = open(auditfilename, 'a')
    else:
        auditfile = open(auditfilename, 'w')
        auditfile.writelines('\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n<meta name="description" content="audit trail of NPK processing"/>\n<meta name="generator" content="NPK, version %(NPK_version)s"/>\n<title>%(title)s</title>\n</head>\n<body>\n' % vars())
    auditfile.writelines('<h1>' + title + '</h1>\n')
    auditfile.writelines('<h2>Processing conditions</h2>\n <ul><li>date: <b>' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime()) + '</b></li>\n')
    auditfile.writelines('<li>working directory :<b>%s</b></li>\n' % os.path.abspath(os.curdir))
    auditfile.writelines('<li>command line :<b>' + repr(sys.argv) + '</b></li>\n')
    auditfile.writelines('<li>NPK version: <b>' + NPK_version + '</b></li>\n')
    auditfile.writelines('<li>SPIKE kernel version: <b>' + get_version() + '</b></li>\n')
    auditfile.writelines('</ul>\n')
    return auditfile


def audittrail(auditfile, phtx, *argl):
    """ management of the audit trail.
    
    first argument determines action : open close phase text
    arguments depends on the action

    audittrail(open, "title in audit file")
        opens the audit trail - use the argument as title
    audittrail(close)
        closes the audit trail
    audittrail(phase, "title of phase")
        start a new phase, creates a new heading in the audit trail
    audittrail(text, "text to write in audit trail", parameter_name, parameter_value, ...)
        writes in the audit trail

    if text is available on several arguments, several lines are displayed,
    in this case, the first arguments is the text/title, and the following arguments are
    by pair, with parameter_name  parameter_value 
    if phase mode <P> lines are added
    if text mode a <li> list is built
    """
    if auditfile == 'mute':
        return
        writemode = 0
        if phtx == 'close':
            if auditfile is not None:
                writemode = 0
        elif phtx == '3D-phase':
            pre = '</blockquote><hr size="7" noshade="noshade"/><h1>'
            post = '</h1><blockquote>'
            preline = '<p>'
            postline = '</p>\n'
            writemode = 1
        else:
            if phtx == 'phase':
                pre = '<hr width="80%" noshade="noshade"/><h2>'
                post = '</h2>\n'
                preline = ''
                postline = ''
                writemode = 1
            else:
                if phtx == 'text':
                    pre = '<ul>'
                    post = '</ul>'
                    preline = '<li>'
                    postline = '</li>\n'
                    writemode = 1
                else:
                    raise Exception('wrong key error in audit trail')
        if writemode:
            if auditfile is not None:
                auditfile.writelines(pre)
                text = argl[0]
                auditfile.writelines(preline + text)
                leng = len(argl)
                if leng > 1:
                    if phtx == 'text':
                        auditfile.writelines('<ul>')
                    for i in range(1, leng, 2):
                        auditfile.writelines(preline + str(argl[i]))
                        try:
                            text = re.sub('\n', '<br/>', str(argl[(i + 1)]))
                        except:
                            text = ' missing value'

                        auditfile.writelines(': <b>' + text + '</b>' + postline)

                    if phtx == 'text':
                        auditfile.writelines('</ul>\n')
                auditfile.writelines(postline)
                auditfile.write(post)
                auditfile.flush()
    else:
        for t in argl:
            print('--audit--' + repr(t))


def derivative(n, sm):
    """@sig public void derivative( int n, int sm )"""
    if get_dim() != 1:
        raise Exception('derivative is available in 1D only')
    shift = int(sm / 2) + 1
    for i in range(1, sm + 1):
        smooth(2)

    for i in range(1, n + 1):
        dsa(shift, -1)

    mult(-1)


def causal_corr(delay):
    """
    remove the effect of a time shift on the spectrum due to digital filtering (Bruker)

    """
    com_phase(0.0, -360.0 * delay)


def causalize(delay):
    """
    remove the effect of a time shift on the FID due to digital filtering (Bruker)

    brings back the beginning of the FID at the first data point
    shorten the FID length respectively
    """
    if get_dim() == 1:
        si = get_si1_1d()
        revf()
        chsize(4 * power2(si - 1))
        itype(1)
        ft()
        phase(0, -360.0 * delay)
        n = max(2 * int(delay), 0.0)
        real()
        iftbis()
        chsize(si - n)
        revf()
        print('CAUSALIZE 1D', delay, si, n, get_si1_1d(), get_ph0(), get_ph1())
    else:
        if get_dim() == 2:
            si = get_si2_2d()
            revf('f2')
            chsize(get_si1_2d(), 4 * power2(si - 1))
            if get_itype_2d() == 0 or get_itype_2d() == 2:
                itype(get_itype_2d() + 1)
            ft('f2')
            phase(0, -360.0 / delay, 'f2')
            n = max(2 * int(delay), 0.0)
            real('f2')
            iftbis('f2')
            chsize(get_si1_2d(), si - n)
            revf('f2')


def conv_n_p():
    """
    realizes the preparation of 2D FID acquired in n+p mode (echo / anti echo
    """
    for i in range(2, get_si1_2d() + 2, 2):
        k = i - 1
        row(k)
        dim(1)
        put('data')
        dim(2)
        row(i)
        dim(1)
        adddata()
        dim(2)
        put('row', k)
        row(i)
        dim(1)
        mult(-1.0)
        adddata()
        phase(90.0, 0.0)
        dim(2)
        put('row', i)


def autocalib_old():
    """
    on a 2D experiment, assuming the F2 axis is 1H
    try to detect spin nature from frequency, and apply the unified scale as proposed by IUPAC-2001
    WARNING, proteins tend to use DSS reference, where IUPAC imposes TMS
    this makes +2.66 ppm shift in 13C.
    IDEM, for 15N proteins tend to use NH3 reference, where IUPAC imposes MeNO3
    this makes a +385.50 ppm shift in 15N.
    """
    n15 = Nucleus.freq('15N', 1.0)
    c13 = Nucleus.freq('13C', 1.0)
    if get_dim() == 1:
        print('Nothing to do in F1')
    else:
        if get_dim() == 2:
            r = get_freq_1_2d() / get_freq_2_2d()
            if 0.09 < r and r < 0.11:
                print('set to 1H-15N')
                vish = n15
                ret = '15N'
            else:
                if 0.24 < r and r < 0.26:
                    print('set to 1H-13C')
                    vish = c13
                    ret = '13C'
                else:
                    if 0.98 < r and r < 1.02:
                        print('set to homonuclear')
                        vish = 1.0
                        ret = '1H'
                    else:
                        vish = r
                        print('unknown Nucleus')
                        ret = 'Unknown'
            decalh = itoh(get_si2_2d() / 2, 2, 2)
            zeroh = get_freq_2_2d() * 1000000 - decalh
            zerox = zeroh * vish
            decalx = get_freq_1_2d() * 1000000 - zerox
            offset(decalx - get_specw_1_2d() / 2, get_offset_2_2d())
        else:
            print('Not available yet')
            ret = 'None'
    return ret


def autocalib(mode='IUPAC'):
    """
    on a 2D experiment, assuming the F2 axis is 1H
    try to detect spin nature from frequency, and apply the unified scale as proposed by IUPAC-2001
        Harris et al. NMR Nomenclature: Nuclear Spin Properties and Conventions for Chemical Shifts—IUPAC Recommendations. Journal of Magnetic Resonance (2002) vol. 156 (2) pp. 323-326

    WARNING, a different setting for biomolecules was proposed in a IUPAC/IUB recommendation in 1998
        Markley et al. Recommendations for the presentation of NMR structures of proteins and nucleic acids. Journal of Molecular Biology (1998) vol. 280 (5) pp. 933-952
    This previous recommendation was only mentionning 2D 13C, 15N and 31P, but was using  different references

    Usage is to use 1998 recommendation for proteins and nucleic acids.
    these are enforced when mode = "IUB" or "biomolecule"
    this makes +2.6645 ppm shift in 13C.
    this makes a +380.4434 ppm shift in 15N.
    
    Returns the name of the defined nucleus in F1, "15N" "13C" "31P" or "None" if nothing was done
    """
    ret = 'None'
    if get_dim() == 1:
        print('Nothing to do in F1')
    else:
        if get_dim() == 2:
            F1 = get_freq_1_2d()
            F2 = get_freq_2_2d()
            for nuc in ('1H', '13C', '15N', '31P', '2H'):
                fnuc = Nucleus.freq(nuc, F2, mode)
                if abs(fnuc - F1) / fnuc < 0.001:
                    print('set to ', nuc)
                    vish = Nucleus.freq(nuc, 1.0, mode)
                    ret = nuc
                    break

            if ret != 'None':
                decalh = itoh(F2 / 2, 2, 2)
                zeroh = F2 * 1000000 - decalh
                zerox = zeroh * vish
                decalx = F1 * 1000000 - zerox
                off1 = decalx - get_specw_1_2d() / 2
                offset(off1, get_offset_2_2d())
        else:
            print('Not available yet')
    return ret


def hilbert(axis='F1'):
    """convert a real data set to a complex dataset by using the Hilbert transform

    the number of data point is doubled, thus hilbert();real() is (nearly) a null operation

    axis can be F1 F2 or F12

    in dim(1) no axis is needed
    does not work in dim(3) yet

    minimal error checking, done mostly by the FT operations.

    Note that a small apodisation is done on the Fourier transform to reduce truncation artifacts
    you might want to remove this in certain cases, for instance if you plan to have several hilbert()
    applied to the same data in sequence.

    see also : tocomplex() invhilbert()
    """
    if get_dim() == 1:
        if get_itype_1d() == 1:
            raise Exception('Wrong data format in hilbert()')
        si = get_si1_1d()
        chsize(2 * power2(get_si1_1d() - 2))
        iftbis()
        tm(1, int(get_si1_1d() * 0.6))
        chsize(get_si1_1d() * 2)
        ft()
        if 2 * si != get_si1_1d():
            chsize(2 * si)
    else:
        if get_dim() == 2:
            axis = axis.upper()
            if axis == 'F1' or axis == 'F12':
                if get_itype_2d() == 2 or get_itype_2d() == 3:
                    raise Exception('Wrong data format in hilbert()')
            else:
                si = get_si1_2d()
                chsize(2 * power2(get_si1_2d() - 2), get_si2_2d())
                iftbis('F1')
                tm(1, int(get_si1_2d() * 0.6), 'F1')
                chsize(get_si1_2d() * 2, get_si2_2d())
                ft('F1')
                if 2 * si != get_si1_2d():
                    chsize(2 * si, get_si2_2d())
                if axis == 'F2' or axis == 'F12':
                    if get_itype_2d() == 1 or get_itype_2d() == 3:
                        raise Exception('Wrong data mode in hilbert.g')
                    si = get_si2_2d()
                    chsize(get_si1_2d(), 2 * power2(get_si2_2d() - 2))
                    iftbis('F2')
                    tm(1, int(get_si2_2d() * 0.6), 'F2')
                    chsize(get_si1_2d(), get_si2_2d() * 2)
                    ft('F2')
                    if 2 * si != get_si2_2d():
                        chsize(get_si1_2d(), 2 * si)


def invhilbert(axis='F1'):
    """convert a complex data set to a real dataset by using the Hilbert transform

    the number of data point is unchanged,
    thus the final real dataset is zerofilled once compared to the initial
    
    invhilbert() is nearly equivalent to having zerofillied once before FT, but processing time is faster.

    despite the name, not quite the inverse of hilbert() !

    axis can be F1 F2 or F12

    in dim(1) no axis is needed
    does not work in dim(3) yet

    minimal error checking, done mostly by the FT operations.

    see also : tocomplex() hilbert()
    """
    if get_dim() == 1:
        if get_itype_1d() == 0:
            raise Exception('wrong data format in invhilbert()')
        si = get_si1_1d()
        chsize(2 * power2(get_si1_1d() - 2))
        ift()
        ftbis()
        if si != get_si1_1d():
            chsize(si)
    else:
        if get_dim() == 2:
            axis = axis.upper()
            if axis == 'F1' or axis == 'F12':
                if get_itype_2d() < 2:
                    raise Exception('wrong data format in invhilbert()')
                si = get_si1_2d()
                chsize(2 * power2(get_si1_2d() - 2), get_si2_2d())
                ift('F1')
                ftbis('F1')
                if si != get_si1_2d():
                    chsize(si, get_si2_2d())
            if axis == 'F2' or axis == 'F12':
                if get_itype_2d() % 2 == 0:
                    raise Exception('wrong data format in invhilbert()')
                si = get_si2_2d()
                chsize(get_si1_1d(), 2 * power2(get_si2_2d() - 2))
                ift('F2')
                ftbis('F2')
                if si != get_si2_2d():
                    chsize(get_si1_2d(), si)


def plane_size(axis='F1'):
    """
    returns (si1,si2) the size of the plane orthogonal to axis from the joined dataset
    """
    if get_c_dim() != 3:
        raise Exception('only on 3D data')
    ax = axis.upper()
    if ax == 'F1':
        return (
         get_c_sizef2(), get_c_sizef3())
    if ax == 'F2':
        return (
         get_c_sizef1(), get_c_sizef3())
    if ax == 'F3':
        return (
         get_c_sizef1(), get_c_sizef2())
    raise Exception('wrong axis')


def filec_status():
    """dumps the detailled header of a joined cache file
    used mostly for debugging
    """
    print('\n    Dim     : %i\n    FREQ    : %f\n                 F1       F2       F3\n    Size    : %8i %8i %8i\n    SW      : %8f %8f %8f\n    offsets : %8f %8f %8f\n    Freq    : %8f %8f %8f\n    ' % (get_c_dim(), get_c_freq(),
     get_c_sizef1(), get_c_sizef2(), get_c_sizef3(),
     get_c_specwf1(), get_c_specwf2(), get_c_specwf3(),
     get_c_offsf1(), get_c_offsf2(), get_c_offsf3(),
     get_c_freq1(), get_c_freq2(), get_c_freq3()))


def proc3d(sourcefile, destinationfile, plane_to_process, commands, context):
    """
 this macro processes a 3D file using the cache system (join, getc, putc)
 it permits to handle very large files, which would not fit into memory.

 sourcefile         : is the initial data-set
 destinationfile    : is the result of the process
 plane_to_process   : either F1, F2 or F3 (NOT F12 or F123)
                      F1 means : planes perpendicular to F1, thus the planes containing the F2 and F3 axes.
 commands           : a string holding the commands to be applied to each plane in 2D notation
 context            : a dictionary containing the variables needed to execute commands,
                      i.e. exec(commands,context) will actually be used
                      usually built from globals() and locals()

 the commands are the regular commands you would used to process a 2D data-set.
 when called without parameters, 'commands' can be several line long, as typed
 when proc3d is called with parameters on the line, then 'commands' should be a single
 command line within quotes.

 e.g.
 proc3(ser_file, F1_proc, "F1",  'sin(0.2,"f12"); ft_sim();  phase(30,-40,f2); real("f12"); ft_tppi()')
        #  process axes f3 and f2 as 2D
 proc3(F1_proc, full_proc, "F2", 'sin(0.2,"f1"); ft_tppi(); real("f1");  bcorr(3,"f1")')
        #  process axis f1

 would process a whole 3D in 2 steps.

    """
    debug = 0
    infile = sourcefile
    join(infile)
    if get_c_dim() != 3:
        raise Exception('available on 3D data only')
    else:
        outfile = destinationfile
        if infile == outfile:
            raise Exception('input file and output file must be different')
        else:
            axis = plane_to_process.upper()
            if axis not in ('F1', 'F2', 'F3'):
                raise Exception('error with axis')
            ancdim = get_dim()
            dim(2)
            join(infile)
            si1, si2 = plane_size(axis)
            getc(axis, 1, 1, 1, si1, si2)
            exec(commands, context)
            it1, it2 = get_itype(2)
            si1ap = get_si1_2d()
            si2ap = get_si2_2d()
            if axis == 'F1':
                itc = int(get_c_type() / 4)
                it = 4 * itc + 2 * it1 + it2
            else:
                if axis == 'F3':
                    itc = get_c_type() % 2
                    it = 4 * it1 + 2 * it2 + itc
                else:
                    if axis == 'F2':
                        itc = int(get_c_type() / 2)
                        itc = itc % 2
                        it = 4 * it1 + 2 * itc + it2
    if axis == 'F1':
        newfilec(outfile, get_c_freq(), it, (
         get_c_sizef1(), get_si1_2d(), get_si2_2d()), (
         get_c_offsf1(), get_offset_1_2d(), get_offset_2_2d()), (
         get_c_specwf1(), get_specw_1_2d(), get_specw_2_2d()), (
         get_c_freq1(), get_freq_1_2d(), get_freq_2_2d()))
        iter = get_c_sizef1()
    else:
        if axis == 'F2':
            newfilec(outfile, get_c_freq(), it, (
             get_si1_2d(), get_c_sizef2(), get_si2_2d()), (
             get_offset_1_2d(), get_c_offsf2(), get_offset_2_2d()), (
             get_specw_1_2d(), get_c_specwf2(), get_specw_2_2d()), (
             get_freq_1_2d(), get_c_freq2(), get_freq_2_2d()))
            iter = get_c_sizef2()
        else:
            if axis == 'F3':
                newfilec(outfile, get_c_freq(), it, (
                 get_si1_2d(), get_si2_2d(), get_c_sizef3()), (
                 get_offset_1_2d(), get_offset_2_2d(), get_c_offsf3()), (
                 get_specw_1_2d(), get_specw_2_2d(), get_c_specwf3()), (
                 get_freq_1_2d(), get_freq_2_2d(), get_c_freq3()))
                iter = get_c_sizef3()
            disjoin()
            join(outfile)
            dim(2)
            if debug == 1:
                print('PROC3D : number of plane to process :', iter)
                iter = min(iter, 4)
                print('PROC3D : limited to ', iter, 'for debuging purposes')
                print('PROC3D : planes : (%i,%i)->(%i,%i)' % (si1, si2, si1ap, si2ap))
            for i in range(1, iter + 1):
                print('### IN : %s, OUT %s, plane %d / %d' % (infile, outfile, i, iter))
                join(infile)
                getc(axis, i, 1, 1, si1, si2)
                exec(commands, context)
                join(outfile)
                putc(axis, i, 1, 1, si1ap, si2ap)

            join(infile)
            disjoin()
            join(outfile)
            disjoin()


def tocomplex(axis='F1'):
    """ tocomplex  --  make dataset complex
    """
    if get_dim() == 1:
        if get_itype_1d() == 0:
            hilbert()
            itype(1)
        else:
            if get_dim() == 2:
                axis = axis.upper()
                if axis == 'F1':
                    if get_itype_2d() == 1 or get_itype_2d() == 0:
                        hilbert('F1')
            elif axis == 'F2':
                if get_itype_2d() == 2 or get_itype_2d() == 0:
                    hilbert('F2')
                elif axis == 'F12' or axis == 'F21':
                    if get_itype_2d() == 0:
                        hilbert('F12')
                    elif get_itype_2d() == 1:
                        hilbert('F1')
                    elif get_itype_2d() == 2:
                        hilbert('F2')
            else:
                raise Exception('Wrong argument in tocomplex()')
    else:
        raise Exception('Wrong dimension in tocomplex()')


def toreal(axis='F1'):
    """ toreal  --  make dataset real
    """
    if get_dim() == 1:
        if get_itype_1d() == 1:
            real()
        else:
            if get_dim() == 2:
                axis = axis.upper()
                if axis == 'F1':
                    if get_itype_2d() == 2 or get_itype_2d() == 3:
                        real('F1')
            elif axis == 'F2':
                if get_itype_2d() == 1 or get_itype_2d() == 3:
                    real('F2')
                elif axis == 'F12' or axis == 'F21':
                    if get_itype_2d() == 1:
                        real('F2')
                    elif get_itype_2d() == 2:
                        real('F1')
                    elif get_itype_2d() == 3:
                        real('F12')
            else:
                raise Exception('Wrong argument in toreal')
    else:
        raise Exception('Wrong dimension in toreal')


def flat_solvent(param, delay=0.0):
    """reduces the solvent signal supposed to be at the carrier frequency
    to be applied on the time domain, before Fourier transform
    
    actually performs a "baseline" fit type of processing on the FID, real and imaginary parts are handled independantly
    param is either
        polynomial
        moving_average
        polynomial+moving_average
        moving_average+polynomial
    and determines the fitting algo used.
    
    delays is the timezeo delay offset (not implemented yet)
    """
    if param == 'no':
        return
    else:
        if get_dim() == 1:
            i = get_si1_1d()
        else:
            if get_dim() == 2:
                i = get_si2_2d()
            else:
                raise Exception('Not implemented in 3D')
        if get_dim() == 1:
            svspecw = get_specw_1d()
            svfreq = get_freq_1d()
            svoff = get_offset_1d()
            dim(2)
            itype(get_itype_1d())
            chsize(1, get_si1_1d())
            rem_1d = 1
            com_put('row', 1)
        else:
            if get_dim() == 2:
                rem_1d = 0
        row(1)
        if get_itype_1d() != 0:
            rem_uswa = 1
            if power2(get_si1_1d()) != get_si1_1d():
                chsize(get_si1_2d(), 2 * power2(get_si1_1d()))
            uswa('F2')
            modifysize(2 * get_si1_2d(), get_si2_2d() / 2)
        else:
            rem_uswa = 0
    if param == 'polynomial':
        bcorrp0()
        segm1(0)
        bcorr(3, 'F2')
        bcorrp0()
    else:
        if param == 'moving_average':
            bcorrp1()
            segm1(0)
            bcorr(3, 'F2')
            bcorrp0()
        else:
            if param == 'polynomial+moving_average':
                bcorrp0()
                segm1(0)
                bcorr(3, 'F2')
                bcorrp0()
                bcorrp1()
                segm1(0)
                bcorr(3, 'F2')
                bcorrp0()
            else:
                if param == 'moving_average+polynomial':
                    bcorrp1()
                    segm1(0)
                    bcorr(3, 'F2')
                    bcorrp0()
                    bcorrp0()
                    segm1(0)
                    bcorr(3, 'F2')
                    bcorrp0()
                if rem_uswa != 0:
                    modifysize(get_si1_2d() / 2, get_si2_2d() * 2)
                    swa('F2')
                    if get_si1_1d() != get_si2_2d():
                        chsize(get_si1_2d(), get_si1_1d())
                if rem_1d == 1:
                    row(1)
                    dim(1)
                    specw(svspecw)
                    freq(get_freq(), svfreq)
                    offset(svoff)


def burg_mirror(n, bsz):
    if n == -1:
        msz = get_si1_1d()
    else:
        msz = get_si1_1d() - 2 * n - 2
    mirror(n)
    burg(msz + bsz)
    reverse()
    chsize(bsz)
    reverse


def burg_back(nsz):
    if get_dim() != 1:
        raise Exception('Available in 1D only')
    if nsz <= get_si1_1d():
        raise Exception('Wrong size')
    if nsz != int(nsz / 2) * 2:
        raise Exception('size should be even')
    itype(1)
    reverse()
    burg(int(nsz))
    reverse()


def burg2d_back(axis, nsz):
    if get_dim() != 2:
        raise Exception('Available in 2D only')
    else:
        axis = axis.upper()
        if nsz != int(nsz / 2) * 2:
            raise Exception('size should be even')
        elif axis == 'F1':
            if nsz <= get_si1_2d():
                raise Exception('Wrong size')
            osz = get_si1_2d()
            chsize(nsz, get_si2_2d())
            ext = 'col'
            imax = get_si2_2d()
        else:
            if axis == 'F2':
                if nsz <= get_si2_2d():
                    raise Exception('Wrong size')
                osz = get_si2_2d()
                chsize(get_si1_1d(), nsz)
                ext = 'row'
                imax = get_si1_1d()
            else:
                raise Exception('Wrong axis for LP')
        if ext == 'row':
            for i in range(1, imax + 1):
                row(i)
                dim(1)
                chsize(osz)
                itype(1)
                reverse()
                burg(nsz)
                reverse()
                dim(2)
                put('row', i)

        else:
            for i in range(1, imax + 1):
                col(i)
                dim(1)
                chsize(osz)
                itype(1)
                reverse()
                burg(nsz)
                reverse()
                dim(2)
                put('col', i)


def burg2d_mirror(axis, n, bsz):
    axis = axis.upper()
    if axis == 'F1':
        if bsz <= get_si1_2d():
            raise Exception('Wrong size')
        elif n == -1:
            msz = get_si1_2d()
        else:
            msz = get_si1_2d() - 2 * n - 2
        cmd = 'col'
        count = get_si2_2d()
        osz = get_si1_2d()
        chsize(bsz, get_si2_2d())
    else:
        if axis == 'F2':
            if bsz <= get_si2_2d():
                raise Exception('Wrong size')
            elif n == -1:
                msz = get_si2_2d()
            else:
                msz = get_si2_2d() - 2 * n - 2
            cmd = 'col'
            count = get_si1_1d()
            osz = get_si2_2d()
            chsize(get_si1_1d(), bsz)
        else:
            raise Exception('wrong axis in burg2d_mirror.g')
    dim(2)
    if cmd == 'row':
        for i in range(1, count + 1):
            row(i)
            dim(1)
            chsize(osz)
            mirror(n)
            burg(msz + bsz)
            reverse()
            chsize(bsz)
            reverse()
            dim(2)
            put('row', i)

    else:
        for i in range(1, count + 1):
            col(i)
            dim(1)
            chsize(osz)
            mirror(n)
            burg(msz + bsz)
            reverse()
            chsize(bsz)
            reverse()
            dim(2)
            put('col', i)

    dim(2)


def burg2d(axis='F1', nsz=None):
    """apply burg extension to all columns (or rows) of current 2D
    axis is either "F1" or "F2"
    nsz is extended size, default (None) implies doubling of the size
    """
    writec('toto.gf2')
    if get_dim() != 2:
        raise Exception('available in 2D only')
    else:
        axis = axis.upper()
        if nsz is None:
            if axis == 'F1':
                nsz = 2 * get_si1_2d()
            else:
                if axis == 'F2':
                    nsz = 2 * get_si2_2d()
        elif axis == 'F1':
            if nsz <= get_si1_2d():
                raise Exception('Wrong size')
            osz = get_si1_2d()
            chsize(int(nsz), get_si2_2d())
            ext = 'col'
            imax = get_si2_2d()
        else:
            if axis == 'F2':
                if nsz <= get_si2_2d():
                    raise Exception('Wrong size')
                osz = get_si2_2d()
                chsize(get_si1_1d(), int(nsz))
                ext = 'row'
                imax = get_si1_2d()
            else:
                raise Exception('Wrong axis for LP')
    if ext == 'col':
        print(get_order())
        for i in range(1, imax + 1):
            col(i)
            dim(1)
            chsize(osz)
            itype(1)
            burg(int(nsz))
            dim(2)
            put('col', i)

    else:
        for i in range(1, imax + 1):
            row(i)
            dim(1)
            chsize(osz)
            itype(1)
            burg(int(nsz))
            dim(2)
            put('row', i)


def dc_offset(zone):
    """corrects each FID of a dataset for constant offset, estimated on the last % of the fid
    
    zone has a value between 0 and 1; 1 means the whole data set, 0.1 means the last 10%
    """
    if get_dim() == 1:
        if zone == 0:
            d = 1
        else:
            d = (1 - zone) * get_si1_1d()
        evaln(d, get_si1_1d())
        s = get_shift()
        addbase(s)
        return s
    if get_dim() == 2:
        if zone == 0:
            d = 1
        else:
            d = (1 - zone) * get_si1_2d()
        s = 0
        for i in range(1, get_si1_2d() + 1):
            dim(2)
            row(i)
            dim(1)
            evaln(d, get_si1_2d())
            s = s + get_shift()
            addbase(get_shift())
            dim(2)
            put('row', i)

        return s / get_si1_2d()
    raise Exception('dc-offset.g reste a faire')


def bcorr_quest(p=4, axis='F1'):
    """ apply the QUEST baseline correction, based on the Linear Prediction reconstruction on the beginning of the FID.

        p is the number of point to reconstruct
        axis is the axis to process when in nD
        
        works on complex as well as real datasets.

        from
            MAGMA. 2004 May;16(6):284-96. 2004
            Time-domain quantitation of 1H short echo-time signals: background accommodation.
            Ratiney H, Coenradie Y, Cavassila S, van Ormondt D, Graveron-Demilly D.
    """
    if get_dim() == 1 and not p < 0:
        if p > get_si1_1d() / 2:
            raise Exception('wrong value for QUEST order')
        si = get_si1_1d()
        sip2 = int(2 * power2(si - 2))
        it = get_itype_1d()
        chsize(int(sip2))
        if it == 0:
            iftbis()
        else:
            ift()
        reverse()
        chsize(sip2 - int(p))
        reverse()
        burg_back(sip2)
        if it == 0:
            ftbis()
        else:
            ft()
        chsize(si)
    else:
        if get_dim() == 2:
            axis = axis.upper()
            if not axis == 'F1':
                if axis == 'F12':
                    if p < 0 or p > get_si1_2d() / 2:
                        raise Exception('wrong value for QUEST order')
                    else:
                        si = get_si1_2d()
                        sip2 = 2 * power2(si - 2)
                        it = int(get_itype_2d() / 2)
                        chsize(sip2, get_si2_2d())
                        if it == 0:
                            iftbis('F1')
                        else:
                            ift('F1')
                        reverse('F1')
                        chsize(sip2 - p, get_si2_2d())
                        reverse('F1')
                        burg2d_back('F1', sip2)
                        if it == 0:
                            ftbis('F1')
                        else:
                            ft('F1')
                    chsize(si, get_si2_2d())
                if axis == 'F2' or axis == 'F12':
                    if p < 0 or p > get_si2_2d():
                        raise Exception('wrong value for QUEST mode')
                    else:
                        si = get_si2_2d()
                        sip2 = 2 * power2(si - 2)
                        it = get_itype_2d() % 2
                        chsize(get_si1_2d(), sip2)
                        if it == 0:
                            iftbis('F2')
                        else:
                            ift('F2')
                    reverse('F2')
                    chsize(get_si1_2d(), sip2 - p)
                    reverse('F2')
                    burg2d_back('F2', sip2)
                    if it == 0:
                        ftbis('F2')
            else:
                ft('F2')
            chsize(get_si1_2d(), si)
        else:
            raise Exception('reste a faire en 3D')


def bcorr_offset(spec_n=30, axis='F1'):
    """correct for an offset of the spectrum, computed from an empty region of the spectrum
    
    spec_n is the argument to spec_noise() 
    axis is the axis to process when in nD 
    """
    print('bcorr_offset', spec_n, axis)
    if get_dim() == 1:
        spec_noise(spec_n)
        addbase(get_shift())
    else:
        if get_dim() == 2:
            axis = axis.upper()
            if axis == 'F1' or axis == 'F12':
                for i in range(1, get_si2_2d() + 1):
                    col(i)
                    dim(1)
                    spec_noise(spec_n)
                    addbase(get_shift())
                    dim(2)
                    put('col', i)

            if axis == 'F2' or axis == 'F12':
                for i in range(1, get_si1_2d() + 1):
                    row(i)
                    dim(1)
                    spec_noise(spec_n)
                    addbase(get_shift())
                    dim(2)
                    put('row', i)

        else:
            raise Exception('reste a faire')


def add_files(list_of_files, list_of_coefficients=[]):
    """ add a list of files weighted by the given coefficients
    
    if coefficients are lacking, no weighting is made
    """
    list_loc = list_of_files
    if list_of_coefficients == []:
        coef_loc = [
         1.0] * len(list_loc)
    else:
        coef_loc = list_of_coefficients
    if len(list_loc) != len(coef_loc):
        raise Exception('the two lists should be of the same length')
    read(list_loc.pop())
    dloc = get_dim()
    mult(coef_loc.pop())
    put('data')
    for i in range(len(coef_loc)):
        read(list_loc.pop())
        if dloc != get_dim():
            raise Exception('datasets are not all of the same dimension')
        mult(coef_loc.pop())
        adddata()
        put('data')


def shear(slope, pivot):
    """shearing of a given NMR 2D experiment
        realized by a frequency shift of all the F1 spectra
        pivot is the position of the invariant column (0 is left, 1 is right)"""
    if get_dim() != 2:
        raise Exception('To be applied on 2D only')
    else:
        si = get_si1_2d()
        sisi = 2 * power2(si - 2)
        chsize(sisi, get_si2_2d())
        if get_itype_2d() == 0 or get_itype_2d() == 1:
            thetype = 'real'
            iftbis('f1')
        else:
            thetype = 'complex'
            ift('f1')
        si2 = get_si2_2d()
        sw2 = get_specw_2_2d()
        sw1 = get_specw_1_2d()
        for i in range(1, si2 + 1):
            col(i)
            dim(1)
            f2 = (i - pivot * si2) * sw2 / si2
            decal = f2 * si / sw1
            coef = -180.0 * decal * slope
            phase(0.5 * coef, coef)
            dim(2)
            put('col', i)

        if thetype == 'real':
            ftbis('f1')
        else:
            ft('f1')
    chsize(si, get_si2_2d())


def SecsyToCosy():
    """shearing operation that transform a "secsy" symmetry type experiment to a "cosy" one  """
    shear(1.0, 0.5)


def CosyToSecsy():
    """shearing operation that transform a "cosy" symmetry type experiment to a "secsy" one  """
    shear(-1.0, 0.5)


def InadequateToCosy():
    """shearing operation that transform a "Inadequate" symmetry type experiment to a "cosy" one  """
    shear(-1.0, 0.5)


def CosyToInadequate():
    """shearing operation that transform a "cosy" symmetry type experiment to a "Inadequate" one  """
    shear(1.0, 0.5)


def tilt(slope, pivot):
    """tilt of a 2D experiment
    realized by a frequency shift of all the F2 spectra
    pivot is the position of the invariant row (0 is bottom, 1 is top)"""
    if get_dim() != 2:
        raise Exception('To be applied on 2D only')
    else:
        si = get_si2_2d()
        sisi = 2 * power2(si - 2)
        chsize(get_si1_2d(), sisi)
        if get_itype_2d() == 0 or get_itype_2d() == 2:
            thetype = 'real'
            iftbis('F2')
        else:
            thetype = 'complex'
            ift('F2')
        si1 = get_si1_2d()
        sw1 = get_specw_1_2d()
        sw2 = get_specw_2_2d()
        for i in range(1, si1 + 1):
            row(i)
            dim(1)
            f1 = (i - pivot * si1) * sw1 / si1
            decal = f1 * si / sw2
            coef = -180.0 * slope * decal
            phase(0.5 * coef, coef)
            dim(2)
            put('row', i)

        if thetype == 'real':
            ftbis('F2')
        else:
            ft('F2')
    chsize(get_si1_2d(), si)


def JResTilt():
    """tilt operation that transform a JRes experiment to a symmetric one  """
    tilt(1.0, 0.5)


def Symmetrize2D(type='Cosy', algorithm='mean'):
    """realize the symmetrization of the current 2D
    available types are : Inadequate,Cosy, JRes
    available algorithm are : mean (X+Y)/2 , smallest value min(X,Y), 
        and continuous (XY^2+YX^2)/(X^2 + Y^2) (not for JRes)
    """
    dim(2)
    toreal('F12')
    if type.upper() == 'COSY':
        SymmetrizeCosy(algorithm)
    else:
        if type.upper() == 'JRES':
            SymmetrizeJRes(algorithm)
        else:
            if type.upper() == 'INADEQUATE':
                SymmetrizeInadequate(algorithm)


def SymmetrizeCosy(algorithm='mean'):
    """realize the symmetrization of COSY 2D 
    available algorithm are : mean (X+Y)/2 , smallest value min(X,Y), continuous (XY^2+YX^2)/(X^2 + Y^2)
    """
    si1 = get_si1_2d()
    si2 = get_si2_2d()
    if get_si1_2d() < get_si2_2d():
        axe = 'F1'
        iftbis('F1')
        chsize(get_si2_2d(), get_si2_2d())
        ftbis('F1')
    else:
        if get_si1_2d() > get_si2_2d():
            axe = 'F2'
            iftbis('F2')
            chsize(get_si1_2d(), get_si1_2d())
            ftbis('F2')
        else:
            axe = 'none'
    if algorithm.upper() == 'MEAN':
        symetrize(1)
    else:
        if algorithm.upper() == 'MIN':
            symetrize(2)
        else:
            if algorithm.upper() == 'CONTINUOUS':
                symetrize(3)
            else:
                raise Exception('algorithm not available')
    if axe != 'none':
        iftbis(axe)
        chsize(si1, si2)
        ftbis(axe)


def SymmetrizeJRes(algorithm='mean'):
    """realize the symmetrization of JRes 2D 
    available algorithm are : mean (X+Y)/2 , smallest value min(X,Y)
    """
    put('data')
    reverse('F1')
    if algorithm.upper() == 'MEAN':
        adddata()
        mult(0.5)
    else:
        if algorithm.upper() == 'MIN':
            mindata()
        else:
            raise Exception('algorithm not available')


def SymmetrizeInadequate(algorithm='mean'):
    """realize the symmetrization of INADEQUATE 2D 
    available algorithm are : mean (X+Y)/2 , smallest value min(X,Y), continuous (XY^2+YX^2)/(X^2 + Y^2)
    """
    InadequateToCosy()
    SymmetrizeCosy(algorithm)
    CosyToInadequate()


def local_proj(axis='F1', algo='M', f1_left=0, f2_left=0, f1_right=0, f2_right=0):
    """
    realize a local projection of the 2D data-set
    axis : "F1" - "F2" : the axis along which the projection is performed
    algo : "M" - "S" ; Mean or Skyline 
    f1_left, f2_left, f1_right, f2_right : the coordinates of the local projection
        O (default) means that the complete data-set will be used, thus:
        f1_left=1 f2_left=1 f1_right=get_si1_2D(), f2_right=get_si2_2D()
    thus : local_proj("F1","M") is equivalent to proj("F1","M")

    WARNING - local_proj("F1") will create a F2 1D.
    """
    if get_dim() != 2:
        raise Exception('To be applied on 2D only')
    elif f1_left == 0:
        f1_left = 1
    else:
        if f2_left == 0:
            f2_left = 1
        if f1_right == 0:
            f1_right = get_si1_2d()
        if f2_right == 0:
            f2_right = get_si2_2d()
        if algo not in ('M', 'S'):
            raise Exception('Wrong algorithme for local_proj()')
        if axis.upper() == 'F1':
            dim(2)
            row(1)
            dim(1)
            zero()
            put('data')
            for i in range(f1_left, f1_right + 1):
                dim(2)
                row(i)
                dim(1)
                if algo.upper() == 'M':
                    adddata()
                else:
                    maxdata()
                put('data')

            dim(1)
            get('data')
            extract(f2_left, f2_right)
        else:
            if axis.upper() == 'F2':
                dim(2)
                col(1)
                dim(1)
                zero()
                put('data')
                for i in range(f2_left, f2_right + 1):
                    dim(2)
                    col(i)
                    dim(1)
                    if algo.upper() == 'M':
                        adddata()
                    else:
                        maxdata()
                    put('data')

                dim(1)
                get('data')
                extract(f1_left, f1_right)
            else:
                raise Exception('Wrong axis in local_proj()')


def local_proj_3d(axis='F1', algo='M', f1_left=0, f2_left=0, f3_left=0, f1_right=0, f2_right=0, f3_right=0):
    """
    realize a local projection of the 3D data-set
    axis : "F1" - "F2" - "F3": the axis along which the projection is performed
    algo : "M" - "S" ; Mean or Skyline 
    f1_left, f2_left, f3_lest, f1_right, f2_right, f3_left : the coordinates of the local projection
        O (default) means that the complete data-set will be used, thus:
        f1_left=1 f2_left=1 f3_left=1  f1_right=get_si1_3D(), f2_right=get_si2_3D() f3_right=get_si3_3D()
    """
    if get_c_dim() != 3:
        raise Exception('Works only on a JOINed 3D')
    elif f1_left == 0:
        f1_left = 1
    else:
        if f2_left == 0:
            f2_left = 1
        elif f3_left == 0:
            f3_left = 1
        else:
            if f1_right == 0:
                f1_right = get_c_sizef1()
            elif f2_right == 0:
                f2_right = get_c_sizef2()
            elif f3_right == 0:
                f3_right = get_c_sizef3()
            else:
                si1 = f1_right - f1_left + 1
                si2 = f2_right - f2_left + 1
                si3 = f3_right - f3_left + 1
                dim(2)
                if axis == 'F1':
                    p01, s01, s02 = f1_left, f2_left, f3_left
                    pn1, sn1, sn2 = f1_right, f2_right, f3_right
                else:
                    if axis == 'F2':
                        s01, p01, s02 = f1_left, f2_left, f3_left
                        sn1, pn1, sn2 = f1_right, f2_right, f3_right
                    else:
                        if axis == 'F3':
                            s01, s02, p01 = f1_left, f2_left, f3_left
                            sn1, sn2, pn1 = f1_right, f2_right, f3_right
                        else:
                            raise Exception('Wrong axis')
            siz = pn1 - p01 + 1
            dim(2)
            chsize(sn1 - s01 + 1, sn2 - s02 + 1)
            if algo[0] == 'S':
                todo = 'maxdata()'
            else:
                if algo[0] == 'M':
                    todo = 'adddata()'
                else:
                    raise Exception('wrong algorithm')
        try:
            if algo[1] == 'A':
                tabs = 1
            else:
                tabs = 0
        except:
            tabs = 0

    getc(axis, 1, s01, s02, sn1, sn2)
    if tabs == 1:
        itype(0)
        com_abs()
    put('data')
    for i in range(p01, pn1 + 1):
        getc(axis, i, s01, s02, sn1, sn2)
        if tabs == 1:
            itype(0)
            com_abs()
        eval(todo)
        put('data')

    get('data')
    if algo == 'M':
        mult(1 / siz)


def pkwrite_p(filepeak):
    """write the content of the peak table in the kernel to a peak file
    
    the file is formated as a property list
    coordinates are in index, widths are in Hz, phases in degrees.
    format is not fully compatible with the format used in Gifa 5, as the coordinates are ouput in index
    it will write the 1D, 2D or 3D peak table, depending on get_dim()
    """
    fout = open(filepeak, 'w')
    pph2 = get_specw_2_2d() / get_si2_2d()
    ppp2 = pph2 / get_freq_2_2d()
    pph1 = get_specw_1_2d() / get_si1_2d()
    ppp1 = pph1 / get_freq_1_2d()
    if get_dim() == 1:
        fout.write('# 1D Peak file, date :' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime()) + '\n')
        fout.write('# ID=Freq Amp Amp_err F1_Freq_err F1_Width F1_Width_err F1_phase F1_phase_err F2_Freq_err F2_Width F2_Width_err F2_phase F2_phase_err Type Label\n')
        for i in range(1, get_npk1d() + 1):
            fout.write(repr(i) + '=' + repr(geta_pk1d_f(i)) + ' ' + repr(geta_pk1d_a(i)) + ' ' + repr(geta_pk1d_a_err(i)) + ' ' + repr(ppp1 * geta_pk1d_f_err(i)) + ' ' + repr(pph1 * geta_pk1d_w(i)) + ' ' + repr(pph1 * geta_pk1d_w_err(i)) + ' 0 0 ' + repr(geta_pk1d_t(i)) + ' ' + repr(geta_pk1d_id(i)))
            fout.write('\n')

    else:
        if get_dim() == 2:
            fout.write('# 2D Peak file, date :' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime()) + '\n')
            fout.write('# ID=F1_Freq F2_Freq Amp Amp_err F1_Freq_err F1_Width F1_Width_err F1_phase F1_phase_err F2_Freq_err F2_Width F2_Width_err F2_phase F2_phase_err Type Label\n')
            for i in range(1, get_npk2d() + 1):
                fout.write(repr(i) + '=' + repr(geta_pk2d_f1f(i)) + ' ' + repr(geta_pk2d_f2f(i)) + ' ' + repr(geta_pk2d_a(i)) + ' ' + repr(geta_pk2d_a_err(i)) + ' ' + repr(ppp1 * geta_pk2d_f1f_err(i)) + ' ' + repr(pph1 * geta_pk2d_f1w(i)) + ' ' + repr(pph1 * geta_pk2d_f1w_err(i)) + ' 0 0 ' + repr(ppp2 * geta_pk2d_f2f_err(i)) + ' ' + repr(pph2 * geta_pk2d_f2w(i)) + ' ' + repr(pph2 * geta_pk2d_f2w_err(i)) + ' 0 0 ' + repr(geta_pk2d_t(i)) + ' ' + repr(geta_pk2d_id(i)))
                fout.write('\n')

        else:
            if get_dim() == 3:
                fout.close()
                raise Exception('reste a faire')
    fout.close()


def pkfilter(mode='add', tol=10):
    """peak filtering
    
    first try...
    """
    print('   nbr de pics:', get_npk2d())


def pksym_p(mode='add', tol=10):
    """peak symmetrisation algorithm
    
    first try...
    """
    if get_dim() != 2:
        raise Exception('works only on 2D data-sets')
    print('   nbr de pics:', get_npk2d())
    t = time.clock()
    print('----------debut du timer')
    for i in range(1, get_npk2d() + 1):
        f1i = geta_pk2d_f1f(i)
        f2i = geta_pk2d_f2f(i)
        for j in range(i, get_npk2d() + 1):
            diff1 = f1i - geta_pk2d_f1f(j)
            diff2 = f2i - geta_pk2d_f2f(j)
            diff = math.sqrt(diff1 * diff1 / 10 + diff2 * diff2 / 10)
            if diff > 10:
                a = i + j

    t = time.clock() - t
    print('----------fin du timer', str(t))


def peak1d_integ(index, factor=0.1, thresh=0, slope=0.001):
    """ compute the integration zone around a given 1D peak

    returns (left,right) as the integration zones
    left and right are determined as the points were either 
        value gets below thresh  (default value 0)
            determines an absolute stop point
        value gets below top_of_peak*factor (default value 0.1 = 10%)
            determines a relative stop point
        value > lower_point_so_far and abs(value-previous)>top_of_peak*slope (default value 0.001 = 0.1%)
            allows going up as much as slope*top
    warning, definitions are different from the integ kernel command
    """
    dim(1)
    if index < 0 or index > get_si1_1d():
        raise Exception('Wrong index value')
    toreal()
    top = val1d(index)
    level = max(thresh, top * factor)
    print(level)
    left = index - 1
    lval = val1d(left)
    prev = top
    while left > 1 and lval > level and lval - prev < slope * top:
        prev = min(lval, prev)
        left = left - 1
        lval = val1d(left)

    right = index + 1
    lval = val1d(right)
    prev = top
    while right < get_si1_1d() and lval > level and lval - prev < slope * top:
        prev = min(lval, prev)
        right = right + 1
        lval = val1d(right)

    return (
     left, right)


def spectral_zone(left, right, axis='F1', left_unit='ppm', right_unit='ppm'):
    """
    extract one spectral zone of the spectrum
    left float
       the left border of the extract zone, in unit
    left_unit enum ppm hz index 
       the unit in which spec_zone_left is given
    right float
       the right border of the extract zone, in unit
    right_unit enum ppm hz index
       the unit in which spec_zone_right is given
    axis enum F1 F2 F3
        if in 2D or 3D, the axis along the extract is to be done,
        ignored if in 1D

    returns [left,right]
        the left and right coordinates of the extracted spectral zone in index
    """
    print(left, right, axis, left_unit, right_unit)
    if get_dim() == 1:
        pass
    else:
        if get_dim() == 2:
            if axis == 'F1':
                iaxis = 1
                si = get_si1_2d()
            else:
                if axis == 'F2':
                    iaxis = 2
                    si = get_si2_2d()
                else:
                    raise Exception('Error with axis in spectral_zone')
            if left_unit == 'ppm':
                l = ptoi(left, 2, iaxis)
                print('L :', left, 'ppm ->', l)
            else:
                if left_unit == 'hz':
                    l = htoi(left, 2, iaxis)
                else:
                    if left_unit == 'index':
                        l = left
                    else:
                        raise Exception('Error with left unit')
            if right_unit == 'ppm':
                r = ptoi(right, 2, iaxis)
                print('R :', right, 'ppm ->', r)
            else:
                if right_unit == 'hz':
                    r = htoi(right, 2, iaxis)
                else:
                    if right_unit == 'index':
                        r = right
                    else:
                        raise Exception('Error with righ unit')
            l = int(max(1, round(l)))
            r = int(min(si, round(r)))
            if l > r:
                raise Exception('Wrong spectral zone coordinates : ' + repr(l) + ' ' + repr(r))
            else:
                if r - l < 8:
                    raise Exception('spectral zone too small')
                if l != 1 or r != si:
                    if axis == 'F1':
                        extract(l, 1, r, get_si2_2d())
                    else:
                        if axis == 'F2':
                            extract(1, l, get_si1_2d(), r)
        return (
         l, r)


def aparm():
    """
    computes phase correction form a reconstruction of the beginning of the FID
    """
    if get_dim() != 1:
        raise Exception('aparm works only in 1D')
    put('data')
    ift()
    if get_si1_1d() > 256:
        chsize(256)
    ft()
    chsize(32 * get_si1_1d())
    ift()
    print(get_si1_1d())
    reverse()
    burg(get_si1_1d() + 64)
    reverse()
    modulus()
    imax = 1
    vmax = val1d(1)
    for i in range(1, 65):
        if val1d(i) > vmax:
            imax = i
            vmax = val1d(i)

    get('data')
    print('max at', 32 - (imax - 1) / 32)
    ph1 = -360 * (imax - 1) / 64
    print('PH1', ph1)
    phase(0, ph1)
    ift()
    ph0 = -(180 / math.pi) * math.atan(val1d(2) / val1d(1))
    print('PH0', ph0)
    ft()
    phase(ph0, 0)


def writet(filename):
    """
    writes the 1D memory as a simple 1D series
    skip # and ; comments

    """
    try:
        fout = open(filename, 'w')
    except:
        raise Exception(filename, ' cannot be opened')

    dim(1)
    fout.write('#text data file, created by NPK :' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime()) + '\n')
    fout.write('#dim=1\n')
    fout.write('#size=%i\n' % get_si1_1d())
    fout.write('#itype=%i\n' % get_itype_1d())
    fout.write('#frequency=%i\n' % get_freq_1d())
    fout.write('#specw=%i\n' % get_specw_1d())
    fout.write('#offset=%i\n' % get_offset_1d())
    for i in range(get_si1_1d()):
        fout.write('%f\n' % val1d(i + 1))

    fout.close()


def load(filename):
    """
    load in 1D memory a simple 1D series
    skip # and ; comments

    """
    fin = open(filename)
    list = []
    f = fin.read()
    lines = f.split('\n')
    for v in lines:
        v = v.lstrip()
        if v and v[0] != '#' and v[0] != ';':
            list.append(float(v))

    fin.close()
    dim(1)
    chsize(len(list))
    for i in range(len(list)):
        setval(i + 1, list[i])


def config_get(config, section, option, default=None, raw=0, vars=None):
    """read a value from the configuration, with a default value"""
    if config.has_option(section, option):
        return config.get(section, option, raw=raw, vars=vars)
    return default


def config_getint(config, section, option, default=0, raw=0, vars=None):
    """read a int value from the configuration, with a default value"""
    return int(config_get(config, section, option, default=default, raw=raw, vars=vars))


def config_getfloat(config, section, option, default=0.0, raw=0, vars=None):
    """read a float value from the configuration, with a default value"""
    return float(config_get(config, section, option, default=default, raw=raw, vars=vars))


def config_getboolean(config, section, option, default='OFF', raw=0, vars=vars):
    """read a boolean value from the configuration, with a default value"""
    v = config_get(config, section, option, default=default, raw=raw, vars=vars)
    if v.lower() not in ConfigParser.SafeConfigParser._boolean_states:
        raise (
         ValueError, 'Not a boolean: %s' % v)
    return ConfigParser.SafeConfigParser._boolean_states[v.lower()]


class Generic_Tests(unittest.TestCase):

    def setUp(self):
        rootfiles = os.getcwd()
        cp = ConfigParser.SafeConfigParser()
        cp.read(rootfiles + '/NPKv1.mscf')
        self.TestFolder = config_get(cp, 'npkv1', 'TestFolder')
        self.fid = os.path.join(self.TestFolder, 'fid')
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def test_load(self):
        load(self.fid)


if __name__ == '__main__':
    unittest.main()