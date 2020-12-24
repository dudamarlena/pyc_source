# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pumpkin/router.py
# Compiled at: 2014-12-13 05:07:25
import sys, re, pumpkin
if sys.version < '3':
    from urlparse import parse_qs
else:
    from urllib.parse import parse_qs

class RouterException(Exception):
    pass


class Router(object):
    """Router object for request routing.
    """

    def __init__(self):
        self.rules = {}
        self.url_pattern = re.compile(' (?P<static>([:\\\\/\\w\\d]*)\\.(\\w+)) #static\n                |\n                (?P<prefix>(/\\w*)+)(?P<suffix><(?P<type>\\w*)?:(?P<arg>\\w*)>)?\n            ', re.VERBOSE)
        self.methods = {}
        self.methods.setdefault('GET', [])
        self.methods.setdefault('POST', [])
        self.methods.setdefault('DELETE', [])
        self.methods.setdefault('PUT', [])

    def register(self, path, fn, methods):
        if not callable(fn):
            raise RouterException('Router only accept callable object.')
        for m in methods:
            self.methods[m].append(fn)

        g = self.url_pattern.match(path)
        if not g:
            raise RouterException('Router rules : %s can not be accepted.' % path)
        p = g.group('prefix')
        if g.group('suffix'):
            assert g.group('type') == 'int', g.group('type')
            p += '(?P<args>\\d+$)'
            self.rules[(re.compile(p), g.group('arg'))] = fn
        else:
            self.rules[p] = fn

    def __call__(self, p, method='GET'):
        return self.get(p, method)

    def get(self, path, method='GET'):
        try:
            f, args = self._match_path(path)
        except TypeError:
            return

        if not f:
            return
        else:
            method = method.upper()
            if self.methods.get(method) is None:
                raise RouterException('Request method %s not allowed in this app.' % method)
            return (
             f, args)

    def _match_path(self, p):
        for k in self.rules:
            if isinstance(k, str):
                if k == p:
                    return (self.rules[k], None)
            elif isinstance(k[0], type(re.compile('dummy'))):
                _g = k[0].match(p)
                if _g:
                    return (self.rules[k], {k[1]: _g.group('args')})

        return

    def url_for(self, fn, **kwargs):
        if not callable(object):
            raise RouterException('router url_for method only accept callable object.')
        for k, v in self.rules.items():
            if v == fn:
                if isinstance(k, tuple):
                    if not kwargs:
                        raise RouterException('need a argument.')
                    return k[0].pattern.replace('(?P<args>\\d+$)', str(kwargs[k[1]]))
                return k

        raise RouterException("callable object doesn't matched any routing rule.")

    def all_callables(self):
        return self.rules.values()