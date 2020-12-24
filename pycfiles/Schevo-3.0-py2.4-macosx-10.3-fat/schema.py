# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/schema.py
# Compiled at: 2007-03-21 14:34:41
"""Schevo schema support.  Allows a declarative syntax and other
helpful shortcuts not directly supported by Python.  Use it by putting
the following lines at the top of your application schema modules.

# All Schevo schema modules must have these lines.
from schevo.schema import *
schevo.schema.prep(locals())

For copyright, license, and warranty, see bottom of file.
"""
__all__ = [
 '_hide', '_key', '_index', 'ANY', 'CASCADE', 'DEFAULT', 'RESTRICT', 'UNASSIGN', 'UNASSIGNED', 'extentmethod', 'schevo', 'with_label']
import os, sys, schevo
from schevo.constant import ANY, CASCADE, DEFAULT, RESTRICT, UNASSIGN, UNASSIGNED
from schevo.label import with_label
import schevo.base, schevo.entity, schevo.error, schevo.field, schevo.label, schevo.namespace, schevo.query, schevo.transaction, schevo.view
from schevo.entity import extentmethod
from schevo.lib import optimize
import inspect, threading
from types import FunctionType, TypeType

def _hide(*args):
    """Append names to list of hidden names."""
    clsLocals = inspect.currentframe(1).f_locals
    hidden_actions = clsLocals.setdefault('_hidden_actions', set(['create_if_necessary', 'generic_update']))
    hidden_queries = clsLocals.setdefault('_hidden_queries', set([]))
    hidden_views = clsLocals.setdefault('_hidden_views', set())
    for name in args:
        if name.startswith('q_'):
            hidden_queries.add(name[2:])
        elif name.startswith('t_'):
            hidden_actions.add(name[2:])
        elif name.startswith('v_'):
            hidden_views.add(name[2:])


def _key(*args):
    """Append a key spec to the Entity subclass currently being
    defined."""
    clsLocals = inspect.currentframe(1).f_locals
    spec = clsLocals.setdefault('_key_spec_additions', [])
    spec.append(args)


def _index(*args):
    """Append an index spec to the Entity subclass currently being
    defined."""
    clsLocals = inspect.currentframe(1).f_locals
    spec = clsLocals.setdefault('_index_spec_additions', [])
    spec.append(args)


import_lock = threading.Lock()

def start(db=None, evolving=False):
    """Lock schema importing."""
    import_lock.acquire()
    schevo.namespace.SCHEMADB = db
    schevo.namespace.EVOLVING = evolving
    if db:
        db._imported_schemata = {}


def prep(schema_namespace):
    """Add syntax support magic to the schema namespace."""
    schevo.namespace.SCHEMADEF = schevo.namespace.SchemaDefinition()
    schema_def = schevo.namespace.SCHEMADEF
    schema_def.E.Entity = schevo.entity.Entity
    for (k, v) in schevo.query.__dict__.items():
        if inspect.isclass(v) and issubclass(v, schevo.query.Query):
            schema_def.Q._set(k, v)

    for (k, v) in schevo.transaction.__dict__.items():
        if inspect.isclass(v) and issubclass(v, schevo.transaction.Transaction):
            schema_def.T._set(k, v)

    for (k, v) in schevo.view.__dict__.items():
        if inspect.isclass(v) and issubclass(v, schevo.view.View):
            schema_def.V._set(k, v)

    _field_info_extract(schevo.field)
    schema_namespace['d'] = schema_def
    schema_namespace['E'] = schema_def.E
    schema_namespace['F'] = schema_def.F
    schema_namespace['f'] = schema_def.f
    schema_namespace['Q'] = schema_def.Q
    schema_namespace['T'] = schema_def.T
    schema_namespace['V'] = schema_def.V
    schema_namespace['db'] = _null_db


def finish(db, schema_module=None):
    """Unlock the schema import mutex and return the schema definition."""
    if schema_module is None:
        import_lock.release()
        return
    schema_def = schevo.namespace.SCHEMADEF
    schevo.namespace.SCHEMADEF = None
    schevo.namespace.SCHEMADB = None
    schevo.namespace.EVOLVING = False
    del schema_def.E.Entity
    for entity_name in schema_def.E:
        EntityClass = schema_def.E[entity_name]
        for FieldClass in EntityClass._field_spec.itervalues():
            FieldClass.readonly = True

    for (parent, spec) in schema_def.relationships.iteritems():
        E = schema_def.E
        parentClass = getattr(E, parent, None)
        if parentClass is None:
            raise schevo.error.ExtentDoesNotExist(parent)
        other_map = {}
        for (other_extent_name, other_field_name) in spec:
            other_extent_field_set = other_map.setdefault(other_extent_name, set())
            other_extent_field_set.add(other_field_name)

        spec = []
        for (other_extent_name, other_extent_field_set) in other_map.items():
            other_class = getattr(E, other_extent_name)
            spec.extend(((other_extent_name, other_field_name) for other_field_name in other_class._field_spec if other_field_name in other_extent_field_set))

        parentClass._relationships = spec

    del schema_def.relationships
    q = schema_def.q
    for (name, func) in schema_module.__dict__.iteritems():
        if isinstance(func, FunctionType) and name.startswith('q_'):
            name = name[2:]
            if getattr(func, '_label', None) is None:
                func._label = schevo.label.label_from_name(name)
            q._set(name, func)

    t = schema_def.t
    for (name, func) in schema_module.__dict__.iteritems():
        if isinstance(func, FunctionType) and name.startswith('t_'):
            name = name[2:]
            if getattr(func, '_label', None) is None:
                func._label = schevo.label.label_from_name(name)
            t._set(name, func)

    del schema_module.db
    optimize.bind_all(schema_module)
    schema_module.db = db
    import_lock.release()
    return schema_def


def _field_info_extract(module):
    """Extract field stuff to add to the schema definition namespace."""
    F_set = schevo.namespace.SCHEMADEF.F._set
    f_set = schevo.namespace.SCHEMADEF.f._set
    for FieldClass in module.__dict__.values():
        if isinstance(FieldClass, TypeType) and issubclass(FieldClass, schevo.field.Field):
            F_set(FieldClass.__name__, FieldClass)
            f_set(FieldClass._def_name, FieldClass._def_class)


class _NullDatabase(object):
    """A dummy object to serve as the global 'db' var during schema
    loading."""
    __module__ = __name__

    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kw):
        return self


_null_db = _NullDatabase()

def name(version):
    """Return canonical name for schema version."""
    return 'schema_%03i' % version


def path(location):
    """If location is a module or package, return its path; otherwise,
    return location."""
    from_list = location.split('.')[:1]
    try:
        pkg = __import__(location, {}, {}, from_list)
    except ImportError:
        return location

    return os.path.dirname(pkg.__file__)


def read(location, version):
    """Return text contents of the schema file version at location."""
    schema_path = path(location)
    schema_filename = name(version) + '.py'
    schema_filepath = os.path.join(schema_path, schema_filename)
    try:
        schema_file = file(schema_filepath, 'rU')
        schema_source = schema_file.read()
    except IOError:
        raise schevo.error.SchemaFileIOError('Could not open schema file %r' % schema_filepath)

    schema_file.close()
    return schema_source