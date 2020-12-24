# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pyprof2html/environment.py
# Compiled at: 2016-10-19 12:59:46
__doc__ = "Global pyprof2html's environment.\n"
from jinja2 import Environment, PackageLoader
__all__ = [
 'ENVIRON']
CODEC = 'utf-8'
ENVIRON = Environment(loader=PackageLoader('pyprof2html', './templates', encoding=CODEC))