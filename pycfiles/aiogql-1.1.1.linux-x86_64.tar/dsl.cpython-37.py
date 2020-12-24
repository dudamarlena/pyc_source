# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/aiogql/dsl.py
# Compiled at: 2020-01-21 09:02:42
# Size of source mod 2**32: 5753 bytes
import collections, decimal
from functools import partial
import six
from graphql.language import ast
from graphql.language.printer import print_ast
from graphql.type import GraphQLField, GraphQLList, GraphQLNonNull, GraphQLEnumType, GraphQLInputObjectField, GraphQLInputObjectType
from .utils import to_camel_case
import graphql.utils.ast_from_value as ast_from_value

class DSLSchema(object):

    def __init__(self, client):
        self.client = client

    @property
    def schema(self):
        return self.client.schema

    def __getattr__(self, name):
        type_def = self.schema.get_type(name)
        return DSLType(type_def)

    async def query(self, *args, **kwargs):
        return await self.execute(query(*args, **kwargs))

    async def mutate(self, *args, **kwargs):
        return await (self.query)(args, operation='mutation', **kwargs)

    async def execute(self, document):
        return await self.client.execute(document)


class DSLType(object):

    def __init__(self, type):
        self.type = type

    def __getattr__(self, name):
        formatted_name, field_def = self.get_field(name)
        return DSLField(formatted_name, field_def)

    def get_field(self, name):
        camel_cased_name = to_camel_case(name)
        if name in self.type.fields:
            return (
             name, self.type.fields[name])
        if camel_cased_name in self.type.fields:
            return (
             camel_cased_name, self.type.fields[camel_cased_name])
        raise KeyError('Field {} doesnt exist in type {}.'.format(name, self.type.name))


def selections(*fields):
    for _field in fields:
        yield field(_field).ast


def get_ast_value(value):
    if isinstance(value, ast.Node):
        return value
    if isinstance(value, ast.Value):
        return value
    if isinstance(value, six.string_types):
        return ast.StringValue(value=value)
    if isinstance(value, bool):
        return ast.BooleanValue(value=value)
    if isinstance(value, (float, decimal.Decimal)):
        return ast.FloatValue(value=value)
    if isinstance(value, int):
        return ast.IntValue(value=value)
    if isinstance(value, list):
        return ast.ListValue(values=[get_ast_value(v) for v in value])


class DSLField(object):

    def __init__(self, name, field):
        self.field = field
        self.ast_field = ast.Field(name=ast.Name(value=name), arguments=[])
        self.selection_set = None

    def select(self, *fields):
        if not self.ast_field.selection_set:
            self.ast_field.selection_set = ast.SelectionSet(selections=[])
        self.ast_field.selection_set.selections.extend(selections(*fields))
        return self

    def __call__(self, *args, **kwargs):
        return (self.args)(*args, **kwargs)

    def alias(self, alias):
        self.ast_field.alias = ast.Name(value=alias)
        return self

    def args(self, **args):
        for name, value in args.items():
            arg = self.field.args.get(name)
            arg_type_serializer = get_arg_serializer(arg.type)
            value = arg_type_serializer(value)
            self.ast_field.arguments.append(ast.Argument(name=ast.Name(value=name),
              value=(get_ast_value(value))))

        return self

    @property
    def ast(self):
        return self.ast_field

    def __str__(self):
        return print_ast(self.ast_field)


def field(field, **args):
    if isinstance(field, GraphQLField):
        return (DSLField(field).args)(**args)
    if isinstance(field, DSLField):
        return field
    raise Exception('Received incompatible query field: "{}".'.format(field))


def query(*fields, operation='query'):
    return ast.Document(definitions=[
     ast.OperationDefinition(operation=operation,
       selection_set=ast.SelectionSet(selections=(list(selections(*fields)))))])


def serialize_list(serializer, values):
    assert isinstance(values, collections.Iterable), 'Expected iterable, received "{}"'.format(repr(values))
    result = list()
    for val in values:
        result.append(serializer(val))

    return result


def serialize_string(value):
    return ast.StringValue(value=value)


def serialize_enum(arg_type, value):
    return ast.EnumValue(value=(arg_type.serialize(value)))


def serialize_input_object(arg_type, value):
    serializers = {k:get_arg_serializer(v) for k, v in arg_type.fields.items()}
    result = ast_from_value(value)
    for field in result.fields:
        serialized = serializers[field.name.value](value[field.name.value])
        if isinstance(field.value, ast.ListValue):
            field.value = ast.ListValue(values=serialized)
        else:
            field.value = serialized

    return result


def get_arg_serializer(arg_type):
    if isinstance(arg_type, GraphQLNonNull):
        return get_arg_serializer(arg_type.of_type)
    if isinstance(arg_type, six.string_types):
        return serialize_string
    if isinstance(arg_type, GraphQLInputObjectField):
        return get_arg_serializer(arg_type.type)
    if isinstance(arg_type, GraphQLList):
        inner_serializer = get_arg_serializer(arg_type.of_type)
        return partial(serialize_list, inner_serializer)
    if isinstance(arg_type, GraphQLEnumType):
        return partial(serialize_enum, arg_type)
    if isinstance(arg_type, GraphQLInputObjectType):
        return partial(serialize_input_object, arg_type)
    return lambda value: ast_from_value(str(value) if arg_type.serialize(value) is None else arg_type.serialize(value))


def var(name):
    return ast.Variable(name=name)