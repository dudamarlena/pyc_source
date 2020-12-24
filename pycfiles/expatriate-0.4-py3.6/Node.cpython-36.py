# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\Node.py
# Compiled at: 2018-01-18 12:34:40
# Size of source mod 2**32: 21710 bytes
import logging, math, re
from .exceptions import *
from .xpath import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Node(object):
    __doc__ = '\n    Class representing a XML node\n\n    :param parent: Parent node of this node\n    :type parent: expatriate.Parent or None\n\n    '

    def __init__(self, parent=None):
        self._parent = parent

    @property
    def parent(self):
        """
        The Parent of this Node.

        :getter: Returns the parent Node
        :setter: Sets the parent Node
        :type: expatriate.Parent or None
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def prefix_to_namespace(self, prefix):
        """
        Resolve the given prefix into the namespace URI it represents.

        :param str prefix: The prefix to resolve.
        """
        if prefix == 'xmlns':
            return 'http://www.w3.org/2000/xmlns/'
        else:
            if prefix == 'xml':
                return 'http://www.w3.org/XML/1998/namespace'
            if isinstance(self._parent, Node):
                return self._parent.prefix_to_namespace(prefix)
        raise UnknownPrefixException('Unknown prefix: ' + str(prefix))

    def namespace_to_prefix(self, namespace_uri):
        """
        Resolve the given namespace URI into the prefix it is represented by.

        :param str namespace: The namespace to resolve.
        """
        if namespace_uri == 'http://www.w3.org/2000/xmlns/':
            return 'xmlns'
        else:
            if namespace_uri == 'http://www.w3.org/XML/1998/namespace':
                return 'xml'
            if isinstance(self._parent, Node):
                return self._parent.namespace_to_prefix(namespace_uri)
        raise UnknownNamespaceException('Unknown namespace uri: ' + str(namespace_uri))

    def _tokenize(self, expr):
        tokens = []
        parens = 0
        braces = 0
        t = ''
        for i, char in enumerate(expr):
            if len(t) > 0:
                if t[0] in '\'"':
                    t += char
                    if char == t[0]:
                        if t[(-1)] != '\\':
                            tokens.append(t)
                            t = ''
                else:
                    if t == '-':
                        tokens.append(t)
                        t = char
                    else:
                        if t == '.':
                            if char != '.':
                                tokens.extend(['self', '::', 'node', '(', ')'])
                                t = char
                        if re.fullmatch('[0-9][0-9.]*', t):
                            if char.isdigit() or char == '.':
                                t += char
                        if t[0] == '$' and char.isalpha():
                            t += char
                        else:
                            if t.isspace():
                                t = char
                            else:
                                if t in ':/.!<>':
                                    if t + char in ('::', '//', '..', '!=', '<=', '>='):
                                        t += char
                                        if t == '//':
                                            tokens.extend(['/', 'descendant-or-self', '::', 'node', '(', ')', '/'])
                                        else:
                                            if t == '..':
                                                tokens.extend(['parent', '::', 'node', '(', ')'])
                                            else:
                                                tokens.append(t)
                                        t = ''
                                    else:
                                        tokens.append(t)
                                        t = char
                                else:
                                    if t == '@':
                                        tokens.extend(['attribute', '::'])
                                        t = char
                                    else:
                                        if t == '(':
                                            tokens.append(t)
                                            t = char
                                            parens += 1
                                        else:
                                            if t == ')':
                                                tokens.append(t)
                                                t = char
                                                parens -= 1
                                            else:
                                                if t == '[':
                                                    tokens.append(t)
                                                    t = char
                                                    braces += 1
                                                else:
                                                    if t == ']':
                                                        tokens.append(t)
                                                        t = char
                                                        braces -= 1
                                                    else:
                                                        if t in ',\'"*|+=':
                                                            tokens.append(t)
                                                            t = char
                                                        else:
                                                            if char.isalnum() or char == '-':
                                                                t += char
                                                            else:
                                                                tokens.append(t)
                                                                t = char
            elif char.isspace():
                pass
            else:
                t += char

        if t == '.':
            tokens.extend(['self', '::', 'node', '(', ')'])
        else:
            if t.isspace():
                pass
            else:
                if t == ')':
                    tokens.append(t)
                    parens -= 1
                else:
                    if t == ']':
                        tokens.append(t)
                        braces -= 1
                    else:
                        if t != '':
                            tokens.append(t)
        if parens != 0 or braces != 0:
            raise XPathSyntaxException('Paren or brace expression not closed')
        return tokens

    def xpath(self, expr, version=1.0, variables={}, add_functions={}):
        """
        Return the nodes matching the given XPath expression (expr).

        :param str expr: XPath expression
        :param version: Version of XPath the expression conforms to
        :type version: float or defaults to 1.0
        :param dict variables: Variables to substitute in the XPath expression
        :param dict add_functions: Functions to use within the XPath expression
        :rtype: list[Node]
        """
        if version != 1.0:
            raise NotImplementedError('Only XPath 1.0 has been implemented')
        if self.get_document() is None:
            raise ValueError("Can't resolve xpath expression on Node not attached to a document")
        logger.debug('********************************************')
        logger.debug('Tokenizing xpath expression: ' + str(expr))
        tokens = self._tokenize(expr)
        logger.debug('Tokens: ' + str(tokens))
        functions = Function.FUNCTIONS.copy()
        functions.update(add_functions)
        stack = []
        for i, token in enumerate(tokens):
            if token == '(':
                e = Expression()
                logger.debug('Starting sub expression ' + str(e))
                stack.append(e)
            elif token == ')':
                if len(stack) <= 1:
                    pass
                else:
                    logger.debug('End of ' + str(stack[(-1)]))
                    if i > 0 and tokens[(i - 1)] == '(':
                        stack.pop()
                        logger.debug('Ignoring empty expression')
                    elif len(stack) > 1:
                        e = stack.pop()
                        logger.debug('Adding ' + str(e) + ' to ' + str(stack[(-1)]))
                        stack[(-1)].children.append(e)
            elif token == '[':
                p = Predicate()
                stack.append(p)
                logger.debug('Starting predicate ' + str(p))
                e = Expression()
                stack.append(e)
                logger.debug('Starting sub expression ' + str(e))
            elif token == ']':
                logger.debug('End of ' + str(stack[(-1)]))
                if i > 0:
                    if tokens[(i - 1)] == '[':
                        stack.pop()
                        stack.pop()
                        logger.debug('Ignoring empty expression & predicate')
                else:
                    while len(stack) > 1 and not isinstance(stack[(-1)], Predicate):
                        i = stack.pop()
                        logger.debug('Adding ' + str(i) + ' to ' + str(stack[(-1)]))
                        stack[(-1)].children.append(i)

                    p = stack.pop()
                    if not isinstance(stack[(-1)], Axis):
                        raise SyntaxException('Expecting Axis on stack before predicate')
                    logger.debug('Adding ' + str(p) + ' to ' + str(stack[(-1)]))
                    stack[(-1)].children.append(p)
            else:
                if token == '::':
                    pass
                elif token == ':':
                    continue
                if token == '*':
                    if i > 0:
                        if tokens[(i - 1)] not in ('::', '(', '[', ',', 'and', 'or',
                                                   'mod', 'div', '*', '/', '//',
                                                   '|', '+', '-', '=', '!=', '<',
                                                   '<=', '>', '>='):
                            o = Operator(token)
                            o.children.append(stack.pop())
                            stack.append(o)
                            logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                    else:
                        if len(stack) == 0 or not isinstance(stack[(-1)], Axis):
                            a = Axis('child')
                            stack.append(a)
                            logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                        nt = AnyNodeTest(stack[(-1)].get_principal_node_type())
                        stack[(-1)].children.append(nt)
                        logger.debug('Adding ' + str(nt) + ' to children of ' + str(stack[(-1)]))
                elif token == ',':
                    try:
                        while not isinstance(stack[(-1)], Function):
                            i = stack.pop()
                            logger.debug('Adding ' + str(i) + ' to children of ' + str(stack[(-1)]))
                            stack[(-1)].children.append(i)

                    except IndexError:
                        raise SyntaxException('Unable to add argument to function')

                    logger.debug('Starting new expression ' + str(e) + ' for function argument')
                    e = Expression()
                    stack.append(e)
                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                elif token[0] in '\'"':
                    l = Literal(token[1:-1])
                    stack.append(l)
                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                elif re.fullmatch('[0-9.]+', token):
                    if '.' in token:
                        l = Literal(float(token))
                    else:
                        l = Literal(int(token))
                    if len(stack) > 0:
                        if isinstance(stack[(-1)], Operator):
                            op = stack.pop()
                            op.children.append(l)
                            logger.debug('Added ' + str(l) + ' to children of ' + str(op))
                            stack.append(op)
                    else:
                        stack.append(l)
                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                elif token == '-' and (len(stack) == 0 or isinstance(stack[(-1)], Operator) or i > 0 and tokens[(i - 1)] in ('(',
                                                                                                                             ',',
                                                                                                                             '[')):
                    o = Operator('negate')
                    stack.append(o)
                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                elif token in Operator.OPERATORS and i > 0 and tokens[(-1)] not in ('::',
                                                                                    '(',
                                                                                    '[',
                                                                                    ',',
                                                                                    'and',
                                                                                    'or',
                                                                                    'mod',
                                                                                    'div',
                                                                                    '*',
                                                                                    '/',
                                                                                    '//',
                                                                                    '|',
                                                                                    '+',
                                                                                    '-',
                                                                                    '=',
                                                                                    '!=',
                                                                                    '<',
                                                                                    '<=',
                                                                                    '>',
                                                                                    '>='):
                    o = Operator(token)
                    o.children.append(stack.pop())
                    stack.append(o)
                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                elif token == '/':
                    if i == 0:
                        s = RootStep(self.get_document())
                    else:
                        while len(stack) > 0 and not isinstance(stack[(-1)], Step):
                            i = stack.pop()
                            if len(stack) > 0:
                                logger.debug('Adding ' + str(i) + ' to children of ' + str(stack[(-1)]))
                                stack[(-1)].children.append(i)

                        if len(stack) == 0 or not isinstance(stack[(-1)], Step):
                            logger.debug('Step is not the last item on the stack')
                            parent_step = Step()
                            logger.debug('Adding ' + str(i) + ' to children of ' + str(parent_step))
                            parent_step.children.append(i)
                            stack.append(parent_step)
                            logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                        s = Step()
                    stack.append(s)
                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                elif token == 'Infinity':
                    stack.append(Literal(math.inf))
                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                else:
                    if token == 'NaN':
                        stack.append(Literal(math.nan))
                        logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                    else:
                        if re.fullmatch('[a-zA-Z0-9_-]+', token):
                            if len(stack) > 0:
                                if isinstance(stack[(-1)], Axis):
                                    if token in TypeNodeTest.NODE_TYPES:
                                        stack[(-1)].children.append(TypeNodeTest(token))
                                        logger.debug('Added ' + str(stack[(-1)].children[(-1)]) + ' to children of ' + str(stack[(-1)]))
                                    elif len(tokens) > i + 1:
                                        if tokens[(i + 1)] == ':':
                                            stack.append(QNameNodeTest(token))
                                            logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                    else:
                                        stack[(-1)].children.append(NCNameNodeTest(token))
                                        logger.debug('Added ' + str(stack[(-1)].children[(-1)]) + ' to children of ' + str(stack[(-1)]))
                            else:
                                if len(tokens) > i + 1:
                                    if tokens[(i + 1)] == '::':
                                        if token not in Axis.AXES:
                                            raise XPathSyntaxException('Unknown axis: ' + str(token))
                                        a = Axis(token)
                                        stack.append(a)
                                        logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                if len(tokens) > i + 1:
                                    if tokens[(i + 1)] == '(':
                                        if token in Function.FUNCTIONS:
                                            f = Function(token, Function.FUNCTIONS[token])
                                            stack.append(f)
                                            logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                        else:
                                            if token in TypeNodeTest.NODE_TYPES:
                                                if len(stack) == 0 or not isinstance(stack[(-1)], Axis):
                                                    stack.append(Axis('child'))
                                                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                                nt = TypeNodeTest(token)
                                                stack[(-1)].children.append(nt)
                                                logger.debug('Added ' + str(nt) + ' to children of ' + str(stack[(-1)]))
                                            else:
                                                raise XPathSyntaxException('Unknown function or node type test: ' + str(token))
                            if token == 'true':
                                stack.append(Literal(True))
                                logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                            else:
                                if token == 'false':
                                    stack.append(Literal(False))
                                    logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                else:
                                    if token in Operator.OPERATORS:
                                        if i > 0:
                                            if tokens[(-1)] not in ('::', '(', '[',
                                                                    ',', 'and', 'or',
                                                                    'mod', 'div',
                                                                    '*', '/', '//',
                                                                    '|', '+', '-',
                                                                    '=', '!=', '<',
                                                                    '<=', '>', '>='):
                                                o = Operator(token)
                                                o.children.append(stack.pop())
                                                stack.append(o)
                                                logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                    if len(tokens) > i + 1:
                                        if tokens[(i + 1)] == ':':
                                            if len(stack) == 0 or not isinstance(stack[(-1)], Axis):
                                                stack.append(Axis('child'))
                                                logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                            nt = QNameNodeTest(token)
                                            stack.append(nt)
                                            logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                    elif i > 0 and tokens[(i - 1)] == ':':
                                        if len(stack) == 0 or not isinstance(stack[(-1)], QNameNodeTest):
                                            raise SyntaxException('Expecting QNameNodeTest on stack; got second half of QName')
                                        nt = stack.pop()
                                        nt.name += ':' + token
                                        if len(stack) == 0 or not isinstance(stack[(-1)], Axis):
                                            raise SyntaxException('Expecting Axis on stack; finished QNameNodeTest')
                                        stack[(-1)].children.append(nt)
                                        logger.debug('Added ' + str(nt) + ' to ' + str(stack[(-1)]))
                                    else:
                                        if len(stack) == 0 or not isinstance(stack[(-1)], Axis):
                                            stack.append(Axis('child'))
                                            logger.debug('Pushed ' + str(stack[(-1)]) + ' on stack')
                                        nt = NCNameNodeTest(token)
                                        stack[(-1)].children.append(nt)
                                        logger.debug('Added ' + str(nt) + ' to children of ' + str(stack[(-1)]))
                        else:
                            raise XPathSyntaxException('Unknown token: ' + str(token))

        while len(stack) > 1:
            i = stack.pop()
            logger.debug('Adding ' + str(i) + ' to children of ' + str(stack[(-1)]))
            stack[(-1)].children.append(i)

        i = stack.pop()
        logger.debug('Final pop off stack got ' + str(i))
        logger.debug('********************************************')
        logger.debug('Evaluating ' + str(i))
        return i.evaluate(self, 1, 1, variables)

    def __str__(self):
        return self.__class__.__name__ + ' ' + hex(id(self))

    def __repr__(self):
        return self.__str__()

    def get_document(self):
        """
        Get this node's enclosing document.

        :rtype: expatriate.Document or None
        """
        from .Document import Document
        n = self
        while n is not None and not isinstance(n, Document):
            n = n._parent

        return n

    def get_type(self):
        """
        Return the type of the node. Overriden by subclasses.

        :rtype: str
        """
        raise NotImplementedError

    def escape(self, text):
        """
        Escape disallowed characters within *text* with their SGML entities.

        :param str text: The text to escape
        :rtype: str
        """
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def unescape(self, text):
        """
        Unescape SGML entities in *text* with their character equivalents.

        :param str text: The text to unescape
        :rtype: str
        """
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text

    def find_by_id(self, ref):
        """
        Find the node referenced by *ref* within this node's children.

        :param str ref: The id attribute of the Node to match
        :rtype: Node or None
        """
        pass

    def get_node_count(self):
        """
        Get the count of this node and any children nodes within.

        :rtype: int
        """
        return 1

    def get_document_order(self):
        """
        Get the index of this Node's order in the enclosing Document.

        :rtype: int
        :raises UnattachedElementException: if the Node is not attached to a Document
        """
        if self._parent is None:
            raise UnattachedElementException('Element ' + str(self) + ' is not attached to a document')
        do = self._parent.get_document_order()
        try:
            do += len(self._parent.namespace_nodes)
        except AttributeError:
            pass

        try:
            do += len(self._parent.attribute_nodes)
        except AttributeError:
            pass

        for c in self._parent.children:
            if c == self:
                return do
            do += c.get_node_count()

        raise ValueError('Unable to find node ' + str(self) + ' in ' + str(self._parent) + ' children')