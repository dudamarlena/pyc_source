# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/core/env.py
# Compiled at: 2011-05-23 08:33:02
import tempfile, os

def init_tempdir(tempdir):
    if not os.path.exists(tempdir):
        msg = 'Cannot set the temporary directory %s because it doesn t exist' % tempdir
        raise ValueError(msg)
    tempfile.tempdir = tempdir