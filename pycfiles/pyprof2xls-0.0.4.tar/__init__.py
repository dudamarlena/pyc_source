# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pyprof2html/__init__.py
# Compiled at: 2017-07-31 22:01:26
__doc__ = "pyprof2html - Profile data convert to HTML.\n\nThis module is converted to HTML file from Python's cProfile and\nhotshot profiling data.\n"
from pyprof2html.core import Converter
from pyprof2html.commands import pyprof2html_main
from pyprof2html._version import __version__
__licence__ = 'New BSD License'
__author__ = 'Hideo Hattori <hhatto.jp@gmail.com>'
__all__ = [
 'Converter', 'pyprof2html_main', '__version__']