# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/securitytool/testing.py
# Compiled at: 2010-10-22 19:01:08
import os
from zope.app.testing import functional
SecurityToolLayer = functional.ZCMLLayer(os.path.join(os.path.dirname(__file__), 'site.zcml'), __name__, 'SecuritiyToolLayer', allow_teardown=True)