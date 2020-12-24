# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/interfaces/container.py
# Compiled at: 2013-09-22 07:20:44
__docformat__ = 'restructuredtext'
from ztfy.base.interfaces.container import IContainer as IContainerBase
from ztfy.base.interfaces.container import IOrderedContainer as IOrderedContainerBase

class IContainer(IContainerBase):
    """Marker interface to containers"""
    pass


class IOrderedContainer(IOrderedContainerBase):
    """Marker interface for ordered containers"""
    pass