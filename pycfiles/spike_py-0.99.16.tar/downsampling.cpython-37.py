# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Miscellaneous/downsampling.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 26285 bytes
"""
Processing.py

This program realises the processing of an FTICR data

Created by Marc-André on 2011-09-23.
Copyright (c) 2011 IGBMC. All rights reserved.
"""
from __future__ import print_function
import sys, os, unittest, time
from scipy.signal import decimate, lfilter, cheby1, medfilt, medfilt2d
import spike.NPKConfigParser as NPKConfigParser
from spike.FTICR import *
from spike.File.Apex import Import_2D
from spike.NPKData import copyaxes
from spike.HDF5File import HDF5File, determine_chunkshape
import spike.Algo.urQRd as urQRd
from numpy import fft
debug = 1
import tables
import util.progressbar as pg
import util.mpiutil as mpiutil
LARGESTDATA = 8589934592
SIZEMIN = 1024

def pred_sizes(d0, zf=0, sizemin=SIZEMIN):
    """
    given an input data set, determines the optimum size s1,s2 to process it with a zerofilling of zf
    zf = +n is doubling n times along each axis
    zf = -n is halving n times along each axis
    zf = 0 is no zerofiling
    however, axes can never get smaller than sizemin
    returns (si1, si2, ...) as the dataset dimension
    """

    def dopow2(s, zf, sizemin):
        """do the math"""
        sm = min(sizemin, s)
        s1 = s * pow(2, zf)
        s = max(sm, s1)
        return int(s)

    r = []
    for i in range(d0.dim):
        r.append(dopow2(d0.axes(i + 1).size, zf, sizemin))

    if debug > 0:
        print(r, reduce(lambda x, y: x * y, r) / 1024 / 1024, 'Mpoint')
    return tuple(r)


def comp_sizespow2(d0, zflist, largest=LARGESTDATA, sizemin=SIZEMIN, vignette=True):
    """
    apply pred_sizes to all zerofiling values in zflist, and return a list with unique values
    largest determines the largest dataset allowed
    sizemini determines the minimum size when downzerofilling
    when vignette == True (default) a minimum size data (defined by sizemini) is appended to the list
    """
    sizes = []
    for zf in zflist:
        sz = pred_sizes(d0, zf)
        si1, si2 = sz
        while si1 * si2 > largest:
            si2 /= 2
            print('Warning, reducing SI2 to %s' % si2)

        sz = (
         si1, si2)
        if sz not in sizes:
            sizes.append(sz)

    if vignette:
        sz = (
         sizemin, sizemin)
        if sz not in sizes:
            sizes.append(sz)
    return sizes


def nearfactor(num, thresh):
    """
    find the product of prime factors of num the nearest from thresh 
    """

    def primefactors(x):
        """
        decomposition in prime factors
        """
        factorlist = []
        loop = 2
        while loop <= x:
            if x % loop == 0:
                x /= loop
                factorlist.append(loop)
            else:
                loop += 1

        return factorlist

    lprime = primefactors(num)
    div = 1
    for i in lprime[::-1]:
        div *= i
        if num / div != 0:
            if div <= thresh:
                continue
        div /= i

    return div


def comp_sizes(d0, zflist, largest=LARGESTDATA, sizemin=SIZEMIN, vignette=True):
    """
    apply pred_sizes to all zerofiling values in zflist, and return a list with unique values
    largest determines the largest dataset allowed
    sizemini determines the minimum size when downzerofilling
    when vignette == True (default) a minimum size data (defined by sizemini) is appended to the list
    """
    sizes = []
    for zf in zflist:
        sz = (
         d0.axes(1).size, d0.axes(2).size)
        si1, si2 = sz
        while si1 * si2 > largest:
            si2 /= 2
            print('Warning, reducing SI2 to %s' % si2)

        sz = (
         si1, si2)
        if sz not in sizes:
            sizes.append(sz)

    if vignette:
        print('############################')
        print('nearfactor(d0.axes(1).size,sizemin)', nearfactor(d0.axes(1).size, sizemin))
        sz = (nearfactor(d0.axes(1).size, sizemin), nearfactor(d0.axes(2).size, sizemin))
        if sz not in sizes:
            sizes.append(sz)
    return sizes


def apod(d, size):
    """apply sin 0.5 apodisation and change size"""
    if d.size1 < size:
        d.apod_sin(maxi=0.5)
        d.chsize(size)
    else:
        if d.size1 > size:
            d.chsize(size)
            d.apod_sin(maxi=0.5)
        else:
            d.apod_sin(maxi=0.5)
    return d


def do_proc_F2(dinp, doutp):
    """scan all rows of dinp, apply proc() and store into doutp"""
    size = doutp.axis2.size
    scan = dinp.size1
    widgets = ['Processing F2: ', pg.Percentage(), ' ', pg.Bar(marker='-', left='[', right=']'), pg.ETA()]
    pbar = pg.ProgressBar(widgets=widgets, maxval=scan)
    print('dinp.axis1.itype ', dinp.axis1.itype)
    print('dinp.axis2.itype ', dinp.axis2.itype)
    print('doutp.axis1.itype ', doutp.axis1.itype)
    print('doutp.axis2.itype ', doutp.axis2.itype)
    print('dinp.axis1.size ', dinp.axis1.size)
    print('dinp.axis2.size ', dinp.axis2.size)
    print('doutp.axis1.size ', doutp.axis1.size)
    print('doutp.axis2.size ', doutp.axis2.size)
    print(doutp.report())
    print(dir(doutp))
    for i in xrange(scan):
        r = dinp.row(i)
        apod(r, size)
        r.rfft()
        doutp.set_row(i, r)
        pbar.update(i + 1)

    pbar.finish()


def do_proc_F1(dinp, doutp):
    """scan all cols of dinp, apply proc() and store into doutp"""
    size = doutp.axis1.size
    scan = min(dinp.size2, doutp.size2)
    widgets = ['Processing F1: ', pg.Percentage(), ' ', pg.Bar(marker='-', left='[', right=']'), pg.ETA()]
    pbar = pg.ProgressBar(widgets=widgets, maxval=scan)
    for i in xrange(scan):
        c = dinp.col(i)
        apod(c, size)
        c.rfft()
        doutp.set_col(i, c)
        pbar.update(i)

    pbar.finish()


def do_proc_F1_modu(dinp, doutp):
    """as do_proc_F1, but applies hypercomplex modulus() at the end"""
    size = 2 * doutp.axis1.size
    scan = doutp.size2
    widgets = [
     'Processing F1 modu: ', pg.Percentage(), ' ', pg.Bar(marker='-', left='[', right=']'), pg.ETA()]
    pbar = pg.ProgressBar(widgets=widgets, maxval=scan)
    for i in xrange(scan):
        d = FTICRData(buffer=(np.zeros((2 * doutp.size1, 2))))
        for off in (0, 1):
            p = dinp.col(2 * i + off)
            apod(p, size)
            p.rfft()
            d.set_col(off, p)

        d.axis1.itype = 1
        d.axis2.itype = 1
        d.modulus()
        doutp.set_col(i, d.col(0))
        pbar.update(i + 1)

    pbar.finish()


def _do_proc_F1_flip_modu(data):
    """given a pair of columns, return the processed fliped FTed modulused column"""
    import math as m
    c0, c1, shift, size, do_rqrd, rqrd_rank = data
    d = FTICRData(buffer=(np.zeros((c0.size1, 2))))
    d.set_col(0, c0)
    d.set_col(1, c1)
    d.axis1.itype = 0
    d.axis2.itype = 1
    d.f1demodu(shift)
    pbuf = d.col(0).buffer
    if do_rqrd:
        pbuf = urQRd(pbuf, rqrd_rank)
    p = FTICRData(buffer=pbuf)
    apod(p, size)
    p.rfft()
    p.modulus()
    return p


def iterarg(dinp, rot, size, do_rqrd, rqrd_rank):
    """an iterator used by the MPI set-up"""
    for i in range(0, dinp.size2, 2):
        c0 = dinp.col(i)
        c1 = dinp.col(i + 1)
        yield (
         c0, c1, rot, size, do_rqrd, rqrd_rank)


def do_proc_F1_flip_modu(dinp, doutp, parameter, nproc=None):
    """as do_proc_F1, but applies flip and then complex modulus() at the end"""
    size = 2 * doutp.axis1.size
    scan = min(dinp.size2, doutp.size2)
    widgets = [
     'Processing F1 flip-modu: ', pg.Percentage(), ' ', pg.Bar(marker='-', left='[', right=']'), pg.ETA()]
    pbar = pg.ProgressBar(widgets=widgets, maxval=scan)
    shift = doutp.axis1.mztoi(doutp.axis1.highmass)
    hshift = doutp.axis1.itoh(shift)
    rot = dinp.axis1.mztoi(dinp.axis1.highmass)
    print('LEFT_POINT', shift)
    doutp.axis1.left_point = shift
    doutp.axis1.specwidth += hshift
    if mpiutil.MPI_size > 1:
        nproc = 0
    elif nproc == None:
        print('doutp.axis1.itype ', doutp.axis1.itype)
        d = FTICRData(buffer=(np.zeros((dinp.size1, 2))))
        for i in xrange(scan):
            for off in (0, 1):
                p = dinp.col(2 * i + off)
                d.set_col(off, p)

            d.axis1.itype = 0
            d.axis2.itype = 1
            d.f1demodu(rot)
            p = d.col(0)
            apod(p, size)
            if parameter.do_rqrd:
                p.buffer = urQRd(p.buffer, parameter.rqrd_rank)
            p.rfft()
            p.modulus()
            doutp.set_col(i, p)
            pbar.update(i + 1)

    else:
        if nproc > 1:
            import multiprocessing as mp
            xarg = iterarg(dinp, rot, size, parameter.do_rqrd, parameter.rqrd_rank)
            pool = mp.Pool(nproc)
            res = pool.map(_do_proc_F1_flip_modu, xarg)
            for i, p in enumerate(res):
                doutp.set_col(i, p)
                pbar.update(i + 1)

        else:
            if nproc == 0:
                mpiutil.mprint('MPI NEW STYLE')
                xarg = iterarg(dinp, rot, size, parameter.do_rqrd, parameter.rqrd_rank)
                res = mpiutil.enum_imap(_do_proc_F1_flip_modu, xarg)
                for i, p in res:
                    doutp.set_col(i, p)
                    pbar.update(i + 1)

            else:
                raise Exception('We have an internal problem n.1 here !')
    pbar.finish()


def do_process2D(dinp, datatemp, doutp, parameter, nproc=None):
    """
    apply the processing to an input 2D data set : dinp
    result is found in an output file : doutp
    
    dinter and doutp should have been created before, size of doutp will determine the processing
    will use a temporay file if needed
    """
    if debug > 0:
        for f, d in ((parameter.infile, dinp), (parameter.interfile, datatemp), (parameter.outfile, doutp)):
            print('----------', f)
            print(d)

    else:
        if parameter.do_F2:
            do_proc_F2(dinp, datatemp)
        elif parameter.do_F1:
            if parameter.do_f1demodu and parameter.do_modulus:
                do_proc_F1_flip_modu(datatemp, doutp, parameter, nproc=nproc)
            else:
                if parameter.do_modulus:
                    do_proc_F1_modu(datatemp, doutp)
                else:
                    do_proc_F1(datatemp, doutp)
        if parameter.do_F1 and parameter.do_rem_ridge:
            from rem_ridge import rem_ridge
            rem_ridge(doutp)


def downsample2D(data, outp, n1, n2):
    """
    takes data (a 2D) and generate a smaller dataset downsampled by factor (n1,n2) on each axis
    then returned data-set is n1*n2 times smaller
    - simply takes the mean
    
    ** Not tested on non powers of 2 **
    
    """
    print('downsampling')
    print('data.row(0).buffer ', data.row(0).buffer)
    print(data.report())
    ooo
    for i in xrange(0, data.size1, n1):
        temp = np.zeros(data.size2 / n2)
        for j in xrange(n1):
            yy = decimate((data.row(i + j).buffer), n2, ftype='fir')
            print('data.row(i+j).buffer ', data.row(i + j).buffer)
            print('yy ', yy)
            temp += yy

        outp.buffer[i / n1, :] = 1.0 / n1 * temp
        print('########## outp.buffer[i/n1,:] ', outp.buffer[i / n1, :])

    copyaxes(data, outp)
    outp.axis1.left_point = outp.axis1.left_point / n1
    outp.axis2.left_point = outp.axis2.left_point / n2
    outp.adapt_size()
    return outp


def load_input(name):
    """load input file and returns it, in read-only mode"""
    if debug > 0:
        print('reading', name)
    hf = HDF5File(name, 'r')
    d0 = hf.load()
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
        self.do_rqrd = False
        self.rqrd_rank = 10
        self.zflist = [0]
        self.apex = None
        self.infile = None
        self.interfile = None
        self.outfile = None
        self.tempdir = '/tmp'
        self.largest = LARGESTDATA
        if configfile:
            self.load(configfile)

    def load(self, cp):
        """load from cp config file - should have been opened with ConfigParser() first"""
        self.apex = cp.get('import', 'apex')
        self.infile = cp.get('processing', 'infile')
        self.interfile = cp.get('processing', 'interfile', None)
        self.outfile = cp.get('processing', 'outfile')
        self.tempdir = cp.get('processing', 'tempdir', '.')
        self.largest = cp.getint('processing', 'largest', LARGESTDATA)
        self.do_modulus = cp.getboolean('processing', 'do_modulus', str(self.do_modulus))
        self.do_f1demodu = cp.getboolean('processing', 'do_f1demodu', str(self.do_f1demodu))
        self.do_rqrd = cp.getboolean('processing', 'do_rqrd', str(self.do_rqrd))
        self.rqrd_rank = cp.getint('processing', 'rqrd_rank', str(self.rqrd_rank))
        self.do_rem_ridge = cp.getboolean('processing', 'do_rem_ridge', str(self.do_rem_ridge))
        self.do_F1 = cp.getboolean('processing', 'do_F1', str(self.do_F1))
        self.do_F2 = cp.getboolean('processing', 'do_F2', str(self.do_F2))
        zflist = cp.get('processing', 'zerofilling', '0 -2 -4')
        self.zflist = [int(i) for i in zflist.split()]
        self.zflist.sort()
        self.zflist.reverse()
        if not (self.do_F1 or self.do_F2):
            raise Exception('no processing !')
        if self.interfile is None:
            raise self.do_F1 and self.do_F2 or Exception('Partial processing, without intermediate file')
        if self.do_F1:
            if self.do_f1demodu and not self.do_modulus:
                raise Exception('do_f1demodu but not do_modulus is not implemented !')
        for f1, f2 in ((self.infile, self.interfile), (self.interfile, self.outfile), (self.infile, self.outfile)):
            if f1 == f2:
                raise Exception('input and output files have the same name : %s - this is not possible' % f1)

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

    def test_zf(self):
        """testing zerofilling computation"""
        print(self.test_zf.__doc__)
        d = FTICRData(dim=2)
        d.axis1.size = 1024
        d.axis2.size = 16384
        sizes = comp_sizes(d, (1, 0, -1))
        self.assertEqual(sizes, [(2048, 32768), (1024, 16384), (512, 8192), (512, 512)])

    def test_proc(self):
        """apply a complete processing test"""
        main(['prgm', 'test.mscf'])


def Report_Table_Param():
    print('---------------SETTINGS---------------------')
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
    print('| MAX_THREADS ', tables.parameters.MAX_THREADS)
    print('---------------SETTINGS---------------------')


def Set_Table_Param():
    tables.parameters.CHUNK_CACHE_PREEMPT = 1
    tables.parameters.CHUNK_CACHE_SIZE = 104857600
    tables.parameters.METADATA_CACHE_SIZE = 104857600
    tables.parameters.NODE_CACHE_SLOTS = 104857600


def print_time(t, st='Processing time'):
    """prints processing time"""
    h = int(t / 3600)
    m = int((t - 3600 * h) / 60)
    s = int(t - 3600 * h - 60 * m)
    print(' %s : %d:%02d:%02d' % (st, h, m, s))


def main(argv=None):
    """
    Does the whole on-file processing, 
    
    syntax is
    processing.py [ configuration_file.mscf ]
    if no argument is given, the standard file : process.mscf is used.
    
    """
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
        cp = NPKConfigParser()
        cp.readfp(open(configfile))
        print('reading config file')
        param = Proc_Parameters(cp)
        param.report()
        opt_param = {}
        for p in ('F1_specwidth', 'F2_specwidth', 'highmass'):
            v = cp.getfloat('import', p, 0.0)
            if v != 0.0:
                opt_param[p] = v

        imported = False
        if not os.path.exists(param.infile):
            print('importing %s into %s' % (dir, param.infile))
            d0 = Import_2D(param.apex, param.infile)
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
                        fileitem = item[3:]
                        hf.axes_update(axis=1, infos={item: opt_param[item]})
                        hf.axes_update(axis=2, infos={item: opt_param[item]})
                        print('Updating all axes %s to %f' % (item, opt_param[item]))

                hf.close()
                d0 = load_input(param.infile)
            else:
                d0 = load_input(param.infile)
            d0.check2D()
            if imported:
                print_time(time.time() - t0, 'Import')
            else:
                print_time(time.time() - t0, 'Load')
            Set_Table_Param()
            if debug > 0:
                Report_Table_Param()
                print(d0.report())
            else:
                allsizes = comp_sizes(d0, (param.zflist), largest=(param.largest))
                print('allsizes ', allsizes)
                if debug > 0:
                    print(allsizes)
                else:
                    sizeF1, sizeF2 = allsizes.pop(0)
                    if param.interfile is None:
                        interfile = os.path.join(param.tempdir, 'tmpfile.msh5')
                        print('creating TEMPFILE:', interfile)
                    else:
                        interfile = param.interfile
                if param.do_F2:
                    temp = HDF5File(interfile, 'w')
                    datatemp = FTICRData(dim=2)
                    copyaxes(d0, datatemp)
                    if param.do_modulus:
                        datatemp.axis1.size = min(d0.size1, sizeF1)
                        datatemp.axis2.size = 2 * sizeF2
                    else:
                        datatemp.axis1.size = min(d0.size1, sizeF1)
                        datatemp.axis2.size = sizeF2
                    temp.create_from_template(datatemp)
                else:
                    datatemp = load_input(param.interfile)
            if param.do_F1:
                hfar = HDF5File((param.outfile), 'w', debug=1)
                d1 = FTICRData(dim=2)
                copyaxes(d0, d1)
                d1.axis2.size = sizeF2
                d1.axis1.size = sizeF1
                group = 'resol1'
                hfar.create_from_template(d1, group)
        else:
            d1 = None
    print('\n=============================\nprocessing FT\n=============================')
    t0 = time.time()
    if param.do_F1:
        hfar.axes_update(group=group, axis=1, infos={'specwidth':d1.axis1.specwidth,  'left_point':int(d1.axis1.left_point)})
    if param.interfile is None:
        temp.close()
        os.unlink(interfile)
    print('==  FT Processing finished  ==')
    print_time(time.time() - t0, 'FT processing time')
    if param.do_F1:
        down = None
        t0 = time.time()
        for i, (sizeF1, sizeF2) in enumerate(allsizes):
            print('d1.size1,sizeF1 ', d1.size1, sizeF1)
            print('d1.size2,sizeF2 ', d1.size2, sizeF2)
            if not d1.size1 % sizeF1 != 0:
                if d1.size2 % sizeF2 != 0:
                    print('downsampling not available for level %d : %d x %d -> %d x %d' % (param.zflist[(i + 1)], d1.size1, d1.size2, sizeF1, sizeF2))
                    break
                try:
                    zflevel = 'level %d' % param.zflist[(i + 1)]
                except IndexError:
                    zflevel = 'vignette'

                print('\n================\ndownsampling %s\n================' % zflevel)
                group = 'resol%d' % (i + 2)
                if debug > 1:
                    print('downsampling', group, (sizeF1, sizeF2))
                down = FTICRData(dim=2)
                copyaxes(d1, down)
                down.axis1.size = sizeF1
                down.axis2.size = sizeF2
                hfar.create_from_template(down, group)
                if debug > 0:
                    print(down)
                downsample2D(d1, down, d1.size1 / sizeF1, d1.size2 / sizeF2)
                hfar.axes_update(group=group, axis=1, infos={'left_point': down.axis1.left_point})

        print_time(time.time() - t0, 'Downsampling time')
    print('== Processing finished  ==')
    print_time(time.time() - t00, 'Total processing time')


if __name__ == '__main__':
    if mpiutil.MPI_size < 2:
        main()
    else:
        if mpiutil.MPI_rank == 0:
            main()
        else:
            mpiutil.slave()