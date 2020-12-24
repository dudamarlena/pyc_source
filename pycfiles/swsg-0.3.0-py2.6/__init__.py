# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/swsg/__init__.py
# Compiled at: 2010-11-29 08:26:31
__version__ = '0.3.0'

class NoninstalledPackage(Exception):
    """raised if a required python package is not installed"""

    def __init__(self, package_name):
        self.package_name = package_name

    def __str__(self):
        return ('the package {0!r} is not installed').format(self.package_name)

    def __repr__(self):
        return ('{0}({1})').format(self.__class__.__name__, self.package_name)