# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/datamanager.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 5480 bytes
"""PyAMS_form.datamanager module

This module provides base data manager classes.
"""
from zope.interface import implementer, Interface
from zope.interface.common.mapping import IMapping
from zope.schema.interfaces import IField
from zope.security import canAccess, canWrite
from zope.security.interfaces import ForbiddenAttribute
from zope.security.proxy import Proxy
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import IDataManager, NO_VALUE
__docformat__ = 'restructuredtext'
_MARKER = []
ALLOWED_DATA_CLASSES = [
 dict]
try:
    import persistent.mapping, persistent.dict
    ALLOWED_DATA_CLASSES.append(persistent.mapping.PersistentMapping)
    ALLOWED_DATA_CLASSES.append(persistent.dict.PersistentDict)
except ImportError:
    pass

@implementer(IDataManager)
class DataManager:
    __doc__ = 'Data manager base class.'


@adapter_config(required=(Interface, IField), provides=IDataManager)
class AttributeField(DataManager):
    __doc__ = 'Attribute field.'

    def __init__(self, context, field):
        self.context = context
        self.field = field

    @property
    def adapted_context(self):
        """Data manager adapted context getter"""
        context = self.context
        if self.field.interface is not None:
            context = self.field.interface(context)
        return context

    def get(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        return getattr(self.adapted_context, self.field.__name__)

    def query(self, default=NO_VALUE):
        """See pyams_utils.interfaces.form.IDataManager"""
        try:
            return self.get()
        except ForbiddenAttribute as e:
            raise e
        except AttributeError:
            return default

    def set(self, value):
        """See pyams_utils.interfaces.form.IDataManager"""
        if self.field.readonly:
            raise TypeError("Can't set values on read-only fields (name=%s, class=%s.%s)" % (
             self.field.__name__,
             self.context.__class__.__module__,
             self.context.__class__.__name__))
        setattr(self.adapted_context, self.field.__name__, value)

    def can_access(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        context = self.adapted_context
        if isinstance(context, Proxy):
            return canAccess(context, self.field.__name__)
        return True

    def can_write(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        context = self.adapted_context
        if isinstance(context, Proxy):
            return canWrite(context, self.field.__name__)
        return True


@adapter_config(required=(dict, IField), provides=IDataManager)
class DictionaryField(DataManager):
    __doc__ = 'Dictionary field.\n\n    NOTE: Even though, this data manager allows nearly all kinds of\n    mappings, by default it is only registered for dict, because it\n    would otherwise get picked up in undesired scenarios. If you want\n    to it use for another mapping, register the appropriate adapter in\n    your application.\n\n    '
    _allowed_data_classes = tuple(ALLOWED_DATA_CLASSES)

    def __init__(self, data, field):
        if not isinstance(data, self._allowed_data_classes) and not IMapping.providedBy(data):
            raise ValueError('Data are not a dictionary: %s' % type(data))
        self.data = data
        self.field = field

    def get(self):
        """See pyams_utils.interfaces.form.IDataManager"""
        value = self.data.get(self.field.__name__, _MARKER)
        if value is _MARKER:
            raise AttributeError
        return value

    def query(self, default=NO_VALUE):
        """See pyams_utils.interfaces.form.IDataManager"""
        return self.data.get(self.field.__name__, default)

    def set(self, value):
        """See pyams_utils.interfaces.form.IDataManager"""
        if self.field.readonly:
            raise TypeError("Can't set values on read-only fields name=%s" % self.field.__name__)
        self.data[self.field.__name__] = value

    @staticmethod
    def can_access():
        """See pyams_utils.interfaces.form.IDataManager"""
        return True

    @staticmethod
    def can_write():
        """See pyams_utils.interfaces.form.IDataManager"""
        return True