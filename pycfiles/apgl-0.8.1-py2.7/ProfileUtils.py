# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/ProfileUtils.py
# Compiled at: 2013-05-13 12:16:40
"""
Some functions to make profiling code a bit simpler.
"""
import logging, numpy, scipy.sparse
from apgl.util.PathDefaults import PathDefaults
import os

class ProfileUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def profile(command, globalVars, localVars, numStats=30):
        """
        Just profile the given command with the global and local variables
        and print out the cumulative and function times. 
        """
        try:
            import pstats, cProfile
        except ImportError:
            raise ImportError('profile() requires pstats and cProfile')

        outputDirectory = PathDefaults.getOutputDir()
        directory = outputDirectory + 'test/'
        profileFileName = directory + 'profile.cprof'
        logging.info('Starting to profile ...')
        cProfile.runctx(command, globalVars, localVars, profileFileName)
        logging.info('Done')
        stats = pstats.Stats(profileFileName)
        stats.strip_dirs().sort_stats('cumulative').print_stats(numStats)
        stats.strip_dirs().sort_stats('time').print_stats(numStats)

    @staticmethod
    def memDisplay(localDict):
        """
        Try to display the memory usage of numpy and scipy arrays. The input
        is the local namespace dict, found using memDisplay(locals())
        """
        arrayList = []
        for item in localDict.keys():
            if type(localDict[item]) == numpy.ndarray:
                bytes = localDict[item].nbytes
                arrayList.append((item, localDict[item].shape, bytes))
            elif scipy.sparse.issparse(localDict[item]):
                bytes = localDict[item].getnnz() * localDict[item].dtype.itemsize
                arrayList.append((item, localDict[item].shape, bytes))

        for item in globals().keys():
            if type(globals()[item]) == numpy.ndarray:
                bytes = globals()[item].nbytes
                arrayList.append((item, globals()[item].shape, bytes))
            elif scipy.sparse.issparse(globals()[item]):
                bytes = globals()[item].data.nbytes
                arrayList.append((item, globals()[item].shape, bytes))

        arrayList.sort(key=lambda s: s[2])
        arrayList.reverse()
        logging.debug('---------------------------------------')
        for item in arrayList:
            logging.debug(str(item[0]) + ': ' + str(item[1]) + ' - ' + str(float(item[2]) / 1000000) + ' MB')

        logging.debug('---------------------------------------')

    @staticmethod
    def _VmB(VmKey):
        """Private.
        """
        _proc_status = '/proc/%d/status' % os.getpid()
        _scale = {'kB': 1024.0, 'mB': 1048576.0, 'KB': 1024.0, 
           'MB': 1048576.0}
        try:
            t = open(_proc_status)
            v = t.read()
            t.close()
        except:
            return 0.0

        i = v.index(VmKey)
        v = v[i:].split(None, 3)
        if len(v) < 3:
            return 0.0
        else:
            return float(v[1]) * _scale[v[2]]

    @staticmethod
    def memory(since=0.0):
        """Return memory usage in bytes.
        """
        return ProfileUtils._VmB('VmSize:') - since

    @staticmethod
    def resident(since=0.0):
        """Return resident memory usage in bytes.
        """
        return ProfileUtils._VmB('VmRSS:') - since

    @staticmethod
    def stacksize(since=0.0):
        """Return stack size in bytes.
        """
        return ProfileUtils._VmB('VmStk:') - since