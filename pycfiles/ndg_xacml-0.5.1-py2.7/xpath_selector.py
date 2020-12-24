# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/utils/xpath_selector.py
# Compiled at: 2012-06-19 10:10:38
"""XPath selection for XACML AttributeSelector
"""
__author__ = 'R B Wilkinson'
__date__ = '23/12/11'
__copyright__ = '(C) 2011 Science and Technology Facilities Council'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: xpath_selector.py 8078 2012-06-19 14:10:35Z pjkersha $'
from abc import ABCMeta, abstractmethod
from ndg.xacml import Config, importElementTree
ElementTree = importElementTree()

class XPathSelectorInterface(object):
    """Interface for XPath selectors.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, contextElem):
        """
        @type contextElem: type of an XML element appropriate to implementation
        @param contextElem: context element on which searches are based
        """
        pass

    @abstractmethod
    def selectText(self, path):
        """Performs an XPath search and returns text content of matched
        elements.
        @type path: str
        @param path: XPath path expression
        @rtype: list of basestr
        @return: text from selected elements
        """
        pass


class EtreeXPathSelector(XPathSelectorInterface):
    """XPathSelectorInterface using ElementTree XPath selection.
    """

    def __init__(self, contextElem):
        """
        @type contextElem: ElementTree.Element
        @param contextElem: context element on which searches are based
        """
        if not ElementTree.iselement(contextElem):
            raise TypeError('Expecting %r input type for parsing; got %r' % (
             ElementTree.Element, contextElem))
        self.contextElem = contextElem

    if Config.use_lxml:

        def selectText(self, path):
            """Performs an XPath search and returns text content of matched
            elements.
            @type path: str
            @param path: XPath path expression
            @rtype: list of basestring
            @return: text from selected elements
            """
            if path.startswith('/'):
                relPath = '.' + path
            else:
                relPath = path
            find = ElementTree.ETXPath(relPath)
            elems = find(self.contextElem)
            returnList = []
            for m in elems:
                if hasattr(m, 'text'):
                    returnList.append(m.text)
                else:
                    returnList.append(m.__str__())

            return returnList

    else:

        def selectText(self, path):
            """Performs an XPath search and returns text content of matched
            elements.
            @type path: str
            @param path: XPath path expression
            @rtype: list of basestring
            @return: text from selected elements
            """
            if path.startswith('/'):
                relPath = '.' + path
            else:
                relPath = path
            elems = self.contextElem.findall(relPath)
            return [ e.text for e in elems ]