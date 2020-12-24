# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/djangoflash/__init__.py
# Compiled at: 2011-02-12 11:21:43
"""
    Django-flash
    ~~~~~~~~~~~~

    Rails-like *flash* messages support for Django.

    :copyright: 2008-2009, Destaquenet Technology Solutions.
    :license: BSD.
"""
__version__ = '1.8'
__author__ = 'Daniel Fernandes Martins'
__email__ = 'daniel@destaquenet.com'

def run_tests(verbosity=1):
    """Runs the tests. This function is useful when you want to check if an
    already installed version of Django-Flash (e.g. one that don't have a
    ``setup.py`` file) works as expected. Example::
    
        $ python -c "import djangoflash; djangoflash.run_tests();"
    """
    from djangoflash.tests import suite
    import unittest
    runner = unittest.TextTestRunner(verbosity=verbosity)
    unittest.main(module=suite, testRunner=runner)