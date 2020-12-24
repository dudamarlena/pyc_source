# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/_wire.py
# Compiled at: 2008-05-07 15:44:29
"""
$Id: _wire.py 2205 2008-05-07 19:44:27Z hazmat $
"""
try:
    from zope.component import provideAdapter
except ImportError:
    provideAdapter = None

from interfaces import ISubversionNode, ISubversionProperties
from property import SubversionProperties
if provideAdapter is not None:
    provideAdapter(provides=ISubversionProperties, adapts=(
     ISubversionNode,), factory=SubversionProperties)