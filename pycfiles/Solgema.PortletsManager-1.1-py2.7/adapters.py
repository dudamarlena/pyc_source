# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Solgema/PortletsManager/portlets/adapters.py
# Compiled at: 2014-11-05 08:49:31
from zope.interface import implements
from Solgema.PortletsManager.interfaces import ISolgemaPortletAssignment
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.annotation.attribute import AttributeAnnotations
from plone.app.portlets.portlets.base import Assignment
from Solgema.PortletsManager import options
try:
    from zope.annotation import IAnnotations
except ImportError:
    from zope.app.annotation import IAnnotations

from persistent.dict import PersistentDict
from persistent import Persistent
_marker = object()
SolgemaPortletAssignmentStorage = options.PersistentOptions.wire('SolgemaPortletAssignmentStorage', 'SolgemaPortletAssignment', ISolgemaPortletAssignment)

class SolgemaPortletAssignment(SolgemaPortletAssignmentStorage, AttributeAnnotations):
    implements(ISolgemaPortletAssignment)
    _storage = None

    def __init__(self, context):
        self.context = context