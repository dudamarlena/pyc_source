# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/template.py
# Compiled at: 2013-10-14 11:16:25
"""
This file is part of the web2py Web Framework (Copyrighted, 2007-2011).
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)

Author: Thadeus Burgess

Contributors:

- Thank you to Massimo Di Pierro for creating the original gluon/template.py
- Thank you to Jonathan Lundell for extensively testing the regex on Jython.
- Thank you to Limodou (creater of uliweb) who inspired the block-element support for web2py.
"""
import os, cgi, logging
from re import compile, sub, escape, DOTALL
try:
    import cStringIO as StringIO
except:
    from io import StringIO

try:
    from gluon.restricted import RestrictedError
    from gluon.globals import current
except ImportError:
    current = None

    def RestrictedError(a, b, c):
        logging.error(str(a) + ':' + str(b) + ':' + str(c))
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


def output_aux(node, blocks):
    if isinstance(node, BlockNode):
        return blocks[node.name].output(blocks) if node.name in blocks else node.output(blocks)
    return str(node)


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
        lines += [ str(node) for node in self.nodes ]
        lines.append('%send%s' % (self.left, self.right))
        return ('').join(lines)

    def __str__(self):
        """
        Get this BlockNodes content, not including child Nodes
        """
        return ('').join(str(node) for node in self.nodes if not isinstance(node, BlockNode))

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
        return ('').join(output_aux(node, blocks) for node in self.nodes)


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
        return ('').join(output_aux(node, self.blocks) for node in self.nodes)

    def _insert(self, other, index=0):
        """
        Inserts object at index.
        """
        if isinstance(other, (str, Node)):
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
        if isinstance(node, (str, Node)):
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
    default_delimiters = ('{{', '}}')
    r_tag = compile('(\\{\\{.*?\\}\\})', DOTALL)
    r_multiline = compile('(""".*?""")|(\\\'\\\'\\\'.*?\\\'\\\'\\\')', DOTALL)
    re_block = compile('^(elif |else:|except:|except |finally:).*$', DOTALL)
    re_unblock = compile('^(return|continue|break|raise)( .*)?$', DOTALL)
    re_pass = compile('^pass( .*)?$', DOTALL)

    def __init__(self, text, name='ParserContainer', context=dict(), path='views/', writer='response.write', lexers={}, delimiters=('{{', '}}'), _super_nodes=[]):
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
        if delimiters != self.default_delimiters:
            escaped_delimiters = (
             escape(delimiters[0]),
             escape(delimiters[1]))
            self.r_tag = compile('(%s.*?%s)' % escaped_delimiters, DOTALL)
        elif hasattr(context.get('response', None), 'delimiters'):
            if context['response'].delimiters != self.default_delimiters:
                escaped_delimiters = (escape(context['response'].delimiters[0]),
                 escape(context['response'].delimiters[1]))
                self.r_tag = compile('(%s.*?%s)' % escaped_delimiters, DOTALL)
        self.content = Content(name=name)
        self.stack = [
         self.content]
        self.super_nodes = []
        self.child_super_nodes = _super_nodes
        self.blocks = {}
        self.parse(text)
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
        context = self.context
        if current and 'response' not in context:
            context['response'] = getattr(current, 'response', None)
        filename = eval(filename, context)
        if not filename:
            return ''
        else:
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
        text = self._get_file_text(filename) or '%sinclude%s' % tuple(self.delimiters)
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
        t_content = t.content
        t_content.blocks['__include__' + filename] = buf
        t_content.insert(pre)
        t_content.extend(self.content)
        self.content = t_content

    def parse(self, text):
        in_tag = False
        extend = None
        pre_extend = True
        ij = self.r_tag.split(text)
        stack = self.stack
        for j in range(len(ij)):
            i = ij[j]
            if i:
                if not stack:
                    self._raise_error('The "end" tag is unmatched, please check if you have a starting "block" tag')
                top = stack[(-1)]
                if in_tag:
                    line = i
                    line = line[len(self.delimiters[0]):-len(self.delimiters[1])].strip()
                    if not line:
                        continue

                    def remove_newline(re_val):
                        return re_val.group(0).replace('\n', '\\n')

                    line = sub(TemplateParser.r_multiline, remove_newline, line)
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
                        self.lexers[name](parser=self, value=value, top=top, stack=stack)
                    elif name == '=':
                        buf = '\n%s(%s)' % (self.writer, value)
                        top.append(Node(buf, pre_extend=pre_extend))
                    elif name == 'block' and not value.startswith('='):
                        node = BlockNode(name=value.strip(), pre_extend=pre_extend, delimiters=self.delimiters)
                        top.append(node)
                        stack.append(node)
                    elif name == 'end' and not value.startswith('='):
                        self.blocks[top.name] = top
                        stack.pop()
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
                        for k, token in enumerate(tokens):
                            token = tokens[k] = token.strip()
                            len_parsed += len(token)
                            if token.startswith('='):
                                if token.endswith('\\'):
                                    continuation = True
                                    tokens[k] = '\n%s(%s' % (
                                     self.writer, token[1:].strip())
                                else:
                                    tokens[k] = '\n%s(%s)' % (
                                     self.writer, token[1:].strip())
                            elif continuation:
                                tokens[k] += ')'
                                continuation = False

                        buf = '\n%s' % ('\n').join(tokens)
                        top.append(Node(buf, pre_extend=pre_extend))
                else:
                    buf = '\n%s(%r, escape=False)' % (self.writer, i)
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


def parse_template(filename, path='views/', context=dict(), lexers={}, delimiters=(
 '{{', '}}')):
    """
    filename can be a view filename in the views folder or an input stream
    path is the path of a views folder
    context is a dictionary of symbols used to render the template
    """
    if isinstance(filename, str):
        try:
            fp = open(os.path.join(path, filename), 'rb')
            text = fp.read()
            fp.close()
        except IOError:
            raise RestrictedError(filename, '', 'Unable to find the file')

    else:
        text = filename.read()
    return str(TemplateParser(text, context=context, path=path, lexers=lexers, delimiters=delimiters))


def get_parsed(text):
    """
    Returns the indented python code of text. Useful for unit testing.

    """
    return str(TemplateParser(text))


class DummyResponse():

    def __init__(self):
        self.body = StringIO.StringIO()

    def write(self, data, escape=True):
        if not escape:
            self.body.write(str(data))
        elif hasattr(data, 'xml') and callable(data.xml):
            self.body.write(data.xml())
        else:
            if not isinstance(data, (str, unicode)):
                data = str(data)
            elif isinstance(data, unicode):
                data = data.encode('utf8', 'xmlcharrefreplace')
            data = cgi.escape(data, True).replace("'", '&#x27;')
            self.body.write(data)


class NOESCAPE():
    """
    A little helper to avoid escaping.
    """

    def __init__(self, text):
        self.text = text

    def xml(self):
        return self.text


def render(content='hello world', stream=None, filename=None, path=None, context={}, lexers={}, delimiters=(
 '{{', '}}'), writer='response.write'):
    r"""
    >>> render()
    'hello world'
    >>> render(content='abc')
    'abc'
    >>> render(content='abc'')
    "abc'"
    >>> render(content='a"'bc')
    'a"\'bc'
    >>> render(content='a\nbc')
    'a\nbc'
    >>> render(content='a"bcd"e')
    'a"bcd"e'
    >>> render(content="'''a\nc'''")
    "'''a\nc'''"
    >>> render(content="'''a\'c'''")
    "'''a'c'''"
    >>> render(content='{{for i in range(a):}}{{=i}}<br />{{pass}}', context=dict(a=5))
    '0<br />1<br />2<br />3<br />4<br />'
    >>> render(content='{%for i in range(a):%}{%=i%}<br />{%pass%}', context=dict(a=5),delimiters=('{%','%}'))
    '0<br />1<br />2<br />3<br />4<br />'
    >>> render(content="{{='''hello\nworld'''}}")
    'hello\nworld'
    >>> render(content='{{for i in range(3):\n=i\npass}}')
    '012'
    """
    try:
        from globals import Response
    except ImportError:
        Response = DummyResponse
        if 'NOESCAPE' not in context:
            context['NOESCAPE'] = NOESCAPE

    if context and 'response' in context:
        old_response_body = context['response'].body
        context['response'].body = StringIO.StringIO()
    else:
        old_response_body = None
        context['response'] = Response()
    if not content and not stream and not filename:
        raise SyntaxError('Must specify a stream or filename or content')
    close_stream = False
    if not stream:
        if filename:
            stream = open(filename, 'rb')
            close_stream = True
        elif content:
            stream = StringIO.StringIO(content)
    code = str(TemplateParser(stream.read(), context=context, path=path, lexers=lexers, delimiters=delimiters, writer=writer))
    try:
        exec code in context
    except Exception:
        raise

    if close_stream:
        stream.close()
    text = context['response'].body.getvalue()
    if old_response_body is not None:
        context['response'].body = old_response_body
    return text


if __name__ == '__main__':
    import doctest
    doctest.testmod()