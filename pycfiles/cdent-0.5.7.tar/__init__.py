# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: package/__init__.py
# Compiled at: 2010-06-11 01:30:06
"""package package package
"""
import os, sys, glob
from distutils.core import Command
__version__ = '0.0.8'
has_setuptools = False
from package.errors import *
try:
    from setuptools import setup as real_setup
    has_setuptools = True
except ImportError, err:
    try:
        from distutils.core import setup as real_setup
    except ImportError, err:
        die(ENOSETUP)

class setup:

    def __init__(self):
        args = self.get_args()
        self.check_args(args)
        real_setup(**args)

    def get_args(self):
        try:
            import package.info
        except ImportError, err:
            die(ENOINFO)

        args = package.info.get()
        args['cmdclass'] = {'test': Test, 
           'devtest': DevTest}
        return args

    def check_args(self, args):
        if args.get('install_requires') and 'install' in sys.argv:
            if not has_setuptools:
                die(ENOSETUPTOOLS)


class Test(Command):
    user_options = []
    test_dir = 'tests'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_cmd = self.get_finalized_command('build')
        build_cmd.run()
        sys.path.insert(0, build_cmd.build_lib)
        sys.path.insert(0, self.test_dir)

        def exit(code):
            pass

        sys.exit = exit
        for test in glob.glob(self.test_dir + '/*.py'):
            name = test[test.index('/') + 1:test.rindex('.')]
            module = __import__(name)
            module.main(module=module, argv=[''])


class DevTest(Test):
    test_dir = 'dev-tests'