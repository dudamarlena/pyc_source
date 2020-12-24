# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/Cadzow_mpi2.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 7772 bytes
"""
Created by Marc-André Delsuc and Lionel Chiron on 2011-07
Copyright (c) 2010 IGBMC. All rights reserved.

Cadzow in MPI mode
complete rewrite from the code from Cyrille Bonamy for the MPI part

code compatible avec la version 0.4.0 de NPK

Thresholding to make Cadzow on the main relevant columns.

note that the cadzow algo is multithreaded if running over the MKL library.
So if MKL is installed, run only on instance per node, as all cores from the node will be solicited.
"""
from __future__ import print_function
import sys, numpy as np
import util.mpiutil as mpiutil
import util.progressbar as pg
import tables, time, urQRd, Cadzow
from spike.NPKData import NPKData, copyaxes
from spike.FTICR import FTICRData
import spike.File.HDF5File as HDF5File
import spike.NPKConfigParser as NPKConfigParser
debug = False

def Set_Table_Param():
    tables.parameters.CHUNK_CACHE_PREEMPT = 1
    tables.parameters.CHUNK_CACHE_SIZE = 104857600
    tables.parameters.METADATA_CACHE_SIZE = 104857600
    tables.parameters.NODE_CACHE_SLOTS = 104857600


def selectcol(data, limitpts, nbrows=200):
    """
    returns a list of index of the limitpts largest columns of the 2D 'data'
    
    first averaging on nbrows rows
    
    return index list
    """
    if debug:
        print('averaging on ', nbrows, ' rows ')
    else:
        roughft2 = data.row(0)
        if roughft2.axis1.itype == 1:
            roughft2.modulus()
        else:
            roughft2.abs()
    for i in range(min(nbrows, data.size1)):
        rr = data.row(i)
        if rr.axis1.itype == 1:
            rr.modulus()
        else:
            rr.abs()
        roughft2.add(rr)

    roughft2.mult(1.0 / nbrows)
    n = roughft2.size1 * 0.1
    roughft2.buffer[0:n] = 0.0
    index = find_thres(roughft2, limitpts=limitpts)
    if debug:
        roughft2.display()
        disp = NPKData(buffer=(np.zeros(roughft2.size1)))
        disp.buffer[index] = roughft2.buffer[index]
        disp.display(show=True)
    return index


def find_thres(b, limitpts):
    """
    returns a list of index of the limitpts largest points in the 1D data 'b' 
    """
    thresh = max(b.buffer) + 1.0
    nbpts = 0
    count = 0
    inter = b.buffer.copy()
    while abs(nbpts - limitpts) / float(limitpts) > 0.1:
        if debug:
            print('thresh : ', thresh)
        else:
            nbpts = (inter > thresh).sum()
            inter[inter < thresh] = 0
            if debug:
                print('nbpts', nbpts, 'count ', count)
            count += 1
            if nbpts < limitpts:
                c = inter
                threshold = thresh
                if debug:
                    print('threshold ', threshold)
                thresh /= 2.0
                ind = np.where(c > 0)[0]
            else:
                if debug:
                    print('treshold min = ', thresh)
                thresh = (threshold + thresh) / 2.0
                if debug:
                    print('nouveau threshold ', thresh)
        inter = np.copy(b.buffer)
        if debug:
            print('au dessus thresh ', (inter > thresh).sum())
        if debug:
            print('=0 ', (inter == 0).sum())

    return ind


def load_input(name):
    """load input file and returns it, in read-only mode"""
    if debug > 0:
        print('reading', name)
    hf = HDF5File(name, 'r')
    d0 = hf.load()
    return d0


def iterarg(xindex, dinp, n_of_line, n_of_iter, orda):
    """an iterator used by the MPI set-up"""
    for i in xindex:
        c0 = dinp.col(i)
        if debug:
            print(c0.buffer, n_of_line, n_of_iter, orda)
        yield (
         c0.buffer, n_of_line, n_of_iter, orda)


def cadz(args):
    """utility function"""
    if debug:
        print(args)
    return (Cadzow.cadzow)(*args)


def rqr(args):
    """utility function"""
    if debug:
        print(args)
    argu = (
     args[0], args[1], args[3])
    return (urQRd.urQRd)(*argu)


def main():
    """does the whole job,
    if we are running in MPI, this is only called by job #0
    all other jobs are running mpi.slave()
    """
    argv = sys.argv
    if len(argv) != 2:
        print('\nsyntax is :\n(mpirun -np N) python  program   configfile.mscf\n')
        sys.exit(1)
    else:
        configfile = argv[1]
        cp = NPKConfigParser()
        cp.readfp(open(configfile))
        infile = cp.getword('Cadzow', 'namein')
        print('infile', infile)
        outfile = cp.getword('Cadzow', 'nameout')
        print('outfile', outfile)
        algo = cp.getword('Cadzow', 'algorithm')
        print('algorithm', algo)
        n_of_line = cp.getint('Cadzow', 'n_of_lines', 70)
        print('n_of_line', n_of_line)
        n_of_iter = cp.getint('Cadzow', 'n_of_iters', 1)
        print('n_of_iter', n_of_iter)
        orda = cp.getint('Cadzow', 'order', 500)
        print('order', orda)
        n_of_column = cp.getint('Cadzow', 'n_of_column', 100)
        print('n_of_column', n_of_column)
        progress = cp.getboolean('Cadzow', 'progress', True)
        d0 = load_input(infile)
        d0.check2D()
        Set_Table_Param()
        hfar = HDF5File(outfile, 'w', debug=0)
        d1 = FTICRData(dim=2)
        copyaxes(d0, d1)
        group = 'resol1'
        hfar.create_from_template(d1, group)
        if n_of_column == 0:
            indexes = range(d0.size2)
        else:
            indexes = selectcol(d0, n_of_column)
        if algo == 'Cadzow':
            meth = cadz
        else:
            if algo == 'rQRd':
                meth = rqr
            else:
                raise 'wrong algo'
    t0 = time.time()
    if progress:
        widgets = [
         'Processing %s: ' % algo, pg.Percentage(), ' ', pg.Bar(marker='-', left='[', right=']'), pg.ETA()]
        pbar = pg.ProgressBar(widgets=widgets, maxval=(len(indexes)))
    d1D = d0.col(0)
    xarg = iterarg(indexes, d0, n_of_line, n_of_iter, orda)
    if mpiutil.MPI_size > 1:
        mpiutil.mprint('MPI Master job  - starting slave jobs - ')
        res = mpiutil.enum_imap(meth, xarg)
        for i, p in res:
            d1D.buffer = p
            d1.set_col(indexes[i], d1D)
            if progress:
                pbar.update(i + 1)

    else:
        import itertools
        res = itertools.imap(meth, xarg)
        for i, p in enumerate(res):
            d1D.buffer = p
            d1.set_col(indexes[i], d1D)
            if progress:
                pbar.update(i + 1)

    print('Processing time : ', time.time() - t0)


if __name__ == '__main__':
    if mpiutil.MPI_size < 2:
        print('Running in single processor mode')
        main()
    else:
        print('Running in MPI mode')
        if mpiutil.MPI_rank == 0:
            main()
        else:
            mpiutil.slave()