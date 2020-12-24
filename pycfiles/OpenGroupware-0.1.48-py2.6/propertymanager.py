# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/propertymanager.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.foundation import *
from exception import AccessForbiddenException, CoilsException
OGO_EXT_ATTR_SPACE = 'http://www.opengroupware.org/properties/ext-attr'
OGO_APT_EXT_ATTR_DEFAULT = 'OGoExtendedAptAttributes'

class PropertyManager(object):
    __slots__ = '_ctx'
    _apt_ext_attr_dict = None

    def __init__(self, ctx):
        self._ctx = ctx
        if PropertyManager._apt_ext_attr_dict is None:
            PropertyManager.load_extended_attributes()
        return

    @staticmethod
    def Get_Object_Id(value):
        object_id = None
        try:
            if isinstance(value, ORMEntity):
                object_id = value.object_id
            else:
                object_id = long(value)
        except Exception, e:
            print e
            raise CoilsException(('Unable to understand {0} as an entity reference (objectId)').format(value))

        return object_id

    @staticmethod
    def Parse_Property_Name(name):
        return ObjectProperty.Parse_Property_Name(name)

    @staticmethod
    def load_extended_attributes():
        """ Read the defined Appointment extended attributes from the server's
            global defaults.  Contacts and Enterprises use Company Values for
            extended (custom) attributes, where Appointments use the property
            system.
            Result:
              {'Billable': {'kind': '2', 'label': '', 'values': ['YES', 'NO']},
               'Color': {'kind': '1', 'label': '', 'values': []},
               'EMail': {'kind': '3', 'label': '', 'values': []}}
            Type: 1 = String, does not need to be specified, default
                  2 = Boolean (Check box) of YES / NO
                  3 = E-Mail Address (string)
                  9 = Multi-select, produces a CSV string """
        PropertyManager._apt_ext_attr_dict = {}
        sd = ServerDefaultsManager()
        if sd.is_default_defined(OGO_APT_EXT_ATTR_DEFAULT):
            for attr in sd.default_as_list(OGO_APT_EXT_ATTR_DEFAULT):
                spec = {}
                if attr.has_key('type'):
                    spec['kind'] = attr['type']
                    if spec['kind'] == '2':
                        spec['values'] = [
                         'YES', 'NO']
                    elif attr.has_key('values'):
                        spec['values'] = attr['values'].keys()
                    else:
                        spec['values'] = []
                else:
                    spec['kind'] = '1'
                    spec['values'] = []
                if attr.has_key('label'):
                    spec['label'] = attr['label']
                else:
                    spec['label'] = ''
                PropertyManager._apt_ext_attr_dict[attr['key']] = spec

    def get_defined_appointment_properties(self):
        return PropertyManager._apt_ext_attr_dict

    def get_preferred_kinds(self):
        return [
         'valueString', 'valueInt', 'valueFloat',
         'valueDate', 'valueOID', 'valueBlob']

    def get_property(self, entity, namespace, name):
        db = self._ctx.db_session()
        object_id = PropertyManager.Get_Object_Id(entity)
        query = db.query(ObjectProperty).filter(and_(ObjectProperty.parent_id == object_id, ObjectProperty.namespace == namespace, ObjectProperty.name == name, or_(ObjectProperty.access_id == self._ctx.account_id, ObjectProperty.access_id == None)))
        result = query.first()
        return result

    def get_properties(self, entity):
        db = self._ctx.db_session()
        data = []
        object_id = PropertyManager.Get_Object_Id(entity)
        query = db.query(ObjectProperty).filter(and_(ObjectProperty.parent_id == object_id, or_(ObjectProperty.access_id == self._ctx.account_id, ObjectProperty.access_id == None)))
        for prop in query.all():
            if prop.namespace == OGO_EXT_ATTR_SPACE:
                prop.kind = PropertyManager._apt_ext_attr_dict[prop.name]['kind']
                prop.label = PropertyManager._apt_ext_attr_dict[prop.name]['label']
                prop.values = PropertyManager._apt_ext_attr_dict[prop.name]['values']
            else:
                prop.kind = ''
                prop.label = ''
                prop.values = ''
            data.append(prop)

        query = None
        return data

    @staticmethod
    def Name_Of_Property(prop):
        if isinstance(prop, dict):
            if 'propertyName' in prop:
                return PropertyManager.Parse_Property_Name(prop.get('propertyName'))
            if 'namespace' in prop:
                if 'name' in prop:
                    return (prop.get('namespace'), prop.get('name'))
                if 'attribute' in prop:
                    return (prop.get('namespace'), prop.get('attribute'))
        elif isinstance(prop, ObjectProperty):
            return (prop.namespace, prop.name)
        return (None, None)

    def set_property(self, entity, namespace, attribute, value, private=False):
        object_id = PropertyManager.Get_Object_Id(entity)
        if object_id == 0:
            if not self._ctx.is_admin:
                raise AccessForbiddenException('Only administrative contexts can set server properties')
        prop = self.get_property(object_id, namespace, attribute)
        if prop is None:
            name = ('{{{0}}}{1}').format(namespace, attribute)
            if private:
                self._ctx.db_session().add(ObjectProperty(object_id, name, value=value, access_id=self._ctx.account_id))
            else:
                self._ctx.db_session().add(ObjectProperty(object_id, name, value=value))
        else:
            prop.set_value(value)
        return

    def set_properties(self, entity, props):
        object_id = PropertyManager.Get_Object_Id(entity)
        if entity.object_id == 0:
            if self._ctx.is_admin:
                pass
            else:
                raise AccessForbiddenException('Only administrative contexts can set server properties')
        if isinstance(props, list):
            db_props = self.get_properties(object_id)
            removes = []
            for prop in db_props:
                removes.append(int(prop.object_id))

            for in_prop in props:
                (in_namespace, in_name) = PropertyManager.Name_Of_Property(in_prop)
                for ex_prop in db_props:
                    if in_namespace == ex_prop.namespace and in_name == ex_prop.name:
                        ex_prop.set_value(in_prop.get('value'))
                        removes.remove(int(ex_prop.object_id))
                        break
                else:
                    new_prop = ObjectProperty(object_id, ('{{{0}}}{1}').format(in_namespace, in_name), value=in_prop.get('value'))
                    self._ctx.db_session().add(new_prop)
                    new_prop = None

            db_props = None
            db = self._ctx.db_session()
            if len(removes) > 0:
                db.query(ObjectProperty).filter(ObjectProperty.object_id.in_(removes)).delete(synchronize_session='fetch')
        return

    def delete_property(self, entity, namespace, attribute, private=False):
        object_id = PropertyManager.Get_Object_Id(entity)
        if object_id == 0:
            if not self._ctx.is_admin:
                raise AccessForbiddenException('Only administrative contexts can set server properties')
        prop = self.get_property(object_id, namespace, attribute)
        if prop:
            self._ctx.db_session().delete(prop)
            return True
        return False

    def get_server_property(self, namespace, name):
        return self.get_property(0, namespace, name)

    def get_server_properties(self):
        return self.get_properties(0)

    def set_server_property(self, namespace, name, value):
        self.set_property(0, namespace, name, value)