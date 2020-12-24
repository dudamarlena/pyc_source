# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dotcloud/ui/tests/test_hello.py
# Compiled at: 2012-09-19 14:56:08
from dotcloud.cli2 import CLI

def test_hello():
    CLI().run()
    assert True