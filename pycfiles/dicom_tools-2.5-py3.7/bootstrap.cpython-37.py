# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/multiprocess/bootstrap.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1162 bytes
"""For starting up remote processes"""
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