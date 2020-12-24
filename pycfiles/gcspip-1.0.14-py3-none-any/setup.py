# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manuel/gcspypi/test/data/test_package/setup.py
# Compiled at: 2018-11-22 07:00:57
from setuptools import setup
setup(name='test_package', version='1.0.0', packages=[
 'package'], install_requires=[
 'test_dep1',
 'test_dep2'])