# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/interfaces.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 2169 bytes
"""PyAMS_viewlet.interfaces module

The module defines viewlet and viewlets manager interfaces.
"""
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute
from zope.interface.common.mapping import IReadMapping
__docformat__ = 'restructuredtext'

class IViewlet(IContentProvider):
    __doc__ = 'A content provider that is managed by another content provider, known\n    as viewlet manager.\n\n    Note that you *cannot* call viewlets directly as a provider, i.e. through\n    the TALES ``provider`` expression, since it always has to know its manager.\n    '
    manager = Attribute('The Viewlet Manager\n\n                        The viewlet manager for which the viewlet is registered. The viewlet\n                        manager will contain any additional data that was provided by the\n                        view.\n                        ')


class IViewletManager(IContentProvider, IReadMapping):
    __doc__ = "A component that provides access to the content providers.\n\n    The viewlet manager's responsibilities are:\n\n      (1) Aggregation of all viewlets registered for the manager.\n\n      (2) Apply a set of filters to determine the availability of the\n          viewlets.\n\n      (3) Sort the viewlets based on some implemented policy.\n\n      (4) Provide an environment in which the viewlets are rendered.\n\n      (5) Render itself by rendering the HTML content of the viewlets.\n    "

    def filter(self, viewlets):
        """Filter manager viewlets"""
        pass

    def sort(self, viewlets):
        """Sort manager viewlets"""
        pass

    def reset(self):
        """Reset manager status; this can be required if the manager between renderings"""
        pass