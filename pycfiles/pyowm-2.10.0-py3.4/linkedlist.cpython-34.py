# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/abstractions/linkedlist.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2323 bytes
"""
Module containing abstractions for defining a linked list data structure
"""
from abc import ABCMeta, abstractmethod

class LinkedList(object):
    __doc__ = '\n    An abstract class representing a Linked List data structure. Each element\n    in the list should contain data and a reference to the next element in the\n    list.\n    '
    __metaclass__ = ABCMeta

    @abstractmethod
    def size(self):
        """
        Returns the number of elements in the list

        :returns: an int

        """
        raise NotImplementedError

    @abstractmethod
    def add(self, data):
        """
        Adds a new node to the list. Implementations should decide where
        to put this new element (at the top, in the middle or at the end of
        the list) and should therefore update pointers to next elements and
        the list's size.

        :param data: the data to be inserted in the new list node
        :type data: object

        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, data):
        """
        Removes a node from the list. Implementations should decide the
        policy to be followed when list items having the same data are to be
        removed, and should therefore update pointers to next elements and
        the list's size.

        :param data: the data to be removed in the new list node
        :type data: object

        """
        raise NotImplementedError

    @abstractmethod
    def contains(self, data):
        """
        Checks if the provided data is stored in at least one node of the list.

        :param data: data of the seeked node
        :type data: object
        :returns: a boolean

        """
        raise NotImplementedError

    @abstractmethod
    def index_of(self, data):
        """
        Finds the position of a node in the list. The index of the first
        occurrence of the data is returned (indexes start at 0)

        :param data: data of the seeked node
        :type: object
        :returns: the int index or -1 if the node is not in the list

        """
        raise NotImplementedError

    @abstractmethod
    def pop(self):
        """
        Removes the last node from the list

        :returns: the object data that was stored in the last node
        """
        raise NotImplementedError