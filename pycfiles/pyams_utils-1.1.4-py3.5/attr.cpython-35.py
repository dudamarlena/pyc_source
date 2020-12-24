# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/attr.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1678 bytes
"""PyAMS_utils.attr module

This module provides an :ref:`ITraversable` adapter which can be used to get access to an object's
attribute from a browser URL.
This adapter is actually used to get access to 'file' attributes in PyAMS_file package.
"""
from pyramid.exceptions import NotFound
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable
from pyams_utils.adapter import ContextAdapter, adapter_config
__docformat__ = 'restructuredtext'

@adapter_config(name='attr', context=Interface, provides=ITraversable)
class AttributeTraverser(ContextAdapter):
    __doc__ = '++attr++ namespace traverser\n\n    This custom traversing adapter can be used to access an object attribute directly from\n    an URL by using a path like this::\n\n    /path/to/object/++attr++name\n\n    Where *name* is the name of the requested attribute.\n    '

    def traverse(self, name, furtherpath=None):
        """Traverse from current context to given attribute"""
        if '.' in name:
            name = name.split('.', 1)
        try:
            return getattr(self.context, name)
        except AttributeError:
            raise NotFound