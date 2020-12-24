#!/usr/bin/env python

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-vs', 'crawlers']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        self.handle_exit()
        sys.exit(errno)

    @staticmethod
    def handle_exit():
        import atexit
        atexit._run_exitfuncs()


setup(name='crawlers',
      version='0.0.1',
      description='WEB Crawlers for multiple services',
      url='http://github.com/lensacom/crawlers',
      maintainer='Krisztian Szucs',
      maintainer_email='szucs.krisztian@gmail.com',
      keywords='',
      packages=['crawlers'],
      install_requires=[],
      tests_require=[],
      cmdclass={'test': PyTest},
      zip_safe=False)
