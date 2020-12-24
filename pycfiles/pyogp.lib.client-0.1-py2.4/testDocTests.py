# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/testDocTests.py
# Compiled at: 2010-02-09 00:00:15
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
import unittest, doctest
optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

def setUp(self):
    pass


def tearDown(self):
    pass


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocFileSuite('agent.txt', 'login.txt', 'caps.txt', 'region.txt', package='pyogp.lib.client.tests.doctests', setUp=setUp, tearDown=tearDown, optionflags=optionflags))
    return suite