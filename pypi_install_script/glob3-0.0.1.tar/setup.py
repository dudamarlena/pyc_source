#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='glob3',
    version='0.0.1',
    description='WORK IN PROGRESS - Glob with recursive search support/ multiple filetypes',
    author='camabeh',
    url='https://github.com/camabeh/glob3',
    packages=['glob3'],
    entry_points={
        'console_scripts': ['glob3 = glob3.__main__:main']
    }
)
