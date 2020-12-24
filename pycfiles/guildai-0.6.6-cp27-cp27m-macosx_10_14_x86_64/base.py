# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/html5lib/treebuilders/base.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import text_type
from ..constants import scopingElements, tableInsertModeElements, namespaces
Marker = None
listElementsMap = {None: (
        frozenset(scopingElements), False), 
   b'button': (
             frozenset(scopingElements | set([(namespaces[b'html'], b'button')])), False), 
   b'list': (
           frozenset(scopingElements | set([(namespaces[b'html'], b'ol'),
            (
             namespaces[b'html'], b'ul')])), False), 
   b'table': (
            frozenset([(namespaces[b'html'], b'html'),
             (
              namespaces[b'html'], b'table')]), False), 
   b'select': (
             frozenset([(namespaces[b'html'], b'optgroup'),
              (
               namespaces[b'html'], b'option')]), True)}

class Node(object):
    """Represents an item in the tree"""

    def __init__(self, name):
        """Creates a Node

        :arg name: The tag name associated with the node

        """
        self.name = name
        self.parent = None
        self.value = None
        self.attributes = {}
        self.childNodes = []
        self._flags = []
        return

    def __str__(self):
        attributesStr = (b' ').join([ b'%s="%s"' % (name, value) for name, value in self.attributes.items()
                                    ])
        if attributesStr:
            return b'<%s %s>' % (self.name, attributesStr)
        else:
            return b'<%s>' % self.name

    def __repr__(self):
        return b'<%s>' % self.name

    def appendChild(self, node):
        """Insert node as a child of the current node

        :arg node: the node to insert

        """
        raise NotImplementedError

    def insertText(self, data, insertBefore=None):
        """Insert data as text in the current node, positioned before the
        start of node insertBefore or to the end of the node's text.

        :arg data: the data to insert

        :arg insertBefore: True if you want to insert the text before the node
            and False if you want to insert it after the node

        """
        raise NotImplementedError

    def insertBefore(self, node, refNode):
        """Insert node as a child of the current node, before refNode in the
        list of child nodes. Raises ValueError if refNode is not a child of
        the current node

        :arg node: the node to insert

        :arg refNode: the child node to insert the node before

        """
        raise NotImplementedError

    def removeChild(self, node):
        """Remove node from the children of the current node

        :arg node: the child node to remove

        """
        raise NotImplementedError

    def reparentChildren(self, newParent):
        """Move all the children of the current node to newParent.
        This is needed so that trees that don't store text as nodes move the
        text in the correct way

        :arg newParent: the node to move all this node's children to

        """
        for child in self.childNodes:
            newParent.appendChild(child)

        self.childNodes = []

    def cloneNode(self):
        """Return a shallow copy of the current node i.e. a node with the same
        name and attributes but with no parent or child nodes
        """
        raise NotImplementedError

    def hasContent(self):
        """Return true if the node has children or text, false otherwise
        """
        raise NotImplementedError


class ActiveFormattingElements(list):

    def append(self, node):
        equalCount = 0
        if node != Marker:
            for element in self[::-1]:
                if element == Marker:
                    break
                if self.nodesEqual(element, node):
                    equalCount += 1
                if equalCount == 3:
                    self.remove(element)
                    break

        list.append(self, node)

    def nodesEqual(self, node1, node2):
        if not node1.nameTuple == node2.nameTuple:
            return False
        if not node1.attributes == node2.attributes:
            return False
        return True


class TreeBuilder(object):
    """Base treebuilder implementation

    * documentClass - the class to use for the bottommost node of a document
    * elementClass - the class to use for HTML Elements
    * commentClass - the class to use for comments
    * doctypeClass - the class to use for doctypes

    """
    documentClass = None
    elementClass = None
    commentClass = None
    doctypeClass = None
    fragmentClass = None

    def __init__(self, namespaceHTMLElements):
        """Create a TreeBuilder

        :arg namespaceHTMLElements: whether or not to namespace HTML elements

        """
        if namespaceHTMLElements:
            self.defaultNamespace = b'http://www.w3.org/1999/xhtml'
        else:
            self.defaultNamespace = None
        self.reset()
        return

    def reset(self):
        self.openElements = []
        self.activeFormattingElements = ActiveFormattingElements()
        self.headPointer = None
        self.formPointer = None
        self.insertFromTable = False
        self.document = self.documentClass()
        return

    def elementInScope(self, target, variant=None):
        exactNode = hasattr(target, b'nameTuple')
        if exactNode or isinstance(target, text_type):
            target = (
             namespaces[b'html'], target)
        assert isinstance(target, tuple)
        listElements, invert = listElementsMap[variant]
        for node in reversed(self.openElements):
            if exactNode and node == target:
                return True
            if not exactNode and node.nameTuple == target:
                return True
            if invert ^ (node.nameTuple in listElements):
                return False

        assert False

    def reconstructActiveFormattingElements(self):
        if not self.activeFormattingElements:
            return
        i = len(self.activeFormattingElements) - 1
        entry = self.activeFormattingElements[i]
        if entry == Marker or entry in self.openElements:
            return
        while entry != Marker and entry not in self.openElements:
            if i == 0:
                i = -1
                break
            i -= 1
            entry = self.activeFormattingElements[i]

        while True:
            i += 1
            entry = self.activeFormattingElements[i]
            clone = entry.cloneNode()
            element = self.insertElement({b'type': b'StartTag', b'name': clone.name, 
               b'namespace': clone.namespace, 
               b'data': clone.attributes})
            self.activeFormattingElements[i] = element
            if element == self.activeFormattingElements[(-1)]:
                break

    def clearActiveFormattingElements(self):
        entry = self.activeFormattingElements.pop()
        while self.activeFormattingElements and entry != Marker:
            entry = self.activeFormattingElements.pop()

    def elementInActiveFormattingElements(self, name):
        """Check if an element exists between the end of the active
        formatting elements and the last marker. If it does, return it, else
        return false"""
        for item in self.activeFormattingElements[::-1]:
            if item == Marker:
                break
            elif item.name == name:
                return item

        return False

    def insertRoot(self, token):
        element = self.createElement(token)
        self.openElements.append(element)
        self.document.appendChild(element)

    def insertDoctype(self, token):
        name = token[b'name']
        publicId = token[b'publicId']
        systemId = token[b'systemId']
        doctype = self.doctypeClass(name, publicId, systemId)
        self.document.appendChild(doctype)

    def insertComment(self, token, parent=None):
        if parent is None:
            parent = self.openElements[(-1)]
        parent.appendChild(self.commentClass(token[b'data']))
        return

    def createElement(self, token):
        """Create an element but don't insert it anywhere"""
        name = token[b'name']
        namespace = token.get(b'namespace', self.defaultNamespace)
        element = self.elementClass(name, namespace)
        element.attributes = token[b'data']
        return element

    def _getInsertFromTable(self):
        return self._insertFromTable

    def _setInsertFromTable(self, value):
        """Switch the function used to insert an element from the
        normal one to the misnested table one and back again"""
        self._insertFromTable = value
        if value:
            self.insertElement = self.insertElementTable
        else:
            self.insertElement = self.insertElementNormal

    insertFromTable = property(_getInsertFromTable, _setInsertFromTable)

    def insertElementNormal(self, token):
        name = token[b'name']
        assert isinstance(name, text_type), b'Element %s not unicode' % name
        namespace = token.get(b'namespace', self.defaultNamespace)
        element = self.elementClass(name, namespace)
        element.attributes = token[b'data']
        self.openElements[(-1)].appendChild(element)
        self.openElements.append(element)
        return element

    def insertElementTable(self, token):
        """Create an element and insert it into the tree"""
        element = self.createElement(token)
        if self.openElements[(-1)].name not in tableInsertModeElements:
            return self.insertElementNormal(token)
        else:
            parent, insertBefore = self.getTableMisnestedNodePosition()
            if insertBefore is None:
                parent.appendChild(element)
            else:
                parent.insertBefore(element, insertBefore)
            self.openElements.append(element)
            return element

    def insertText(self, data, parent=None):
        """Insert text data."""
        if parent is None:
            parent = self.openElements[(-1)]
        if not self.insertFromTable or self.insertFromTable and self.openElements[(-1)].name not in tableInsertModeElements:
            parent.insertText(data)
        else:
            parent, insertBefore = self.getTableMisnestedNodePosition()
            parent.insertText(data, insertBefore)
        return

    def getTableMisnestedNodePosition(self):
        """Get the foster parent element, and sibling to insert before
        (or None) when inserting a misnested table node"""
        lastTable = None
        fosterParent = None
        insertBefore = None
        for elm in self.openElements[::-1]:
            if elm.name == b'table':
                lastTable = elm
                break

        if lastTable:
            if lastTable.parent:
                fosterParent = lastTable.parent
                insertBefore = lastTable
            else:
                fosterParent = self.openElements[(self.openElements.index(lastTable) - 1)]
        else:
            fosterParent = self.openElements[0]
        return (
         fosterParent, insertBefore)

    def generateImpliedEndTags(self, exclude=None):
        name = self.openElements[(-1)].name
        if name in frozenset(('dd', 'dt', 'li', 'option', 'optgroup', 'p', 'rp', 'rt')) and name != exclude:
            self.openElements.pop()
            self.generateImpliedEndTags(exclude)

    def getDocument(self):
        """Return the final tree"""
        return self.document

    def getFragment(self):
        """Return the final fragment"""
        fragment = self.fragmentClass()
        self.openElements[0].reparentChildren(fragment)
        return fragment

    def testSerializer(self, node):
        """Serialize the subtree of node in the format required by unit tests

        :arg node: the node from which to start serializing

        """
        raise NotImplementedError