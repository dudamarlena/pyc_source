#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages


def _load_requires_from_file(filepath):
    return [pkg_name.rstrip('\r\n') for pkg_name in open(filepath).readlines()]


def _install_requires():
    requires = _load_requires_from_file('requirements.txt')
    if sys.version_info >= (2, 7, 0):
        requires.remove('argparse')
    return requires


def _test_requires():
    test_requires = _load_requires_from_file('test-requirements.txt')
    if sys.version_info >= (3, 3, 0):
        test_requires.remove('mock')
    return test_requires


def _packages():
    return find_packages(
        exclude=[
            '*.tests',
            '*.tests.*',
            'tests.*',
            'tests'
        ],
    )


if __name__ == '__main__':
    setup(
        name='cmonkey',
        version='0.1.1',
        description='Simple scripting framework for Apache CloudStack',
        author='momijiame',
        author_email='amedama.ginmokusei@gmail.com',
        url='https://github.com/momijiame/cmonkey',
        classifiers=[
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Intended Audience :: Developers',
            'Natural Language :: Japanese',
            'Operating System :: POSIX'
        ],
        packages=_packages(),
        install_requires=_install_requires(),
        tests_require=_test_requires(),
        test_suite='nose.collector',
        include_package_data=True,
        zip_safe=False,
        entry_points="""
        [console_scripts]
        cmonkey = cmonkey.cmd:main
        """,
    )
