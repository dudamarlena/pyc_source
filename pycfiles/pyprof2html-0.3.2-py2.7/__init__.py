# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pyprof2html/__init__.py
# Compiled at: 2017-07-31 22:01:26
"""pyprof2html - Profile data convert to HTML.

This module is converted to HTML file from Python's cProfile and
hotshot profiling data.
"""
from pyprof2html.core import Converter
from pyprof2html.commands import pyprof2html_main
from pyprof2html._version import __version__
__licence__ = 'New BSD License'
__author__ = 'Hideo Hattori <hhatto.jp@gmail.com>'
__all__ = [
 'Converter', 'pyprof2html_main', '__version__']