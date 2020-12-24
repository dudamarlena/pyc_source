# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/urlson.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 6394 bytes
"""
This module is used to parse JSON-like objects from the URL into a python
structure of dicts and lists.

Be aware that all values will be strings, so parse anything that you expect
to be something else, e.g. an int.

>>> loads_dict(request.GET)
"""
import re
from spynl.main.locale import SpynlTranslationString as _
WS = re.compile('\\s+')
KEY = re.compile('([^:]*)')
LITERALS = {'object': re.compile('([^,\\}]*)'), 
 'array': re.compile('([^,\\]]*)')}

def loads_dict(dictionary):
    """
    Read in a dict, parse each value into a python structure
    """
    result = []
    for k, v in dictionary.items():
        try:
            v = loads(v)
        except UnexpectedEndOfInput as e:
            extra = ' when processing argument "{}".'.format(k)
            e.args = (e.args[0][:-1] + extra,) + e.args[1:]
            raise

        result.append((k, v))

    return dict(result)


def loads(urlson):
    """
    This method runs the parser on any string and returns its collected
    end-product. We call the string we work on "urlson" throughout.
    """
    parser = Parser()
    value_ctx(urlson, parser)
    return parser.value


class Parser:
    __doc__ = '\n    This parser uses a stack of lists and dicts to model the object structure\n    we find. The functions value_ctx, array_ctx and object_ctx call this object\n    whenever they ancounter a meaningful event.\n    '

    def __init__(self):
        """initialise parser"""
        self.stack = [[{}, 'value']]

    def __call__(self, event, token):
        """call parser"""
        stack = self.stack
        top = stack[(-1)]
        value = top[0]
        if event == 'object_start':
            stack.append([{}, None])
        else:
            if event == 'array_start':
                stack.append([[], None])
            else:
                if event == 'key':
                    top[1] = token
                else:
                    if event == 'literal':
                        if isinstance(value, list):
                            value.append(token)
                        elif isinstance(value, dict):
                            dict_key = top[1]
                            value[dict_key] = token
                    elif event in ('object_stop', 'array_stop'):
                        parent_value = stack[(-2)][0]
        if isinstance(parent_value, list):
            parent_value.append(value)
        else:
            if isinstance(parent_value, dict):
                parent_key = stack[(-2)][1]
                parent_value[parent_key] = value
            stack.pop()

    @property
    def value(self):
        """return value"""
        return self.stack[0][0]['value']


class InvalidToken(ValueError):
    __doc__ = 'Exception if token was invalid'

    def __init__(self, urlson, offset):
        """initialise Token Error"""
        super().__init__()
        self.urlson = urlson
        self.offset = offset

    def __str__(self):
        """str representation of this Error"""
        context = self.urlson[self.offset:self.offset + 10]
        return 'Invalid token at offset ${offset}: ${context}...'.format({'offset': self.offset, 'context': context})


class UnexpectedEndOfInput(ValueError):
    __doc__ = 'Exeption if end of input was reached'

    def __init__(self):
        """initialize"""
        super().__init__(_('unexpected-end-of-input', default='Unexpected end of input.'))


def handle_ws(urlson, offset=0):
    """return index of next non-whitespace character"""
    result = re.match(WS, urlson[offset:])
    if result:
        offset += result.end()
    return offset


def value_ctx(urlson, cb, offset=0, ctx=None):
    """
    This function parses a value of the GET string in.
    It tells the parser about literals or, alternatively, if objects or arrays
    are detected, it calls the appropriate parsing methods (array_ctx,
    object_ctx), who tell the parser what they found (they, in turn, do the
    same and also call value_ctx if they find something new which needs to be
    defined here).
    """
    if not ctx:
        ctx = [
         'root']
    ctx.append('value')
    offset = handle_ws(urlson, offset)
    if offset == len(urlson):
        cb('literal', '')
    else:
        if urlson[offset] == '{':
            offset = object_ctx(urlson, cb, offset, ctx)
        else:
            if urlson[offset] == '[':
                offset = array_ctx(urlson, cb, offset, ctx)
            else:
                if ctx[(-2)] == 'root':
                    cb('literal', urlson[offset:].strip())
                    offset = len(urlson)
                else:
                    if ctx[(-2)] in ('array', 'object'):
                        expr = LITERALS[ctx[(-2)]]
                        result = re.match(expr, urlson[offset:])
                        if result:
                            cb('literal', result.groups()[0].strip())
                            offset += result.end()
                        else:
                            cb('literal', '')
                    else:
                        raise InvalidToken(urlson, offset)
    ctx.pop()
    return offset


def array_ctx(urlson, cb, offset=0, ctx=None):
    """parse an Array"""
    if not ctx:
        ctx = [
         'root']
    ctx.append('array')
    offset += 1
    cb('array_start', None)
    while True:
        offset = handle_ws(urlson, offset)
        if offset == len(urlson):
            raise UnexpectedEndOfInput()
        if urlson[offset] == ']':
            offset += 1
            break
        else:
            if urlson[offset] == ',':
                offset += 1
            else:
                offset = value_ctx(urlson, cb, offset, ctx)

    cb('array_stop', None)
    ctx.pop()
    return offset


def object_ctx(urlson, cb, offset=0, ctx=None):
    """parse an object"""
    if not ctx:
        ctx = [
         'root']
    ctx.append('object')
    offset += 1
    cb('object_start', None)
    while True:
        offset = handle_ws(urlson, offset)
        if offset == len(urlson):
            raise UnexpectedEndOfInput()
        else:
            if urlson[offset] == '}':
                offset += 1
                break
            else:
                if urlson[offset] == ',':
                    offset += 1
                else:
                    result = re.match(KEY, urlson[offset:])
                    if result:
                        offset += result.end()
                        cb('key', result.groups()[0].strip())
                        if offset == len(urlson):
                            raise UnexpectedEndOfInput()
                        offset += 1
                        offset = value_ctx(urlson, cb, offset, ctx)
                    else:
                        raise InvalidToken(urlson, offset)

    cb('object_stop', None)
    ctx.pop()
    return offset