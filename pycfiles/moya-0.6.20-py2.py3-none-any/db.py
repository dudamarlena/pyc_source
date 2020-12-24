# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/db.py
# Compiled at: 2017-09-06 16:09:30
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from ..elements.elementbase import ElementBase, Attribute
from .. import logic
from .. import errors
from ..db import wrap_db_errors, dbobject
from .. import interface
from ..context import Context
from ..logic import DeferNodeContents, SkipNext
from ..tags import dbcolumns
from ..tags.dbcolumns import no_default
from ..tags.context import DataSetter, ContextElementBase
from ..elements.boundelement import BoundElement
from ..console import make_table_header, Cell
from .. import namespaces
from ..context.expressiontime import ExpressionDateTime
from ..context.missing import is_missing
from ..containers import OrderedDict
from ..dbexpression import DBExpression
from ..template.rendercontainer import RenderContainer
from .. import timezone
from .. import http
from ..compat import PY2, text_type, implements_bool, implements_to_string, iteritems, py2bytes, xrange, number_types, string
from .. import pilot
from json import loads
from collections import namedtuple
from random import choice
import uuid
from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, DateTime, desc, UniqueConstraint
from sqlalchemy.sql import text
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound, UnmappedInstanceError
from sqlalchemy.exc import ArgumentError, IntegrityError, OperationalError
from sqlalchemy.engine import RowProxy, ResultProxy
from sqlalchemy import event
import weakref, logging
log = logging.getLogger(b'moya.db')
ExtendedDefinition = namedtuple(b'ExtendedDefinition', [b'columns',
 b'properties',
 b'object_properties',
 b'constraints'])

class AdaptValueError(ValueError):

    def __init__(self, msg, k, v):
        super(AdaptValueError, self).__init__(msg)
        self.k = k
        self.v = v


@implements_to_string
class DBValidationError(Exception):

    def __init__(self, msg, diagnosis=None):
        self.msg = msg
        self.diagnosis = diagnosis

    def __str__(self):
        return self.msg


class DBMixin(object):

    def get_model(self, context, model, app):
        try:
            model_app, model = self.get_app_element(model, app=app)
        except errors.ElementNotFoundError as e:
            raise errors.ElementError(text_type(e), element=self)

        return (
         model_app, model)

    def get_session(self, context, db=None):
        if db is None:
            db = self.db(context)
        dbsessions = context.get(b'._dbsessions', None)
        if dbsessions is None:
            raise logic.MoyaException(b'db.no-session', b'unable to get database session', diagnosis=b'Have you initialized a database in settings?')
        try:
            session = dbsessions[db]
        except KeyError:
            if db == b'_default':
                raise logic.MoyaException(b'db.missing-db', (b'No database defined').format(db))
            else:
                raise logic.MoyaException(b'db.missing-db', (b"No database called '{}'").format(db))
        else:
            return session

        return


@implements_bool
class MoyaQuerySet(interface.AttributeExposer):
    """Context interface for an sqlalchemy query set"""
    __moya_exposed_attributes__ = [
     b'sql',
     b'first',
     b'last',
     b'list',
     b'count',
     b'exists']

    def __init__(self, qs, table_class, session):
        self._qs = qs
        self.table_class = table_class
        self.dbsession = session
        self._count = None
        return

    def __repr__(self):
        if self.table_class:
            return (b'<queryset {!r}>').format(self.table_class._model)
        else:
            return b'<queryset>'

    def _get_query_set(self):
        return self._qs

    @wrap_db_errors
    def __iter__(self):
        return iter(self._qs)

    @wrap_db_errors
    def __len__(self):
        return self.count

    @property
    def sql(self):
        return text_type(self._qs.statement)

    @wrap_db_errors
    def slice(self, start, stop, step=None):
        if step is not None:
            raise logic.MoyaException(b'db.slice-error', b'Querysets do not support slicing with a step')
        if start < 0 or stop < 0:
            raise logic.MoyaException(b'db.slice-error', b'Querysets do not support negative indexing')
        return MoyaQuerySet(self._qs.slice(start, stop), self.table_class, self.dbsession)

    @wrap_db_errors
    def __bool__(self):
        return self._qs.first() is not None

    @property
    def first(self):
        return self._qs.first()

    @property
    def last(self):
        """Get the last item in the qs"""
        last = self.count - 1
        return self._qs[(last - 1)]

    @property
    def list(self):
        return list(self._qs)

    @property
    def count(self):
        if self._count is None:
            self._count = self._qs.count()
        return self._count

    @property
    def exists(self):
        return self._qs.first() is not None

    def in_(self, context, b):
        return self.table_class.id.in_(b)

    def notin_(self, context, b):
        return self.table_class.id.notin_(b)

    def __add__(self, rhs):
        if isinstance(rhs, MoyaQuerySet):
            union_qs = self._qs.order_by(None).union(rhs._qs.order_by(None))
            return MoyaQuerySet(union_qs, self.table_class, self.dbsession)
        else:
            raise TypeError(b'Can only add query sets to query sets')
            return


class DBElement(ElementBase):
    xmlns = namespaces.db


def make_table_class(model, name, columns, app, table):
    attributes = {b'_model': model, 
       b'_app': app, 
       b'_moyadb': MoyaDB(model, columns, app), 
       b'_table': table}
    cls = type(py2bytes(name), (
     TableClassBase,), attributes)
    return cls


class TableClassBase(object):
    """The base class for dynamically created classes that map on to DB abstractions"""
    moya_render_targets = [
     b'html']

    def __init__(self, **kwargs):
        moyadb = self._moyadb
        adapt = moyadb.adapt
        for k, v in iteritems(kwargs):
            try:
                setattr(self, k, adapt(k, v))
            except Exception as e:
                raise AdaptValueError((b"unable to adapt field '{}' to {}").format(k, v), k, v)

        for k, v in moyadb.defaults.items():
            if k not in kwargs and k + b'_id' not in kwargs:
                setattr(self, k, v() if callable(v) else v)

        super(TableClassBase, self).__init__()

    @classmethod
    def get_defaults(cls):
        """Get a mapping of defaults for this db class"""
        moyadb = cls._moyadb
        defaults = {}
        for k, v in moyadb.defaults.items():
            if not callable(v):
                defaults[k] = v

        return defaults

    @classmethod
    def _get_column(cls, column_name, default=None):
        return cls._moyadb.moya_columns_map.get(column_name, default)

    @classmethod
    def _get_index(self, archive, context, app, exp_context, index):
        index = index[:]
        node = self
        joins = []
        while index:
            attribute_name = index.pop(0)
            if not index:
                node = getattr(node, attribute_name)
            elif issubclass(node, TableClassBase):
                col = node._get_column(attribute_name)
                if col is None:
                    raise KeyError(attribute_name)
                node, join = col.get_join(node)
                if join is not None:
                    joins.append(join)
            else:
                raise ValueError(b'get index fail')

        if joins:
            exp_context.add_joins(joins)
        return dbobject(node)

    def __moyaconsole__(self, console):
        moyadb = self._moyadb
        table = make_table_header(b'field name', b'value')
        table_body = [ (field.name, pilot.context.to_expr(getattr(self, field.name))) for field in moyadb.moya_columns
                     ]
        table += table_body
        console.table(table)

    def __iter__(self):
        raise NotImplementedError(b'not iterable')

    def moya_render(self, archive, context, target, options):
        if target != b'html':
            return repr(self)
        else:
            template = self._model.template(context)
            if template is None:
                return self.__moyarepr__(context)
            template = self._app.resolve_template(template)
            render_container = RenderContainer.create(self._app, template=template)
            render_container[b'self'] = self
            if b'with' in options:
                render_container.update(options[b'with'])
            return render_container.moya_render(archive, context, target, options)

    def __getitem__(self, key):
        """Allow context to return proxy for datetime"""
        try:
            value = getattr(self, key)
        except AttributeError:
            raise KeyError(key)
        else:
            try:
                if isinstance(value, list):
                    value._instance = self
                rel = self._model.relationships.get(key, None)
            except Exception as e:
                pass

            if isinstance(value, datetime):
                return ExpressionDateTime.from_datetime(value)
            return value

        return

    def __setitem__(self, key, value):
        try:
            setattr(self, key, dbobject(value))
        except:
            raise ValueError((b"invalid data type for attribute '{}'").format(key))

        return self

    def keys(self):
        return [ name for name in self._moyadb.dbfields ]

    def values(self):
        return [ getattr(self, name) for name in self._moyadb.dbfields ]

    def items(self):
        return [ (name, getattr(self, name)) for name in self._moyadb.dbfields ]

    def map(self):
        return {name:getattr(self, name) for name in self._moyadb.dbfields}

    def __contains__(self, key):
        return any(key == name for name in self._moyadb.dbfields)

    if PY2:

        def __unicode__(self):
            return self.__moyarepr__(pilot.context)

    else:

        def __str__(self):
            return self.__moyarepr__(pilot.context)

    def __moyarepr__(self, context):
        """Generated from the `repr` attribute, or uses default of '<model> <id>'."""
        r = self._repr
        try:
            with context.data_scope(self):
                return (b'<{}>').format(pilot.context.sub(r))
        except Exception as e:
            log.error(b'error with repr: %s', e)
            try:
                return (b'<{} #{}>').format(self._model.get_appid(self._app), self.id)
            except:
                log.exception(b'error in default repr')
                return b'<error in repr>'


class MoyaDB(object):

    def __init__(self, model, columns, app):
        columns = [ col(app, model) if callable(col) else col for col in columns ]
        self.moya_columns = columns
        self.moya_columns_map = dict((col.name, col) for col in columns)
        sa_columns = sum((list(col.get_sa_columns(model)) for col in columns), [])
        self.sa_columns = dict((col.name, col) for col in sa_columns)
        self.dbfields = sorted(col.name for col in columns)
        self.attrib_set = set(self.dbfields)
        self.defaults = {col.name:col.default for col in columns if col.default is not no_default if col.default is not no_default}

    def adapt(self, field, value):
        if value is None:
            return value
        else:
            if field not in self.sa_columns:
                return value
            col = self.sa_columns[field]
            if isinstance(col.type, DateTime):
                if hasattr(value, b'__datetime__'):
                    value = value.__datetime__()
                elif isinstance(value, (list, tuple)):
                    value = ExpressionDateTime(*value)
            elif field in self.moya_columns_map:
                value = self.moya_columns_map[field].adapt(value)
            return value


class ModelProxy(object):

    def __init__(self, model, app):
        super(ModelProxy, self).__init__()
        self._model = model
        self.name = model.name
        self.title = model.title
        self.ref = app.qualify_ref(model.ref)
        self.app = app
        columns = self.columns = []
        for def_app, ext in model._get_extended_definition(app):
            columns.extend((col(app, model) if callable(col) else col) for col in ext.columns)

        self.relationships = model.relationships.values()

    def __repr__(self):
        return (b'<model {} {}>').format(self._model.get_appid(self.app), self._model.name)

    def __moyamodel__(self):
        return (
         self.app, self._model)

    def __moyaconsole__(self, console):
        console.text(repr(self), fg=b'magenta', bold=True)
        console.text(b'[columns]', fg=b'green', bold=True)
        table = [
         [
          Cell(b'Name', bold=True),
          Cell(b'Type', bold=True),
          Cell(b'DB name', bold=True)]]
        for column in self.columns:
            table.append([column.name,
             column.type,
             column.dbname])

        console.table(table, header=True)
        console.text(b'[relationships]', fg=b'green', bold=True)
        table = [
         [
          Cell(b'Name', bold=True),
          Cell(b'Type', bold=True)]]
        for rel in self.relationships:
            table.append([rel.name,
             rel.type])

        console.table(table, header=True)


class RelationshipProxy(object):

    def __init__(self, type, name, params, ref_model, widget=None, picker=None):
        for k, v in params.items():
            setattr(self, k, v)

        self.type = type
        self.name = name
        self.ref_model = BoundElement.from_tuple(ref_model)
        if b'widget' not in params:
            self.widget = widget
        self.picker = picker or params.get(b'picker', None)
        return

    def __repr__(self):
        return (b'<{} {}>').format(self.type, self.name)


class Doc(DBElement):
    """
    Document a model.

    """

    class Help:
        synopsis = b'document a DB model'


class DBModel(DBElement):
    """
    Defines a database [i]model[/i], which maps data stored in a database table on to Moya objects.

    Models are referenced by their [i]libname[/i] in database expressions, the [c]name[/c] attribute is used when creating tables. If you convert a model instance to a string, it will return the value of the [c]repr[/c] attribute, with substitutions made with the object context.

    """

    class Help:
        synopsis = b'define a database model'
        example = b'\n        <model name="Permission" libname="Permission" xmlns="http://moyaproject.com/db"\n            repr="Permission \'${name}\' ${description}">\n            <string name="name" required="yes" null="no" blank="no" length="30" unique="yes"/>\n            <text name="description" null="no" default=""/>\n        </model>\n\n        '

    _name = Attribute(b'Name of the model (used internally by the db)', required=False, map_to=b'name')
    _db = Attribute(b'Database to use (default will use the default database)', map_to=b'db', default=None)
    _repr = Attribute(b'Text representation of a model instance (substitution will use the model as a data context)', type=b'raw', map_to=b'repr', default=None)
    _abstract = Attribute(b'Is the model abstract?', type=b'boolean', default=False, map_to=b'abstract')
    extends = Attribute(b'Extend this model', type=b'elementref', default=None)
    title = Attribute(b'Descriptive title', type=b'text', default=None)
    template = Attribute(b'Optional template to render object', default=None)
    preserve_attributes = [
     b'columns',
     b'column_names',
     b'properties',
     b'object_properties',
     b'constraints',
     b'name',
     b'dbname',
     b'table_map',
     b'_repr']

    class Meta:
        tag_name = b'model'

    def get_db(self):
        db = self.archive.database_engines.get(self.dbname, None)
        return db

    def post_build(self, context):
        self.table_map = {}
        self.columns = []
        self.properties = []
        self.object_properties = []
        self.constraints = []
        self.relationships = OrderedDict()
        self._extended_definitions = {}
        self.references = []
        if b'libname' not in self._attrs:
            raise errors.ElementError(b"a 'libname' attribute is required on this tag", element=self)
        name, db, _repr, abstract, title = self.get_parameters(context, b'name', b'db', b'repr', b'abstract', b'title')
        if name is None:
            name = self.libname.lower()
        self.ref = self.document.qualify_element_ref(self.libid)
        if _repr is None:
            _repr = name + b' #${id}'
        self.name = name
        self.title = title or name.title()
        self.abstract = abstract
        self.dbname = db or self.archive.default_db_engine
        self._repr = _repr
        self.columns.append(dbcolumns.PKColumn(self.tag_name, b'id', primary=True))
        super(DBModel, self).post_build(context)
        self._built_model = False
        return

    def add_column(self, name, column):
        self.columns.append(column)

    def add_property(self, name, prop):
        self.properties.append((name, prop))

    def add_relationship(self, tag_name, name, params, ref_model, widget=None, picker=None):
        rel = RelationshipProxy(tag_name, name, params, ref_model, widget=widget, picker=picker)
        self.relationships[name] = rel

    def add_object_property(self, name, prop):
        self.object_properties.append((name, prop))

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def add_reference(self, ref):
        self.references.append(ref)

    def validate(self, app):
        validate_fails = []
        for element in self:
            if hasattr(element, b'validate'):
                try:
                    element.validate(app, self)
                except Exception as e:
                    validate_fails.append((self, app, element, e))

        return validate_fails

    @classmethod
    def validate_all(cls, archive):
        validate_fails = []
        archive.build_libs()
        apps = archive.apps.values()
        for app in apps:
            for model in app.lib.get_elements_by_type((namespaces.db, b'model')):
                try:
                    model._build_model(app)
                except Exception as e:
                    raise
                    if hasattr(e, b'element'):
                        validate_fails.append([model, app, e.element, text_type(e)])
                    else:
                        validate_fails.append([model, app, None, text_type(e)])

        for app in apps:
            for model in app.lib.get_elements_by_type((namespaces.db, b'model')):
                validate_fails.extend(model.validate(app))

        return validate_fails

    @property
    def metadata(self):
        return self.get_db().metadata

    def get_table_and_class(self, app):
        app_name = self.get_table_name(app)
        if app_name not in self.table_map:
            self._build_model(app)
        return self.table_map[app_name]

    def get_table_class(self, app):
        table, table_class = self.get_table_and_class(app)
        return table_class

    def get_table(self, app):
        table, table_class = self.get_table_and_class(app)
        return table

    def get_table_name(self, app):
        for app, _ in self._get_extended_definition(app):
            break

        return b'%s_%s' % (app.name.lower(), self.name.lower())

    def make_association_table(self, left_model_table_name, right_model_table_name):
        left = left_model_table_name
        right = right_model_table_name
        name = b'%s_to_%s' % (left, right)
        sa_columns = [
         Column(b'left_id', Integer, ForeignKey(b'%s.id' % left, ondelete=b'CASCADE'), nullable=False),
         Column(b'right_id', Integer, ForeignKey(b'%s.id' % right, ondelete=b'CASCADE'), nullable=False)]
        table = Table(name, self.metadata, *sa_columns)
        return table

    def _get_extended_definition(self, app):
        _app = app
        if app.name in self._extended_definitions:
            return self._extended_definitions[app.name]
        else:
            model = self
            extends_chain = [(app, self)]
            context = Context(name=b'_get_extended_definition')
            while 1:
                extend_model_ref = model.extends(context)
                if extend_model_ref is None:
                    break
                app, extend_model = self.document.get_app_element(extend_model_ref, app=app)
                if (
                 app, extend_model) in extends_chain:
                    raise errors.StartupFailedError((b'recursive extends in {!r}, {!r} previously included').format(self, extend_model))
                extends_chain.append((app, extend_model))
                model = extend_model

            definitions = []
            for app, model in reversed(extends_chain):
                definition = ExtendedDefinition(model.columns, model.properties, model.object_properties, model.constraints)
                definitions.append((app, definition))

            self._extended_definitions[_app.name] = definitions
            return definitions

    def _build_model(self, app):
        if self.abstract:
            return
        else:
            if self.get_db() is None:
                raise errors.StartupFailedError((b"can't build model for {}; no database defined").format(self.libid))
            app_name = self.get_table_name(app)
            if app_name in self.table_map:
                return
            table_name = self.get_table_name(app)
            table_names = self.get_db().table_names
            if table_name in table_names:
                raise errors.StartupFailedError((b"can't build model for {}; duplicate table name '{}'").format(self.libid, table_name))
            table_names.add(table_name)
            app_columns = []
            columns = []
            sa_columns = []
            definitions = self._get_extended_definition(app)
            names = set()
            for definition_app, ext in definitions:
                columns = [ (definition_app, col(app, self) if callable(col) else col) for col in ext.columns ]
                columns = [ (_, c) for _, c in columns if c.name not in names ]
                names.update(c.name for _, c in columns)
                app_columns.extend(columns)

            columns = [ col for _, col in app_columns ]
            sa_columns = sum((list(col.get_sa_columns(self)) for col in columns), [])
            for definition_app, ext in definitions:
                sa_columns += ext.constraints

            table = Table(table_name, self.metadata, *sa_columns)
            table_class = make_table_class(self, self.name, columns, app, table)
            table_class._repr = self._repr
            self.table_map[app_name] = (
             table, table_class)
            properties_map = {}
            for definition_app, col in app_columns:
                for name, prop in col.get_properties(self, table_class):
                    if callable(prop):
                        prop = prop(definition_app, self)
                    properties_map[name] = prop

            for definition_app, ext in definitions:
                for name, prop in ext.properties:
                    if callable(prop):
                        prop = prop(definition_app, self)
                    properties_map[name] = prop

            for definition_app, ext in definitions:
                for k, v in ext.object_properties:
                    _prop = property(v(definition_app, self) if callable(v) else v)
                    setattr(table_class, k, _prop)

            mapper(table_class, table, properties=properties_map)

            def make_listener(event):
                return lambda mapper, connection, target: self.event_listener(event, app, target)

            event.listen(table_class, b'before_insert', make_listener(b'db.pre-insert'))
            event.listen(table_class, b'after_insert', make_listener(b'db.post-insert'))
            event.listen(table_class, b'before_update', make_listener(b'db.pre-update'))
            event.listen(table_class, b'after_update', make_listener(b'db.post-update'))
            event.listen(table_class, b'before_delete', make_listener(b'db.pre-delete'))
            event.listen(table_class, b'after_delete', make_listener(b'db.post-delete'))
            return

    def create_all(self, archive, engine, app):
        self.metadata.create_all(engine.engine)

    def event_listener(self, event, app, _object):
        if _object is None:
            return
        else:
            signal_params = {b'object': _object, 
               b'app': app, 
               b'model': self.libid}
            self.archive.fire(pilot.context, event, app, self.libid, signal_params)
            return


class _PropertyCallable(object):

    def __init__(self, element, name, expression, cache=False):
        self._element = weakref.ref(element)
        self._name = name
        self._expression = expression
        self._cache = cache

    def __call__(self, app, model):
        if self._expression is not None:
            expression = self._expression

            def expression_property(obj):
                return expression.call(pilot.context, obj)

            _property = expression_property
        else:

            def moya_code_property(obj):
                element = self._element()
                _call = element.archive.get_callable_from_element(element, app=app)
                result = _call(pilot.context, object=obj)
                return result

            _property = moya_code_property
        if self._cache:

            def cache_property(obj):
                try:
                    return getattr(obj, b'_prop_cache_' + self._name)
                except AttributeError:
                    result = _property(obj)
                    setattr(obj, b'_prop_cache_' + self._name, result)
                    return result

            return cache_property
        else:
            return _property


class Property(DBElement):
    """Add a property to a db object"""

    class Help:
        synopsis = b'add a property to a database object'

    class Meta:
        is_call = True

    _name = Attribute(b'Property name', required=True)
    expression = Attribute(b'expression using database object', type=b'function', default=None)
    cache = Attribute(b'cache result on object?', type=b'boolean', default=False)

    def document_finalize(self, context):
        params = self.get_parameters(context)
        model = self.get_ancestor((self.xmlns, b'model'))
        expression = params.expression if self.has_parameter(b'expression') else None
        model.add_object_property(params.name, _PropertyCallable(self, params.name, expression, cache=params.cache))
        return


class _ForeignKey(DBElement):
    """Add a [i]foreign key[/i] to a model. A foreign key is a reference to another table.

    A [tag]foreign-key[/tag] tag must appear within a [tag]model[/tag] tag.
    """

    class Help:
        synopsis = b'a key to another model'
        example = b'\n        <!-- foreign key to a User model, called "user", must not be NULL -->\n        <foreign-key model="#User" name="user" null="no"/>\n        '

    _name = Attribute(b'Name of the foreign key in the model', required=True)
    model = Attribute(b'Model element reference', required=True)
    null = Attribute(b'Allow Null?', type=b'boolean', default=True)
    blank = Attribute(b'Allow empty field in Moya admin?', type=b'boolean')
    default = Attribute(b'Default value if not set explicitly', default=None)
    primary = Attribute(b'Primary key?', type=b'boolean', default=False)
    index = Attribute(b'Generate a db index?', type=b'boolean', default=False)
    options = Attribute(b'Objects to consider in admin forms', type=b'dbexpression', required=False, default=None)
    orderby = Attribute(b'Default order for admin forms', required=False, default=b'id')
    label = Attribute(b'Short description of field purpose')
    help = Attribute(b'Additional help text for use in object forms')
    backref = Attribute(b'Back reference', required=False, default=None)
    picker = Attribute(b'Picker table for admin view', required=False)
    owner = Attribute(b'Does this model own the referenced object?', type=b'boolean', default=False)
    owned = Attribute(b'Is this model owned by the referenced model?', type=b'boolean', default=False)

    def document_finalize(self, context):
        params = self.get_parameters_nonlazy(context)
        self.name = name = params.name
        model = self.get_ancestor((self.xmlns, b'model'))
        ref_model_ref = params.model

        def get_backref_collection(app, model, name):

            class ListCollection(list):

                def __repr__(self):
                    return (b'<ListCollection {}>').format(self._instance)

                @property
                def table_class(self):
                    return model.get_table_class(app)

                def __moyaqs__(self, context, dbsession):
                    qs = dbsession.query(self.table_class)
                    qs = qs.filter(getattr(self.table_class, name + b'_id') == getattr(self._instance, b'id'))
                    return qs

                def _get_query_set(self):
                    return [ getattr(i, b'id') for i in self if hasattr(i, b'id') ]

            return ListCollection

        def get_col(app, model):
            try:
                ref_model = self.document.get_app_element(ref_model_ref, app)
            except errors.ElementNotFoundError as e:
                raise errors.ElementError(text_type(e), element=self)

            default = no_default if self.has_parameter(b'default') else params.default
            ondelete = b'CASCADE' if not params.null else b'SET NULL'
            cascade = b'save-update, merge'
            back_cascade = b'save-update, merge'
            if params.owned:
                back_cascade = b'all, delete'
            if params.owner:
                cascade = b'all, delete'
                ondelete = b'CASCADE'
            col = dbcolumns.ForeignKeyColumn(self.tag_name, name, ref_model.element, ref_model.app, label=params.label, help=params.help, default=default, null=params.null, blank=params.blank, primary=params.primary, index=params.index, ondelete=ondelete, options=params.options, orderby=params.orderby, backref=params.backref, picker=params.picker, cascade=cascade, back_cascade=back_cascade, uselist=True, backref_collection=get_backref_collection(app, model, name))
            ref_model.element.add_reference(model.libid)
            return col

        self.dbname = name + b'_id'
        model.add_column(params.name, get_col)


class OneToOne(_ForeignKey):
    """
    A [i]one to one[/i] is a foreign key, that create a single reference to the other model.
    This is reflected in the remote side which has a reference to the linked object, rather than a collection."""

    class Help:
        synopsis = b'create a one to one relationship'

    def document_finalize(self, context):
        params = self.get_parameters_nonlazy(context)
        del context
        self.name = name = params.name
        self.model = model = self.get_ancestor((self.xmlns, b'model'))
        ref_model_ref = params.model

        def get_col(app, model):
            try:
                ref_model = self.document.get_app_element(ref_model_ref, app)
            except errors.ElementNotFoundError as e:
                raise errors.ElementError(text_type(e), element=self)

            default = no_default if self.has_parameter(b'default') else params.default
            ondelete = b'CASCADE' if not params.null else b'SET NULL'
            cascade = b'save-update, merge'
            back_cascade = b'save-update, merge'
            if params.owned:
                back_cascade = b'all, delete-orphan'
            if params.owner:
                cascade = b'all, delete'
                ondelete = b'CASCADE'
            col = dbcolumns.ForeignKeyColumn(self.tag_name, name, ref_model.element, ref_model.app, label=params.label, help=params.help, default=default, null=params.null, blank=params.blank, primary=params.primary, index=params.index, ondelete=ondelete, options=params.options, orderby=params.orderby, backref=params.backref, picker=params.picker, cascade=cascade, back_cascade=back_cascade, uselist=False)
            ref_model.element.add_reference(model.libid)
            return col

        self.dbname = name + b'_id'
        model.add_column(params.name, get_col)


class Relationship(DBElement):
    """Defines a relationship between two tables."""

    class Help:
        synopsis = b'define a model relationship that creates a collection'
        example = b'<relationship name="links" model="#Link" orderby="-hotness"/>'

    _name = Attribute(b'Name of the relationship', required=True)
    model = Attribute(b'Model', required=True)
    backref = Attribute(b'Backref')
    orderby = Attribute(b'Order by', type=b'commalist', required=False, default=('id', ))
    search = Attribute(b'DB query referencing search field q', type=b'dbexpression', required=False, default=None)
    picker = Attribute(b'Picker table for admin view', required=False)

    def validate(self, app, model):
        try:
            ref_model = self.document.get_app_element(self.ref_model_ref, app)
        except errors.ElementNotFoundError as e:
            raise errors.ElementError(text_type(e), element=self)

        model = self.get_ancestor((self.xmlns, b'model'))
        if not isinstance(ref_model.element, DBModel):
            raise DBValidationError((b"reference '{}' is not a model").format(self.ref_model_ref))
        ref_libid = ref_model.element.libid
        if ref_libid not in model.references:
            msg = b"Referenced model '{ref_libid}' should contain a foreignkey to '{libid}'"
            diagnosis = b'Add a <foreignkey> to the model referenced by \'{ref_libid}\', with attribute model="{libid}"'
            raise DBValidationError(msg.format(ref_libid=ref_libid, libid=model.libid), diagnosis=diagnosis.format(ref_libid=ref_libid, libid=model.libid))

    def document_finalize(self, context):
        params = self.get_parameters_nonlazy(context)
        model = self.get_ancestor((self.xmlns, b'model'))
        orderby = self.orderby(context)

        def make_relationship(app, model):
            try:
                app, ref_model = self.document.get_app_element(params.model, app=app)
            except errors.ElementNotFoundError as e:
                raise errors.ElementError(text_type(e), element=self)

            self.ref_model_ref = ref_model.libid
            ref_table, ref_table_class = ref_model.get_table_and_class(app)
            order = lambda : Query._get_order(self.archive, context, ref_table_class, orderby, reverse=False, app=app)
            model.add_relationship(self.tag_name, params.name, params._get_param_dict(), (
             app, ref_model))
            return relationship(ref_table_class, order_by=order)

        model.add_property(params.name, make_relationship)


def check_collection_target(collection, obj):
    if hasattr(collection, b'__check_type__'):
        return collection.__check_type__(obj)
    return True


class ManyToMany(DBElement, DBMixin):

    class Help:
        synopsis = b'define a many to may relationship'
        example = b'<many-to-many name="following" backref="followers" model="moya.auth#User"/>'

    _name = Attribute(b'Name of the relationship', required=True)
    model = Attribute(b'Model', required=True)
    backref = Attribute(b'Back reference', required=False, default=None)
    through = Attribute(b'Through model', required=False, default=None)
    options = Attribute(b'Objects to consider in admin forms', type=b'dbexpression', required=False, default=None)
    search = Attribute(b'DB query referencing search field q', type=b'dbexpression', required=False, default=None)
    orderby = Attribute(b'Default order for admin forms', required=False, default=b'id')
    keys = Attribute(b'Foreign keys in association table', required=False, type=b'commalist', map_to=b'_keys')
    lazy = Attribute(b'Specifies how related items should be loaded', required=False)
    label = Attribute(b'Short description of field purpose')
    backlabel = Attribute(b'Short description of backref purpose, if used', required=False, default=None)
    help = Attribute(b'Additional help text for use in object forms')
    picker = Attribute(b'Admin table to use as a picker control', type=b'elementref', required=False, default=None)
    backpicker = Attribute(b'Admin table to use as a picker control for the other side of the relationship', type=b'elementref', required=False, default=None)

    def validate(self, app, model):
        pass

    def document_finalize(self, context):
        params = self.get_parameters_nonlazy(context)
        model = self.get_ancestor((self.xmlns, b'model'))
        self.ref_model_ref = ref_model_ref = params.model
        backref_name = params.backref
        backlabel = params.backlabel
        self.through = through = params.through
        foreign_keys = params._keys

        def get_property(app, model):
            try:
                ref_model = self.document.get_app_element(ref_model_ref, app)
            except errors.ElementNotFoundError as e:
                raise errors.ElementError(text_type(e), element=self)

            ref_table, ref_table_class = ref_model.element.get_table_and_class(ref_model.app)
            table = model.get_table(app)
            _foreign_keys = None
            if through is None:
                assoc_table = model.make_association_table(model.get_table_name(app), ref_model.element.get_table_name(ref_model.app))
                primaryjoin = table.c.id == assoc_table.c.left_id
                secondaryjoin = ref_table.c.id == assoc_table.c.right_id
                left_key = b'left_id'
                right_key = b'right_id'
            else:
                try:
                    _app, assoc_model = self.document.get_app_element(through, app)
                except Exception as e:
                    raise errors.ElementError(text_type(e), element=self)

                assoc_table, assoc_table_class = assoc_model.get_table_and_class(_app)
                try:
                    if not foreign_keys:
                        left_key = model.libname.lower()
                        right_key = ref_model.element.libname.lower()
                    else:
                        left_key, right_key = foreign_keys
                except:
                    primaryjoin = None
                    secondaryjoin = None
                else:
                    left_key += b'_id'
                    right_key += b'_id'
                    primaryjoin = table.c.id == getattr(assoc_table.c, left_key)
                    secondaryjoin = ref_table.c.id == getattr(assoc_table.c, right_key)

            def get_collection(many_to_many):

                class ListCollection(list):

                    def __repr__(self):
                        return (b'<ListCollection {}>').format(self._instance)

                    @property
                    def table_class(self):
                        return ref_table_class

                    def __moyadbsubselect__(self, context):
                        dbsession = many_to_many.get_session(context, model.dbname)
                        qs = dbsession.query(getattr(assoc_table.c, right_key))
                        qs = qs.filter(self._instance.id == getattr(assoc_table.c, left_key))
                        return qs

                    def __moyaqs__(self, context, dbsession):
                        qs = dbsession.query(getattr(assoc_table.c, right_key))
                        qs = qs.filter(self._instance.id == getattr(assoc_table.c, left_key))
                        qs = dbsession.query(ref_table_class).filter(ref_table_class.id.in_(qs))
                        return qs

                    def __check_type__(self, obj):
                        return isinstance(obj, ref_table_class)

                return ListCollection

            def get_backref_collection(many_to_many):

                class ListCollection(list):

                    def __repr__(self):
                        return (b'<ListCollection {}>').format(self._instance)

                    @property
                    def table_class(self):
                        return model.get_table_class(app)

                    def __moyadbsubselect__(self, context):
                        dbsession = many_to_many.get_session(context, model.dbname)
                        qs = dbsession.query(getattr(assoc_table.c, left_key))
                        qs = qs.filter(self._instance.id == getattr(assoc_table.c, right_key))
                        return qs

                    def __moyaqs__(self, context, dbsession):
                        table_class = model.get_table_class(app)
                        qs = dbsession.query(getattr(assoc_table.c, left_key))
                        qs = qs.filter(self._instance.id == getattr(assoc_table.c, right_key))
                        qs = dbsession.query(table_class).filter(table_class.id.in_(qs))
                        return qs

                    def __check_type__(self, obj):
                        table_class = model.get_table_class(app)
                        return isinstance(obj, table_class)

                return ListCollection

            if backref_name:
                rel_backref = backref(backref_name, collection_class=get_backref_collection(self))
            else:
                rel_backref = None
            rel_property = relationship(ref_table_class, secondary=assoc_table, backref=rel_backref, primaryjoin=primaryjoin, secondaryjoin=secondaryjoin, foreign_keys=_foreign_keys, collection_class=get_collection(self))
            model.add_relationship(self.tag_name, params.name, params._get_param_dict(), ref_model)
            if backref_name:
                ref_model.element.add_relationship(self.tag_name, backref_name, {b'backlabel': backlabel or backref_name}, (
                 app, model), picker=params.backpicker)
            return rel_property

        model.add_property(params.name, get_property)


class FieldElement(DBElement):
    _non_field_attributes = []
    name = Attribute(b'Name of the element', type=b'text', required=True)
    null = Attribute(b'Allow null?', type=b'boolean', default=False)
    blank = Attribute(b'Allow blank?', type=b'boolean', default=True)
    default = Attribute(b'Default value', default=None)
    primary = Attribute(b'Use as primary key?', type=b'boolean')
    index = Attribute(b'Create index?', type=b'boolean', default=False)
    unique = Attribute(b'Impose unique constraint?', type=b'boolean', default=False)
    label = Attribute(b'Short description of field purpose')
    help = Attribute(b'Additional help text for use in object forms')
    formfield = Attribute(b'Macro to create a form field, used in admin', required=False, default=None)

    def document_finalize(self, context):
        params = self.get_all_parameters(context)
        self.name = params.pop(b'name').lower()
        del params[b'default']
        model = self.get_ancestor((self.xmlns, b'model'))
        col = self.get_moya_column(context, params)
        self.dbname = col.dbname
        model.add_column(col.name, col)

    def get_default(self, context):
        default = self.default(context) if self.has_parameter(b'default') else no_default
        return default

    def get_moya_column(self, context, params):
        params = {k:v for k, v in params.items() if k not in self._non_field_attributes}
        return self.moya_column(self.tag_name, self.name, default=self.get_default(context), **params)


class _Boolean(FieldElement):
    """Defines a [i]boolean[/i] field. Must appear within a <model> tag."""
    moya_column = dbcolumns.BoolColumn
    default = Attribute(b'Default value', default=None, type=b'expression')

    class Help:
        synopsis = b'a field that is True or False'
        example = b'\n        <boolean name="published" default="no" />\n        '


class _Float(FieldElement):
    """Defines a [i]floating point[/i] field. Must appear within a <model> tag."""
    moya_column = dbcolumns.FloatColumn
    default = Attribute(b'Default value', default=None, type=b'expression')

    class Help:
        synopsis = b'a field that stores a floating point number'
        example = b'\n            <float name="hotness" default="0"  null="n"/>\n        '


class _Decimal(FieldElement):
    """Defines a fixed precision number field in a <model>. Use this field element for currency."""
    moya_column = dbcolumns.DecimalColumn
    precision = Attribute(b'number of digits', type=b'integer', default=36)
    scale = Attribute(b'number of digits after the decimal point', type=b'integer', default=8)
    default = Attribute(b'Default value', default=None, type=b'expression')

    class Help:
        synopsis = b'a fix precision number'
        example = b'\n            <decimal name="balance" precision="12" scale="2" />\n        '


class _Integer(FieldElement):
    """Defines an [i]integer[/i] field. Must appear within a <model> tag."""
    moya_column = dbcolumns.IntegerColumn
    choices = Attribute(b'A reference to an enum', type=b'elementref')
    default = Attribute(b'Default value', default=None, type=b'expression')

    class Help:
        synopsis = b'a field that stores an integer'
        example = b'\n        <integer label="Comment count" name="count" default="0" null="no"/>\n        '


class _BigInteger(FieldElement):
    """Defines a [i]big integer[/i] field. Must appear within a <model> tag."""
    moya_column = dbcolumns.BigIntegerColumn
    default = Attribute(b'Default value', default=None, type=b'expression')

    class Help:
        synopsis = b'a field that stores a big integer'


class _SmallInteger(FieldElement):
    """Defines a [i]small integer[/i] field. Must appear within a <model> tag."""
    moya_column = dbcolumns.SmallIntegerColumn
    default = Attribute(b'Default value', default=None, type=b'expression')

    class Help:
        synopsis = b'a field that stores a small integer'


class _String(FieldElement):
    """Defines a [i]string[/i] field. Must appear within a <model> tag."""

    class Help:
        synopsis = b'a field that stores a string of characters'
        example = b'\n        <string name="first_name" label="First Name" length="30" default="" />\n        '

    moya_column = dbcolumns.StringColumn
    length = Attribute(b'Length of text', required=True, type=b'integer')
    choices = Attribute(b'A reference to a choices tag', type=b'elementref')


class _Upload(FieldElement):
    """An upload field"""

    class Help:
        synopsis = b'a field to store the path of an uploaded file'

    moya_column = dbcolumns.UploadColumn
    length = Attribute(b'Length of text', required=False, type=b'integer', default=200)
    getfs = Attribute(b'A macro to get the filesystem to use', required=False, default=b'elementref')
    getpath = Attribute(b"Macro that returns a path, will be called with 'upload' and 'form'", type=b'elementref', required=False)
    geturl = Attribute(b'Macro that returns a URL for this upload', type=b'elementref', required=False)

    def get_default(self, context):
        return


class Token(FieldElement):
    """A string column containing a randomly generated token. Note, that the string is not [i]guaranteed[/i] to be unique.
    If you want a unique token you will have to implement that logic independently."""

    class Help:
        synopsis = b'create a randomly generated token in the database'
        example = b'\n        <token name="token" length="16" unique="yes" characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" />\n        '

    moya_column = dbcolumns.StringColumn
    length = Attribute(b'Maximum length of token', required=True, type=b'integer')
    size = Attribute(b'Number of randomly generated characters in the token (defaults to same as length)', required=False, type=b'integer', default=None)
    characters = Attribute(b'Choice of characters to use in token (if set, this overrides other character related attributes).', default=None, required=False)
    lowercase = Attribute(b'Use lower case characters?', type=b'boolean', default=True, required=False)
    uppercase = Attribute(b'Use upper case characters?', type=b'boolean', default=False, required=False)
    digits = Attribute(b'Use digits?', type=b'boolean', default=True, required=False)
    punctuation = Attribute(b'Use punctuation?', type=b'boolean', default=False, required=False)
    _non_field_attributes = [
     b'size', b'characters', b'lowercase', b'uppercase', b'digits', b'punctuation']

    def get_default(self, context):
        size = self.size(context)
        length = self.length(context)
        size = min(length, size or length)
        choices = self.characters(context) or b''
        lowercase, uppercase, digits, punctuation = self.get_parameters(context, b'lowercase', b'uppercase', b'digits', b'punctuation')
        if not choices:
            if lowercase:
                choices += string.lowercase
            if uppercase:
                choices += string.uppercase
            if digits:
                choices += string.digits
            if punctuation:
                choices += string.punctuation
        if not choices:
            raise errors.ElementError(b'No choice of characters for random token', element=self, diagnosis=b"Set the 'characters' attribute to a non-empty string, or one of the other attributes to set the choice of characters.")
        return lambda : (b'').join(choice(choices) for _ in xrange(size))


class UUID(FieldElement):
    """
    Create a UUID field (http://en.wikipedia.org/wiki/Universally_unique_identifier).

    """

    class Help:
        synopsis = b'create a UUID in the database'
        example = b'\n        <uuid name="uuid" version="3" namespace="dns" name="moyaproject.com" />\n        '

    moya_column = dbcolumns.StringColumn
    length = Attribute(b'Maximum length of UUID (should be >= 36)', required=False, default=36, type=b'integer')
    version = Attribute(b'Type of UUID', choices=[b'1', b'3', b'4', b'5'], default=b'1')
    nstype = Attribute(b'Namespace (if using variant 3 or 5)', choices=[b'dns', b'url', b'oid', b'x500'], default=b'url')
    nsname = Attribute(b'Name in namespace (if using variant 3 or 5)', default=b'http://moyaproject.org')
    _non_field_attributes = [
     b'version', b'nstype', b'nsname']
    _namespace_map = {b'dns': uuid.NAMESPACE_DNS, 
       b'url': uuid.NAMESPACE_URL, 
       b'oid': uuid.NAMESPACE_OID, 
       b'x500': uuid.NAMESPACE_X500}

    def get_default(self, context):
        version, nstype, nsname = self.get_parameters(context, b'version', b'nstype', b'nsname')

        def getter():
            namespace = self._namespace_map[nstype]
            if version == b'1':
                uid = uuid.uuid1()
            elif version == b'3':
                uid = uuid.uuid3(namespace, nsname)
            elif version == b'4':
                uid = uuid.uuid4()
            elif version == b'5':
                uid = uuid.uuid5(namespace, nsname)
            uid_value = text_type(uid)
            return uid_value

        return getter


class Timezone(FieldElement):
    """Defines a [i]timezone[/i] field."""

    class Help:
        synopsis = b'a field that stores a timezone'

    moya_column = dbcolumns.TimezoneColumn
    length = Attribute(b'Length of text', required=True, type=b'integer', default=50)
    choices = Attribute(b'A sequence of possible choices', type=b'expression', default=timezone.get_common_timezones_groups())


class _Text(FieldElement):
    """Defines a [i]text[i] field."""
    markup = Attribute(b'Format of text field, used by Moya Admin to pick an editor', required=False, default=b'text')

    class Help:
        synopsis = b'a field that stores arbitrary length text'
        example = b'\n        <text name="description" null="no" default=""/>\n        '

    moya_column = dbcolumns.TextColumn


class _Datetime(FieldElement):
    """Defines a [i]datetime[/i] field."""

    class Help:
        synopsis = b'a field that stores a date and time'
        example = b'\n        <datetime name="last_login" label="Date of last login" null="yes" />\n        '

    moya_column = dbcolumns.DatetimeColumn
    auto = Attribute(b'Set to current time when created', type=b'boolean', default=False)

    def get_default(self, context):
        if self.auto(context):
            return lambda : ExpressionDateTime.utcnow()


class _Date(FieldElement):
    """Defines a [i]date[/i] field."""

    class Help:
        synopsis = b'a field that stores a date'

    moya_column = dbcolumns.DateColumn
    auto = Attribute(b'Set to current time when created', type=b'boolean', default=False)

    def get_default(self, context):
        if self.auto(context):
            return lambda : ExpressionDateTime.utcnow().date


class StringMap(FieldElement):
    moya_column = dbcolumns.StringMapColumn

    class Help:
        synopsis = b'a field that stores a mapping of keys and strings'

    def get_default(self, context):
        return


class _GenericKey(FieldElement):
    """
    Create a [i]generic[/i] key. A generic key is [tag db]foreign-key[/tag], but can link to any database object.

    """
    moya_column = dbcolumns.GenericKeyColumn

    class Help:
        synopsis = b'a generic foreign key'

    def get_default(self, context):
        return


class DBDataSetter(DataSetter, DBMixin):
    xmlns = namespaces.db

    class Help:
        undocumented = True

    def _qs(self, context, dbsession, value):
        if hasattr(value, b'__moyaqs__'):
            return value.__moyaqs__(context, dbsession)
        if hasattr(value, b'_get_query_set'):
            value = value._get_query_set()
        return value


class Create(DBDataSetter):
    """Create new object in the database."""

    class Help:
        synopsis = b'create an object in the database'
        example = b'\n\n            <db:create model="#User"\n                let:username="username"\n                let:email="email"\n                let:first_name="first_name"\n                let:last_name="last_name"\n                let:password="password"\n                dst="newuser" />\n\n        '

    model = Attribute(b'Model element reference', type=b'text', required=True)
    db = Attribute(b'Database name', default=b'_default')
    dst = Attribute(b'Destination', default=None)
    obj = Attribute(b'Object with initial values', required=False, default=None, type=b'index')
    _from = Attribute(b'Application', type=b'application', default=None)

    @wrap_db_errors
    def logic(self, context):
        params = self.get_parameters(context)
        element_app = self.get_app(context)
        app, model = self.get_model(context, params.model, app=element_app)
        dbsession = self.get_session(context, params.db)
        table_class = model.get_table_class(app)
        obj = params.obj or {}
        fields = {k:dbobject(v) for k, v in obj.items()}
        fields.update({k:dbobject(v) for k, v in self.get_let_map(context, check_missing=True).items()})
        fields.pop(b'id', None)
        with context.data_scope(fields):
            yield DeferNodeContents(self)
        try:
            value = table_class(**fields)
        except AdaptValueError as e:
            self.throw(b'db.create-fail', (b"unable to set field '{}' to {}").format(e.k, context.to_expr(e.v)), fields, diagnosis=b'Check the field supports the data type you are setting')
        except Exception as e:
            self.throw(b'db.create-fail', (b'unable to create a new {} object ({})').format(model, e), fields, diagnosis=b'Check the field supports the data type you are setting')

        if params.dst is not None:
            self.set_context(context, params.dst, value)
        signal_params = {b'object': value, b'model': model.libid, b'app': app}
        self.archive.fire(context, b'db.pre-create', element_app, model.libid, signal_params)
        try:
            with dbsession.manage(self):
                dbsession.add(value)
        except IntegrityError as e:
            value = None
            self.throw(b'db.integrityerror', text_type(e))
        except OperationalError as e:
            value = None
            self.throw(b'db.operationalerror', text_type(e))

        self.archive.fire(context, b'db.post-create', element_app, model.libid, signal_params)
        return


class GetOrCreate(DBDataSetter):
    """
    Get an object from the db if it exists, create it if it doesn't.

    If the object is created, the code in the enclosed block is executed.

    """

    class Help:
        synopsis = b"get an object from the database, or create it if it doesn't exist."
        example = b'\n            <db:get-or-create model="#Permission" let:name="\'admin\'"\n                let:description="\'User may perform administration tasks\'">\n                <echo>New permission was created.\n            </db:get-or-create>\n        '

    model = Attribute(b'Model element reference', type=b'text', required=True)
    db = Attribute(b'Database name', default=b'_default')
    dst = Attribute(b'Destination', default=None)
    created = Attribute(b'Destination to store created flag', type=b'index', default=None)
    initial = Attribute(b'Object with initial values', required=False, default=None, type=b'expression')
    _from = Attribute(b'Application', type=b'application', default=None)
    filter = Attribute(b'Filter expression', type=b'dbexpression', required=False, default=None)
    forupdate = Attribute(b'Issue a select FOR UPDATE?', type=b'boolean', required=False, default=False)

    @wrap_db_errors
    def logic(self, context):
        params = self.get_parameters(context)
        element_app = self.get_app(context)
        app, model = self.get_model(context, params.model, app=element_app)
        if params.filter:
            filter, exp_context = params.filter.eval2(self.archive, context, app)
        else:
            filter = None
        dbsession = self.get_session(context, params.db)
        table_class = model.get_table_class(app)
        created = False
        dst = params.dst
        let_map = self.get_let_map(context, check_missing=True)
        query = Get._get_attributes_query(self, context, table_class, let_map)
        qs = dbsession.query(table_class).filter(*query)
        if params.forupdate:
            qs = qs.with_for_update()
        if filter is not None:
            qs = qs.filter(filter)
            qs = exp_context.process_qs(qs)
        value = qs.first()
        if value is None:
            created = True
            obj = params.initial or {}
            fields = {k:dbobject(v) for k, v in obj.items() if k != b'id' if k != b'id'}
            fields.update({k:dbobject(v) for k, v in let_map.items()})
            try:
                value = table_class(**fields)
            except AdaptValueError as e:
                self.throw(b'db.create-fail', (b"unable to set field '{}' to {}").format(e.k, context.to_expr(e.v)), fields, diagnosis=b'Check the field supports the data type you are setting')
            except Exception as e:
                self.throw(b'db.create-fail', (b'unable to create a new {} object ({})').format(model, e), fields, diagnosis=b'Check the field supports the data type you are setting')

            signal_params = {b'object': value, b'model': model.libid, 
               b'app': app}
            self.archive.fire(context, b'db.pre-create', element_app, model.libid, signal_params)
            try:
                with dbsession.manage(self):
                    dbsession.add(value)
            except IntegrityError as e:
                self.throw(b'db.integrity-error', text_type(e))
            except OperationalError as e:
                self.throw(b'db.operational-error', text_type(e))

            self.archive.fire(context, b'db.post-create', element_app, model.libid, signal_params)
        dst = self.set_context(context, dst, value)
        if params.created:
            context[params.created] = created
        if created:
            yield logic.DeferNodeContents(self)
        return


class DBContextElement(ContextElementBase, DBMixin):
    xmlns = namespaces.db

    class Help:
        undocumented = True


class BulkCreate(ContextElementBase, DBMixin):
    """Create database object in bulk via JSON. Useful for quickly adding fixture data."""

    class Help:
        synopsis = b'bulk create database objects'

    xmlns = namespaces.db
    model = Attribute(b'Model', type=b'text', required=True)
    db = Attribute(b'Database', type=b'text', default=b'_default')
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'expression', default=None)

    @wrap_db_errors
    def logic(self, context):
        params = self.get_parameters(context)
        try:
            json = loads(self.text)
        except ValueError as error:
            self.throw(b'bad-value.json-error', text_type(error))

        app, model = self.get_model(context, params.model, app=self.get_app(context))
        dbsession = self.get_session(context, params.db)
        table_class = model.get_table_class(app)
        with dbsession.manage(self):
            for item in json:
                dbsession.add(table_class(**item))


class DeleteAll(ContextElementBase, DBMixin):
    """Delete every object from a table"""

    class Help:
        synopsis = b'delete all objects in a table'
        example = b'\n        <db:delete-all model="#Post"/>\n        '

    xmlns = namespaces.db
    model = Attribute(b'Model', required=True)
    db = Attribute(b'Database', default=b'_default')

    @wrap_db_errors
    def logic(self, context):
        _model, db = self.get_parameters(context, b'model', b'db')
        app, model = self.get_model(context, _model)
        session = self.get_session(context, db)
        session.query(model.get_table_class(app)).delete()


class Delete(ContextElementBase, DBMixin):
    """Delete an object from the database."""

    class Help:
        synopsis = b'delete from the database'
        example = b'\n        <db:get model="#Post" let:name="first_post" dst="post"/>\n        <db:delete src="post"/>\n        '

    xmlns = namespaces.db
    db = Attribute(b'Database', default=b'_default')
    src = Attribute(b'Object or queryset to delete', type=b'expression', required=True, missing=False)

    @wrap_db_errors
    def logic(self, context):
        db, src = self.get_parameters(context, b'db', b'src')
        dbsession = self.get_session(context, db)
        try:
            with dbsession.manage(self):
                if isinstance(src, MoyaQuerySet):
                    for item in src:
                        dbsession.delete(item)

                else:
                    dbsession.delete(src)
        except UnmappedInstanceError as e:
            self.throw(b'db.delete.fail', (b'Object {} is not stored in the db and could not be deleted').format(context.to_expr(src)))


class Get(DBDataSetter):
    """
    Get an object from the database.

    This tag will return a dagabase object if it exists, otherwise `None`. Additionally, if the object exists, the enclosed block will be executed.
    """

    class Help:
        synopsis = b'get an object in the database.'
        example = b'\n            <db:get model="#Topic" let:slug="url.topic" dst="topic"/>\n        '

    class Meta:
        one_of = [
         ('model', 'modelobj')]

    xmlns = namespaces.db
    default = None
    model = Attribute(b'Model element reference', required=False)
    modelobj = Attribute(b'Model object', type=b'expression', default=None)
    db = Attribute(b'Database to use', default=b'_default')
    orderby = Attribute(b'Order by', type=b'commalist', required=False, default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'application', default=None)
    filter = Attribute(b'Filter expression', type=b'dbexpression', required=False, default=None)
    src = Attribute(b'query set to restrict search', type=b'expression', required=False, default=None, missing=False)
    forupdate = Attribute(b'Issue a select FOR UPDATE?', type=b'boolean', required=False, default=False)

    @classmethod
    def _get_attributes_query(cls, element, context, table_class, let_map):
        q = []
        append = q.append
        for k, v in let_map.items():
            try:
                append(getattr(table_class, k) == dbobject(v))
            except:
                element.throw(b'db.get.invalid-comparison', (b'field {} can not be compared with value {}').format(context.to_expr(k), context.to_expr(v)), diagnosis=b'check the type of the value matches the column in the database model')

        return q

    @wrap_db_errors
    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        if params.modelobj is None:
            app, model = self.get_model(context, params.model, app=app)
        else:
            model = params.modelobj
        if params.filter:
            filter, exp_context = params.filter.eval2(self.archive, context, app)
        else:
            filter = None
        dbsession = self.get_session(context, params.db)
        let_map = self.get_let_map(context).items()
        for k, v in let_map:
            if is_missing(v):
                diagnosis = b'Moya can\'t except a missing value here. If you intended to use this value (i.e. it wasn\'t a typo), you should convert it to a non-missing value.\n\nFor example **let:{k}="name or \'anonymous\'"**\n'
                raise errors.ElementError((b"parameter '{k}' must not be missing (it is {v!r})").format(k=k, v=v), diagnosis=diagnosis.format(k=k, v=v))

        query = {k:dbobject(v) for k, v in let_map}
        table_class = model.get_table_class(app)
        for k in query:
            if not hasattr(table_class, k):
                self.throw(b'db.unknown-field', (b"the value '{}' is not a valid attribute for this model").format(k))

        query = self._get_attributes_query(self, context, table_class, query)
        if self.has_parameter(b'src'):
            src = params.src
            qs = self._qs(context, dbsession, src)
            qs = qs.filter(*query)
        else:
            qs = dbsession.query(table_class).filter(*query)
        if params.forupdate:
            qs = qs.with_for_update()
        if filter is not None:
            qs = qs.filter(filter)
            qs = exp_context.process_qs(qs)
        if params.orderby:
            qs = Query._make_order(self, qs, self.archive, context, table_class, params.orderby, app=app)
        value = self.get_value(context, qs)
        self.check_value(context, value)
        self.set_context(context, self.dst(context), value)
        if value:
            yield logic.DeferNodeContents(self)
        return

    def get_value(self, context, qs):
        try:
            return qs.first()
        except Exception as error:
            self.throw(b'db.error', (b'failed to query database; {}').format(error))

    def check_value(self, context, value):
        pass


class GetOne(Get):
    """
    Like [tag db]get[/tag], but will throw a [c]db.multiple-results[/c] if there are more than one result, or [c]db.no-result[/c] if there are no results.

    """

    class Help:
        synopsis = b'get precisely one matching object'
        example = None

    def get_value(self, context, qs):
        try:
            result = qs.one()
        except NoResultFound:
            self.throw(b'db.no-result', b'there was no matching result')
        except MultipleResultsFound:
            self.throw(b'db.multiple-results', b'multiple objects were returned')
        else:
            return result


class IfExists(ContextElementBase, DBMixin):
    """Execute the enclosed block if a object exists in the db."""

    class Help:
        synopsis = b'execute a block if an object exists in the database'
        example = b'\n            <db:if-exists model="#Link" let:topic="topic" let:slug="slug" >\n                <forms:error>Slug exists, please edit the title</forms:error>\n                <break/>\n            </db:if-exists>\n        '

    xmlns = namespaces.db
    model = Attribute(b'Model', required=False)
    modelobj = Attribute(b'Model object', type=b'expression', default=None)
    filter = Attribute(b'Filter expression', type=b'dbexpression', required=False, default=None)
    db = Attribute(b'Database', default=b'_default')
    _from = Attribute(b'Application', type=b'application', default=None)

    @wrap_db_errors
    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        if params.modelobj is None:
            app, model = self.get_model(context, params.model, app)
        else:
            model = params.modelobj
        dbsession = self.get_session(context, params.db)
        let_map = self.get_let_map(context)
        for k, v in let_map.items():
            if is_missing(v):
                diagnosis = b'Moya can\'t except a missing value here. If you intended to use this value (i.e. it wasn\'t a typo), you should convert it to a non-missing value.\n\nFor example **let:{k}="name or \'anonymous\'"**\n'
                raise errors.ElementError((b"parameter '{k}' must not be missing (it is {v!r})").format(k=k, v=v), diagnosis=diagnosis.format(k=k, v=v))

        query = {k:dbobject(v) for k, v in let_map.items()}
        table_class = model.get_table_class(app)
        query = Get._get_attributes_query(self, context, table_class, query)
        qs = dbsession.query(table_class).filter(*query)
        if params.filter:
            filter, exp_context = params.filter.eval2(self.archive, context, app)
            qs = qs.filter(filter)
        value = qs.first()
        if self._test(value):
            yield DeferNodeContents(self)
            yield SkipNext((namespaces.default, b'else'), (namespaces.default, b'elif'))
        return

    def _test(self, value):
        return value is not None


class IfNotExists(IfExists):
    """Executes the enclosed block if an object does not exists in the db."""

    class Help:
        synopsis = b'executes a block of code if an object does not exist in the db'

    def _test(self, value):
        return value is None


class GetRequired(Get):
    """Gets an object from the db. If the object is not present in the db then return a 404 (not found) response. This is useful when page content corresponds to a single object in the database."""
    xmlns = namespaces.db
    default = None
    status = Attribute(b'Status code', type=b'httpstatus', required=False, default=404)

    class Help:
        synopsis = b"get an object from the database, or return a 404 if it doesn't exist"
        example = b'\n        <db:get-required model="#Post" dst="post" let:slug="url.slug" />\n        '

    def check_value(self, context, value):
        if value is None:
            status = self.status(context)
            raise logic.EndLogic(http.RespondWith(status))
        return


class GetExist(Get):
    """Gets an object from the db, or throws a [c]moya.db.does-not-exist[/c] exception if it doesn't exist"""
    xmlns = namespaces.db
    default = None

    def check_value(self, context, value):
        if value is None:
            self.throw(b'moya.db.does-not-exist', b'No such object in the database')
        return


def query_flatten(qs):
    for obj in qs:
        if hasattr(obj, b'__iter__'):
            for item in obj:
                yield item

        else:
            yield obj


class GetColumn(DBDataSetter):
    """Get a specific column from the database. This is required if you don't know the column reference ahead of time, i.e. when you want to generate a query dynamically from a table. Moya Admin uses this tag, but it unlikely to be useful for general applications."""

    class Help:
        synopsis = b'get a column from a model'
        example = b'\n       <db:getcolumn model="${table.params.model}"\n            name="id" from="${.url.appname}" dst="id_column" />\n        '

    xmlns = namespaces.db
    _from = Attribute(b'Model app', type=b'application', required=False, default=None)
    model = Attribute(b'Model reference', required=False, default=None)
    modelobj = Attribute(b'Model object', type=b'expression', required=False, default=None)
    name = Attribute(b'Column name', required=True)

    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        if params.model is not None:
            model_app, model = self.get_element(params.model, app=app)
        else:
            model = params.modelobj
            model_app = app
        if hasattr(model, b'__moyamodel__'):
            model_app, model = model.__moyamodel__()
        try:
            table_class = model.get_table_class(model_app)
        except AttributeError:
            self.throw(b'bad-value.not-a-model', (b'value {} does not appear to be a model').format(context.to_expr(model)))

        try:
            column = getattr(table_class, params.name)
        except AttributeError:
            self.throw(b'bad-value.missing-column', (b"model doesn't contain a column called '{}'").format(params.name))

        self.set_context(context, params.dst, column)
        return


class Inspect(DBDataSetter):
    """Inspect a DB model, so you can view column information. Used by Moya Admin."""

    class Help:
        synopsis = b'get model information'
        example = b'\n            <db:inspect model="${table.params.model}" from="${.url.appname}" dst="model" />\n        '

    xmlns = namespaces.db
    _from = Attribute(b'Model app', type=b'application', required=False, default=None)
    model = Attribute(b'Model reference', required=True)

    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        model_app, model = self.get_element(params.model, app=app)
        table_class = model.get_table_class(model_app)
        model_proxy = ModelProxy(model, model_app)
        self.set_context(context, params.dst, model_proxy)


class GetDefaults(DataSetter):
    xmlns = namespaces.db
    _from = Attribute(b'Model app', type=b'application', required=False, default=None)
    model = Attribute(b'Model reference', required=True)

    def get_value(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        model_app, model = self.get_element(params.model, app=app)
        table_class = model.get_table_class(model_app)
        return table_class.get_defaults()


class NewQuery(DBDataSetter):
    """Create a query object dynamically."""

    class Help:
        synopsis = b'dynamically create a database query'
        example = b'\n        <db:new-query model="relationship.ref_model" from="${relationship.ref_model.app.name}" dst="related" />\n        '

    xmlns = namespaces.db
    db = Attribute(b'Database', default=b'_default')
    model = Attribute(b'Model', type=b'expression', required=True)
    _from = Attribute(b'Model app', type=b'application', required=False, default=None)

    def logic(self, context):
        params = self.get_parameters(context)
        dbsession = self.get_session(context, params.db)
        app = self.get_app(context)
        model = params.model
        if hasattr(model, b'__moyamodel__'):
            app, model = model.__moyamodel__()
        table_class = model.get_table_class(app)
        qs = dbsession.query(table_class)
        qs = MoyaQuerySet(qs, table_class, dbsession)
        self.set_context(context, params.dst, qs)


class Sort(DBDataSetter):
    """Sort a Query Set"""

    class Help:
        synopsis = b'sort a query set'

    xmlns = namespaces.db
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Model app', type=b'application', required=False, default=None)
    src = Attribute(b'Source query, if further query operations are required', type=b'reference', default=None, metavar=b'QUERYSET')
    orderby = Attribute(b'Order by', type=b'commalist', required=True)
    reverse = Attribute(b'Reverse order?', type=b'expression', required=False, default=False)

    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        qs = context[params.src]
        dbsession = qs.dbsession
        table_class = qs.table_class
        if hasattr(qs, b'_get_query_set'):
            qs = qs._get_query_set()
        qs = Query._make_order(qs, self.archive, context, None, params.orderby, params.reverse, app=app)
        dst = params.dst or params.src
        qs = MoyaQuerySet(qs, table_class, dbsession)
        self.set_context(context, dst, qs)
        return


class SortMap(DBDataSetter):
    """
    Sort a query set in one of a number of different ways.

    This is typically used to sort a table of results based on a value in the query set.

    """

    class Help:
        synopsis = b'sort a query set dynamically'
        example = b'\n        <db:sort-map src="characters" sort=".request.GET.sort" reverse=".request.GET.order==\'desc\'">\n            <str dst="name">#Character.name</str>\n            <str dst="species">#Character.species</str>\n            <str dst="age">#Character.age</str>\n        </db:sort-map>\n        '

    xmlns = namespaces.db
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Model app', type=b'application', required=False, default=None)
    src = Attribute(b'Query to sort', type=b'reference', default=None, metavar=b'QUERYSET', missing=False, required=True)
    sort = Attribute(b'Sort value?', type=b'expression', required=False, evaldefault=True, default=b'.request.GET.sort')
    reverse = Attribute(b'Reverse order?', type=b'expression', required=False, default=b".request.GET.order=='desc'", evaldefault=True)
    columns = Attribute(b'Sort columns', type=b'expression', required=False)

    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        qs = context[params.src]
        if is_missing(qs):
            raise errors.ElementError((b"attribute 'src' must not be missing (it is {!r})").format(qs), element=self)
        dbsession = qs.dbsession
        table_class = qs.table_class
        if hasattr(qs, b'_get_query_set'):
            qs = qs._get_query_set()
        sort_map = params.columns or {}
        if not hasattr(sort_map, b'items'):
            self.throw(b'bad-value.columns', b'Columns attribute should be a dict or other mapping')
        with context.data_scope(sort_map):
            yield DeferNodeContents(self)
        orderby = sort_map.get(params.sort, None)
        if orderby is not None:
            qs = Query._make_order(self, qs, self.archive, context, None, [
             orderby], params.reverse, app=app)
            dst = params.dst or params.src
            qs = MoyaQuerySet(qs, table_class, dbsession)
            self.set_context(context, dst, qs)
        return


class Query(DBDataSetter):
    """Query the database. Will return a query set object that may be iterated over by default, unless [c]'collect'[/c] is specified."""

    class Help:
        synopsis = b'query the database'
        example = b'\n        <!-- examples taken from Moya apps -->\n\n        <!-- Get a month worth of posts -->\n        <db:query model="#Post" dst="posts" orderby="-published_date"\n            filter="#Post.published_date gte start and #Post.published_date lt start.next_month"/>\n\n        <!-- delete a user session -->\n        <db:query model="#Session" let:session_key=".request.cookies.authsession" action="delete"/>\n\n        <!-- get promoted topics in Moya Social Links -->\n        <db:query model="#Topic" filter="#Topic.promoted == yes" orderby="#Topic.title" dst="promoted_topics"/>\n\n    '

    class Meta:
        one_of = [
         ('model', 'columns', 'src')]

    xmlns = namespaces.db
    model = Attribute(b'Model', required=False, default=None, metavar=b'ELEMENTREF')
    _from = Attribute(b'Model app', type=b'application', required=False, default=None)
    db = Attribute(b'Database', default=b'_default')
    src = Attribute(b'Source query, if further query operations are required', type=b'expression', default=None, metavar=b'QUERYSET', missing=False)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    filter = Attribute(b'Filter expression', type=b'dbexpression', required=False, default=None)
    orderby = Attribute(b'Order by', type=b'commalist', required=False, default=None)
    reverse = Attribute(b'Reverse order?', type=b'expression', required=False, default=False)
    distinct = Attribute(b'Make query distinct (remove duplicates from results)?', type=b'boolean', default=False)
    columns = Attribute(b'Columns to return, if model is not specified', type=b'dbexpression', required=False, default=None)
    flat = Attribute(b'Flatten results in to a list?', type=b'boolean', required=False, default=False)
    collect = Attribute(b'Collect results?', required=False, choices=[b'list', b'set', b'dict', b'dict_sequence'])
    collectkey = Attribute(b'Collect key if collect is True', required=False, default=None)
    start = Attribute(b'Start index', type=b'expression', required=False, default=None)
    maxresults = Attribute(b'Maximum number of items to return', type=b'expression', default=None, required=False)
    action = Attribute(b'Action to perform on query', default=None, required=False, choices=[b'delete', b'count', b'exists'])
    join = Attribute(b'Join expressions', type=b'dbexpression', required=False, default=None)
    groupby = Attribute(b'Group by column(s)', type=b'commalist', required=False, default=None)
    forupdate = Attribute(b'Issue a select FOR UPDATE?', type=b'boolean', required=False, default=False)

    @classmethod
    def _get_order(cls, archive, context, table_class, orderby, reverse=False, app=None):
        order = []
        for field in orderby:
            if not field:
                continue
            descending = field.startswith(b'-')
            if descending:
                field = field[1:]
            if b'#' in field:
                sort_col, exp_context = DBExpression(field).eval2(archive, context, app)
                if reverse or descending:
                    sort_col = desc(sort_col)
                order.append(sort_col)
            elif not table_class:
                raise ValueError(b'Model required for order')
            else:
                sort_col = getattr(table_class, field)
                if reverse or descending:
                    sort_col = sort_col.desc()
                order.append(sort_col)

        return order

    @classmethod
    def _make_order(cls, element, qs, archive, context, table_class, orderby, reverse=False, app=None):
        order = []
        for field in orderby:
            if not field:
                continue
            descending = field.startswith(b'-')
            if descending:
                field = field[1:]
            if b'#' in field:
                sort_col, exp_context = DBExpression(field).eval2(archive, context, app)
                if qs is not None:
                    qs = exp_context.process_qs(qs)
                if reverse or descending:
                    sort_col = desc(sort_col)
                order.append(sort_col)
            elif not table_class:
                element.throw(b'db.model-required', b'Model required for order', diagnosis=b'Specify the model attribute, or use a field reference in order by (e.g. order="#Model.field")')
            else:
                sort_col = getattr(table_class, field, None)
                if sort_col is None:
                    raise errors.ElementError((b"sort field '{}' was not recognized").format(field), diagnosis=b'check the "orderby" field for typos')
                if reverse or descending:
                    sort_col = sort_col.desc()
                order.append(sort_col)

        if order:
            try:
                qs = qs.order_by(False).order_by(*order)
            except ArgumentError:
                raise errors.ElementError((b'unable to sort by {}').format((b', ').join(orderby)), diagnosis=b'check all values in orderby are database fields (properties may not be used in orderby argument)')

        return qs

    @wrap_db_errors
    def logic(self, context):
        params = self.get_parameters(context)
        dbsession = self.get_session(context, params.db)
        app = self.get_app(context)
        if params.filter:
            filter, exp_context = params.filter.eval2(self.archive, context, app)
        else:
            filter = None
        table_class = None
        if params.src is not None:
            qs = self._qs(context, dbsession, params.src)
            table_class = getattr(dbobject(params.src), b'table_class', None)
            if table_class is None:
                raise errors.ElementError((b'src attribute must be a database object, not {}').format(context.to_expr(params.src)), element=self)
        elif params.model:
            try:
                model_app, model = self.get_app_element(params.model, app=app)
            except errors.ElementNotFoundError as e:
                raise errors.ElementError(text_type(e), element=self)

            table_class = model.get_table_class(model_app)
            qs = dbsession.query(table_class)
        else:
            qs = dbsession.query()
        if params.forupdate:
            qs = qs.with_for_update()
        if params.columns is not None:
            columns = params.columns.eval(self.archive, context, app=app)
            if not isinstance(columns, list):
                columns = [
                 columns]
            try:
                qs = dbsession.query(*columns)
            except:
                raise self.throw(b'db.bad-columns', b"'columns' attribute must refer to columns only")

        if params.join is not None:
            joins = params.join.eval(self.archive, context)
            if not isinstance(joins, list):
                joins = [
                 joins]
            try:
                for j in joins:
                    if isinstance(j, (tuple, list)):
                        qs = qs.join(*j)
                    else:
                        qs = qs.join(j)

                qs = qs.join(*joins)
            except Exception as e:
                self.throw(b'db.bad-join', text_type(e))

        if params.groupby is not None:
            group_by = [ DBExpression(g).eval(self.archive, context, app) for g in params.groupby ]
            qs = qs.group_by(*group_by)
        if filter is not None:
            try:
                qs = qs.filter(filter)
            except Exception as e:
                self.throw(b'db.filter-failed', b'unable to apply filter to queryset', diagnosis=(b"Moya's db engine reported the following:\n\n**{}**").format(e))

            qs = exp_context.process_qs(qs)
        if table_class is not None:
            query_data = {k:dbobject(v) for k, v in self.get_let_map(context).items()}
            for k, v in query_data.items():
                if is_missing(v):
                    self.throw(b'bad-value.missing', (b"filter attribute '{{{}}}{}' should not be missing (it is {!r})").format(namespaces.let, k, v), diagnosis=(b"Let key '{}' refers to a missing value, which is invalid for this tag. If you want to query a null value in the database, you could convert to None with the **none:** modifier.").format(k))
                try:
                    qs = qs.filter(getattr(table_class, k) == v)
                except:
                    self.throw(b'bad-value.invalid-filter', (b"Can't filter {} on column '{}'").format(context.to_expr(v), k), diagnosis=b'Check the field type is compatible with the value you wish to filter on.')

        elif self.get_let_map(context):
            self.throw(b'bad-value.model-required', b"Moya can't use LET attributes without a model", diagnosis=b"Specfiy the 'model' or use the 'filter' attribute")
        if params.orderby:
            qs = Query._make_order(self, qs, self.archive, context, table_class, params.orderby, params.reverse, app=app)
        if params.distinct:
            qs = qs.distinct()
        if params.start or params.maxresults:
            start = params.start or 0
            qs = qs.slice(start, start + params.maxresults)
        if params.action == b'delete':
            self.set_context(context, params.dst, qs.delete())
            return
        else:
            if params.action == b'count':
                self.set_context(context, params.dst, qs.count())
                return
            if params.action == b'exists':
                self.set_context(context, params.dst, qs.first() is not None)
                return
            if params.flat:
                qs = list(query_flatten(qs))
            elif params.collect:
                if params.collect == b'list':
                    collectkey = params.collectkey
                    if collectkey:
                        qs = [ getattr(result, collectkey, None) for result in qs ]
                    else:
                        qs = list(qs)
                elif params.collect == b'set':
                    qs = set(qs)
                elif params.collect == b'dict':
                    collectkey = params.collectkey
                    qs = OrderedDict((getattr(obj, collectkey), obj) for obj in qs if hasattr(obj, collectkey))
                elif params.collect == b'dict_sequence':
                    qs = OrderedDict(qs)
            else:
                qs = MoyaQuerySet(qs, table_class, dbsession)
            self.set_context(context, params.dst, qs)
            return


def _flatten_result(obj):
    if isinstance(obj, (ResultProxy, list, tuple)):
        return [ _flatten_result(i) for i in obj ]
    if isinstance(obj, RowProxy):
        return OrderedDict((k, v) for k, v in obj.items())
    return obj


@implements_bool
class MoyaResultFetcher(object):
    __moya_exposed_attributes__ = [
     b'one', b'all', b'scalar']

    def __init__(self, results):
        self._results = results

    def __moyarepr__(self, context):
        return b'<fetcher>'

    def __getitem__(self, k):
        if isinstance(k, text_type):
            if k == b'one':
                return self.one
            else:
                if k == b'all':
                    return self.all
                if k == b'scalar':
                    return self.scalar
                return KeyError(k)

        elif isinstance(k, number_types):
            i = int(k)
            if i <= 0:
                raise KeyError(k)
            try:
                return _flatten_result(self._results.fetchmany(i))
            except:
                return []

        raise KeyError(i)

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return 3

    def __bool__(self):
        return True

    def keys(self):
        return [
         b'one', b'all', b'scalar']

    def values(self):
        return [
         self.one, self.all, self.scalar]

    def items(self):
        return zip(self.keys(), self.values())

    @property
    def one(self):
        try:
            return _flatten_result(self._results.fetchone())
        except:
            return

        return

    @property
    def all(self):
        try:
            return _flatten_result(self._results.fetchall())
        except:
            return []

    @property
    def scalar(self):
        try:
            return self._results.scalar()
        except:
            return

        return


@implements_bool
class MoyaResultProxy(interface.AttributeExposer):
    """A proxy to SQL Alchemy's ResultProxy"""
    __moya_exposed_attributes__ = [
     b'rowcount',
     b'rowkeys',
     b'fetch']

    def __init__(self, results, sql):
        self._results = results
        self.sql = sql.strip()
        self.fetch = MoyaResultFetcher(results)

    def __bool__(self):
        return bool(self.rowcount)

    def __moyarepr__(self, context):
        return (b'<results {}>').format(context.to_expr(self.sql))

    def __iter__(self):
        return iter(_flatten_result(r) for r in self._results.fetchall())

    @property
    def rowcount(self):
        return self._results.rowcount

    @property
    def rowkeys(self):
        return self._results.keys()


class SQL(DBDataSetter):
    """
    This tag executes raw SQL and returns a [i]results[/i] object.

    Results objects have the properties [c]rowcount[/c] (number of rows matched), [c]rowkeys[/c] (list of field names), and [c]fetch[/c] (an interface to retrieve results).

    You can retrieve all rows with [c]results.fetch.all[/c], or a single row at a time with [c]results.fetch.one[/c]. You can get a batch of a rows by using an integer index. For example, [c]results.fetch.10[/c] retrieves the next 10 rows.

    If your query returns a scalar value, you can retrieve it with [c]results.fetch.scalar[/c].

    """

    class Help:
        synopsis = b'execute raw sql'
        example = b'\n        <db:sql dst="results" let:username="\'John\'">\n            select * from auth_user where auth_user.username=:username;\n        </db:sql>\n        <echo obj="results.fetch.one"/>\n\n        '

    db = Attribute(b'Database', default=b'_default')
    bind = Attribute(b'Parameters to bind to SQL', type=b'expression', default=None)

    @wrap_db_errors
    def get_value(self, context):
        params = self.get_parameters(context)
        sql_text = self.text
        sql = text(sql_text)
        sql_params = self.bind(context) or {}
        if not isinstance(sql_params, dict):
            self.throw(b'bad-value.wrong-type', b'bind must be a dict or dict-like object')
        sql_params.update(self.get_let_map(context))
        dbsession = self.get_session(context, params.db)
        result = dbsession.execute(sql, sql_params)
        result = MoyaResultProxy(result, sql_text)
        return result


class Update(DBDataSetter):
    """
    Update a query set with database expressions. Not to be confused with [tag]{}update[/tag] in the default namespace.

    """

    class Help:
        synopsis = b'update fields in a query'
        example = b'\n        <db:query model="#Vote" filter="#Vote.topic==\'moya\'" dst="votes"/>\n        <db:update src="votes" let:topic="#Vote.score + 1" />\n        '

    src = Attribute(b'Queryset', required=True, type=b'expression', metavar=b'QUERYSET')
    db = Attribute(b'Database', default=b'_default')
    synchronize = Attribute(b'Synchronize session strategy', choices=[b'none', b'fetch', b'evaulate'], default=b'fetch')

    def logic(self, context):
        params = self.get_parameters(context)
        dbsession = self.get_session(context, params.db)
        qs = self._qs(context, dbsession, params.src)
        let = self.get_let_map_eval(context, lambda l: DBExpression(l).eval(self.archive, context))
        sync = params.synchronize
        if sync == b'none':
            sync = None
        with dbsession.manage(self):
            qs.update(let, synchronize_session=sync)
        return


class Commit(DBContextElement):
    """
    Commit any pending transaction. This will [i]flush[/i] db operations to the database. If you have create new objects and you want to know their [i]primary key[/i] (id), you will need to commit them to the database.

    Note, that if this tag is called from within a [tag db]transaction[/tag] tag, nothing will be committed until the end of the [tag db]transaction[/tag].

    """

    class Help:
        synopsis = b'commit the current transaction'
        example = b'\n        <db:create model="model.shorturl" obj="form.data" dst="shorturl"/>\n        <db:commit />\n        <echo>${shorturl.id}</echo>\n        '

    db = Attribute(b'Database', default=b'_default')

    @wrap_db_errors
    def logic(self, context):
        dbsession = self.get_session(context, self.db(context))
        with dbsession.manage(self):
            pass


class RollBack(DBContextElement):
    """
    This tag will rollback a transaction, and restore the database to the state where it was previously commited.

    """

    class Help:
        synopsis = b'roll back the current transactions'

    db = Attribute(b'Database', default=b'_default')

    @wrap_db_errors
    def logic(self, context):
        dbsession = self.get_session(context)
        dbsession.rollback()


class Check(DBContextElement):
    """Check connection to DB, throw db.no-connection if connection failed. This tag is used by Moya Debug, it is unlikely to be generally useful."""

    class Help:
        synopsis = b'check connection to the database'

    db = Attribute(b'Database', default=b'_default')

    def logic(self, context):
        dbsession = self.get_session(context, self.db(context))
        try:
            dbsession.connection()
        except Exception as e:
            self.throw(b'db.no-connection', text_type(e))


class Atomic(DBContextElement):
    """
    Makes the enclosed block [i]atomic[/i].

    An atomic block works much like [tag db]transaction[/tag], but uses the databases SAVEPOINT feature to better handle nested atomic blocks.

    """

    class Help:
        synopsis = b'mark a block as being atomic'
        example = b'\n        <!--- taken from Moya Social Links -->\n        <db:atomic>\n            <db:get model="#Link" let:id="link" dst="link" />\n            <db:get model="#Vote" let:link="link" dst="vote" />\n            <db:create if="not vote"\n                model="#Vote" let:link="link" let:user=".user" let:score="score" dst="vote" />\n            <let link.score="link.score - vote.score" vote.score="score" />\n            <let link.score="link.score + vote.score" />\n        </db:atomic>\n\n        '

    db = Attribute(b'Database', default=b'_default')

    @wrap_db_errors
    def logic(self, context):
        dbsession = self.get_session(context, self.db(context))
        if dbsession.engine.driver == b'pysqlite':
            log.warning(b'sqlite driver does not support <atomic>')
            try:
                yield DeferNodeContents(self)
            except Exception as e:
                log.warning((b'exception in <atomic> block ()').format(e))
                raise

        else:
            session = dbsession.session
            session.begin_nested()
            try:
                yield DeferNodeContents(self)
            except Exception as e:
                session.rollback()
                raise
            else:
                session.commit()


class Transaction(DBContextElement):
    """
    Executes the enclosed block in a single transaction.

    If the block executes successfully, the changes will be committed. If an exception is thrown, the changes will be rolled back.

    Note that databases related exceptions in the enclosed black won't be thrown until the end of the transaction.

    In the case of nested transactions (a transaction inside a transactions), only the outer-most transaction will actually commit the changes. For more granular control over transactions, the [tag db]atomic[/tag] tag is preferred.

2260
    """

    class Help:
        synopsis = b'commit changes to the database'

    db = Attribute(b'Database', default=b'_default')

    @wrap_db_errors
    def logic(self, context):
        dbsession = self.get_session(context, self.db(context))
        with dbsession.manage(self):
            yield DeferNodeContents(self)


class UniqueTogether(DBContextElement):
    xmlns = namespaces.db

    class Help:
        synopsis = b'require combinations of fields to be unique'

    fields = Attribute(b'Fields', type=b'commalist', required=False, default=None)

    def document_finalize(self, context):
        fields = self.fields(context)
        if fields is None:
            fields = []
            for child in self.children():
                if isinstance(child, (FieldElement, _ForeignKey)):
                    fields.append(child.dbname)

        fields = list(set(fields))
        model = self.get_ancestor((self.xmlns, b'model'))
        model.add_constraint(UniqueConstraint(*fields))
        return