# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\cDomlette.py
# Compiled at: 2006-08-27 14:21:39
"""
cDomlette implementation: a very fast DOM-like library tailored for use in XPath/XSLT

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import re
from Ft.Xml import XML_NAMESPACE, XMLNS_NAMESPACE
from cDomlettec import implementation, DOMImplementation, DocumentFragment, Document, Node, CharacterData, Attr, Element, Text, Comment, ProcessingInstruction, XPathNamespace
from cDomlettec import NonvalParse, ValParse, Parse, ParseFragment
from cDomlettec import GetAllNs, SeekNss
from cDomlettec import TestTree
from cDomlettec import XPTR_ELEMENT_ID as ELEMENT_ID
from cDomlettec import XPTR_ELEMENT_COUNT as ELEMENT_COUNT
from cDomlettec import XPTR_ELEMENT_MATCH as ELEMENT_MATCH
from cDomlettec import XPTR_ATTRIBUTE_MATCH as ATTRIBUTE_MATCH
__all__ = [
 'implementation', 'DOMImplementation', 'DocumentFragment', 'Document', 'Node', 'CharacterData', 'Attr', 'Element', 'Text', 'Comment', 'ProcessingInstruction', 'XPathNamespace', 'NonvalParse', 'Parse', 'GetAllNs', 'SeekNss', 'ValParse']

def ProcessFragment(frag):
    """
    Take an XPointer fragment and return a structure suitable for the
    cDomlette parser to update state tables
    Xptr e.g. xmlns(x=http://uche.ogbuji.net/eg) xpointer(/x:spam/x:eggs)
    """
    from Ft.Xml.XPointer import Compile, XPtrException
    from Ft.Xml.XPointer.XPointer import Shorthand, SchemeBased, ElementScheme, XmlnsScheme, XPointerScheme
    from Ft.Xml.XPath.ParsedAbsoluteLocationPath import ParsedAbsoluteLocationPath
    xptr = Compile(frag)
    if isinstance(xptr, Shorthand):
        return [
         [
          (
           ELEMENT_ID, xptr.identifier)]]
    assert isinstance(xptr, SchemeBased)
    namespaces = {'xml': XML_NAMESPACE}
    for part in xptr.parts:
        if isinstance(part, XmlnsScheme):
            if part.prefix != 'xml' and part.uri not in (XML_NAMESPACE, XMLNS_NAMESPACE):
                namespaces[part.prefix] = part.uri
        elif isinstance(part, XPointerScheme):
            expr = part.expr
            if isinstance(expr, ParsedAbsoluteLocationPath):
                expr = expr._child
                if expr is None:
                    return None
            return HandleStep(expr, [], namespaces)
        elif isinstance(part, ElementScheme):
            states = []
            if part.identifier:
                states.append([(ELEMENT_ID, part.identifier)])
            for index in part.sequence:
                states.append([(ELEMENT_MATCH, None, None), (ELEMENT_COUNT, index)])

            return states

    raise XPtrException(XPtrExpression.SUB_RESOURCE_ERROR)
    return


def HandleStep(expr, states, nss):
    from Ft.Xml.XPath.ParsedRelativeLocationPath import ParsedRelativeLocationPath
    from Ft.Xml.XPath.ParsedStep import ParsedStep
    from Ft.Xml.XPath.ParsedAxisSpecifier import ParsedChildAxisSpecifier, ParsedAttributeAxisSpecifier
    from Ft.Xml.XPath.ParsedNodeTest import LocalNameTest, QualifiedNameTest, NamespaceTest, PrincipalTypeTest
    from Ft.Xml.XPath.ParsedExpr import ParsedNLiteralExpr, ParsedEqualityExpr
    if isinstance(expr, ParsedRelativeLocationPath):
        HandleStep(expr._left, states, nss)
        curr_step = expr._right
    elif isinstance(expr, ParsedStep):
        curr_step = expr
    else:
        raise NotImplementedError(expr)
    if not isinstance(curr_step._axis, ParsedChildAxisSpecifier):
        raise NotImplementedError(curr_step._axis)
    node_test = curr_step._nodeTest
    if isinstance(node_test, LocalNameTest):
        namespace = None
        local = node_test._name
    elif isinstance(node_test, (QualifiedNameTest, NamespaceTest)):
        try:
            namespace = nss[node_test._prefix]
        except KeyError:
            from Ft.Xml.XPath import RuntimeException
            from Ft.Xml.XPointer import XPtrException
            error = RuntimeException(RuntimeException.UNDEFINED_PREFIX, node_test._prefix)
            raise XPtrException(XPtrException.SYNTAX_ERROR, error.message)
        else:
            local = getattr(node_test, '_localName', None)
    elif isinstance(node_test, PrincipalTypeTest):
        namespace = None
        local = None
    else:
        raise NotImplementedError(node_test)
    criteria = [
     (
      ELEMENT_MATCH, namespace, local)]
    if curr_step._predicates:
        pred = curr_step._predicates._predicates[0]
        if isinstance(pred, ParsedNLiteralExpr):
            criteria.extend([(ELEMENT_COUNT, int(pred._literal))])
        elif isinstance(pred, ParsedEqualityExpr) and pred._op == '=':
            if isinstance(pred._left, ParsedStep) and isinstance(pred._left._axis, ParsedAttributeAxisSpecifier):
                criterion = [
                 ATTRIBUTE_MATCH]
                if hasattr(pred._left._nodeTest, '_localName'):
                    criterion.append(nss[pred._left._nodeTest._prefix])
                    criterion.append(pred._left._nodeTest._localName)
                else:
                    criterion.append(None)
                    criterion.append(pred._left._nodeTest._name)
                criterion.append(pred._right._literal)
                criteria.append(tuple(criterion))
    states.append(criteria)
    return states
    return