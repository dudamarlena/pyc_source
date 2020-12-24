# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/certbotlib/_version.py
# Compiled at: 2017-09-11 15:29:22
__doc__ = '\nDefines __version__\n\nSet the package version here\n'
import os
VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.VERSION'))
LOCAL_VERSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '.VERSION'))
try:
    with open(VERSION_FILE_PATH) as (f):
        __version__ = f.read()
except IOError:
    with open(LOCAL_VERSION_FILE_PATH) as (f):
        __version__ = f.read()