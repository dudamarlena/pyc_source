# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/hid/cparser.py
# Compiled at: 2010-09-10 09:00:00
from ctypes import *
import re
TOKENS = re.compile('[\\w_]+|[()*,]')
WORD = re.compile('^[_\\w]+$')
_keywords = set()
_types = {}

def define(name, t):
    if isinstance(t, basestring):
        t = _parse_type(t)
    _types[name] = t
    for token in re.findall('\\w+', name):
        _keywords.add(token)

    return t


define('void', None)
define('void*', c_void_p)
define('char', c_char)
define('wchar_t', c_wchar)
define('unsigned char', c_ubyte)
define('short', c_short)
define('unsigned short', c_ushort)
define('int', c_int)
define('unsigned int', c_uint)
define('long', c_long)
define('unsigned long', c_ulong)
define('long long', c_longlong)
define('unsigned long long', c_ulonglong)
define('float', c_float)
define('double', c_double)
define('char*', c_char_p)
define('wchar_t*', c_wchar_p)

def _parse_type(type_str):
    if _types.has_key(type_str):
        return _types[type_str]
    if type_str.endswith('*'):
        type_str = type_str[:-1]
        return POINTER(_parse_type(type_str))
    else:
        raise ValueError('unknown type: ' + type_str)


class tokenizer(object):

    def __init__(self, s):
        self.s = s
        tokens = TOKENS.findall(s)
        self.tokens = []
        k = []
        for t in tokens:
            if t in _keywords:
                k.append(t)
            else:
                if len(k) > 0:
                    self.tokens.append((' ').join(k))
                    k = []
                self.tokens.append(t)

        if len(k) > 0:
            self.tokens.append((' ').join(k))
        self.i = -1

    def next(self):
        if self.empty():
            raise ValueError('no more tokens found parsing - %s' % self.s)
        self.i += 1
        return self.current()

    def current(self):
        return self.tokens[self.i]

    def push_back(self):
        if self.i < 0:
            raise ValueError('pushed back too far parsing - %s' % self.s)
        self.i -= 1

    def empty(self):
        return self.i >= len(self.tokens) - 1


class c_type(object):

    def __init__(self, type_name, name=''):
        self.type_name = type_name
        self.name = name

    @property
    def ctype(self):
        return _parse_type(self.type_name)

    @property
    def cstruct(self):
        """convert the type for use in a struct"""
        return (
         self.name, self.ctype)

    def cast(self, value):
        return cast(value, self.ctype)

    def __repr__(self):
        if self.name:
            return 'c_type(%s %s)' % (self.type_str, self.name)
        return 'c_type(%s)' % self.type_str


class c_function(object):

    def __init__(self, return_type, name, param_list):
        self.return_type = return_type
        self.name = name
        self.param_list = param_list

    @property
    def ctype(self):
        params = [ p.ctype for p in self.param_list ]
        return CFUNCTYPE(self.return_type.ctype, *params)

    @property
    def cstruct(self):
        """convert the type for use in a struct"""
        return (
         self.name, self.ctype)

    def from_lib(self, lib):
        fn = getattr(lib, self.name)
        fn.restype = self.return_type.ctype
        fn.argtypes = [ p.ctype for p in self.param_list ]
        return fn

    def __repr__(self):
        return 'c_function(%s %s %s)' % (self.return_type, self.name, self.param_list)


def parse_type(t):
    base_type = t.next()
    while not t.empty():
        if t.next() == '*':
            base_type += '*'
        else:
            t.push_back()
            break

    return c_type(base_type)


def parse_fn_name(t):
    if t.next() == '(':
        assert t.next() == '*'
        name = t.next()
        assert t.next() == ')'
    else:
        name = t.current()
    return name


def parse_param(t):
    param_type = parse_type(t)
    name = t.next()
    if WORD.match(name):
        param_type.name = name
    else:
        t.push_back()
    return param_type


def parse_param_list(t):
    assert t.next() == '('
    params = []
    while t.next() != ')':
        t.push_back()
        params.append(parse_param(t))
        if t.next() != ',':
            break

    assert t.current() == ')'
    return params


def parse(s):
    """
    parse a c definition/declaration returning a variable def, function def etc
    as appropriate
    """
    t = tokenizer(s)
    def_type = parse_type(t)
    if not t.empty():
        if t.next() == '(':
            t.push_back()
            fn_name = parse_fn_name(t)
            param_list = parse_param_list(t)
            if not t.empty():
                raise ValueError('unexpected tokens at end of function def in - %s' % s)
            return c_function(def_type, fn_name, param_list)
        else:
            t.push_back()
            name = t.next()
            if not t.empty():
                if t.next() == '(':
                    t.push_back()
                    param_list = parse_param_list(t)
                    if not t.empty():
                        raise ValueError('unexpected tokens at end of function def in - %s' % s)
                    return c_function(def_type, name, param_list)
            if not t.empty():
                raise ValueError('unexpected tokens at end of variable def in - %s' % s)
            def_type.name = name
            return def_type
    else:
        return def_type


__all__ = [
 'parse', 'define']