# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/value.py
# Compiled at: 2019-12-24 07:39:43
# Size of source mod 2**32: 1558 bytes
__doc__ = 'PyAMS_table.value module\n\nThis module provides several default values adapters.\n'
from pyramid.interfaces import IRequest
from zope.container.interfaces import IContainer
from zope.interface import Interface, implementer
from pyams_table.interfaces import ISequenceTable, ITable, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
__docformat__ = 'reStructuredText'

@implementer(IValues)
class ValuesMixin(ContextRequestViewAdapter):
    """ValuesMixin"""
    pass


@adapter_config(context=(IContainer, IRequest, ITable), provides=IValues)
class ValuesForContainer(ValuesMixin):
    """ValuesForContainer"""

    @property
    def values(self):
        """Get container values"""
        return self.context.values()


@adapter_config(context=(Interface, IRequest, ISequenceTable), provides=IValues)
class ValuesForSequence(ValuesMixin):
    """ValuesForSequence"""

    @property
    def values(self):
        """Get sequence values"""
        return self.context