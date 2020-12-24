# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPointer\__init__.py
# Compiled at: 2005-10-07 18:33:06
__doc__ = '\nModule for XPointer processing\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft import FtException

class XPtrException(FtException):
    __module__ = __name__
    INTERNAL_ERROR = 1
    SYNTAX_ERROR = 2
    RESOURCE_ERROR = 3
    SUB_RESOURCE_ERROR = 4

    def __init__(self, errorCode, *args):
        FtException.__init__(self, errorCode, MessageSource.g_errorMessages, args)
        return


import MessageSource

def Compile(expr):
    """
    Given an XPointer expression as a string, returns an object that allows
    an evaluation engine to operate on the expression efficiently.
    """
    if not isinstance(expr, (str, unicode)):
        raise TypeError('Expected string or unicode, %s found' % (expr is None and 'None' or type(expr).__name__))
    try:
        return XPointerParser.new().parse(expr)
    except SyntaxError, error:
        raise XPtrException(XPtrException.SYNTAX_ERROR, str(error))
    except Exception, exc:
        import traceback, cStringIO
        stream = cStringIO.StringIO()
        traceback.print_exc(None, stream)
        raise XPtrException(XPtrException.INTERNAL_ERROR, stream.getvalue())

    return


def SelectUri(uri, contextNode=None, nss=None):
    """
    Parses the document with the given URI, and returns the node
    corresponding to the XPointer given in the fragment of the URI.

    uri must be an absolute URI reference. If it doesn't have a
    fragment, returns the root node.

    contextNode, if given, is the original XPointer context node
    (e.g., from the referring document, if any; accessible in the
    XPointer via the 'here' function).

    nss is a set of explicit namespace mappings for use when evaluating
    the XPointer (e.g., when the xmlns scheme isn't being used).
    """
    from Ft.Lib.Uri import SplitFragment, PercentDecode
    try:
        from xml.sax.saxlib import SAXException
    except ImportError:
        from xml.sax import SAXException

    from Ft.Xml import Domlette
    (base, fragment) = SplitFragment(uri)
    if fragment is None:
        return reader.fromUri(base)
    fragment = PercentDecode(fragment)
    try:
        doc = Domlette.NonvalidatingReader.parseUri(base)
    except FtException:
        raise
    except SAXException, exc:
        raise XPtrException(XPtrException.RESOURCE_ERROR, str(exc))
    except Exception, exc:
        import traceback
        traceback.print_exc()
        raise XPtrException(XPtrException.INTERNAL_ERROR, str(exc))

    return SelectNode(doc, fragment, nss, contextNode)
    return


def SelectNode(doc, xpointer, nss=None, contextNode=None):
    """
    Given a valid DOM node, evaluates an XPointer against it.

    contextNode, if given, is the original XPointer context node
    (e.g., from the referring document, if any; accessible in the
    XPointer via the 'here' function).

    nss is a set of explicit namespace mappings for use when evaluating
    the XPointer (e.g., when the xmlns scheme isn't being used).
    """
    parser = XPointerParser.new()
    try:
        xptr = parser.parse(xpointer)
    except SyntaxError, exc:
        raise XPtrException(XPtrException.SYNTAX_ERROR, str(exc))
    except Exception, exc:
        import traceback
        traceback.print_exc()
        raise XPtrException(XPtrException.INTERNAL_ERROR, str(exc))

    context = XPtrContext.XPtrContext(doc, 1, 1, contextNode or doc, nss or {})
    return xptr.select(context)


import XPointerParserc as XPointerParser