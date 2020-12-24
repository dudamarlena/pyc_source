# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/repoze/what/release.py
# Compiled at: 2010-04-06 05:16:33
"""
repoze.what release information.

The version number is loaded to help the Quickstart plugin configure
repoze.what correctly, depending on the version available -- although it may
be useful on other packages.

"""
import os
_here = os.path.abspath(os.path.dirname(__file__))
_root = os.path.dirname(os.path.dirname(_here))
version = open(os.path.join(_root, 'VERSION.txt')).readline().rstrip()
major_version = int(version.split('.')[0])