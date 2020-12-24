# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/helper/list.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'ListFullError', 'ListEmptyError', 'List', 'Node', 'StaticList']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractmethod

class ListFullError(StandardError):
    pass


class ListEmptyError(StandardError):
    pass


class List(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert_left(self, element):
        pass

    @abstractmethod
    def append(self, element):
        pass

    @abstractmethod
    def pop_left(self):
        pass

    @abstractmethod
    def pop_right(self):
        pass

    @abstractmethod
    def is_full(self):
        pass

    @abstractmethod
    def peek_left(self):
        pass


class Node(object):

    def __init__(self, element=None, next=None):
        self._element = element
        self._next = next

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        self._element = element

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next


class StaticList(List):

    def __init__(self, max_size):
        assert max_size > 0, 'max size should be more than 0'
        self._nodes = [ Node() for _ in range(max_size) ]
        self._head = Node()
        self._space = Node()
        self._current_size = 0
        for ind in range(len(self._nodes) - 1):
            self._nodes[ind].next = self._nodes[(ind + 1)]

        self._space.next = self._nodes[0]

    def insert_left(self, element):
        node = self._space.next
        if node is None:
            raise ListFullError('list is full')
        self._space.next = node.next
        node.element = element
        self._current_size = self._current_size + 1
        node.next = self._head.next
        self._head.next = node
        return

    def pop_left(self):
        if self._current_size <= 0:
            raise ListEmptyError('list is empty')
        node = self._head.next
        try:
            return node.element
        finally:
            self._head.next = node.next
            self._current_size = self._current_size - 1
            node.next = self._space.next
            self._space.next = node

    def peek_left(self):
        if self._head.next is None:
            return
        else:
            return self._head.next.element

    def pop_right(self):
        raise NotImplementedError('not implemented now')

    def append(self):
        raise NotImplementedError('not implemented now')

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        raise RuntimeError('can not override head node')

    @property
    def size(self):
        return self._current_size

    @size.setter
    def size(self, size):
        raise RuntimeError('can not override size')

    def is_full(self):
        return self._space.next is None