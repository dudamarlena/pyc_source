# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/boot_common.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 3035 bytes
import sys
if getattr(sys, 'frozen', False):
    try:
        from ctypes import *
        hwnd = windll.user32.GetForegroundWindow()
        out = windll.kernel32.GetStdHandle(-11)
        USECONSOLE = bool(windll.kernel32.SetConsoleTextAttribute(out, 7))
    except:
        USECONSOLE = False

    if not USECONSOLE:

        class Stderr(object):
            softspace = 0
            _file = None
            _error = None

            def write(self, text, alert=None, fname=sys.executable + '.log'):
                if self._file is None and self._error is None:
                    try:
                        self._file = open(fname, 'a')
                    except Exception as e:
                        self._error = str(e)

                    if self._file is not None:
                        self._file.write(text)
                        self.flush()

            def flush(self):
                if self._file is not None:
                    self._file.flush()


        sys.stderr = Stderr()

        class Stdout(Stderr):
            __doc__ = ''


        sys.stdout = Stdout()