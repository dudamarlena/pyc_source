# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/utils/benchmark.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 5557 bytes
"""
This module is containing benchmarks for rsync
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '07/06/2017'
import os, shutil, tempfile, time
from tomwer.synctools.rsyncmanager import RSyncManager

class BenchRSyncClass(object):
    ORI_FOLDER = '/home/payno/testRSync/data/'

    def __init__(self):
        """
        """
        self.folder1Path = tempfile.mkdtemp()
        print(self.folder1Path)
        self.folder2Path = tempfile.mkdtemp()
        assert os.path.isdir(self.folder1Path)
        assert os.path.isdir(self.folder2Path)

    def __del__(self):
        if os.path.isdir(self.folder1Path):
            shutil.rmtree(self.folder1Path)
        if os.path.isdir(self.folder2Path):
            shutil.rmtree(self.folder2Path)

    def testCopy(self, options, parallel=False, nbIter=3):
        startTime = time.time()
        for it in range(nbIter):
            RSyncManager().syncFolderRaw(source=(self.folder1Path), target=(self.folder2Path),
              options=options,
              parallel=parallel,
              block=True)
            RSyncManager().syncFolderRaw(source=(self.folder2Path), target=(self.folder1Path),
              options=options,
              parallel=parallel,
              block=True)

        return (time.time() - startTime) / nbIter

    def testCopyFolders(self, f1, f2, options, parallel=False, nbIter=1):
        fullTime = 0
        for it in range(nbIter):
            startTime = time.time()
            RSyncManager().syncFolderRaw(source=f1, target=f2,
              options=options,
              parallel=parallel,
              block=True)
            fullTime += time.time() - startTime
            RSyncManager().syncFolderRaw(source=f2, target=f1,
              options=options,
              parallel=parallel,
              block=True)

        return fullTime / nbIter

    def testCopyTree(self, parallel=True):
        startTime = time.time()
        shutil.copytree(src=(self.folder1Path), dst=(os.path.join(self.folder2Path, 'test')))
        shutil.rmtree(os.path.join(self.folder1Path, 'test'))
        shutil.copytree(src=(self.folder2Path), dst=(os.path.join(self.folder1Path, 'test')))
        return time.time() - startTime


def benchemark_rsync():
    l = BenchRSyncClass()
    options = []
    options.append(['-a'])
    options.append(['-r'])
    f1 = '/lbsram/data/visitor/mi1226/bm05/nemoz/test1_'
    f2 = '/data/visitor/mi1226/bm05/nemoz/test1_'
    print('----- not using parallel ------')
    for opt in options:
        print('options are : ')
        print(opt)
        print(l.testCopyFolders(f1, f2, opt, parallel=False))

    print('----- default shutil ------')
    print(l.testCopyTree())


if __name__ == '__main__':
    benchemark_rsync()