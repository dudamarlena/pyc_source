# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/elements/attributetypes.py
# Compiled at: 2017-06-30 10:57:25
from __future__ import unicode_literals, print_function
from ..errors import BadValueError
from ..versioning import VersionSpec
from ..context import Expression, TrueExpression, FalseExpression, dataindex
from ..dbexpression import DBExpression
from ..context.expressiontime import TimeSpan
from ..context.color import Color as ExpressionColor
from ..context.tools import to_expression
from ..elements.elementproxy import ElementProxy
from ..http import StatusCode
from ..compat import implements_to_string, int_types, text_type, string_types, with_metaclass
import re
__all__ = [
 b'Constant',
 b'Text',
 b'Number',
 b'Integer',
 b'Index',
 b'ExpressionAttribute',
 b'ApplicationAttribute',
 b'Reference',
 b'TimeSpanAttribute',
 b'CommaList']
valid_types = []

class AttributeTypeMeta(type):
    """Keeps a registry of all AttributeType classes"""
    registry = {}

    def __new__(cls, name, base, attrs):
        new_class = type.__new__(cls, name, base, attrs)
        if name != b'AttributeType':
            name = getattr(new_class, b'name', name.lower())
            AttributeTypeMeta.registry[name] = new_class
            valid_types.append(name)
        return new_class


def lookup(name):
    """Return the AttributeType of a given name

    Non-string are passed through, unaltered.

    """
    if not isinstance(name, string_types):
        return name
    try:
        return AttributeTypeMeta.registry[name.lower()]
    except KeyError:
        raise KeyError(name)


@implements_to_string
class AttributeTypeBase(object):
    """Base class for attribute types"""
    __slots__ = [
     b'attribute_name', b'element', b'text', b'const']
    translate = False

    def __init__(self, element, attribute_name, text):
        self.attribute_name = attribute_name
        self.element = element
        self.text = text
        if not isinstance(text, string_types):
            self.const = True
        else:
            self.const = b'${' not in text
        super(AttributeTypeBase, self).__init__()

    def __call__(self, context):
        if self.const:
            return self.process(self.text)
        return self.process(context.sub(self.text))

    @classmethod
    def check(self, value):
        return

    @property
    def value(self):
        if not hasattr(self, b'_value'):
            self._value = self.process(self.text)
        return self._value

    @classmethod
    def get_type_display(cls):
        return cls.type_display

    @classmethod
    def display(cls, value):
        if isinstance(value, text_type):
            return (b'"{}"').format(value)

    def process(self, text):
        return text

    def __str__(self):
        return self.text

    def invalid(self, text):
        raise BadValueError((b"In attribute '{}': '{}' is not a valid {}").format(self.attribute_name, text, self.get_type_display()))


class AttributeType(with_metaclass(AttributeTypeMeta, AttributeTypeBase)):
    __slots__ = []


class Constant(AttributeType):
    type_display = b'constant'
    __slots__ = [b'element', b'attribute_name', b'value']

    def __init__(self, element, attribute_name, value):
        self.element = element
        self.attribute_name = attribute_name
        self.value = value

    def __call__(self, context):
        return self.value

    @classmethod
    def get_type_display(self):
        return text_type(self.value)


class Text(AttributeType):
    type_display = b'text'
    __slots__ = []

    def __call__(self, context):
        if self.const:
            return self.text
        return self.process(context.sub(self.text))


class Bytes(AttributeType):
    type_display = b'bytes'
    __slots__ = []

    def process(self, text):
        try:
            text = self.text.encode(b'utf-8')
        except:
            raise BadValueError(b'must be encodeable as UTF-8')

        return text


class Raw(AttributeType):
    type_display = b'raw'
    __slots__ = []

    def __call__(self, context):
        return self.text


class Number(AttributeType):
    type_display = b'number'
    __slots__ = []

    def process(self, text):
        try:
            return float(text)
        except ValueError:
            self.invalid(text)

    @classmethod
    def check(cls, value):
        if b'${' not in value:
            try:
                float(value)
            except:
                return (b'expected a number, not "{}"').format(value)


class Integer(AttributeType):
    type_display = b'integer'
    __slots__ = []

    def process(self, text):
        try:
            return int(float(text))
        except ValueError:
            self.invalid(text)

    @classmethod
    def display(cls, value):
        if isinstance(value, int_types):
            return text_type(value)

    @classmethod
    def check(cls, value):
        if b'${' not in value:
            try:
                int(float(value))
            except:
                return (b'expected an integer, not "{}"').format(value)


class Color(AttributeType):
    type_display = b'color'
    __slots__ = []

    def __call__(self, context):
        return ExpressionColor.parse(context.sub(self.text))

    @classmethod
    def check(cls, value):
        if b'${' not in value:
            try:
                ExpressionColor.parse(value)
            except Exception as e:
                return text_type(e)


class Index(AttributeType):
    type_display = b'index'
    __slots__ = []

    def __call__(self, context):
        return context.get_sub(self.text)


class Reference(AttributeType):
    type_display = b'reference'
    __slots__ = [b'reference']

    def __init__(self, element, attribute_name, text):
        super(Reference, self).__init__(element, attribute_name, text)
        self.reference = dataindex.parse(self.text)

    def __call__(self, context):
        return self.reference


class Element(AttributeType):
    type_display = b'element'
    __slots__ = []

    def __call__(self, context):
        element_ref = context.sub(self.text)
        app, element = self.element.archive.get_element(element_ref, app=context.get(b'.app'))
        return ElementProxy(context, app, element)


class ElementRef(AttributeType):
    type_display = b'element reference'
    __slots__ = []

    def __call__(self, context):
        return context.sub(self.text)


class ExpressionAttribute(AttributeType):
    type_display = b'expression'
    name = b'expression'
    __slots__ = [b'element', b'attribute_name', b'exp']

    def __init__(self, element, attribute_name, text):
        self.element = element
        self.attribute_name = attribute_name
        self.exp = Expression(text)

    def __call__(self, context):
        return self.exp.eval(context)

    @classmethod
    def display(cls, value):
        return to_expression(None, value)

    @classmethod
    def check(self, value):
        try:
            Expression(value).compile()
        except Exception as e:
            return text_type(e)

        return
        return


class FunctionAttribute(AttributeType):
    type_display = b'function'
    name = b'function'
    __slots__ = [b'element', b'attribute_name', b'exp']

    def __init__(self, element, attribute_name, text):
        self.element = element
        self.attribute_name = attribute_name
        self.exp = Expression(text)

    def __call__(self, context):
        return self.exp.make_function(context)

    @classmethod
    def check(self, value):
        try:
            Expression(value).compile()
        except Exception as e:
            return text_type(e)

        return
        return


class ApplicationAttribute(AttributeType):
    type_display = b'application reference'
    name = b'application'
    __slots__ = [b'element', b'attribute_name', b'text']

    def __init__(self, element, attribute_name, text):
        self.element = element
        self.attribute_name = attribute_name
        self.text = text

    def __call__(self, context):
        app_name = context.sub(self.text)
        if app_name == b'':
            raise BadValueError(b'app name must not be an empty string')
        if not app_name:
            return None
        else:
            try:
                app = self.element.archive.find_app(app_name)
            except Exception as e:
                raise BadValueError(text_type(e))

            return app


class DBExpressionAttribute(AttributeType):
    type_display = b'database expression'
    name = b'dbexpression'
    __slots__ = [b'element', b'attribute_name', b'text']

    def __init__(self, element, attribute_name, text):
        self.element = element
        self.attribute_name = attribute_name
        self.text = text

    def __call__(self, context):
        text = context.sub(self.text)
        if text:
            return DBExpression(text)
        else:
            return

    @classmethod
    def check(self, value):
        if b'${' not in value:
            try:
                DBExpression(value).compile()
            except Exception as e:
                return text_type(e)

            return
        return


class Boolean(ExpressionAttribute):
    type_display = b'boolean'
    name = b'boolean'
    __slots__ = [b'attribute_name', b'text', b'exp']

    def __init__(self, element, attribute_name, text):
        self.attribute_name = attribute_name
        self.text = text
        if text in ('yes', 'True'):
            self.exp = TrueExpression()
        elif text in ('no', 'False'):
            self.exp = FalseExpression()
        else:
            self.exp = Expression(text)

    @classmethod
    def display(cls, value):
        if isinstance(value, bool):
            if value:
                return b'yes'
            return b'no'

    def __call__(self, context):
        return bool(self.exp.eval(context))

    @classmethod
    def check(self, value):
        try:
            Expression(value).compile()
        except Exception as e:
            return text_type(e)

        return
        return


class DictExpression(ExpressionAttribute):
    type_display = b'dict expression'
    name = b'dict'
    __slots__ = [b'element', b'exp']

    def __init__(self, element, attribute_name, text):
        self.attribute_name = attribute_name
        self.exp = Expression(text)

    def __call__(self, context):
        d = self.exp.eval(context)
        if not (hasattr(d, b'items') and hasattr(d, b'__getitem__')):
            raise BadValueError(b'must be a dictionary or similar type')
        return d

    @classmethod
    def check(self, value):
        try:
            Expression(value).compile()
        except Exception as e:
            return text_type(e)

        return
        return


class TimeSpanAttribute(AttributeType):
    type_display = b'timespan'
    name = b'timespan'
    __slots__ = []

    def process(self, text):
        return TimeSpan(text)

    @classmethod
    def check(self, value):
        if b'${' not in value:
            try:
                TimeSpan(value)
            except Exception as e:
                return text_type(e)

            return
        return


class CommaList(AttributeType):
    type_display = b'comma list'
    name = b'commalist'
    __slots__ = []

    def process(self, text):
        if b',' in text:
            return [ t.strip() for t in text.split(b',') ]
        else:
            return [
             text]


class Namespace(AttributeType):
    type_display = b'namespace'
    name = b'namespace'
    __slots__ = []


class Templates(AttributeType):
    type_display = b'list of template paths'
    name = b'templates'
    __slots__ = []

    def __call__(self, context):
        sub = context.sub
        text = self.text
        if b',' in text:
            return [ sub(t.strip()) for t in text.split(b',') ]
        else:
            return [
             text.strip()]


class Template(AttributeType):
    type_display = b'template path'
    name = b'template'
    __slots__ = []

    def __call__(self, context):
        text = context.sub(self.text).strip()
        return text


class Version(AttributeType):
    type_display = b'version spec'
    name = b'version'
    __slots__ = []

    def __call__(self, context):
        text = VersionSpec(self.text)
        return text

    @classmethod
    def check(self, value):
        try:
            VersionSpec(value)
        except Exception as e:
            return text_type(e)

        return
        return


class RegEx(AttributeType):
    type_display = b'regular expression'
    name = b'regex'
    __slots__ = [b'_regex']

    def __call__(self, contet):
        try:
            regex = re.compile(self.text)
        except Exception as error:
            raise BadValueError((b"failed to compile '{}' as a regex ({})").format(self.text, error))

        return regex


class HTTPStatus(AttributeType):
    type_display = b'http status code'
    name = b'httpstatus'
    __slots__ = []

    def __call__(self, context):
        if self.text.isdigit():
            return int(self.text)
        try:
            status_code = StatusCode(self.text.lower())
        except KeyError:
            raise BadValueError((b"'{}' is not a valid status code").format(self.text))

        status = int(status_code)
        return status

    @classmethod
    def check(self, value):
        try:
            StatusCode(value.lower())
        except Exception as e:
            return ValueError((b"'{}' is not a valid status code").format(value))

        return
        return

    @classmethod
    def display(cls, value):
        return text_type(StatusCode(value)).upper()


if __name__ == b'__main__':
    from moya.context import Context
    c = Context()
    c[b'foo'] = [1, 2, 3, 4, 5]
    c[b'fruit'] = [b'apples', b'orange', b'pears']
    t = Number(b'${foo.2}.14')
    print(t.__call__)
    print(repr(t))
    print(t(c))
    i = Index(b'fruit.${foo.1}')
    print(i(c))