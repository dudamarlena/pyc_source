# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chimera/tests/runalltests.py
# Compiled at: 2007-02-11 13:01:51
import os, sys, unittest
from distutils.util import get_platform
plat_specifier = '.%s-%s' % (get_platform(), sys.version[0:3])
build_platlib = os.path.join('build', 'lib' + plat_specifier)
test_lib = os.path.join(os.path.abspath('..'), build_platlib)
sys.path.insert(0, test_lib)
TestRunner = unittest.TextTestRunner
suite = unittest.TestSuite()
tests = [
 'test_pangocairo',
 'test_svg',
 'test_snippets',
 'test_doctest',
 'test_chimera']
for test in tests:
    m = __import__(test)
    if hasattr(m, 'test_suite'):
        suite.addTest(m.test_suite())

def main():
    TestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    main()