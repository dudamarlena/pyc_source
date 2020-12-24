# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\file\xmind-sdk-python-master\setup.py
# Compiled at: 2019-07-01 23:22:26
# Size of source mod 2**32: 431 bytes
from setuptools import setup, find_packages
setup(name='xmind',
  version='0.1a.0',
  packages=(find_packages()),
  install_requires=[
 'distribute'],
  author='Woody Ai',
  author_email='aiqi@xmind.net',
  description='The offical XMind python SDK',
  license='MIT',
  keywords='XMind, SDK, mind mapping',
  url='https://github.com/xmindltd/xmind-sdk-python')