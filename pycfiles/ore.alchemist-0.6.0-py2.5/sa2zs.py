# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/alchemist/sa2zs.py
# Compiled at: 2008-09-11 20:29:53
"""
SQLAlchemy to Zope3 Schemas

$Id: sa2zs.py 299 2008-05-23 20:31:48Z kapilt $
"""
from zope import interface, schema, component
from zope.interface.interface import InterfaceClass
from zope.schema.interfaces import ValidationError
from sqlalchemy.util import OrderedDict
from sqlalchemy import types as rt
import sqlalchemy as rdb
from interfaces import ITableSchema, TransmutationException, IAlchemistTransmutation, IModelDescriptor, IIModelInterface
interface.moduleProvides(IAlchemistTransmutation)

class TableAnnotation(object):
    """
    Annotations for Table objects, to annotate as needed, the notion
    is that the annotation keys correspond to column, and values correspond
    to application specific column metadata.
    """
    _marker = object()
    schema_invariants = ()

    def __init__(self, table_name, columns=(), properties=(), schema_order=(), listing_columns=(), order_by=()):
        self.table_name = table_name
        self._options = {}
        self._annot = OrderedDict()
        for info in columns:
            self._annot[info['name']] = info

        self.properties = properties
        self.schema_order = schema_order
        self.listing_columns = listing_columns
        self.order_by = order_by

    def setOption(self, name, value):
        self._options[name] = value

    def getOption(self, name, default=None):
        return self._options.get(name, default)

    def __call__(self, iface):
        return self

    def __setitem__(self, name, value):
        self._annot[name] = value

    def get(self, name, default=None):
        return self._annot.get(name, default)

    def __getitem__(self, name):
        return self.get(name)

    def values(self):
        return self._annot.values()

    def __contains__(self, name):
        return not self._marker == self.get(name, self._marker)


class ColumnTranslator(object):

    def __init__(self, schema_field):
        self.schema_field = schema_field

    def extractInfo(self, column, info):
        d = {}
        d['title'] = unicode(info.get('label', column.name))
        d['description'] = unicode(info.get('description', ''))
        d['required'] = not column.nullable
        if not d['required'] and info.get('required'):
            d['required'] = True
        if isinstance(column.default, rdb.ColumnDefault):
            default = column.default.arg
        else:
            default = column.default
        validator = self.schema_field()
        try:
            validator.validate(default)
            d['default'] = default
        except ValidationError:
            pass

        return d

    def __call__(self, column, annotation):
        info = annotation.get(column.name, {})
        d = self.extractInfo(column, info)
        return self.schema_field(**d)


class SizedColumnTranslator(ColumnTranslator):

    def extractInfo(self, column, info):
        d = super(SizedColumnTranslator, self).extractInfo(column, info)
        d['max_length'] = column.type.length
        return d


class ColumnVisitor(object):
    column_type_map = [
     (
      rt.Float, ColumnTranslator(schema.Float)),
     (
      rt.SmallInteger, ColumnTranslator(schema.Int)),
     (
      rt.Date, ColumnTranslator(schema.Date)),
     (
      rt.DateTime, ColumnTranslator(schema.Datetime)),
     (
      rt.TEXT, ColumnTranslator(schema.Text)),
     (
      rt.Boolean, ColumnTranslator(schema.Bool)),
     (
      rt.String, SizedColumnTranslator(schema.TextLine)),
     (
      rt.Binary, ColumnTranslator(schema.Bytes)),
     (
      rt.Unicode, SizedColumnTranslator(schema.Bytes)),
     (
      rt.Numeric, ColumnTranslator(schema.Float)),
     (
      rt.Integer, ColumnTranslator(schema.Int))]

    def __init__(self, info):
        self.info = info or {}

    def visit(self, column):
        column_handler = None
        for (ctype, handler) in self.column_type_map:
            if isinstance(column.type, ctype):
                if isinstance(handler, str):
                    handler = getattr(self, handler)
                column_handler = handler
                break

        if column_handler is None:
            raise TransmutationException('no column handler for %r' % column)
        return column_handler(column, self.info)


class SQLAlchemySchemaTranslator(object):

    def applyProperties(self, field_map, annotation):
        order_value = 0
        cascade_order = False
        values = list(annotation.values())
        for idx in range(len(values)):
            info = values[idx]
            if info.name in field_map:
                if info.property:
                    if cascade_order:
                        order_value += 2
                        field_map[info.name] = f = info.property
                        f.order = order_value
                if cascade_order:
                    order_value += 2
                    field_map[info.name].order = order_value
                else:
                    order_value = field_map[info.name].order
            if not info.property:
                continue
            cascade_order = True
            order_value += 2
            field_map[info.name] = info.property
            field_map[info.name].order = order_value

    def applyOrdering(self, field_map, schema_order):
        """ apply global ordering to all fields, any fields not specified have ordering
            preserved, but are now located after fields specified in the schema order, which is
            a list of field names.
        """
        self.verifyNames(field_map, schema_order)
        visited = set()
        order = 1
        for s in schema_order:
            field_map[s].order = order
            visited.add(s)
            order += 1

        remainder = [ (field.order, field) for (field_name, field) in field_map.items() if field_name not in visited ]
        remainder.sort()
        for (order, field) in remainder:
            field.order = order
            order += 1

    def verifyNames(self, field_map, names):
        for n in names:
            if n not in field_map:
                raise AssertionError('invalid field specified  %s' % n)

    def generateFields(self, table, annotation):
        visitor = ColumnVisitor(annotation)
        d = {}
        for column in table.columns:
            if annotation.get(column.name, {}).get('omit', False):
                continue
            d[column.name] = visitor.visit(column)

        return d

    def applyTaggedValues(self, iface, annotation, kw):
        invariants = kw.get('invariants') or annotation.schema_invariants
        if not invariants:
            return
        assert isinstance(invariants, (list, tuple))
        iface.setTaggedValue('invariants', invariants)

    def translate(self, table, annotation, __module__, **kw):
        annotation = annotation or TableAnnotation(table.name)
        iname = kw.get('interface_name') or 'I%sTable' % table.name
        field_map = self.generateFields(table, annotation)
        self.applyProperties(field_map, annotation)
        schema_order = kw.get('schema_order', None) or annotation.schema_order
        if schema_order:
            self.applyOrdering(field_map, schema_order)
        if 'bases' in kw:
            bases = (
             ITableSchema,) + kw.get('bases')
        else:
            bases = (
             ITableSchema,)
        DerivedTableSchema = InterfaceClass(iname, attrs=field_map, bases=bases, __module__=__module__)
        self.applyTaggedValues(DerivedTableSchema, annotation, kw)
        return DerivedTableSchema


def transmute(table, annotation=None, __module__=None, **kw):
    if __module__ is None:
        import sys
        __module__ = sys._getframe(1).f_globals['__name__']
    z3iface = SQLAlchemySchemaTranslator().translate(table, annotation, __module__, **kw)
    interface.directlyProvides(z3iface, IIModelInterface)
    if annotation is not None:
        name = '%s.%s' % (z3iface.__module__, z3iface.__name__)
        component.provideAdapter(annotation, adapts=(
         IIModelInterface,), provides=IModelDescriptor, name=name)
    return z3iface


def transmute_mapper(mapper, annotation=None, __module__=None, **kw):
    pass