# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/multiprocess/bootstrap.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1162 bytes
__doc__ = 'For starting up remote processes'
import sys, pickle, os
if __name__ == '__main__':
    if hasattr(os, 'setpgrp'):
        os.setpgrp()
    elif sys.version[0] == '3':
        opts = pickle.load(sys.stdin.buffer)
    else:
        opts = pickle.load(sys.stdin)
    path = opts.pop('path', None)
    if path is not None:
        while len(sys.path) > 0:
            sys.path.pop()

        sys.path.extend(path)
    if opts.pop('pyside', False):
        import PySide
    targetStr = opts.pop('targetStr')
    target = pickle.loads(targetStr)
    target(**opts)
    sys.exit(0)