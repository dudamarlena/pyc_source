# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/value.py
# Compiled at: 2019-12-24 07:39:43
# Size of source mod 2**32: 1558 bytes
"""PyAMS_table.value module

This module provides several default values adapters.
"""
from pyramid.interfaces import IRequest
from zope.container.interfaces import IContainer
from zope.interface import Interface, implementer
from pyams_table.interfaces import ISequenceTable, ITable, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
__docformat__ = 'reStructuredText'

@implementer(IValues)
class ValuesMixin(ContextRequestViewAdapter):
    __doc__ = 'Mixin for different value adapters'


@adapter_config(context=(IContainer, IRequest, ITable), provides=IValues)
class ValuesForContainer(ValuesMixin):
    __doc__ = 'Values adapter from a simple IContainer'

    @property
    def values(self):
        """Get container values"""
        return self.context.values()


@adapter_config(context=(Interface, IRequest, ISequenceTable), provides=IValues)
class ValuesForSequence(ValuesMixin):
    __doc__ = 'Values adapter from a simple sequence table'

    @property
    def values(self):
        """Get sequence values"""
        return self.context