# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\Parent.py
# Compiled at: 2018-01-18 12:34:45
# Size of source mod 2**32: 8976 bytes
import logging
from .exceptions import *
from .Node import Node
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Parent(Node):
    __doc__ = '\n    Super class for nodes containing children\n\n    :param parent: parent Node of this Node\n    :type parent: Parent or None\n\n    '

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.children = []

    def spawn_character_data(self, *args, **kwargs):
        """
        Spawn a :py:class:`.CharacterData` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.CharacterData
        """
        from .CharacterData import CharacterData
        n = CharacterData(args, **kwargs, **{'parent': self})
        self.children.append(n)
        return n

    def spawn_comment(self, *args, **kwargs):
        """
        Spawn a :py:class:`.Comment` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.Comment
        """
        from .Comment import Comment
        n = Comment(args, **kwargs, **{'parent': self})
        self.children.append(n)
        return n

    def spawn_element(self, *args, **kwargs):
        """
        Spawn a :py:class:`.Element` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.Element
        """
        from .Element import Element
        n = Element(args, **kwargs, **{'parent': self})
        self.children.append(n)
        return n

    def spawn_processing_instruction(self, *args, **kwargs):
        """
        Spawn a :py:class:`.ProcessingInstruction` object using this node as the parent

        All arguments are passed to the newly created object's constructor

        :rtype: expatriate.ProcessingInstruction
        """
        from .ProcessingInstruction import ProcessingInstruction
        n = ProcessingInstruction(args, **kwargs, **{'parent': self})
        self.children.append(n)
        return n

    def __len__(self):
        """
        Returns the length of this node's children.
        """
        return len(self.children)

    def __getitem__(self, key):
        """
        Returns the indexed child from the node's children
        """
        if not isinstance(key, int):
            if not isinstance(key, slice):
                raise TypeError('Key values must be of int type or slice; got: ' + key.__class__.__name__)
        return self.children[key]

    def __setitem__(self, key, value):
        """
        Sets the indexed child in the node's children
        """
        if not isinstance(key, int):
            raise TypeError('Key values must be of int type; got: ' + key.__class__.__name__)
        if not isinstance(value, Node):
            raise TypeError('Values must be of Node type; got: ' + value.__class__.__name__)
        self.children[key] = value

    def __delitem__(self, key):
        """
        Deletes the indexed child in the node's children
        """
        if not isinstance(key, int):
            raise TypeError('Key values must be of int type; got: ' + key.__class__.__name__)
        del self.children[key]

    def __iter__(self):
        """
        Returns an iter on the node's children
        """
        return iter(self.children)

    def append(self, x):
        """
        Add an item to the end of the node's children

        :param x: The item to add
        :type x: str or int or float or bool or expatriate.Node
        """
        from .CharacterData import CharacterData
        if isinstance(x, str):
            n = CharacterData(x, parent=self)
        else:
            if isinstance(x, int) or isinstance(x, float) or isinstance(x, bool):
                n = CharacterData((str(x)), parent=self)
            else:
                if isinstance(x, Node):
                    n = x
                    n._parent = self
                else:
                    raise ValueError('Children of ' + self.__class__.__name__ + ' must be a simple type (str, int, float)' + ' or a subclass of Node; got: ' + x.__class__.__name__)
        self.children.append(n)

    def count(self, x):
        """
        Returns the number of times node x appears in the node's children

        :param expatriate.Node x: The node
        """
        return self.children.count(x)

    def index(self, x, *args):
        """
        Returns zero-based index in the node's children of the first item
        which is x.

        :param expatriate.Node x: The node
        :param int start: Interpreted as the start in slice notation. Optional
        :param int end: Interpreted as the end in slice notation. Optional
        :rtype: int
        :raises ValueError: if there is no such item
        """
        return (self.children.index)(x, *args)

    def extend(self, iterable):
        """
        Extend the node's children by appending all the items from the
        iterable.

        :param list[expatriate.Node] iterable: The iterable which returns items appropriate for appending to the node's children
        """
        for c in iterable:
            self.append(c)

    def insert(self, i, x):
        """
        Insert an item at a given position in the node's children.

        :param int i: The index of the item before which to insert.
        :param expatriate.Node x: The node to insert.
        """
        from .CharacterData import CharacterData
        if isinstance(x, str):
            n = CharacterData(x, parent=self)
        else:
            if isinstance(x, int) or isinstance(x, float):
                n = CharacterData((str(x)), parent=self)
            else:
                if isinstance(x, Node):
                    n = x
                else:
                    raise ValueError('Children of ' + self.__class__.__name__ + ' must be subclass of Node; got: ' + x.__class__.__name__)
        self.children.insert(i, n)

    def pop(self, *args):
        """
        Remove the item at the given position in the node's children, and
        return it. If no index is specified, pop() removes and returns the last
        item in the children.

        :param int i: The position to remove. Optional.
        :rtype: expatriate.Node
        """
        n = (self.children.pop)(*args)
        self.detach(n)
        return n

    def remove(self, x):
        """
        Remove the first item from the node's children whose value is x. It is
        an error if there is no such item.

        :param expatriate.Node x: The node to remove.
        """
        n = self.children[self.children.index(x)]
        self.children.remove(x)

    def reverse(self):
        """
        Reverse the items of the node's children in place.
        """
        self.children.reverse()

    def sort(self, key=None, reverse=False):
        """
        Sort the items of the list in place.

        :param key: Specifies a function of one argument that is used to extract a comparison key from each list element: key=str.lower. Defaults to None (compare the elements directly).
        :type key: function or None
        :param bool reverse: A boolean value. If set to True, then the list elements are sorted as if each comparison were reversed. Defaults to False.
        """
        self.children.sort(key=key, reverse=reverse)

    def find_by_id(self, ref):
        logger.debug(str(self) + ' checking children for id: ' + str(ref))
        for c in self.children:
            el = c.find_by_id(ref)
            if el is not None:
                return el

        return super().find_by_id(ref)