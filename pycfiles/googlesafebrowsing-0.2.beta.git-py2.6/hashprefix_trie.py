# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesafebrowsing/hashprefix_trie.py
# Compiled at: 2010-12-12 06:19:01
"""Simple trie implementation that is used by the SB client."""
import itertools

class HashprefixTrie(object):
    """Trie that maps hash prefixes to a list of values."""
    MIN_PREFIX_LEN = 4

    class Node(object):
        """Represents a node in the trie.

    Holds a list of values and a dict that maps char -> Node.
    """
        __slots__ = ('values', 'children', 'parent')

        def __init__(self, parent=None):
            self.values = []
            self.children = {}
            self.parent = parent

    def __init__(self):
        self._root = HashprefixTrie.Node()
        self._size = 0

    def _GetPrefixComponents(self, hashprefix):
        assert len(hashprefix) >= HashprefixTrie.MIN_PREFIX_LEN
        yield hashprefix[:HashprefixTrie.MIN_PREFIX_LEN]
        for char in hashprefix[HashprefixTrie.MIN_PREFIX_LEN:]:
            yield char

    def _GetNode(self, hashprefix, create_if_necessary=False):
        """Returns the trie node that will contain hashprefix.

    If create_if_necessary is True this method will create the necessary
    trie nodes to store hashprefix in the trie.
    """
        node = self._root
        for char in self._GetPrefixComponents(hashprefix):
            if char in node.children:
                node = node.children[char]
            elif create_if_necessary:
                node = node.children.setdefault(char, HashprefixTrie.Node(node))
            else:
                return

        return node

    def Insert(self, hashprefix, entry):
        """Insert entry with a given hash prefix."""
        self._GetNode(hashprefix, True).values.append(entry)
        self._size += 1

    def Delete(self, hashprefix, entry):
        """Delete a given entry with hash prefix."""
        node = self._GetNode(hashprefix)
        if node and entry in node.values:
            node.values.remove(entry)
            self._size -= 1
            while not node.values and not node.children and node.parent:
                node = node.parent
                if len(hashprefix) == HashprefixTrie.MIN_PREFIX_LEN:
                    del node.children[hashprefix]
                    break
                char, hashprefix = hashprefix[(-1)], hashprefix[:-1]
                del node.children[char]

    def Size(self):
        """Returns the number of values stored in the trie."""
        return self._size

    def GetPrefixMatches(self, fullhash):
        """Yields all values that have a prefix of the given fullhash."""
        node = self._root
        for char in self._GetPrefixComponents(fullhash):
            node = node.children.get(char, None)
            if not node:
                break
            for value in node.values:
                yield value

        return

    def PrefixIterator(self):
        """Iterator over all the hash prefixes that have values."""
        stack = [
         (
          '', self._root)]
        while stack:
            (hashprefix, node) = stack.pop()
            if node.values:
                yield hashprefix
            for (char, child) in node.children.iteritems():
                stack.append((hashprefix + char, child))