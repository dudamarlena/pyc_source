# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/entity.py
# Compiled at: 2007-03-21 14:34:41
"""Entity class.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from string import digits, ascii_letters
import inspect
from schevo import base
from schevo.constant import UNASSIGNED
from schevo.error import EntityDoesNotExist, ExtentDoesNotExist, FieldDoesNotExist, SchemaError
from schevo.fieldspec import field_spec_from_class
from schevo.fieldspec import FieldMap, FieldSpecMap
from schevo.label import LabelMixin, label_from_name, plural_from_name, with_label
import schevo.namespace
from schevo.namespace import NamespaceExtension
from schevo import query
from schevo import transaction
from schevo import view

def extentmethod(fn):

    def outer_fn(cls, *args, **kw):
        return fn(cls._extent, *args, **kw)

    if hasattr(fn, '_label'):
        _plural = getattr(fn, '_plural', None)
        decorator = with_label(fn._label, _plural)
        outer_fn = decorator(outer_fn)
    outer_fn = classmethod(outer_fn)
    return outer_fn


class EntityMeta(type):
    """Convert field definitions to a field specification ordered
    dictionary."""
    __module__ = __name__

    def __new__(cls, class_name, bases, class_dict):
        if class_name != 'Entity':
            class_dict['__slots__'] = bases[0].__slots__
        return type.__new__(cls, class_name, bases, class_dict)

    def __init__(cls, class_name, bases, class_dict):
        type.__init__(cls, class_name, bases, class_dict)
        if class_name == 'Entity':
            return
        if '_actual_name' in class_dict:
            class_name = cls._actual_name
            cls.__name__ = class_name
        cls._field_spec = field_spec_from_class(cls, class_dict, slots=True)
        cls.setup_fields()
        spec = field_spec_from_class(cls, class_dict)
        q_spec = spec.copy()
        t_spec = spec.copy()
        v_spec = spec.copy()
        for field_name in cls._fget_fields:
            del q_spec[field_name]
            del t_spec[field_name]

        class _GenericUpdate(transaction.Update):
            __module__ = __name__
            _EntityClass = cls
            _extent_name = class_name
            _fget_fields = cls._fget_fields
            _field_spec = t_spec.copy()

        cls._GenericUpdate = _GenericUpdate
        if not class_name.startswith('_'):
            cls.setup_transactions(class_name, class_dict, t_spec)
            cls.setup_views(class_name, bases, class_dict, v_spec)
        cls._hidden_actions = set(cls._hidden_actions)
        cls._hidden_queries = set(cls._hidden_queries)
        cls._hidden_views = set(cls._hidden_views)
        cls.setup_key_spec()
        cls.setup_index_spec()
        cls.validate_key_and_index_specs()
        if not class_name.startswith('_'):
            cls.assign_labels(class_name, class_dict)
        cls._q_names = cls.get_method_names('q_')
        cls._t_names = cls.get_method_names('t_')
        cls._v_names = cls.get_method_names('v_')
        cls._x_names = cls.get_method_names('x_')
        cls.update_schema(class_name)

    def assign_labels(cls, class_name, class_dict):
        if '_label' not in class_dict and not hasattr(cls, '_label'):
            cls._label = label_from_name(class_name)
        if '_plural' not in class_dict and not hasattr(cls, '_plural'):
            cls._plural = plural_from_name(class_name)
        for key in class_dict:
            if key[:2] in ('q_', 't_', 'v_'):
                m_name = key
                func = getattr(cls, m_name)
                method_name = m_name[2:]
                new_label = None
                if getattr(func, '_label', None) is None:
                    new_label = label_from_name(method_name)
                if func.im_self == cls:
                    if new_label is not None:
                        func.im_func._label = new_label
                elif new_label is not None:
                    class_dict[m_name]._label = new_label

        return

    def get_method_names(cls, prefix):
        """Return list of method names that start with prefix."""
        names = []
        for name in dir(cls):
            if name.startswith(prefix):
                func = getattr(cls, name)
                if func.im_self is None:
                    names.append(name)

        return names

    def setup_fields(cls):
        fget_fields = []
        for (field_name, FieldClass) in cls._field_spec.iteritems():
            fget = FieldClass.fget
            if fget is not None:
                fget_fields.append(field_name)

                def get_field_value(self, fget=fget[0]):
                    return fget(self)

            else:
                field = FieldClass(instance=None)

                def get_field_value(self, field_name=field_name, field=field):
                    """Get the field value from the database."""
                    db = self._db
                    extent_name = self._extent.name
                    oid = self._oid
                    try:
                        value = db._entity_field(extent_name, oid, field_name)
                    except EntityDoesNotExist:
                        raise
                    except KeyError:
                        value = UNASSIGNED

                    field._value = value
                    return field.get()

            setattr(cls, field_name, property(fget=get_field_value))

        cls._fget_fields = tuple(fget_fields)
        return

    def setup_index_spec(cls):
        index_set = set(cls._index_spec)
        for s in cls._index_spec_additions:
            names = tuple((getattr(field_def, 'name', field_def) for field_def in s))
            index_set.add(names)

        cls._index_spec = tuple(index_set)
        cls._index_spec_additions = ()

    def setup_key_spec(cls):
        key_set = set(cls._key_spec)
        for s in cls._key_spec_additions:
            names = tuple((getattr(field_def, 'name', field_def) for field_def in s))
            key_set.add(names)
            if cls._default_key is None:
                cls._default_key = names

        cls._key_spec = tuple(key_set)
        cls._key_spec_additions = ()
        return

    def setup_transactions(cls, class_name, class_dict, t_spec):
        """Create standard transaction classes."""
        for name in ('_Create', '_Delete', '_Update'):
            OldClass = getattr(cls, name)
            NewClass = type(name, (OldClass,), {})
            NewClass._EntityClass = cls
            NewClass._extent_name = class_name
            NewClass._fget_fields = cls._fget_fields
            NewClass._field_spec = t_spec.copy()
            NewClass._field_spec.update(OldClass._field_spec, reorder=True)
            if hasattr(NewClass, '_init_class'):
                NewClass._init_class()
            setattr(cls, name, NewClass)

    def setup_views(cls, class_name, bases, class_dict, v_spec):
        for parent in reversed(bases):
            for (name, attr) in parent.__dict__.iteritems():
                if name not in class_dict and inspect.isclass(attr) and issubclass(attr, base.View):
                    ViewClass = type(name, (attr,), {})
                    ViewClass._label = attr._label
                    setattr(cls, name, ViewClass)

        for (name, attr) in cls.__dict__.iteritems():
            if inspect.isclass(attr) and issubclass(attr, base.View):
                ViewClass = attr
                ViewClass._EntityClass = cls
                ViewClass._extent_name = class_name
                ViewClass._hidden_actions = set(cls._hidden_actions)
                ViewClass._hidden_queries = set(cls._hidden_queries)
                base_spec = ViewClass._field_spec
                ViewClass._fget_fields = cls._fget_fields
                ViewClass._field_spec = v_spec.copy()
                ViewClass._field_spec.update(base_spec, reorder=True)
                if hasattr(ViewClass, '_init_class'):
                    ViewClass._init_class()

    def update_schema(cls, class_name):
        if schevo.namespace.SCHEMADEF is not None and (schevo.namespace.EVOLVING or not cls._evolve_only):
            schevo.namespace.SCHEMADEF.E._set(class_name, cls)
            relationships = schevo.namespace.SCHEMADEF.relationships
            for (field_name, FieldClass) in cls._field_spec.iteritems():
                if hasattr(FieldClass, 'allow') and field_name not in cls._fget_fields:
                    for entity_name in FieldClass.allow:
                        spec = relationships.setdefault(entity_name, [])
                        spec.append((class_name, field_name))

        return

    def validate_key_and_index_specs(cls):
        """Raise a `SchemaError` if there are any shared key/index specs."""
        key_set = set(cls._key_spec)
        index_set = set(cls._index_spec)
        duplicates = key_set.intersection(index_set)
        if len(duplicates):
            raise SchemaError('Cannot use same spec for both key and index.')


class Entity(base.Entity, LabelMixin):
    __module__ = __name__
    __metaclass__ = EntityMeta
    __slots__ = LabelMixin.__slots__ + ['_oid', 'sys', 'f', 'm', 'q', 't', 'v', 'x']
    _actual_name = None
    _db = None
    _default_key = None
    _evolve_only = False
    _extent = None
    _field_spec = FieldSpecMap()
    _hidden = False
    _hidden_actions = set(['create_if_necessary', 'generic_update'])
    _hidden_queries = set([])
    _hidden_views = set()
    _index_spec = ()
    _index_spec_additions = ()
    _initial = []
    _initial_priority = 0
    _key_spec = ()
    _key_spec_additions = ()
    _relationships = []
    _sample = []
    _was = None
    _q_names = []
    _t_names = []
    _v_names = []
    _x_names = []

    def __init__(self, oid):
        self._oid = oid

    def __cmp__(self, other):
        if other is UNASSIGNED:
            return 1
        if other.__class__ is self.__class__:
            if self._default_key:
                key = self._default_key
                return cmp([ getattr(self, fieldname) for fieldname in key ], [ getattr(other, fieldname) for fieldname in key ])
            else:
                return cmp(self._oid, other._oid)
        else:
            return cmp(hash(self), hash(other))

    def __eq__(self, other):
        try:
            return self._extent is other._extent and self._oid == other._oid
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def __getattr__(self, name):
        if name == 'sys':
            self.sys = attr = EntitySys(self)
        elif name == 'f':
            self.f = attr = EntityFields(self)
        elif name == 'm':
            self.m = attr = EntityOneToMany(self)
        elif name == 'q':
            self.q = attr = EntityQueries(self)
        elif name == 't':
            self.t = attr = EntityTransactions(self)
        elif name == 'v':
            self.v = attr = EntityViews(self)
        elif name == 'x':
            self.x = attr = EntityExtenders(self)
        else:
            msg = 'Field %r does not exist on %r.' % (name, self._extent.name)
            raise AttributeError(msg)
        return attr

    def __hash__(self):
        return hash((self._extent, self._oid))

    def __repr__(self):
        oid = self._oid
        extent = self._extent
        if oid not in extent:
            return '<%s entity oid:%i rev:DELETED>' % (extent.name, oid)
        else:
            rev = self._rev
            return '<%s entity oid:%i rev:%i>' % (extent.name, oid, rev)

    def __str__(self):
        return str(unicode(self))

    def __unicode__(self):
        key = self._default_key
        if key:
            return (' :: ').join([ unicode(getattr(self, name)) for name in key ])
        else:
            return repr(self)

    @extentmethod
    @with_label('Exact Matches')
    def q_exact(extent, **kw):
        """Return a simple parameterized query for finding instances
        using the extent's ``find`` method."""
        return query.Exact(extent, **kw)

    @extentmethod
    @with_label('By Example')
    def q_by_example(extent, **kw):
        """Return an extensible query for finding instances, built
        upon Match and Intersection queries."""
        q = query.ByExample(extent, **kw)
        return q

    @classmethod
    @with_label('Create')
    def t_create(cls, *args, **kw):
        """Return a Create transaction."""
        tx = cls._Create(*args, **kw)
        return tx

    @classmethod
    @with_label('Create If Necessary')
    def t_create_if_necessary(cls, *args, **kw):
        """Return a Create transaction that creates if necessary."""
        tx = cls._Create(*args, **kw)
        tx._style = transaction._Create_If_Necessary
        return tx

    @with_label('Delete')
    def t_delete(self):
        """Return a Delete transaction."""
        tx = self._Delete(self)
        return tx

    @with_label('Generic Update')
    def t_generic_update(self, **kw):
        """Return a Generic Update transaction."""
        tx = self._GenericUpdate(self, **kw)
        return tx

    @with_label('Update')
    def t_update(self, **kw):
        """Return an Update transaction."""
        tx = self._Update(self, **kw)
        return tx

    @with_label('View')
    def v_default(self):
        """Return the Default view."""
        return self._DefaultView(self)

    @property
    def _rev(self):
        """Return the revision number of the entity."""
        return self._db._entity_rev(self._extent.name, self._oid)

    class _Create(transaction.Create):
        __module__ = __name__

    class _Delete(transaction.Delete):
        __module__ = __name__

    class _Update(transaction.Update):
        __module__ = __name__

    class _DefaultView(view.View):
        __module__ = __name__
        _label = 'View'


class EntityExtenders(NamespaceExtension):
    """A namespace of entity-level methods."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__

    def __init__(self, entity):
        NamespaceExtension.__init__(self)
        d = self._d
        for x_name in entity._x_names:
            func = getattr(entity, x_name)
            name = x_name[2:]
            d[name] = func


class EntityFields(object):
    __module__ = __name__
    __slots__ = [
     '_entity']

    def __init__(self, entity):
        self._entity = entity

    def __getattr__(self, name):
        e = self._entity
        FieldClass = e._field_spec[name]
        field = FieldClass(e, getattr(e, name))
        return field

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __iter__(self):
        return iter(self._entity._field_spec)

    def _getAttributeNames(self):
        """Return list of hidden attributes to extend introspection."""
        return sorted(iter(self))


class EntityOneToMany(NamespaceExtension):
    """A namespace of entity-level methods."""
    __module__ = __name__

    def __init__(self, entity):
        NamespaceExtension.__init__(self)
        d = self._d
        e = entity
        db = e._db
        extent_name = e._extent.name
        oid = e._oid
        last_extent_name = ''
        for (other_extent_name, other_field_name) in e._extent.relationships:
            if other_extent_name == last_extent_name:
                continue
            last_extent_name = other_extent_name
            many_name = _many_name(db.extent(other_extent_name)._plural)
            many_func = _many_func(db, extent_name, oid, other_extent_name, other_field_name)
            d[many_name] = many_func


def _many_func(db, extent_name, oid, other_extent_name, other_field_name):
    """Return a many function."""
    links = db._entity_links

    def many(other_field_name=other_field_name):
        return links(extent_name, oid, other_extent_name, other_field_name)

    return many


_ALLOWED = digits + ascii_letters + ' '

def _many_name(name):
    """Return a canonical many name."""
    name = ('').join((c for c in name if c in _ALLOWED))
    name = str(name).lower()
    name = name.replace(' ', '_')
    return name


class EntityQueries(NamespaceExtension):
    """A namespace of entity-level queries."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__ + ['_e']

    def __init__(self, entity):
        NamespaceExtension.__init__(self)
        d = self._d
        self._e = entity
        for q_name in entity._q_names:
            func = getattr(entity, q_name)
            name = q_name[2:]
            d[name] = func

    def __contains__(self, name):
        return name in self._d and name not in self._e._hidden_queries

    def __iter__(self):
        return (k for k in self._d.iterkeys() if k not in self._e._hidden_queries)


class EntitySys(NamespaceExtension):
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__ + ['_entity']

    def __init__(self, entity):
        """Create a sys namespace for the `entity`."""
        NamespaceExtension.__init__(self)
        self._entity = entity

    def as_data(self):
        """Return tuple of entity values in a form suitable for
        initial or sample data in a schema."""

        def resolve(entity, fieldname):
            field = entity.f[fieldname]
            value = getattr(entity, fieldname)
            if isinstance(value, Entity):
                entity = value
                values = []
                for fieldname in entity.sys.extent.default_key:
                    value = resolve(entity, fieldname)
                    values.append(value)

                if len(field.allow) > 1:
                    values = (
                     entity.sys.extent.name, tuple(values))
                return tuple(values)
            else:
                return value

        values = []
        create = self._entity.t_create()
        e = self._entity
        for f_name in e.f:
            if f_name not in create.f or create.f[f_name].hidden or create.f[f_name].readonly:
                continue
            f = e.f[f_name]
            if f.fget is not None or f.hidden:
                pass
            else:
                value = resolve(e, f_name)
                values.append(value)

        return tuple(values)

    def count(self, other_extent_name=None, other_field_name=None):
        """Return count of all links, or specific links if
        `other_extent_name` and `other_field_name` are supplied."""
        e = self._entity
        return e._db._entity_links(e._extent.name, e._oid, other_extent_name, other_field_name, return_count=True)

    @property
    def db(self):
        """Return the database to which this entity belongs."""
        return self._entity._db

    @property
    def exists(self):
        """Return True if the entity exists; False if it was deleted."""
        entity = self._entity
        oid = entity._oid
        extent = entity._extent
        return oid in extent

    @property
    def extent(self):
        """Return the extent to which this entity belongs."""
        return self._entity._extent

    @property
    def extent_name(self):
        """Return the name of the extent to which this entity belongs."""
        return self._entity._extent.name

    def field_map(self, *filters):
        """Return field_map for the entity, filtered by optional
        callable objects specified in `filters`."""
        e = self._entity
        stored_values = e._db._entity_fields(e._extent.name, e._oid)
        entity_field_map = e._field_spec.field_map(e, stored_values)
        new_fields = entity_field_map.itervalues()
        for filt in filters:
            new_fields = [ field for field in new_fields if filt(field) ]

        entity_field_map = FieldMap(((field.name, field) for field in new_fields))
        for field in entity_field_map.itervalues():
            if field.fget is not None:
                value = field.fget[0](e)
            else:
                value = field._value
            field._value = field.convert(value)

        return entity_field_map

    def links(self, other_extent_name=None, other_field_name=None):
        """Return dictionary of (extent_name, field_name): entity_list
        pairs, or list of linking entities if `other_extent_name` and
        `other_field_name` are supplied."""
        e = self._entity
        return e._db._entity_links(e._extent.name, e._oid, other_extent_name, other_field_name)

    def links_filter(self, other_extent_name, other_field_name):
        """Return a callable that returns the current list of linking
        entities whenever called."""
        db = self._entity._db
        try:
            extent = db.extent(other_extent_name)
        except KeyError:
            raise ExtentDoesNotExist('%r does not exist.' % other_extent_name)

        if other_field_name not in extent.field_spec:
            raise FieldDoesNotExist('%r does not exist in %r' % (other_field_name, other_extent_name))

        def _filter():
            return self.links(other_extent_name, other_field_name)

        return _filter

    @property
    def oid(self):
        """Return the OID of the entity."""
        return self._entity._oid

    @property
    def rev(self):
        """Return the revision number of the entity."""
        return self._entity._rev


class EntityTransactions(NamespaceExtension):
    """A namespace of entity-level transactions."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__ + ['_e']

    def __init__(self, entity):
        NamespaceExtension.__init__(self)
        d = self._d
        self._e = entity
        for t_name in entity._t_names:
            func = getattr(entity, t_name)
            name = t_name[2:]
            d[name] = func

    def __contains__(self, name):
        return name in self._d and name not in self._e._hidden_actions

    def __iter__(self):
        return (k for k in self._d.iterkeys() if k not in self._e._hidden_actions)


class EntityViews(NamespaceExtension):
    """A namespace of entity-level views."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__ + ['_e']

    def __init__(self, entity):
        NamespaceExtension.__init__(self)
        d = self._d
        self._e = entity
        for v_name in entity._v_names:
            func = getattr(entity, v_name)
            name = v_name[2:]
            d[name] = func

    def __contains__(self, name):
        return name in self._d and name not in self._e._hidden_views

    def __iter__(self):
        return (k for k in self._d.iterkeys() if k not in self._e._hidden_views)


class EntityRef(object):
    """Reference to an Entity via its extent name and OID."""
    __module__ = __name__

    def __init__(self, extent_name, oid):
        """Create an EntityRef instance.

        - `extent_name`: The name of the extent.
        - `oid`: The OID of the entity.
        """
        self.extent_name = extent_name
        self.oid = oid


optimize.bind_all(sys.modules[__name__])