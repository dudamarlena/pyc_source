# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup, find_packages

VERSION = '0.1.0'

setup(
    name='syncitems',
    version=VERSION,
    license='GPL-3.0',
    description='Sync item between clients with server',
    url='https://github.com/ipconfiger/syncitems',
    author='Alexander.Li',
    author_email='superpowerlee@gmail.com',
    platforms='any',
    install_requires=[
        'SQLAlchemy>=1.1.4',
        'redis>=2.10.5',
    ],
    packages=find_packages()
)
