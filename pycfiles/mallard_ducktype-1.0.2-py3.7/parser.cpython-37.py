# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mallard/ducktype/parser.py
# Compiled at: 2019-07-19 10:38:27
# Size of source mod 2**32: 71487 bytes
import collections, importlib, inspect, os, sys, urllib.parse
from . import entities

def FIXME(msg=None):
    if msg is not None:
        print('FIXME: %s' % msg)
    else:
        print('FIXME')


def _escape_xml_attr(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')


def _escape_xml(s):
    return s.replace('&', '&amp;').replace('<', '&lt;')


_escaped_chars = '$*=-.@[]()"\''

class Attributes:

    def __init__(self):
        self._attrlist = []
        self._attrvals = {}

    def add_attribute(self, key, value):
        if key not in self._attrlist:
            self._attrlist.append(key)
        elif key in ('style', 'type'):
            self._attrvals.setdefault(key, [])
            self._attrvals[key].append(value)
        else:
            self._attrvals[key] = value

    def get_attribute(self, key):
        val = self._attrvals.get(key)
        if isinstance(val, list):
            return ' '.join(val)
        return val

    def get_attributes(self):
        return self._attrlist

    def __contains__(self, item):
        return item in self._attrlist

    def _write_xml(self, fd):
        for attr in self._attrlist:
            fd.write(' ' + attr + '="')
            val = self._attrvals[attr]
            if isinstance(val, list):
                fd.write(' '.join([_escape_xml_attr(s) for s in val]))
            else:
                fd.write(_escape_xml_attr(val))
            fd.write('"')


class Directive:

    def __init__(self, name):
        self.name = name
        self.content = ''

    def set_content(self, content):
        self.content = content

    @staticmethod
    def parse_line(line, parser):
        i = 1
        while i < len(line):
            if line[i].isspace():
                break
            i += 1

        if i == 1:
            raise SyntaxError('Directive must start with a name', parser)
        directive = Directive(line[1:i])
        directive.set_content(line[i:].lstrip().rstrip('\n'))
        return directive


class Node:

    def __init__(self, name, outer=0, inner=None, parser=None, linenum=None, extensions=False):
        self.name = name
        self.nsprefix = None
        self.nsuri = None
        self.localname = name
        self.default_namespace = None
        self.extension = None
        self.is_external = False
        if ':' in name:
            self.nsprefix = name[:name.index(':')]
            self.nsuri = parser.document.get_namespace(self.nsprefix)
            self.localname = self.name[len(self.nsprefix) + 1:]
            if self.nsuri is not None:
                if not self.nsuri.startswith('http://projectmallard.org/'):
                    self.is_external = True
        elif extensions:
            if parser is not None:
                if self.nsprefix in parser.extensions_by_module:
                    self.extension = self.nsprefix
            elif self.extension is None and self.nsuri is None:
                if self.nsprefix == 'xml':
                    pass
                elif self.nsprefix == 'its':
                    parser.document.add_namespace('its', 'http://www.w3.org/2005/11/its')
                else:
                    raise SyntaxError('Unrecognized namespace prefix: ' + self.nsprefix, parser)
            else:
                self.localname = name
            self.outer = outer
            if inner is None:
                self.inner = outer
        else:
            self.inner = inner
        self.info = None
        self.children = []
        self.attributes = None
        self.is_verbatim = name in ('screen', 'code')
        self.is_list = name in ('list', 'steps', 'terms', 'tree')
        self.is_greedy = self.is_name(('list', 'steps', 'terms', 'tree', 'table', 'thead',
                                       'tfoot', 'tbody', 'tr'))
        self._is_leaf = None
        self.linenum = linenum
        if self.linenum is None:
            if parser is not None:
                self.linenum = parser.linenum
        self._namespaces = collections.OrderedDict()
        self._definitions = {}
        self._parent = None
        self._softbreak = False

    def is_name(self, localname, nsuri=None):
        if nsuri in (None, 'http://projectmallard.org/1.0/'):
            if self.nsuri not in (None, 'http://projectmallard.org/1.0/'):
                return False
        elif nsuri != self.nsuri:
            return False
        if isinstance(localname, (list, tuple)):
            for name in localname:
                if name == self.localname:
                    return True

            return False
        return localname == self.localname

    @property
    def is_leaf(self):
        if self._is_leaf is not None:
            return self._is_leaf
        else:
            leafs = ('p', 'screen', 'code', 'title', 'subtitle', 'desc', 'cite', 'name',
                     'email', 'years')
            if self.is_name(leafs):
                return True
            if self.nsprefix is not None:
                if self.nsuri is None:
                    return False
                if self.nsuri == 'http://projectmallard.org/1.0/':
                    return self.localname in leafs
        return False

    @is_leaf.setter
    def is_leaf(self, is_leaf):
        self._is_leaf = is_leaf

    @property
    def is_tree_item(self):
        if not self.is_name('item'):
            return False
        cur = self
        while cur.is_name('item'):
            cur = cur.parent

        if cur.is_name('tree'):
            return True
        return False

    @property
    def has_tree_items(self):
        if self.is_tree_item:
            for item in self.children:
                if isinstance(item, Node) and item.is_name('item'):
                    return True

        return False

    @property
    def is_external_leaf(self):
        if not self.is_external:
            return False
        if len(self.children) == 0:
            return False
        if isinstance(self.children[0], str) or isinstance(self.children[0], Inline):
            return True
        return False

    @property
    def is_empty(self):
        return len(self.children) == 0 and self.info is None

    @property
    def available(self):
        for child in self.children:
            if not child.is_name(('info', 'title', 'desc', 'cite')):
                return False

        return True

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        self._parent = node

    def add_child(self, child):
        if isinstance(child, str):
            self.add_text(child)
            return
        if self._softbreak:
            if len(self.children) > 0:
                self.children[(-1)] += '\n'
            self._softbreak = False
        self.children.append(child)
        child.parent = self

    def insert_child(self, index, child):
        self.children.insert(index, child)
        child.parent = self

    def add_text(self, text):
        if self._softbreak:
            if len(self.children) > 0:
                self.children[(-1)] += '\n'
            self._softbreak = False
        else:
            if not isinstance(self, Inline):
                if text.endswith('\n'):
                    text = text[:-1]
                    self._softbreak = True
            if len(self.children) > 0 and isinstance(self.children[(-1)], str):
                self.children[(-1)] += text
            else:
                self.children.append(text)

    def add_namespace(self, prefix, uri):
        self._namespaces[prefix] = uri

    def get_namespace(self, prefix):
        uri = self._namespaces.get(prefix)
        if uri is not None:
            return uri
        if self._parent is not None:
            return self._parent.get_namespace(prefix)

    def add_definition(self, name, value):
        self._definitions[name] = value

    def write_xml(self, outfile=None):
        close = False
        if outfile is None:
            fd = sys.stdout
        else:
            if isinstance(outfile, str):
                close = True
                fd = open(outfile, 'w', encoding='utf-8')
            else:
                fd = outfile
        self._write_xml(fd)
        if close:
            fd.close()

    def _write_xml(self, fd, *, depth=0, verbatim=False):
        verbatim = verbatim or self.is_verbatim
        if not isinstance(self, Inline):
            fd.write(' ' * depth)
        else:
            fd.write('<' + self.name)
            if self.default_namespace is not None:
                fd.write(' xmlns="' + self.default_namespace + '"')
            else:
                for prefix in self._namespaces:
                    fd.write(' xmlns:' + prefix + '="' + self._namespaces[prefix] + '"')

                if self.attributes is not None:
                    self.attributes._write_xml(fd)
                elif self.is_empty:
                    if isinstance(self, Inline):
                        fd.write('/>')
                    else:
                        fd.write('/>\n')
                elif isinstance(self.children[0], Block) or isinstance(self.children[0], Info):
                    fd.write('>\n')
                else:
                    fd.write('>')
            for i in range(len(self.children)):
                child = self.children[i]
                if isinstance(child, Inline):
                    child._write_xml(fd, depth=depth, verbatim=verbatim)
                elif isinstance(child, Fence):
                    child._write_xml(fd, depth=depth, verbatim=verbatim)
                    if i + 1 < len(self.children):
                        fd.write('\n')
                    elif isinstance(child, Node):
                        child._write_xml(fd, depth=(depth + 1), verbatim=verbatim)
                elif i > 0 and isinstance(self.children[(i - 1)], Fence):
                    if not verbatim:
                        fd.write(' ' * depth)
                    if '\n' in child:
                        nl = child.find('\n')
                        while nl >= 0:
                            if nl + 1 == len(child) and i + 1 == len(self.children):
                                fd.write(_escape_xml(child[:nl]))
                            else:
                                if not (verbatim or nl + 1) < len(child) or child[(nl + 1)] == '\n':
                                    fd.write(_escape_xml(child[:nl]) + '\n')
                                else:
                                    if self.is_tree_item:
                                        fd.write(_escape_xml(child[:nl]) + '\n')
                                        if nl + 1 < len(child):
                                            fd.write(' ' * (depth + 1))
                                    else:
                                        fd.write(_escape_xml(child[:nl]) + '\n' + ' ' * depth)
                            child = child[nl + 1:]
                            nl = child.find('\n')

                        if child != '':
                            fd.write(_escape_xml(child))
                else:
                    fd.write(_escape_xml(child))

            if not self.is_empty:
                leafy = self.is_leaf or self.is_external_leaf
                for child in self.children:
                    if isinstance(child, (Block, Info)):
                        leafy = False
                        break

                if isinstance(self, Inline):
                    fd.write('</' + self.name + '>')
                else:
                    if leafy:
                        fd.write('</' + self.name + '>\n')
                    else:
                        if self.is_tree_item:
                            if self.has_tree_items:
                                fd.write(' ' * depth + '</' + self.name + '>\n')
                        else:
                            fd.write('</' + self.name + '>\n')
            else:
                fd.write(' ' * depth + '</' + self.name + '>\n')


class Document(Node):

    def __init__(self, parser=None):
        Node.__init__(self, '_', parser=parser)
        self.divdepth = 0
        self.default_namespace = 'http://projectmallard.org/1.0/'

    def _write_xml(self, fd, *args, depth=0, verbatim=False):
        if len(self.children) == 1:
            fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        for child in self.children:
            if child.default_namespace is None:
                child.default_namespace = self.default_namespace
            for ns in self._namespaces:
                child.add_namespace(ns, self._namespaces[ns])

            child._write_xml(fd)


class Division(Node):

    def __init__(self, name, depth, **kwargs):
        (Node.__init__)(self, name, **kwargs)
        self.divdepth = depth


class Block(Node):
    pass


class Info(Node):
    pass


class Inline(Node):
    pass


class Fence(Node):

    def add_line(self, line):
        self.add_text(line)
        return
        self.children[0] += line[min(indent, self.inner):]
        if not line.endswith('\n'):
            self.children[0] += '\n'

    def _write_xml(self, fd, *, depth=0, verbatim=False):
        lines = self.children[0].split('\n')
        trim = min(self.inner, DuckParser.get_indent(lines[0]))
        for i in range(len(lines)):
            line = lines[i]
            indent = DuckParser.get_indent(line)
            if i != 0:
                fd.write('\n')
            fd.write(_escape_xml(line[min(indent, trim):]))


class NodeFactory:

    def __init__(self, parser):
        self.parser = parser
        self.id_attribute = 'id'

    def create_info_node(self, name, outer):
        node = Info(name, outer=outer, parser=(self.parser), extensions=True)
        return node

    def create_info_paragraph_node(self, outer):
        node = Info('p', outer=outer, parser=(self.parser))
        return node

    def create_block_node(self, name, outer):
        node = Block(name, outer=outer, parser=(self.parser), extensions=True)
        return node

    def create_block_paragraph_node(self, outer):
        node = Block('p', outer=outer, parser=(self.parser))
        return node

    def handle_division_title(self, depth, inner):
        name = 'page' if depth == 1 else 'section'
        page = Division(name, depth=depth, parser=(self.parser))
        title = Block('title', inner=inner, parser=(self.parser))
        self.parser.current.add_child(page)
        page.add_child(title)
        self.parser.current = title

    def handle_division_subtitle(self, depth, inner):
        node = Block('subtitle', inner=inner, parser=(self.parser))
        self.parser.current.add_child(node)
        self.parser.current = node

    def handle_info_container(self, outer):
        info = Block('info', outer=outer, parser=(self.parser))
        self.parser.current.insert_child(0, info)
        self.parser.current.info = info
        info.parent = self.parser.current

    def handle_block_title(self, outer, inner):
        title = Block('title', outer, inner, parser=(self.parser))
        self.parser.current.add_child(title)
        self.parser.current = title

    def handle_block_item_title(self, outer, inner):
        if self.parser.current.is_name('tr'):
            node = Block('th', outer, inner, parser=(self.parser))
            self.parser.current.add_child(node)
            self.parser.current = node
            return
            if not self.parser.current.is_name('terms'):
                node = Block('terms', outer, parser=(self.parser))
                self.parser.current.add_child(node)
                self.parser.current = node
        else:
            if not self.parser.current.is_empty:
                if isinstance(self.parser.current.children[(-1)], Block):
                    if self.parser.current.children[(-1)].is_name('item'):
                        item = self.parser.current.children[(-1)]
                        if not item.is_empty:
                            if isinstance(self.parser.current.children[(-1)], Block):
                                if item.children[(-1)].is_name('title'):
                                    self.parser.current = item
            item = self.parser.current.is_name('item') or Block('item', outer, inner, parser=(self.parser))
            self.parser.current.add_child(item)
            self.parser.current = item
        title = Block('title', outer, inner, parser=(self.parser))
        self.parser.current.add_child(title)
        self.parser.current = title

    def handle_block_item_content(self, outer, inner):
        if self.parser.current.is_name('tr'):
            node = Block('td', outer=outer, inner=inner, parser=(self.parser))
            self.parser.current.add_child(node)
            self.parser.current = node
            return node
        if self.parser.current.is_name('terms'):
            if not (self.parser.current.is_empty or self.parser.current.children[(-1)].is_name('item')):
                raise SyntaxError('Missing item title in terms', self.parser)
            self.parser.current = self.parser.current.children[(-1)]
            return self.parser.current
        if self.parser.current.is_name('tree') or self.parser.current.is_tree_item:
            item = Block('item', outer=outer, inner=inner, parser=(self.parser))
            self.parser.current.add_child(item)
            self.parser.current = item
            return item
        if self.parser.current.is_name(('list', 'steps')):
            item = Block('item', outer=outer, inner=inner, parser=(self.parser))
            self.parser.current.add_child(item)
            self.parser.current = item
            return item
        node = Block('list', outer=outer, parser=(self.parser))
        self.parser.current.add_child(node)
        item = Block('item', outer=outer, inner=inner, parser=(self.parser))
        node.add_child(item)
        self.parser.current = item
        return item


class SyntaxError(Exception):

    def __init__(self, message, parser):
        self.message = message
        self.parser = parser
        self.filename = parser.filename if parser else None
        self.linenum = parser.linenum if parser else None
        self.fullmessage = ''
        if self.filename is not None:
            self.fullmessage += os.path.basename(self.filename)
            if self.linenum is not None:
                self.fullmessage += ':' + str(self.linenum)
            self.fullmessage += ': '
        self.fullmessage += self.message


class ParserExtension:

    def __init__(self, parser, prefix, version):
        pass

    def parse_line_block(self, line):
        return False

    def take_directive(self, directive):
        return False

    def take_block_node(self, node):
        return False


class InlineParser:

    def __init__(self, parent, linenum=1):
        self.current = Inline('_', linenum=linenum)
        self.document = parent.document
        self.filename = parent.filename
        self.linenum = linenum
        self._parent = parent

    def lookup_entity(self, entity):
        return self._parent.lookup_entity(entity)

    def parse_text(self, text):
        self._parse_text(text)
        while self.current.parent is not None:
            self.current = self.current.parent

        return self.current.children

    def _parse_text(self, text):
        start = cur = 0
        parens = []
        while cur < len(text):
            if self.current.parent is not None and text[cur] == ')':
                if len(parens) > 0 and parens[(-1)] > 0:
                    parens[(-1)] -= 1
                    cur += 1
                else:
                    self.current.add_text(text[start:cur])
                    self.current = self.current.parent
                    parens.pop()
                    cur += 1
                    start = cur
            elif self.current.parent is not None and text[cur] == '(':
                parens[(-1)] += 1
                cur += 1
            elif cur == len(text) - 1:
                cur += 1
                self.current.add_text(text[start:cur])
            elif text[cur] == '$' and text[(cur + 1)] in _escaped_chars:
                self.current.add_text(text[start:cur])
                self.current.add_text(text[(cur + 1)])
                cur += 2
                start = cur
            elif text[cur] == '$' and _isnmtoken(text[(cur + 1)]):
                end = cur + 1
                while end < len(text):
                    if not _isnmtoken(text[end]):
                        break
                    end += 1

                if end == len(text):
                    self.current.add_text(text[start:end])
                    cur = end
                elif text[end] == ';':
                    self.current.add_text(text[start:cur])
                    entname = text[cur + 1:end]
                    entval = self._parent.lookup_entity(entname)
                    if entval is not None:
                        parser = InlineParser(self, linenum=(self.current.linenum))
                        for child in parser.parse_text(entval):
                            if isinstance(child, str):
                                self.current.add_text(child)
                            else:
                                self.current.add_child(child)

                    else:
                        raise SyntaxError('Unrecognized entity: ' + entname, self)
                    start = cur = end + 1
                elif text[end] == '[':
                    self.current.add_text(text[start:cur])
                    node = Inline((text[cur + 1:end]), parser=self)
                    self.current.add_child(node)
                    attrparser = AttributeParser(self)
                    attrparser.parse_line(text[end + 1:])
                    if not attrparser.finished:
                        FIXME('unclosed attribute list')
                    node.attributes = attrparser.attributes
                    self.linenum = attrparser.linenum
                    start = cur = len(text) - len(attrparser.remainder)
                    if cur < len(text) and text[cur] == '(':
                        self.current = node
                        parens.append(0)
                        start = cur = cur + 1
                elif text[end] == '(':
                    self.current.add_text(text[start:cur])
                    node = Inline((text[cur + 1:end]), parser=self)
                    self.current.add_child(node)
                    self.current = node
                    parens.append(0)
                    start = cur = end + 1
                else:
                    cur = end
            else:
                if text[cur] == '\n':
                    self.linenum += 1
                cur += 1


class AttributeParser:

    def __init__(self, parent, node=None):
        self.remainder = ''
        self.node = node
        self.attributes = Attributes()
        self.finished = False
        self.filename = parent.filename
        self.linenum = parent.linenum
        self._quote = None
        self._value = ''
        self._attrname = None
        self._parent = parent

    def lookup_entity(self, entity):
        return self._parent.lookup_entity(entity)

    def parse_value(self, text):
        retval = ''
        start = cur = 0
        while cur < len(text):
            if text[cur] == '$':
                if cur == len(text) - 1:
                    cur += 1
                    retval += text[start:cur]
                    start = cur
                elif text[cur] == '$' and text[(cur + 1)] in _escaped_chars:
                    retval += text[start:cur]
                    retval += text[(cur + 1)]
                    cur += 2
                    start = cur
                elif text[cur] == '$':
                    if _isnmtoken(text[(cur + 1)]):
                        end = cur + 1
                        while end < len(text):
                            if not _isnmtoken(text[end]):
                                break
                            end += 1

                        if end == len(text):
                            retval += text[start:end]
                            start = cur = end
                    elif text[end] == ';':
                        retval += text[start:cur]
                        start = cur
                        entname = text[cur + 1:end]
                        entval = self.lookup_entity(entname)
                        if entval is not None:
                            parser = AttributeParser(self)
                            retval += parser.parse_value(entval)
                        else:
                            raise SyntaxError('Unrecognized entity: ' + entname, self)
                        start = cur = end + 1
                    else:
                        cur = end
                else:
                    cur += 1
            else:
                if text[cur] == '\n':
                    self.linenum += 1
                cur += 1

        if cur != start:
            retval += text[start:cur]
        return retval

    def parse_line(self, line):
        i = 0
        while i < len(line) and not self.finished:
            if self._quote is not None:
                j = i
                while j < len(line):
                    if line[j] == '$':
                        if j + 1 < len(line) and line[j] in _escaped_chars:
                            j += 2
                        else:
                            j += 1
                    elif line[j] == self._quote:
                        self._value += line[i:j]
                        self._value = self.parse_value(self._value)
                        self.attributes.add_attribute(self._attrname, self._value)
                        self._value = ''
                        self._quote = None
                        i = j
                        break
                    else:
                        j += 1

                if self._quote is not None:
                    self._value += line[i:j]
                i = j + 1
            elif line[i].isspace():
                if line[i] == '\n':
                    self.linenum += 1
                i += 1
            elif line[i] == ']':
                self.finished = True
                self.remainder = line[i + 1:]
            elif line[i] in ('.', '#', '>'):
                j = i + 1
                while j < len(line) and not line[j].isspace():
                    if line[j] == ']':
                        break
                    j += 1

                word = self.parse_value(line[i + 1:j])
                if line[i] == '>':
                    if len(line) > i + 1 and line[(i + 1)] == '>':
                        self.attributes.add_attribute('href', word[1:])
                    else:
                        self.attributes.add_attribute('xref', word)
                else:
                    if line[i] == '.':
                        self.attributes.add_attribute('style', word)
                    else:
                        self.attributes.add_attribute('id', word)
                i = j
            else:
                j = i
                while j < len(line) and _isnmtoken(line[j]):
                    j += 1

                word = line[i:j]
                if line[j] == '=':
                    if word != '':
                        if ':' in word:
                            nsprefix, localname = word.split(':', maxsplit=1)
                            nsuri = self._parent.document.get_namespace(nsprefix)
                            if nsprefix == 'xml' if nsuri is None else nsprefix == 'its':
                                self._parent.document.add_namespace('its', 'http://www.w3.org/2005/11/its')
                    else:
                        raise SyntaxError('Unrecognized namespace prefix: ' + nsprefix, self)
                    if line[(j + 1)] in ('"', "'"):
                        self._quote = line[(j + 1)]
                        self._value = ''
                        i = j + 2
                        self._attrname = word
                    else:
                        k = j + 1
                        while k < len(line) and not line[k].isspace():
                            if line[k] == ']':
                                break
                            k += 1

                        value = self.parse_value(line[j + 1:k])
                        self.attributes.add_attribute(word, value)
                        i = k
                elif line[j].isspace() or line[j] == ']':
                    value = self.parse_value(line[i:j])
                    self.attributes.add_attribute('type', value)
                    i = j
                else:
                    raise SyntaxError('Invalid character ' + line[j] + ' in attribute list', self)


class DirectiveIncludeParser:

    def __init__(self, parent):
        self.parent = parent
        self.document = parent.document
        self.extensions = []
        self.extensions_by_module = {}
        self._start = True
        self._comment = False

    def parse_file(self, filename):
        self.filename = filename
        self.absfilename = os.path.join(os.path.dirname(self.parent.absfilename), filename)
        if isinstance(self.parent, DuckParser):
            self._parentfiles = [
             self.parent.absfilename, self.absfilename]
        else:
            self._parentfiles = self.parent._parentfiles + [self.absfilename]
        self.linenum = 0
        try:
            fd = open((self.absfilename), encoding='utf-8')
        except:
            raise SyntaxError('Missing included file ' + filename, self.parent)

        for line in fd:
            self.parse_line(line)

        fd.close()

    def parse_line(self, line):
        self.linenum += 1
        if self._comment:
            if line.strip() == '--]':
                self._comment = False
            return
        indent = DuckParser.get_indent(line)
        iline = line[indent:]
        if iline.startswith('[-]'):
            return
        if iline.startswith('[--'):
            self._comment = True
            return
        if line.strip() == '':
            return
        if not line.startswith('@'):
            raise SyntaxError('Directive includes can only include directives', self)
        self._parse_line(line)

    def take_directive(self, directive):
        if directive.name.startswith('ducktype/'):
            if not self._start:
                raise SyntaxError('Ducktype declaration must be first', self)
            if directive.name != 'ducktype/1.0':
                raise SyntaxError('Unsupported ducktype version: ' + directive.name, self)
            for value in directive.content.split():
                try:
                    prefix, version = value.split('/', maxsplit=1)
                    extmod = importlib.import_module('mallard.ducktype.extensions.' + prefix)
                    for extclsname, extcls in inspect.getmembers(extmod, inspect.isclass):
                        if issubclass(extcls, ParserExtension):
                            extension = extcls(self, prefix, version)
                            self.extensions.append(extension)
                            self.extensions_by_module.setdefault(prefix, [])
                            self.extensions_by_module[prefix].append(extension)

                except SyntaxError as e:
                    try:
                        raise e
                    finally:
                        e = None
                        del e

                except:
                    raise SyntaxError('Unsupported ducktype extension: ' + value, self)

        else:
            if ':' in directive.name:
                prefix, name = directive.name.split(':', maxsplit=1)
                if prefix not in self.extensions_by_module:
                    raise SyntaxError('Unrecognized directive prefix: ' + prefix, self)
                for extension in self.extensions_by_module[prefix]:
                    if extension.take_directive(directive):
                        return

                raise SyntaxError('Unrecognized directive: ' + directive.name, self)
            else:
                if directive.name == 'define':
                    try:
                        self.parent.take_directive(directive)
                    except SyntaxError as e:
                        try:
                            raise SyntaxError(e.message, self)
                        finally:
                            e = None
                            del e

                else:
                    if directive.name == 'encoding':
                        FIXME('encoding')
                    else:
                        if directive.name == 'include':
                            if ' ' in directive.content:
                                raise SyntaxError('Multiple values in include. URL encode file name?', self)
                            relfile = urllib.parse.unquote(directive.content)
                            absfile = os.path.join(os.path.dirname(self.absfilename), relfile)
                            if absfile in self._parentfiles:
                                raise SyntaxError('Recursive include detected: ' + directive.content, self)
                            incparser = DirectiveIncludeParser(self)
                            incparser.parse_file(relfile)
                        else:
                            if directive.name == 'namespace':
                                try:
                                    self.parent.take_directive(directive)
                                except SyntaxError as e:
                                    try:
                                        raise SyntaxError(e.message, self)
                                    finally:
                                        e = None
                                        del e

                            else:
                                raise SyntaxError('Unrecognized directive: ' + directive.name, self)
        self._start = False

    def _parse_line(self, line):
        directive = Directive.parse_line(line, self)
        self.take_directive(directive)


class DuckParser:
    STATE_START = 1
    STATE_TOP = 2
    STATE_HEADER = 3
    STATE_HEADER_POST = 4
    STATE_SUBHEADER = 5
    STATE_SUBHEADER_POST = 6
    STATE_HEADER_ATTR = 7
    STATE_HEADER_ATTR_POST = 8
    STATE_HEADER_INFO = 9
    STATE_BLOCK = 10
    STATE_BLOCK_ATTR = 11
    STATE_BLOCK_READY = 12
    STATE_BLOCK_INFO = 13
    INFO_STATE_NONE = 101
    INFO_STATE_INFO = 102
    INFO_STATE_READY = 103
    INFO_STATE_BLOCK = 104
    INFO_STATE_ATTR = 105

    def __init__(self):
        self.state = DuckParser.STATE_START
        self.info_state = DuckParser.INFO_STATE_NONE
        self.linenum = 0
        self.document = Document(parser=self)
        self.current = self.document
        self.curinfo = None
        self.extensions = []
        self.extensions_by_module = {}
        self.factory = NodeFactory(self)
        self._text = ''
        self._attrparser = None
        self._defaultid = None
        self._comment = False
        self._fenced = False
        self._fragments = False

    @staticmethod
    def get_indent(line):
        for i in range(len(line)):
            if line[i] != ' ':
                return i

        return 0

    def lookup_entity(self, entity):
        cur = self.current
        while cur is not None:
            if entity in cur._definitions:
                return cur._definitions[entity]
            cur = cur.parent

        if entity in entities.entities:
            return entities.entities[entity]
        hexnum = 0
        for c in entity:
            if c in '0123456789':
                hexnum = hexnum * 16 + (ord(c) - 48)
            elif c in 'abcdef':
                hexnum = hexnum * 16 + (ord(c) - 87)
            elif c in 'ABCDEF':
                hexnum = hexnum * 16 + (ord(c) - 55)
            else:
                hexnum = None
                break

        if hexnum is not None:
            return chr(hexnum)

    def parse_file(self, filename):
        self.filename = filename
        self.absfilename = os.path.abspath(filename)
        self._defaultid = os.path.basename(filename)
        if self._defaultid.endswith('.duck'):
            self._defaultid = self._defaultid[:-5]
        fd = open(filename, encoding='utf-8')
        for line in fd:
            self.parse_line(line)

        fd.close()

    def parse_inline(self, node=None):
        if node is None:
            node = self.document
        oldchildren = node.children
        node.children = []
        if node.info is not None:
            self.parse_inline(node.info)
        for child in oldchildren:
            if isinstance(child, str):
                parser = InlineParser(self, linenum=(node.linenum))
                for c in parser.parse_text(child):
                    node.add_child(c)

            elif isinstance(child, Fence):
                node.add_child(child)
            else:
                self.parse_inline(child)
                node.add_child(child)

    def take_directive(self, directive):
        if directive.name.startswith('ducktype/'):
            if self.state != DuckParser.STATE_START:
                raise SyntaxError('Ducktype declaration must be first', self)
            if directive.name != 'ducktype/1.0':
                raise SyntaxError('Unsupported ducktype version: ' + directive.name, self)
            for value in directive.content.split():
                if value == '__future__/fragments':
                    self._fragments = True
                    continue
                try:
                    prefix, version = value.split('/', maxsplit=1)
                    extmod = importlib.import_module('mallard.ducktype.extensions.' + prefix)
                    for extclsname, extcls in inspect.getmembers(extmod, inspect.isclass):
                        if issubclass(extcls, ParserExtension):
                            extension = extcls(self, prefix, version)
                            self.extensions.append(extension)
                            self.extensions_by_module.setdefault(prefix, [])
                            self.extensions_by_module[prefix].append(extension)

                except SyntaxError as e:
                    try:
                        raise e
                    finally:
                        e = None
                        del e

                except:
                    raise SyntaxError('Unsupported ducktype extension: ' + value, self)

        else:
            if ':' in directive.name:
                prefix, name = directive.name.split(':', maxsplit=1)
                if prefix not in self.extensions_by_module:
                    raise SyntaxError('Unrecognized directive prefix: ' + prefix, self)
                for extension in self.extensions_by_module[prefix]:
                    if extension.take_directive(directive):
                        return

                raise SyntaxError('Unrecognized directive: ' + directive.name, self)
            else:
                if directive.name == 'define':
                    values = directive.content.split(maxsplit=1)
                    if len(values) != 2:
                        raise SyntaxError('Entity definition takes exactly two values', self)
                    (self.current.add_definition)(*values)
                else:
                    if directive.name == 'encoding':
                        FIXME('encoding')
                    else:
                        if directive.name == 'include':
                            if ' ' in directive.content:
                                raise SyntaxError('Multiple values in include. URL encode file name?', self)
                            relfile = urllib.parse.unquote(directive.content)
                            incparser = DirectiveIncludeParser(self)
                            incparser.parse_file(relfile)
                        else:
                            if directive.name == 'namespace':
                                values = directive.content.split(maxsplit=1)
                                if len(values) != 2:
                                    raise SyntaxError('Namespace declaration takes exactly two values', self)
                                if values[0] == 'xml':
                                    if values[1] != 'http://www.w3.org/XML/1998/namespace':
                                        raise SyntaxError('Wrong value of xml namespace prefix', self)
                                if values[0] == 'its':
                                    if values[1] != 'http://www.w3.org/2005/11/its':
                                        raise SyntaxError('Wrong value of its namespace prefix', self)
                                (self.current.add_namespace)(*values)
                            else:
                                raise SyntaxError('Unrecognized directive: ' + directive.name, self)

    def finish(self):
        if self.state in (DuckParser.STATE_HEADER_ATTR, DuckParser.STATE_BLOCK_ATTR) or self.info_state == DuckParser.INFO_STATE_ATTR:
            raise SyntaxError('Unterminated block declaration', self)
        self.push_text()
        if self._defaultid is not None:
            if len(self.document.children) == 1:
                root = self.document.children[0]
                if isinstance(root, Division):
                    if root.attributes is None:
                        root.attributes = Attributes()
                    idattr = self.factory.id_attribute
                    if idattr not in root.attributes:
                        root.attributes.add_attribute(idattr, self._defaultid)
        self.parse_inline()

    def parse_line(self, line):
        self.linenum += 1
        self._parse_line(line)

    def _parse_line(self, line):
        if self._comment:
            if line.strip() == '--]':
                self._comment = False
        else:
            return
            if self._fenced:
                if line.strip() == ']]]':
                    self._fenced = False
                    self.current = self.current.parent
                else:
                    self.current.add_line(line)
                return
                indent = DuckParser.get_indent(line)
                iline = line[indent:]
                if iline.startswith('[-]'):
                    return
                if iline.startswith('[--'):
                    self._comment = True
                    return
                if self.info_state == DuckParser.INFO_STATE_INFO:
                    self._parse_line_info(line)
            elif self.info_state == DuckParser.INFO_STATE_READY:
                self._parse_line_info(line)
            else:
                if self.info_state == DuckParser.INFO_STATE_BLOCK:
                    self._parse_line_info(line)
                else:
                    if self.info_state == DuckParser.INFO_STATE_ATTR:
                        self._parse_line_info_attr(line)
                    else:
                        if self.state == DuckParser.STATE_START:
                            self._parse_line_top(line)
                        else:
                            if self.state == DuckParser.STATE_TOP:
                                self._parse_line_top(line)
                            else:
                                if self.state == DuckParser.STATE_HEADER:
                                    self._parse_line_header(line)
                                else:
                                    if self.state == DuckParser.STATE_HEADER_POST:
                                        self._parse_line_header_post(line)
                                    else:
                                        if self.state == DuckParser.STATE_SUBHEADER:
                                            self._parse_line_subheader(line)
                                        else:
                                            if self.state == DuckParser.STATE_SUBHEADER_POST:
                                                self._parse_line_subheader_post(line)
                                            else:
                                                if self.state == DuckParser.STATE_HEADER_ATTR:
                                                    self._parse_line_header_attr(line)
                                                else:
                                                    if self.state == DuckParser.STATE_HEADER_ATTR_POST:
                                                        self._parse_line_header_attr_post(line)
                                                    else:
                                                        if self.state == DuckParser.STATE_HEADER_INFO:
                                                            self._parse_line_header_info(line)
                                                        else:
                                                            if self.state == DuckParser.STATE_BLOCK:
                                                                self._parse_line_block(line)
                                                            else:
                                                                if self.state == DuckParser.STATE_BLOCK_ATTR:
                                                                    self._parse_line_block_attr(line)
                                                                else:
                                                                    if self.state == DuckParser.STATE_BLOCK_READY:
                                                                        self._parse_line_block_ready(line)
                                                                    else:
                                                                        FIXME('unknown state')

    def _parse_line_top(self, line):
        if line.strip() == '':
            self.state = DuckParser.STATE_TOP
        else:
            if line.startswith('@'):
                self._parse_line_directive(line)
            else:
                if line.startswith('= '):
                    self.factory.handle_division_title(depth=1, inner=2)
                    self.set_text(line[2:])
                    self.state = DuckParser.STATE_HEADER
                else:
                    if line.strip().startswith('[') or line.startswith('=='):
                        if self._fragments == False:
                            raise SyntaxError('Missing page header', self)
                        self.state = DuckParser.STATE_BLOCK
                        self._parse_line(line)
                    else:
                        raise SyntaxError('Missing page header', self)

    def _parse_line_directive(self, line):
        directive = Directive.parse_line(line, self)
        self.take_directive(directive)
        if self.state == DuckParser.STATE_START:
            self.state == DuckParser.STATE_TOP

    def _parse_line_header(self, line):
        indent = DuckParser.get_indent(line)
        iline = line[indent:]
        if iline.startswith('@'):
            self.push_text()
            self.current = self.current.parent
            self.state = DuckParser.STATE_BLOCK
            self.info_state = DuckParser.INFO_STATE_INFO
            self._parse_line(line)
        else:
            if indent > 0 and iline.startswith('['):
                self._parse_line_header_attr_start(line)
            else:
                if indent >= self.current.inner:
                    self.add_text(line[self.current.inner:])
                else:
                    self.push_text()
                    self.current = self.current.parent
                    self.state = DuckParser.STATE_HEADER_POST
                    self._parse_line(line)

    def _parse_line_header_post(self, line):
        depth = self.current.divdepth
        if line.startswith('-' * depth + ' '):
            self.factory.handle_division_subtitle(depth=depth, inner=(depth + 1))
            self.set_text(line[depth + 1:])
            self.state = DuckParser.STATE_SUBHEADER
        else:
            if line.lstrip().startswith('@'):
                self.state = DuckParser.STATE_BLOCK
                self.info_state = DuckParser.INFO_STATE_INFO
                self._parse_line(line)
            else:
                if line.strip() == '':
                    self.state = DuckParser.STATE_HEADER_INFO
                else:
                    self.state = DuckParser.STATE_BLOCK
                    self._parse_line(line)

    def _parse_line_subheader(self, line):
        indent = DuckParser.get_indent(line)
        iline = line[indent:]
        if iline.startswith('@'):
            self.push_text()
            self.current = self.current.parent
            self.state = DuckParser.STATE_BLOCK
            self.info_state = DuckParser.INFO_STATE_INFO
            self._parse_line(line)
        else:
            if indent > 0 and iline.startswith('['):
                self._parse_line_header_attr_start(line)
            else:
                if indent >= self.current.inner:
                    self.add_text(line[self.current.inner:])
                else:
                    self.push_text()
                    self.current = self.current.parent
                    self.state = DuckParser.STATE_SUBHEADER_POST
                    self._parse_line(line)

    def _parse_line_subheader_post(self, line):
        if line.lstrip().startswith('@'):
            self.state = DuckParser.STATE_BLOCK
            self.info_state = DuckParser.INFO_STATE_INFO
            self._parse_line(line)
        else:
            if line.strip() == '':
                self.state = DuckParser.STATE_HEADER_INFO
            else:
                self.state = DuckParser.STATE_BLOCK
                self._parse_line(line)

    def _parse_line_header_attr_start(self, line):
        indent = DuckParser.get_indent(line)
        if indent > 0:
            if line[indent:].startswith('['):
                self.push_text()
                self.current = self.current.parent
                self._attrparser = AttributeParser(self)
                self._attrparser.parse_line(line[indent + 1:])
                if self._attrparser.finished:
                    self.current.attributes = self._attrparser.attributes
                    self.state = DuckParser.STATE_HEADER_ATTR_POST
                    self._attrparser = None
            else:
                self.state = DuckParser.STATE_HEADER_ATTR
        else:
            self.push_text()
            self.current = self.current.parent
            self.state = DuckParser.STATE_HEADER_ATTR_POST
            self._parse_line(line)

    def _parse_line_header_attr(self, line):
        self._attrparser.parse_line(line)
        if self._attrparser.finished:
            self.current.attributes = self._attrparser.attributes
            self.state = DuckParser.STATE_HEADER_ATTR_POST
            self._attrparser = None

    def _parse_line_header_attr_post(self, line):
        if line.lstrip().startswith('@'):
            self.state = DuckParser.STATE_BLOCK
            self.info_state = DuckParser.INFO_STATE_INFO
            self._parse_line(line)
        else:
            if line.strip() == '':
                self.state = DuckParser.STATE_HEADER_INFO
            else:
                self.state = DuckParser.STATE_BLOCK
                self._parse_line(line)

    def _parse_line_header_info(self, line):
        if line.lstrip().startswith('@'):
            self.state = DuckParser.STATE_BLOCK
            self.info_state = DuckParser.INFO_STATE_INFO
            self._parse_line(line)
        else:
            if line.strip() == '':
                self.state = DuckParser.STATE_HEADER_INFO
            else:
                self.state = DuckParser.STATE_BLOCK
                self._parse_line(line)

    def _parse_line_info(self, line):
        if line.strip() == '':
            if self.current.outer == self.current.inner:
                if not isinstance(self.current, Division):
                    self.push_text()
                    self.info_state = DuckParser.INFO_STATE_NONE
                    self._parse_line(line)
                    return
            elif self.curinfo.is_leaf:
                if self.curinfo.is_verbatim and self.curinfo.inner > self.curinfo.outer:
                    self.add_text('\n')
                else:
                    self.push_text()
                    self.curinfo = self.curinfo.parent
                    self.info_state = DuckParser.INFO_STATE_INFO
            return
            indent = DuckParser.get_indent(line)
            if self.current.info is None:
                self.factory.handle_info_container(indent)
                self.curinfo = self.current.info
            if indent < self.current.info.outer:
                self.push_text()
                self.info_state = DuckParser.INFO_STATE_NONE
                self._parse_line(line)
                return
            iline = line[indent:]
            if iline.startswith('@'):
                self._parse_line_info_info(iline, indent)
        else:
            if indent <= self.current.info.outer:
                self.push_text()
                self.info_state = DuckParser.INFO_STATE_NONE
                self._parse_line(line)
                return
            self._parse_line_info_block(iline, indent)

    def _parse_line_info_info(self, iline, indent):
        if indent <= self.curinfo.outer:
            self.push_text()
            while indent <= self.curinfo.outer:
                if self.curinfo == self.current.info:
                    break
                self.curinfo = self.curinfo.parent

        elif self.info_state == DuckParser.INFO_STATE_READY:
            self.curinfo.inner = indent
        else:
            self.info_state = DuckParser.INFO_STATE_INFO
            for j in range(1, len(iline)):
                if not _isnmtoken(iline[j]):
                    break

            name = iline[1:j]
            node = self.factory.create_info_node(name, indent)
            self.curinfo.add_child(node)
            self.curinfo = node
            if iline[j] == '[':
                self.info_state = DuckParser.INFO_STATE_ATTR
                self._attrparser = AttributeParser(self)
                self._parse_line_info_attr(iline[j + 1:])
            else:
                remainder = iline[j:].lstrip()
                if remainder != '':
                    if not self.curinfo.is_leaf:
                        pnode = self.factory.create_info_paragraph_node(self.curinfo.outer)
                        self.curinfo.add_child(pnode)
                        self.curinfo = pnode
                    self.set_text(remainder)
                else:
                    self.info_state = DuckParser.INFO_STATE_READY

    def _parse_line_info_block(self, iline, indent):
        if self.curinfo.is_leaf or self.curinfo.is_external:
            if indent < self.curinfo.inner:
                self.push_text()
                self.curinfo = self.curinfo.parent
        elif indent <= self.curinfo.outer:
            self.push_text()
            while indent <= self.curinfo.outer:
                if self.curinfo == self.current.info:
                    break
                self.curinfo = self.curinfo.parent

        if iline.strip() != '':
            if not self.curinfo.is_leaf:
                if not self.curinfo.is_external:
                    node = self.factory.create_info_paragraph_node(indent)
                    self.curinfo.add_child(node)
                    self.curinfo = node
        if self.info_state == DuckParser.INFO_STATE_READY:
            self.curinfo.inner = indent
            self.info_state = DuckParser.INFO_STATE_BLOCK
        self.info_state = DuckParser.INFO_STATE_BLOCK
        self.add_text(iline)

    def _parse_line_info_attr(self, line):
        self._attrparser.parse_line(line)
        if self._attrparser.finished:
            self.curinfo.attributes = self._attrparser.attributes
            remainder = self._attrparser.remainder.lstrip()
            if remainder != '':
                if not self.curinfo.is_leaf:
                    pnode = self.factory.create_info_paragraph_node(self.curinfo.outer)
                    self.curinfo.add_child(pnode)
                    self.curinfo = pnode
                self.set_text(remainder)
            else:
                self._attrparser = None
                if self._text == '':
                    self.info_state = DuckParser.INFO_STATE_READY
                else:
                    self.info_state = DuckParser.INFO_STATE_INFO

    def _parse_line_block--- This code section failed: ---

 L.1461         0  LOAD_FAST                'line'
                2  LOAD_METHOD              strip
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  LOAD_STR                 ''
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE   154  'to 154'

 L.1462        12  LOAD_FAST                'self'
               14  LOAD_ATTR                current
               16  LOAD_ATTR                is_leaf
               18  POP_JUMP_IF_FALSE    74  'to 74'

 L.1463        20  LOAD_FAST                'self'
               22  LOAD_ATTR                current
               24  LOAD_ATTR                is_verbatim
               26  POP_JUMP_IF_FALSE    56  'to 56'

 L.1464        28  LOAD_FAST                'self'
               30  LOAD_ATTR                current
               32  LOAD_ATTR                inner
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                current
               38  LOAD_ATTR                outer
               40  COMPARE_OP               >
               42  POP_JUMP_IF_FALSE    56  'to 56'

 L.1465        44  LOAD_FAST                'self'
               46  LOAD_METHOD              add_text
               48  LOAD_STR                 '\n'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  POP_TOP          
               54  JUMP_FORWARD         74  'to 74'
             56_0  COME_FROM            42  '42'
             56_1  COME_FROM            26  '26'

 L.1467        56  LOAD_FAST                'self'
               58  LOAD_METHOD              push_text
               60  CALL_METHOD_0         0  '0 positional arguments'
               62  POP_TOP          

 L.1468        64  LOAD_FAST                'self'
               66  LOAD_ATTR                current
               68  LOAD_ATTR                parent
               70  LOAD_FAST                'self'
               72  STORE_ATTR               current
             74_0  COME_FROM            54  '54'
             74_1  COME_FROM            18  '18'

 L.1469        74  SETUP_LOOP          150  'to 150'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                current
               80  LOAD_ATTR                inner
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                current
               86  LOAD_ATTR                outer
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   148  'to 148'

 L.1470        92  LOAD_GLOBAL              isinstance
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                current
               98  LOAD_GLOBAL              Division
              100  LOAD_GLOBAL              Document
              102  BUILD_TUPLE_2         2 
              104  CALL_FUNCTION_2       2  '2 positional arguments'
              106  POP_JUMP_IF_FALSE   110  'to 110'

 L.1471       108  BREAK_LOOP       
            110_0  COME_FROM           106  '106'

 L.1472       110  LOAD_FAST                'self'
              112  LOAD_ATTR                current
              114  LOAD_ATTR                is_greedy
              116  POP_JUMP_IF_FALSE   120  'to 120'

 L.1473       118  BREAK_LOOP       
            120_0  COME_FROM           116  '116'

 L.1474       120  LOAD_FAST                'self'
              122  LOAD_ATTR                current
              124  LOAD_ATTR                is_leaf
              126  POP_JUMP_IF_FALSE   136  'to 136'

 L.1475       128  LOAD_FAST                'self'
              130  LOAD_METHOD              push_text
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  POP_TOP          
            136_0  COME_FROM           126  '126'

 L.1476       136  LOAD_FAST                'self'
              138  LOAD_ATTR                current
              140  LOAD_ATTR                parent
              142  LOAD_FAST                'self'
              144  STORE_ATTR               current
              146  JUMP_BACK            76  'to 76'
            148_0  COME_FROM            90  '90'
              148  POP_BLOCK        
            150_0  COME_FROM_LOOP       74  '74'

 L.1477       150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM            10  '10'

 L.1479       154  LOAD_CONST               0
              156  STORE_FAST               'sectd'

 L.1480       158  LOAD_FAST                'line'
              160  LOAD_METHOD              startswith
              162  LOAD_STR                 '=='
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_JUMP_IF_FALSE   238  'to 238'

 L.1481       168  LOAD_CONST               0
              170  STORE_FAST               'i'

 L.1482       172  SETUP_LOOP          210  'to 210'
              174  LOAD_FAST                'i'
              176  LOAD_GLOBAL              len
              178  LOAD_FAST                'line'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  COMPARE_OP               <
              184  POP_JUMP_IF_FALSE   208  'to 208'
              186  LOAD_FAST                'line'
              188  LOAD_FAST                'i'
              190  BINARY_SUBSCR    
              192  LOAD_STR                 '='
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   208  'to 208'

 L.1483       198  LOAD_FAST                'i'
              200  LOAD_CONST               1
              202  INPLACE_ADD      
              204  STORE_FAST               'i'
              206  JUMP_BACK           174  'to 174'
            208_0  COME_FROM           196  '196'
            208_1  COME_FROM           184  '184'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP      172  '172'

 L.1484       210  LOAD_FAST                'i'
              212  LOAD_GLOBAL              len
              214  LOAD_FAST                'line'
              216  CALL_FUNCTION_1       1  '1 positional argument'
              218  COMPARE_OP               <
              220  POP_JUMP_IF_FALSE   238  'to 238'
              222  LOAD_FAST                'line'
              224  LOAD_FAST                'i'
              226  BINARY_SUBSCR    
              228  LOAD_STR                 ' '
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   238  'to 238'

 L.1485       234  LOAD_FAST                'i'
              236  STORE_FAST               'sectd'
            238_0  COME_FROM           232  '232'
            238_1  COME_FROM           220  '220'
            238_2  COME_FROM           166  '166'

 L.1486       238  LOAD_FAST                'sectd'
              240  LOAD_CONST               0
              242  COMPARE_OP               >
          244_246  POP_JUMP_IF_FALSE   468  'to 468'

 L.1487       248  LOAD_FAST                'self'
              250  LOAD_METHOD              push_text
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  POP_TOP          

 L.1488       256  SETUP_LOOP          292  'to 292'
              258  LOAD_GLOBAL              isinstance
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                current
              264  LOAD_GLOBAL              Division
              266  LOAD_GLOBAL              Document
              268  BUILD_TUPLE_2         2 
              270  CALL_FUNCTION_2       2  '2 positional arguments'
          272_274  POP_JUMP_IF_TRUE    290  'to 290'

 L.1489       276  LOAD_FAST                'self'
              278  LOAD_ATTR                current
              280  LOAD_ATTR                parent
              282  LOAD_FAST                'self'
              284  STORE_ATTR               current
          286_288  JUMP_BACK           258  'to 258'
            290_0  COME_FROM           272  '272'
              290  POP_BLOCK        
            292_0  COME_FROM_LOOP      256  '256'

 L.1490       292  SETUP_LOOP          324  'to 324'
              294  LOAD_FAST                'self'
              296  LOAD_ATTR                current
              298  LOAD_ATTR                divdepth
              300  LOAD_FAST                'sectd'
              302  COMPARE_OP               >=
          304_306  POP_JUMP_IF_FALSE   322  'to 322'

 L.1491       308  LOAD_FAST                'self'
              310  LOAD_ATTR                current
              312  LOAD_ATTR                parent
              314  LOAD_FAST                'self'
              316  STORE_ATTR               current
          318_320  JUMP_BACK           294  'to 294'
            322_0  COME_FROM           304  '304'
              322  POP_BLOCK        
            324_0  COME_FROM_LOOP      292  '292'

 L.1492       324  LOAD_FAST                'sectd'
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                current
              330  LOAD_ATTR                divdepth
              332  LOAD_CONST               1
              334  BINARY_ADD       
              336  COMPARE_OP               !=
          338_340  POP_JUMP_IF_FALSE   414  'to 414'

 L.1493       342  LOAD_GLOBAL              isinstance
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                current
              348  LOAD_GLOBAL              Document
              350  CALL_FUNCTION_2       2  '2 positional arguments'
          352_354  POP_JUMP_IF_FALSE   404  'to 404'

 L.1494       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _fragments
          360_362  POP_JUMP_IF_FALSE   404  'to 404'

 L.1495       364  LOAD_GLOBAL              len
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                current
              370  LOAD_ATTR                children
              372  CALL_FUNCTION_1       1  '1 positional argument'
              374  LOAD_CONST               0
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_TRUE    414  'to 414'

 L.1496       382  LOAD_FAST                'sectd'
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                current
              388  LOAD_ATTR                children
              390  LOAD_CONST               0
              392  BINARY_SUBSCR    
              394  LOAD_ATTR                divdepth
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   404  'to 404'

 L.1497       402  JUMP_FORWARD        414  'to 414'
            404_0  COME_FROM           398  '398'
            404_1  COME_FROM           360  '360'
            404_2  COME_FROM           352  '352'

 L.1499       404  LOAD_GLOBAL              SyntaxError
              406  LOAD_STR                 'Incorrect section depth'
              408  LOAD_FAST                'self'
              410  CALL_FUNCTION_2       2  '2 positional arguments'
              412  RAISE_VARARGS_1       1  'exception instance'
            414_0  COME_FROM           402  '402'
            414_1  COME_FROM           378  '378'
            414_2  COME_FROM           338  '338'

 L.1500       414  LOAD_FAST                'self'
              416  LOAD_ATTR                factory
              418  LOAD_ATTR                handle_division_title
              420  LOAD_FAST                'sectd'
              422  LOAD_FAST                'sectd'
              424  LOAD_CONST               1
              426  BINARY_ADD       
              428  LOAD_CONST               ('depth', 'inner')
              430  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              432  POP_TOP          

 L.1501       434  LOAD_FAST                'self'
              436  LOAD_METHOD              set_text
              438  LOAD_FAST                'line'
              440  LOAD_FAST                'sectd'
              442  LOAD_CONST               1
              444  BINARY_ADD       
              446  LOAD_CONST               None
              448  BUILD_SLICE_2         2 
              450  BINARY_SUBSCR    
              452  CALL_METHOD_1         1  '1 positional argument'
              454  POP_TOP          

 L.1502       456  LOAD_GLOBAL              DuckParser
              458  LOAD_ATTR                STATE_HEADER
              460  LOAD_FAST                'self'
              462  STORE_ATTR               state

 L.1503       464  LOAD_CONST               None
              466  RETURN_VALUE     
            468_0  COME_FROM           244  '244'

 L.1512       468  LOAD_GLOBAL              DuckParser
              470  LOAD_METHOD              get_indent
              472  LOAD_FAST                'line'
              474  CALL_METHOD_1         1  '1 positional argument'
              476  STORE_FAST               'indent'

 L.1513       478  LOAD_FAST                'indent'
              480  LOAD_FAST                'self'
              482  LOAD_ATTR                current
              484  LOAD_ATTR                inner
              486  COMPARE_OP               <
          488_490  POP_JUMP_IF_FALSE   552  'to 552'

 L.1514       492  LOAD_FAST                'self'
              494  LOAD_METHOD              push_text
              496  CALL_METHOD_0         0  '0 positional arguments'
              498  POP_TOP          

 L.1515       500  SETUP_LOOP          552  'to 552'
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                current
              506  LOAD_ATTR                inner
              508  LOAD_FAST                'indent'
              510  COMPARE_OP               >
          512_514  POP_JUMP_IF_FALSE   550  'to 550'

 L.1516       516  LOAD_GLOBAL              isinstance
              518  LOAD_FAST                'self'
              520  LOAD_ATTR                current
              522  LOAD_GLOBAL              Division
              524  LOAD_GLOBAL              Document
              526  BUILD_TUPLE_2         2 
              528  CALL_FUNCTION_2       2  '2 positional arguments'
          530_532  POP_JUMP_IF_FALSE   536  'to 536'

 L.1517       534  BREAK_LOOP       
            536_0  COME_FROM           530  '530'

 L.1518       536  LOAD_FAST                'self'
              538  LOAD_ATTR                current
              540  LOAD_ATTR                parent
              542  LOAD_FAST                'self'
              544  STORE_ATTR               current
          546_548  JUMP_BACK           502  'to 502'
            550_0  COME_FROM           512  '512'
              550  POP_BLOCK        
            552_0  COME_FROM_LOOP      500  '500'
            552_1  COME_FROM           488  '488'

 L.1520       552  LOAD_FAST                'self'
              554  LOAD_ATTR                current
              556  LOAD_ATTR                is_verbatim
          558_560  POP_JUMP_IF_FALSE   580  'to 580'

 L.1521       562  LOAD_FAST                'line'
              564  LOAD_FAST                'self'
              566  LOAD_ATTR                current
              568  LOAD_ATTR                inner
              570  LOAD_CONST               None
              572  BUILD_SLICE_2         2 
              574  BINARY_SUBSCR    
              576  STORE_FAST               'iline'
              578  JUMP_FORWARD        592  'to 592'
            580_0  COME_FROM           558  '558'

 L.1523       580  LOAD_FAST                'line'
              582  LOAD_FAST                'indent'
              584  LOAD_CONST               None
              586  BUILD_SLICE_2         2 
              588  BINARY_SUBSCR    
              590  STORE_FAST               'iline'
            592_0  COME_FROM           578  '578'

 L.1530       592  LOAD_FAST                'iline'
              594  LOAD_METHOD              startswith
              596  LOAD_STR                 '[[['
              598  CALL_METHOD_1         1  '1 positional argument'
          600_602  POP_JUMP_IF_FALSE   926  'to 926'

 L.1531       604  LOAD_FAST                'self'
              606  LOAD_METHOD              push_text
              608  CALL_METHOD_0         0  '0 positional arguments'
              610  POP_TOP          

 L.1532       612  LOAD_GLOBAL              Fence
              614  LOAD_STR                 '_'
              616  LOAD_FAST                'indent'
              618  LOAD_FAST                'self'
              620  LOAD_CONST               ('parser',)
              622  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              624  STORE_FAST               'node'

 L.1534       626  LOAD_FAST                'self'
              628  LOAD_ATTR                current
              630  LOAD_ATTR                is_leaf
          632_634  POP_JUMP_IF_TRUE    806  'to 806'
              636  LOAD_FAST                'self'
              638  LOAD_ATTR                current
              640  LOAD_ATTR                is_external
          642_644  POP_JUMP_IF_TRUE    806  'to 806'

 L.1535       646  LOAD_FAST                'self'
              648  LOAD_ATTR                current
              650  LOAD_ATTR                is_tree_item
          652_654  POP_JUMP_IF_FALSE   666  'to 666'
              656  LOAD_FAST                'self'
              658  LOAD_ATTR                current
              660  LOAD_ATTR                has_tree_items
          662_664  POP_JUMP_IF_FALSE   806  'to 806'
            666_0  COME_FROM           652  '652'

 L.1536       666  LOAD_FAST                'self'
              668  LOAD_ATTR                current
              670  LOAD_ATTR                is_tree_item
          672_674  POP_JUMP_IF_FALSE   708  'to 708'

 L.1537       676  SETUP_LOOP          708  'to 708'
              678  LOAD_FAST                'self'
              680  LOAD_ATTR                current
              682  LOAD_METHOD              is_name
              684  LOAD_CONST               ('tree', 'item')
              686  CALL_METHOD_1         1  '1 positional argument'
          688_690  POP_JUMP_IF_FALSE   706  'to 706'

 L.1538       692  LOAD_FAST                'self'
              694  LOAD_ATTR                current
              696  LOAD_ATTR                parent
              698  LOAD_FAST                'self'
              700  STORE_ATTR               current
          702_704  JUMP_BACK           678  'to 678'
            706_0  COME_FROM           688  '688'
              706  POP_BLOCK        
            708_0  COME_FROM_LOOP      676  '676'
            708_1  COME_FROM           672  '672'

 L.1539       708  SETUP_LOOP          770  'to 770'
              710  LOAD_FAST                'self'
              712  LOAD_ATTR                current
              714  LOAD_ATTR                outer
              716  LOAD_FAST                'indent'
              718  COMPARE_OP               ==
          720_722  POP_JUMP_IF_FALSE   768  'to 768'
              724  LOAD_FAST                'self'
              726  LOAD_ATTR                current
              728  LOAD_ATTR                available
          730_732  POP_JUMP_IF_TRUE    768  'to 768'

 L.1540       734  LOAD_GLOBAL              isinstance
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                current
              740  LOAD_GLOBAL              Division
              742  LOAD_GLOBAL              Document
              744  BUILD_TUPLE_2         2 
              746  CALL_FUNCTION_2       2  '2 positional arguments'
          748_750  POP_JUMP_IF_FALSE   754  'to 754'

 L.1541       752  BREAK_LOOP       
            754_0  COME_FROM           748  '748'

 L.1542       754  LOAD_FAST                'self'
              756  LOAD_ATTR                current
              758  LOAD_ATTR                parent
              760  LOAD_FAST                'self'
              762  STORE_ATTR               current
          764_766  JUMP_BACK           710  'to 710'
            768_0  COME_FROM           730  '730'
            768_1  COME_FROM           720  '720'
              768  POP_BLOCK        
            770_0  COME_FROM_LOOP      708  '708'

 L.1543       770  LOAD_FAST                'self'
              772  LOAD_ATTR                factory
              774  LOAD_METHOD              create_block_paragraph_node
              776  LOAD_FAST                'indent'
              778  CALL_METHOD_1         1  '1 positional argument'
              780  STORE_FAST               'pnode'

 L.1544       782  LOAD_FAST                'self'
              784  LOAD_ATTR                current
              786  LOAD_METHOD              add_child
              788  LOAD_FAST                'pnode'
              790  CALL_METHOD_1         1  '1 positional argument'
              792  POP_TOP          

 L.1545       794  LOAD_FAST                'pnode'
              796  LOAD_METHOD              add_child
              798  LOAD_FAST                'node'
              800  CALL_METHOD_1         1  '1 positional argument'
              802  POP_TOP          
              804  JUMP_FORWARD        818  'to 818'
            806_0  COME_FROM           662  '662'
            806_1  COME_FROM           642  '642'
            806_2  COME_FROM           632  '632'

 L.1547       806  LOAD_FAST                'self'
              808  LOAD_ATTR                current
              810  LOAD_METHOD              add_child
              812  LOAD_FAST                'node'
              814  CALL_METHOD_1         1  '1 positional argument'
              816  POP_TOP          
            818_0  COME_FROM           804  '804'

 L.1549       818  LOAD_FAST                'iline'
              820  LOAD_METHOD              strip
              822  CALL_METHOD_0         0  '0 positional arguments'
              824  LOAD_CONST               3
              826  LOAD_CONST               None
              828  BUILD_SLICE_2         2 
              830  BINARY_SUBSCR    
              832  STORE_FAST               'sline'

 L.1550       834  LOAD_FAST                'sline'
              836  LOAD_METHOD              endswith
              838  LOAD_STR                 ']]]'
              840  CALL_METHOD_1         1  '1 positional argument'
          842_844  POP_JUMP_IF_FALSE   876  'to 876'

 L.1551       846  LOAD_CONST               0
              848  LOAD_FAST                'node'
              850  STORE_ATTR               inner

 L.1552       852  LOAD_FAST                'node'
              854  LOAD_METHOD              add_line
              856  LOAD_FAST                'sline'
              858  LOAD_CONST               None
              860  LOAD_CONST               -3
              862  BUILD_SLICE_2         2 
              864  BINARY_SUBSCR    
              866  LOAD_STR                 '\n'
              868  BINARY_ADD       
              870  CALL_METHOD_1         1  '1 positional argument'
              872  POP_TOP          
              874  JUMP_FORWARD        922  'to 922'
            876_0  COME_FROM           842  '842'

 L.1554       876  LOAD_FAST                'sline'
              878  LOAD_METHOD              strip
              880  CALL_METHOD_0         0  '0 positional arguments'
              882  LOAD_STR                 ''
              884  COMPARE_OP               !=
          886_888  POP_JUMP_IF_FALSE   910  'to 910'

 L.1555       890  LOAD_CONST               0
              892  LOAD_FAST                'node'
              894  STORE_ATTR               inner

 L.1556       896  LOAD_FAST                'node'
              898  LOAD_METHOD              add_line
              900  LOAD_FAST                'sline'
              902  LOAD_STR                 '\n'
              904  BINARY_ADD       
              906  CALL_METHOD_1         1  '1 positional argument'
              908  POP_TOP          
            910_0  COME_FROM           886  '886'

 L.1557       910  LOAD_FAST                'node'
              912  LOAD_FAST                'self'
              914  STORE_ATTR               current

 L.1558       916  LOAD_CONST               True
              918  LOAD_FAST                'self'
              920  STORE_ATTR               _fenced
            922_0  COME_FROM           874  '874'

 L.1559       922  LOAD_CONST               None
              924  RETURN_VALUE     
            926_0  COME_FROM           600  '600'

 L.1563       926  SETUP_LOOP          960  'to 960'
              928  LOAD_FAST                'self'
              930  LOAD_ATTR                extensions
              932  GET_ITER         
            934_0  COME_FROM           946  '946'
              934  FOR_ITER            958  'to 958'
              936  STORE_FAST               'extension'

 L.1564       938  LOAD_FAST                'extension'
              940  LOAD_METHOD              parse_line_block
              942  LOAD_FAST                'line'
              944  CALL_METHOD_1         1  '1 positional argument'
          946_948  POP_JUMP_IF_FALSE   934  'to 934'

 L.1565       950  LOAD_CONST               None
              952  RETURN_VALUE     
          954_956  JUMP_BACK           934  'to 934'
              958  POP_BLOCK        
            960_0  COME_FROM_LOOP      926  '926'

 L.1567       960  LOAD_FAST                'iline'
              962  LOAD_METHOD              startswith
              964  LOAD_STR                 '['
              966  CALL_METHOD_1         1  '1 positional argument'
          968_970  POP_JUMP_IF_FALSE  1280  'to 1280'

 L.1569       972  LOAD_FAST                'self'
              974  LOAD_METHOD              push_text
              976  CALL_METHOD_0         0  '0 positional arguments'
              978  POP_TOP          

 L.1571       980  SETUP_LOOP         1022  'to 1022'
              982  LOAD_GLOBAL              range
              984  LOAD_CONST               1
              986  LOAD_GLOBAL              len
              988  LOAD_FAST                'iline'
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  CALL_FUNCTION_2       2  '2 positional arguments'
              994  GET_ITER         
            996_0  COME_FROM          1010  '1010'
              996  FOR_ITER           1020  'to 1020'
              998  STORE_FAST               'j'

 L.1572      1000  LOAD_GLOBAL              _isnmtoken
             1002  LOAD_FAST                'iline'
             1004  LOAD_FAST                'j'
             1006  BINARY_SUBSCR    
             1008  CALL_FUNCTION_1       1  '1 positional argument'
         1010_1012  POP_JUMP_IF_TRUE    996  'to 996'

 L.1573      1014  BREAK_LOOP       
         1016_1018  JUMP_BACK           996  'to 996'
             1020  POP_BLOCK        
           1022_0  COME_FROM_LOOP      980  '980'

 L.1574      1022  LOAD_FAST                'iline'
             1024  LOAD_CONST               1
             1026  LOAD_FAST                'j'
             1028  BUILD_SLICE_2         2 
             1030  BINARY_SUBSCR    
             1032  STORE_FAST               'name'

 L.1575      1034  LOAD_FAST                'self'
             1036  LOAD_ATTR                factory
             1038  LOAD_METHOD              create_block_node
             1040  LOAD_FAST                'name'
             1042  LOAD_FAST                'indent'
             1044  CALL_METHOD_2         2  '2 positional arguments'
             1046  STORE_FAST               'node'

 L.1577      1048  LOAD_FAST                'node'
             1050  LOAD_METHOD              is_name
             1052  LOAD_STR                 'item'
             1054  CALL_METHOD_1         1  '1 positional argument'
         1056_1058  POP_JUMP_IF_FALSE  1072  'to 1072'

 L.1578      1060  LOAD_FAST                'self'
             1062  LOAD_METHOD              unravel_for_list_item
             1064  LOAD_FAST                'indent'
             1066  CALL_METHOD_1         1  '1 positional argument'
             1068  POP_TOP          
             1070  JUMP_FORWARD       1154  'to 1154'
           1072_0  COME_FROM          1056  '1056'

 L.1579      1072  LOAD_FAST                'node'
             1074  LOAD_METHOD              is_name
             1076  LOAD_CONST               ('td', 'th')
             1078  CALL_METHOD_1         1  '1 positional argument'
         1080_1082  POP_JUMP_IF_FALSE  1096  'to 1096'

 L.1580      1084  LOAD_FAST                'self'
             1086  LOAD_METHOD              unravel_for_table_cell
             1088  LOAD_FAST                'indent'
             1090  CALL_METHOD_1         1  '1 positional argument'
             1092  POP_TOP          
             1094  JUMP_FORWARD       1154  'to 1154'
           1096_0  COME_FROM          1080  '1080'

 L.1581      1096  LOAD_FAST                'node'
             1098  LOAD_METHOD              is_name
             1100  LOAD_STR                 'tr'
             1102  CALL_METHOD_1         1  '1 positional argument'
         1104_1106  POP_JUMP_IF_FALSE  1120  'to 1120'

 L.1582      1108  LOAD_FAST                'self'
             1110  LOAD_METHOD              unravel_for_table_row
             1112  LOAD_FAST                'indent'
             1114  CALL_METHOD_1         1  '1 positional argument'
             1116  POP_TOP          
             1118  JUMP_FORWARD       1154  'to 1154'
           1120_0  COME_FROM          1104  '1104'

 L.1583      1120  LOAD_FAST                'node'
             1122  LOAD_METHOD              is_name
             1124  LOAD_CONST               ('thead', 'tfoot', 'tbody')
             1126  CALL_METHOD_1         1  '1 positional argument'
         1128_1130  POP_JUMP_IF_FALSE  1144  'to 1144'

 L.1584      1132  LOAD_FAST                'self'
             1134  LOAD_METHOD              unravel_for_table_body
             1136  LOAD_FAST                'indent'
             1138  CALL_METHOD_1         1  '1 positional argument'
             1140  POP_TOP          
             1142  JUMP_FORWARD       1154  'to 1154'
           1144_0  COME_FROM          1128  '1128'

 L.1586      1144  LOAD_FAST                'self'
             1146  LOAD_METHOD              unravel_for_block
             1148  LOAD_FAST                'indent'
             1150  CALL_METHOD_1         1  '1 positional argument'
             1152  POP_TOP          
           1154_0  COME_FROM          1142  '1142'
           1154_1  COME_FROM          1118  '1118'
           1154_2  COME_FROM          1094  '1094'
           1154_3  COME_FROM          1070  '1070'

 L.1588      1154  LOAD_FAST                'iline'
             1156  LOAD_FAST                'j'
             1158  BINARY_SUBSCR    
             1160  LOAD_STR                 ']'
             1162  COMPARE_OP               ==
         1164_1166  POP_JUMP_IF_FALSE  1188  'to 1188'

 L.1589      1168  LOAD_GLOBAL              DuckParser
             1170  LOAD_ATTR                STATE_BLOCK_READY
             1172  LOAD_FAST                'self'
             1174  STORE_ATTR               state

 L.1590      1176  LOAD_FAST                'self'
             1178  LOAD_METHOD              _take_block_node
             1180  LOAD_FAST                'node'
             1182  CALL_METHOD_1         1  '1 positional argument'
             1184  POP_TOP          
             1186  JUMP_FORWARD       1554  'to 1554'
           1188_0  COME_FROM          1164  '1164'

 L.1592      1188  LOAD_GLOBAL              AttributeParser
             1190  LOAD_FAST                'self'
             1192  LOAD_FAST                'node'
             1194  LOAD_CONST               ('node',)
             1196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1198  LOAD_FAST                'self'
             1200  STORE_ATTR               _attrparser

 L.1593      1202  LOAD_FAST                'self'
             1204  LOAD_ATTR                _attrparser
             1206  LOAD_METHOD              parse_line
             1208  LOAD_FAST                'iline'
             1210  LOAD_FAST                'j'
             1212  LOAD_CONST               None
             1214  BUILD_SLICE_2         2 
             1216  BINARY_SUBSCR    
             1218  CALL_METHOD_1         1  '1 positional argument'
             1220  POP_TOP          

 L.1594      1222  LOAD_FAST                'self'
             1224  LOAD_ATTR                _attrparser
             1226  LOAD_ATTR                finished
         1228_1230  POP_JUMP_IF_FALSE  1268  'to 1268'

 L.1595      1232  LOAD_FAST                'self'
             1234  LOAD_ATTR                _attrparser
             1236  LOAD_ATTR                attributes
             1238  LOAD_FAST                'node'
             1240  STORE_ATTR               attributes

 L.1596      1242  LOAD_GLOBAL              DuckParser
             1244  LOAD_ATTR                STATE_BLOCK_READY
             1246  LOAD_FAST                'self'
             1248  STORE_ATTR               state

 L.1597      1250  LOAD_CONST               None
             1252  LOAD_FAST                'self'
             1254  STORE_ATTR               _attrparser

 L.1598      1256  LOAD_FAST                'self'
             1258  LOAD_METHOD              _take_block_node
             1260  LOAD_FAST                'node'
             1262  CALL_METHOD_1         1  '1 positional argument'
             1264  POP_TOP          
             1266  JUMP_FORWARD       1554  'to 1554'
           1268_0  COME_FROM          1228  '1228'

 L.1600      1268  LOAD_GLOBAL              DuckParser
             1270  LOAD_ATTR                STATE_BLOCK_ATTR
             1272  LOAD_FAST                'self'
             1274  STORE_ATTR               state
         1276_1278  JUMP_FORWARD       1554  'to 1554'
           1280_0  COME_FROM           968  '968'

 L.1601      1280  LOAD_FAST                'iline'
             1282  LOAD_METHOD              startswith
             1284  LOAD_STR                 '. '
             1286  CALL_METHOD_1         1  '1 positional argument'
         1288_1290  POP_JUMP_IF_FALSE  1306  'to 1306'

 L.1602      1292  LOAD_FAST                'self'
             1294  LOAD_METHOD              _parse_line_block_title
             1296  LOAD_FAST                'iline'
             1298  LOAD_FAST                'indent'
             1300  CALL_METHOD_2         2  '2 positional arguments'
             1302  POP_TOP          
             1304  JUMP_FORWARD       1554  'to 1554'
           1306_0  COME_FROM          1288  '1288'

 L.1603      1306  LOAD_FAST                'iline'
             1308  LOAD_METHOD              startswith
             1310  LOAD_STR                 '- '
             1312  CALL_METHOD_1         1  '1 positional argument'
         1314_1316  POP_JUMP_IF_FALSE  1332  'to 1332'

 L.1604      1318  LOAD_FAST                'self'
             1320  LOAD_METHOD              _parse_line_block_item_title
             1322  LOAD_FAST                'iline'
             1324  LOAD_FAST                'indent'
             1326  CALL_METHOD_2         2  '2 positional arguments'
             1328  POP_TOP          
             1330  JUMP_FORWARD       1554  'to 1554'
           1332_0  COME_FROM          1314  '1314'

 L.1605      1332  LOAD_FAST                'iline'
             1334  LOAD_METHOD              startswith
             1336  LOAD_STR                 '* '
             1338  CALL_METHOD_1         1  '1 positional argument'
         1340_1342  POP_JUMP_IF_FALSE  1358  'to 1358'

 L.1606      1344  LOAD_FAST                'self'
             1346  LOAD_METHOD              _parse_line_block_item_content
             1348  LOAD_FAST                'iline'
             1350  LOAD_FAST                'indent'
             1352  CALL_METHOD_2         2  '2 positional arguments'
             1354  POP_TOP          
             1356  JUMP_FORWARD       1554  'to 1554'
           1358_0  COME_FROM          1340  '1340'

 L.1607      1358  LOAD_FAST                'self'
             1360  LOAD_ATTR                current
             1362  LOAD_ATTR                is_leaf
         1364_1366  POP_JUMP_IF_TRUE   1544  'to 1544'
             1368  LOAD_FAST                'self'
             1370  LOAD_ATTR                current
             1372  LOAD_ATTR                is_external
         1374_1376  POP_JUMP_IF_TRUE   1544  'to 1544'

 L.1608      1378  LOAD_FAST                'self'
             1380  LOAD_ATTR                current
             1382  LOAD_ATTR                is_tree_item
         1384_1386  POP_JUMP_IF_FALSE  1398  'to 1398'
             1388  LOAD_FAST                'self'
             1390  LOAD_ATTR                current
             1392  LOAD_ATTR                has_tree_items
         1394_1396  POP_JUMP_IF_FALSE  1544  'to 1544'
           1398_0  COME_FROM          1384  '1384'

 L.1609      1398  LOAD_FAST                'self'
             1400  LOAD_ATTR                current
             1402  LOAD_ATTR                is_tree_item
         1404_1406  POP_JUMP_IF_FALSE  1440  'to 1440'

 L.1610      1408  SETUP_LOOP         1440  'to 1440'
             1410  LOAD_FAST                'self'
             1412  LOAD_ATTR                current
             1414  LOAD_METHOD              is_name
             1416  LOAD_CONST               ('tree', 'item')
             1418  CALL_METHOD_1         1  '1 positional argument'
         1420_1422  POP_JUMP_IF_FALSE  1438  'to 1438'

 L.1611      1424  LOAD_FAST                'self'
             1426  LOAD_ATTR                current
             1428  LOAD_ATTR                parent
             1430  LOAD_FAST                'self'
             1432  STORE_ATTR               current
         1434_1436  JUMP_BACK          1410  'to 1410'
           1438_0  COME_FROM          1420  '1420'
             1438  POP_BLOCK        
           1440_0  COME_FROM_LOOP     1408  '1408'
           1440_1  COME_FROM          1404  '1404'

 L.1612      1440  SETUP_LOOP         1502  'to 1502'
             1442  LOAD_FAST                'self'
             1444  LOAD_ATTR                current
             1446  LOAD_ATTR                outer
             1448  LOAD_FAST                'indent'
             1450  COMPARE_OP               ==
         1452_1454  POP_JUMP_IF_FALSE  1500  'to 1500'
             1456  LOAD_FAST                'self'
             1458  LOAD_ATTR                current
             1460  LOAD_ATTR                available
           1462_0  COME_FROM          1186  '1186'
         1462_1464  POP_JUMP_IF_TRUE   1500  'to 1500'

 L.1613      1466  LOAD_GLOBAL              isinstance
             1468  LOAD_FAST                'self'
             1470  LOAD_ATTR                current
             1472  LOAD_GLOBAL              Division
             1474  LOAD_GLOBAL              Document
             1476  BUILD_TUPLE_2         2 
             1478  CALL_FUNCTION_2       2  '2 positional arguments'
         1480_1482  POP_JUMP_IF_FALSE  1486  'to 1486'

 L.1614      1484  BREAK_LOOP       
           1486_0  COME_FROM          1480  '1480'

 L.1615      1486  LOAD_FAST                'self'
             1488  LOAD_ATTR                current
             1490  LOAD_ATTR                parent
             1492  LOAD_FAST                'self'
             1494  STORE_ATTR               current
         1496_1498  JUMP_BACK          1442  'to 1442'
           1500_0  COME_FROM          1462  '1462'
           1500_1  COME_FROM          1452  '1452'
             1500  POP_BLOCK        
           1502_0  COME_FROM_LOOP     1440  '1440'

 L.1616      1502  LOAD_FAST                'self'
             1504  LOAD_ATTR                factory
             1506  LOAD_METHOD              create_block_paragraph_node
             1508  LOAD_FAST                'indent'
             1510  CALL_METHOD_1         1  '1 positional argument'
             1512  STORE_FAST               'node'

 L.1617      1514  LOAD_FAST                'self'
             1516  LOAD_ATTR                current
             1518  LOAD_METHOD              add_child
             1520  LOAD_FAST                'node'
             1522  CALL_METHOD_1         1  '1 positional argument'
             1524  POP_TOP          

 L.1618      1526  LOAD_FAST                'node'
             1528  LOAD_FAST                'self'
             1530  STORE_ATTR               current

 L.1619      1532  LOAD_FAST                'self'
             1534  LOAD_METHOD              add_text
             1536  LOAD_FAST                'iline'
             1538  CALL_METHOD_1         1  '1 positional argument'
             1540  POP_TOP          
           1542_0  COME_FROM          1266  '1266'
             1542  JUMP_FORWARD       1554  'to 1554'
           1544_0  COME_FROM          1394  '1394'
           1544_1  COME_FROM          1374  '1374'
           1544_2  COME_FROM          1364  '1364'

 L.1621      1544  LOAD_FAST                'self'
             1546  LOAD_METHOD              add_text
             1548  LOAD_FAST                'iline'
             1550  CALL_METHOD_1         1  '1 positional argument'
             1552  POP_TOP          
           1554_0  COME_FROM          1542  '1542'
           1554_1  COME_FROM          1356  '1356'
           1554_2  COME_FROM          1330  '1330'
           1554_3  COME_FROM          1304  '1304'
           1554_4  COME_FROM          1276  '1276'

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 1462_1464

    def _parse_line_block_title(self, iline, indent):
        self.push_text()
        self.unravel_for_block(indent)
        self.factory.handle_block_title(indent, indent + 2)
        self._parse_line(' ' * self.current.inner + iline[2:])

    def _parse_line_block_item_title(self, iline, indent):
        self.push_text()
        self.unravel_for_indent(indent)
        self.factory.handle_block_item_title(indent, indent + 2)
        self._parse_line(' ' * self.current.inner + iline[2:])

    def _parse_line_block_item_content(self, iline, indent):
        self.push_text()
        self.unravel_for_indent(indent)
        node = self.factory.handle_block_item_content(indent, indent + 2)
        self._parse_line(' ' * node.inner + iline[2:])

    def _parse_line_block_attr(self, line):
        self._attrparser.parse_line(line)
        if self._attrparser.finished:
            node = self._attrparser.node
            node.attributes = self._attrparser.attributes
            self.state = DuckParser.STATE_BLOCK_READY
            self._attrparser = None
            self._take_block_node(node)

    def _parse_line_block_ready(self, line):
        indent = DuckParser.get_indent(line)
        if indent < self.current.outer:
            while self.current.outer > indent:
                if isinstance(self.current, (Division, Document)):
                    break
                self.current = self.current.parent

        else:
            if line.lstrip().startswith('@'):
                self.info_state = DuckParser.INFO_STATE_INFO
            self.current.inner = DuckParser.get_indent(line)
        self.state = DuckParser.STATE_BLOCK
        self._parse_line(line)

    def _take_block_node(self, node):
        if node.extension:
            for extension in self.extensions_by_module[node.extension]:
                if extension.take_block_node(node):
                    return

            if node.nsuri is not None:
                self.current.add_child(node)
                self.current = node
            else:
                raise SyntaxError('Unrecognized extension element: ' + node.name, self)
        else:
            self.current.add_child(node)
            self.current = node

    def set_text(self, text):
        self._text = text

    def add_text(self, text):
        self._text += text

    def push_text(self):
        if self._text != '':
            if self.info_state != DuckParser.INFO_STATE_NONE:
                self.curinfo.add_text(self._text)
            else:
                self.current.add_text(self._text)
            self.set_text('')

    def unravel_for_list_item(self, indent):
        self.unravel_for_indent(indent)
        while self.current.outer == indent:
            if isinstance(self.current, (Division, Document)):
                break
            if self.current.available:
                break
            if self.current.is_list:
                break
            self.current = self.current.parent

    def unravel_for_table_cell(self, indent):
        self.unravel_for_indent(indent)
        while self.current.outer == indent:
            if isinstance(self.current, (Division, Document)):
                break
            if self.current.available:
                break
            if self.current.is_name('tr'):
                break
            self.current = self.current.parent

        if self.current.is_tree_item:
            while self.current.is_name(('tree', 'item')):
                self.current = self.current.parent

    def unravel_for_table_row(self, indent):
        self.unravel_for_indent(indent)
        while self.current.outer == indent:
            if isinstance(self.current, (Division, Document)):
                break
            if self.current.available:
                break
            if self.current.is_name(('table', 'thead', 'tfoot', 'tbody')):
                break
            self.current = self.current.parent

        if self.current.is_tree_item:
            while self.current.is_name(('tree', 'item')):
                self.current = self.current.parent

    def unravel_for_table_body(self, indent):
        self.unravel_for_indent(indent)
        while self.current.outer == indent:
            if isinstance(self.current, (Division, Document)):
                break
            if self.current.available:
                break
            if self.current.is_name('table'):
                break
            self.current = self.current.parent

        if self.current.is_tree_item:
            while self.current.is_name(('tree', 'item')):
                self.current = self.current.parent

    def unravel_for_block(self, indent):
        self.unravel_for_indent(indent)
        while self.current.outer == indent:
            if isinstance(self.current, (Division, Document)):
                break
            if self.current.available:
                break
            self.current = self.current.parent

        if self.current.is_tree_item:
            while self.current.is_name(('tree', 'item')):
                self.current = self.current.parent

    def unravel_for_indent(self, indent):
        while self.current.outer > indent or self.current.is_leaf:
            if isinstance(self.current, (Division, Document)):
                break
            self.current = self.current.parent


def _isnmtoken--- This code section failed: ---

 L.1782         0  LOAD_GLOBAL              ord
                2  LOAD_FAST                'c'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'i'

 L.1783         8  LOAD_STR                 'A'
               10  LOAD_FAST                'c'
               12  DUP_TOP          
               14  ROT_THREE        
               16  COMPARE_OP               <=
               18  JUMP_IF_FALSE_OR_POP    26  'to 26'
               20  LOAD_STR                 'Z'
               22  COMPARE_OP               <=
               24  JUMP_IF_TRUE_OR_POP   506  'to 506'
             26_0  COME_FROM            18  '18'
               26  ROT_TWO          
               28  POP_TOP          
            30_32  JUMP_IF_TRUE_OR_POP   506  'to 506'
               34  LOAD_STR                 'a'
               36  LOAD_FAST                'c'
               38  DUP_TOP          
               40  ROT_THREE        
               42  COMPARE_OP               <=
               44  JUMP_IF_FALSE_OR_POP    52  'to 52'
               46  LOAD_STR                 'z'
               48  COMPARE_OP               <=
               50  JUMP_IF_TRUE_OR_POP   506  'to 506'
             52_0  COME_FROM            44  '44'
               52  ROT_TWO          
               54  POP_TOP          
            56_58  JUMP_IF_TRUE_OR_POP   506  'to 506'
               60  LOAD_STR                 '0'
               62  LOAD_FAST                'c'
               64  DUP_TOP          
               66  ROT_THREE        
               68  COMPARE_OP               <=
               70  JUMP_IF_FALSE_OR_POP    78  'to 78'
               72  LOAD_STR                 '9'
               74  COMPARE_OP               <=
               76  JUMP_IF_TRUE_OR_POP   506  'to 506'
             78_0  COME_FROM            70  '70'
               78  ROT_TWO          
               80  POP_TOP          
            82_84  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1784        86  LOAD_FAST                'c'
               88  LOAD_STR                 ':'
               90  COMPARE_OP               ==
               92  JUMP_IF_TRUE_OR_POP   124  'to 124'
               94  LOAD_FAST                'c'
               96  LOAD_STR                 '_'
               98  COMPARE_OP               ==
              100  JUMP_IF_TRUE_OR_POP   124  'to 124'
              102  LOAD_FAST                'c'
              104  LOAD_STR                 '-'
              106  COMPARE_OP               ==
              108  JUMP_IF_TRUE_OR_POP   124  'to 124'
              110  LOAD_FAST                'c'
              112  LOAD_STR                 '.'
              114  COMPARE_OP               ==
              116  JUMP_IF_TRUE_OR_POP   124  'to 124'
              118  LOAD_FAST                'i'
              120  LOAD_CONST               183
              122  COMPARE_OP               ==
            124_0  COME_FROM           116  '116'
            124_1  COME_FROM           108  '108'
            124_2  COME_FROM           100  '100'
            124_3  COME_FROM            92  '92'
          124_126  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1785       128  LOAD_CONST               192
              130  LOAD_FAST                'i'
              132  DUP_TOP          
              134  ROT_THREE        
              136  COMPARE_OP               <=
              138  JUMP_IF_FALSE_OR_POP   146  'to 146'
              140  LOAD_CONST               214
              142  COMPARE_OP               <=
              144  JUMP_IF_TRUE_OR_POP   506  'to 506'
            146_0  COME_FROM           138  '138'
              146  ROT_TWO          
              148  POP_TOP          
          150_152  JUMP_IF_TRUE_OR_POP   506  'to 506'
              154  LOAD_CONST               216
              156  LOAD_FAST                'i'
              158  DUP_TOP          
              160  ROT_THREE        
              162  COMPARE_OP               <=
              164  JUMP_IF_FALSE_OR_POP   172  'to 172'
              166  LOAD_CONST               246
              168  COMPARE_OP               <=
              170  JUMP_IF_TRUE_OR_POP   506  'to 506'
            172_0  COME_FROM           164  '164'
              172  ROT_TWO          
              174  POP_TOP          
          176_178  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1786       180  LOAD_CONST               248
              182  LOAD_FAST                'i'
              184  DUP_TOP          
              186  ROT_THREE        
              188  COMPARE_OP               <=
              190  JUMP_IF_FALSE_OR_POP   198  'to 198'
              192  LOAD_CONST               767
              194  COMPARE_OP               <=
              196  JUMP_IF_TRUE_OR_POP   506  'to 506'
            198_0  COME_FROM           190  '190'
              198  ROT_TWO          
              200  POP_TOP          
          202_204  JUMP_IF_TRUE_OR_POP   506  'to 506'
              206  LOAD_CONST               880
              208  LOAD_FAST                'i'
              210  DUP_TOP          
              212  ROT_THREE        
              214  COMPARE_OP               <=
              216  JUMP_IF_FALSE_OR_POP   224  'to 224'
              218  LOAD_CONST               893
              220  COMPARE_OP               <=
              222  JUMP_IF_TRUE_OR_POP   506  'to 506'
            224_0  COME_FROM           216  '216'
              224  ROT_TWO          
              226  POP_TOP          
          228_230  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1787       232  LOAD_CONST               895
              234  LOAD_FAST                'i'
              236  DUP_TOP          
              238  ROT_THREE        
              240  COMPARE_OP               <=
              242  JUMP_IF_FALSE_OR_POP   250  'to 250'
              244  LOAD_CONST               8191
              246  COMPARE_OP               <=
              248  JUMP_IF_TRUE_OR_POP   506  'to 506'
            250_0  COME_FROM           242  '242'
              250  ROT_TWO          
              252  POP_TOP          
          254_256  JUMP_IF_TRUE_OR_POP   506  'to 506'
              258  LOAD_CONST               8204
              260  LOAD_FAST                'i'
              262  DUP_TOP          
              264  ROT_THREE        
              266  COMPARE_OP               <=
          268_270  JUMP_IF_FALSE_OR_POP   278  'to 278'
              272  LOAD_CONST               8205
              274  COMPARE_OP               <=
              276  JUMP_IF_TRUE_OR_POP   506  'to 506'
            278_0  COME_FROM           268  '268'
              278  ROT_TWO          
              280  POP_TOP          
          282_284  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1788       286  LOAD_CONST               8304
              288  LOAD_FAST                'i'
              290  DUP_TOP          
              292  ROT_THREE        
              294  COMPARE_OP               <=
          296_298  JUMP_IF_FALSE_OR_POP   306  'to 306'
              300  LOAD_CONST               8591
              302  COMPARE_OP               <=
              304  JUMP_IF_TRUE_OR_POP   506  'to 506'
            306_0  COME_FROM           296  '296'
              306  ROT_TWO          
              308  POP_TOP          
          310_312  JUMP_IF_TRUE_OR_POP   506  'to 506'
              314  LOAD_CONST               11264
              316  LOAD_FAST                'i'
              318  DUP_TOP          
              320  ROT_THREE        
              322  COMPARE_OP               <=
          324_326  JUMP_IF_FALSE_OR_POP   334  'to 334'
              328  LOAD_CONST               12271
              330  COMPARE_OP               <=
              332  JUMP_IF_TRUE_OR_POP   506  'to 506'
            334_0  COME_FROM           324  '324'
              334  ROT_TWO          
              336  POP_TOP          
          338_340  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1789       342  LOAD_CONST               12289
              344  LOAD_FAST                'i'
              346  DUP_TOP          
              348  ROT_THREE        
              350  COMPARE_OP               <=
          352_354  JUMP_IF_FALSE_OR_POP   362  'to 362'
              356  LOAD_CONST               55295
              358  COMPARE_OP               <=
              360  JUMP_IF_TRUE_OR_POP   506  'to 506'
            362_0  COME_FROM           352  '352'
              362  ROT_TWO          
              364  POP_TOP          
          366_368  JUMP_IF_TRUE_OR_POP   506  'to 506'
              370  LOAD_CONST               63744
              372  LOAD_FAST                'i'
              374  DUP_TOP          
              376  ROT_THREE        
              378  COMPARE_OP               <=
          380_382  JUMP_IF_FALSE_OR_POP   390  'to 390'
              384  LOAD_CONST               64975
              386  COMPARE_OP               <=
              388  JUMP_IF_TRUE_OR_POP   506  'to 506'
            390_0  COME_FROM           380  '380'
              390  ROT_TWO          
              392  POP_TOP          
          394_396  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1790       398  LOAD_CONST               65008
              400  LOAD_FAST                'i'
              402  DUP_TOP          
              404  ROT_THREE        
              406  COMPARE_OP               <=
          408_410  JUMP_IF_FALSE_OR_POP   418  'to 418'
              412  LOAD_CONST               65533
              414  COMPARE_OP               <=
              416  JUMP_IF_TRUE_OR_POP   506  'to 506'
            418_0  COME_FROM           408  '408'
              418  ROT_TWO          
              420  POP_TOP          
          422_424  JUMP_IF_TRUE_OR_POP   506  'to 506'
              426  LOAD_CONST               65536
              428  LOAD_FAST                'i'
              430  DUP_TOP          
              432  ROT_THREE        
              434  COMPARE_OP               <=
          436_438  JUMP_IF_FALSE_OR_POP   446  'to 446'
              440  LOAD_CONST               983039
              442  COMPARE_OP               <=
              444  JUMP_IF_TRUE_OR_POP   506  'to 506'
            446_0  COME_FROM           436  '436'
              446  ROT_TWO          
              448  POP_TOP          
          450_452  JUMP_IF_TRUE_OR_POP   506  'to 506'

 L.1791       454  LOAD_CONST               768
              456  LOAD_FAST                'i'
              458  DUP_TOP          
              460  ROT_THREE        
              462  COMPARE_OP               <=
          464_466  JUMP_IF_FALSE_OR_POP   474  'to 474'
              468  LOAD_CONST               879
              470  COMPARE_OP               <=
            472_0  COME_FROM           472  '472'
            472_1  COME_FROM           450  '450'
            472_2  COME_FROM           444  '444'
            472_3  COME_FROM           422  '422'
            472_4  COME_FROM           416  '416'
            472_5  COME_FROM           394  '394'
            472_6  COME_FROM           388  '388'
            472_7  COME_FROM           366  '366'
            472_8  COME_FROM           360  '360'
            472_9  COME_FROM           338  '338'
           472_10  COME_FROM           332  '332'
           472_11  COME_FROM           310  '310'
           472_12  COME_FROM           304  '304'
           472_13  COME_FROM           282  '282'
           472_14  COME_FROM           276  '276'
           472_15  COME_FROM           254  '254'
           472_16  COME_FROM           248  '248'
           472_17  COME_FROM           228  '228'
           472_18  COME_FROM           222  '222'
           472_19  COME_FROM           202  '202'
           472_20  COME_FROM           196  '196'
           472_21  COME_FROM           176  '176'
           472_22  COME_FROM           170  '170'
           472_23  COME_FROM           150  '150'
           472_24  COME_FROM           144  '144'
           472_25  COME_FROM           124  '124'
           472_26  COME_FROM            82  '82'
           472_27  COME_FROM            76  '76'
           472_28  COME_FROM            56  '56'
           472_29  COME_FROM            50  '50'
           472_30  COME_FROM            30  '30'
           472_31  COME_FROM            24  '24'
              472  JUMP_IF_TRUE_OR_POP   506  'to 506'
            474_0  COME_FROM           464  '464'
              474  ROT_TWO          
              476  POP_TOP          
          478_480  JUMP_IF_TRUE_OR_POP   506  'to 506'
              482  LOAD_CONST               8255
              484  LOAD_FAST                'i'
              486  DUP_TOP          
              488  ROT_THREE        
              490  COMPARE_OP               <=
          492_494  JUMP_IF_FALSE_OR_POP   502  'to 502'
              496  LOAD_CONST               8256
              498  COMPARE_OP               <=
              500  RETURN_VALUE     
            502_0  COME_FROM           492  '492'
              502  ROT_TWO          
              504  POP_TOP          
            506_0  COME_FROM           478  '478'
              506  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_IF_TRUE_OR_POP' instruction at offset 24