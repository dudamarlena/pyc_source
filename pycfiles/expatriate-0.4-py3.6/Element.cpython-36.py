# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\Element.py
# Compiled at: 2018-01-18 12:27:29
# Size of source mod 2**32: 13412 bytes
import logging
from .Attribute import Attribute
from .exceptions import *
from .Namespace import Namespace
from .Node import Node
from .Parent import Parent
from .publishsubscribe import PublishingDict, Subscriber
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Element(Parent, Subscriber):
    __doc__ = "\n    Class representing a XML element\n\n    :param str local_name: Local name of the attribute (the part after the :)\n    :param attributes: The attributes to be used by this Element\n    :type attributes: dict[str, Attribute] or None\n    :param prefix: The prefix used in this attribute's name (the part before the :)\n    :type prefix: str or None\n    :param namespace: The namespace of this Attribute. Must be defined if the prefix is not defined by the parent Nodes\n    :type namespace: str or None\n    :param parent: The node to use as the parent to this node\n    :type parent: expatriate.Parent or None\n    "

    def __init__(self, local_name, attributes=None, prefix=None, namespace=None, parent=None):
        super().__init__(parent=parent)
        if attributes is None:
            self._attributes = PublishingDict({})
        else:
            self._attributes = PublishingDict(attributes)
        self._attributes.subscribe(self)
        self._prefix = prefix
        self._namespace = namespace
        self._local_name = local_name
        self._init_namespaces()
        self._init_attributes()
        if namespace is not None:
            if namespace not in self._namespace_to_prefixes:
                logger.debug(str(self) + ' parent does not define namespace ' + namespace + '; adding to attributes')
                if prefix is None:
                    self.attributes['xmlns'] = namespace
                else:
                    self.attributes['xmlns:' + prefix] = namespace

    @property
    def parent(self):
        """
        The parent node of this Element.

        :getter: Returns the parent Node
        :setter: Sets the parent Node
        :type: expatriate.Parent or None
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        self._init_namespaces()

    @property
    def attributes(self):
        """
        The attributes of this Element. Read-only.

        :getter: Returns the attribute dict.
        :type: dict
        """
        return self._attributes

    @property
    def name(self):
        """
        The name of this Element.

        :getter: Returns the name.
        :setter: Sets the name. Updates the prefix and namespace and local_name if they change.
        :type: str
        """
        if self._prefix is None:
            return self._local_name
        else:
            return self._prefix + ':' + self._local_name

    @name.setter
    def name(self, name):
        if ':' in name:
            self._prefix, colon, self._name = name.partition(':')
        else:
            self._prefix = None
            self._name = name
        if self._parent is not None:
            self._namespace = self.prefix_to_namespace(self._prefix)

    @property
    def local_name(self):
        """
        The local name (part after the :) of this Element.

        :getter: Returns the local name.
        :setter: Sets the local name.
        :type: str
        """
        return self._local_name

    @local_name.setter
    def local_name(self, local_name):
        self._local_name = local_name

    @property
    def prefix(self):
        """
        The prefix (part before the :) of this Element.

        :getter: Returns the prefix.
        :setter: Sets the prefix.
        :type: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = prefix
        if self._parent is not None:
            self._namespace = self.prefix_to_namespace(self._prefix)

    @property
    def namespace(self):
        """
        The namespace (URI the prefix maps to) of this Element.

        :getter: Returns the namespace URI.
        :setter: Sets the namespace URI.
        :type: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        self._namespace = namespace
        if self._parent is not None:
            self._prefix = self.namespace_to_prefix(namespace)

    def _data_added(self, publisher, id_, item):
        logger.debug(str(self) + ' added attributes: ' + str(id_))
        self._init_attributes()
        if id_.startswith('xmlns'):
            self._init_namespaces()

    def _data_updated(self, publisher, id_, old_item, new_item):
        logger.debug(str(self) + ' updated attributes: ' + str(id_))
        self._init_attributes()
        if id_.startswith('xmlns'):
            self._init_namespaces()

    def _data_deleted(self, publisher, id_, item):
        logger.debug(str(self) + ' deleted attributes: ' + str(id_))
        self._init_attributes()
        if id_.startswith('xmlns'):
            self._init_namespaces()

    def _init_attributes(self):
        self.attribute_nodes = {}
        for k, v in self._attributes.items():
            if ':' in k:
                prefix, colon, local_name = k.partition(':')
                namespace = self.prefix_to_namespace(prefix)
            else:
                local_name = k
                prefix = None
                namespace = None
            n = Attribute(local_name, v, parent=self, prefix=prefix, namespace=namespace)
            self.attribute_nodes[k] = n

    def _init_namespaces(self):
        if isinstance(self._parent, Element):
            self._prefix_to_namespace = self._parent._prefix_to_namespace.copy()
            self._namespace_to_prefixes = self._parent._namespace_to_prefixes.copy()
        else:
            self._prefix_to_namespace = {'xml': 'http://www.w3.org/XML/1998/namespace'}
            self._namespace_to_prefixes = {v:k for k, v in self._prefix_to_namespace.items()}
        for k, v in self._attributes.items():
            if k.startswith('xmlns:'):
                prefix = k.partition(':')[2]
                if prefix in self._prefix_to_namespace:
                    raise PrefixRedefineException('Prefix ' + prefix + ' has already been used but is being redefined')
                self._prefix_to_namespace[prefix] = v
                self._namespace_to_prefixes[v] = prefix
                logger.debug(str(self) + ' Added prefix ' + prefix + ' for uri ' + v)
            else:
                if k.startswith('xmlns'):
                    self._prefix_to_namespace[None] = v
                    self._namespace_to_prefixes[v] = None
                    logger.debug(str(self) + ' Added prefix None for uri ' + v)

        if self._namespace is None:
            if self._prefix is None:
                if None in self._prefix_to_namespace:
                    self._namespace = self._prefix_to_namespace[None]
        if self._namespace is None:
            if self._prefix is not None:
                self._namespace = self.prefix_to_namespace(self._prefix)
        self.namespace_nodes = {}
        for prefix in self._prefix_to_namespace.keys():
            uri = self._prefix_to_namespace[prefix]
            n = Namespace(prefix, uri, parent=self)
            self.namespace_nodes[prefix] = n

    def prefix_to_namespace(self, prefix):
        logger.debug(str(self) + ' resolving prefix: ' + str(prefix) + ' using ' + str(self._prefix_to_namespace))
        if prefix in self._prefix_to_namespace:
            return self._prefix_to_namespace[prefix]
        else:
            return super().prefix_to_namespace(prefix)

    def namespace_to_prefix(self, namespace):
        logger.debug(str(self) + ' resolving namespace: ' + str(namespace) + ' using ' + str(self._namespace_to_prefixes))
        if namespace in self._namespace_to_prefixes:
            return self._namespace_to_prefixes[namespace]
        else:
            return super().namespace_to_prefix(namespace)

    def escape_attribute(self, text):
        """
        Escape characters disallowed in an element's attribute within *text*
        with their SGML entities.

        :param str text: The text to escape
        :rtype: str
        """
        return self.escape(text).replace('"', '&quot;')

    def produce(self):
        """
        Produce an XML str (not encoded) from the contents of this
        node

        :rtype: str
        """
        logger.debug(str(self) + ' producing xml: ' + self.name + ' attributes ' + str(self.attributes) + '; ' + str(len(self.children)) + ' children')
        s = '<' + self.name
        for k, v in self.attributes.items():
            s += ' ' + self.escape(k) + '="' + self.escape_attribute(v) + '"'

        if len(self.children) == 0:
            s += '/>'
        else:
            s += '>'
            for c in self.children:
                s += c.produce()

            s += '</' + self.name + '>'
        return s

    def get_type(self):
        """
        Return the type of the node

        :rtype: str
        """
        return 'element'

    def get_string_value(self):
        """
        Return the string value of the node

        :rtype: str
        """
        from .CharacterData import CharacterData
        s = ''
        for c in self.children:
            if isinstance(c, CharacterData):
                s += c.data
            else:
                if isinstance(c, Element):
                    s += c.get_string_value()

        return s

    def get_expanded_name(self):
        """
        Return the expanded name of the node

        :rtype: tuple(namespace str, local_name str)
        """
        return (
         self.namespace, self.local_name)

    def __str__(self):
        s = self.__class__.__name__ + ' ' + hex(id(self)) + ' ' + self.name
        if 'id' in self.attributes:
            s += ' id=' + self.attributes['id']
        if 'name' in self.attributes:
            s += ' name=' + self.attributes['name']
        return s

    def find_by_id(self, ref):
        logger.debug(str(self) + ' checking attributes for id: ' + str(ref))
        for k, v in self.attributes.items():
            k = k.lower()
            if k.endswith(':id') or k == 'id':
                logger.debug(str(self) + ' found id: ' + str(v))
                if v == ref:
                    logger.debug(str(self) + ' matches id: ' + str(ref))
                    return self
                logger.debug(str(self) + ' id ' + str(v) + ' does not match id: ' + str(ref))

        return super().find_by_id(ref)

    def get_node_count(self):
        """
        Get the count of this node and any children nodes within.

        :rtype: int
        """
        do = 1 + len(self.namespace_nodes) + len(self.attribute_nodes)
        for c in self.children:
            do += c.get_node_count()

        return do

    def is_nil(self):
        """
        Returns if the element has the XMLSchema-instance attribute set for a
        nil value'd element

        :rtype: bool
        """
        try:
            prefix = self.namespace_to_prefix('http://www.w3.org/2001/XMLSchema-instance')
        except UnknownNamespaceException:
            return False
        else:
            name = prefix + ':nil'
            if name in self.attributes:
                if self.attributes[name] == 'true':
                    return True
            return False