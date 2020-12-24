#!/usr/bin/env python

from __future__ import absolute_import  # unicode_literals breaks setup.py

import os
import re
import sys
from codecs import open

from setuptools import setup
from setuptools.command.test import test as test_command


class MakeTest(test_command):
    user_options = [('nosetests', '[PATH]', "(Optional) Path to test files to run.")]

    def initialize_options(self):
        test_command.initialize_options(self)
        self.nose_args = []

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import nose

        errno = nose.run(*self.nose_args)
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'mason',
    'mason.query',
]

requires = []
test_requirements = ['nose>=1.3.7']

with open('mason/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='mason',
    version=version,
    description='Python SQL query generation without the ORM.',
    long_description=readme,
    author='Vail Gold',
    author_email='vail130@gmail.com',
    url='https://github.com/vail130/mason',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'mason': 'mason'},
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=True,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    cmdclass={'test': MakeTest},
    tests_require=test_requirements,
    extras_require={},
)
