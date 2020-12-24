# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\CoreFunctions.py
# Compiled at: 2006-09-22 13:17:17
__doc__ = '\nThe implementation of the core functions from XPath 1.0.\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import warnings
from xml.dom import Node
from Ft import TranslateMessage as _
from Ft.Lib import number, boolean, Set
from Ft.Xml import EMPTY_NAMESPACE, XML_NAMESPACE
from Ft.Xml.XPath import NAMESPACE_NODE
from Ft.Xml.XPath import Conversions, RuntimeException
from Ft.Xml.XPath.XPathTypes import NodesetType, NumberType
from Ft.Xml.XPath.XPathTypes import StringType as XPathStringType

def Last(context):
    """Function: <number> last()"""
    return float(context.size)


def Position(context):
    """Function: <number> position()"""
    return float(context.position)


def Count(context, nodeSet):
    """Function: <number> count(<node-set>)"""
    if not isinstance(nodeSet, NodesetType):
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'count', _('expected node-set argument'))
    return float(len(nodeSet))


def Id(context, object_):
    """Function: <node-set> id(<object>)"""
    if not isinstance(object_, NodesetType):
        st = Conversions.StringValue(object_)
        id_list = st.split()
    else:
        id_list = [ Conversions.StringValue(n) for n in object_ ]
    id_list = Set.Unique(id_list)
    doc = context.node.rootNode
    nodeset = []
    for id in id_list:
        element = doc.getElementById(id)
        if element:
            nodeset.append(element)

    return nodeset


def LocalName(context, nodeSet=None):
    """Function: <string> local-name(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    elif not isinstance(nodeSet, NodesetType):
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'local-name', _('expected node-set'))
    elif not nodeSet:
        return ''
    else:
        nodeSet.sort()
        node = nodeSet[0]
    node_type = getattr(node, 'nodeType', None)
    if node_type in (Node.ELEMENT_NODE, Node.ATTRIBUTE_NODE):
        return node.localName or ''
    elif node_type == NAMESPACE_NODE:
        return node.localName or ''
    elif node_type == Node.PROCESSING_INSTRUCTION_NODE:
        return node.target
    return ''
    return


def NamespaceUri(context, nodeSet=None):
    """Function: <string> namespace-uri(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    elif not isinstance(nodeSet, NodesetType):
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'namespace-uri', _('expected node-set'))
    elif not nodeSet:
        return ''
    else:
        nodeSet.sort()
        node = nodeSet[0]
    node_type = getattr(node, 'nodeType', None)
    if node_type in (Node.ELEMENT_NODE, Node.ATTRIBUTE_NODE):
        return node.namespaceURI or ''
    return ''
    return


def Name(context, nodeSet=None):
    """Function: <string> name(<node-set>?)"""
    if nodeSet is None:
        node = context.node
    elif not isinstance(nodeSet, NodesetType):
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'name', _('expected node-set'))
    elif not nodeSet:
        return ''
    else:
        nodeSet.sort()
        node = nodeSet[0]
    node_type = getattr(node, 'nodeType', None)
    if node_type in (Node.ELEMENT_NODE, Node.ATTRIBUTE_NODE):
        return node.nodeName
    elif node_type == NAMESPACE_NODE:
        return node.localName or ''
    elif node_type == Node.PROCESSING_INSTRUCTION_NODE:
        return node.target
    return ''
    return


def String(context, object_=None):
    """Function: <string> string(<object>?)"""
    if isinstance(object_, XPathStringType):
        return object_
    if object_ is None:
        object_ = context.node
    return Conversions.StringValue(object_)
    return


def Concat(context, *args):
    """Function: <string> concat(<string>, <string>, ...)"""
    if len(args) < 1:
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'concat', _('at least 2 arguments expected'))
    return reduce(lambda a, b: a + Conversions.StringValue(b), args, '')


def StartsWith(context, outer, inner):
    """Function: <string> starts-with(<string>, <string>)"""
    if not isinstance(outer, XPathStringType):
        outer = Conversions.StringValue(outer)
    if not isinstance(inner, XPathStringType):
        inner = Conversions.StringValue(inner)
    if not inner:
        return boolean.true
    return outer[:len(inner)] == inner and boolean.true or boolean.false


def Contains(context, outer, inner):
    """Function: <string> contains(<string>, <string>)"""
    if not isinstance(outer, XPathStringType):
        outer = Conversions.StringValue(outer)
    if not isinstance(inner, XPathStringType):
        inner = Conversions.StringValue(inner)
    if not inner:
        return boolean.true
    return outer.find(inner) >= 0 and boolean.true or boolean.false


def SubstringBefore(context, outer, inner):
    """Function: <string> substring-before(<string>, <string>)"""
    if not isinstance(outer, XPathStringType):
        outer = Conversions.StringValue(outer)
    if not isinstance(inner, XPathStringType):
        inner = Conversions.StringValue(inner)
    if not inner:
        return ''
    index = outer.find(inner)
    if index == -1:
        return ''
    return outer[:index]


def SubstringAfter(context, outer, inner):
    """Function: <string> substring-after(<string>, <string>)"""
    if not isinstance(outer, XPathStringType):
        outer = Conversions.StringValue(outer)
    if not isinstance(inner, XPathStringType):
        inner = Conversions.StringValue(inner)
    if not inner:
        return ''
    index = outer.find(inner)
    if index == -1:
        return ''
    return outer[index + len(inner):]


def Substring(context, st, start, length=None):
    """Function: <string> substring(<string>, <number>, <number>?)"""
    if not isinstance(st, XPathStringType):
        st = Conversions.StringValue(st)
    if not isinstance(start, NumberType):
        start = Conversions.NumberValue(start)
    if number.isnan(start) or number.isinf(start):
        return ''
    start = int(round(start))
    if start < 1:
        startidx = 0
    else:
        startidx = start - 1
    if length is None:
        return st[startidx:]
    elif not isinstance(length, NumberType):
        length = Conversions.NumberValue(length)
    if number.isnan(length):
        return ''
    elif number.isinf(length):
        if length > 0:
            return st[startidx:]
        else:
            return ''
    length = int(round(length))
    endidx = start + length - 1
    if endidx > startidx:
        return st[startidx:endidx]
    else:
        return ''
    return


def StringLength(context, st=None):
    """Function: <number> string-length(<string>?)"""
    if st is None:
        st = context.node
    if not isinstance(st, XPathStringType):
        st = Conversions.StringValue(st)
    return float(len(st))
    return


def Normalize(context, st=None):
    """Function: <string> normalize-space(<string>?)"""
    if st is None:
        st = context.node
    if not isinstance(st, XPathStringType):
        st = Conversions.StringValue(st)
    return (' ').join(st.split())
    return


def Translate(context, source, fromChars, toChars):
    """Function: <string> translate(<string>, <string>, <string>)"""
    if not isinstance(source, XPathStringType):
        source = Conversions.StringValue(source)
    if not isinstance(fromChars, XPathStringType):
        fromChars = Conversions.StringValue(fromChars)
    if not isinstance(toChars, XPathStringType):
        toChars = Conversions.StringValue(toChars)
    fromChars = reduce(lambda st, c: st + c * (st.find(c) == -1), fromChars, '')
    toChars = toChars[:len(fromChars)]
    translate = {}
    for (from_char, to_char) in map(None, fromChars, toChars):
        translate[ord(from_char)] = to_char

    result = reduce(lambda a, b, t=translate: a + (t.get(ord(b), b) or ''), source, '')
    return result
    return


def Boolean(context, object_):
    """Function: <boolean> boolean(<object>)"""
    return Conversions.BooleanValue(object_)


def Not(context, object_):
    """Function: <boolean> not(<boolean>)"""
    return not Conversions.BooleanValue(object_) and boolean.true or boolean.false


def True(context):
    """Function: <boolean> true()"""
    return boolean.true


def False(context):
    """Function: <boolean> false()"""
    return boolean.false


def Lang(context, lang):
    """Function: <boolean> lang(<string>)"""
    lang = Conversions.StringValue(lang).lower()
    node = context.node
    while node.parentNode:
        for attr in node.attributes.values():
            if attr.localName == 'lang' and attr.namespaceURI == XML_NAMESPACE:
                value = attr.nodeValue.lower()
                if value == lang:
                    return boolean.true
                index = value.find('-')
                if index != -1 and value[:index] == lang:
                    return boolean.true
                return boolean.false

        node = node.parentNode

    return boolean.false


def Number(context, object_=None):
    """Function: <number> number(<object>?)"""
    if object_ is None:
        object_ = [
         context.node]
    return Conversions.NumberValue(object_)
    return


def Sum(context, nodeSet):
    """Function: <number> sum(<node-set>)"""
    if not isinstance(nodeSet, NodesetType):
        raise RuntimeException(RuntimeException.WRONG_ARGUMENTS, 'sum', _('expected node-set argument'))
    nns = map(Conversions.NumberValue, nodeSet)
    return reduce(lambda x, y: x + y, nns, 0)


def Floor(context, object_):
    """Function: <number> floor(<number>)"""
    num = Conversions.NumberValue(object_)
    if number.isnan(num) or number.isinf(num):
        return num
    elif int(num) == num:
        return num
    elif num < 0:
        return float(int(num) - 1)
    else:
        return float(int(num))


def Ceiling(context, object_):
    """Function: <number> ceiling(<number>)"""
    num = Conversions.NumberValue(object_)
    if number.isnan(num) or number.isinf(num):
        return num
    elif int(num) == num:
        return num
    elif num > 0:
        return float(int(num) + 1)
    else:
        return float(int(num))


def Round(context, object_):
    """Function: <number> round(<number>)"""
    num = Conversions.NumberValue(object_)
    if number.isnan(num) or number.isinf(num):
        return num
    elif num < 0 and num % 1.0 == 0.5:
        return round(num, 0) + 1
    else:
        return round(num, 0)


CoreFunctions = {(EMPTY_NAMESPACE, 'last'): Last, (EMPTY_NAMESPACE, 'position'): Position, (EMPTY_NAMESPACE, 'count'): Count, (EMPTY_NAMESPACE, 'id'): Id, (EMPTY_NAMESPACE, 'local-name'): LocalName, (EMPTY_NAMESPACE, 'namespace-uri'): NamespaceUri, (EMPTY_NAMESPACE, 'name'): Name, (EMPTY_NAMESPACE, 'string'): String, (EMPTY_NAMESPACE, 'concat'): Concat, (EMPTY_NAMESPACE, 'starts-with'): StartsWith, (EMPTY_NAMESPACE, 'contains'): Contains, (EMPTY_NAMESPACE, 'substring-before'): SubstringBefore, (EMPTY_NAMESPACE, 'substring-after'): SubstringAfter, (EMPTY_NAMESPACE, 'substring'): Substring, (EMPTY_NAMESPACE, 'string-length'): StringLength, (EMPTY_NAMESPACE, 'normalize-space'): Normalize, (EMPTY_NAMESPACE, 'translate'): Translate, (EMPTY_NAMESPACE, 'boolean'): Boolean, (EMPTY_NAMESPACE, 'not'): Not, (EMPTY_NAMESPACE, 'true'): True, (EMPTY_NAMESPACE, 'false'): False, (EMPTY_NAMESPACE, 'lang'): Lang, (EMPTY_NAMESPACE, 'number'): Number, (EMPTY_NAMESPACE, 'sum'): Sum, (EMPTY_NAMESPACE, 'floor'): Floor, (EMPTY_NAMESPACE, 'ceiling'): Ceiling, (EMPTY_NAMESPACE, 'round'): Round}