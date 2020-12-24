# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolelib/powermolelib/_version.py
# Compiled at: 2019-04-06 08:36:04
# Size of source mod 2**32: 2100 bytes
__doc__ = '\nManages the version of the package.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\n'
import os
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-04-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.VERSION'))
LOCAL_VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '.VERSION'))
try:
    with open(VERSION_FILE_PATH) as (f):
        __version__ = f.read()
except IOError:
    with open(LOCAL_VERSION_FILE_PATH) as (f):
        __version__ = f.read()