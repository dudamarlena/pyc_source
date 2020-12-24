# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\win7ools\__init__.py
# Compiled at: 2014-12-26 18:14:34
"""wintools -- Collection of code snippets for the Windows OS"""
__author__ = 'Jason Wohlgemuth'
__version__ = '1.0'
__versioninfo__ = (1, 0, 0)
import doctest, unittest
from distutils.log import warn
from win7ools.system import System
from win7ools.ipl import IPL
from win7ools.reg import RegistryKeys as keys
python_paths = [
 'C:\\Python27',
 'C:\\Python27\\Lib\\site-packages',
 'C:\\Python27\\Scripts',
 'C:\\Python27\\Tools\\Scripts']

def test():
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=2)
    modules = ['ipl', 'lib', 'pdf', 'sec']
    for module in modules:
        warn('importing ' + module + ' ...')
        _temp = __import__('win7ools', globals(), locals(), [module], -1)
        mod_test_suite = doctest.DocTestSuite(eval(module))
        suite.addTest(mod_test_suite)

    runner.run(suite)


if __name__ == '__main__':
    print 'Under construction...'