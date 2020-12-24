# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\zope\setup.py
# Compiled at: 2019-08-29 22:24:39
# Size of source mod 2**32: 767 bytes
import sys
from cx_Freeze import setup, Executable
options = {'build_exe': {'namespace_packages': ['zope']}}
executables = [
 Executable('qotd.py')]
setup(name='QOTD sample', version='1.0', description='QOTD sample for demonstrating use of namespace packages', options=options, executables=executables)