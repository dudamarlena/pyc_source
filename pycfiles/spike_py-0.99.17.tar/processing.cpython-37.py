# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/processing.py
# Compiled at: 2020-02-04 11:07:43
# Size of source mod 2**32: 44166 bytes
"""
Processing.py

This program makes the processing of a 2D-FTICR dataset

First version by Marc-Andre on 2011-09-23.
"""
from __future__ import print_function, division
import sys, os, time, unittest, numpy as np
from numpy import fft as npfft
import tables
from scipy.signal import decimate, lfilter, cheby1, medfilt, medfilt2d
import multiprocessing as mp, pickle, functools
from .NPKConfigParser import NPKConfigParser
from .FTICR import *
import File.Apex as Import_2D_Apex
import File.Solarix as Import_2D_Solarix
Import_2D = {'Apex':Import_2D_Apex, 
 'Solarix':Import_2D_Solarix}
from .NPKData import copyaxes
from File.HDF5File import HDF5File, determine_chunkshape
from .util import progressbar as pg
from .util import widgets
from .util import mpiutil
from .NPKData import as_cpx
from util.simple_logger2 import TeeLogger
debug = 0
interfproc = False
if sys.version_info[0] < 3:
    from itertools import imap
else:
    imap = map
    xrange = range
LARGESTDATA = 8589934592
SIZEMIN = 1024

def intelliround(x):
    """returns a number rounded to the nearest 'round' (easy to FT) integer"""
    from math import log
    lx = int(log(x) / log(2))
    err = 2 * x
    r = 0
    for t in (2 ** lx, 2 ** (lx + 1), 3 * 2 ** (lx - 1), 5 * 2 ** (lx - 2), 9 * 2 ** (lx - 3), 15 * 2 ** (lx - 3)):
        if abs(t - x) < err:
            err = abs(t - x)
            r = t
            if err == 0:
                break

    return r


def pred_sizes_zf(d0, zf=0, sizemin=SIZEMIN):
    """
    given an input data set, determines the optimum size s1,s2 to process it with a zerofilling of zf
    zf = +n is doubling n times along each axis
    zf = -n is halving n times along each axis
    zf = 0 is no zerofiling
    however, axes can never get smaller than sizemin
    returns (si1, si2, ...) as the dataset dimension
    """

    def dopow2(s, zf, sizemin):
        """return s * 2^zf rounded to the nearest 2^n or p*2^n"""
        sm = min(sizemin, s)
        s1 = s * pow(2, zf)
        s = max(sm, s1)
        return intelliround(s)

    def dopow(s, zf, sizemin):
        """do the math  not used"""
        sm = min(sizemin, s)
        s1 = s * pow(2, zf)
        s = max(sm, s1)
        return int(s)

    r = []
    for i in range(d0.dim):
        r.append(dopow2(d0.axes(i + 1).size, zf, sizemin))

    if debug > 0:
        print(r, functools.reduce(lambda x, y: x * y, r) // 1024 // 1024, 'Mpoint')
    return tuple(r)


def pred_sizes(d0, szmult=(1, 1), sizemin=SIZEMIN):
    """
    given an input data set, determines the optimum size s1,s2 to process it
        with a size multiplicant of szmult
    szmult (szm1, szm2)     where szm1 is multiplicant for s1 and szm2 for s2
    szmx = 1 : no change  /  2 : size doubling  /  0.5 : size halving
    any strictly positive value is possible, 0.2 0.33 1.1 2 2.2 5 etc...
    
    however, axes can never get smaller than sizemin
    returns (si1, si2, ...) as the dataset dimension
    """

    def dosize(s, szm, sizemin):
        """return s * 2^zf rounded to the nearest 2^n or 3*2^n"""
        sm = min(sizemin, s)
        s1 = s * szm
        s = max(sm, s1)
        return intelliround(s)

    r = []
    for i in range(d0.dim):
        r.append(dosize(d0.axes(i + 1).size, szmult[i], sizemin))

    if debug > 0:
        print(r, functools.reduce(lambda x, y: x * y, r) // 1024 // 1024, 'Mpoint')
    return tuple(r)


def comp_sizes(d0, zflist=None, szmlist=None, largest=LARGESTDATA, sizemin=SIZEMIN, vignette=True):
    """
    return a list with data-sizes, computed either
        zflist : from zerofilling index    eg : (1,0,-1)
        szmlist : from multiplicant pairs  eg : (2,2)

    largest determines the largest dataset allowed
    sizemini determines the minimum size when downzerofilling
    when vignette == True (default) a minimum size data (defined by sizemini) is appended to the list
    """
    sizes = []
    if zflist != None:
        if szmlist != None:
            raise Exception('Please define only one value : zerofilling or sizes multipliers')
    if zflist == None:
        if szmlist == None:
            zflist = [
             0]
    szres = []
    if szmlist != None:
        sm1, sm2 = szmlist
        while True:
            si1, si2 = pred_sizes(d0, (sm1, sm2))
            if debug > 0:
                print((sm1, sm2))
            if debug > 0:
                print((si1, si2))
            if si1 * si2 <= 1.5 * SIZEMIN * SIZEMIN:
                break
            szres.append((si1, si2))
            sm1, sm2 = 0.25 * sm1, 0.25 * sm2

    if zflist != None:
        for zf in zflist:
            szres.append(pred_sizes_zf(d0, zf))

    for si1, si2 in szres:
        while si1 * si2 > largest:
            si2 //= 2
            print('Warning, reducing SI2 to %s' % si2)

        sz = (
         si1, si2)
        if sz not in sizes:
            sizes.append(sz)

    if vignette:
        sz1, sz2 = sizes[(-1)]
        while sz1 >= sizemin:
            sz1 //= 2

        while sz2 >= sizemin:
            sz2 //= 2

        if (
         sz1, sz2) not in sizes:
            sizes.append((2 * sz1, 2 * sz2))
    if debug > 0:
        print('sizes to process', sizes)
    return sizes


def apod(d, size, axis=0):
    """
    apply apodisation and change size
    4 cases
        - 2D F1 or F2
        - 1D coming from F1 or F2
    1D or 2D in F2 are default  - apodisation in apod_sin(0.5)
    in 2D F1 (axis=1) - apodisation is kaiser(5)
    
    3 situations
        size after >  size before
        size after <  size before
        size after == size before
    """

    def do_apod(ax):
        if ax == 1:
            d.kaiser(beta=5, axis=todo)
        else:
            d.kaiser(beta=3.5, axis=todo)

    todo = d.test_axis(axis)
    initialsize = d.axes(todo).size
    if d.dim == 1:
        szf1 = size
        szf2 = None
    else:
        if d.dim == 2:
            if todo == 1:
                szf1 = size
                szf2 = d.size2
            else:
                szf1 = d.size1
                szf2 = size
        elif initialsize < size:
            do_apod(axis)
            d.chsize(szf1, szf2)
        else:
            if initialsize > size:
                d.chsize(szf1, szf2)
                do_apod(axis)
            else:
                do_apod(axis)
        return d


def hmclear(d):
    """
    given a 1D spectrum d, set to zeros all points betwen freq 0 and highmass
    helps compression
    """
    ihm = int(d.axis1.mztoi(d.axis1.highmass))
    d.buffer[:ihm] = 0.0
    return d


def iterargF2(dinp, size, scan):
    """an iterator used by the F2 processing to allow multiprocessing or MPI set-up"""
    for i in range(scan):
        r = dinp.row(i)
        yield (r, size)


def _do_proc_F2(data):
    """do the elementary F2 processing - called by the mp loop"""
    r, size = data
    apod(r, size)
    r.rfft()
    return r


def do_proc_F2mp(dinp, doutp, parameter):
    """do the F2 processing in MP"""
    size = doutp.axis2.size
    scan = min(dinp.size1, doutp.size1)
    F2widgets = ['Processing F2: ', widgets.Percentage(), ' ', widgets.Bar(marker='-', left='[', right=']'), widgets.ETA()]
    pbar = pg.ProgressBar(widgets=F2widgets, maxval=scan).start()
    xarg = iterargF2(dinp, size, scan)
    if parameter.mp:
        res = Pool.imap(_do_proc_F2, xarg)
        for i, r in enumerate(res):
            doutp.set_row(i, r)
            pbar.update(i + 1)

    else:
        if mpiutil.MPI_size > 1:
            res = mpiutil.enum_imap(_do_proc_F2, xarg)
            for i, r in res:
                doutp.set_row(i, r)
                pbar.update(i + 1)

        else:
            res = imap(_do_proc_F2, xarg)
            for i, r in enumerate(res):
                doutp.set_row(i, r)
                pbar.update(i + 1)

    pbar.finish()


def do_proc_F2(dinp, doutp, parameter):
    """do the F2 processing - serial code"""
    size = doutp.axis2.size
    scan = min(dinp.size1, doutp.size1)
    F2widgets = [
     'Processing F2: ', widgets.Percentage(), ' ', widgets.Bar(marker='-', left='[', right=']'), widgets.ETA()]
    pbar = pg.ProgressBar(widgets=F2widgets, maxval=scan).start()
    print('############  in do_proc_F2 #########')
    print('dinp.axis1.itype ', dinp.axis1.itype)
    print('dinp.axis2.itype ', dinp.axis2.itype)
    print('doutp.axis1.itype ', doutp.axis1.itype)
    print('doutp.axis2.itype ', doutp.axis2.itype)
    print('dinp.axis1.size ', dinp.axis1.size)
    print('dinp.axis2.size ', dinp.axis2.size)
    print('doutp.axis1.size ', doutp.axis1.size)
    print('doutp.axis2.size ', doutp.axis2.size)
    print('########################### doutp.report() ')
    print(doutp.report())
    for i in xrange(scan):
        r = dinp.row(i)
        apod(r, size)
        r.rfft()
        if parameter.compress_outfile:
            r = hmclear(r)
        doutp.set_row(i, r)
        pbar.update(i + 1)
        if interfproc:
            output = open('InterfProc/progbar.pkl', 'wb')
            pb = ['F2', int((i + 1) / float(scan) * 100)]
            pickle.dump(pb, output)
            output.close()

    pbar.finish()


def do_proc_F1(dinp, doutp, parameter):
    """scan all cols of dinp, apply proc() and store into doutp"""
    size = doutp.axis1.size
    scan = min(dinp.size2, doutp.size2)
    F1widgets = ['Processing F1: ', widgets.Percentage(), ' ', widgets.Bar(marker='-', left='[', right=']'), widgets.ETA()]
    pbar = pg.ProgressBar(widgets=F1widgets, maxval=scan).start()
    for i in xrange(scan):
        c = dinp.col(i)
        apod(c, size)
        c.rfft()
        buff = c.get_buffer()
        b = buff.copy()
        for i in range(10):
            b = b[(b - b.mean() < 3 * b.std())]

        if parameter.do_F1:
            if parameter.do_rem_ridge:
                c -= b.mean()
        if parameter.compress_outfile:
            threshold = parameter.compress_level * b.std()
            c.zeroing(threshold)
            c = hmclear(c)
        doutp.set_col(i, c)
        pbar.update(i)

    pbar.finish()


def do_proc_F1_modu(dinp, doutp, parameter):
    """as do_proc_F1, but applies hypercomplex modulus() at the end"""
    size = 2 * doutp.axis1.size
    scan = min(dinp.size2, doutp.size2)
    F1widgets = ['Processing F1 modu: ', widgets.Percentage(), ' ', widgets.Bar(marker='-', left='[', right=']'), widgets.ETA()]
    pbar = pg.ProgressBar(widgets=F1widgets, maxval=scan).start()
    d = FTICRData(buffer=(np.zeros((2 * doutp.size1, 2))))
    for i in xrange(scan):
        d.chsize(2 * doutp.size1, 2)
        for off in (0, 1):
            p = dinp.col(2 * i + off)
            apod(p, size)
            p.rfft()
            d.set_col(off, p)

        d.axis1.itype = 1
        d.axis2.itype = 1
        d.modulus()
        c = d.col(0)
        buff = c.get_buffer()
        b = buff.copy()
        for i in range(10):
            b = b[(b - b.mean() < 3 * b.std())]

        if parameter.do_F1:
            if parameter.do_rem_ridge:
                c -= b.mean()
        if parameter.compress_outfile:
            threshold = parameter.compress_level * b.std()
            c.zeroing(threshold)
            c = hmclear(c)
        doutp.set_col(i, c)
        pbar.update(i + 1)

    pbar.finish()


def _do_proc_F1_demodu_modu(data):
    """given a pair of columns, return the processed demodued FTed modulused column"""
    c0, c1, shift, size, parameter = data
    if c0.buffer.max() == 0:
        if c1.buffer.max() == 0:
            return np.zeros(size // 2)
    d = FTICRData(buffer=(np.zeros((c0.size1, 2))))
    d.set_col(0, c0)
    d.set_col(1, c1)
    d.axis1.itype = 0
    d.axis2.itype = 1
    if parameter.samplingfile is not None:
        d.axis1.load_sampling(parameter.samplingfile)
        samp = d.axis1.get_sampling()
        if parameter.samplingfile_fake:
            d.set_buffer(d.get_buffer()[samp])
        d.zf()
    d.f1demodu(shift)
    if parameter.do_urqrd:
        d.urqrd(k=(parameter.urqrd_rank), iterations=(parameter.urqrd_iterations), axis=1)
    if parameter.do_sane:
        d.sane(rank=(parameter.sane_rank), iterations=(parameter.sane_iterations), axis=1)
    if parameter.samplingfile is not None:
        if parameter.do_pgsane:
            d.chsize(size, d.size2)
            d.pg_sane(iterations=(parameter.pgsane_iterations), rank=(parameter.pgsane_rank), sampling=samp, Lthresh=(parameter.pgsane_threshold), axis=1, size=size)
    apod(d, size, axis=1)
    d.rfft(axis=1)
    d.modulus()
    buff = d.col(0).get_buffer()
    b = buff.copy()
    for i in range(10):
        b = b[(b - b.mean() < 3 * b.std())]

    if parameter.do_F1:
        if parameter.do_rem_ridge:
            buff -= b.mean()
    if parameter.compress_outfile:
        threshold = parameter.compress_level * b.std()
        buff[abs(buff) < threshold] = 0.0
    return buff


def iterarg(dinp, rot, size, parameter):
    """an iterator used by the processing to allow  multiprocessing or MPI set-up"""
    for i in range(0, dinp.size2, 2):
        c0 = dinp.col(i)
        c1 = dinp.col(i + 1)
        yield (
         c0, c1, rot, size, parameter)


def do_proc_F1_demodu_modu(dinp, doutp, parameter):
    """as do_proc_F1, but applies demodu and then complex modulus() at the end"""
    size = 2 * doutp.axis1.size
    scan = min(dinp.size2, doutp.size2)
    F1widgets = ['Processing F1 demodu-modulus: ', widgets.Percentage(), ' ', widgets.Bar(marker='-', left='[', right=']'), widgets.ETA()]
    pbar = pg.ProgressBar(widgets=F1widgets, maxval=scan).start()
    if parameter.freq_f1demodu == 0:
        hshift = dinp.axis2.lowfreq
    else:
        hshift = parameter.freq_f1demodu
    shift = doutp.axis1.htoi(hshift)
    rot = dinp.axis1.htoi(hshift)
    if parameter.samplingfile is not None:
        dinp.axis1.load_sampling(parameter.samplingfile)
        cdinp = dinp.col(0)
        cdinp.zf()
        rot = cdinp.axis1.htoi(hshift)
        del cdinp
    elif debug > 0:
        print('LEFT_POINT', shift)
    else:
        doutp.axis1.offsetfreq = hshift
        xarg = iterarg(dinp, rot, size, parameter)
        if parameter.mp:
            res = Pool.imap(_do_proc_F1_demodu_modu, xarg)
            for i, buf in enumerate(res):
                doutp.buffer[:, i] = buf
                pbar.update(i + 1)

        else:
            if mpiutil.MPI_size > 1:
                res = mpiutil.enum_imap(_do_proc_F1_demodu_modu, xarg)
                for i, buf in res:
                    doutp.buffer[:, i] = buf
                    pbar.update(i + 1)
                    if interfproc:
                        output = open('InterfProc/progbar.pkl', 'wb')
                        pb = ['F1', int((i + 1) / float(scan) * 100)]
                        pickle.dump(pb, output)
                        output.close()

                if interfproc:
                    output = open('InterfProc/progbar.pkl', 'wb')
                    pb = ['end']
                    pickle.dump(pb, output)
                    output.close()
            else:
                res = imap(_do_proc_F1_demodu_modu, xarg)
                for i, buf in enumerate(res):
                    doutp.buffer[:, i] = buf
                    pbar.update(i + 1)

    pbar.finish()


def do_process2D(dinp, datatemp, doutp, parameter):
    """
    apply the processing to an input 2D data set : dinp
    result is found in an output file : doutp
    
    dinp and doutp should have been created before, size of doutp will determine the processing
    will use a temporay file if needed
    """
    if debug > 1:
        for f, d in ((parameter.infile, dinp), (parameter.interfile, datatemp), (parameter.outfile, doutp)):
            print('----------', f)
            print(d)

    t00 = time.time()
    if parameter.do_F2:
        print('######### processing in F2')
        print('------ From:\n%s\n------ To:\n%s\n' % (dinp.report(), datatemp.report()))
        do_proc_F2mp(dinp, datatemp, parameter)
        print_time(time.time() - t00, 'F2 processing time')
    if parameter.do_F1:
        print('######### processing in F1')
        print('------ From\n%s\n------ To:\n%s\n' % (datatemp.report(), doutp.report()))
        t0 = time.time()
        if parameter.do_f1demodu and parameter.do_modulus:
            do_proc_F1_demodu_modu(datatemp, doutp, parameter)
        else:
            if parameter.do_modulus:
                do_proc_F1_modu(datatemp, doutp, parameter)
            else:
                do_proc_F1(datatemp, doutp, parameter)
        print_time(time.time() - t0, 'F1 processing time')
    print_time(time.time() - t00, 'F1-F2 processing time')


def downsample2D(data, outp, n1, n2, compress=False, compress_level=3.0):
    """
    takes data (a 2D) and generate a smaller dataset downsampled by factor (n1,n2) on each axis
    then returned data-set is n1*n2 times smaller
    - do a filtered decimation along n2
    - simply takes the mean along n1
    - set to zero all entries below 3*sigma if compress is True
    ** Not fully tested on non powers of 2 **
    """
    if debug > 0:
        print('in downsample2D : %s x %s' % (n1, n2))
    for i in xrange(0, data.size1, n1):
        temp = np.zeros(data.size2 // n2)
        for j in xrange(n1):
            if n2 > 1:
                try:
                    yy = decimate((data.row(i + j).buffer), (int(n2)), ftype='fir', zero_phase=True)
                except TypeError:
                    yy = decimate((data.row(i + j).buffer), (int(n2)), ftype='fir')

            else:
                yy = data.row(i + j).buffer
            temp += yy

        temp *= 1.0 / n1
        if compress:
            b = temp.copy()
            for j in range(3):
                b = b[(b - b.mean() < 3 * b.std())]

            threshold = compress_level * b.std()
            temp[abs(temp) < threshold] = 0.0
        outp.buffer[i // n1, :] = temp

    copyaxes(data, outp)
    outp.adapt_size()
    return outp


def load_input(name):
    """load input file and returns it, in read-only mode"""
    if debug > 0:
        print('reading', name)
    hf = HDF5File(name, 'r')
    d0 = hf.load()
    d0.hdf5file = hf
    return d0


class Proc_Parameters(object):
    __doc__ = 'this class is a container for processing parameters'

    def __init__(self, configfile=None):
        """initialisation, see processe.mscf for comments on parameters"""
        self.do_F2 = True
        self.do_F1 = True
        self.do_modulus = True
        self.do_rem_ridge = True
        self.do_f1demodu = True
        self.do_urqrd = False
        self.urqrd_rank = 20
        self.urqrd_iterations = 3
        self.do_sane = False
        self.sane_rank = 20
        self.sane_iterations = 1
        self.do_pgsane = False
        self.pgsane_rank = 10
        self.pgsane_iterations = 10
        self.pgsane_threshold = 2.0
        self.zflist = None
        self.szmlist = None
        self.mp = False
        self.nproc = 4
        self.apex = None
        self.format = None
        self.infile = None
        self.interfile = None
        self.outfile = None
        self.compress_outfile = True
        self.compress_level = 1.0
        self.samplingfile = None
        self.samplingfile_fake = False
        self.tempdir = '/tmp'
        self.largest = LARGESTDATA
        self.freq_f1demodu = 0.0
        if configfile:
            self.load(configfile)

    def from_json(self, jsontxt):
        """updates attributes from json text input"""
        dic = json.loads(jsontxt)
        for k, v in dic.items():
            setattr(self, k, v)

        self.verify()

    def to_json(self):
        """creates a json output of self"""
        out = {}
        for i in dir(self):
            if not i.startswith('_'):
                v = getattr(self, i)
                out[i] = callable(v) or v

        return json.dumps(out)

    def load(self, cp):
        """load from cp config file - should have been opened with ConfigParser() first"""
        if cp.has_option('processing', 'sizemulipliers'):
            raise Exception('Error on the name of sizemultiplier parameter, sizemuliplier instead of sizemultiplier')
        else:
            self.apex = cp.get('import', 'apex')
            self.format = cp.get('import', 'format', default='Solarix')
            self.infile = cp.get('processing', 'infile')
            self.interfile = cp.get('processing', 'interfile', None)
            self.outfile = cp.get('processing', 'outfile')
            self.compress_outfile = cp.getboolean('processing', 'compress_outfile', str(self.compress_outfile))
            self.compress_level = cp.getfloat('processing', 'compress_level', self.compress_level)
            self.tempdir = cp.get('processing', 'tempdir', '.')
            self.samplingfile = cp.get('processing', 'samplingfile')
            self.samplingfile_fake = cp.getboolean('processing', 'samplingfile_fake', str(self.samplingfile_fake))
            self.largest = cp.getint('processing', 'largest_file', 8 * LARGESTDATA)
            self.largest = self.largest // 8
            self.do_modulus = cp.getboolean('processing', 'do_modulus', str(self.do_modulus))
            self.do_f1demodu = cp.getboolean('processing', 'do_f1demodu', str(self.do_f1demodu))
            self.freq_f1demodu = cp.getfloat('processing', 'freq_f1demodu')
            self.do_urqrd = cp.getboolean('processing', 'do_urqrd', str(self.do_urqrd))
            self.urqrd_rank = cp.getint('processing', 'urqrd_rank', self.urqrd_rank)
            self.urqrd_iterations = cp.getint('processing', 'urqrd_iterations', self.urqrd_iterations)
            self.do_sane = cp.getboolean('processing', 'do_sane', str(self.do_sane))
            self.sane_rank = cp.getint('processing', 'sane_rank', self.sane_rank)
            self.sane_iterations = cp.getint('processing', 'sane_iterations', self.sane_iterations)
            self.do_pgsane = cp.getboolean('processing', 'do_pgsane', str(self.do_pgsane))
            self.pgsane_rank = cp.getint('processing', 'pgsane_rank', self.pgsane_rank)
            self.pgsane_iterations = cp.getint('processing', 'pgsane_iterations', self.pgsane_iterations)
            self.pgsane_threshold = cp.getfloat('processing', 'pgsane_threshold', self.pgsane_threshold)
            self.do_rem_ridge = cp.getboolean('processing', 'do_rem_ridge', str(self.do_rem_ridge))
            self.mp = cp.getboolean('processing', 'use_multiprocessing', str(self.mp))
            self.nproc = cp.getint('processing', 'nb_proc', self.nproc)
            self.do_F1 = cp.getboolean('processing', 'do_F1', str(self.do_F1))
            self.do_F2 = cp.getboolean('processing', 'do_F2', str(self.do_F2))
            zflist = cp.get('processing', 'zerofilling', self.zflist)
            if zflist:
                self.zflist = [int(i) for i in zflist.split()]
                self.zflist.sort()
                self.zflist.reverse()
            else:
                self.zflist = None
            szmlist = cp.get('processing', 'sizemultipliers', self.szmlist)
            if szmlist:
                self.szmlist = [float(i) for i in szmlist.split()]
                if debug > 0:
                    print('szmlist:', self.szmlist)
            else:
                self.szmlist = None
        self.verify()

    def verify(self):
        """performs internal coherence of parameters"""
        if not self.do_F1:
            if not self.do_F2:
                raise Exception('no processing !')
            else:
                if self.interfile is None:
                    if self.do_F1:
                        if not self.do_F2:
                            raise Exception('Partial processing, without intermediate file')
                    elif self.do_F1:
                        if self.do_f1demodu and not self.do_modulus:
                            raise Exception('do_f1demodu but not do_modulus is not implemented !')
                else:
                    for f1, f2 in ((self.infile, self.interfile), (self.interfile, self.outfile), (self.infile, self.outfile)):
                        if f1 == f2:
                            raise Exception('input and output files have the same name : %s - this is not possible' % f1)

                    if self.do_sane:
                        if self.do_urqrd:
                            raise Exception('Sane and urQRd are self excluding')
                    if self.samplingfile and self.do_urqrd:
                        raise Exception('urQRd cannot be applied on a NUS data-set')
                if self.samplingfile and self.do_sane:
                    raise Exception('sane cannot be applied on a NUS data-set - use pg_sane')
            if not self.samplingfile:
                if self.do_pgsane:
                    raise Exception('PG_Sane can only be applied on a NUS data-set')
        else:
            if self.zflist != None:
                if self.szmlist != None:
                    raise Exception('Please define only one value : zerofilling or sizes multipliers')
            if self.mp and mpiutil.MPI_size > 1:
                raise Exception('use_multiprocessing is not compatible with MPI')

    def report(self):
        """print a formatted report"""
        print('------------ processing parameters ------------------')
        for i in dir(self):
            if not i.startswith('_'):
                v = getattr(self, i)
                callable(v) or print(i, ' :', v)

        print('-----------------------------------------------------')


class Test(unittest.TestCase):
    __doc__ = 'tests '

    def test_intelli(self):
        """testing 'intelligent' rounding"""
        r = []
        for i in range(16, 33):
            r.append(intelliround(i))

        self.assertEqual(r, [16, 16, 18, 20, 20, 20, 24, 24, 24, 24, 24, 24, 30, 30, 30, 32, 32])

    def test_zf(self):
        """testing zerofilling computation"""
        print(self.test_zf.__doc__)
        d = FTICRData(dim=2)
        d.axis1.size = 1024
        d.axis2.size = 10230
        sizes = comp_sizes(d, zflist=(1, 0, -1))
        if SIZEMIN == 1024:
            self.assertEqual(sizes, [(2048, 20480), (1024, 10240), (1024, 5120), (1024, 1280)])
        sizes = comp_sizes(d, szmlist=(3, 1.5))
        if SIZEMIN == 1024:
            self.assertEqual(sizes, [(3072, 15360), (1024, 3840), (1024, 1920)])

    def test_proc(self):
        """apply a complete processing test"""
        from .Tests import directory
        os.chdir(directory())
        print(os.path.realpath(os.curdir))
        main(['prgm', 'test.mscf'])


def Report_Table_Param():
    print('---------------PyTables/HDF5 SETTINGS---------------------')
    print('| MAX_COLUMNS ', tables.parameters.MAX_COLUMNS)
    print('| MAX_NODE_ATTRS ', tables.parameters.MAX_NODE_ATTRS)
    print('| MAX_GROUP_WIDTH ', tables.parameters.MAX_GROUP_WIDTH)
    print('| MAX_UNDO_PATH_LENGTH ', tables.parameters.MAX_UNDO_PATH_LENGTH)
    print('| CHUNK_CACHE_NELMTS ', tables.parameters.CHUNK_CACHE_NELMTS)
    print('| CHUNK_CACHE_PREEMPT ', tables.parameters.CHUNK_CACHE_PREEMPT)
    print('| CHUNK_CACHE_SIZE ', tables.parameters.CHUNK_CACHE_SIZE)
    print('| METADATA_CACHE_SIZE ', tables.parameters.METADATA_CACHE_SIZE)
    print('| NODE_CACHE_SLOTS ', tables.parameters.NODE_CACHE_SLOTS)
    print('| IO_BUFFER_SIZE ', tables.parameters.IO_BUFFER_SIZE)
    print('| BUFFER_TIMES ', tables.parameters.BUFFER_TIMES)
    print('| EXPECTED_ROWS_EARRAY ', tables.parameters.EXPECTED_ROWS_EARRAY)
    print('| EXPECTED_ROWS_TABLE ', tables.parameters.EXPECTED_ROWS_TABLE)
    print('| PYTABLES_SYS_ATTRS ', tables.parameters.PYTABLES_SYS_ATTRS)
    print('---------------PyTables/HDF5 SETTINGS---------------------')


def Set_Table_Param():
    tables.parameters.CHUNK_CACHE_PREEMPT = 1
    tables.parameters.CHUNK_CACHE_SIZE = 104857600
    tables.parameters.METADATA_CACHE_SIZE = 104857600
    tables.parameters.NODE_CACHE_SLOTS = 104857600


def print_time(t, st='Processing time'):
    """prints processing time, t is in seconds"""
    d = int(t / 86400)
    h = int((t - 86400 * d) / 3600)
    m = int((t - 3600 * (h + 24 * d)) / 60)
    s = int(t - 3600 * (h + 24 * d) - 60 * m)
    if d == 0:
        print(' %s : %dh %02dm %02ds' % (st, h, m, s))
    else:
        print(' %s : %dd %dh %02dm %02ds' % (st, d, h, m, s))


def main(argv=None):
    """
    Does the whole on-file processing, 
    syntax is
    processing.py [ configuration_file.mscf ]
    if no argument is given, the standard file : process.mscf is used.
    """
    global Pool
    import datetime as dt
    print('CONFIG:', os.path.realpath(os.curdir), os.path.exists(sys.argv[1]))
    stdate = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d_%Hh%M')
    logflux = TeeLogger(erase=True, log_name=('processing_%s.log' % stdate))
    print('Processing 2D FT-MS data -', dt.datetime.strftime(dt.datetime.now(), '%Y-%h-%d %Hh%M'))
    print('\n=============================\n    reading configuration\n=============================')
    Pool = None
    t0 = time.time()
    t00 = t0
    if not argv:
        argv = sys.argv
    else:
        try:
            configfile = argv[1]
        except IndexError:
            configfile = 'process.mscf'

        print('using %s as configuration file' % configfile)
        if interfproc:
            output = open('InterfProc/progbar.pkl', 'wb')
            pb = ['F2', 0]
            pickle.dump(pb, output)
            output.close()
        else:
            cp = NPKConfigParser()
            print('address configfile is ', configfile)
            cp.readfp(open(configfile, 'r'))
            print('reading config file')
            param = Proc_Parameters(cp)
            opt_param = {}
            for p in ('F1_specwidth', 'F2_specwidth', 'highmass', 'ref_mass', 'ref_freq'):
                v = cp.getfloat('import', p, 0.0)
                if v != 0.0:
                    opt_param[p] = v

            if param.mp:
                Pool = mp.Pool(param.nproc)
            param.report()
            logflux.log.flush()
            imported = False
            print('\n=============================\n    preparating files\n=============================')
            if not os.path.exists(param.infile):
                print('importing %s into %s' % ('.', param.infile))
                d0 = Import_2D[param.format](param.apex, param.infile)
                imported = True
                if opt_param != {}:
                    d0.hdf5file.close()
                    del d0
                    hf = HDF5File(param.infile, 'rw')
                    for item in opt_param:
                        if item.startswith('F1_'):
                            fileitem = item[3:]
                            hf.axes_update(axis=1, infos={fileitem: opt_param[item]})
                            print('Updating axis F1 %s to %f' % (fileitem, opt_param[item]))
                        elif item.startswith('F2_'):
                            fileitem = item[3:]
                            hf.axes_update(axis=2, infos={fileitem: opt_param[item]})
                            print('Updating axis F2 %s to %f' % (fileitem, opt_param[item]))
                        else:
                            hf.axes_update(axis=1, infos={item: opt_param[item]})
                            hf.axes_update(axis=2, infos={item: opt_param[item]})
                            print('Updating all axes %s to %f' % (item, opt_param[item]))

                    hf.close()
                    d0 = load_input(param.infile)
                else:
                    d0 = load_input(param.infile)
                d0.check2D()
                try:
                    d0.params
                except:
                    d0.params = {}

                if imported:
                    print_time(time.time() - t0, 'Import')
                else:
                    print_time(time.time() - t0, 'Load')
                logflux.log.flush()
                Set_Table_Param()
                if debug > 0:
                    Report_Table_Param()
                    print(d0.report())
                else:
                    allsizes = comp_sizes(d0, zflist=(param.zflist), szmlist=(param.szmlist), largest=(param.largest))
                    if debug > 0:
                        print(allsizes)
                    else:
                        sizeF1, sizeF2 = allsizes.pop(0)
                        if debug > 0:
                            print('preparing intermediate file ')
                        if param.interfile is None:
                            interfile = os.path.join(param.tempdir, 'tmpfile_for_{}'.format(os.path.basename(param.outfile)))
                            print('creating TEMPFILE:', interfile)
                        else:
                            interfile = param.interfile
                    if param.do_F2:
                        temp = HDF5File(interfile, 'w')
                        datatemp = FTICRData(dim=2)
                        copyaxes(d0, datatemp)
                        datatemp.params = d0.params
                        if param.do_modulus:
                            datatemp.axis1.size = min(d0.size1, sizeF1)
                            datatemp.axis2.size = 2 * sizeF2
                        else:
                            datatemp.axis1.size = min(d0.size1, sizeF1)
                            datatemp.axis2.size = sizeF2
                        temp.create_from_template(datatemp)
                    else:
                        datatemp = load_input(param.interfile)
                datatemp.params = d0.params
                logflux.log.flush()
                if debug > 0:
                    print('preparing output file ')
                if param.do_F1:
                    hfar = HDF5File(param.outfile, 'w')
                    d1 = FTICRData(dim=2)
                    copyaxes(d0, d1)
                    d1.axis2.size = sizeF2
                    d1.axis1.size = sizeF1
                    group = 'resol1'
                    if param.compress_outfile:
                        hfar.set_compression(True)
                    hfar.create_from_template(d1, group)
                    d1.params = d0.params
                    if debug > 0:
                        print('######################### d1.report() ################')
                        print(d1.report())
                        print('######################### Checked ################')
            else:
                d1 = None
    logflux.log.flush()
    print('\n=============================\n    FT processing\n=============================')
    t0 = time.time()
    do_process2D(d0, datatemp, d1, param)
    datatemp.hdf5file.close()
    if param.do_F1:
        hfar.axes_update(group=group, axis=1, infos={'offsetfreq': d1.axis1.offsetfreq})
    if param.interfile is None:
        temp.close()
        os.unlink(interfile)
    print('==  FT Processing finished  ==')
    print_time(time.time() - t0, 'FT processing time')
    logflux.log.flush()
    if param.do_F1:
        print('\n=============================\n    downsampling\n=============================')
        downprevious = d1
        t0 = time.time()
        for i, (sizeF1, sizeF2) in enumerate(allsizes):
            if not downprevious.size1 % sizeF1 != 0:
                if downprevious.size2 % sizeF2 != 0:
                    print('downsampling not available for level %d : %d x %d -> %d x %d' % (i + 1, downprevious.size1, downprevious.size2, sizeF1, sizeF2))
                    continue
                zflevel = 'level %d' % (i + 1)
                group = 'resol%d' % (i + 2)
                print('downsampling %s - %s  (%d x %d)' % (zflevel, group, sizeF1, sizeF2))
                down = FTICRData(dim=2)
                copyaxes(d1, down)
                down.axis1.size = sizeF1
                down.axis2.size = sizeF2
                hfar.create_from_template(down, group)
                if debug > 0:
                    print(down)
                downsample2D(downprevious, down, (downprevious.size1 // sizeF1), (downprevious.size2 // sizeF2), compress=(param.compress_outfile))
                downprevious = down

        print_time(time.time() - t0, 'Downsampling time')
    print('== Processing finished  ==')
    print_time(time.time() - t00, 'Total processing time')
    logflux.log.flush()
    print('\n=============================\n    cleaning and closing\n=============================')
    hfar.store_internal_file(filename=configfile, h5name='config.mscf', where='/attached')
    try:
        hfar.store_internal_object(h5name='params', obj=d0.hdf5file.retrieve_object(h5name='params'))
    except:
        print('No params copied to Output file')

    print('parameters and configuration file copied')
    for h5name in ('apexAcquisition.method', 'ExciteSweep'):
        try:
            Finh5 = d0.hdf5file.open_internal_file(h5name)
        except:
            print('no %s internal file to copy' % h5name)
        else:
            Fouth5 = hfar.open_internal_file(h5name, access='w')
            Fouth5.write(Finh5.read())
            Finh5.close()
            Fouth5.close()
            print('%s internal file copied' % h5name)

    logflux.log.flush()
    hfar.store_internal_file(filename=(logflux.log_name), h5name='processing.log', where='/attached')
    print('log file copied')
    d0.hdf5file.close()
    hfar.close()
    if param.mp:
        Pool.close()
    logflux.log.flush()


if __name__ == '__main__':
    mp.freeze_support()
    if mpiutil.MPI_size < 2:
        main()
    else:
        if mpiutil.MPI_rank == 0:
            main()
            mpiutil.shutdown()
        else:
            mpiutil.slave()