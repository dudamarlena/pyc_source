"""
Use this file for building the 'nal-scripts' scripts functionality.

This file is used for creating the 'nal-scripts' executable for running
the scripts for the nal-ml program.
"""
from setuptools import setup

setup(
    name='nal-scripts',
    version='0.1',
    py_modules=['nal_scripts'],
    install_requires=[
        'Click',
        'request',
        'Python-Dotenv',
        ],
    entry_points='''
        [console_scripts]
        nal-scripts=__init__:cli
    ''',
    )
