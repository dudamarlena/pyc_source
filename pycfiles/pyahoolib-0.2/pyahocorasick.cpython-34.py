# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/wojtek/pyahocorasick/py/pyahocorasick.py
# Compiled at: 2016-04-28 14:34:30
# Size of source mod 2**32: 6373 bytes
__doc__ = '\n\tAho-Corasick string search algorithm.\n\n\tAuthor    : Wojciech Muła, wojciech_mula@poczta.onet.pl\n\tWWW       : http://0x80.pl\n\tLicense   : public domain\n'
from collections import deque
nil = object()

class TrieNode(object):
    """TrieNode"""
    __slots__ = [
     'char', 'output', 'fail', 'children']

    def __init__(self, char):
        """
                Constructs an empty node
                """
        self.char = char
        self.output = nil
        self.fail = nil
        self.children = {}

    def __repr__(self):
        """
                Textual representation of node.
                """
        if self.output is not nil:
            return "<TrieNode '%s' '%s'>" % (self.char, self.output)
        else:
            return "<TrieNode '%s'>" % self.char


class Trie(object):
    """Trie"""

    def __init__(self):
        """
                Construct an empty trie
                """
        self.root = TrieNode('')

    def __get_node(self, word):
        """
                Private function retrieving a final node of trie
                for given word

                Returns node or None, if the trie doesn't contain the word.
                """
        node = self.root
        for c in word:
            try:
                node = node.children[c]
            except KeyError:
                return

        return node

    def get(self, word, default=nil):
        """
                Retrieves output value associated with word.

                If there is no word returns default value,
                and if default is not given rises KeyError.
                """
        node = self._Trie__get_node(word)
        output = nil
        if node:
            output = node.output
        if output is nil:
            if default is nil:
                raise KeyError("no key '%s'" % word)
            else:
                return default
        else:
            return output

    def keys(self):
        """
                Generator returning all keys (i.e. word) stored in trie
                """
        for key, _ in self.items():
            yield key

    def values(self):
        """
                Generator returning all values associated with words stored in a trie.
                """
        for _, value in self.items():
            yield value

    def items(self):
        """
                Generator returning all keys and values stored in a trie.
                """
        L = []

        def aux(node, s):
            s = s + node.char
            if node.output is not nil:
                L.append((s, node.output))
            for child in node.children.values():
                if child is not node:
                    aux(child, s)
                    continue

        aux(self.root, '')
        return iter(L)

    def __len__(self):
        """
                Calculates number of words in a trie.
                """
        stack = deque()
        stack.append(self.root)
        n = 0
        while stack:
            node = stack.pop()
            if node.output is not nil:
                n += 1
            for child in node.children.values():
                stack.append(child)

        return n

    def add_word(self, word, value):
        """
                Adds word and associated value.

                If word already exists, its value is replaced.
                """
        if not word:
            return
        node = self.root
        for i, c in enumerate(word):
            try:
                node = node.children[c]
            except KeyError:
                n = TrieNode(c)
                node.children[c] = n
                node = n

        node.output = value

    def clear(self):
        """
                Clears trie.
                """
        self.root = TrieNode('')

    def exists(self, word):
        """
                Checks if whole word is present in the trie.
                """
        node = self._Trie__get_node(word)
        if node:
            return bool(node.output != nil)
        else:
            return False

    def match(self, word):
        """
                Checks if word is a prefix of any existing word in the trie.
                """
        return self._Trie__get_node(word) is not None

    def make_automaton(self):
        """
                Converts trie to Aho-Corasick automaton.
                """
        queue = deque()
        for i in range(256):
            c = chr(i)
            if c in self.root.children:
                node = self.root.children[c]
                node.fail = self.root
                queue.append(node)
            else:
                self.root.children[c] = self.root

        while queue:
            r = queue.popleft()
            for node in r.children.values():
                queue.append(node)
                state = r.fail
                while node.char not in state.children:
                    state = state.fail

                node.fail = state.children.get(node.char, self.root)

    def iter(self, string):
        """
                Generator performs Aho-Corasick search string algorithm, yielding
                tuples containing two values:
                - position in string
                - outputs associated with matched strings
                """
        state = self.root
        for index, c in enumerate(string):
            while c not in state.children:
                state = state.fail

            state = state.children.get(c, self.root)
            tmp = state
            output = []
            while tmp is not nil:
                if tmp.output is not nil:
                    output.append(tmp.output)
                tmp = tmp.fail

            if output:
                yield (
                 index, output)
                continue

    def iter_long(self, string, overlapping=False):
        """
                Generator performs a modified Aho-Corasick search string algorithm,
                which maches only the longest word.

                """
        state = self.root
        last = None
        index = 0
        while index < len(string):
            c = string[index]
            if c in state.children:
                state = state.children[c]
                if state.output is not nil:
                    last = (state.output, index)
                index += 1
            else:
                if last:
                    yield last
                if overlapping or not last:
                    while c not in state.children:
                        state = state.fail

                else:
                    index = last[1] + 1
                    state = self.root
                    last = None

        if last:
            yield last

    def find_all(self, string, callback):
        """
                Wrapper on iter method, callback gets an iterator result
                """
        for index, output in self.iter(string):
            callback(index, output)


if __name__ == '__main__':

    def demo():
        words = 'he hers his she hi him man'.split()
        t = Trie()
        for w in words:
            t.add_word(w, w)

        s = 'he rshershidamanza '
        t.make_automaton()
        for res in t.items():
            print(res)

        for res in t.iter(s):
            print
            print('%s' % s)
            pos, matches = res
            for fragment in matches:
                print('%s%s' % ((pos - len(fragment) + 1) * ' ', fragment))


    demo()

    def bug():
        patterns = [
         'GT-C3303', 'SAMSUNG-GT-C3303K/']
        text = 'SAMSUNG-GT-C3303i/1.0 NetFront/3.5 Profile/MIDP-2.0 Configuration/CLDC-1.1'
        t = Trie()
        for pattern in patterns:
            ret = t.add_word(pattern, (0, pattern))

        t.make_automaton()
        res = list(t.iter(text))
        assert len(res) == 1, 'failed'


    bug()