# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/silva/purge/tests/PurgingTestCase.py
# Compiled at: 2012-05-16 10:37:34
from Products.Silva.tests import SilvaTestCase
from Products.Silva.testing import TestCase
import bethel.silva.purge, layer

class PurgingTestCase(TestCase):
    layer = layer.PurgeLayer(bethel.silva.purge, zcml_file='configure.zcml')