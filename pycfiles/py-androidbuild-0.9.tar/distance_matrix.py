# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/tools/distance_matrix.py
# Compiled at: 2016-03-23 12:35:00
import threading, datetime, numpy as np, Queue
rt = 6378.137
verbose = 0

class ThreadClass(threading.Thread):

    def __init__(self, input_q, indices_q, result_q, alat, alon, blat, blon):
        threading.Thread.__init__(self)
        self.input = input_q
        self.indices = indices_q
        self.result = result_q
        self.alat = alat
        self.alon = alon
        self.blat = blat
        self.blon = blon
        del alat
        del alon
        del blat
        del blon
        self.na = len(self.alon)
        self.nb = len(self.blon)

    def task(self):
        input = self.input.get()
        index = input[1]
        id = input[0]
        if verbose > 0:
            print '%s started at time: %s' % (self.getName(), datetime.datetime.now())
        alat = self.alat[index]
        alon = self.alon[index]
        na = len(alat)
        nb = len(self.blat)
        dum = np.tile(np.deg2rad(alat), (nb, 1))
        dumdst = np.cos(dum)
        interm = np.sin(dum)
        del dum
        dum = np.tile(np.deg2rad(self.blat).transpose(), (na, 1)).transpose()
        dumdst *= np.cos(dum)
        interm *= np.sin(dum)
        del dum
        dum = np.tile(np.deg2rad(alon), (nb, 1))
        dum -= np.tile(np.deg2rad(self.blon).transpose(), (na, 1)).transpose()
        dumdst *= np.cos(dum)
        del dum
        dumdst += interm
        dumdst = rt * np.arccos(dumdst)
        del interm
        self.indices.put(id)
        self.result.put(dumdst)
        del dumdst
        if verbose > 0:
            print '%s ended at time: %s' % (self.getName(), datetime.datetime.now())

    def run(self):
        self.task()
        self.input.task_done()


def distance_matrix_parallel(alat, alon, blat, blon, N_thread=4):
    input_q = Queue.Queue()
    indices_q = Queue.Queue()
    result_q = Queue.Queue()
    x = len(alat)
    y = len(blat)
    step = np.ceil(np.float(x) / N_thread)
    if N_thread * step < x:
        raise '[ERROR] splitting of time series is not valid'
    if step <= N_thread:
        if verbose > 1:
            print '[WARNING] series too short. back to sequential code'
        return distance_matrix(alat, alon, blat, blon)
    indices = []
    for i in np.arange(N_thread):
        indices.append(np.arange(i * step, i * step + step))

    indices = []
    for i in np.arange(N_thread):
        dumind = np.arange(i * step, i * step + step, dtype=np.long)
        dumind = dumind.compress((dumind >= 0) & (dumind <= x - 1))
        indices.append(dumind)

    for i in range(N_thread):
        t = ThreadClass(input_q, indices_q, result_q, alat, alon, blat, blon)
        t.setDaemon(True)
        t.start()

    for i in range(N_thread):
        input_q.put((i, indices[i]))

    input_q.join()
    tnb = []
    for i in range(N_thread):
        tnb.append(indices_q.get(i))

    tsort = np.argsort(tnb)
    for i in np.arange(N_thread):
        r = result_q.get(i)
        if i == 0:
            dum = [r]
        else:
            dum.append(r)

    for i in tsort:
        if i == tsort[0]:
            dist_matrix = dum[i]
        else:
            dist_matrix = np.append(dist_matrix, dum[i], 1)

    if dist_matrix.shape != (y, x):
        raise Exception('[ERROR]Output matrix is not coherent with input data - check matrix reconstruction')
    return dist_matrix


def distance_matrix_inline(lat_a, lon_a, lat_b, lon_b):
    na = np.size(lat_a)
    nb = np.size(lat_b)
    rt = 6378.137
    dum = np.tile(np.deg2rad(lat_a), (nb, 1))
    dist_matrix = np.cos(dum)
    interm = np.sin(dum)
    del dum
    dum = np.tile(np.deg2rad(lat_b).transpose(), (na, 1)).transpose()
    dist_matrix *= np.cos(dum)
    interm *= np.sin(dum)
    del dum
    dum = np.tile(np.deg2rad(lon_a), (nb, 1))
    dum -= np.tile(np.deg2rad(lon_b).transpose(), (na, 1)).transpose()
    dist_matrix *= np.cos(dum)
    del dum
    dist_matrix += interm
    del interm
    dist_matrix = rt * np.arccos(dist_matrix)
    return dist_matrix


def distance_matrix(alat, alon, blat, blon, parallel=True, **kwargs):
    if parallel:
        return distance_matrix_inline(alat, alon, blat, blon, **kwargs)
    else:
        return distance_matrix_inline(alat, alon, blat, blon)