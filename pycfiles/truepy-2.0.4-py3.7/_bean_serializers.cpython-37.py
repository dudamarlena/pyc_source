# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/truepy/_bean_serializers.py
# Compiled at: 2020-01-23 12:02:01
# Size of source mod 2**32: 4963 bytes
import sys, types
from datetime import datetime, timedelta
from ._bean import bean_serializer, bean_deserializer, camel_to_snake, deserialize, value_to_xml, UnknownFragmentException

@bean_serializer(bool)
def bool_serializer(value):
    return value_to_xml('true' if value else 'false', 'boolean')


@bean_serializer(int)
def int_serializer(value):
    return value_to_xml(str(value), 'int')


@bean_serializer(str)
def str_serializer(value):
    return value_to_xml(value, 'string')


if sys.version_info.major < 3:

    @bean_serializer(unicode)
    def str_serializer_py2_unicode(value):
        return value_to_xml(value, 'string')


@bean_serializer(datetime)
def datetime_serializer(v):
    timedelta_since_epoch = v - datetime.strptime('1970-01-01 UTC', '%Y-%m-%d %Z')
    ms_since_epoch = int(timedelta_since_epoch.total_seconds() * 1000)
    return value_to_xml(str(ms_since_epoch), 'long', 'java.util.Date')


@bean_deserializer
def bool_deserializer(element):
    if element.tag == 'boolean':
        value = element.text.strip()
        if value == 'true':
            return True
        if value == 'false':
            return False
        raise ValueError('invalid boolean value: %s', value)
    else:
        raise UnknownFragmentException()


@bean_deserializer
def int_deserializer(element):
    if element.tag == 'int':
        return int(element.text.strip())
    raise UnknownFragmentException()


@bean_deserializer
def str_deserializer(element):
    if element.tag == 'string':
        return (element.text or '').strip()
    raise UnknownFragmentException()


@bean_deserializer
def datetime_deserializer(element):
    if element.tag == 'object':
        if element.attrib.get('class', None) == 'java.util.Date':
            ms_since_epoch = int(element.find('.//long').text)
            return datetime.strptime('1970-01-01 UTC', '%Y-%m-%d %Z') + timedelta(milliseconds=ms_since_epoch)
    raise UnknownFragmentException()


_DESERIALIZER_CLASSES = {}

def default_bean_deserialize(self, element):
    """The default bean deserialiser for classes decorated with
    `@`:meth:`~truepy._bean_serializers.bean_class`.

    This function will call the constructor with all properties read from
    element as named arguments. If this fails with `TypeError`, it will call
    the empty constructor and then set all properties.

    :param xml.etree.ElementTree.Element element: The XML fragment to
        deserialise.
    :return: an object
    :rtype: self
    """
    properties = {camel_to_snake(e.attrib['property']):deserialize(e[0]) for e in element.findall('.//void')}
    try:
        return self(**properties)
    except TypeError:
        pass

    result = self()
    for name, value in properties.items():
        setattr(result, name, value)

    return result


def bean_class(class_name):
    """Marks a class as deserialisable and sets its class name.

    A class decorated with this decorator does not need to define the
    `bean_class` attribute.

    The class method `_bean_deserialize` will be called when the XML fragment
    `<object class="(class_name)">...</object>` is encountered. If the class
    does not have this callable, it will be set to
    :meth:`~truepy._bean_serializers.default_bean_deserialize`.

    :param str class_name: The class name to use for this class.
    """

    def inner(c):
        if not callable(getattr(c, '_bean_deserialize', None)):
            c._bean_deserialize = types.MethodType(default_bean_deserialize, c)
        c.bean_class = class_name
        _DESERIALIZER_CLASSES[class_name] = c
        return c

    return inner


@bean_deserializer
def object_deserializer(element):
    """Deserialises XML for registered bean classes.

    The XML must be like `<object class="(class_name)">...</object>`.

    A class is registered by decorating it with `@`:meth:`~bean_class`.
    """
    try:
        deserializer_class = _DESERIALIZER_CLASSES[element.attrib['class']]
        return deserializer_class._bean_deserialize(element)
    except KeyError:
        raise UnknownFragmentException()