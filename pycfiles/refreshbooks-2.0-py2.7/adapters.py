# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/refreshbooks/adapters.py
# Compiled at: 2014-01-20 11:54:38
from lxml import etree, objectify
import decimal
from refreshbooks import elements, client
_stringable_types = frozenset([float, int, decimal.Decimal])

def encode_as_simple_from_element(name, value):
    """Creates an etree element following the simple field convention. To 
    ease reuse of returned data in future calls, we smash anything that looks 
    like an ObjectifiedDataElement to unicode:
    
        >>> value = objectify.DataElement(5)
        >>> element = encode_as_simple('foo', value)
        >>> element.tag == 'foo'
        True
        >>> element.text == '5'
        True
    """
    return encode_as_simple(name, value.text)


def encode_as_simple(name, value):
    """Creates an etree element following the simple field convention. Values
    are assumed to be strs, unicodes, ints, floats, or Decimals:
    
        >>> element = encode_as_simple('foo', '5')
        >>> element.tag == 'foo'
        True
        >>> element.text == '5'
        True
        >>> element = encode_as_simple('bar', 8)
        >>> element.tag == 'bar'
        True
        >>> element.text == '8'
        True
    """
    if isinstance(value, objectify.ObjectifiedDataElement):
        return encode_as_simple(name, unicode(value))
    if type(value) in _stringable_types:
        value = str(value)
    return elements.field(name, value)


def encode_as_dict(_name, **kwargs):
    return elements.type(_name, [ encode_parameter(name, value) for name, value in kwargs.items() ])


def encode_as_list_of_dicts(name, *args):
    return elements.type(name, [ encode_parameter(name, value) for name, value in args ])


def encode_parameter(name, value):
    try:
        return encode_as_simple_from_element(name, value)
    except AttributeError:
        try:
            return encode_as_dict(name, **value)
        except TypeError:
            try:
                return encode_as_simple(name, value)
            except TypeError:
                return encode_as_list_of_dicts(name, *value)


def xml_request(method, **params):
    request_document = elements.request(method, [ encode_parameter(name, value) for name, value in params.items()
                                                ])
    return etree.tostring(request_document)


def fail_to_exception_response(response):
    if response.attrib['status'] == 'fail':
        raise client.FailedRequest(response.error)
    return response