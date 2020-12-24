# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pyprof2html/environment.py
# Compiled at: 2016-10-19 12:59:46
"""Global pyprof2html's environment.
"""
from jinja2 import Environment, PackageLoader
__all__ = [
 'ENVIRON']
CODEC = 'utf-8'
ENVIRON = Environment(loader=PackageLoader('pyprof2html', './templates', encoding=CODEC))