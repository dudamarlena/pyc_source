# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bktree/bktree.py
# Compiled at: 2016-08-24 12:36:18
# Size of source mod 2**32: 1306 bytes


class Node(object):

    def __init__(self, num):
        self.num = num
        self.children = {}

    def __str__(self):
        return self.num


class Tree(object):

    def __init__(self, nums=None):
        self.root = None
        if nums:
            for num in nums:
                self.add(num)

    def add(self, num):
        if self.root is None:
            self.root = Node(num)
        else:
            node = Node(num)
            curr = self.root
            distance = self._hamming(num, curr.num)
            while distance in curr.children:
                curr = curr.children[distance]
                distance = self._hamming(num, curr.num)

            curr.children[distance] = node
            node.parent = curr

    def search(self, num, max_distance):
        candidates = [self.root]
        found = []
        while len(candidates) > 0:
            node = candidates.pop(0)
            distance = self._hamming(node.num, num)
            if distance > max_distance:
                pass
            else:
                found.append(node)
                candidates.extend(node[child] for child in node.children if distance - max_distance <= child <= distance + max_distance)

        return found

    @staticmethod
    def _hamming(num1, num2):
        return bin(num1 ^ num2).count('1')