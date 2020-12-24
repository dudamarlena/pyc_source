# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\Conversions.py
# Compiled at: 2005-08-09 10:24:01
__doc__ = '\nThe implementation of the XPath object type conversions.\n\nCopyright 2000-2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import types
from xml.dom import Node
from Ft.Lib import number, boolean
StringValue = lambda obj: _strConversions.get(type(obj), _strUnknown)(obj)
NumberValue = lambda obj: _numConversions.get(type(obj), _numUnknown)(obj)
BooleanValue = lambda obj: _boolConversions.get(type(obj), _boolUnknown)(obj)

def _strUnknown(obj):
    if hasattr(obj, 'nodeType'):
        _strConversions[type(obj)] = _strInstance
        return _strInstance(obj)
    return ''


def _strInstance(obj):
    if hasattr(obj, 'stringValue'):
        return obj.stringValue
    elif hasattr(obj, 'nodeType'):
        node_type = obj.nodeType
        if node_type in [Node.ELEMENT_NODE, Node.DOCUMENT_NODE]:
            text_elem_children = filter(lambda x: x.nodeType in [Node.TEXT_NODE, Node.ELEMENT_NODE], obj.childNodes)
            return reduce(lambda x, y: StringValue(x) + StringValue(y), text_elem_children, '')
        if node_type in [Node.ATTRIBUTE_NODE, NAMESPACE_NODE]:
            return obj.value
        if node_type in [Node.PROCESSING_INSTRUCTION_NODE, Node.COMMENT_NODE, Node.TEXT_NODE]:
            return obj.data
    return ''


def _strFloat(float):
    if number.finite(float):
        if float == round(float):
            return unicode(str(long(float)))
        else:
            return '%0.12g' % float
    elif number.isnan(float):
        return 'NaN'
    elif float < 0:
        return '-Infinity'
    else:
        return 'Infinity'


_strConversions = {str: unicode, unicode: unicode, int: lambda i: unicode(str(i)), 
   long: lambda l: unicode(str(l)), 
   float: _strFloat, boolean.BooleanType: lambda b: unicode(str(b)), 
   types.InstanceType: _strInstance, list: lambda x: x and _strConversions.get(type(x[0]), _strUnknown)(x[0]) or ''}

def _numString(string):
    try:
        return float(string)
    except:
        return number.nan


_numUnknown = lambda obj: _numString(StringValue(obj))
_numConversions = {int: float, long: float, float: float, boolean.BooleanType: float, str: _numString, unicode: _numString}
_boolConversions = {boolean.BooleanType: boolean.bool, int: boolean.bool, long: boolean.bool, float: boolean.bool, str: boolean.bool, unicode: boolean.bool, list: boolean.bool}
_boolUnknown = lambda obj: boolean.bool(StringValue(obj))
try:
    from _conversions import *
except:
    from Ft.Xml.XPath import NAMESPACE_NODE