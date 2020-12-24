# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/portlet/toc/interfaces.py
# Compiled at: 2010-03-01 12:20:27
from zope.viewlet.interfaces import IViewletManager

class IFullViewManager(IViewletManager):
    """Viewlet manager on top of the full view on the expanded view
       used to show the table of contents
    """
    __module__ = __name__