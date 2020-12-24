# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xmlconfig/setup.py
# Compiled at: 2015-06-29 10:25:54
import os
from setuptools import setup, find_packages
setup(name='xmlconfig', version='0.0.1', description='XML config helper', author='Gustavo Maia Neto (Guto Maia)', author_email='guto@guto.net', license='GPL3', packages=find_packages(), scripts=[
 'bin/xmlconfig'], classifiers=[
 'Development Status :: 3 - Alpha',
 'Environment :: Console'], url='http://github.com/gutomaia/xmlconfig/')