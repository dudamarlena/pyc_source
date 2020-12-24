# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/util/mutex.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2938 bytes
from ..Qt import QtCore
import traceback

class Mutex(QtCore.QMutex):
    """Mutex"""

    def __init__(self, *args, **kargs):
        if kargs.get('recursive', False):
            args = (
             QtCore.QMutex.Recursive,)
        (QtCore.QMutex.__init__)(self, *args)
        self.l = QtCore.QMutex()
        self.tb = []
        self.debug = True

    def tryLock(self, timeout=None, id=None):
        if timeout is None:
            locked = QtCore.QMutex.tryLock(self)
        else:
            locked = QtCore.QMutex.tryLock(self, timeout)
        if self.debug:
            if locked:
                self.l.lock()
                try:
                    if id is None:
                        self.tb.append(''.join(traceback.format_stack()[:-1]))
                    else:
                        self.tb.append('  ' + str(id))
                finally:
                    self.l.unlock()

        return locked

    def lock(self, id=None):
        c = 0
        waitTime = 5000
        while 1:
            if self.tryLock(waitTime, id):
                break
            c += 1
            if self.debug:
                self.l.lock()
                try:
                    print('Waiting for mutex lock (%0.1f sec). Traceback follows:' % (c * waitTime / 1000.0))
                    traceback.print_stack()
                    if len(self.tb) > 0:
                        print('Mutex is currently locked from:\n')
                        print(self.tb[(-1)])
                    else:
                        print('Mutex is currently locked from [???]')
                finally:
                    self.l.unlock()

    def unlock(self):
        QtCore.QMutex.unlock(self)
        if self.debug:
            self.l.lock()
            try:
                if len(self.tb) > 0:
                    self.tb.pop()
                else:
                    raise Exception('Attempt to unlock mutex before it has been locked')
            finally:
                self.l.unlock()

    def depth(self):
        self.l.lock()
        n = len(self.tb)
        self.l.unlock()
        return n

    def traceback(self):
        self.l.lock()
        try:
            ret = self.tb[:]
        finally:
            self.l.unlock()

        return ret

    def __exit__(self, *args):
        self.unlock()

    def __enter__(self):
        self.lock()
        return self