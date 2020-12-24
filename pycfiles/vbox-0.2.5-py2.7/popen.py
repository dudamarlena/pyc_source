# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\cli\popen.py
# Compiled at: 2013-03-15 12:05:06
import subprocess

class Popen(subprocess.Popen):
    """Popen class that executes python callable when called process finishes."""

    def __init__(self, *args, **kwargs):
        self._returnHandle = kwargs.pop('onFinish', None)
        super(Popen, self).__init__(*args, **kwargs)
        return

    _realReturnCode = None

    def returncode():
        doc = 'The returncode property.'

        def fget(self):
            return self._realReturnCode

        def fset(self, value):
            self._realReturnCode = value
            if value is not None and self._returnHandle:
                self._returnHandle(self)
            return

        return locals()

    returncode = property(**returncode())