# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treedraw/parser.py
# Compiled at: 2017-10-18 08:39:32
# Size of source mod 2**32: 2894 bytes
from .tree import Tree
from .util import error, warning
import sys, re

class Parser:
    __doc__ = '\n    .tree file parser class\n    '

    def __init__(self, f):
        """
        :param f: name of file to parse
        """
        self.file = f
        self.def_regex = re.compile('^\\w+\\s*:\\s*.+$')
        self.child_regex = re.compile('^\\w+\\s*>\\s*\\w*(,\\s*\\w*)*$')
        self.tree = Tree()

    def load(self, f):
        with open(f, 'r') as (f):
            file_lines = f.read().split('\n')
        lines = []
        for line in file_lines:
            if not line:
                pass
            else:
                for statement in line.split(';'):
                    if statement.strip():
                        lines.append(statement.strip())

        return lines

    def make_tree(self):
        lines = self.load(self.file)
        for line in lines:
            self.parse_line(line)

        self.tree.check()
        return self.tree

    def parse_line(self, line):
        if line.startswith('::'):
            return self.parse_special(line[2:].strip())
        else:
            if self.def_regex.match(line):
                return self.parse_definition(line)
            if self.child_regex.match(line):
                return self.parse_child(line)
        self.syntax_error(line)

    def parse_special(self, line):
        keyword = line.split()[0]
        if keyword == 'root':
            symbol = line.split()[1]
            if not self.tree.exists(symbol):
                warning('root symbol {} does not exist'.format(symbol))
            self.tree.set_root(symbol)
        elif keyword == 'children':
            self.tree.children = 2

    def parse_definition(self, line):
        symbol = line.split(':')[0].strip()
        value = ':'.join(line.split(':')[1:]).strip()
        self.tree.add_symbol(symbol, value)

    def parse_child(self, line):
        parent = line.split('>')[0].strip()
        if not self.tree.exists(parent):
            return self.unknown_symbol(parent)
        children = line.split('>')[1].strip()
        children = [x.strip() for x in children.split(',')]
        children = [' ' if x == '' else x for x in children]
        for child in children:
            if not self.tree.exists(child):
                if child is not ' ':
                    return self.unknown_symbol(child)

        self.tree.add_children(parent, children)

    def syntax_error(self, string):
        error('syntax error in line "{}"'.format(string))

    def unknown_symbol(self, symbol):
        error('unknown symbol "{}"'.format(symbol))


if __name__ == '__main__':
    parser = Parser(sys.argv[1])
    tree = parser.make_tree()
    tree.print_levels()