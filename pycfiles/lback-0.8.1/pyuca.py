# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/pyuca/pyuca.py
# Compiled at: 2013-10-14 11:16:24
"""
Preliminary implementation of the Unicode Collation Algorithm.

This only implements the simple parts of the algorithm but I have successfully
tested it using the Default Unicode Collation Element Table (DUCET) to collate
Ancient Greek correctly.

Usage example:

    from pyuca import Collator
    c = Collator("allkeys.txt")

    sorted_words = sorted(words, key=c.sort_key)

allkeys.txt (1 MB) is available at

    http://www.unicode.org/Public/UCA/latest/allkeys.txt

but you can always subset this for just the characters you are dealing with.
"""

class Node:

    def __init__(self):
        self.value = None
        self.children = {}
        return


class Trie:

    def __init__(self):
        self.root = Node()

    def add(self, key, value):
        curr_node = self.root
        for part in key:
            curr_node = curr_node.children.setdefault(part, Node())

        curr_node.value = value

    def find_prefix(self, key):
        curr_node = self.root
        remainder = key
        for part in key:
            if part not in curr_node.children:
                break
            curr_node = curr_node.children[part]
            remainder = remainder[1:]

        return (
         curr_node.value, remainder)


class Collator:

    def __init__(self, filename):
        self.table = Trie()
        self.load(filename)

    def load(self, filename):
        for line in open(filename):
            if line.startswith('#') or line.startswith('%'):
                continue
            if line.strip() == '':
                continue
            line = line[:line.find('#')] + '\n'
            line = line[:line.find('%')] + '\n'
            line = line.strip()
            if line.startswith('@'):
                pass
            else:
                semicolon = line.find(';')
                charList = line[:semicolon].strip().split()
                x = line[semicolon:]
                collElements = []
                while True:
                    begin = x.find('[')
                    if begin == -1:
                        break
                    end = x[begin:].find(']')
                    collElement = x[begin:begin + end + 1]
                    x = x[begin + 1:]
                    alt = collElement[1]
                    chars = collElement[2:-1].split('.')
                    collElements.append((alt, chars))

                integer_points = [ int(ch, 16) for ch in charList ]
                self.table.add(integer_points, collElements)

    def sort_key(self, string):
        collation_elements = []
        lookup_key = [ ord(ch) for ch in string ]
        while lookup_key:
            value, lookup_key = self.table.find_prefix(lookup_key)
            if not value:
                value = []
                value.append(('.', ['%X' % (64320 + (lookup_key[0] >> 15)), '0020', '0002', '0001']))
                value.append(('.', ['%X' % (lookup_key[0] & 32767 | 32768), '0000', '0000', '0000']))
                lookup_key = lookup_key[1:]
            collation_elements.extend(value)

        sort_key = []
        for level in range(4):
            if level:
                sort_key.append(0)
            for element in collation_elements:
                ce_l = int(element[1][level], 16)
                if ce_l:
                    sort_key.append(ce_l)

        return tuple(sort_key)