# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mallard/ducktype/extensions/csv.py
# Compiled at: 2019-03-23 09:49:43
# Size of source mod 2**32: 3062 bytes
import mallard.ducktype

class CsvExtension(mallard.ducktype.parser.ParserExtension):

    def __init__(self, parser, prefix, version):
        if version == 'experimental':
            self.version = version
        else:
            raise mallard.ducktype.parser.SyntaxError('Unsupported csv extension version: ' + version, parser)
        self.parser = parser
        self.prefix = prefix
        self.version = version
        self.table = None

    def take_block_node(self, node):
        if node.name != 'csv:table':
            return False
        self.table = mallard.ducktype.parser.Block('table')
        self.table.is_greedy = False
        self.parser.current.add_child(self.table)
        self.parser.current = self.table
        return True

    def parse_line_block(self, line):
        if self.table is None:
            return False
        if self.table is not self.parser.current:
            self.table = None
            return False
        tr = mallard.ducktype.parser.Block('tr')
        self.parser.current.add_child(tr)
        cells = line.split(',')
        for cell in cells:
            td = mallard.ducktype.parser.Block('td')
            tr.add_child(td)
            tdp = mallard.ducktype.parser.Block('p')
            td.add_child(tdp)
            tdp.add_text(cell)

        return True