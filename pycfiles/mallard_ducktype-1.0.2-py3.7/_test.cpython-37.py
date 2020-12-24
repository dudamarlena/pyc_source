# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mallard/ducktype/extensions/_test.py
# Compiled at: 2019-03-23 09:43:18
# Size of source mod 2**32: 10533 bytes
import mallard.ducktype

class TestExtension(mallard.ducktype.parser.ParserExtension):

    def __init__(self, parser, prefix, version):
        if version == 'block':
            self.mode = 'block'
        else:
            if version == 'blocknode':
                self.mode = 'blocknode'
            else:
                if version == 'directive':
                    self.mode = 'directive'
                else:
                    raise mallard.ducktype.parser.SyntaxError('Unsupported _test extension version: ' + version, parser)
        self.parser = parser
        self.prefix = prefix
        self.version = version
        self.parser.document.add_namespace('test', 'http://projectmallard.org/test/')

    def parse_line_block(self, line):
        if self.mode != 'block':
            return False
        else:
            indent = mallard.ducktype.parser.DuckParser.get_indent(line)
            iline = line[indent:]
            return iline.startswith('*** ') or False
        self.parser.push_text()
        self.parser.unravel_for_block(indent)
        qnode = mallard.ducktype.parser.Block('test:TEST', indent, parser=(self.parser))
        qnode.attributes = mallard.ducktype.parser.Attributes()
        qnode.attributes.add_attribute('line', iline[4:].strip())
        self.parser.current.add_child(qnode)
        self.parser.current = qnode
        self.parser.state = mallard.ducktype.parser.DuckParser.STATE_BLOCK_READY
        return True

    def take_block_node(self, node):
        if self.mode != 'blocknode':
            return False
        if node.name != '_test:block':
            return False
        qnode = mallard.ducktype.parser.Block('note', outer=(node.outer), parser=(self.parser))
        qnode.attributes = mallard.ducktype.parser.Attributes()
        qnode.attributes.add_attribute('style', 'warning')
        if node.attributes is not None:
            for attr in node.attributes.get_attributes():
                qnode.attributes.add_attribute(attr, node.attributes.get_attribute(attr))

        self.parser.current.add_child(qnode)
        self.parser.current = qnode
        return True

    def take_directive(self, directive):
        if self.mode != 'directive':
            return False
        if directive.name == '_test:defines':
            self.parser.document.add_definition('TEST', 'This is a $em(test). It is only a $em[.strong](test).')
            return True
        return False