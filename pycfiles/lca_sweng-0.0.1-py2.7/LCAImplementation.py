# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lca_sweng\LCAImplementation.py
# Compiled at: 2019-10-17 16:52:02


class TreeNode:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        return


class LCA:

    def __init__(self):
        self.size = 0
        self.root = None
        return

    def isempty(self):
        return self.root is None

    def __size__(self):
        return self.size

    def insert(self, data):
        if data is None or type(data) is not int:
            return False
        if self.root is None:
            self.root = TreeNode(data)
            self.size += 1
            return True
        else:
            self.__insert(self.root, data)
            return True
            return

    def __insert(self, node, data):
        if node.data:
            if node.data > data:
                if node.left is None:
                    node.left = TreeNode(data)
                    self.size += 1
                else:
                    self.__insert(node.left, data)
            elif node.data < data:
                if node.right is None:
                    node.right = TreeNode(data)
                    self.size += 1
                else:
                    self.__insert(node.right, data)
        else:
            node.data = data
        return

    def findlca(self, a, b):
        if self.isempty():
            return False
        if type(a) is not int or type(b) is not int:
            return False
        path1 = []
        path2 = []
        if not self.__findpath(self.root, path1, a) or not self.__findpath(self.root, path2, b):
            return -1
        i = 0
        while i < len(path1) and i < len(path2):
            if path1[i] != path2[i]:
                break
            i += 1

        return path1[(i - 1)]

    def __findpath(self, node, path, k):
        if node is None:
            return False
        else:
            path.append(node.data)
            if node.data == k:
                return True
            if node.left is not None and self.__findpath(node.left, path, k) or node.right is not None and self.__findpath(node.right, path, k):
                return True
            path.pop()
            return False


def motivate_me():
    print 'you are doing great, keep it up'