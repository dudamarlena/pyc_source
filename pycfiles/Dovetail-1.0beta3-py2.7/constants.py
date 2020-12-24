# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/constants.py
# Compiled at: 2012-08-19 03:54:41
"""Version and product information constants"""
from os import path

def read(filename):
    """Returns the contants of the file as a string"""
    return open(path.join(path.dirname(__file__), filename)).read()


VERSION = '1.0beta3'
DEVELOPMENT_STATUS = 'Development Status :: 4 - Beta'
DESCRIPTION = 'Dovetail: A light-weight, multi-platform build tool with Continuous Integration servers like Jenkins in mind'
USAGE = read('USAGE.rst') + '\n' + read('NOTICE.txt')
EPILOG = read('NOTICE.txt')
WARRANTY = read('WARRANTY.txt')
LICENSE = read('LICENSE.txt')