# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/Cadzow_mpi.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 9897 bytes
"""
Created by Marc-André Delsuc and Lionel Chiron on 2011-07

Cadzow en mode MPI
code de Cyrille Bonamy pour la partie MPI

code compatible avec la version 0.3.4 de NPK

Thresholding to make Cadzow on the main relevant columns. 

note that the cadzow algo is multithreaded if running over the MKL library.
So if MKL is installed, run only on instance per node, as all cores from the node will be solicited.
"""
from __future__ import print_function
import Cadzow
import spike.NPKData as NPKData
import sys, os, numpy as np
from mpi4py import MPI
import time, urQRd
debug = False

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


def cadzow2dl(d2D, index, n_of_line=5, n_of_iter=5, orda=100):
    """
    applies the cadzow procedure to all columns of the 2D listed in index
    """
    d2D.check2D()
    d1D = d2D.col(0)
    t0 = time.time()
    if debug:
        print('d2D.size2 ', d2D.size2)
    for i in xrange(d2D.size2):
        if i in index:
            print('processing column %d / %d' % (i, d2D.size2))
            d1D = d2D.col(i)
            corr = Cadzow.cadzow((d1D.buffer), n_of_line=n_of_line, n_of_iter=n_of_iter, orda=orda)
            d1D.buffer = corr
            d2D.set_col(i, d1D)
            if debug:
                print('column n ', i, 'cadzowed ', time.time() - t0)
            elif debug:
                if i % 1000 == 0:
                    print('skip', i, time.time() - t0)
        else:
            d1D.fill(0.0)
            d2D.set_col(i, d1D)


def cadzow2dp(d2D, p, N, n_of_line=5, n_of_iter=5, orda=100):
    """
    applies the cadzow procedure to all columns of the 2D
    like cadzow, but makes the  pth task of a calculus in N processes
    """
    d2D.check2D()
    d1D = d2D.col(0)
    if debug:
        print('type(d1D.buffer)', type(d1D.buffer))
    for i in xrange(d2D.size2):
        if i % N == p:
            print('processing column %d / %d' % (i + 1, d2D.size2), p, N)
            d1D = d2D.col(i)
            corr = Cadzow.cadzow(d1D.buffer, n_of_line, n_of_iter, orda)
            d1D.buffer = corr
            d2D.set_col(i, d1D)
        else:
            d1D.fill(0.0)
            d2D.set_col(i, d1D)


def mpirQRd(d2D, p, N, n_of_line=5, k=10, n_of_iter=5, orda=100):
    """
    applies the cadzow procedure to all columns of the 2D
    like cadzow, but makes the  pth task of a calculus in N processes
    """
    d2D.check2D()
    d1D = d2D.col(0)
    if debug:
        print('type(d1D.buffer)', type(d1D.buffer))
    for i in xrange(d2D.size2):
        if i % N == p:
            print('processing column %d / %d' % (i + 1, d2D.size2), p, N)
            d1D = d2D.col(i)
            corr = urQRd.urQRd(fid=(d1D.buffer), k=k, n_of_iter=n_of_iter, orda=orda)
            d1D.buffer = corr
            d2D.set_col(i, d1D)
        else:
            d1D.fill(0.0)
            d2D.set_col(i, d1D)


def main():
    """does the job"""

    def message():
        print('il faut choisir   start  ou  start_MPI  ou  start_MPI_thresh ou run p  ou  collect  ou start_rand')
        sys.exit(1)

    argv = sys.argv
    if len(argv) < 2:
        message()
    else:
        N_proc = MPI.COMM_WORLD.Get_size()
        print('Running on', N_proc, 'processes')
        if argv[1] == 'start_MPI':
            rank = MPI.COMM_WORLD.Get_rank()
            p = int(rank)
            print('run #', p)
            donnees = NPKData(name=namein)
            cadzow2dp(donnees, p, N_proc, n_of_line, n_of_iter, orda)
            donnees.save(nameout % p)
        else:
            if argv[1] == 'start_rQR':
                rank = MPI.COMM_WORLD.Get_rank()
                p = int(rank)
                print('run #', p)
                donnees = NPKData(name=namein)
                mpirQRd(donnees, p, N_proc, n_of_line, k, n_of_iter, orda)
                donnees.save(nameout % p)
            else:
                if argv[1] == 'start_MPI_thresh':
                    rank = MPI.COMM_WORLD.Get_rank()
                    p = int(rank)
                    print('run #', p)
                    donnees = NPKData(name=namein)
                    index = selectcol(donnees, n_of_columns)
                    indexp = [ind for ind in index if ind % N_proc == p]
                    cadzow2dl(donnees, indexp, n_of_line=n_of_line, n_of_iter=n_of_iter, orda=orda)
                    donnees.save(nameout % p)
                    print('processing finished for bog #', p)
                else:
                    if argv[1] == 'run':
                        p = int(argv[2])
                        print('run #', p)
                        donnees = NPKData(name=namein)
                        cadzow2dp(donnees, p, N_proc, n_of_line, n_of_iter, orda)
                        donnees.save(nameout % p)
                    else:
                        if argv[1] == 'collect':
                            N_proc = int(argv[2])
                            print(nameout % 0)
                            donnees = NPKData(name=(nameout % 0))
                            for p in range(1, N_proc):
                                print(nameout % p)
                                d = NPKData(name=(nameout % p))
                                donnees.add(d)

                            ff = nameout % N_proc
                            donnees.save(ff)
                            print('le fichier final est dans %s' % ff)
                        else:
                            message()
    sys.exit()


namein = '/Echange/data_FT_F2.gf2'
nameout = '/Echange/data_FT_F2_CADZOW-%d.gf2'
n_of_line = 70
n_of_iter = 3
k = 50
orda = 500
n_of_columns = 100
main()