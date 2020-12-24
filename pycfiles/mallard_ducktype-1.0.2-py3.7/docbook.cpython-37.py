# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mallard/ducktype/extensions/docbook.py
# Compiled at: 2019-04-22 10:13:15
# Size of source mod 2**32: 5743 bytes
import mallard.ducktype
NSDB = 'http://docbook.org/ns/docbook'
leafs = ('abbrev', 'acronym', 'address', 'arg', 'artpagenums', 'authorinitials', 'bibliocoverage',
         'biblioid', 'bibliomisc', 'bibliomixed', 'bibliomset', 'bibliorelation',
         'bibliosource', 'bridgehead', 'caption', 'citation', 'classsynopsisinfo',
         'command', 'confdates', 'confnum', 'confsponsor', 'conftitle', 'contractnum',
         'contractsponsor', 'contrib', 'date', 'edition', 'email', 'exceptionname',
         'firstname', 'funcdef', 'funcparams', 'funcsynopsisinfo', 'givenname', 'glosssee',
         'glossseealso', 'glossterm', 'holder', 'honorific', 'initializer', 'issuenum',
         'jobtitle', 'keyword', 'lhs', 'lineage', 'link', 'literallayout', 'manvolnum',
         'member', 'methodname', 'modifier', 'msgaud', 'msglevel', 'msgorig', 'option',
         'orgdiv', 'orgname', 'othername', 'pagenums', 'para', 'paramdef', 'parameter',
         'personname', 'phrase', 'primary', 'primaryie', 'productname', 'productnumber',
         'programlisting', 'pubdate', 'publishername', 'quote', 'refclass', 'refdescriptor',
         'refentrytitle', 'refmiscinfo', 'refname', 'refpurpose', 'releaseinfo',
         'remark', 'replaceable', 'revnumber', 'revremark', 'rhs', 'screen', 'secondary',
         'secondaryie', 'see', 'seealso', 'seealsoie', 'seeie', 'seg', 'segtitle',
         'seriesvolnums', 'shortaffil', 'simpara', 'subjectterm', 'subtitle', 'surname',
         'synopfragmentref', 'synopsis', 'term', 'tertiary', 'tertiaryie', 'title',
         'titleabbrev', 'tocentry', 'type', 'uri', 'varname', 'volumenum', 'year')

class DocBookNodeFactory(mallard.ducktype.parser.NodeFactory):

    def __init__(self, parser):
        super().__init__(parser)
        self.id_attribute = 'xml:id'

    def create_block_node(self, name, outer):
        node = mallard.ducktype.parser.Block(name, outer=outer, parser=(self.parser))
        if name in leafs:
            node.is_leaf = True
        return node

    def create_block_paragraph_node(self, outer):
        return self.create_block_node('para', outer=outer)

    def create_info_node(self, name, outer):
        node = mallard.ducktype.parser.Info(name, outer=outer, parser=(self.parser))
        if name in leafs:
            node.is_leaf = True
        return node

    def create_info_paragraph_node(self, outer):
        return self.create_info_node('para', outer=outer)

    def handle_division_title(self, depth, inner):
        name = 'article' if depth == 1 else 'section'
        page = mallard.ducktype.parser.Division(name, depth=depth, parser=(self.parser))
        title = mallard.ducktype.parser.Block('title', inner=inner, parser=(self.parser))
        self.parser.current.add_child(page)
        page.add_child(title)
        self.parser.current = title

    def handle_info_container(self, outer):
        info = mallard.ducktype.parser.Block('info', outer=outer, parser=(self.parser))
        self.parser.current.add_child(info)
        self.parser.current.info = info
        info.parent = self.parser.current

    def handle_block_item_content(self, outer, inner):
        if self.parser.current.is_name(('itemizedlist', 'orderedlist')):
            item = mallard.ducktype.parser.Block('listitem', outer=outer, inner=inner, parser=(self.parser))
            self.parser.current.add_child(item)
            self.parser.current = item
            return item
        node = mallard.ducktype.parser.Block('itemizedlist', outer=outer, parser=(self.parser))
        self.parser.current.add_child(node)
        item = mallard.ducktype.parser.Block('listitem', outer=outer, inner=inner, parser=(self.parser))
        node.add_child(item)
        self.parser.current = item
        return item


class DocBookExtension(mallard.ducktype.parser.ParserExtension):

    def __init__(self, parser, prefix, version):
        if version == 'experimental':
            self.version = version
        else:
            raise mallard.ducktype.parser.SyntaxError('Unsupported docbook extension version: ' + version, parser)
        self.parser = parser
        self.prefix = prefix
        self.version = version
        self.parser.document.default_namespace = NSDB
        parser.factory = DocBookNodeFactory(parser)