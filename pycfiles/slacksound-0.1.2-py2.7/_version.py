# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/slacksound/_version.py
# Compiled at: 2017-10-13 17:29:19
"""
Manages the version of the package.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import os
__author__ = 'Oriol Fabregas <fabregas.oriol@gmail.com>'
__docformat__ = 'google'
__date__ = '2017-10-13'
__copyright__ = 'Copyright 2017, Oriol Fabregas'
__license__ = 'MIT'
__maintainer__ = 'Oriol Fabregas'
__email__ = '<fabregas.oriol@gmail.com>'
__status__ = 'Development'
VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.VERSION'))
LOCAL_VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '.VERSION'))
try:
    with open(VERSION_FILE_PATH) as (f):
        __version__ = f.read()
except IOError:
    with open(LOCAL_VERSION_FILE_PATH) as (f):
        __version__ = f.read()