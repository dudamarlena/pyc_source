# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\Namespace.py
# Compiled at: 2018-01-18 12:34:37
# Size of source mod 2**32: 2450 bytes
import logging
from .exceptions import *
from .Node import Node
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Namespace(Node):
    __doc__ = '\n    Class representing a XML namespace\n\n    :param str prefix: Prefix to use for the namespace\n    :param str uri: URI of the namespace\n    :param parent: Parent node of this node.\n    :type parent: expatriate.Parent or None\n    '

    def __init__(self, prefix, uri, parent=None):
        super().__init__(parent=parent)
        self.prefix = prefix
        self.uri = uri

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def get_type(self):
        """
        Return the type of the node

        :rtype: str
        """
        return 'namespace'

    def get_string_value(self):
        """
        Return the string value of the node

        :rtype: str
        """
        return self.uri

    def get_expanded_name(self):
        """
        Return the expanded name of the node

        :rtype: tuple(None, prefix str)
        """
        return (
         None, self.prefix)

    def get_document_order(self):
        """
        Get the index of this Node's order in the enclosing Document.

        :rtype: int
        :raises UnattachedElementException: if the Node is not attached to a Document
        """
        if self._parent is None:
            raise UnattachedElementException('Element ' + str(self) + ' is not attached to a document')
        do = self._parent.get_document_order()
        ordered_ns = [self._parent.namespace_nodes[k] for k in self._parent.namespace_nodes.keys()]
        return do + ordered_ns.index(self)