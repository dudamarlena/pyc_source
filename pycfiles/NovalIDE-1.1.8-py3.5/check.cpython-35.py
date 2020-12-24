# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/check.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1146 bytes
import noval.util.appdirs as appdirs, os, psutil, noval.util.utils as utils, noval.python.parser.utils as parserutils

class SingleInstanceChecker(object):
    __doc__ = 'description of class'

    def __init__(self):
        user_data_path = appdirs.get_user_data_path()
        if not os.path.exists(user_data_path):
            parserutils.MakeDirs(user_data_path)
        self.lock = os.path.join(user_data_path, 'lock')
        self.pid = None
        self.Create()

    def Create(self):
        if not os.path.exists(self.lock):
            self.SetPid()
        else:
            self.GetPid()

    def IsAnotherRunning(self):
        if self.pid is None:
            return False
            try:
                psutil.Process(int(self.pid))
            except:
                utils.get_logger().info('app process id %s is not run again', self.pid)
                self.SetPid()
                return False

            return True

    def GetPid(self):
        with open(self.lock) as (f):
            self.pid = f.read()

    def SetPid(self):
        with open(self.lock, 'w') as (f):
            f.write(str(os.getpid()))