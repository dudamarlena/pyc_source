# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/ipc/httputil.py
# Compiled at: 2008-07-28 17:15:44
import warnings
warnings.warn('indra.ipc.httputil has been deprecated; use eventlet.httpc instead', DeprecationWarning, 2)
from eventlet.httpc import *
makeConnection = make_connection