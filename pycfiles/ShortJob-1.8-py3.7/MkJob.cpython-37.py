# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ShortJob/MkJob.py
# Compiled at: 2020-04-28 04:53:42
# Size of source mod 2**32: 1054 bytes
import os
from ShortJob import MkMulJob

class MkJob(MkMulJob.MkMulJob):
    __doc__ = ' Make job with only one task, inherited from MkMulJob\n    '

    def __init__(self, cpp='fit.cxx'):
        MkMulJob.MkMulJob.__init__(self, [cpp])
        self._cwd = os.getcwd()

    def Make(self, index, var):
        """generate a bash script contains only one task

        Args:
            index(int): the ID of job, the job is named as job_{index}.sh
            var(tuple or list): the in put args for the task

        Returns
            void
        """
        tail = self._cpp.split('.')[0]
        logName = 'log_{}.{}'.format(index, tail)
        MkMulJob.Make(index, [var], [logName])