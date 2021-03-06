# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\XPath\Util.py
# Compiled at: 2006-01-14 19:55:53
"""
General utilities for XPath applications

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import os
from xml.dom import Node
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Domlette import GetAllNs
from Ft.Xml.Lib.XmlString import SplitQName
__all__ = [
 'Compile', 'Evaluate', 'SimpleEvaluate', 'NormalizeNode', 'ExpandQName']

def ExpandQName(qname, refNode=None, namespaces=None):
    """
    Expand the given QName in the context of the given node,
    or in the given namespace dictionary.

    Returns a 2-tuple consisting of the namespace URI and local name.
    """
    nss = {}
    if refNode:
        nss = GetAllNs(refNode)
    elif namespaces:
        nss = namespaces
    (prefix, local) = SplitQName(qname)
    if prefix:
        try:
            split_name = (
             nss[prefix], local)
        except KeyError:
            from Ft.Xml.XPath import RuntimeException
            raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

    else:
        split_name = (
         EMPTY_NAMESPACE, local)
    return split_name


def NormalizeNode(node):
    """
    NormalizeNode is used to prepare a DOM for XPath evaluation.

    1.  Convert CDATA Sections to Text Nodes.
    2.  Normalize all text nodes (adjacent nodes are merged into the first one).
    """
    node = node.firstChild
    while node:
        if node.nodeType == Node.CDATA_SECTION_NODE:
            if node.nextSibling and node.nextSibling.nodeType == Node.TEXT_NODE:
                node.nextSibling.insertData(0, node.data)
            elif node.data:
                text = node.ownerDocument.createTextNode(node.data)
                node.parentNode.replaceChild(text, node)
                node = text
            else:
                next = node.nextSibling
                node.parentNode.removeChild(node)
                node = next
                continue
        elif node.nodeType == Node.TEXT_NODE:
            next = node.nextSibling
            while next and next.nodeType in [Node.TEXT_NODE, Node.CDATA_SECTION_NODE]:
                node.appendData(next.data)
                node.parentNode.removeChild(next)
                next = node.nextSibling

            if not node.data:
                next = node.nextSibling
                node.parentNode.removeChild(node)
                node = next
                continue
        elif node.nodeType == Node.ELEMENT_NODE:
            for attr in node.attributes.values():
                if len(attr.childNodes) > 1:
                    NormalizeNode(attr)

            NormalizeNode(node)
        node = node.nextSibling

    return


def SimpleEvaluate(expr, node, explicitNss=None):
    """
    Designed to be the most simple/brain-dead interface to using XPath
    Usually invoked through Node objects using:
      node.xpath(expr[, explicitNss])

    expr - XPath expression in string or compiled form
    node - the node to be used as core of the context for evaluating the XPath
    explicitNss - (optional) any additional or overriding namespace mappings
                  in the form of a dictionary of prefix: namespace
                  the base namespace mappings are taken from in-scope
                  declarations on the given node.  This explicit dictionary
                  is suprimposed on the base mappings
    """
    if 'EXTMODULES' in os.environ:
        ext_modules = os.environ['EXTMODULES'].split(':')
    else:
        ext_modules = []
    explicitNss = explicitNss or {}
    nss = GetAllNs(node)
    nss.update(explicitNss)
    context = Context.Context(node, 0, 0, processorNss=nss, extModuleList=ext_modules)
    if hasattr(expr, 'evaluate'):
        retval = expr.evaluate(context)
    else:
        retval = XPathParser.new().parse(expr).evaluate(context)
    return retval


def Evaluate(expr, contextNode=None, context=None):
    """
    Evaluates the given XPath expression.

    Two arguments are required: the expression (as a string or compiled
    expression object), and a context. The context can be given as a
    Domlette node via the 'contextNode' named argument, or can be given as
    an Ft.Xml.XPath.Context.Context object via the 'context' named
    argument.

    If namespace bindings or variable bindings are needed, use a
    Context object. If extension functions are needed, either use a
    Context object, or set the EXTMODULES environment variable to be a
    ':'-separated list of names of Python modules that implement
    extension functions.

    The return value will be one of the following:
    node-set: list of Domlette node objects (xml.dom.Node based);
    string: Unicode string type;
    number: float type;
    boolean: Ft.Lib.boolean C extension object;
    or a non-XPath object (i.e. as returned by an extension function).
    """
    if 'EXTMODULES' in os.environ:
        ext_modules = os.environ['EXTMODULES'].split(':')
    else:
        ext_modules = []
    if contextNode and context:
        con = context.clone()
        con.node = contextNode
    elif context:
        con = context
    elif contextNode:
        if isinstance(contextNode, Context.Context):
            con = contextNode
        else:
            con = Context.Context(contextNode, 0, 0, extModuleList=ext_modules)
    else:
        from Ft.Xml.XPath import RuntimeException
        raise RuntimeException(RuntimeException.NO_CONTEXT)
    if hasattr(expr, 'evaluate'):
        retval = expr.evaluate(con)
    else:
        retval = XPathParser.new().parse(expr).evaluate(con)
    return retval


def Compile(expr):
    """
    Given an XPath expression as a string, returns an object that allows
    an evaluation engine to operate on the expression efficiently.
    This "compiled" expression object can be passed to the Evaluate
    function instead of a string, in order to shorten the amount of time
    needed to evaluate the expression.
    """
    if not isinstance(expr, (str, unicode)):
        raise TypeError('Expected string, found %s' % type(expr))
    try:
        return XPathParser.new().parse(expr)
    except SyntaxError, error:
        from Ft.Xml.XPath import CompiletimeException
        raise CompiletimeException(CompiletimeException.SYNTAX, 0, 0, str(error))
    except:
        import traceback, cStringIO
        stream = cStringIO.StringIO()
        traceback.print_exc(None, stream)
        from Ft.Xml.XPath import CompiletimeException
        raise CompiletimeException(CompiletimeException.INTERNAL, stream.getvalue())

    return