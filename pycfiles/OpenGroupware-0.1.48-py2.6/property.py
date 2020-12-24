# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/property.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, date, tzinfo
from sqlalchemy import *
from utcdatetime import UTCDateTime, UniversalTimeZone
from base import *

class ObjectProperty(Base):
    """ An OpenGroupware Property Object """
    __tablename__ = 'obj_property'
    __entityName__ = 'objectProperty'
    __internalName__ = 'ObjectProperty'
    object_id = Column('obj_property_id', Integer, Sequence('key_generator'), primary_key=True)
    parent_id = Column('obj_id', Integer, ForeignKey('person.company_id'), ForeignKey('enterprise.company_id'), ForeignKey('date_x.date_id'), ForeignKey('job.job_id'), ForeignKey('project.project_id'), ForeignKey('doc.document_id'), ForeignKey('route.route_id'), ForeignKey('process.process_id'), ForeignKey('company_value.company_value_id'), nullable=False)
    namespace = Column('namespace_prefix', String(255), nullable=False)
    name = Column('value_key', String(255), nullable=False)
    _string_value = Column('value_string', String(255))
    _date_value = Column('value_date', UTCDateTime())
    _integer_value = Column('value_int', Integer)
    _float_value = Column('value_float', Float)
    _oid_value = Column('value_oid', String(255))
    _blob_value = Column('value_blob', Text)
    _blob_size = Column('blob_size', Integer)
    _data_hint = Column('preferred_type', String(255))
    kind = 1
    label = ''
    values = []
    access_id = Column('access_key', Integer)

    def __init__(self, object_id, name, value=None, access_id=None):
        self.parent_id = object_id
        (self.namespace, self.name) = ObjectProperty.Parse_Property_Name(name)
        self.set_value(value)
        self.access_id = access_id

    def __repr__(self):
        return ('<ObjectProperty parentId={0} namespace="{1}" name="{2}">').format(self.parent_id, self.namespace, self.name)

    @staticmethod
    def get_preferred_kinds():
        return ['valueString', 'valueInt', 'valueFloat',
         'valueDate', 'valueOID', 'valueBlob']

    @staticmethod
    def Parse_Property_Name(name):
        """ Takes a full formally formed property name and splits it into
            namespace and attribute.
            For example:
                {http://www.example.com/properties/ext-attr}skyColor
                - returns -
               ('http://www.example.com/properties/ext-attr', 'skyColor')
            DO NOT PARSE PROPERTY NAMES YOURSELF, USE THIS METHOD! """
        x = name.split('}')
        return (x[0][1:], x[1])

    def get_value(self):
        hint = self.get_hint()
        if hint is None:
            hint = 'string'
        elif self._data_hint not in ObjectProperty.get_preferred_kinds():
            hint = 'string'
        if hint == 'string':
            if self._blob_value:
                return self._blob_value
            return self._string_value
        else:
            if hint in 'timestamp':
                return self._date_value
            if hint == 'int':
                return self._integer_value
            if hint == 'float':
                return self._float_value
            if hint == 'oid':
                return self._oid_value
            if hint == 'data':
                raise 'Unsupported property type encountered, patches welcome.'
            else:
                return self._string_value
            return

    def set_value(self, x):
        """ Store the value in the appropriate field(s) and hint for next time
            the value is retrieved: we get back the type we stored."""
        if x is None:
            self._string_value = None
            self._integer_value = None
            self._date_value = None
            self._float_value = None
            self._oid_value = None
            self._blob_value = None
        elif isinstance(x, basestring):
            try:
                self._integer_value = int(x)
            except:
                self._integer_value = None
            else:
                self._date_value = None
                try:
                    self._float_value = int(x)
                except:
                    self._float_value = None
                else:
                    self._oid_value = None
                    if len(x) > 254:
                        self._blob_value = x
                        self._blob_size = len(x)
                        self._string_value = x[:255]
                    else:
                        self._string_value = x
                        self._blob_value = None
                    self._data_hint = 'valueString'
        elif isinstance(x, int) or isinstance(x, long):
            self._string_value = str(x)
            self._integer_value = x
            self._date_value = None
            self._float_value = x
            self._oid_value = None
            self._blob_value = None
            self._data_hint = 'valueInt'
        elif isinstance(x, float):
            self._string_value = str(x)
            self._integer_value = int(x)
            self._date_value = None
            self._float_value = x
            self._oid_value = None
            self._blob_value = None
            self._data_hint = 'valueFloat'
        elif isinstance(x, datetime):
            if not x.tzinfo:
                x = x.replace(tzinfo=UniversalTimeZone())
            x = x.astimezone(UniversalTimeZone())
            self._string_value = x.strftime('%Y-%m-%d %H:%M:%S')
            self._integer_value = x.toordinal()
            self._date_value = x
            self._float_value = float(self._integer_value)
            self._oid_value = None
            self._blob_value = None
            self._data_hint = 'valueDate'
        elif isinstance(x, date):
            x = datetime(x.year, x.month, x.day, tzinfo=UniversalTimeZone())
            self._string_value = x.strftime('%Y-%m-%d')
            self._integer_value = x.toordinal()
            self._date_value = x
            self._float_value = float(self._integer_value)
            self._oid_value = None
            self._blob_value = None
            self._data_hint = 'valueDate'
        else:
            raise Exception(('Property value of type {0} cannot be preserved for property {1}/{2}').format(type(x).__name__, self.namespace, self.name))
        return

    def get_hint(self):
        if self._data_hint is None:
            return 'unknown'
        else:
            if self._data_hint == 'valueString':
                return 'string'
            else:
                if self._data_hint == 'valueDate':
                    return 'timestamp'
                if self._data_hint == 'valueInt':
                    return 'int'
                if self._data_hint == 'valueFloat':
                    return 'float'
                if self._data_hint == 'valueOID':
                    return 'oid'
                if self._data_hint == 'valueBlob':
                    return 'data'
                return 'unknown'
            return