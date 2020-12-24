# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/attr.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1678 bytes
__doc__ = "PyAMS_utils.attr module\n\nThis module provides an :ref:`ITraversable` adapter which can be used to get access to an object's\nattribute from a browser URL.\nThis adapter is actually used to get access to 'file' attributes in PyAMS_file package.\n"
from pyramid.exceptions import NotFound
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable
from pyams_utils.adapter import ContextAdapter, adapter_config
__docformat__ = 'restructuredtext'

@adapter_config(name='attr', context=Interface, provides=ITraversable)
class AttributeTraverser(ContextAdapter):
    """AttributeTraverser"""

    def traverse(self, name, furtherpath=None):
        """Traverse from current context to given attribute"""
        if '.' in name:
            name = name.split('.', 1)
        try:
            return getattr(self.context, name)
        except AttributeError:
            raise NotFound