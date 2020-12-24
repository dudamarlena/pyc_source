# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/test/testall.py
# Compiled at: 2007-06-28 09:07:49
"""Launch all tests from the dasty/tests directory.

Author: Jean-Christophe Hoelt <hoelt@irit.fr>
Copyright (c) 2007, IRIT-CNRS

This file is released under the CECILL-C licence.

"""
from test.SceneTest import SceneTest
from test.ViewPlatformTest import ViewPlatformTest
import unittest
if __name__ == '__main__':
    unittest.main()