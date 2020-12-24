# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joekavalieri/git/conversionman/conversionman/lib/python2.7/site-packages/redisengine/proxy/base/metaclasses.py
# Compiled at: 2016-03-29 09:53:56
import warnings
from redisengine.core.common import _tree_registry
from redisengine.core.fields import BaseField
from redisengine.core.manager import ProxyTreeManager, DirectTreeManager
from redisengine.proxy.base.tree import BaseProxyTree
from redisengine.connection import DEFAULT_CONNECTION_NAME
from redisengine.exceptions import InvalidTreeError, InvalidTreeWarning

class TreeMetaclass(type):
    allowed_names = ('id', 'save', 'validate', 'clean')

    def __new__(cls, name, bases, attrs):
        super_new = super(TreeMetaclass, cls).__new__
        if attrs.get('__metaclass__') == cls:
            return super_new(cls, name, bases, attrs)
        else:
            if bases and issubclass(bases[0], BaseProxyTree):
                if hasattr(bases[0], '_meta'):
                    raise ValueError(('Cannot subclass {}').format(bases[0]))
                classes = bases[0].__base__.mro() + [bases[0]]
                reserved_attrs = {attr for kls in classes for attr in dir(kls) if not attr.startswith('_') and attr not in cls.allowed_names}
                overlapping_attrs = set(attrs.keys()) & reserved_attrs
                if overlapping_attrs:
                    raise InvalidTreeError(('model `{}` defines illegal attributes/methods: {}').format(name, list(overlapping_attrs)))
            meta_attrs = {'tree_key_prefix': None, 'tree_index_key': None, 
               'pk_field_name': 'id', 
               'has_auto_pk': True, 
               'db_alias': DEFAULT_CONNECTION_NAME, 
               'ttl': None}
            field_names = {}
            doc_fields = {}

            def adjust_pk_index_name(tree_index_key):
                if not tree_index_key.startswith('__'):
                    tree_index_key = '__' + tree_index_key.lower()
                if not tree_index_key.endswith(':idx'):
                    tree_index_key += ':idx'
                return tree_index_key

            users_meta = attrs.get('Meta', None)
            if users_meta:
                meta_attrs = {k:getattr(users_meta, k, v) for k, v in meta_attrs.iteritems()}
            meta_attrs['__slots__'] = meta_attrs.keys()
            meta = type('Meta', (object,), meta_attrs)
            reserved = {attr for kls in classes for attr in dir(kls) if not attr == 'id' if not attr == 'id'}
            for field_name, field in attrs.iteritems():
                if not isinstance(field, BaseField):
                    continue
                if field_name in reserved:
                    raise InvalidTreeError(('`{}` is not a valid name for a field').format(field_name))
                field.name = field_name
                if not field.db_field:
                    field.db_field = field_name
                if hasattr(field, 'pk_type'):
                    if not field_name == 'id':
                        raise InvalidTreeError('A field name for PrimaryKey can only be `id`')
                    if issubclass(field.pk_type, str):
                        meta.has_auto_pk = False
                    meta.tree_index_key = adjust_pk_index_name(field._prefix or name)
                    meta.tree_key_prefix = name.lower()
                doc_fields[field_name] = field
                field_names[field.db_field] = field_names.get(field.db_field, 0) + 1

            attrs.pop('id', None)
            if not meta.tree_key_prefix:
                meta.has_auto_pk = True
                meta.tree_key_prefix = name.lower()
                meta.tree_index_key = adjust_pk_index_name(meta.tree_index_key or name)
            attrs['_ttl'] = meta.ttl
            duplicate_db_fields = [ k for k, v in field_names.items() if v > 1 ]
            if duplicate_db_fields:
                msg = 'Multiple db_fields defined for: %s ' % (', ').join(duplicate_db_fields)
                raise InvalidTreeError(msg)
            attrs['_fields'] = doc_fields
            attrs['_db_field_map'] = {k:getattr(v, 'db_field', k) for k, v in doc_fields.iteritems()}
            attrs['_reverse_db_field_map'] = {v:k for k, v in attrs['_db_field_map'].iteritems()}
            attrs['_fields_ordered'] = tuple(i[1] for i in sorted((v.creation_counter, v.name) for v in doc_fields.itervalues()))
            attrs['_class_name'] = name
            attrs['_meta'] = meta
            if 'proxy_tree' not in dir(attrs):
                proxy_tree_manager = ProxyTreeManager
            else:
                assert issubclass(attrs['proxy_tree'], ProxyTreeManager)
                proxy_tree_manager = attrs['proxy_tree']
            attrs['proxy_tree'] = proxy_tree_manager(meta.tree_key_prefix)
            if 'direct_tree' not in dir(attrs):
                direct_tree_manager = DirectTreeManager
            else:
                assert issubclass(attrs['direct_tree'], DirectTreeManager)
                direct_tree_manager = attrs['direct_tree']
            attrs['direct_tree'] = direct_tree_manager(attrs.copy())
            new_class = super_new(cls, name, bases, attrs)
            _tree_registry[new_class._class_name] = new_class
            for field in new_class._fields.itervalues():
                if field.owner_tree is None:
                    field.owner_tree = new_class

            return new_class