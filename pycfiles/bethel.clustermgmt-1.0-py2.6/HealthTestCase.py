# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/clustermgmt/tests/HealthTestCase.py
# Compiled at: 2012-04-27 11:10:15
from Products.Silva.testing import TestCase
import bethel.clustermgmt, layer

class HealthTestCase(TestCase):
    layer = layer.HealthLayer(bethel.clustermgmt, zcml_file='configure.zcml')