# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_erd.py
# Compiled at: 2016-02-12 12:18:44
import os
from nose.tools import ok_
from dmsa import erd
SERVICE = os.environ.get('DMSA_TEST_SERVICE', 'http://data-models.origins.link/')

def test_all():
    erd.write('omop', '5.0.0', 'test_erd_out.png', SERVICE)
    ok_(os.path.exists('test_erd_out.png'))