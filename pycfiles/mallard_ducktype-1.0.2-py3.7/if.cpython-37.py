# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mallard/ducktype/extensions/if.py
# Compiled at: 2019-04-08 15:26:29
# Size of source mod 2**32: 3079 bytes
import mallard.ducktype
IFURI = 'http://projectmallard.org/if/1.0/'

class IfExtension(mallard.ducktype.parser.ParserExtension):

    def __init__(self, parser, prefix, version):
        if version == 'experimental':
            self.version = version
        else:
            raise mallard.ducktype.parser.SyntaxError('Unsupported if extension version: ' + version, parser)
        self.parser = parser
        self.prefix = prefix
        self.version = version
        self.parser.document.add_namespace('if', IFURI)

    def parse_line_block(self, line):
        indent = mallard.ducktype.parser.DuckParser.get_indent(line)
        iline = line[indent:]
        if iline.strip() == '??':
            self.parser.push_text()
            self.parser.unravel_for_block(indent)
            if self.parser.current.is_name('choose', IFURI):
                elname = 'if:else'
            else:
                elname = 'if:choose'
            qnode = mallard.ducktype.parser.Block(elname, indent, parser=(self.parser))
            self.parser.current.add_child(qnode)
            self.parser.current = qnode
            self.parser.state = mallard.ducktype.parser.DuckParser.STATE_BLOCK_READY
            return True
        if iline.startswith('? '):
            self.parser.push_text()
            self.parser.unravel_for_block(indent)
            if self.parser.current.is_name('choose', IFURI):
                elname = 'if:when'
            else:
                elname = 'if:if'
            qnode = mallard.ducktype.parser.Block(elname, indent, parser=(self.parser))
            qnode.attributes = mallard.ducktype.parser.Attributes()
            qnode.attributes.add_attribute('test', iline[2:].strip())
            self.parser.current.add_child(qnode)
            self.parser.current = qnode
            self.parser.state = mallard.ducktype.parser.DuckParser.STATE_BLOCK_READY
            return True
        return False