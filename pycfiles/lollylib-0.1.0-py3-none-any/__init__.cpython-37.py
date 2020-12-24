# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\assets\prog_python\2019\lollylib\lollylib\tests\__init__.py
# Compiled at: 2019-06-21 04:27:19
# Size of source mod 2**32: 341 bytes
"""
Following code adds parent directory to sys.path so that
all python files in it can be directly imported by tests.
As a result, the tests always use library version
located in their parent dir.
"""
import os, sys, ntpath
head, tail = ntpath.split(os.path.realpath(__file__))
sys.path.append(os.path.dirname(head))