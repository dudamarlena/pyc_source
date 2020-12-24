# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jphillips/go/src/github.com/lyft/toasted-marshmallow/toastedmarshmallow/jit.py
# Compiled at: 2019-06-18 11:53:25
# Size of source mod 2**32: 28312 bytes
import base64, keyword, re
from abc import ABCMeta, abstractmethod
from collections import Mapping
import attr
from six import exec_, iteritems, add_metaclass, text_type, string_types
from marshmallow import missing, Schema, fields
from marshmallow.base import SchemaABC
from .compat import is_overridden
from .utils import IndentedString
_VALID_IDENTIFIER = re.compile('[a-zA-Z_][a-zA-Z0-9_]*')

def field_symbol_name(field_name):
    """Generates the symbol name to be used when accessing a field in generated
    code.

    If the field name isn't a valid identifier name, synthesizes a name by
    base64 encoding the fieldname.
    """
    if not _VALID_IDENTIFIER.match(field_name):
        field_name = str(base64.b64encode(field_name.encode('utf-8')).decode('utf-8').strip('='))
    return '_field_{field_name}'.format(field_name=field_name)


def attr_str(attr_name):
    """Gets the string to use when accessing an attribute on an object.

    Handles case where the attribute name collides with a keyword and would
    therefore be illegal to access with dot notation.
    """
    if keyword.iskeyword(attr_name):
        return 'getattr(obj, "{0}")'.format(attr_name)
    else:
        return 'obj.{0}'.format(attr_name)


@add_metaclass(ABCMeta)
class FieldSerializer(object):
    __doc__ = 'Base class for generating code to serialize a field.\n    '

    def __init__(self, context=None):
        """
        :param context: The context for the current Jit
        """
        self.context = context or JitContext()

    @abstractmethod
    def serialize(self, attr_name, field_symbol, assignment_template, field_obj):
        """Generates the code to pull a field off of an object into the result.

        :param attr_name: The name of the attribute being accessed/
        :param field_symbol: The symbol to use when accessing the field.  Should
            be generated via field_symbol_name.
        :param assignment_template: A string template to use when generating
            code.  The assignment template is passed into the serializer and
            has a single possitional placeholder for string formatting.  An
            example of a value that may be passed into assignment_template is:
            `res['some_field'] = {0}`
        :param field_obj: The instance of the Marshmallow field being
            serialized.
        :return: The code to pull a field off of the object passed in.
        """
        pass


class InstanceSerializer(FieldSerializer):
    __doc__ = "Generates code for accessing fields as if they were instance variables.\n\n    For example, generates:\n\n    res['some_value'] = obj.some_value\n    "

    def serialize(self, attr_name, field_symbol, assignment_template, field_obj):
        return IndentedString(assignment_template.format(attr_str(attr_name)))


class DictSerializer(FieldSerializer):
    __doc__ = "Generates code for accessing fields as if they were a dict, generating\n    the proper code for handing missing fields as well.  For example, generates:\n\n    # Required field with no default\n    res['some_value'] = obj['some_value']\n\n    # Field with a default.  some_value__default will be injected at exec time.\n    res['some_value'] = obj.get('some_value', some_value__default)\n\n    # Non required field:\n    if 'some_value' in obj:\n        res['some_value'] = obj['some_value']\n    "

    def serialize(self, attr_name, field_symbol, assignment_template, field_obj):
        body = IndentedString()
        if self.context.is_serializing:
            default_str = 'default'
            default_value = field_obj.default
        else:
            default_str = 'missing'
            default_value = field_obj.missing
        if field_obj.required:
            body += assignment_template.format('obj["{attr_name}"]'.format(attr_name=attr_name))
            return body
        else:
            if default_value == missing:
                body += 'if "{attr_name}" in obj:'.format(attr_name=attr_name)
                with body.indent():
                    body += assignment_template.format('obj["{attr_name}"]'.format(attr_name=attr_name))
            else:
                if callable(default_value):
                    default_str += '()'
                body += assignment_template.format('obj.get("{attr_name}", {field_symbol}__{default_str})'.format(attr_name=attr_name,
                  field_symbol=field_symbol,
                  default_str=default_str))
            return body


class HybridSerializer(FieldSerializer):
    __doc__ = "Generates code for accessing fields as if they were a hybrid object.\n\n    Hybrid objects are objects that don't inherit from `Mapping`, but do\n    implement `__getitem__`.  This means we first have to attempt a lookup by\n    key, then fall back to looking up by instance variable.\n\n    For example, generates:\n\n    try:\n        value = obj['some_value']\n    except (KeyError, AttributeError, IndexError, TypeError):\n        value = obj.some_value\n    res['some_value'] = value\n    "

    def serialize(self, attr_name, field_symbol, assignment_template, field_obj):
        body = IndentedString()
        body += 'try:'
        with body.indent():
            body += 'value = obj["{attr_name}"]'.format(attr_name=attr_name)
        body += 'except (KeyError, AttributeError, IndexError, TypeError):'
        with body.indent():
            body += 'value = {attr_str}'.format(attr_str=(attr_str(attr_name)))
        body += assignment_template.format('value')
        return body


@attr.s
class JitContext(object):
    __doc__ = " Bag of properties to keep track of the context of what's being jitted.\n\n    "
    namespace = attr.ib(default={})
    use_inliners = attr.ib(default=True)
    schema_stack = attr.ib(default=(attr.Factory(set)))
    only = attr.ib(default=None)
    exclude = attr.ib(default=(set()))
    is_serializing = attr.ib(default=True)


@add_metaclass(ABCMeta)
class FieldInliner(object):
    __doc__ = "Base class for generating code to serialize a field.\n\n    Inliners are used to generate the code to validate/parse fields without\n    having to bounce back into the underlying marshmallow code.  While this is\n    somewhat fragile as it requires the inliners to be kept in sync with the\n    underlying implementation, it's good for a >2X speedup on benchmarks.\n    "

    @abstractmethod
    def inline(self, field, context):
        pass


class StringInliner(FieldInliner):

    def inline(self, field, context):
        """Generates a template for inlining string serialization.

        For example, generates "unicode(value) if value is not None else None"
        to serialize a string in Python 2.7
        """
        if is_overridden(field._serialize, fields.String._serialize):
            return
        else:
            result = text_type.__name__ + '({0})'
            result += ' if {0} is not None else None'
            if not context.is_serializing:
                string_type_strings = ','.join([x.__name__ for x in string_types])
                result = '(' + result + ') if (isinstance({0}, (' + string_type_strings + ')) or {0} is None) else dict()["error"]'
            return result


class BooleanInliner(FieldInliner):

    def inline(self, field, context):
        """Generates a template for inlining boolean serialization.

        For example, generates:

        (
            (value in __some_field_truthy) or
            (False if value in __some_field_falsy else bool(value))
        )

        This is somewhat fragile but it tracks what Marshmallow does.
        """
        if is_overridden(field._serialize, fields.Boolean._serialize):
            return
        else:
            truthy_symbol = '__{0}_truthy'.format(field.name)
            falsy_symbol = '__{0}_falsy'.format(field.name)
            context.namespace[truthy_symbol] = field.truthy
            context.namespace[falsy_symbol] = field.falsy
            result = '(({0} in ' + truthy_symbol + ') or (False if {0} in ' + falsy_symbol + ' else dict()["error"]))'
            return result + ' if {0} is not None else None'


class NumberInliner(FieldInliner):

    def inline(self, field, context):
        """Generates a template for inlining string serialization.

        For example, generates "float(value) if value is not None else None"
        to serialize a float.  If `field.as_string` is `True` the result will
        be coerced to a string if not None.
        """
        if is_overridden(field._validated, fields.Number._validated) or is_overridden(field._serialize, fields.Number._serialize) or field.num_type not in (int, float):
            return
        else:
            result = field.num_type.__name__ + '({0})'
            if field.as_string:
                if context.is_serializing:
                    result = 'str({0})'.format(result)
            if field.allow_none is True:
                result += ' if {0} is not None else None'
            return result


class NestedInliner(FieldInliner):

    def inline(self, field, context):
        """Generates a template for inlining nested field.

        This doesn't pass tests yet in Marshmallow, namely due to issues around
        code expecting the context of nested schema to be populated on first
        access, so disabling for now.
        """
        if is_overridden(field._serialize, fields.Nested._serialize):
            return
        else:
            if not (isinstance(field.nested, type) and issubclass(field.nested, SchemaABC)):
                return
            else:
                if field.nested.__class__ in context.schema_stack:
                    return
                method_name = '__nested_{}_serialize'.format(field_symbol_name(field.name))
                old_only = context.only
                old_exclude = context.exclude
                old_namespace = context.namespace
                context.only = set(field.only) if field.only else None
                context.exclude = set(field.exclude)
                context.namespace = {}
                for only_field in old_only or []:
                    if only_field.startswith(field.name + '.'):
                        if not context.only:
                            context.only = set()
                        context.only.add(only_field[len(field.name + '.'):])

                for only_field in list(context.only or []):
                    if '.' in only_field:
                        if not context.only:
                            context.only = set()
                        context.only.add(only_field.split('.')[0])

                for exclude_field in old_exclude:
                    if exclude_field.startswith(field.name + '.'):
                        context.exclude.add(exclude_field[len(field.name + '.'):])

                serialize_method = generate_marshall_method(field.schema, context)
                if serialize_method is None:
                    return
                context.namespace = old_namespace
                context.only = old_only
                context.exclude = old_exclude
                context.namespace[method_name] = serialize_method
                if field.many:
                    return '[' + method_name + '(_x) for _x in {0}] if {0} is not None else None'
            return method_name + '({0}) if {0} is not None else None'


INLINERS = {fields.String: StringInliner(), 
 fields.Number: NumberInliner(), 
 fields.Boolean: BooleanInliner()}
EXPECTED_TYPE_TO_CLASS = {'object':InstanceSerializer, 
 'dict':DictSerializer, 
 'hybrid':HybridSerializer}

def _should_skip_field(field_name, field_obj, context):
    load_only = getattr(field_obj, 'load_only', False)
    dump_only = getattr(field_obj, 'dump_only', False)
    if isinstance(field_obj, fields.Method):
        load_only = bool(field_obj.deserialize_method_name) and not bool(field_obj.serialize_method_name)
        dump_only = bool(field_obj.serialize_method_name) and not bool(field_obj.deserialize_method_name)
    if load_only:
        if context.is_serializing:
            return True
    if dump_only:
        if not context.is_serializing:
            return True
    if context.only:
        if field_name not in context.only:
            return True
    if context.exclude:
        if field_name in context.exclude:
            return True
    return False


def generate_transform_method_body(schema, on_field, context):
    """Generates the method body for a schema and a given field serialization
    strategy.
    """
    body = IndentedString()
    body += 'def {method_name}(obj):'.format(method_name=(on_field.__class__.__name__))
    with body.indent():
        if schema.dict_class is dict:
            body += 'res = {}'
        else:
            body += 'res = dict_class()'
        if not context.is_serializing:
            body += '__res_get = res.get'
        for field_name, field_obj in iteritems(schema.fields):
            if _should_skip_field(field_name, field_obj, context):
                pass
            else:
                attr_name, destination = _get_attr_and_destination(context, field_name, field_obj)
                result_key = ''.join([
                 schema.prefix or '', destination])
                field_symbol = field_symbol_name(field_name)
                assignment_template = ''
                value_key = '{0}'
                jit_options = getattr(schema.opts, 'jit_options', {})
                no_callable_fields = jit_options.get('no_callable_fields') or not context.is_serializing
                if not no_callable_fields:
                    assignment_template = 'value = {0}; value = value() if callable(value) else value; '
                    value_key = 'value'
                inliner = inliner_for_field(context, field_obj)
                if inliner:
                    assignment_template += _generate_inlined_access_template(inliner, result_key, no_callable_fields)
                else:
                    assignment_template += _generate_fallback_access_template(context, field_name, field_obj, result_key, value_key)
                if not field_obj._CHECK_ATTRIBUTE:
                    body += assignment_template.format('None')
                    context.namespace['__marshmallow_missing'] = missing
                    body += 'if res["{key}"] is __marshmallow_missing:'.format(key=result_key)
                    with body.indent():
                        body += 'del res["{key}"]'.format(key=result_key)
                else:
                    serializer = on_field
                    if not _VALID_IDENTIFIER.match(attr_name):
                        serializer = DictSerializer(context)
                    body += serializer.serialize(attr_name, field_symbol, assignment_template, field_obj)
                    if not context.is_serializing:
                        if field_obj.load_from:
                            body += 'if "{key}" not in res:'.format(key=result_key)
                            with body.indent():
                                body += serializer.serialize(field_obj.load_from, field_symbol, assignment_template, field_obj)
                        if not context.is_serializing:
                            if field_obj.required:
                                body += 'if "{key}" not in res:'.format(key=result_key)
                                with body.indent():
                                    body += 'raise ValueError()'
                            if field_obj.allow_none is not True:
                                body += 'if __res_get("{key}", res) is None:'.format(key=result_key)
                                with body.indent():
                                    body += 'raise ValueError()'
                            if field_obj.validators or is_overridden(field_obj._validate, fields.Field._validate):
                                body += 'if "{key}" in res:'.format(key=result_key)
                                with body.indent():
                                    body += '{field_symbol}__validate(res["{result_key}"])'.format(field_symbol=field_symbol,
                                      result_key=result_key)

        body += 'return res'
    return body


def _generate_fallback_access_template(context, field_name, field_obj, result_key, value_key):
    field_symbol = field_symbol_name(field_name)
    transform_method_name = 'serialize'
    if not context.is_serializing:
        transform_method_name = 'deserialize'
    key_name = field_name
    if not context.is_serializing:
        key_name = field_obj.load_from or field_name
    return 'res["{key}"] = {field_symbol}__{transform}({value_key}, "{key_name}", obj)'.format(key=result_key,
      field_symbol=field_symbol,
      transform=transform_method_name,
      key_name=key_name,
      value_key=value_key)


def _get_attr_and_destination(context, field_name, field_obj):
    attr_name = field_name
    destination = field_name
    if context.is_serializing:
        destination = field_obj.dump_to or field_name
    if field_obj.attribute:
        if context.is_serializing:
            attr_name = field_obj.attribute
        else:
            destination = field_obj.attribute
    return (
     attr_name, destination)


def _generate_inlined_access_template(inliner, key, no_callable_fields):
    """Generates the code to access a field with an inliner."""
    value_key = 'value'
    assignment_template = ''
    if not no_callable_fields:
        assignment_template += 'value = {0}; '.format(inliner.format(value_key))
    else:
        assignment_template += 'value = {0}; '
        value_key = inliner.format('value')
    assignment_template += 'res["{key}"] = {value_key}'.format(key=key,
      value_key=value_key)
    return assignment_template


def inliner_for_field(context, field_obj):
    if context.use_inliners:
        inliner = None
        for field_type, inliner_class in iteritems(INLINERS):
            if isinstance(field_obj, field_type):
                inliner = inliner_class.inline(field_obj, context)
                if inliner:
                    break

        return inliner


def generate_method_bodies(schema, context):
    """Generate 3 method bodies for marshalling objects, dictionaries, or hybrid
    objects.
    """
    result = IndentedString()
    result += generate_transform_method_body(schema, InstanceSerializer(context), context)
    result += generate_transform_method_body(schema, DictSerializer(context), context)
    result += generate_transform_method_body(schema, HybridSerializer(context), context)
    return str(result)


class SerializeProxy(object):
    __doc__ = 'Proxy object for calling serializer methods.\n\n    Initially trace calls to serialize and if the number of calls\n    of a specific type crosses `threshold` swaps out the implementation being\n    used for the most specialized one available.\n    '

    def __init__(self, dict_serializer, hybrid_serializer, instance_serializer, threshold=100):
        self.dict_serializer = dict_serializer
        self.hybrid_serializer = hybrid_serializer
        self.instance_serializer = instance_serializer
        self.threshold = threshold
        self.dict_count = 0
        self.hybrid_count = 0
        self.instance_count = 0
        self._call = self.tracing_call
        if not threshold:
            self._call = self.no_tracing_call

    def __call__(self, obj):
        return self._call(obj)

    def tracing_call(self, obj):
        """Dispatcher which traces calls and specializes if possible.
        """
        try:
            if isinstance(obj, Mapping):
                self.dict_count += 1
                return self.dict_serializer(obj)
            if hasattr(obj, '__getitem__'):
                self.hybrid_count += 1
                return self.hybrid_serializer(obj)
            self.instance_count += 1
            return self.instance_serializer(obj)
        finally:
            non_zeros = [x for x in [
             self.dict_count,
             self.hybrid_count,
             self.instance_count] if x > 0]
            if len(non_zeros) > 1:
                self._call = self.no_tracing_call
            else:
                if self.dict_count >= self.threshold:
                    self._call = self.dict_serializer
                else:
                    if self.hybrid_count >= self.threshold:
                        self._call = self.hybrid_serializer
                    else:
                        if self.instance_count >= self.threshold:
                            self._call = self.instance_serializer

    def no_tracing_call(self, obj):
        """Dispatcher with no tracing.
        """
        if isinstance(obj, Mapping):
            return self.dict_serializer(obj)
        else:
            if hasattr(obj, '__getitem__'):
                return self.hybrid_serializer(obj)
            return self.instance_serializer(obj)


def generate_marshall_method(schema, context=missing, threshold=100):
    """Generates a function to marshall objects for a given schema.

    :param schema: The Schema to generate a marshall method for.
    :param threshold: The number of calls of the same type to observe before
        specializing the marshal method for that type.
    :return: A Callable that can be used to marshall objects for the schema
    """
    if is_overridden(schema.get_attribute, Schema.get_attribute):
        return
    else:
        if context is missing:
            context = JitContext()
        else:
            context.namespace = {}
            context.namespace['dict_class'] = lambda : schema.dict_class()
            jit_options = getattr(schema.opts, 'jit_options', {})
            context.schema_stack.add(schema.__class__)
            result = generate_method_bodies(schema, context)
            context.schema_stack.remove(schema.__class__)
            namespace = context.namespace
            for key, value in iteritems(schema.fields):
                if value.attribute:
                    if '.' in value.attribute:
                        return
                    namespace[field_symbol_name(key) + '__serialize'] = value._serialize
                    namespace[field_symbol_name(key) + '__deserialize'] = value._deserialize
                    namespace[field_symbol_name(key) + '__validate_missing'] = value._validate_missing
                    namespace[field_symbol_name(key) + '__validate'] = value._validate
                    if value.default is not missing:
                        namespace[field_symbol_name(key) + '__default'] = value.default
                    if value.missing is not missing:
                        namespace[field_symbol_name(key) + '__missing'] = value.missing

            exec_(result, namespace)
            proxy = None
            marshall_method = None
            if not context.is_serializing:
                marshall_method = namespace[DictSerializer.__name__]
            else:
                if jit_options.get('expected_marshal_type') in EXPECTED_TYPE_TO_CLASS:
                    marshall_method = namespace[EXPECTED_TYPE_TO_CLASS[jit_options['expected_marshal_type']].__name__]
                else:
                    marshall_method = SerializeProxy((namespace[DictSerializer.__name__]),
                      (namespace[HybridSerializer.__name__]),
                      (namespace[InstanceSerializer.__name__]),
                      threshold=threshold)
                    proxy = marshall_method

        def marshall(obj, many=False):
            if many:
                return [marshall_method(x) for x in obj]
            else:
                return marshall_method(obj)

        if proxy:
            marshall.proxy = proxy
        marshall._source = result
        return marshall


def generate_unmarshall_method(schema, context=missing):
    context = context or JitContext()
    context.is_serializing = False
    return generate_marshall_method(schema, context)