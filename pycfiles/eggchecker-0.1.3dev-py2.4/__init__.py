# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/eggchecker/__init__.py
# Compiled at: 2007-11-29 10:47:26
"""
setuptools commands
"""
import sys, os
from setuptools import Command
from runflakes import run_flake
from runtests import run_tests

class QAChecker(Command):
    """setuptools Command"""
    __module__ = __name__
    description = 'run quality assurance tests over the package'
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        run_flake()


class ZChecker(Command):
    """setuptools Command"""
    __module__ = __name__
    description = 'run zope.testing test runner over the package'
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        if os.curdir == '.':
            top_dir = os.path.realpath(os.curdir)
        else:
            top_dir = os.curdir
        exit = False
        for dirname in os.listdir(top_dir):
            if not os.path.isdir(dirname):
                continue
            if dirname in ('build', 'dist') or dirname.startswith('.'):
                continue
            try:
                run_tests(os.path.join(top_dir, dirname))
            except SystemExit, e:
                if e.code:
                    exit = e.code

        sys.exit(exit)