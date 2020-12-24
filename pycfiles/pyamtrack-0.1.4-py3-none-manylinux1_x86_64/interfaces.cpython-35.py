# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/interfaces.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 2169 bytes
__doc__ = 'PyAMS_viewlet.interfaces module\n\nThe module defines viewlet and viewlets manager interfaces.\n'
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute
from zope.interface.common.mapping import IReadMapping
__docformat__ = 'restructuredtext'

class IViewlet(IContentProvider):
    """IViewlet"""
    manager = Attribute('The Viewlet Manager\n\n                        The viewlet manager for which the viewlet is registered. The viewlet\n                        manager will contain any additional data that was provided by the\n                        view.\n                        ')


class IViewletManager(IContentProvider, IReadMapping):
    """IViewletManager"""

    def filter(self, viewlets):
        """Filter manager viewlets"""
        pass

    def sort(self, viewlets):
        """Sort manager viewlets"""
        pass

    def reset(self):
        """Reset manager status; this can be required if the manager between renderings"""
        pass