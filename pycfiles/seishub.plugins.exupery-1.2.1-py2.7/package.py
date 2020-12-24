# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\plugins\exupery\package.py
# Compiled at: 2010-12-23 17:42:41
"""
Exupery package for seishub.core.
"""
from seishub.core.core import Component, implements
from seishub.core.packages.interfaces import IPackage

class ExuperyPackage(Component):
    """
    Exupery package for seishub.core.
    """
    implements(IPackage)
    package_id = 'exupery'
    version = '0.1'