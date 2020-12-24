# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/stack.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2788 bytes


class Stack(object):
    __doc__ = '\n    This class represents a simple version of a stack.\n    '

    def __init__(self):
        """
        Standard constructor.
        """
        self.list = list()
        self.currentIndex = -1

    def push(self, elem):
        """
        Pushes an element to the stack
        :param elem: a single element
        :type elem: object
        """
        self.currentIndex += 1
        self.list.append(elem)

    def pop(self):
        """
        Returns the last element on the stack.
        :return: a single object if not empty, otherwise None
        :rtype: object
        """
        if self.is_empty():
            return
        else:
            temp = self.list[self.currentIndex]
            self.currentIndex -= 1
            self.list.remove(temp)
            return temp

    def is_empty(self):
        """
        Returns true if this stack is empty.
        :return: True if empty, otherwise False.
        :rtype: bool
        """
        return len(self.list) == 0

    def top(self):
        return self.list[self.currentIndex]

    def pop_n_to_list(self, n):
        """
        Pops the first n items and returns them in a list
        :param n: the number of items
        :return: int
        """
        ret = list()
        for i in range(0, n):
            ret.append(self.pop())

        return ret

    def pop_n_first_to_list(self, n):
        """
        Pops the first n items and returns them in a list
        :param n: the number of items
        :return: int
        """
        ret = list()
        for i in range(0, n):
            ret.append(self.pop_first())

        return ret

    def pop_first(self):
        """
        Returns the first element on the stack.
        :return: a single object if not empty, otherwise None
        :rtype: object
        """
        if self.is_empty():
            return
        else:
            temp = self.list[0]
            self.currentIndex = self.currentIndex - 1
            self.list.remove(temp)
            return temp