# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/progress.py
# Compiled at: 2019-09-19 10:33:37
# Size of source mod 2**32: 2214 bytes
import sys, itertools

class progressBar(object):

    def __init__(self, progress_message, type='pulse', refresh_delay=0.25, finish_message='Finished', error_message='An error has occurred'):
        self.barArray = itertools.cycle(self._pulseArrays(type))
        self.refreshDelay = float(refresh_delay)
        self.messagelen = 0
        self.msg = '\r' + progress_message
        self.fin = '\r' + finish_message
        self.err = '\r' + error_message
        self.overwrite_progress_length = len(self.msg) + 21

    def _pulseArrays(self, ptype='pulse'):
        types = [
         'pulse', 'dial', 'dots']
        if ptype not in types:
            ptype = 'pulse'
        elif ptype == 'pulse':
            parray = [
             '___________________'] * 20
            parray = [parray[i][:i] + '/\\' + parray[i][i:] for i in range(len(parray))]
            parray = parray + parray[-2:0:-1]
        else:
            if ptype == 'dial':
                parray = [
                 '-', '\\', '|', '/', '-', '\\', '|', '/']
            else:
                if ptype == 'dots':
                    parray = [
                     ' '] * 19
                    parray = ['.' * i + ''.join(parray[i:]) for i in range(len(parray))]
        return parray

    def _clearLine(self):
        chars = len(self.msg) + 27
        sys.stdout.write('\r%s' % (chars * ' '))
        sys.stdout.flush()

    def updateProgressMessage(self, msg):
        self.msg = '\r' + msg

    def writeprogress(self):
        msg = '\r' + ' '.join([self.msg, next(self.barArray)])
        sys.stdout.write(msg)
        sys.stdout.flush()

    def success(self):
        self._clearLine()
        sys.stdout.write(self.fin + '\n')
        sys.stdout.flush()

    def error(self):
        self._clearLine()
        sys.stdout.write(self.err + '\n')
        sys.stdout.flush()

    def update(self, *args):
        self._clearLine()
        msg = self.msg + ' %s  '
        args += tuple([next(self.barArray)])
        sys.stdout.write(msg % args)
        sys.stdout.flush()