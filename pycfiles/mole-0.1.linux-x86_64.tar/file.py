# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/input/file.py
# Compiled at: 2012-07-12 07:13:07
from mole.input import Input

class InputFile(file, Input):
    """Dummy class which wrapper a file."""
    pass


class InputFileWrapper(Input):

    def __init__(self, f):
        self.f = f

    def close(self):
        self.f.close()

    def __iter__(self):
        return iter(self.f)