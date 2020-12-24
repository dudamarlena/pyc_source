# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/chessmind/grok/testing.py
# Compiled at: 2008-04-25 19:13:35
import os.path, chessmind.grok
from zope.app.testing.functional import ZCMLLayer
ftesting_zcml = os.path.join(os.path.dirname(chessmind.grok.__file__), 'ftesting.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer')