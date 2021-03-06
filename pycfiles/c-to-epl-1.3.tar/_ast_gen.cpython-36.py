# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kukui/Development/pycparser/c-to-epl-1.3/ctoepl/_ast_gen.py
# Compiled at: 2018-04-15 19:34:18
# Size of source mod 2**32: 10603 bytes
import pprint
from string import Template

class ASTCodeGenerator(object):

    def __init__(self, cfg_filename='_c_ast.cfg'):
        """ Initialize the code generator from a configuration
            file.
        """
        self.cfg_filename = cfg_filename
        self.node_cfg = [NodeCfg(name, contents) for name, contents in self.parse_cfgfile(cfg_filename)]

    def generate(self, file=None):
        """ Generates the code into file, an open file buffer.
        """
        src = Template(_PROLOGUE_COMMENT).substitute(cfg_filename=(self.cfg_filename))
        src += _PROLOGUE_CODE
        for node_cfg in self.node_cfg:
            src += node_cfg.generate_source() + '\n\n'

        file.write(src)

    def parse_cfgfile(self, filename):
        """ Parse the configuration file and yield pairs of
            (name, contents) for each node.
        """
        with open(filename, 'r') as (f):
            for line in f:
                line = line.strip()
                if not not line:
                    if line.startswith('#'):
                        pass
                    else:
                        colon_i = line.find(':')
                        lbracket_i = line.find('[')
                        rbracket_i = line.find(']')
                        if colon_i < 1 or lbracket_i <= colon_i or rbracket_i <= lbracket_i:
                            raise RuntimeError('Invalid line in %s:\n%s\n' % (filename, line))
                        name = line[:colon_i]
                        val = line[lbracket_i + 1:rbracket_i]
                        vallist = [v.strip() for v in val.split(',')] if val else []
                        yield (name, vallist)


class NodeCfg(object):
    __doc__ = ' Node configuration.\n\n        name: node name\n        contents: a list of contents - attributes and child nodes\n        See comment at the top of the configuration file for details.\n    '

    def __init__(self, name, contents):
        self.name = name
        self.all_entries = []
        self.attr = []
        self.child = []
        self.seq_child = []
        for entry in contents:
            clean_entry = entry.rstrip('*')
            self.all_entries.append(clean_entry)
            if entry.endswith('**'):
                self.seq_child.append(clean_entry)
            else:
                if entry.endswith('*'):
                    self.child.append(clean_entry)
                else:
                    self.attr.append(entry)

    def generate_source(self):
        src = self._gen_init()
        src += '\n' + self._gen_children()
        src += '\n' + self._gen_iter()
        src += '\n' + self._gen_attr_names()
        return src

    def _gen_init(self):
        src = 'class %s(Node):\n' % self.name
        if self.all_entries:
            args = ', '.join(self.all_entries)
            slots = ', '.join("'{0}'".format(e) for e in self.all_entries)
            slots += ", 'coord', '__weakref__'"
            arglist = '(self, %s, coord=None)' % args
        else:
            slots = "'coord', '__weakref__'"
            arglist = '(self, coord=None)'
        src += '    __slots__ = (%s)\n' % slots
        src += '    def __init__%s:\n' % arglist
        for name in self.all_entries + ['coord']:
            src += '        self.%s = %s\n' % (name, name)

        return src

    def _gen_children(self):
        src = '    def children(self):\n'
        if self.all_entries:
            src += '        nodelist = []\n'
            for child in self.child:
                src += ('        if self.%(child)s is not None:' + ' nodelist.append(("%(child)s", self.%(child)s))\n') % dict(child=child)

            for seq_child in self.seq_child:
                src += '        for i, child in enumerate(self.%(child)s or []):\n            nodelist.append(("%(child)s[%%d]" %% i, child))\n' % dict(child=seq_child)

            src += '        return tuple(nodelist)\n'
        else:
            src += '        return ()\n'
        return src

    def _gen_iter(self):
        src = '    def __iter__(self):\n'
        if self.all_entries:
            for child in self.child:
                src += ('        if self.%(child)s is not None:\n' + '            yield self.%(child)s\n') % dict(child=child)

            for seq_child in self.seq_child:
                src += '        for child in (self.%(child)s or []):\n            yield child\n' % dict(child=seq_child)

            if not (self.child or self.seq_child):
                src += '        return\n' + '        yield\n'
        else:
            src += '        return\n' + '        yield\n'
        return src

    def _gen_attr_names(self):
        src = '    attr_names = (' + ''.join('%r, ' % nm for nm in self.attr) + ')'
        return src


_PROLOGUE_COMMENT = '#-----------------------------------------------------------------\n# ** ATTENTION **\n# This code was automatically generated from the file:\n# $cfg_filename\n#\n# Do not modify it directly. Modify the configuration file and\n# run the generator again.\n# ** ** *** ** **\n#\n# pycparser: c_ast.py\n#\n# AST Node classes.\n#\n# Eli Bendersky [http://eli.thegreenplace.net]\n# License: BSD\n#-----------------------------------------------------------------\n\n'
_PROLOGUE_CODE = '\nimport sys\n\ndef _repr(obj):\n    """\n    Get the representation of an object, with dedicated pprint-like format for lists.\n    """\n    if isinstance(obj, list):\n        return \'[\' + (\',\\n \'.join((_repr(e).replace(\'\\n\', \'\\n \') for e in obj))) + \'\\n]\'\n    else:\n        return repr(obj) \n\nclass Node(object):\n    __slots__ = ()\n    """ Abstract base class for AST nodes.\n    """\n    def __repr__(self):\n        """ Generates a python representation of the current node\n        """\n        result = self.__class__.__name__ + \'(\'\n        \n        indent = \'\'\n        separator = \'\'\n        for name in self.__slots__[:-2]:\n            result += separator\n            result += indent\n            result += name + \'=\' + (_repr(getattr(self, name)).replace(\'\\n\', \'\\n  \' + (\' \' * (len(name) + len(self.__class__.__name__)))))\n            \n            separator = \',\'\n            indent = \'\\n \' + (\' \' * len(self.__class__.__name__))\n        \n        result += indent + \')\'\n        \n        return result\n\n    def children(self):\n        """ A sequence of all children that are Nodes\n        """\n        pass\n\n    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):\n        """ Pretty print the Node and all its attributes and\n            children (recursively) to a buffer.\n\n            buf:\n                Open IO buffer into which the Node is printed.\n\n            offset:\n                Initial offset (amount of leading spaces)\n\n            attrnames:\n                True if you want to see the attribute names in\n                name=value pairs. False to only see the values.\n\n            nodenames:\n                True if you want to see the actual node names\n                within their parents.\n\n            showcoord:\n                Do you want the coordinates of each Node to be\n                displayed.\n        """\n        lead = \' \' * offset\n        if nodenames and _my_node_name is not None:\n            buf.write(lead + self.__class__.__name__+ \' <\' + _my_node_name + \'>: \')\n        else:\n            buf.write(lead + self.__class__.__name__+ \': \')\n\n        if self.attr_names:\n            if attrnames:\n                nvlist = [(n, getattr(self,n)) for n in self.attr_names]\n                attrstr = \', \'.join(\'%s=%s\' % nv for nv in nvlist)\n            else:\n                vlist = [getattr(self, n) for n in self.attr_names]\n                attrstr = \', \'.join(\'%s\' % v for v in vlist)\n            buf.write(attrstr)\n\n        if showcoord:\n            buf.write(\' (at %s)\' % self.coord)\n        buf.write(\'\\n\')\n\n        for (child_name, child) in self.children():\n            child.show(\n                buf,\n                offset=offset + 2,\n                attrnames=attrnames,\n                nodenames=nodenames,\n                showcoord=showcoord,\n                _my_node_name=child_name)\n\n\nclass NodeVisitor(object):\n    """ A base NodeVisitor class for visiting c_ast nodes.\n        Subclass it and define your own visit_XXX methods, where\n        XXX is the class name you want to visit with these\n        methods.\n\n        For example:\n\n        class ConstantVisitor(NodeVisitor):\n            def __init__(self):\n                self.values = []\n\n            def visit_Constant(self, node):\n                self.values.append(node.value)\n\n        Creates a list of values of all the constant nodes\n        encountered below the given node. To use it:\n\n        cv = ConstantVisitor()\n        cv.visit(node)\n\n        Notes:\n\n        *   generic_visit() will be called for AST nodes for which\n            no visit_XXX method was defined.\n        *   The children of nodes for which a visit_XXX was\n            defined will not be visited - if you need this, call\n            generic_visit() on the node.\n            You can use:\n                NodeVisitor.generic_visit(self, node)\n        *   Modeled after Python\'s own AST visiting facilities\n            (the ast module of Python 3.0)\n    """\n\n    _method_cache = None\n\n    def visit(self, node):\n        """ Visit a node.\n        """\n\n        if self._method_cache is None:\n            self._method_cache = {}\n\n        visitor = self._method_cache.get(node.__class__.__name__, None)\n        if visitor is None:\n            method = \'visit_\' + node.__class__.__name__\n            visitor = getattr(self, method, self.generic_visit)\n            self._method_cache[node.__class__.__name__] = visitor\n\n        return visitor(node)\n\n    def generic_visit(self, node):\n        """ Called if no explicit visitor function exists for a\n            node. Implements preorder visiting of the node.\n        """\n        for c in node:\n            self.visit(c)\n\n'