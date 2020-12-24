# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/optimalgrouping/__init__.py
# Compiled at: 2020-03-04 06:18:40
# Size of source mod 2**32: 533 bytes
from __future__ import absolute_import, division, print_function
import pkgutil, os
__author__ = 'Carlo Ferrigno'
pkg_dir = os.path.abspath(os.path.dirname(__file__))
pkg_name = os.path.basename(pkg_dir)
__all__ = []
for importer, modname, ispkg in pkgutil.walk_packages(path=[pkg_dir], prefix=(pkg_name + '.'),
  onerror=(lambda x: None)):
    if ispkg == True:
        __all__.append(modname)
        continue