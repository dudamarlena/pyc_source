# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/FileLock.py
# Compiled at: 2011-12-24 06:30:42
import os, logging
from apgl.util.Parameter import Parameter

class FileLock(object):
    """
    A simple class to aid multiprocessing by "locking" jobs through the use
    of files.
    """

    def __init__(self, fileName):
        """
        Lock a job whose results are saved as fileName. 
        """
        Parameter.checkClass(fileName, str)
        self.fileName = fileName
        self.lockFileName = self.fileName + '.lock'

    def lock(self):
        """
        Create a lock file for a process.
        """
        lockFile = open(self.lockFileName, 'w')
        lockFile.close()
        logging.debug('Locking file ' + self.lockFileName)

    def unlock(self):
        """
        Release a lock file for a process.
        """
        if os.path.isfile(self.lockFileName):
            os.remove(self.lockFileName)
            logging.debug('Deleted lock file ' + self.lockFileName)
        else:
            logging.warn('Unlocking from non-existant file ' + self.lockFileName)

    def isLocked(self):
        """
        Test whether the process is locked 
        """
        return os.path.isfile(self.lockFileName)

    def fileExists(self):
        """
        Check if the results file exists. 
        """
        return os.path.isfile(self.fileName)