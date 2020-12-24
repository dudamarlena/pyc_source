# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vasctrees/utils.py
# Compiled at: 2012-07-28 17:50:18
"""A set of utilities common to multiple vasctree scripts and packages"""
import gzip, cPickle

def getOrderedGraphKeys(ogs):
    keys = ogs.keys()
    txt = 'Select number of desired key:\n'
    for i in range(len(keys)):
        txt += '%d\t\t%s\n' % (i, keys[i])

    while True:
        try:
            keyNum = input(txt)
            if 0 <= keyNum and keyNum < len(keys):
                return keys[keyNum]
        except:
            pass

    return


def readGraphs(fname):
    try:
        fo = gzip.open(fname, 'rb')
        data = cPickle.load(fo)
        fo.close()
    except:
        fo = file(fname, 'rb')
        data = cPickle.load(fo)
        fo.close()

    return data


def writeGraphs(data, fname):
    fo = gzip.open(fname, 'wb')
    cPickle.dump(data, fo)
    fo.close()