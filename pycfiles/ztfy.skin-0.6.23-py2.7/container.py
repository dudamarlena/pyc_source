# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/interfaces/container.py
# Compiled at: 2014-03-09 18:20:11
__docformat__ = 'restructuredtext'
from ztfy.baseskin.interfaces.container import *
from zope.interface import Interface

class IContainerAddFormMenuTarget(Interface):
    """Marker interface for base add form menu item"""
    pass


class IMainContentAddFormMenuTarget(IContainerAddFormMenuTarget):
    """Marker interface for main content add form menu item"""
    pass