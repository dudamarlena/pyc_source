#!/usr/bin/env python

"""Set-up the module."""

from setuptools import setup

setup(
    name='exploroar',
    version='1.0',
    description='Python library to exploROAR your code!',
    author='Roar Data Team',
    author_email='antoine.toussaint@roardata.com',
    url='https://github.com/roardata/exploroar',
    keywords=['exploroar', 'roardata', 'roar'],
    install_requires=[
        'pandas',
        'python-dateutil',
        'pytz',
        'requests',
        'jsonpath_rw',
        'Algorithmia',
        'tenacity'
    ]
)
