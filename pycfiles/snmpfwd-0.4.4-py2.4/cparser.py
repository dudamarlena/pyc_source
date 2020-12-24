# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpfwd/cparser.py
# Compiled at: 2018-12-30 12:01:29
import sys, re
from snmpfwd import error
from pysnmp.proto.rfc1902 import OctetString
SYMBOL_OPTION = ':'
SYMBOL_SECTION_BEGIN = '{'
SYMBOL_SECTION_END = '}'
SYMBOL_WORD = ''

class Scanner(object):
    __module__ = __name__

    def __init__(self):
        self.lines = None
        self.tokens = []
        self.index = 0
        self.length = 0
        return

    def load(self, filename):
        try:
            self.lines = open(filename).readlines()
        except OSError:
            raise error.SnmpfwdError('cant open config file %s: %s' % (filename, sys.exc_info()[1]))

        self.tokens = []
        while self.lines:
            line = self.lines.pop(0)
            if line and line[0] == '#':
                continue
            tokens = re.findall('(?:[^\\s,"]|"(?:\\\\.|[^"])*")+', line)
            for i in range(len(tokens)):
                if tokens[i] and tokens[i][0] == '"' and tokens[i][(-1)] == '"':
                    tokens[i] = tokens[i][1:-1]

            if not tokens or not tokens[0] or tokens[0][0] == '#':
                continue
            for token in tokens:
                if token and token[(-1)] == SYMBOL_OPTION:
                    symbol = SYMBOL_OPTION
                    token = token[:-1]
                elif token == '{':
                    symbol = SYMBOL_SECTION_BEGIN
                elif token == '}':
                    symbol = SYMBOL_SECTION_END
                else:
                    symbol = SYMBOL_WORD
                self.tokens.append((token, symbol))

        self.index = 0
        self.length = len(self.tokens)
        return self

    def get_token(self):
        if self.index >= self.length:
            raise error.EofError()
        self.index += 1
        return self.tokens[(self.index - 1)]

    def unget_token(self):
        if not self.index:
            raise error.SnmpfwdError('%s nothing to unget' % self)
        self.index -= 1


class Parser(object):
    """The parser class implements config file syntactic analysing. Its
       output is an almost AST. Config file syntax is as follows:
   
       <object-name>
       {
           [attribute-name: [attribute-value]
           ...
       }
    """
    __module__ = __name__

    def __init__(self, scanner):
        self.scanner = scanner

    def load_section(self):
        obj = {'_name': '', '_children': []}
        state = 'FSM_START'
        while 1:
            if state == 'FSM_START':
                try:
                    (token, symbol) = self.scanner.get_token()
                except error.EofError:
                    state = 'FSM_STOP'
                    continue
                else:
                    self.scanner.unget_token()
                    if symbol == SYMBOL_SECTION_END:
                        state = 'FSM_SECTION_END'
                    elif symbol == SYMBOL_OPTION:
                        state = 'FSM_OPTION_NAME'
                    else:
                        state = 'FSM_SECTION_NAME'
            elif state == 'FSM_SECTION_NAME':
                self.scanner.get_token()
                self.scanner.unget_token()
                state = 'FSM_SECTION_BEGIN'
            elif state == 'FSM_SECTION_BEGIN':
                self.scanner.get_token()
                (token, symbol) = self.scanner.get_token()
                self.scanner.unget_token()
                self.scanner.unget_token()
                if symbol != SYMBOL_SECTION_BEGIN:
                    raise error.SnmpfwdError('%s missing object beginning sign: %s' % (self, token))
                state = 'FSM_CHILD_BEGIN'
            elif state == 'FSM_CHILD_BEGIN':
                (name, symbol) = self.scanner.get_token()
                self.scanner.get_token()
                child_object = self.load_section()
                child_object['_name'] = name
                obj['_children'].append(child_object)
                state = 'FSM_CHILD_END'
            elif state == 'FSM_CHILD_END':
                (token, symbol) = self.scanner.get_token()
                if symbol != SYMBOL_SECTION_END:
                    raise error.SnmpfwdError('%s missing object closure sign: %s' % (self, token))
                state = 'FSM_START'
            elif state == 'FSM_SECTION_END':
                (token, symbol) = self.scanner.get_token()
                self.scanner.unget_token()
                if symbol != SYMBOL_SECTION_END:
                    raise error.SnmpfwdError('%s missing object closure sign: %s' % (self, token))
                state = 'FSM_STOP'
            elif state == 'FSM_OPTION_NAME':
                (token, symbol) = self.scanner.get_token()
                if token in obj:
                    raise error.SnmpfwdError('%s multiple option occurrence: %s' % (self, token))
                obj[token] = []
                self.scanner.unget_token()
                state = 'FSM_OPTION_VALUE'
            elif state == 'FSM_OPTION_VALUE':
                (option, symbol) = self.scanner.get_token()
                while 1:
                    try:
                        (token, symbol) = self.scanner.get_token()
                    except error.EofError:
                        state = 'FSM_STOP'
                        break

                    if symbol != SYMBOL_WORD:
                        self.scanner.unget_token()
                        if symbol == SYMBOL_SECTION_BEGIN:
                            self.scanner.unget_token()
                            del obj[option][-1]
                        state = 'FSM_START'
                        break
                    if token.lower()[:2] == '0x':
                        token = str(OctetString(hexValue=token[2:]))
                    obj[option].append(token)

            elif state == 'FSM_STOP':
                return obj
            else:
                raise error.SnmpfwdError('%s unknown FSM state: %s' % (self, state))

    def parse(self):
        try:
            return self.load_section()
        except error.EofError:
            raise error.SnmpfwdError('%s premature EOF while reading config file' % self)


class Config(object):
    __module__ = __name__

    def __init__(self):
        self.objects = {}

    def load(self, filename):
        self.objects = Parser(Scanner().load(filename)).parse()
        return self

    def traverse(self, objects, nodes):
        """Return the leaf object resulted by traversing config
           objects tree by nodes
        """
        for obj in objects:
            if obj['_name'] == nodes[0]:
                if len(nodes) == 1:
                    return obj
                r = self.traverse(obj['_children'], nodes[1:])
                if r is None:
                    return obj
                else:
                    return r

        return

    def getPathsToAttr(self, attr, objects=None, nodes=None, paths=None):
        if objects is None:
            objects = self.objects
        if nodes is None:
            nodes = ()
        if paths is None:
            paths = []
        nodes += (objects['_name'],)
        if attr in objects:
            paths.append(nodes)
        for _objs in objects['_children']:
            self.getPathsToAttr(attr, _objs, nodes, paths)

        return paths

    def getAttrValue(self, attr, *nodes, **kwargs):
        scope = nodes
        while scope:
            obj = self.traverse([self.objects], scope)
            if obj and attr in obj:
                expect = kwargs.get('expect')
                if 'vector' in kwargs:
                    if expect:
                        try:
                            return [ expect(x) for x in obj[attr] ]
                        except Exception:
                            raise error.SnmpfwdError('%s value casting error at scope "%s" attribute "%s"' % (self, ('.').join(nodes), attr))

                    else:
                        return obj[attr]
                elif obj[attr]:
                    if expect:
                        try:
                            return expect(obj[attr][0])
                        except Exception:
                            raise error.SnmpfwdError('%s value casting error at scope "%s" attribute "%s"' % (self, ('.').join(nodes), attr))

                    else:
                        return obj[attr][0]
                else:
                    return ''
            scope = scope[:-1]

        if 'default' in kwargs:
            return kwargs['default']
        else:
            raise error.SnmpfwdError('%s non-existing attribute "%s" at scope "%s"' % (self, attr, ('.').join(nodes)))