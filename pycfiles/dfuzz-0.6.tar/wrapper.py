# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/core/wrapper.py
# Compiled at: 2011-04-25 11:13:45
import logging, subprocess
from dfuzz.core import exceptions

class DfuzzWrapper(object):

    def __str__(self):
        return 'undefined wrapper, add __str__ method'

    def system(self, command):
        logging.debug('Executing: %s', command)
        pr = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = pr.communicate()
        retcode = pr.poll()
        if retcode != 0:
            logging.error('Command "%s" returned nonzero value try running it by hand', command)
            raise exceptions.SyscallException(stdout, stderr)
        return stdout