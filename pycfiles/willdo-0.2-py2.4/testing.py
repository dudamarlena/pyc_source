# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/willdo/testing.py
# Compiled at: 2008-04-22 18:15:38
import os.path, willdo
from zope.app.testing.functional import ZCMLLayer
ftesting_zcml = os.path.join(os.path.dirname(willdo.__file__), 'ftesting.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer')