# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\test\setup.py
# Compiled at: 2020-04-19 22:03:14
# Size of source mod 2**32: 540 bytes
from setuptools import find_packages, setup
setup(name='Delirium',
  version='0.3.0',
  description='Delirium fake DNS server',
  license='LICENSE',
  packages=(find_packages()),
  install_requires=[
 'dnslib',
 'ipaddress',
 'sqlalchemy',
 'click'],
  setup_requires=[
 'pytest-runner'],
  tests_require=[
 'pytest'],
  entry_points={'console_scripts': [
                     'delirium = delirium.app:delirium']})