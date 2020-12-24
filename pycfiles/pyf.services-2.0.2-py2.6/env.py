# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/core/env.py
# Compiled at: 2011-05-23 08:33:02
import tempfile, os

def init_tempdir(tempdir):
    if not os.path.exists(tempdir):
        msg = 'Cannot set the temporary directory %s because it doesn t exist' % tempdir
        raise ValueError(msg)
    tempfile.tempdir = tempdir