# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/shortcuts/contextmanagers.py
# Compiled at: 2016-02-25 04:17:16
from ycyc.base.contextutils import *
from ycyc.base.allowfail import AllowFail
from ycyc.base.filetools import cd, safe_open_for_read, safe_open_for_update, safe_open_for_write
from ycyc.base.logutils import log_disable