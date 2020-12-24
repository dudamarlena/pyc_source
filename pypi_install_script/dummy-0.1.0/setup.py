#! /usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import os
import sys

import dummy

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt','requirements.txt','changes.txt',)

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='dummy',
    version=dummy.__version__,
    url='http://github.com/hn269/dummy/',
    license='Cornell University',
    author='Hoang Long Nguyen',
    tests_require=['pytest',],
    install_requires=['jinja2>=2.0.0','numpy>=1.0.0','mock>=1.0.0',],
    cmdclass={'test': PyTest,},
    author_email='hn269@cornell.com',
    description='Dummy package adding, subtracting or multiplying two numbers - to try releasing a Python package',
    long_description=long_description,
    packages=['dummy',],
    data_files=[('',['requirements.txt','changes.txt'])],
    include_package_data=True,
    platforms='any',
    test_suite='dummy.test.test_dummy',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    extras_require={
        'testing': ['pytest'],
    },
    #zip_safe = True,
)