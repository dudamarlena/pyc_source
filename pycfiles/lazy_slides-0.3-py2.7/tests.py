# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/tests/tests.py
# Compiled at: 2012-01-22 12:14:35
import os, unittest

def run():
    l = unittest.TestLoader()
    s = l.discover(os.path.dirname(__file__))
    unittest.TextTestRunner().run(s)


if __name__ == '__main__':
    run()