# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/simplecms/template.py
# Compiled at: 2015-02-08 05:34:11
"""
This file is part of the wempy template system
Copyrighted by G. Clifford Williams <gcw@notadiscussion.com>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)

Author: G. Clifford Williams (for wempy templating system) 
Original-Author: Thadeus Burgess (for the web2py project)

Contributors:

- Thank you to Massimo Di Pierro for creating the original gluon/template.py
- Thank you to Jonathan Lundell for extensively testing the regex on Jython.
- Thank you to Limodou (creater of uliweb) who inspired the block-element 
support for web2py.

----------------------------
some minor changes
doc: https://jan-karel.nl/user_guide/views.html#template_language

"""
import os, sys, re, simplecms.helpers
try:
    bytes
except Exception:
    bytes = str

try:
    import cStringIO as StringIO
except:
    from io import StringIO

io = StringIO
py = sys.version_info
py3 = py >= (3, 0, 0)
try:
    from restricted import RestrictedError
except:

    def RestrictedError(a, b, c):
        return RuntimeError


class Node(object):
    """
    Basic Container Object
    """

    def __init__(self, value=None, pre_extend=False):
        self.value = value
        self.pre_extend = pre_extend

    def __str__(self):
        return str(self.value)


class SuperNode(Node):

    def __init__(self, name='', pre_extend=False):
        self.name = name
        self.value = None
        self.pre_extend = pre_extend
        return

    def __str__(self):
        if self.value:
            return str(self.value)
        else:
            return ''

    def __repr__(self):
        return '%s->%s' % (self.name, self.value)


class BlockNode(Node):
    """
    Block Container.

    This Node can contain other Nodes and will render in a hierarchical order
    of when nodes were added.

    ie::

        {{ block test }}
            This is default block test
        {{ end }}
    """

    def __init__(self, name='', pre_extend=False, delimiters=('{{', '}}')):
        """
        name - Name of this Node.
        """
        self.nodes = []
        self.name = name
        self.pre_extend = pre_extend
        self.left, self.right = delimiters

    def __repr__(self):
        lines = [
         '%sblock %s%s' % (self.left, self.name, self.right)]
        for node in self.nodes:
            lines.append(str(node))

        lines.append('%send%s' % (self.left, self.right))
        return ('').join(lines)

    def __str__(self):
        """
        Get this BlockNodes content, not including child Nodes
        """
        lines = []
        for node in self.nodes:
            if not isinstance(node, BlockNode):
                lines.append(str(node))

        return ('').join(lines)

    def append(self, node):
        """
        Add an element to the nodes.

        Keyword Arguments

        - node -- Node object or string to append.
        """
        if isinstance(node, str) or isinstance(node, Node):
            self.nodes.append(node)
        else:
            raise TypeError('Invalid type; must be instance of ``str`` or ``BlockNode``. %s' % node)

    def extend(self, other):
        """
        Extend the list of nodes with another BlockNode class.

        Keyword Arguments

        - other -- BlockNode or Content object to extend from.
        """
        if isinstance(other, BlockNode):
            self.nodes.extend(other.nodes)
        else:
            raise TypeError('Invalid type; must be instance of ``BlockNode``. %s' % other)

    def output(self, blocks):
        """
        Merges all nodes into a single string.

        blocks -- Dictionary of blocks that are extending
        from this template.
        """
        lines = []
        for node in self.nodes:
            if isinstance(node, BlockNode):
                if node.name in blocks:
                    lines.append(blocks[node.name].output(blocks))
                else:
                    lines.append(node.output(blocks))
            else:
                lines.append(str(node))

        return ('').join(lines)


class Content(BlockNode):
    """
    Parent Container -- Used as the root level BlockNode.

    Contains functions that operate as such.
    """

    def __init__(self, name='ContentBlock', pre_extend=False):
        """
        Keyword Arguments

        name -- Unique name for this BlockNode
        """
        self.name = name
        self.nodes = []
        self.blocks = {}
        self.pre_extend = pre_extend

    def __str__(self):
        lines = []
        for node in self.nodes:
            if isinstance(node, BlockNode):
                if node.name in self.blocks:
                    lines.append(self.blocks[node.name].output(self.blocks))
                else:
                    lines.append(node.output(self.blocks))
            else:
                lines.append(str(node))

        return ('').join(lines)

    def _insert(self, other, index=0):
        """
        Inserts object at index.
        """
        if isinstance(other, str) or isinstance(other, Node):
            self.nodes.insert(index, other)
        else:
            raise TypeError('Invalid type, must be instance of ``str`` or ``Node``.')

    def insert(self, other, index=0):
        """
        Inserts object at index.

        You may pass a list of objects and have them inserted.
        """
        if isinstance(other, (list, tuple)):
            other.reverse()
            for item in other:
                self._insert(item, index)

        else:
            self._insert(other, index)

    def append(self, node):
        """
        Adds a node to list. If it is a BlockNode then we assign a block for it.
        """
        if isinstance(node, str) or isinstance(node, Node):
            self.nodes.append(node)
            if isinstance(node, BlockNode):
                self.blocks[node.name] = node
        else:
            raise TypeError('Invalid type, must be instance of ``str`` or ``BlockNode``. %s' % node)

    def extend(self, other):
        """
        Extends the objects list of nodes with another objects nodes
        """
        if isinstance(other, BlockNode):
            self.nodes.extend(other.nodes)
            self.blocks.update(other.blocks)
        else:
            raise TypeError('Invalid type; must be instance of ``BlockNode``. %s' % other)

    def clear_content(self):
        self.nodes = []


class TemplateParser(object):
    default_delimiters = (
     '{{', '}}')
    r_tag = re.compile('(\\{\\{.*?\\}\\})', re.DOTALL)
    r_multiline = re.compile('(""".*?""")|(\\\'\\\'\\\'.*?\\\'\\\'\\\')', re.DOTALL)
    re_block = re.compile('^(elif |else:|except:|except |finally:).*$', re.DOTALL)
    re_unblock = re.compile('^(return|continue|break|raise)( .*)?$', re.DOTALL)
    re_pass = re.compile('^pass( .*)?$', re.DOTALL)

    def __init__(self, text, name='ParserContainer', context=dict(), path='views/', writer='sys.stdout.write', lexers={}, delimiters=(
 '{{', '}}'), _super_nodes=[]):
        """
        text -- text to parse
        context -- context to parse in
        path -- folder path to templates
        writer -- string of writer class to use
        lexers -- dict of custom lexers to use.
        delimiters -- for example ('{{','}}')
        _super_nodes -- a list of nodes to check for inclusion
                        this should only be set by "self.extend"
                        It contains a list of SuperNodes from a child
                        template that need to be handled.
        """
        self.name = name
        self.text = text
        self.writer = writer
        if isinstance(lexers, dict):
            self.lexers = lexers
        else:
            self.lexers = {}
        self.path = path
        self.context = context
        self.delimiters = delimiters
        self.content = Content(name=name)
        self.stack = [
         self.content]
        self.super_nodes = []
        self.child_super_nodes = _super_nodes
        self.blocks = {}
        self.parse(text)
        self.last_output = None
        return

    def to_string(self):
        """
        Return the parsed template with correct indentation.

        Used to make it easier to port to python3.
        """
        return self.reindent(str(self.content))

    def __str__(self):
        """Make sure str works exactly the same as python 3"""
        return self.to_string()

    def __unicode__(self):
        """Make sure str works exactly the same as python 3"""
        return self.to_string()

    def reindent(self, text):
        """
        Reindents a string of unindented python code.
        """
        if self.writer == 'sys.stdout.write':
            lines = text.split('\n')
            lines.insert(0, 'import sys')
        else:
            lines = text.split('\n')
        new_lines = []
        credit = 0
        k = 0
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if TemplateParser.re_block.match(line):
                k = k + credit - 1
            k = max(k, 0)
            new_lines.append(' ' * (4 * k) + line)
            credit = 0
            if TemplateParser.re_pass.match(line):
                k -= 1
            if TemplateParser.re_unblock.match(line):
                credit = 1
                k -= 1
            if line.endswith(':') and not line.startswith('#'):
                k += 1

        new_text = ('\n').join(new_lines)
        if k > 0:
            self._raise_error('missing "pass" in view', new_text)
        elif k < 0:
            self._raise_error('too many "pass" in view', new_text)
        return new_text

    def _raise_error(self, message='', text=None):
        """
        Raise an error using itself as the filename and textual content.
        """
        raise RestrictedError(self.name, text or self.text, message)

    def _get_file_text(self, filename):
        """
        Attempt to open ``filename`` and retrieve its text.

        This will use self.path to search for the file.
        """
        if not filename.strip():
            self._raise_error('Invalid template filename')
        filename = eval(filename, self.context)
        filepath = self.path and os.path.join(self.path, filename) or filename
        try:
            fileobj = open(filepath, 'rb')
            text = fileobj.read()
            fileobj.close()
        except IOError:
            self._raise_error('Unable to open included view file: ' + filepath)

        return text

    def include(self, content, filename):
        """
        Include ``filename`` here.
        """
        text = self._get_file_text(filename)
        t = TemplateParser(text, name=filename, context=self.context, path=self.path, writer=self.writer, delimiters=self.delimiters)
        content.append(t.content)

    def extend(self, filename):
        """
        Extend ``filename``. Anything not declared in a block defined by the
        parent will be placed in the parent templates ``{{include}}`` block.
        """
        text = self._get_file_text(filename)
        super_nodes = []
        super_nodes.extend(self.child_super_nodes)
        super_nodes.extend(self.super_nodes)
        t = TemplateParser(text, name=filename, context=self.context, path=self.path, writer=self.writer, delimiters=self.delimiters, _super_nodes=super_nodes)
        buf = BlockNode(name='__include__' + filename, delimiters=self.delimiters)
        pre = []
        for node in self.content.nodes:
            if isinstance(node, BlockNode):
                if node.name in t.content.blocks:
                    continue
            if isinstance(node, Node):
                if node.pre_extend:
                    pre.append(node)
                    continue
                buf.append(node)
            else:
                buf.append(node)

        self.content.nodes = []
        t.content.blocks['__include__' + filename] = buf
        t.content.insert(pre)
        t.content.extend(self.content)
        self.content = t.content

    def parse(self, text):
        in_tag = False
        extend = None
        pre_extend = True
        if py3 and isinstance(text, bytes):
            text = text.decode('utf8')
        ij = self.r_tag.split(text)
        for j in range(len(ij)):
            i = ij[j]
            if i:
                if len(self.stack) == 0:
                    self._raise_error('The "end" tag is unmatched, please check if you have a starting "block" tag')
                top = self.stack[(-1)]
                if in_tag:
                    line = i
                    line = line[2:-2].strip()
                    if not line:
                        continue

                    def remove_newline(re_val):
                        return re_val.group(0).replace('\n', '\\n')

                    line = re.sub(TemplateParser.r_multiline, remove_newline, line)
                    if line.startswith('='):
                        name, value = '=', line[1:].strip()
                    else:
                        v = line.split(' ', 1)
                        if len(v) == 1:
                            name = v[0]
                            value = ''
                        else:
                            name = v[0]
                            value = v[1]
                    if name in self.lexers:
                        self.lexers[name](parser=self, value=value, top=top, stack=self.stack)
                    elif name == '=':
                        if self.writer == 'print':
                            buf = '\n%s(%s),' % (self.writer, value)
                        else:
                            buf = '\n%s(%s)' % (self.writer, value)
                        top.append(Node(buf, pre_extend=pre_extend))
                    elif name == 'block' and not value.startswith('='):
                        node = BlockNode(name=value.strip(), pre_extend=pre_extend, delimiters=self.delimiters)
                        top.append(node)
                        self.stack.append(node)
                    elif name == 'end' and not value.startswith('='):
                        self.blocks[top.name] = top
                        self.stack.pop()
                    elif name == 'super' and not value.startswith('='):
                        if value:
                            target_node = value
                        else:
                            target_node = top.name
                        node = SuperNode(name=target_node, pre_extend=pre_extend)
                        self.super_nodes.append(node)
                        top.append(node)
                    elif name == 'include' and not value.startswith('='):
                        if value:
                            self.include(top, value)
                        else:
                            include_node = BlockNode(name='__include__' + self.name, pre_extend=pre_extend, delimiters=self.delimiters)
                            top.append(include_node)
                    elif name == 'extend' and not value.startswith('='):
                        extend = value
                        pre_extend = False
                    elif line and in_tag:
                        tokens = line.split('\n')
                        continuation = False
                        len_parsed = 0
                        for k in range(len(tokens)):
                            tokens[k] = tokens[k].strip()
                            len_parsed += len(tokens[k])
                            if tokens[k].startswith('='):
                                if tokens[k].endswith('\\'):
                                    continuation = True
                                    tokens[k] = '\n%s(%s' % (self.writer, tokens[k][1:].strip())
                                    tokens[k] = '\n%s(%s' % (self.writer, tokens[k][1:].strip())
                                elif self.writer == 'print':
                                    tokens[k] = '\n%s(%s),' % (self.writer, tokens[k][1:].strip())
                                else:
                                    tokens[k] = '\n%s(%s)' % (self.writer, tokens[k][1:].strip())
                            elif continuation:
                                if self.writer == 'print':
                                    tokens[k] += '),'
                                else:
                                    tokens[k] += ')'
                                continuation = False

                        buf = '\n%s' % ('\n').join(tokens)
                        top.append(Node(buf, pre_extend=pre_extend))
                else:
                    if self.writer == 'print':
                        buf = '\n%s(%r),' % (self.writer, i)
                    else:
                        buf = '\n%s(%r)' % (self.writer, i)
                    top.append(Node(buf, pre_extend=pre_extend))
            in_tag = not in_tag

        to_rm = []
        for node in self.child_super_nodes:
            if node.name in self.blocks:
                node.value = self.blocks[node.name]
                to_rm.append(node)

        for node in to_rm:
            self.child_super_nodes.remove(node)

        if extend:
            self.extend(extend)
        return

    def render(self, *args, **kwargs):
        exec_buffer = io.StringIO()
        sys.stdout = exec_buffer
        temp_context = {}
        temp_context.update(self.context)
        temp_context.update(*args, **kwargs)
        code = str(self)
        try:
            exec code in temp_context
            sys.stdout = sys.__stdout__
            self.last_output = exec_buffer.getvalue()
            exec_buffer.close()
        except Exception:
            raise

        return self.last_output